"""L3: conflict_check — deterministic Layer 1 (id / title / alias collisions)."""
from __future__ import annotations

from pathlib import Path

import pytest

from scripts.ingest.conflict_check import (
    WikiIndexEntry,
    detect_collisions,
    load_wiki_index,
)
from scripts.ingest.schemas import PageCandidate, RelatedLinks


def _make_candidate(title: str, pid: str, aliases: list[str] | None = None) -> PageCandidate:
    return PageCandidate(
        page_type="concept",
        title=title,
        id=pid,
        summary="x",
        aliases=aliases or [],
        related=RelatedLinks(),
    )


def test_no_collision_when_index_empty() -> None:
    assert detect_collisions([_make_candidate("New Thing", "new-thing")], []) == []


def test_id_collision_detected() -> None:
    existing = [
        WikiIndexEntry(
            id="active-inference",
            title="Active Inference (Friston)",
            type="concept",
            path="wiki/concepts/active-inference.md",
        )
    ]
    cands = [_make_candidate("Active Inference", "active-inference")]
    cols = detect_collisions(cands, existing)
    assert len(cols) == 1
    assert cols[0].reason in {"id", "title", "alias"}
    assert cols[0].candidate_id == "active-inference"


def test_title_collision_case_and_whitespace_insensitive() -> None:
    existing = [
        WikiIndexEntry(
            id="active-inference",
            title="Active Inference",
            type="concept",
            path="wiki/concepts/active-inference.md",
        )
    ]
    cands = [_make_candidate("  active   inference ", "aif-alt")]
    cols = detect_collisions(cands, existing)
    assert cols and cols[0].reason == "title"


def test_alias_collision() -> None:
    existing = [
        WikiIndexEntry(
            id="active-inference",
            title="Active Inference",
            type="concept",
            path="wiki/concepts/active-inference.md",
            aliases=["AIF"],
        )
    ]
    cands = [_make_candidate("Action Inference Framework", "action-inference-framework", aliases=["AIF"])]
    cols = detect_collisions(cands, existing)
    assert cols and cols[0].reason == "alias"


def test_candidate_title_matching_existing_alias() -> None:
    existing = [
        WikiIndexEntry(
            id="active-inference",
            title="Active Inference",
            type="concept",
            path="wiki/concepts/active-inference.md",
            aliases=["AIF"],
        )
    ]
    cands = [_make_candidate("AIF", "aif")]
    cols = detect_collisions(cands, existing)
    assert cols


def test_load_wiki_index_reads_real_layout(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    (wiki / "concepts").mkdir(parents=True)
    (wiki / "entities").mkdir(parents=True)
    (wiki / "concepts" / "active-inference.md").write_text(
        "---\n"
        "id: active-inference\n"
        "title: Active Inference\n"
        "type: concept\n"
        "status: draft\n"
        "created: 2026-04-22\n"
        "updated: 2026-04-22\n"
        "sources: []\n"
        "confidence: medium\n"
        "---\n\n# Active Inference\n"
    )
    (wiki / "entities" / "andrej-karpathy.md").write_text(
        "---\n"
        "id: andrej-karpathy\n"
        "title: Andrej Karpathy\n"
        "type: entity\n"
        "status: draft\n"
        "created: 2026-04-22\n"
        "updated: 2026-04-22\n"
        "sources: []\n"
        "aliases: [\"karpathy\"]\n"
        "canonical: true\n"
        "confidence: medium\n"
        "---\n\n# Andrej Karpathy\n"
    )
    index = load_wiki_index(wiki)
    titles = {e.title for e in index}
    assert "Active Inference" in titles
    assert "Andrej Karpathy" in titles
    ak = next(e for e in index if e.id == "andrej-karpathy")
    assert ak.aliases == ["karpathy"]
