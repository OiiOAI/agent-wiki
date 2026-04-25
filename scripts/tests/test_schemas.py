"""L1: Pydantic schema validation for ExtractionOutput and friends."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from scripts.ingest.schemas import (
    ExtractionOutput,
    Fact,
    PageCandidate,
    RelatedLinks,
)


def test_fact_requires_provenance() -> None:
    with pytest.raises(ValidationError):
        Fact(claim="something", provenance="")
    f = Fact(claim="something", provenance="[raw/books/x/y.pdf#p12]")
    assert f.provenance.startswith("[raw/")


def test_page_id_pattern() -> None:
    # Empty / whitespace ids still fail — slugify refuses to invent content.
    with pytest.raises(ValidationError):
        PageCandidate(
            page_type="concept",
            title="T",
            id="",
            summary="x",
        )
    with pytest.raises(ValidationError):
        PageCandidate(
            page_type="concept",
            title="T",
            id="   ",
            summary="x",
        )
    PageCandidate(
        page_type="concept",
        title="T",
        id="valid-kebab-id",
        summary="x",
    )


def test_page_id_is_coerced_to_kebab() -> None:
    # Spaces, uppercase, and leading/trailing dashes all get normalized
    # rather than rejected — LLMs produce near-misses often enough that
    # auto-repair is preferable to crashing the chunk.
    p1 = PageCandidate(page_type="concept", title="T", id="Has Spaces", summary="x")
    assert p1.id == "has-spaces"
    p2 = PageCandidate(page_type="concept", title="T", id="-leading-dash-", summary="x")
    assert p2.id == "leading-dash"
    p3 = PageCandidate(page_type="concept", title="T", id="Mixed_Case/Slash", summary="x")
    assert p3.id == "mixed-case-slash"


def test_page_id_cjk_transliteration() -> None:
    # Chinese ids must transliterate to pinyin so the kebab-case pattern holds.
    # This was the critical bug that caused 100% of Chinese-book failures in S5.
    p = PageCandidate(
        page_type="concept",
        title="道德经",
        id="道德经",
        summary="x",
    )
    assert p.id == "dao-de-jing"
    p2 = PageCandidate(
        page_type="concept",
        title="T",
        id="当代经济学系列丛书",
        summary="x",
    )
    # All ASCII kebab-case after pinyin + normalization
    assert p2.id.replace("-", "").isalnum()
    assert p2.id.islower()
    assert not p2.id.startswith("-") and not p2.id.endswith("-")


def test_page_type_enum() -> None:
    with pytest.raises(ValidationError):
        PageCandidate(
            page_type="dashboard",  # not allowed in extraction output
            title="T",
            id="x",
            summary="x",
        )
    with pytest.raises(ValidationError):
        PageCandidate(
            page_type="conflict",  # produced deterministically, not by LLM
            title="T",
            id="x",
            summary="x",
        )


def test_extraction_output_empty_ok() -> None:
    out = ExtractionOutput(pages=[], skipped_reason="no ingestable content")
    assert out.pages == []
    assert out.skipped_reason == "no ingestable content"


def test_extraction_output_roundtrip() -> None:
    payload = {
        "pages": [
            {
                "page_type": "concept",
                "title": "Active Inference",
                "id": "active-inference",
                "summary": "A principle from Friston.",
                "key_facts": [
                    {"claim": "Agents minimize free energy",
                     "provenance": "[raw/books/neuroscience/Friston.pdf#p42]"}
                ],
                "inferences": [],
                "uncertainties": [],
                "related": {"broader": ["Free Energy Principle"], "narrower": [], "adjacent": []},
                "tags": ["neuro"],
                "aliases": ["AI (Friston)"],
                "frontmatter_extra": {},
            }
        ],
        "skipped_reason": None,
    }
    out = ExtractionOutput.model_validate(payload)
    assert out.pages[0].title == "Active Inference"
    assert out.pages[0].related.broader == ["Free Energy Principle"]


def test_related_links_defaults_empty() -> None:
    r = RelatedLinks()
    assert r.broader == []
    assert r.narrower == []
    assert r.adjacent == []
    assert r.concepts == []


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
