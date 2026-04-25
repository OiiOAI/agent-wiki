"""L5: regression test — run the pipeline on the Karpathy gist and check that
the LLM recovers the same three pages that were hand-produced (see wiki/).

The gist `raw/inbox/karpathy-llm-wiki.md` was manually ingested on 2026-04-21
into these three pages:

    wiki/sources/LLM Wiki (Karpathy gist).md
    wiki/concepts/LLM Wiki.md
    wiki/entities/Andrej Karpathy.md

L5 runs the automated pipeline on the same source and checks that:

  * at least one source, concept (or topic), and entity page appears
  * a concept titled "LLM Wiki" (or close variant) is present
  * core themes (ingest / query / lint / raw / schema / index / log) surface
    in titles, aliases, or related-page wiki links — ≥3 of 7 (a low bar
    tolerant of LLM judgment; the plan's ≥80% figure referred to *explicit*
    concept names of which the manual version has essentially one)
  * every rendered page passes validate_page
  * provenance anchors use line form `[raw/inbox/karpathy-llm-wiki.md#L…]`

Note: the manual Andrej Karpathy entity page was built partly from manifest
metadata (the author field in `_manifest.md`) which the pipeline does not
read. So we do *not* require the LLM to rediscover "Karpathy" — only that
some named entity is extracted from the gist body itself.

Skipped by default. Opt in with `RUN_E2E_LLM=1`. Budget ~$0.10.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import pytest

from scripts.ingest import chunk as chunk_mod
from scripts.ingest import compile as compile_mod
from scripts.ingest import extract as extract_mod
from scripts.ingest.cost_tracker import CostTracker
from scripts.ingest.validate import validate_page

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_MD = REPO_ROOT / "raw" / "inbox" / "karpathy-llm-wiki.md"
SOURCE_REL = "raw/inbox/karpathy-llm-wiki.md"

pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_E2E_LLM") != "1",
    reason="L5 hits the real LLM; set RUN_E2E_LLM=1 to opt in.",
)


@pytest.fixture(scope="module")
def pipeline_output(tmp_path_factory: pytest.TempPathFactory) -> dict:
    if not SOURCE_MD.exists():
        pytest.skip(f"Karpathy source missing: {SOURCE_MD}")

    work = tmp_path_factory.mktemp("e2e_karpathy")
    staging_root = work / "staging" / "karpathy"

    # Phase A is a no-op: markdown source already has line structure. Chunker
    # operates directly on the file.
    md_text = SOURCE_MD.read_text(encoding="utf-8")
    chunks = chunk_mod.semantic_chunking(md_text, max_words=6000, min_chunk_words=150)
    assert chunks, "semantic_chunking produced no chunks for Karpathy gist"

    cost = CostTracker(per_book_cap=1.0, batch_cap=5.0)
    extraction = extract_mod.extract_book(
        book_stem="karpathy-llm-wiki",
        source_path=SOURCE_REL,
        discipline="inbox",
        language="en",
        chunks=chunks,
        cost=cost,
    )

    source_provenance = f"[{SOURCE_REL}#L1-L{len(md_text.splitlines())}]"
    written = compile_mod.write_staging(
        book_stem="karpathy-llm-wiki",
        candidates=extraction.candidates,
        source_provenance=source_provenance,
        staging_root=staging_root,
    )

    return {
        "chunks": chunks,
        "extraction": extraction,
        "staging_root": staging_root,
        "written": written,
        "cost": cost,
    }


def test_has_source_concept_entity_pages(pipeline_output: dict) -> None:
    types = [p.page_type for p in pipeline_output["extraction"].candidates]
    assert "source" in types, f"no source page emitted (got types: {types})"
    assert "concept" in types or "topic" in types, (
        f"no concept/topic page emitted (got types: {types})"
    )
    assert "entity" in types, f"no entity page emitted (got types: {types})"


def test_wiki_concept_captured(pipeline_output: dict) -> None:
    """Core concept of the gist is the LLM-maintained wiki pattern. The LLM
    may title it 'LLM Wiki', 'Persistent Wiki', 'Wiki Operations', etc. —
    accept any non-source page whose title or aliases contain 'wiki'."""
    cands = pipeline_output["extraction"].candidates
    relevant = [
        p for p in cands
        if p.page_type in {"concept", "topic", "entity"}
        and (
            "wiki" in p.title.lower()
            or any("wiki" in a.lower() for a in p.aliases)
        )
    ]
    assert relevant, (
        "no concept/topic/entity page mentions 'wiki' in title. "
        "candidates: "
        + ", ".join(f"{p.page_type}:{p.title!r}" for p in cands)
    )


def test_at_least_one_entity_page(pipeline_output: dict) -> None:
    """Gist body never names the author, so we can't require Karpathy. We
    just require *some* entity emerged — e.g., Memex, qmd, Obsidian."""
    entities = [
        p for p in pipeline_output["extraction"].candidates
        if p.page_type == "entity"
    ]
    assert entities, "no entity pages emitted from Karpathy gist"


def test_core_themes_coverage(pipeline_output: dict) -> None:
    """At least 3 of these 7 themes should surface anywhere in the output
    (title, alias, or related-page wiki link)."""
    themes = {"ingest", "query", "lint", "raw", "schema", "index", "log"}
    surface: set[str] = set()
    for p in pipeline_output["extraction"].candidates:
        haystack = " ".join(
            [p.title, *p.aliases,
             *p.related.broader, *p.related.narrower, *p.related.adjacent,
             *p.related.concepts, *p.related.topics, *p.related.entities]
        ).lower()
        for theme in themes:
            if re.search(rf"\b{theme}\b", haystack):
                surface.add(theme)
    assert len(surface) >= 3, (
        f"only {surface} of {themes} surfaced — expected ≥3. "
        f"Candidates: {[(p.page_type, p.title) for p in pipeline_output['extraction'].candidates]}"
    )


def test_all_provenance_is_md_line_anchor(pipeline_output: dict) -> None:
    """Source is markdown, so every anchor must use the L-range form against
    this file — no page anchors, no other paths."""
    line_pat = re.compile(rf"^\[{re.escape(SOURCE_REL)}#L\d+(?:-L?\d+)?\]$")
    problems: list[str] = []
    for p in pipeline_output["extraction"].candidates:
        for fact in p.key_facts:
            if not line_pat.match(fact.provenance):
                problems.append(f"{p.id}: {fact.provenance!r}")
    assert not problems, "non-line-anchor provenance found: " + "; ".join(problems)


def test_every_rendered_page_validates(pipeline_output: dict) -> None:
    errors_by_page: dict[str, list[str]] = {}
    for path in pipeline_output["written"]:
        md = path.read_text(encoding="utf-8")
        errs = validate_page(
            md,
            existing_ids=set(),
            source_text=SOURCE_MD.read_text(encoding="utf-8"),
            page_path=str(path),
        )
        if errs:
            errors_by_page[path.name] = [str(e) for e in errs]
    assert not errors_by_page, (
        "rendered pages failed validation:\n"
        + "\n".join(f"  {n}: {errs}" for n, errs in errors_by_page.items())
    )


def test_cost_under_budget(pipeline_output: dict) -> None:
    summary = pipeline_output["cost"].summary()
    assert summary["total_dollars"] < 1.0, (
        f"Karpathy ingest cost ${summary['total_dollars']:.4f} — unexpectedly high"
    )
