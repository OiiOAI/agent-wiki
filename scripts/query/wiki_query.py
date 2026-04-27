"""Zero-LLM Python helper for querying the wiki.

Designed for downstream agents (Claude / GPT / Cursor / custom) that
want structured access to wiki pages without re-implementing the
frontmatter parser. No network, no embeddings, no LLM calls — pure
filesystem reads + YAML parsing.

If `wiki/AGENTS_INDEX.json` exists (regenerated on every batch commit
via `scripts/ingest/commit_batch._rebuild_agents_index`), lookups go
through it for O(1) slug/alias resolution. Otherwise we walk the
filesystem on first call and cache results in-memory for the duration
of the process.

Public API:

    list_pages(type=None) -> list[PageStub]
    find_page(query, type=None) -> Page | None
    read_page(slug, type=None) -> Page
    search(query, fields=("title","summary","key_facts"), limit=20) -> list[Match]
    neighbors(slug, depth=1) -> list[Page]
    provenance_for(slug) -> list[str]

Everything returns dataclasses defined here; nothing leaks pyyaml types.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
WIKI_ROOT = REPO_ROOT / "wiki"
AGENTS_INDEX_PATH = WIKI_ROOT / "AGENTS_INDEX.json"

PAGE_TYPE_DIRS = ("entities", "concepts", "topics", "sources", "analyses",
                  "conflicts", "dashboards")

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
_SECTION_RE = re.compile(r"^## .+$", re.MULTILINE)
_WIKILINK_RE = re.compile(r"\[\[([^\[\]]+)\]\]")
_PROVENANCE_RE = re.compile(
    r"\[raw/[^\n]+?\.(?:pdf|epub|md|txt)"
    r"(?:#(?:p\d+(?:-p?\d+)?|L\d+(?:-L?\d+)?))?\]"
)


# ----- data classes --------------------------------------------------


@dataclass
class Fact:
    """One bullet from `## Key facts`, parsed into claim + provenance."""
    claim: str
    provenance: str  # the [raw/.../#anchor] string, or "" if missing


@dataclass
class PageStub:
    """Lightweight metadata used by list_pages / search results."""
    slug: str
    title: str
    type: str
    path: str        # repo-relative
    summary: str = ""
    tags: list[str] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)


@dataclass
class Page:
    """Full parsed page: frontmatter + structured body."""
    slug: str
    title: str
    type: str
    path: Path
    frontmatter: dict
    sections: dict[str, str]   # "## Summary" -> body text
    aliases: list[str]
    tags: list[str]
    related: dict[str, list[str]]
    key_facts: list[Fact]

    @property
    def summary(self) -> str:
        return self.sections.get("## Summary", "").strip()

    @property
    def inferences(self) -> list[str]:
        body = self.sections.get("## Inferences", "")
        return [
            line.lstrip("- ").strip()
            for line in body.splitlines()
            if line.strip().startswith("- ")
        ]

    @property
    def uncertainties(self) -> list[str]:
        body = self.sections.get("## Uncertainties", "")
        return [
            line.lstrip("- ").strip()
            for line in body.splitlines()
            if line.strip().startswith("- ")
        ]


@dataclass
class Match:
    """One search result: which page matched, on what field, with a snippet."""
    slug: str
    title: str
    type: str
    path: str
    score: int           # higher = better; bounded by sum of weights
    field_hits: list[str]   # which fields contributed
    snippet: str         # short excerpt around the hit


# ----- low-level parsing ---------------------------------------------


_PAGE_CACHE: dict[Path, Page] = {}


def _parse_page_text(text: str, path: Path) -> Page:
    fm_match = _FRONTMATTER_RE.match(text)
    if fm_match:
        try:
            fm = yaml.safe_load(fm_match.group(1)) or {}
        except yaml.YAMLError:
            fm = {}
        body = text[fm_match.end():]
    else:
        fm = {}
        body = text

    # Strip leading "# Title" from body before sectioning so it doesn't
    # land in an empty unnamed section.
    if body.lstrip().startswith("# "):
        nl = body.find("\n", body.find("# "))
        body = body[nl + 1:] if nl != -1 else ""

    # Walk sections by ## headers. Use finditer to get start/end ranges.
    headers = list(_SECTION_RE.finditer(body))
    sections: dict[str, str] = {}
    for i, m in enumerate(headers):
        header = m.group(0).strip()
        start = m.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(body)
        sections[header] = body[start:end].strip("\n")

    # Parse key_facts bullets into (claim, provenance)
    key_facts: list[Fact] = []
    for line in sections.get("## Key facts", "").splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        bullet = line[2:].strip()
        m = _PROVENANCE_RE.search(bullet)
        if m:
            prov = m.group(0)
            claim = bullet[: m.start()].rstrip(" .;,")
        else:
            prov = ""
            claim = bullet
        key_facts.append(Fact(claim=claim.strip(), provenance=prov))

    return Page(
        slug=path.stem,
        title=str(fm.get("title") or path.stem),
        type=str(fm.get("type") or path.parent.name.rstrip("s")),
        path=path,
        frontmatter=fm,
        sections=sections,
        aliases=[str(a) for a in (fm.get("aliases") or [])],
        tags=[str(t) for t in (fm.get("tags") or [])],
        related={k: [str(s) for s in v]
                 for k, v in (fm.get("related") or {}).items()
                 if isinstance(v, list)},
        key_facts=key_facts,
    )


def _read_page_file(path: Path) -> Page:
    if path in _PAGE_CACHE:
        return _PAGE_CACHE[path]
    page = _parse_page_text(path.read_text(encoding="utf-8"), path)
    _PAGE_CACHE[path] = page
    return page


# ----- index loading -------------------------------------------------


@dataclass
class _Index:
    pages: list[PageStub]
    by_slug: dict[str, int]
    by_alias: dict[str, str]   # alias_lower -> slug
    by_title: dict[str, str]   # title_lower -> slug


_INDEX_CACHE: _Index | None = None


def _load_index(force_filesystem: bool = False) -> _Index:
    global _INDEX_CACHE
    if _INDEX_CACHE is not None:
        return _INDEX_CACHE

    if not force_filesystem and AGENTS_INDEX_PATH.exists():
        try:
            data = json.loads(AGENTS_INDEX_PATH.read_text(encoding="utf-8"))
            stubs = [
                PageStub(
                    slug=p["slug"],
                    title=p["title"],
                    type=p["type"],
                    path=p["path"],
                    summary=p.get("summary", ""),
                    tags=p.get("tags", []) or [],
                    aliases=p.get("aliases", []) or [],
                )
                for p in data["pages"]
            ]
            by_slug = {s.slug: i for i, s in enumerate(stubs)}
            by_alias = {a.lower(): s.slug for s in stubs for a in s.aliases}
            by_title = {s.title.lower(): s.slug for s in stubs}
            _INDEX_CACHE = _Index(stubs, by_slug, by_alias, by_title)
            return _INDEX_CACHE
        except (json.JSONDecodeError, KeyError, OSError):
            pass  # fall through to filesystem walk

    stubs: list[PageStub] = []
    for sub in PAGE_TYPE_DIRS:
        d = WIKI_ROOT / sub
        if not d.is_dir():
            continue
        for md in sorted(d.glob("*.md")):
            try:
                page = _read_page_file(md)
            except Exception:
                continue
            stubs.append(PageStub(
                slug=page.slug,
                title=page.title,
                type=page.type,
                path=str(md.relative_to(REPO_ROOT)),
                summary=page.summary[:240],
                tags=page.tags,
                aliases=page.aliases,
            ))
    by_slug = {s.slug: i for i, s in enumerate(stubs)}
    by_alias = {a.lower(): s.slug for s in stubs for a in s.aliases}
    by_title = {s.title.lower(): s.slug for s in stubs}
    _INDEX_CACHE = _Index(stubs, by_slug, by_alias, by_title)
    return _INDEX_CACHE


def _reset_caches() -> None:
    """For tests: forget any cached index/pages so the next call rescans."""
    global _INDEX_CACHE
    _INDEX_CACHE = None
    _PAGE_CACHE.clear()


# ----- public API ----------------------------------------------------


def list_pages(type: str | None = None) -> list[PageStub]:
    """Return every page (optionally filtered to one type)."""
    idx = _load_index()
    if type is None:
        return list(idx.pages)
    return [p for p in idx.pages if p.type == type]


def find_page(query: str, type: str | None = None) -> Page | None:
    """Resolve a slug, title, or alias (case-insensitive) to a Page.

    Search order: exact slug → exact title → exact alias → kebab-cased
    title. Returns None if nothing matches.
    """
    idx = _load_index()
    q = query.strip()
    q_lower = q.lower()

    candidate_slug: str | None = None
    if q in idx.by_slug:
        candidate_slug = q
    elif q_lower in idx.by_title:
        candidate_slug = idx.by_title[q_lower]
    elif q_lower in idx.by_alias:
        candidate_slug = idx.by_alias[q_lower]
    else:
        kebab = re.sub(r"\s+", "-", q_lower).strip("-")
        if kebab in idx.by_slug:
            candidate_slug = kebab

    if candidate_slug is None:
        return None
    stub = idx.pages[idx.by_slug[candidate_slug]]
    if type and stub.type != type:
        return None
    return _read_page_file(REPO_ROOT / stub.path)


def read_page(slug: str, type: str | None = None) -> Page:
    """Like find_page but raises KeyError if not found."""
    page = find_page(slug, type=type)
    if page is None:
        raise KeyError(f"no wiki page for {slug!r} (type={type!r})")
    return page


# Field weights for search() — tuned by gut feel, expose as kwarg.
_DEFAULT_FIELD_WEIGHTS = {
    "title": 8,
    "aliases": 6,
    "summary": 3,
    "key_facts": 2,
    "tags": 1,
}


def search(
    query: str,
    fields: tuple[str, ...] = ("title", "summary", "key_facts"),
    limit: int = 20,
    weights: dict[str, int] | None = None,
) -> list[Match]:
    """Substring search across the chosen frontmatter/body fields.

    Multi-word queries split on whitespace and require **every** term
    to hit somewhere on the page (AND semantics). Ranking is
    `sum(weight[field] for field in hit_fields)` — title + alias hits
    dominate. Case-insensitive. Returns up to `limit` matches sorted
    by descending score.
    """
    weights = {**_DEFAULT_FIELD_WEIGHTS, **(weights or {})}
    q_full = query.lower().strip()
    if not q_full:
        return []
    terms = q_full.split()

    idx = _load_index()
    results: list[Match] = []
    for stub in idx.pages:
        # Aggregate text per field for cheap scanning
        cheap_text = {
            "title": stub.title.lower(),
            "aliases": " ".join(a.lower() for a in stub.aliases),
            "tags": " ".join(t.lower() for t in stub.tags),
            "summary": stub.summary.lower(),
        }

        score = 0
        hits: list[str] = []
        snippet = ""

        for f in ("title", "aliases", "tags", "summary"):
            if f not in fields:
                continue
            text = cheap_text[f]
            if all(t in text for t in terms):
                score += weights[f]
                hits.append(f)
                if not snippet and f == "title":
                    snippet = stub.title
                elif not snippet and f == "summary":
                    i = text.find(terms[0])
                    snippet = stub.summary[max(0, i - 40):i + 80]

        if "key_facts" in fields and not hits:
            # Only deep-load the page when the cheap fields didn't already
            # hit — avoids reading every wiki/*.md for every search.
            try:
                page = _read_page_file(REPO_ROOT / stub.path)
            except Exception:
                continue
            for fact in page.key_facts:
                claim_lower = fact.claim.lower()
                if all(t in claim_lower for t in terms):
                    score += weights["key_facts"]
                    hits.append("key_facts")
                    snippet = snippet or fact.claim[:160]
                    break

        if score > 0:
            results.append(Match(
                slug=stub.slug,
                title=stub.title,
                type=stub.type,
                path=stub.path,
                score=score,
                field_hits=hits,
                snippet=snippet,
            ))

    results.sort(key=lambda m: (-m.score, m.title.lower()))
    return results[:limit]


def neighbors(slug: str, depth: int = 1) -> list[Page]:
    """BFS-walk the related-pages graph (frontmatter `related` lists +
    body `[[wikilinks]]`) starting from `slug`. Returns Pages in
    visitation order, excluding the seed page itself.
    """
    seed = find_page(slug)
    if seed is None:
        return []
    seen: set[str] = {seed.slug}
    frontier = [seed]
    out: list[Page] = []
    for _ in range(max(0, depth)):
        next_frontier: list[Page] = []
        for page in frontier:
            for target in _outbound_links(page):
                if target in seen:
                    continue
                p = find_page(target)
                if p is None:
                    continue
                seen.add(p.slug)
                out.append(p)
                next_frontier.append(p)
        frontier = next_frontier
        if not frontier:
            break
    return out


def _outbound_links(page: Page) -> list[str]:
    """Every wikilink target out of a page: frontmatter related lists +
    body `[[X]]` mentions."""
    targets: list[str] = []
    for buckets in page.related.values():
        targets.extend(buckets)
    for header, body in page.sections.items():
        for m in _WIKILINK_RE.finditer(body):
            targets.append(m.group(1).strip())
    # Dedup while preserving order
    seen: set[str] = set()
    out: list[str] = []
    for t in targets:
        if t in seen or not t:
            continue
        seen.add(t)
        out.append(t)
    return out


def provenance_for(slug: str) -> list[str]:
    """Return every distinct `[raw/...]` anchor cited on this page."""
    page = find_page(slug)
    if page is None:
        return []
    found: list[str] = []
    seen: set[str] = set()
    # Frontmatter sources list
    for s in page.frontmatter.get("sources") or []:
        s = str(s)
        if s not in seen:
            seen.add(s)
            found.append(s)
    # Body anchors (key_facts and elsewhere)
    for body in page.sections.values():
        for m in _PROVENANCE_RE.finditer(body):
            ref = m.group(0)
            if ref not in seen:
                seen.add(ref)
                found.append(ref)
    return found
