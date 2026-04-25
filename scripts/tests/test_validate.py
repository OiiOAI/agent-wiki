"""L3: validate — each of the 11 invariants has at least one positive and
one negative test.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from scripts.ingest.compile import render_page
from scripts.ingest.schemas import Fact, PageCandidate, RelatedLinks
from scripts.ingest.validate import (
    check_approval_gate_required,
    check_file_count_threshold,
    check_frontmatter_schema,
    check_id_uniqueness,
    check_inference_uncertain_syntax,
    check_language_consistency,
    check_link_format,
    check_no_unsourced_core_claims,
    check_provenance_format,
    check_raw_write_forbidden,
    check_scope_boundary,
    validate_page,
)

VALID_CONCEPT_MD = """---
id: active-inference
title: Active Inference
type: concept
status: draft
created: 2026-04-22
updated: 2026-04-22
sources:
  - raw/books/neuroscience/Friston.pdf
confidence: medium
tags:
  - neuro
related:
  broader:
    - Free Energy Principle
  narrower: []
  adjacent: []
---

# Active Inference

## Summary

Active Inference frames perception and action as one minimization.

## Key facts

- Agents minimize variational free energy. [raw/books/neuroscience/Friston.pdf#p42]
- Perception and action share the same objective. [raw/books/neuroscience/Friston.pdf#p47]

## Inferences

- Inference: Extends to multi-agent settings.

## Uncertainties

- Uncertain: Scope outside continuous-state systems is unclear.

## Related pages

- Broader: [[Free Energy Principle]]

## Provenance

- Primary source: raw/books/neuroscience/Friston.pdf

## Change notes

- 2026-04-22 — created.
"""


# ---------- 1. frontmatter schema ----------


def test_frontmatter_schema_ok() -> None:
    assert check_frontmatter_schema(VALID_CONCEPT_MD) == []


def test_frontmatter_schema_missing_required() -> None:
    md = VALID_CONCEPT_MD.replace("confidence: medium\n", "")
    errs = check_frontmatter_schema(md)
    assert any("confidence" in str(e) for e in errs)


def test_frontmatter_schema_bogus_status() -> None:
    md = VALID_CONCEPT_MD.replace("status: draft", "status: bogus")
    errs = check_frontmatter_schema(md)
    assert any("status" in str(e) for e in errs)


def test_frontmatter_schema_unknown_type() -> None:
    md = VALID_CONCEPT_MD.replace("type: concept", "type: gizmo")
    errs = check_frontmatter_schema(md)
    assert any("unknown page type" in str(e) for e in errs)


def test_frontmatter_schema_source_page_fields() -> None:
    md = """---
id: src-x
title: Src
type: source
status: draft
created: 2026-04-22
updated: 2026-04-22
sources: []
source_kind: book
source_path: raw/books/x/y.pdf
source_date: 2020
source_author: Someone
reliability: high
---

# Src

## Summary
Body.
"""
    assert check_frontmatter_schema(md) == []


# ---------- 2. provenance format ----------


def test_provenance_format_valid_page_anchor() -> None:
    assert check_provenance_format(VALID_CONCEPT_MD) == []


def test_provenance_format_malformed_anchor() -> None:
    md = VALID_CONCEPT_MD.replace(
        "[raw/books/neuroscience/Friston.pdf#p42]", "[raw/books/neuroscience/Friston.pdf]"
    )
    errs = check_provenance_format(md)
    assert any("malformed" in str(e) for e in errs)


def test_provenance_format_line_anchor_accepted() -> None:
    md = VALID_CONCEPT_MD.replace(
        "[raw/books/neuroscience/Friston.pdf#p42]",
        "[raw/inbox/foo.md#L10-L20]",
    )
    assert check_provenance_format(md) == []


def test_provenance_format_path_with_spaces_accepted() -> None:
    """Real book filenames contain spaces (e.g. 'Atomic Habits_ The life - …'),
    so the provenance regex must accept whitespace in the path segment."""
    md = VALID_CONCEPT_MD.replace(
        "[raw/books/neuroscience/Friston.pdf#p42]",
        "[raw/books/productivity/Atomic Habits_ The life - changing.pdf#p31]",
    ).replace(
        "[raw/books/neuroscience/Friston.pdf#p47]",
        "[raw/books/productivity/Atomic Habits_ The life - changing.pdf#p38]",
    )
    assert check_provenance_format(md) == []


def test_provenance_format_path_with_brackets_accepted() -> None:
    """Chinese-publisher convention puts series labels in [...] inside the
    filename, e.g. `[当代经济学系列丛书]微观经济学.pdf`. The provenance regex
    must match these — earlier `[^\\]]+?` was too strict and stopped at
    the first inner `]`, flagging 4k+ false-positive 'malformed' errors."""
    md = VALID_CONCEPT_MD.replace(
        "[raw/books/neuroscience/Friston.pdf#p42]",
        "[raw/books/economics/[MBA教材精品译丛]微观经济学.pdf#p43]",
    ).replace(
        "[raw/books/neuroscience/Friston.pdf#p47]",
        "[raw/books/business/[工商管理精要]兼并与收购·[美]P.S.萨德沙纳姆 著.pdf#p145]",
    )
    assert check_provenance_format(md) == []


def test_provenance_format_two_anchors_one_line() -> None:
    """Multiple provenance anchors on a single line must each match
    independently — non-greedy regex behavior."""
    md = VALID_CONCEPT_MD.replace(
        "[raw/books/neuroscience/Friston.pdf#p42]",
        "[raw/books/A.pdf#p1] cited by [raw/books/B.pdf#p2]",
    )
    # The two synthesized anchors should both pass; only the original
    # second anchor remains in place. Either way: zero malformed errors.
    errs = check_provenance_format(md)
    assert all("malformed" not in str(e) for e in errs)


def test_provenance_format_page_out_of_range(tmp_path: Path) -> None:
    # create a fake referenced file so file-existence passes
    (tmp_path / "raw" / "books" / "neuroscience").mkdir(parents=True)
    (tmp_path / "raw" / "books" / "neuroscience" / "Friston.pdf").write_bytes(b"%PDF-")
    errs = check_provenance_format(
        VALID_CONCEPT_MD,
        repo_root=tmp_path,
        max_pages_lookup={"raw/books/neuroscience/Friston.pdf": 20},
    )
    assert any("out of range" in str(e) for e in errs)


# ---------- 3. inference / uncertain syntax ----------


def test_inference_uncertain_syntax_valid() -> None:
    assert check_inference_uncertain_syntax(VALID_CONCEPT_MD) == []


def test_inference_midsentence_flagged() -> None:
    md = VALID_CONCEPT_MD.replace(
        "- Inference: Extends to multi-agent settings.",
        "This is true. Inference: X. And then Y.",
    )
    errs = check_inference_uncertain_syntax(md)
    assert errs, "mid-sentence 'Inference:' should be flagged"


# ---------- 4. id uniqueness ----------


def test_id_uniqueness_ok() -> None:
    assert check_id_uniqueness(VALID_CONCEPT_MD, existing_ids=set()) == []


def test_id_uniqueness_collision() -> None:
    errs = check_id_uniqueness(VALID_CONCEPT_MD, existing_ids={"active-inference"})
    assert errs and "duplicate" in str(errs[0])


# ---------- 5. link format ----------


def test_link_format_ok() -> None:
    assert check_link_format(VALID_CONCEPT_MD) == []


def test_link_format_empty() -> None:
    md = VALID_CONCEPT_MD.replace("[[Free Energy Principle]]", "[[]]")
    errs = check_link_format(md)
    assert errs


# ---------- 6. no unsourced core claims ----------


def test_no_unsourced_core_claims_ok() -> None:
    assert check_no_unsourced_core_claims(VALID_CONCEPT_MD) == []


def test_unsourced_claim_flagged() -> None:
    md = VALID_CONCEPT_MD.replace(
        "- Agents minimize variational free energy. [raw/books/neuroscience/Friston.pdf#p42]",
        "- Agents minimize variational free energy.",
    )
    errs = check_no_unsourced_core_claims(md)
    assert errs


# ---------- 7. scope boundary ----------


def test_scope_boundary_ok_when_names_in_source() -> None:
    source = (
        "Friston proposed that agents minimize variational free energy. "
        "Perception and action share one objective."
    )
    # page has 'Active Inference' and 'Free Energy Principle' — neither in
    # the source. We accept that for Key facts because the check only looks
    # at entities in the Key-facts section.
    errs = check_scope_boundary(VALID_CONCEPT_MD, source_text=source)
    # Source is tiny and the key-facts bullets mention no TitleCase beyond
    # general words → we expect no false positives.
    for e in errs:
        # the titlecase detector only triggers on tokens >= min_token_len
        assert "Friston" not in str(e) or "Friston" not in source


def test_scope_boundary_flags_outside_entity() -> None:
    source = "generic prose"
    md = VALID_CONCEPT_MD.replace(
        "## Key facts\n\n- Agents minimize variational free energy. [raw/books/neuroscience/Friston.pdf#p42]",
        "## Key facts\n\n- Noam Chomsky invented this idea. [raw/books/neuroscience/Friston.pdf#p42]",
    )
    errs = check_scope_boundary(md, source_text=source)
    assert errs and any("Noam Chomsky" in str(e) for e in errs)


def test_scope_boundary_accepts_abbreviation_compound() -> None:
    """Compound technical terms like 'IV S4' should pass when both tokens
    appear in source, even though each token is too short (2 chars) to
    trigger the paraphrase-tolerance path."""
    source = (
        "The voltage sensor is formed by the S4 segment in each transmembrane "
        "domain (I, II, III, and IV). Movement of S4 in domain IV is slower "
        "and associated with inactivation."
    )
    md = VALID_CONCEPT_MD.replace(
        "- Agents minimize variational free energy. [raw/books/neuroscience/Friston.pdf#p42]",
        "- IV S4 moves slowly during inactivation. [raw/books/neuroscience/Friston.pdf#p42]",
    )
    errs = check_scope_boundary(md, source_text=source)
    # "IV S4" should not be flagged — both tokens are literally in source.
    assert not any("IV S4" in str(e) for e in errs), f"unexpected: {errs}"


# ---------- 8. file count threshold ----------


def test_file_count_threshold_under_limit_ok() -> None:
    assert check_file_count_threshold([f"a{i}.md" for i in range(5)]) == []


def test_file_count_threshold_over_limit_requires_approval() -> None:
    paths = [f"a{i}.md" for i in range(20)]
    assert check_file_count_threshold(paths) != []
    assert check_file_count_threshold(paths, approved_batch=True) == []


# ---------- 9. approval gate required ----------


def test_approval_gate_delete_blocks() -> None:
    assert check_approval_gate_required("delete") != []
    assert check_approval_gate_required("delete", approved=True) == []


def test_approval_gate_create_ok() -> None:
    assert check_approval_gate_required("create") == []


# ---------- 10. raw write forbidden ----------


def test_raw_write_forbidden_blocks_raw_path() -> None:
    assert check_raw_write_forbidden("raw/inbox/new.md") != []
    assert check_raw_write_forbidden("./raw/inbox/new.md") != []


def test_raw_write_manifest_allowed() -> None:
    # the manifest is an explicit exception (also enforced by block_raw_edits.py)
    assert check_raw_write_forbidden("raw/inbox/_manifest.md") == []


def test_wiki_write_ok() -> None:
    assert check_raw_write_forbidden("wiki/concepts/foo.md") == []


# ---------- 11. language consistency ----------


def test_language_consistency_english_match() -> None:
    errs = check_language_consistency(VALID_CONCEPT_MD, source_text="English source about Friston.")
    assert errs == []


def test_language_consistency_mismatch_flagged() -> None:
    errs = check_language_consistency(VALID_CONCEPT_MD, source_text="中文原文，大量汉字。" * 50)
    assert errs


def test_language_consistency_chinese_body_not_fooled_by_english_provenance() -> None:
    """Chinese pages have long `[raw/.../book.epub#L...]` anchors in their
    key-facts bullets. The raw Latin-char count from those anchors used to
    outvote the CJK body and flag zh pages as 'en'. Strip structural Latin
    (anchors, wikilinks, SOP section headers) before detecting."""
    md = """---
id: ai-bing-bi-sheng
title: 哀兵必胜
type: concept
status: draft
created: '2026-04-22'
updated: '2026-04-22'
sources:
  - '[raw/books/philosophy/道德经.epub#L1-L1]'
confidence: high
tags:
  - 道家思想
related:
  broader: []
  narrower: []
  adjacent: []
---

# 哀兵必胜

## Summary

老子六十九章提出的军事思想，指被迫自卫、心情哀伤的一方能够获胜。

## Key facts

- 抗兵相加，哀者胜矣. [raw/books/philosophy/道德经(精) - 中华经典名著全本全注全译.epub#L4778-L4788]
- 田单设法让燕军割掉被俘齐军的鼻子使自己的军队变为哀兵. [raw/books/philosophy/道德经(精) - 中华经典名著全本全注全译.epub#L4795-L4815]

## Related pages

- Concepts: [[不战而屈人之兵]]

## Provenance

- Primary source: [raw/books/philosophy/道德经.epub#L1-L1]
"""
    errs = check_language_consistency(md, source_text="中文原文，大量汉字。" * 50)
    assert errs == [], f"Chinese page wrongly flagged: {errs}"


# ---------- orchestrator ----------


def test_validate_page_clean() -> None:
    errs = validate_page(
        VALID_CONCEPT_MD,
        existing_ids=set(),
        source_text="Friston proposed variational free energy minimization. Perception and action.",
        page_path="tmp/ingest_staging/x/concepts/active-inference.md",
    )
    # the orchestrator should produce no errors for a valid page
    assert errs == [], f"unexpected errors: {errs}"


def test_validate_page_detects_multiple_issues() -> None:
    bad = VALID_CONCEPT_MD.replace("status: draft", "status: bogus").replace(
        "[raw/books/neuroscience/Friston.pdf#p42]", "[raw/books/neuroscience/Friston.pdf]"
    )
    errs = validate_page(
        bad,
        existing_ids=set(),
        source_text="English source text.",
        page_path="tmp/x/y.md",
    )
    rules = {e.rule for e in errs}
    assert "frontmatter_schema" in rules
    assert "provenance_format" in rules


def test_validate_page_on_rendered_output() -> None:
    page = PageCandidate(
        page_type="concept",
        title="Active Inference",
        id="active-inference",
        summary="Short body.",
        key_facts=[
            Fact(
                claim="Agents minimize free energy",
                provenance="[raw/books/neuroscience/Friston.pdf#p42]",
            )
        ],
        related=RelatedLinks(broader=["Free Energy Principle"]),
    )
    md = render_page(page, source_provenance="raw/books/neuroscience/Friston.pdf")
    errs = validate_page(
        md,
        existing_ids=set(),
        source_text="Active Inference from Friston minimize free energy.",
        page_path="tmp/ingest_staging/x/concepts/active-inference.md",
    )
    # Must be clean for the compile→validate handshake.
    assert errs == [], f"compile→validate handshake broken: {errs}"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
