"""L2: compile.render_page — markdown rendering.

We don't golden-diff full files (formatting drift is too noisy for a unit
test); we assert on structural invariants that downstream validate.py
relies on.
"""
from __future__ import annotations

import re
from datetime import date

import yaml

from scripts.ingest.compile import render_page
from scripts.ingest.schemas import Fact, PageCandidate, RelatedLinks


def _split_fm(md: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n(.*)", md, re.DOTALL)
    assert m, f"no frontmatter in:\n{md[:200]}"
    return yaml.safe_load(m.group(1)), m.group(2)


def _sample_concept() -> PageCandidate:
    return PageCandidate(
        page_type="concept",
        title="Active Inference",
        id="active-inference",
        aliases=["AIF"],
        summary="Active Inference models action selection via free-energy minimization.",
        key_facts=[
            Fact(
                claim="Agents minimize variational free energy",
                provenance="[raw/books/neuroscience/Friston_2010.pdf#p42]",
            ),
            Fact(
                claim="Perception and action share the same objective",
                provenance="[raw/books/neuroscience/Friston_2010.pdf#p47]",
            ),
        ],
        inferences=["The principle generalizes to multi-agent settings"],
        uncertainties=["Scope outside continuous-state systems is unclear"],
        related=RelatedLinks(broader=["Free Energy Principle"], narrower=[], adjacent=["Predictive Coding"]),
        tags=["neuroscience"],
    )


def test_render_contains_frontmatter_and_required_fields() -> None:
    page = _sample_concept()
    md = render_page(page, source_provenance="raw/books/neuroscience/Friston_2010.pdf")
    fm, body = _split_fm(md)
    assert fm["title"] == "Active Inference"
    assert fm["type"] == "concept"
    assert fm["id"] == "active-inference"
    assert fm["status"] == "draft"
    assert fm["created"] == date.today().isoformat()
    assert fm["updated"] == date.today().isoformat()
    assert isinstance(fm["sources"], list) and fm["sources"]


def test_render_emits_headings_validator_depends_on() -> None:
    page = _sample_concept()
    md = render_page(page, source_provenance="raw/books/neuroscience/Friston_2010.pdf")
    assert "# Active Inference" in md
    assert "## Summary" in md
    assert "## Key facts" in md
    # Body of an Inference block is printed as bullet "- Inference: ..."
    assert "- Inference: The principle generalizes" in md
    assert "- Uncertain: Scope outside" in md


def test_render_keeps_provenance_anchors() -> None:
    page = _sample_concept()
    md = render_page(page, source_provenance="raw/books/neuroscience/Friston_2010.pdf")
    assert "[raw/books/neuroscience/Friston_2010.pdf#p42]" in md
    assert "[raw/books/neuroscience/Friston_2010.pdf#p47]" in md


def test_render_handles_empty_sections_gracefully() -> None:
    page = PageCandidate(
        page_type="concept",
        title="Placeholder",
        id="placeholder",
        summary="Short.",
    )
    md = render_page(page, source_provenance="raw/books/x/y.pdf")
    # Key facts emits "(none recorded)" placeholder so validators anchor correctly.
    assert "## Key facts" in md
    assert "(none recorded)" in md


def test_entity_frontmatter_has_required_fields() -> None:
    page = PageCandidate(
        page_type="entity",
        title="Andrej Karpathy",
        id="andrej-karpathy",
        summary="Researcher and educator.",
        aliases=["karpathy"],
        key_facts=[
            Fact(
                claim="Wrote a gist proposing an LLM-maintained wiki",
                provenance="[raw/inbox/karpathy-llm-wiki.md#L1-L10]",
            )
        ],
    )
    md = render_page(page, source_provenance="raw/inbox/karpathy-llm-wiki.md")
    fm, _ = _split_fm(md)
    # Required entity fields from WIKI_SOP template:
    assert "aliases" in fm
    assert "canonical" in fm
    assert "confidence" in fm
    # `related` bucket with entity-specific sub-keys
    assert set(fm["related"].keys()) == {"concepts", "topics", "entities"}


def test_source_frontmatter_has_required_fields() -> None:
    page = PageCandidate(
        page_type="source",
        title="Foo Book",
        id="src-foo-book",
        summary="Book about foo.",
    )
    md = render_page(page, source_provenance="raw/books/x/foo.pdf")
    fm, _ = _split_fm(md)
    for k in ("source_kind", "source_path", "source_date", "source_author", "reliability"):
        assert k in fm


def test_analysis_frontmatter_has_question() -> None:
    page = PageCandidate(
        page_type="analysis",
        title="Does X imply Y?",
        id="does-x-imply-y",
        summary="Short synthesis.",
    )
    md = render_page(page, source_provenance="raw/books/x/foo.pdf")
    fm, _ = _split_fm(md)
    assert "question" in fm
