"""Phase F: detect collisions between staged candidates and the existing wiki.

Layer 1 (deterministic, unit-tested): title / alias / id collisions.
Layer 2 (LLM, deferred): same-title candidates → decide if they are the same
   subject (→ update) or disagreeing (→ create `conflicts/<title>.md`). Layer
   2 is invoked only when Layer 1 flags a collision.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class WikiIndexEntry:
    id: str
    title: str
    type: str
    path: str
    aliases: list[str] = field(default_factory=list)


@dataclass
class CollisionReport:
    candidate_id: str
    candidate_title: str
    collided_with: list[WikiIndexEntry]
    reason: str  # 'title' | 'alias' | 'id'


_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def load_wiki_index(wiki_root: Path) -> list[WikiIndexEntry]:
    """Walk `wiki/<type>/*.md`, parse frontmatter, return index entries.

    We do NOT parse `wiki/index.md` because (a) that file's a human-facing
    register and can drift from the actual pages, (b) the pages themselves
    are authoritative.
    """
    entries: list[WikiIndexEntry] = []
    for sub in ("entities", "concepts", "topics", "sources", "analyses", "conflicts"):
        base = wiki_root / sub
        if not base.is_dir():
            continue
        for md_path in sorted(base.glob("*.md")):
            try:
                txt = md_path.read_text(encoding="utf-8")
            except OSError:
                continue
            m = _FRONTMATTER_RE.match(txt)
            if not m:
                continue
            try:
                fm = yaml.safe_load(m.group(1)) or {}
            except yaml.YAMLError:
                continue
            entries.append(
                WikiIndexEntry(
                    id=str(fm.get("id") or md_path.stem),
                    title=str(fm.get("title") or md_path.stem),
                    type=str(fm.get("type") or sub.rstrip("s")),
                    path=str(md_path.relative_to(wiki_root.parent)),
                    aliases=list(fm.get("aliases") or []),
                )
            )
    return entries


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def detect_collisions(
    candidates: list,  # List[PageCandidate] but avoid circular import
    index: list[WikiIndexEntry],
) -> list[CollisionReport]:
    """Return one CollisionReport per candidate that collides with the
    existing wiki on id, title, or alias."""
    # Build lookup tables
    id_to_entry: dict[str, WikiIndexEntry] = {e.id: e for e in index}
    title_to_entries: dict[str, list[WikiIndexEntry]] = {}
    alias_to_entries: dict[str, list[WikiIndexEntry]] = {}
    for e in index:
        title_to_entries.setdefault(_norm(e.title), []).append(e)
        for a in e.aliases:
            alias_to_entries.setdefault(_norm(a), []).append(e)

    collisions: list[CollisionReport] = []
    for cand in candidates:
        hits: list[WikiIndexEntry] = []
        reason = ""
        if cand.id in id_to_entry:
            hits.append(id_to_entry[cand.id])
            reason = "id"
        t = _norm(cand.title)
        if t in title_to_entries:
            hits.extend(e for e in title_to_entries[t] if e not in hits)
            reason = reason or "title"
        for a in cand.aliases:
            na = _norm(a)
            if na in alias_to_entries:
                hits.extend(e for e in alias_to_entries[na] if e not in hits)
                reason = reason or "alias"
        # symmetric: does candidate title match any existing alias?
        if t in alias_to_entries:
            hits.extend(e for e in alias_to_entries[t] if e not in hits)
            reason = reason or "alias"
        if hits:
            collisions.append(
                CollisionReport(
                    candidate_id=cand.id,
                    candidate_title=cand.title,
                    collided_with=hits,
                    reason=reason,
                )
            )
    return collisions
