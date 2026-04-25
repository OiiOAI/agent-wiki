"""Phase C: chunks → PageCandidate list via the LLM.

One `ExtractionOutput` call per chunk. Merges all candidates for the book
at the end; de-duplicates by `id`. A `source` page is merged across chunks:
if multiple chunks emit a `source` candidate, the first one wins but its
`key_facts` are extended with all subsequent chunks' source-page facts.

If no chunk emits a `source` candidate, a minimal one is synthesized so every
book lands with at least one source page in `wiki/sources/`.
"""
from __future__ import annotations

import concurrent.futures
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

from .chunk import Chunk
from .cost_tracker import CostTracker
from .llm_client import generate_structured_output
from .prompts import SYSTEM_PROMPT_EXTRACTOR, build_user_prompt
from .schemas import ExtractionOutput, Fact, PageCandidate, RelatedLinks


def _default_chunk_workers() -> int:
    """Read INGEST_PARALLEL_CHUNKS at call time so tests can monkeypatch the env."""
    try:
        return max(1, int(os.environ.get("INGEST_PARALLEL_CHUNKS", "4")))
    except (TypeError, ValueError):
        return 4


_DUP_EXT_RE = re.compile(r"(\.(?:pdf|epub|md|txt))(?:\1)+", re.IGNORECASE)
_DUP_LINE_PREFIX_RE = re.compile(r"\bL{2,}(\d)")
_DUP_PAGE_PREFIX_RE = re.compile(r"\bp{2,}(\d)")


def _normalize_provenance(anchor: str, source_path: str) -> str:
    """Clean up common LLM slips in provenance strings.

    * Collapse repeated extensions: `.md.md` → `.md`, `.pdf.pdf` → `.pdf`.
    * Collapse doubled anchor prefixes: `#LL123` → `#L123`, `#pp4` → `#p4`.
      Also handles the range form `L10-LL20` → `L10-L20`.
    * If the path portion clearly intends this book, pin it to the exact
      `source_path` so small variations (adding/removing leading dir) do not
      leak through.
    """
    anchor = anchor.strip()
    # LLM occasionally drops the opening bracket but keeps the close:
    # `raw/books/.../x.pdf#p42]` instead of `[raw/.../x.pdf#p42]`. Recover.
    if (
        not anchor.startswith("[")
        and anchor.endswith("]")
        and anchor.startswith("raw/")
    ):
        anchor = "[" + anchor
    if not anchor.startswith("[") or "#" not in anchor:
        return anchor
    inner = anchor.strip("[]")
    path_part, sep, anchor_part = inner.partition("#")
    path_part = _DUP_EXT_RE.sub(r"\1", path_part)
    anchor_part = _DUP_LINE_PREFIX_RE.sub(r"L\1", anchor_part)
    anchor_part = _DUP_PAGE_PREFIX_RE.sub(r"p\1", anchor_part)
    # If LLM fuzzed the path (e.g. dropped a folder) but kept the basename,
    # snap it back to the canonical source_path. Also handles long Chinese
    # filenames where the LLM truncated 10-20 chars from the middle: if the
    # last 30 characters of both basenames match exactly, it's the same book.
    if path_part != source_path:
        emitted_name = Path(path_part).name
        canonical_name = Path(source_path).name
        if emitted_name == canonical_name:
            path_part = source_path
        elif (
            len(canonical_name) > 30
            and len(emitted_name) > 30
            and emitted_name[-30:] == canonical_name[-30:]
        ):
            path_part = source_path
    return f"[{path_part}#{anchor_part}]" if sep else f"[{path_part}]"


@dataclass
class BookExtraction:
    book_stem: str
    source_path: str
    language: str
    candidates: list[PageCandidate] = field(default_factory=list)
    skipped: list[tuple[int, str]] = field(default_factory=list)  # (chunk_idx, reason)
    total_tokens_in: int = 0
    total_tokens_out: int = 0
    failed_chunks: list[int] = field(default_factory=list)


def _anchor_format(source_path: str, has_pages: bool) -> str:
    if has_pages:
        return f"[{source_path}#p<N>]  (use the page number of the sentence you cite)"
    return f"[{source_path}#L<line_start>-<line_end>]  (line range in this chunk)"


def _merge_candidates(existing: list[PageCandidate], new: list[PageCandidate]) -> list[PageCandidate]:
    """Dedup by id; for same id, prefer existing but extend facts/inferences."""
    by_id: dict[str, PageCandidate] = {p.id: p for p in existing}
    for np in new:
        if np.id not in by_id:
            by_id[np.id] = np
            existing.append(np)
            continue
        prev = by_id[np.id]
        # extend rather than replace
        known_claims = {f.claim for f in prev.key_facts}
        for f in np.key_facts:
            if f.claim not in known_claims:
                prev.key_facts.append(f)
        prev.inferences.extend(i for i in np.inferences if i not in prev.inferences)
        prev.uncertainties.extend(u for u in np.uncertainties if u not in prev.uncertainties)
        for bucket in ("broader", "narrower", "adjacent", "concepts", "topics", "entities"):
            dst = getattr(prev.related, bucket)
            src = getattr(np.related, bucket)
            for link in src:
                if link not in dst:
                    dst.append(link)
    return existing


def _synthesize_source_page(
    book_stem: str, source_path: str, has_pages: bool, pages_total: int | None
) -> PageCandidate:
    """Fallback source page when the LLM did not emit one for this book.

    Always deterministic — it carries only facts derivable from the document
    identity, so no invented knowledge lands in the wiki.
    """
    anchor = (
        f"[{source_path}#p1-p{pages_total}]"
        if has_pages and pages_total
        else f"[{source_path}#L1-L1]"
    )
    title = Path(source_path).stem.replace("_", " ").replace("-", " ").strip() or book_stem
    return PageCandidate(
        page_type="source",
        title=title.title() if title.isascii() else title,
        id=book_stem.lower().replace("_", "-").strip("-") or "source",
        aliases=[],
        frontmatter_extra={
            "source_kind": "book",
            "source_path": source_path,
            "source_author": "",
            "source_date": "",
            "reliability": "unknown",
        },
        summary=(
            f"Auto-synthesized source page for {source_path}. "
            f"Populate author/date/summary manually if needed; the LLM "
            f"did not emit a dedicated source page for this document."
        ),
        key_facts=[Fact(claim=f"Document ingested from {source_path}.", provenance=anchor)],
        inferences=[],
        uncertainties=["Uncertain: auto-synthesized — verify metadata against the source."],
        related=RelatedLinks(),
        tags=[],
    )


def _sanitize_candidate(page: PageCandidate, source_path: str) -> None:
    """Clean LLM output in place: provenance anchors, trimmed extensions."""
    for fact in page.key_facts:
        fact.provenance = _normalize_provenance(fact.provenance, source_path)


def _run_chunk_llm(
    ch: Chunk,
    source_path: str,
    discipline: str,
    language: str,
) -> tuple[int, ExtractionOutput | None, dict, bool]:
    """Build prompt and call the LLM for a single chunk.

    Returns (chunk_index, parsed_output_or_None, usage_dict, has_pages).
    Pure function — no shared-state mutation — so safe to run from a
    ThreadPoolExecutor worker. CostTracker.add_usage is intentionally NOT
    called here; the main thread applies cost in chunk-index order after all
    workers return, which keeps budget enforcement and merge ordering
    deterministic regardless of how the futures finish.
    """
    has_pages = ch.start_page is not None
    page_range = (
        f"p{ch.start_page}-p{ch.end_page}"
        if has_pages
        else f"L{ch.start_line}-L{ch.end_line}"
    )
    user_prompt = build_user_prompt(
        chunk_text=ch.text,
        source_path=source_path,
        discipline=discipline,
        language=language,
        page_range=page_range,
        anchor_format=_anchor_format(source_path, has_pages),
    )
    parsed, usage = generate_structured_output(
        SYSTEM_PROMPT_EXTRACTOR,
        user_prompt,
        ExtractionOutput,
    )
    return ch.index, parsed, usage, has_pages


def extract_book(
    book_stem: str,
    source_path: str,
    discipline: str,
    language: str,
    chunks: list[Chunk],
    cost: CostTracker,
    pages_total: int | None = None,
    max_workers: int | None = None,
) -> BookExtraction:
    result = BookExtraction(
        book_stem=book_stem, source_path=source_path, language=language
    )
    any_pages_anchor = False

    # Phase C-1: run all chunks through the LLM (parallel when worth it).
    # Sequential path is preserved bit-for-bit at workers==1 so behavior
    # hasn't changed for tests / single-chunk books.
    workers = max_workers if max_workers is not None else _default_chunk_workers()
    workers = max(1, min(workers, len(chunks)))
    raw: dict[int, tuple[ExtractionOutput | None, dict, bool]] = {}
    if workers <= 1 or len(chunks) <= 1:
        for ch in chunks:
            idx, parsed, usage, has_pages = _run_chunk_llm(
                ch, source_path, discipline, language
            )
            raw[idx] = (parsed, usage, has_pages)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
            futs = [
                ex.submit(_run_chunk_llm, ch, source_path, discipline, language)
                for ch in chunks
            ]
            for fut in concurrent.futures.as_completed(futs):
                try:
                    idx, parsed, usage, has_pages = fut.result()
                except Exception as e:
                    # Don't lose the book over one rogue chunk; record and move on.
                    print(f"[extract] chunk worker raised: {e}")
                    continue
                raw[idx] = (parsed, usage, has_pages)

    # Phase C-2: apply results in chunk-index order so cost accounting,
    # budget enforcement, and `_merge_candidates` (first-id-wins) match the
    # sequential baseline exactly.
    for idx in sorted(raw.keys()):
        parsed, usage, has_pages = raw[idx]
        any_pages_anchor = any_pages_anchor or has_pages
        tokens_in = usage.get("tokens_in", 0)
        tokens_out = usage.get("tokens_out", 0)
        try:
            cost.add_usage(book_stem, tokens_in, tokens_out)
        except Exception as e:
            result.failed_chunks.append(idx)
            result.skipped.append((idx, f"budget: {e}"))
            break
        result.total_tokens_in += tokens_in
        result.total_tokens_out += tokens_out
        if parsed is None:
            result.failed_chunks.append(idx)
            continue
        if parsed.skipped_reason:
            result.skipped.append((idx, parsed.skipped_reason))
        if parsed.pages:
            for p in parsed.pages:
                _sanitize_candidate(p, source_path)
            _merge_candidates(result.candidates, list(parsed.pages))

    # Collapse multiple source pages (LLM may emit one per chunk when the
    # merge step didn't catch them — different ids, same role).
    source_pages = [p for p in result.candidates if p.page_type == "source"]
    if len(source_pages) > 1:
        primary = source_pages[0]
        known_claims = {f.claim for f in primary.key_facts}
        for extra in source_pages[1:]:
            for f in extra.key_facts:
                if f.claim not in known_claims:
                    primary.key_facts.append(f)
                    known_claims.add(f.claim)
            for inf in extra.inferences:
                if inf not in primary.inferences:
                    primary.inferences.append(inf)
            for unc in extra.uncertainties:
                if unc not in primary.uncertainties:
                    primary.uncertainties.append(unc)
        result.candidates = [
            p for p in result.candidates if p is primary or p.page_type != "source"
        ]

    # Guarantee at least one source page per book.
    if not any(p.page_type == "source" for p in result.candidates):
        result.candidates.append(
            _synthesize_source_page(
                book_stem, source_path, any_pages_anchor, pages_total
            )
        )
    return result
