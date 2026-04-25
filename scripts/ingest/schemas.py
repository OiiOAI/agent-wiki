"""Pydantic schemas for LLM structured output.

These schemas constrain what the LLM can return during Phase C extraction.
They are intentionally permissive on the frontmatter (free-form dict) because
the 5 page types have heterogeneous frontmatter; the `validate.py` module is
where the dict is checked against the per-type required/allowed field matrix.
"""
from __future__ import annotations

import hashlib
import re
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

try:
    from pypinyin import lazy_pinyin as _lazy_pinyin
    _HAS_PYPINYIN = True
except ImportError:
    _HAS_PYPINYIN = False

PageType = Literal["entity", "concept", "topic", "source", "analysis"]

_KEBAB_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")
_NON_KEBAB_CHARS_RE = re.compile(r"[^a-z0-9-]+")
_MULTI_DASH_RE = re.compile(r"-{2,}")


def slugify_id(value: str) -> str:
    """Coerce any string into a kebab-case slug matching PageCandidate.id.

    LLMs occasionally return ids with spaces, uppercase, or CJK characters
    (especially for Chinese-language books). Rather than fail the whole
    chunk, normalize: lowercase → transliterate CJK via pypinyin when
    available → replace remaining non-kebab chars with dashes → collapse
    runs → trim. Falls back to a hash-derived slug if the input yields
    no usable ASCII content.
    """
    s = value.strip().lower()
    if _KEBAB_RE.match(s):
        return s
    if _HAS_PYPINYIN and any(ord(c) > 127 for c in s):
        s = "-".join(_lazy_pinyin(s))
    s = _NON_KEBAB_CHARS_RE.sub("-", s)
    s = _MULTI_DASH_RE.sub("-", s).strip("-")
    if len(s) < 2 or not _KEBAB_RE.match(s):
        digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:10]
        s = f"page-{digest}"
    return s
# Note: "conflict" pages are produced by conflict_check.py (Phase F), not by
# the Phase C extractor — LLM should never emit conflict pages directly.


class Fact(BaseModel):
    """A single factual claim with mandatory provenance anchor."""

    claim: str = Field(..., min_length=1, description="One sentence.")
    provenance: str = Field(
        ...,
        min_length=1,
        description=(
            "Must be of form '[raw/...#pN]' or '[raw/...#Lx-y]'. "
            "For book ingests, prefer page anchor '[raw/books/<disc>/<book>.pdf#pN]'."
        ),
    )


class RelatedLinks(BaseModel):
    broader: list[str] = Field(default_factory=list)
    narrower: list[str] = Field(default_factory=list)
    adjacent: list[str] = Field(default_factory=list)
    concepts: list[str] = Field(default_factory=list)
    topics: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)


class PageCandidate(BaseModel):
    """One wiki page candidate extracted from a chunk.

    The LLM returns a list of these; compile.py renders each to a markdown
    page in tmp/ingest_staging/<book_stem>/.
    """

    page_type: PageType
    title: str = Field(..., min_length=1)
    id: str = Field(..., pattern=r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")

    @field_validator("id", mode="before")
    @classmethod
    def _coerce_id(cls, v):
        if not isinstance(v, str) or not v.strip():
            return v
        return slugify_id(v)

    aliases: list[str] = Field(default_factory=list)
    frontmatter_extra: dict = Field(
        default_factory=dict,
        description=(
            "Type-specific fields. For 'source': source_kind/source_path/"
            "source_date/source_author/reliability. For 'entity': canonical/"
            "confidence. For 'concept'/'topic'/'analysis': confidence/question."
        ),
    )
    summary: str = Field(..., min_length=1, description="One-paragraph summary.")
    key_facts: list[Fact] = Field(default_factory=list)
    inferences: list[str] = Field(
        default_factory=list,
        description="Each must be sensible as 'Inference: <text>' in rendered output.",
    )
    uncertainties: list[str] = Field(
        default_factory=list,
        description="Each rendered as 'Uncertain: <text>'.",
    )
    related: RelatedLinks = Field(default_factory=RelatedLinks)
    tags: list[str] = Field(default_factory=list)


class ExtractionOutput(BaseModel):
    """Single-chunk LLM response envelope."""

    pages: list[PageCandidate] = Field(default_factory=list)
    skipped_reason: Optional[str] = Field(
        default=None,
        description=(
            "Non-null iff the chunk contains nothing worth promoting to wiki "
            "(e.g., publisher boilerplate, index pages)."
        ),
    )


# ---------------- Frontmatter schema matrix ----------------
# Used by validate.check_frontmatter_schema. Keys are required fields; items in
# OPTIONAL_FIELDS are allowed but not required.

COMMON_REQUIRED = {"title", "type", "status", "created", "updated", "sources"}

REQUIRED_FIELDS: dict[str, set[str]] = {
    "entity": COMMON_REQUIRED | {"aliases", "canonical", "confidence"},
    "concept": COMMON_REQUIRED | {"confidence"},
    "topic": COMMON_REQUIRED | {"confidence"},
    "source": COMMON_REQUIRED
    | {
        "source_kind",
        "source_path",
        "source_date",
        "source_author",
        "reliability",
    },
    "analysis": COMMON_REQUIRED | {"question", "confidence"},
    "conflict": COMMON_REQUIRED | {"conflict_scope", "confidence", "affected_pages"},
}

OPTIONAL_FIELDS: dict[str, set[str]] = {
    "entity": {"tags", "related"},
    "concept": {"tags", "related"},
    "topic": {"tags", "related"},
    "source": {"tags", "source_origin"},
    "analysis": {"tags", "related_pages"},
    "conflict": {"tags"},
}

ALLOWED_STATUS = {"draft", "active", "deprecated", "conflicted"}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}
ALLOWED_RELIABILITY = {"low", "medium", "high", "unknown"}
ALLOWED_SOURCE_KIND = {
    "article",
    "paper",
    "book",
    "meeting",
    "note",
    "dataset",
    "image",
    "other",
}
ALLOWED_CONFLICT_SCOPE = {
    "factual",
    "definitional",
    "temporal",
    "methodological",
    "naming",
    "other",
}
