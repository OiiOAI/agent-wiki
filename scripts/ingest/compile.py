"""Phase D: render PageCandidate Pydantic objects to Markdown pages.

Output targets the SOP templates in `schema/templates/` but **only the fields
that are actually populated** — leaving the template's placeholder questions
empty would dilute signal, so we emit only sections with content. Structural
headings that must exist per SOP (Summary / Key facts / …) are always emitted
even when the body is empty (as "— none recorded —") so linters can anchor on
them.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Iterable

import yaml

from .schemas import (
    ALLOWED_CONFIDENCE,
    ALLOWED_RELIABILITY,
    ALLOWED_SOURCE_KIND,
    PageCandidate,
)

WIKI_DIRS = {
    "entity": "entities",
    "concept": "concepts",
    "topic": "topics",
    "source": "sources",
    "analysis": "analyses",
    "conflict": "conflicts",
}

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    s = _SLUG_RE.sub("-", text.lower()).strip("-")
    return s or "untitled"


def _frontmatter_for(page: PageCandidate, source_provenance: str, today: str) -> dict:
    """Merge common + type-specific frontmatter; per-type required fields
    are filled with empty-but-typed defaults if absent."""
    fm: dict = {
        "id": page.id,
        "title": page.title,
        "type": page.page_type,
        "status": "draft",
        "created": today,
        "updated": today,
        "sources": [source_provenance] if source_provenance else [],
    }

    extras = dict(page.frontmatter_extra)

    # `aliases` only belongs on entity pages per SOP templates; drop it for
    # every other type even if the LLM emitted it.
    if page.page_type == "entity":
        if page.aliases and "aliases" not in extras:
            extras["aliases"] = page.aliases
    else:
        extras.pop("aliases", None)

    if page.tags and "tags" not in extras:
        extras.setdefault("tags", page.tags)

    if page.page_type == "entity":
        extras.setdefault("aliases", page.aliases)
        extras.setdefault("canonical", True)
        extras.setdefault("confidence", "medium")
        extras.setdefault(
            "related",
            {
                "concepts": page.related.concepts,
                "topics": page.related.topics,
                "entities": page.related.entities,
            },
        )
    elif page.page_type == "concept":
        extras.setdefault("confidence", "medium")
        extras.setdefault(
            "related",
            {
                "broader": page.related.broader,
                "narrower": page.related.narrower,
                "adjacent": page.related.adjacent,
            },
        )
    elif page.page_type == "topic":
        extras.setdefault("confidence", "medium")
        extras.setdefault(
            "related",
            {
                "concepts": page.related.concepts,
                "entities": page.related.entities,
            },
        )
    elif page.page_type == "source":
        extras.setdefault("source_kind", "book")
        extras.setdefault("source_path", source_provenance or "")
        extras.setdefault("source_date", "")
        extras.setdefault("source_author", "")
        extras.setdefault("reliability", "unknown")
        # Coerce LLM-supplied enum noise (e.g. 'pdf', 'monograph') to a
        # SOP-allowed value so the page still lands cleanly.
        if extras.get("source_kind") not in ALLOWED_SOURCE_KIND:
            extras["source_kind"] = "book"
        if extras.get("reliability") not in ALLOWED_RELIABILITY:
            extras["reliability"] = "unknown"
    elif page.page_type == "analysis":
        extras.setdefault("question", "")
        extras.setdefault("confidence", "medium")

    if page.page_type in {"entity", "concept", "topic", "analysis"}:
        if extras.get("confidence") not in ALLOWED_CONFIDENCE:
            extras["confidence"] = "medium"

    extras.setdefault("tags", page.tags)
    fm.update(extras)
    return fm


def _dump_frontmatter(fm: dict) -> str:
    dumped = yaml.safe_dump(
        fm, sort_keys=False, allow_unicode=True, default_flow_style=False
    )
    return f"---\n{dumped}---\n"


def _section(title: str, lines: Iterable[str]) -> str:
    body_lines = list(lines)
    body = "\n".join(body_lines).strip() or "- (none recorded)"
    return f"## {title}\n\n{body}\n"


def render_page(page: PageCandidate, source_provenance: str, today: str | None = None) -> str:
    today = today or date.today().isoformat()
    fm = _frontmatter_for(page, source_provenance, today)

    parts: list[str] = [_dump_frontmatter(fm), f"\n# {page.title}\n"]

    parts.append(_section("Summary", [page.summary.strip()]))

    fact_lines = [f"- {f.claim.rstrip('.')}. {f.provenance}" for f in page.key_facts]
    parts.append(_section("Key facts", fact_lines))

    inf_lines = [
        f"- Inference: {i.lstrip('Inference: ').strip()}" for i in page.inferences
    ]
    if inf_lines:
        parts.append(_section("Inferences", inf_lines))

    unc_lines = [
        f"- Uncertain: {u.lstrip('Uncertain: ').strip()}" for u in page.uncertainties
    ]
    if unc_lines:
        parts.append(_section("Uncertainties", unc_lines))

    rel_lines: list[str] = []
    bucket_map = {
        "Broader": page.related.broader,
        "Narrower": page.related.narrower,
        "Adjacent": page.related.adjacent,
        "Concepts": page.related.concepts,
        "Topics": page.related.topics,
        "Entities": page.related.entities,
    }
    for label, targets in bucket_map.items():
        for t in targets:
            rel_lines.append(f"- {label}: [[{t}]]")
    if rel_lines:
        parts.append(_section("Related pages", rel_lines))

    parts.append(_section("Provenance", [f"- Primary source: {source_provenance}"]))

    parts.append(
        _section(
            "Change notes",
            [f"- {today} — page created by auto ingest."],
        )
    )

    return "\n".join(parts).rstrip() + "\n"


def staging_path(book_stem: str, page: PageCandidate, root: Path) -> Path:
    """Return the full path where this candidate should land in staging.

    `root` is typically `tmp/ingest_staging/<book_stem>/`.
    """
    subdir = WIKI_DIRS[page.page_type]
    return root / subdir / f"{page.id}.md"


def write_staging(
    book_stem: str,
    candidates: list[PageCandidate],
    source_provenance: str,
    staging_root: Path,
    today: str | None = None,
) -> list[Path]:
    """Render candidates to markdown files under staging_root. Returns the
    list of absolute paths written.
    """
    today = today or date.today().isoformat()
    written: list[Path] = []
    for cand in candidates:
        target = staging_path(book_stem, cand, staging_root)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_page(cand, source_provenance, today=today))
        written.append(target)
    return written
