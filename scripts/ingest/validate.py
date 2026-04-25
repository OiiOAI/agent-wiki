"""Phase E: the 11 SOP invariants.

Each `check_*` function takes a rendered page (or batch) and returns a list
of `ValidationError` (empty = OK). They do NOT fix issues — the caller
decides whether to skip the page or fail the book.

The invariants are derived directly from WIKI_SOP.md + AGENT_PROTOCOL.md:

  1  check_frontmatter_schema        — required/optional fields per type
  2  check_provenance_format         — `[raw/...#pN]` or `[raw/...#Lx-y]`
  3  check_inference_uncertain_syntax— `Inference:` / `Uncertain:` prefixes
  4  check_id_uniqueness             — id not already in wiki/index.md
  5  check_link_format               — `[[Page]]` obsidian style, non-empty
  6  check_no_unsourced_core_claims  — every `Key facts` bullet has a [raw/…]
  7  check_scope_boundary            — entities in page title/facts appear
                                       in source chunk (heuristic)
  8  check_file_count_threshold      — batch >10 triggers approval gate
  9  check_approval_gate_required    — action in {delete,merge,rename} blocks
 10  check_raw_write_forbidden       — target path must not start with raw/
 11  check_language_consistency      — page language matches source language
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml

from .schemas import (
    ALLOWED_CONFIDENCE,
    ALLOWED_CONFLICT_SCOPE,
    ALLOWED_RELIABILITY,
    ALLOWED_SOURCE_KIND,
    ALLOWED_STATUS,
    OPTIONAL_FIELDS,
    REQUIRED_FIELDS,
)


@dataclass
class ValidationError:
    rule: str
    message: str
    page_path: str | None = None

    def __str__(self) -> str:
        where = f" ({self.page_path})" if self.page_path else ""
        return f"[{self.rule}] {self.message}{where}"


# ------------------------- helpers -------------------------

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
_PROVENANCE_RE = re.compile(
    # Book filenames may contain spaces ("Atomic Habits_ The life - …") AND
    # brackets ("[当代经济学系列丛书]微观经济学.pdf"). We allow any non-newline
    # character in the path; the trailing `#<anchor>]` pattern is what
    # delimits the match — non-greedy so multiple anchors on one line work.
    r"\[raw/[^\n]+?\.(?:pdf|epub|md|txt)"
    r"#(?:p\d+(?:-p?\d+)?|L\d+(?:-L?\d+)?)\]"
)
_WIKILINK_RE = re.compile(r"\[\[([^\[\]]*?)\]\]")
_INFERENCE_PREFIX_RE = re.compile(r"^(?:-\s*)?Inference:\s+.+", re.MULTILINE)
_UNCERTAIN_PREFIX_RE = re.compile(r"^(?:-\s*)?Uncertain:\s+.+", re.MULTILINE)
_KEY_FACTS_SECTION_RE = re.compile(r"^## Key facts\n(.*?)(?=^## |\Z)", re.DOTALL | re.MULTILINE)


def _parse_frontmatter(md_text: str) -> dict | None:
    m = _FRONTMATTER_RE.match(md_text)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return None


def _body_without_frontmatter(md_text: str) -> str:
    m = _FRONTMATTER_RE.match(md_text)
    return md_text[m.end() :] if m else md_text


# ------------------------- 1. frontmatter schema -------------------------


def check_frontmatter_schema(md_text: str, *, page_path: str | None = None) -> list[ValidationError]:
    errs: list[ValidationError] = []
    fm = _parse_frontmatter(md_text)
    if fm is None:
        errs.append(ValidationError("frontmatter_schema", "no YAML frontmatter found", page_path))
        return errs

    ptype = fm.get("type")
    if ptype not in REQUIRED_FIELDS:
        errs.append(
            ValidationError(
                "frontmatter_schema",
                f"unknown page type: {ptype!r}",
                page_path,
            )
        )
        return errs

    required = REQUIRED_FIELDS[ptype]
    allowed = required | OPTIONAL_FIELDS.get(ptype, set()) | {"id"}

    missing = required - set(fm.keys())
    if missing:
        errs.append(
            ValidationError(
                "frontmatter_schema",
                f"missing required fields for {ptype}: {sorted(missing)}",
                page_path,
            )
        )

    unknown = set(fm.keys()) - allowed
    if unknown:
        errs.append(
            ValidationError(
                "frontmatter_schema",
                f"unknown frontmatter fields for {ptype}: {sorted(unknown)}",
                page_path,
            )
        )

    # enum checks
    if "status" in fm and fm["status"] not in ALLOWED_STATUS:
        errs.append(
            ValidationError(
                "frontmatter_schema",
                f"invalid status {fm['status']!r}; allowed={sorted(ALLOWED_STATUS)}",
                page_path,
            )
        )
    if "confidence" in fm and fm["confidence"] not in ALLOWED_CONFIDENCE:
        errs.append(
            ValidationError(
                "frontmatter_schema",
                f"invalid confidence {fm['confidence']!r}",
                page_path,
            )
        )
    if ptype == "source":
        if fm.get("source_kind") not in ALLOWED_SOURCE_KIND:
            errs.append(
                ValidationError(
                    "frontmatter_schema",
                    f"invalid source_kind {fm.get('source_kind')!r}",
                    page_path,
                )
            )
        if fm.get("reliability") not in ALLOWED_RELIABILITY:
            errs.append(
                ValidationError(
                    "frontmatter_schema",
                    f"invalid reliability {fm.get('reliability')!r}",
                    page_path,
                )
            )
    if ptype == "conflict":
        if fm.get("conflict_scope") not in ALLOWED_CONFLICT_SCOPE:
            errs.append(
                ValidationError(
                    "frontmatter_schema",
                    f"invalid conflict_scope {fm.get('conflict_scope')!r}",
                    page_path,
                )
            )

    return errs


# ------------------------- 2. provenance format -------------------------


def check_provenance_format(
    md_text: str,
    *,
    page_path: str | None = None,
    repo_root: Path | None = None,
    max_pages_lookup: dict[str, int] | None = None,
) -> list[ValidationError]:
    """`[raw/...#pN]` or `[raw/...#Lx-y]` syntactic check. If `repo_root`
    given, also asserts file existence. If `max_pages_lookup[<path>]` is
    given, also asserts page number within range.
    """
    errs: list[ValidationError] = []
    body = _body_without_frontmatter(md_text)
    # 1. Find every bracketed `[raw/...]` reference. Strict ones match
    #    the full provenance shape (path + #anchor]); the rest are
    #    flagged as malformed. The loose regex must tolerate `]` inside
    #    the path (Chinese publisher series labels: `[当代经济学]xxx.pdf`)
    #    by anchoring on the file extension rather than the first `]`.
    loose = re.findall(
        r"\[raw/[^\n]+?\.(?:pdf|epub|md|txt)[^\n]*?\]",
        body,
    )
    strict = set(_PROVENANCE_RE.findall(body))
    for ref in loose:
        if ref not in strict:
            errs.append(
                ValidationError(
                    "provenance_format",
                    f"malformed provenance anchor: {ref}",
                    page_path,
                )
            )

    if repo_root is not None:
        for ref in strict:
            # ref looks like '[raw/books/x/y.pdf#p42]' — parse out path+anchor.
            inner = ref.strip("[]")
            path_part, _, anchor = inner.partition("#")
            if not (repo_root / path_part).exists():
                errs.append(
                    ValidationError(
                        "provenance_format",
                        f"referenced file does not exist: {path_part}",
                        page_path,
                    )
                )
                continue
            if max_pages_lookup and anchor.startswith("p"):
                cap = max_pages_lookup.get(path_part)
                if cap is not None:
                    nums = re.findall(r"\d+", anchor)
                    if any(int(n) < 1 or int(n) > cap for n in nums):
                        errs.append(
                            ValidationError(
                                "provenance_format",
                                f"page {anchor} out of range (max={cap}) for {path_part}",
                                page_path,
                            )
                        )
    return errs


# ------------------------- 3. inference/uncertain syntax -------------------------


_QUOTED_TITLE_RE = re.compile(
    # Heuristic: a title-cased phrase ending with a colon, surrounded by
    # quotes (single, double, or curly). Catches `'Active Inference:` /
    # `"Active Inference:` / `'Inference:` inside book/paper titles, which
    # is normal English and not a prefix marker.
    r"['\"‘“]\s*[A-Z][\w\s\-]*?(?:Inference|Uncertain):"
)
_PROPER_NOUN_TITLE_RE = re.compile(
    # Catches the same as a proper noun in prose: `... in Active Inference:`
    # or as a heading: `# Active Inference: ...`. The keyword must be
    # preceded by a single capitalized adjacent word (the modifier).
    r"\b[A-Z][a-z]+\s+(?:Inference|Uncertain):"
)


def check_inference_uncertain_syntax(
    md_text: str, *, page_path: str | None = None
) -> list[ValidationError]:
    errs: list[ValidationError] = []
    body = _body_without_frontmatter(md_text)
    # If the body contains 'Inference:' or 'Uncertain:', they must be line-
    # level prefixes — free-floating 'Inference ' mid-sentence is a smell.
    # Exception: when the colon is part of a quoted title like
    # `'Active Inference: The Free Energy...'`, it's an English book title
    # and not a prefix marker. Pre-mask those before scanning.
    def _mask(m: re.Match) -> str:
        return m.group(0).replace("Inference:", "InferenceX").replace("Uncertain:", "UncertainX")

    masked = _QUOTED_TITLE_RE.sub(_mask, body)
    masked = _PROPER_NOUN_TITLE_RE.sub(_mask, masked)
    for bad in re.finditer(r"(?<!^)(?<!\-\s)Inference:\s", masked):
        # allow after newline + bullet
        start = bad.start()
        prefix = masked[max(0, start - 3) : start]
        if "\n" not in prefix and "- " not in prefix and start > 0:
            errs.append(
                ValidationError(
                    "inference_uncertain_syntax",
                    "'Inference:' appears mid-sentence; must be a bullet prefix",
                    page_path,
                )
            )
            break
    # Symmetric check for Uncertain
    for bad in re.finditer(r"(?<!^)(?<!\-\s)Uncertain:\s", masked):
        start = bad.start()
        prefix = masked[max(0, start - 3) : start]
        if "\n" not in prefix and "- " not in prefix and start > 0:
            errs.append(
                ValidationError(
                    "inference_uncertain_syntax",
                    "'Uncertain:' appears mid-sentence; must be a bullet prefix",
                    page_path,
                )
            )
            break
    return errs


# ------------------------- 4. id uniqueness -------------------------


def check_id_uniqueness(
    md_text: str,
    existing_ids: set[str],
    *,
    page_path: str | None = None,
) -> list[ValidationError]:
    fm = _parse_frontmatter(md_text) or {}
    pid = fm.get("id")
    if not pid:
        return [ValidationError("id_uniqueness", "page has no 'id' frontmatter", page_path)]
    if pid in existing_ids:
        return [
            ValidationError(
                "id_uniqueness",
                f"duplicate id {pid!r} — already in wiki index",
                page_path,
            )
        ]
    return []


# ------------------------- 5. link format -------------------------


def check_link_format(md_text: str, *, page_path: str | None = None) -> list[ValidationError]:
    errs: list[ValidationError] = []
    body = _body_without_frontmatter(md_text)
    for m in _WIKILINK_RE.finditer(body):
        target = m.group(1).strip()
        if not target:
            errs.append(ValidationError("link_format", "empty [[]] wikilink", page_path))
        if "|" in target:
            # [[Page Name|alias]] is acceptable; but the left side must be
            # non-empty
            left, _, _right = target.partition("|")
            if not left.strip():
                errs.append(ValidationError("link_format", "[[|alias]] missing page", page_path))
    return errs


# ------------------------- 6. no unsourced core claims -------------------------


def check_no_unsourced_core_claims(
    md_text: str, *, page_path: str | None = None
) -> list[ValidationError]:
    errs: list[ValidationError] = []
    body = _body_without_frontmatter(md_text)
    match = _KEY_FACTS_SECTION_RE.search(body)
    if not match:
        return errs  # absence of Key facts is caught elsewhere
    section = match.group(1)
    bullets = re.findall(r"^(\s*-\s+.+)$", section, re.MULTILINE)
    for line in bullets:
        stripped = line.strip()
        if stripped.startswith("- (none"):
            continue
        if not _PROVENANCE_RE.search(stripped):
            errs.append(
                ValidationError(
                    "no_unsourced_core_claims",
                    f"Key-facts bullet without [raw/...] anchor: {stripped[:80]}",
                    page_path,
                )
            )
    return errs


# ------------------------- 7. scope boundary -------------------------

_TITLECASE_RE = re.compile(r"\b([A-Z][A-Za-z0-9]+(?:\s+[A-Z][A-Za-z0-9]+){1,3})\b")

# Leading capitalized tokens that are grammatical filler, not part of a
# named entity — strip them before checking source presence.
_LEADING_STOPWORDS = {
    "A", "An", "The",
    "In", "On", "At", "By", "For", "From", "Of", "To", "With", "Into", "Onto",
    "Like", "As", "Via",
    "It", "Its", "This", "That", "These", "Those",
    "His", "Her", "Their", "Our", "Your", "My",
    "Each", "Every", "Any", "Some", "All", "Both", "Such",
    "Is", "Are", "Was", "Were", "Be", "Been", "Being",
}


def check_scope_boundary(
    md_text: str,
    source_text: str,
    *,
    page_path: str | None = None,
    min_token_len: int = 4,
) -> list[ValidationError]:
    """Heuristic: every Title-Cased named entity appearing in Key-facts
    should appear in the source chunk. If it doesn't, the LLM likely
    injected outside knowledge.
    """
    errs: list[ValidationError] = []
    body = _body_without_frontmatter(md_text)
    match = _KEY_FACTS_SECTION_RE.search(body)
    if not match:
        return errs
    section = match.group(1)
    named: set[str] = set()
    for m in _TITLECASE_RE.finditer(section):
        token = m.group(1)
        # Strip leading grammatical fillers like "The X" → "X"; drop if only
        # one word remains (single capitalized words are too noisy to check).
        parts = token.split()
        while parts and parts[0] in _LEADING_STOPWORDS:
            parts = parts[1:]
        if len(parts) < 2:
            continue
        cleaned = " ".join(parts)
        if len(cleaned) >= min_token_len:
            named.add(cleaned)

    source_lower = source_text.lower()
    missing: list[str] = []
    for phrase in named:
        if phrase in source_text:
            continue
        # Paraphrase tolerance: accept the phrase if AT LEAST ONE of its
        # content words (≥3 chars, not a stopword) appears in the source.
        # This flags "Linus Torvalds" (no constituent in source) but tolerates
        # "World Wide Web" (Web in source) or "Small CLI" (both in source).
        words = [
            w.lower()
            for w in phrase.split()
            if len(w) >= 3 and w not in _LEADING_STOPWORDS
        ]
        if words and any(w in source_lower for w in words):
            continue
        # Abbreviation-compound tolerance: if every whitespace-separated token
        # (including short ones like "IV" / "S4") appears literally in the
        # source, the LLM is combining existing terms with standard
        # nomenclature, not fabricating. Example: "IV S4" where source has
        # both "domain IV" and "S4 region".
        tokens = [t for t in phrase.split() if t]
        if tokens and all(t in source_text for t in tokens):
            continue
        missing.append(phrase)
    if missing:
        errs.append(
            ValidationError(
                "scope_boundary",
                f"named entities absent from source chunk: {sorted(missing)[:5]}",
                page_path,
            )
        )
    return errs


# ------------------------- 8. file count threshold -------------------------


def check_file_count_threshold(
    file_paths: Iterable[str], *, approved_batch: bool = False, limit: int = 10
) -> list[ValidationError]:
    paths = list(file_paths)
    if len(paths) > limit and not approved_batch:
        return [
            ValidationError(
                "file_count_threshold",
                f"batch touches {len(paths)} files (>{limit}); requires explicit batch approval",
            )
        ]
    return []


# ------------------------- 9. approval gate -------------------------

_HIGH_RISK_ACTIONS = {"delete", "merge", "rename", "schema_edit", "collapse_conflict"}


def check_approval_gate_required(
    action: str, *, approved: bool = False
) -> list[ValidationError]:
    if action in _HIGH_RISK_ACTIONS and not approved:
        return [
            ValidationError(
                "approval_gate_required",
                f"action {action!r} requires explicit user approval before execution",
            )
        ]
    return []


# ------------------------- 10. raw write forbidden -------------------------


def check_raw_write_forbidden(target_path: str) -> list[ValidationError]:
    normalized = target_path.lstrip("./")
    if normalized.startswith("raw/") and not normalized.endswith("raw/inbox/_manifest.md"):
        return [
            ValidationError(
                "raw_write_forbidden",
                f"attempted write under raw/: {target_path}",
            )
        ]
    return []


# ------------------------- 11. language consistency -------------------------


_PROVENANCE_STRIP_RE = re.compile(r"\[raw/[^\]]+\]")
_WIKILINK_STRIP_RE = re.compile(r"\[\[[^\]]*\]\]")
# SOP template headers and list-prefixes are always English regardless of
# content language — they leak Latin char count and skew detection. Strip
# them before counting.
_STRUCTURAL_TOKENS = (
    "## Summary",
    "## Key facts",
    "## Inferences",
    "## Uncertainties",
    "## Related pages",
    "## Provenance",
    "## Change notes",
    "Primary source:",
    "Inference:",
    "Uncertain:",
    "Broader:",
    "Narrower:",
    "Adjacent:",
    "Concepts:",
    "Topics:",
    "Entities:",
    "page created by auto ingest",
)


def _strip_structural_latin(text: str) -> str:
    """Remove provenance anchors, wikilinks, and SOP-template English tokens
    so language detection focuses on the prose body."""
    text = _PROVENANCE_STRIP_RE.sub("", text)
    text = _WIKILINK_STRIP_RE.sub("", text)
    for token in _STRUCTURAL_TOKENS:
        text = text.replace(token, "")
    return text


def _detect_language(text: str, *, strip_structure: bool = False) -> str:
    sample = _strip_structural_latin(text) if strip_structure else text
    cjk = len(re.findall(r"[\u4e00-\u9fff]", sample))
    latin = len(re.findall(r"[A-Za-z]", sample))
    if cjk == 0 and latin == 0:
        return "unknown"
    return "zh" if cjk > latin else "en"


def check_language_consistency(
    md_text: str, source_text: str, *, page_path: str | None = None
) -> list[ValidationError]:
    src_lang = _detect_language(source_text)
    body = _body_without_frontmatter(md_text)
    page_lang = _detect_language(body, strip_structure=True)
    if src_lang == "unknown" or page_lang == "unknown":
        return []
    if src_lang != page_lang:
        return [
            ValidationError(
                "language_consistency",
                f"page language ({page_lang}) ≠ source language ({src_lang})",
                page_path,
            )
        ]
    return []


# ------------------------- orchestrator -------------------------


def validate_page(
    md_text: str,
    *,
    existing_ids: set[str],
    source_text: str | None = None,
    page_path: str | None = None,
    repo_root: Path | None = None,
    max_pages_lookup: dict[str, int] | None = None,
) -> list[ValidationError]:
    """Run checks 1-7, 10, 11 on a single rendered page.

    Checks 8 and 9 are batch/action-level and are invoked separately by the
    orchestrator.
    """
    errs: list[ValidationError] = []
    errs += check_frontmatter_schema(md_text, page_path=page_path)
    errs += check_provenance_format(
        md_text,
        page_path=page_path,
        repo_root=repo_root,
        max_pages_lookup=max_pages_lookup,
    )
    errs += check_inference_uncertain_syntax(md_text, page_path=page_path)
    errs += check_id_uniqueness(md_text, existing_ids, page_path=page_path)
    errs += check_link_format(md_text, page_path=page_path)
    errs += check_no_unsourced_core_claims(md_text, page_path=page_path)
    if source_text is not None:
        errs += check_scope_boundary(md_text, source_text, page_path=page_path)
        errs += check_language_consistency(md_text, source_text, page_path=page_path)
    if page_path:
        errs += check_raw_write_forbidden(page_path)
    return errs
