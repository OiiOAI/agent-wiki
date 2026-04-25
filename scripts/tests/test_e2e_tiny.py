"""L4: end-to-end ingest on a synthetic 5-page PDF — touches the real LLM.

Skipped by default. To run:
    RUN_E2E_LLM=1 pytest scripts/tests/test_e2e_tiny.py -v

The test walks the full pipeline on `scripts/tests/fixtures/tiny_sample.pdf`
(a fictional tutorial about the made-up "Zelnick Framework"). We deliberately
use fictional content so the LLM cannot crib from its own training data —
whatever it emits must have been extracted from the chunk.

Assertions are structural, not byte-for-byte: model output is non-deterministic,
so we check page-type counts, title-name coverage, and validator cleanliness
rather than diffing against a golden file.

Budget: ~$0.05 per run.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest

from scripts.ingest import chunk as chunk_mod
from scripts.ingest import compile as compile_mod
from scripts.ingest import extract as extract_mod
from scripts.ingest import pdf_to_md
from scripts.ingest.cost_tracker import CostTracker
from scripts.ingest.validate import validate_page

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PDF = REPO_ROOT / "scripts" / "tests" / "fixtures" / "tiny_sample.pdf"

# Fake SOP-compliant source_path — the real PDF lives under fixtures/, but we
# feed the LLM a `raw/books/...` path so provenance anchors look correct.
FAKE_SOURCE = "raw/books/test/tiny_sample.pdf"

pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_E2E_LLM") != "1",
    reason="L4 hits the real LLM; set RUN_E2E_LLM=1 to opt in.",
)


@pytest.fixture(scope="module")
def pipeline_output(tmp_path_factory: pytest.TempPathFactory) -> dict:
    """Run Phase A→D once; reuse the result for every assertion."""
    if not FIXTURE_PDF.exists():
        pytest.skip(f"fixture PDF missing: {FIXTURE_PDF}")

    work = tmp_path_factory.mktemp("e2e_tiny")
    cache_dir = work / "md_cache"
    staging_root = work / "staging"

    # Phase A — PDF to markdown with page anchors.
    meta = pdf_to_md.convert_to_markdown(FIXTURE_PDF, cache_dir=cache_dir, force=True)
    md_text = Path(meta.cache_path).read_text(encoding="utf-8")

    # Phase B — chunk.
    chunks = chunk_mod.semantic_chunking(md_text, max_words=6000, min_chunk_words=50)
    assert chunks, "semantic_chunking returned no chunks"

    # Phase C — structured extraction (LLM).
    cost = CostTracker(per_book_cap=1.0, batch_cap=5.0)
    extraction = extract_mod.extract_book(
        book_stem="tiny_sample",
        source_path=FAKE_SOURCE,
        discipline="test",
        language=meta.language,
        chunks=chunks,
        cost=cost,
    )

    # Phase D — render to staging.
    source_provenance = (
        f"[{FAKE_SOURCE}#p1-p{meta.pages_total or 1}]"
    )
    written = compile_mod.write_staging(
        book_stem="tiny_sample",
        candidates=extraction.candidates,
        source_provenance=source_provenance,
        staging_root=staging_root / "tiny_sample",
    )

    return {
        "meta": meta,
        "chunks": chunks,
        "extraction": extraction,
        "staging_root": staging_root / "tiny_sample",
        "written": written,
        "cost": cost,
    }


def test_phase_a_pdf_to_md_has_page_markers(pipeline_output: dict) -> None:
    meta = pipeline_output["meta"]
    assert meta.converter in {"marker", "pdftotext"}
    assert meta.language == "en"
    md_text = Path(meta.cache_path).read_text(encoding="utf-8")
    assert "<!-- PAGE:1 -->" in md_text
    # The tiny PDF is 3+ pages of actual content.
    assert meta.pages_total and meta.pages_total >= 3


def test_phase_b_chunks_carry_pages(pipeline_output: dict) -> None:
    chunks = pipeline_output["chunks"]
    assert len(chunks) >= 2
    # Every chunk should have an inferred page range (fixture uses marker-style
    # anchors, so start_page is never None for this input).
    for ch in chunks:
        assert ch.start_page is not None, f"chunk {ch.index} lost its page anchor"
        assert ch.start_page >= 1
        assert ch.end_page >= ch.start_page


def test_phase_c_extraction_produces_enough_pages(pipeline_output: dict) -> None:
    extraction = pipeline_output["extraction"]
    assert not extraction.failed_chunks, (
        f"chunks failed LLM extraction: {extraction.failed_chunks}"
    )
    # The plan expects ≥1 source + 2-3 concept + 1 entity.
    assert len(extraction.candidates) >= 3, (
        f"only {len(extraction.candidates)} candidates produced — expected ≥3"
    )


def test_phase_c_covers_key_concepts(pipeline_output: dict) -> None:
    """Extraction must surface at least two of the three named protocols."""
    titles = {p.title.lower() for p in pipeline_output["extraction"].candidates}
    aliases = {
        a.lower()
        for p in pipeline_output["extraction"].candidates
        for a in p.aliases
    }
    universe = titles | aliases
    expected = {"alpha protocol", "beta mechanism", "gamma invariant"}

    matched = {
        exp for exp in expected if any(exp in t for t in universe)
    }
    assert len(matched) >= 2, (
        f"only matched {matched} of {expected} — LLM missed core concepts.\n"
        f"titles={sorted(titles)}"
    )


def test_phase_c_captures_zelnick_entity(pipeline_output: dict) -> None:
    """Dr. Margaret Zelnick should appear as an entity page."""
    entities = [
        p for p in pipeline_output["extraction"].candidates if p.page_type == "entity"
    ]
    assert entities, "no entity pages emitted"
    zelnick_entities = [
        p for p in entities if "zelnick" in p.title.lower()
    ]
    assert zelnick_entities, (
        f"no Zelnick entity page — entities: {[e.title for e in entities]}"
    )


def test_phase_c_provenance_points_to_source(pipeline_output: dict) -> None:
    """Every fact should cite the fake raw/ path and a page in [1, pages_total]."""
    pages_total = pipeline_output["meta"].pages_total
    for page in pipeline_output["extraction"].candidates:
        for fact in page.key_facts:
            assert FAKE_SOURCE in fact.provenance, (
                f"{page.id}: provenance missing source: {fact.provenance!r}"
            )
            # Page number must fall in range (or be a line anchor).
            if "#p" in fact.provenance:
                import re

                nums = re.findall(r"\d+", fact.provenance.split("#p", 1)[1])
                assert nums, f"no page number in {fact.provenance}"
                for n in nums:
                    assert 1 <= int(n) <= (pages_total or 99), (
                        f"{page.id}: page {n} out of 1..{pages_total}"
                    )


def test_phase_d_writes_staging_files(pipeline_output: dict) -> None:
    written = pipeline_output["written"]
    staging_root = pipeline_output["staging_root"]
    extraction = pipeline_output["extraction"]

    assert len(written) == len(extraction.candidates)
    for path in written:
        assert path.exists(), f"missing staged file: {path}"
        assert path.is_relative_to(staging_root)
        assert path.read_text().startswith("---\n")


def test_phase_e_every_staged_page_validates(pipeline_output: dict) -> None:
    """Each rendered page must pass all 11 SOP invariants (given empty index)."""
    errors_by_page: dict[str, list[str]] = {}
    for path in pipeline_output["written"]:
        md = path.read_text(encoding="utf-8")
        errs = validate_page(
            md,
            existing_ids=set(),
            source_text=None,
            page_path=str(path),
        )
        if errs:
            errors_by_page[path.name] = [str(e) for e in errs]
    assert not errors_by_page, (
        "rendered pages failed validation:\n"
        + "\n".join(f"  {n}: {errs}" for n, errs in errors_by_page.items())
    )


def test_cost_tracker_stayed_under_book_cap(pipeline_output: dict) -> None:
    cost = pipeline_output["cost"]
    summary = cost.summary()
    assert summary["total_dollars"] < 1.0, (
        f"tiny fixture cost ${summary['total_dollars']:.4f} — over $1 cap is suspicious"
    )
    assert "tiny_sample" in summary["books"]
