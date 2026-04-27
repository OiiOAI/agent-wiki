"""Unit tests for `scripts.query.wiki_query`.

Builds a synthetic wiki/ tree under tmp_path and points the module at
it via monkeypatch. Covers list/find/read/search/neighbors/provenance
+ both index-backed and filesystem-fallback paths.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.query import wiki_query


# ----- fixture -------------------------------------------------------


def _make_wiki(tmp_path: Path) -> Path:
    """Create a tiny but realistic wiki/ tree."""
    wiki = tmp_path / "wiki"
    (wiki / "concepts").mkdir(parents=True)
    (wiki / "entities").mkdir(parents=True)
    (wiki / "sources").mkdir(parents=True)

    (wiki / "concepts" / "bdnf.md").write_text(
        "---\n"
        "id: bdnf\n"
        "title: BDNF\n"
        "type: concept\n"
        "status: draft\n"
        "created: '2026-04-25'\n"
        "updated: '2026-04-25'\n"
        "sources:\n"
        "- '[raw/books/health/Spark.pdf#p1-228]'\n"
        "tags: [neuroscience, neurotrophin, exercise]\n"
        "aliases: [brain-derived-neurotrophic-factor]\n"
        "related:\n"
        "  broader: [neurotrophin]\n"
        "  adjacent: [hippocampus]\n"
        "  concepts: [neurogenesis]\n"
        "---\n\n"
        "# BDNF\n\n"
        "## Summary\n\n"
        "Brain-derived neurotrophic factor is a protein that supports neuron survival and stimulates new neuron growth.\n\n"
        "## Key facts\n\n"
        "- Exercise raises BDNF levels in the hippocampus by ~3x in mice. [raw/books/health/Spark.pdf#p43]\n"
        "- BDNF is concentrated in the hippocampus and cortex. [raw/books/health/Spark.pdf#p41]\n\n"
        "## Inferences\n\n"
        "- Inference: Exercise → BDNF → hippocampal neurogenesis is the proximate mechanism.\n\n"
        "## Uncertainties\n\n"
        "- Uncertain: human dose-response is not quantified.\n\n"
        "## Related pages\n\n"
        "- Broader: [[neurotrophin]]\n"
        "- Adjacent: [[hippocampus]]\n"
        "- Concepts: [[neurogenesis]]\n",
        encoding="utf-8",
    )

    (wiki / "concepts" / "hippocampus.md").write_text(
        "---\n"
        "id: hippocampus\n"
        "title: Hippocampus\n"
        "type: concept\n"
        "status: draft\n"
        "created: '2026-04-25'\n"
        "updated: '2026-04-25'\n"
        "sources:\n"
        "- '[raw/books/neuroscience/Kandel.pdf#p1-1709]'\n"
        "tags: [neuroscience, memory]\n"
        "aliases: []\n"
        "related:\n"
        "  concepts: [bdnf, neurogenesis]\n"
        "---\n\n"
        "# Hippocampus\n\n"
        "## Summary\n\n"
        "Subcortical structure central to declarative memory consolidation.\n\n"
        "## Key facts\n\n"
        "- The hippocampus is one of the few regions where adult neurogenesis occurs. [raw/books/neuroscience/Kandel.pdf#p1234]\n",
        encoding="utf-8",
    )

    (wiki / "entities" / "andrej-karpathy.md").write_text(
        "---\n"
        "id: andrej-karpathy\n"
        "title: Andrej Karpathy\n"
        "type: entity\n"
        "status: draft\n"
        "created: '2026-04-25'\n"
        "updated: '2026-04-25'\n"
        "sources:\n"
        "- '[raw/inbox/karpathy-llm-wiki.md#L1]'\n"
        "tags: [ai]\n"
        "aliases: [karpathy]\n"
        "canonical: true\n"
        "confidence: high\n"
        "related: {}\n"
        "---\n\n"
        "# Andrej Karpathy\n\n"
        "## Summary\n\n"
        "Author of the LLM Wiki gist that seeded this project.\n\n"
        "## Key facts\n\n"
        "- Authored the LLM Wiki idea file in 2025. [raw/inbox/karpathy-llm-wiki.md#L1]\n",
        encoding="utf-8",
    )

    return wiki


@pytest.fixture
def synthetic_wiki(tmp_path: Path, monkeypatch) -> Path:
    wiki = _make_wiki(tmp_path)
    repo = tmp_path
    monkeypatch.setattr(wiki_query, "REPO_ROOT", repo)
    monkeypatch.setattr(wiki_query, "WIKI_ROOT", wiki)
    monkeypatch.setattr(wiki_query, "AGENTS_INDEX_PATH", wiki / "AGENTS_INDEX.json")
    wiki_query._reset_caches()
    return wiki


# ----- list / find / read --------------------------------------------


def test_list_pages_returns_all(synthetic_wiki: Path) -> None:
    pages = wiki_query.list_pages()
    slugs = {p.slug for p in pages}
    assert slugs == {"bdnf", "hippocampus", "andrej-karpathy"}


def test_list_pages_filters_by_type(synthetic_wiki: Path) -> None:
    concepts = wiki_query.list_pages(type="concept")
    assert {p.slug for p in concepts} == {"bdnf", "hippocampus"}
    entities = wiki_query.list_pages(type="entity")
    assert {p.slug for p in entities} == {"andrej-karpathy"}


def test_find_page_resolves_alias(synthetic_wiki: Path) -> None:
    p = wiki_query.find_page("brain-derived-neurotrophic-factor")
    assert p is not None
    assert p.slug == "bdnf"


def test_find_page_resolves_title_case_insensitive(synthetic_wiki: Path) -> None:
    p = wiki_query.find_page("hippocampus")
    assert p is not None and p.slug == "hippocampus"
    p2 = wiki_query.find_page("Hippocampus")
    assert p2 is not None and p2.slug == "hippocampus"


def test_find_page_returns_none_on_unknown(synthetic_wiki: Path) -> None:
    assert wiki_query.find_page("does-not-exist") is None


def test_find_page_type_filter(synthetic_wiki: Path) -> None:
    """Slug exists but wrong type → None (don't accidentally pick it up)."""
    assert wiki_query.find_page("bdnf", type="entity") is None
    assert wiki_query.find_page("bdnf", type="concept").slug == "bdnf"


def test_read_page_parses_sections_and_facts(synthetic_wiki: Path) -> None:
    p = wiki_query.read_page("bdnf")
    assert p.title == "BDNF"
    assert "supports neuron survival" in p.summary
    assert len(p.key_facts) == 2
    f0 = p.key_facts[0]
    assert "Exercise raises BDNF" in f0.claim
    assert f0.provenance == "[raw/books/health/Spark.pdf#p43]"
    # Inferences and uncertainties parsed
    assert any("Exercise → BDNF" in i for i in p.inferences)
    assert any("dose-response" in u for u in p.uncertainties)


# ----- search --------------------------------------------------------


def test_search_matches_title_first(synthetic_wiki: Path) -> None:
    """A title hit must outrank a summary hit for the same query."""
    hits = wiki_query.search("hippocampus", limit=5)
    assert hits[0].slug == "hippocampus"
    # bdnf mentions hippocampus in summary → also a hit but lower score
    bdnf_hit = next((h for h in hits if h.slug == "bdnf"), None)
    assert bdnf_hit is not None
    assert hits[0].score > bdnf_hit.score


def test_search_includes_key_facts(synthetic_wiki: Path) -> None:
    """Query that ONLY appears in a key_facts bullet still surfaces."""
    # "neurogenesis occurs" is unique to hippocampus key_facts
    hits = wiki_query.search("neurogenesis occurs", limit=5)
    assert any(h.slug == "hippocampus" for h in hits)


def test_search_empty_query_returns_empty(synthetic_wiki: Path) -> None:
    assert wiki_query.search("", limit=5) == []
    assert wiki_query.search("   ", limit=5) == []


# ----- neighbors -----------------------------------------------------


def test_neighbors_walks_one_hop(synthetic_wiki: Path) -> None:
    out = wiki_query.neighbors("bdnf", depth=1)
    slugs = {p.slug for p in out}
    # bdnf's related: broader=neurotrophin (no page), adjacent=hippocampus (yes),
    # concepts=neurogenesis (no page). Body wikilinks: same set.
    # Only hippocampus exists as a real page → only it shows up.
    assert "hippocampus" in slugs
    # bdnf itself excluded
    assert "bdnf" not in slugs


def test_neighbors_two_hops(synthetic_wiki: Path) -> None:
    """Hippocampus links back to bdnf — walking 2 hops from bdnf via
    hippocampus brings us back, but bdnf is in `seen` so it's skipped.
    Net: same 1-hop result."""
    out_1 = wiki_query.neighbors("bdnf", depth=1)
    out_2 = wiki_query.neighbors("bdnf", depth=2)
    # 2-hop ⊇ 1-hop
    assert {p.slug for p in out_1}.issubset({p.slug for p in out_2})


def test_neighbors_unknown_slug_returns_empty(synthetic_wiki: Path) -> None:
    assert wiki_query.neighbors("ghost-page", depth=2) == []


# ----- provenance_for ------------------------------------------------


def test_provenance_for_collects_both_frontmatter_and_body(
    synthetic_wiki: Path,
) -> None:
    refs = wiki_query.provenance_for("bdnf")
    # Frontmatter source + 2 body anchors → 3 distinct refs
    assert "[raw/books/health/Spark.pdf#p1-228]" in refs
    assert "[raw/books/health/Spark.pdf#p43]" in refs
    assert "[raw/books/health/Spark.pdf#p41]" in refs
    assert len(refs) == 3


# ----- index path ----------------------------------------------------


def test_loads_from_agents_index_when_present(
    synthetic_wiki: Path, monkeypatch
) -> None:
    """If wiki/AGENTS_INDEX.json exists, lookups go through it (fast path)."""
    idx_data = {
        "version": 1,
        "page_count": 1,
        "pages": [
            {
                "slug": "bdnf",
                "title": "BDNF (from JSON)",
                "type": "concept",
                "path": "wiki/concepts/bdnf.md",
                "summary": "Loaded from JSON, not filesystem",
                "tags": ["from-json"],
                "aliases": ["json-alias"],
            }
        ],
        "by_slug": {"bdnf": 0},
        "by_alias": {"json-alias": "bdnf"},
        "by_tag": {"from-json": ["bdnf"]},
    }
    (synthetic_wiki / "AGENTS_INDEX.json").write_text(
        json.dumps(idx_data), encoding="utf-8"
    )
    wiki_query._reset_caches()

    # The PageStub list comes from the JSON, so the title will be the
    # "(from JSON)" variant — proves we used the index.
    pages = wiki_query.list_pages()
    titles = {p.title for p in pages}
    assert "BDNF (from JSON)" in titles

    # And alias resolution uses the JSON's alias map
    p = wiki_query.find_page("json-alias")
    assert p is not None and p.slug == "bdnf"


def test_falls_back_to_filesystem_when_index_corrupt(
    synthetic_wiki: Path,
) -> None:
    """Garbage AGENTS_INDEX.json → fall back to walking wiki/ instead
    of crashing or returning empty."""
    (synthetic_wiki / "AGENTS_INDEX.json").write_text("not valid json", encoding="utf-8")
    wiki_query._reset_caches()
    pages = wiki_query.list_pages()
    assert {p.slug for p in pages} == {"bdnf", "hippocampus", "andrej-karpathy"}


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
