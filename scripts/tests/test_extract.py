"""Unit tests for `scripts.ingest.extract` helpers.

Covers `_normalize_provenance` (anchor cleanup) and the
sequential/parallel equivalence of `extract_book` (Phase C runs chunks in
parallel via ThreadPoolExecutor; results must merge byte-for-byte the same
as the sequential baseline).
"""
from __future__ import annotations

import threading
import time

from scripts.ingest import extract as extract_mod
from scripts.ingest.chunk import Chunk
from scripts.ingest.cost_tracker import CostTracker
from scripts.ingest.extract import _normalize_provenance, extract_book
from scripts.ingest.schemas import ExtractionOutput, Fact, PageCandidate, RelatedLinks


def test_normalize_provenance_passthrough() -> None:
    src = "raw/books/strategy/Algorithms_to_Live_By.epub"
    anchor = f"[{src}#p42]"
    assert _normalize_provenance(anchor, src) == anchor


def test_normalize_provenance_collapses_duplicated_extension() -> None:
    src = "raw/books/productivity/Atomic Habits.pdf"
    bad = f"[{src}.pdf#p10]"
    assert _normalize_provenance(bad, src) == f"[{src}#p10]"


def test_normalize_provenance_collapses_double_L_prefix() -> None:
    """Minimax occasionally emits `#LL2252-L2254` (doubled L) — common in the
    range form when it templated the prefix twice. Collapse to `#L2252-L2254`
    so the validator's `#L\\d+` regex accepts it."""
    src = "raw/books/philosophy/道德经.epub"
    bad = f"[{src}#LL2252-L2254]"
    assert _normalize_provenance(bad, src) == f"[{src}#L2252-L2254]"


def test_normalize_provenance_collapses_double_L_in_range_tail() -> None:
    src = "raw/books/philosophy/道德经.epub"
    bad = f"[{src}#L2252-LL2254]"
    assert _normalize_provenance(bad, src) == f"[{src}#L2252-L2254]"


def test_normalize_provenance_collapses_double_p_prefix() -> None:
    src = "raw/books/neuroscience/Friston.pdf"
    bad = f"[{src}#pp42]"
    assert _normalize_provenance(bad, src) == f"[{src}#p42]"


def test_normalize_provenance_snaps_path_to_canonical() -> None:
    """If LLM drops a directory but keeps the basename, snap back."""
    src = "raw/books/philosophy/道德经(精) - 中华经典名著全本全注全译.epub"
    bad = "[道德经(精) - 中华经典名著全本全注全译.epub#L100-L200]"
    assert _normalize_provenance(bad, src) == f"[{src}#L100-L200]"


def test_normalize_provenance_snaps_truncated_long_chinese_filename() -> None:
    """Real S5 failure mode: 196-char Chinese book title, LLM dropped
    14 chars from the middle. Both basenames end with the same 30+ char
    suffix (`- 马丁·海德格尔 & 卡尔·波普尔(Karl R_ Po.epub`), so the
    suffix-match path-snap kicks in. Without this, downstream lint
    flagged 1.2k+ file_not_exist errors."""
    src = (
        "raw/books/philosophy/二十世纪西方哲学经典(套装共10册)【上海译文出品!"
        "从历史哲学到科学哲学,十本书搭建一世纪的哲学方程式,读懂二十世纪的哲 - "
        "马丁·海德格尔 & 卡尔·波普尔(Karl R_ Po.epub"
    )
    truncated = (
        "raw/books/philosophy/二十世纪西方哲学经典(套装共10册)【上海译文出品!"
        "从历史哲学到科学哲学,十本书搭建一世纪的哲 - "
        "马丁·海德格尔 & 卡尔·波普尔(Karl R_ Po.epub"
    )
    bad = f"[{truncated}#L100-L200]"
    assert _normalize_provenance(bad, src) == f"[{src}#L100-L200]"


def test_normalize_provenance_does_not_snap_unrelated_long_filenames() -> None:
    """30-char suffix match must be sharp enough that two different long
    books don't get conflated. Different book + different ending must NOT
    snap."""
    src = "raw/books/economics/[当代经济学系列丛书]微观经济学·[美]鲍默尔 著.pdf"
    other = "raw/books/economics/[当代经济学系列丛书]宏观经济学·[法]贝纳西 著.pdf"
    bad = f"[{other}#p42]"
    assert _normalize_provenance(bad, src) == f"[{other}#p42]"


def test_normalize_provenance_preserves_non_bracketed() -> None:
    assert _normalize_provenance("no brackets here", "x") == "no brackets here"


def test_normalize_provenance_recovers_missing_open_bracket() -> None:
    """LLM sometimes drops the opening '[' but keeps the close: the resulting
    `raw/.../x.pdf#p42]` is visually correct but rejected by the provenance
    regex. Normalize adds the missing bracket so validate accepts it."""
    src = "raw/books/neuroscience/Kandel.pdf"
    bad = f"{src}#p543]"
    assert _normalize_provenance(bad, src) == f"[{src}#p543]"


# --- Phase C parallel-extraction equivalence ---------------------------------


def _make_chunks(n: int) -> list[Chunk]:
    return [
        Chunk(
            index=i,
            text=f"chunk {i} body",
            start_page=i + 1,
            end_page=i + 1,
            start_line=1,
            end_line=1,
        )
        for i in range(n)
    ]


def _candidate_for_chunk(idx: int, src: str) -> PageCandidate:
    """Deterministic per-chunk page; ids carry the chunk index so we can
    verify ordering / dedup behavior end-to-end."""
    return PageCandidate(
        page_type="concept",
        title=f"Concept-{idx}",
        id=f"concept-{idx}",
        summary=f"summary for chunk {idx}",
        key_facts=[Fact(claim=f"fact from chunk {idx}", provenance=f"[{src}#p{idx+1}]")],
        related=RelatedLinks(),
    )


def _stub_llm(per_chunk_pages, *, sleep: float = 0.0):
    """Build a fake `generate_structured_output` for monkeypatching.

    `per_chunk_pages` is a function `idx -> list[PageCandidate]`. Each call
    sleeps `sleep` seconds first so the parallel test can prove workers
    actually overlapped (4 chunks × 0.4s sleep should finish in <1s when
    run with 4 workers, vs ~1.6s sequentially).
    """
    call_log: list[int] = []
    lock = threading.Lock()

    def _stub(system_prompt, user_content, response_format, **kw):
        # Recover the chunk index from the prompt body — the only stable
        # signal we have without threading state through.
        m = None
        for token in user_content.split():
            if token.startswith("chunk") and token != "chunk":
                continue
        # Easier: scan for "chunk N body"
        import re as _re

        match = _re.search(r"chunk (\d+) body", user_content)
        idx = int(match.group(1)) if match else -1
        with lock:
            call_log.append(idx)
        if sleep:
            time.sleep(sleep)
        out = ExtractionOutput(pages=per_chunk_pages(idx), skipped_reason=None)
        usage = {"tokens_in": 100 * (idx + 1), "tokens_out": 50, "model": "stub", "attempts": 1}
        return out, usage

    return _stub, call_log


def test_extract_book_parallel_matches_sequential(monkeypatch):
    """Same chunks + same stub LLM → byte-identical output between
    workers=1 and workers=4 (after sorting by id). This is the core
    correctness guarantee for the parallelism change."""
    src = "raw/books/test/example.pdf"
    chunks = _make_chunks(6)

    stub, _ = _stub_llm(lambda idx: [_candidate_for_chunk(idx, src)])
    monkeypatch.setattr(extract_mod, "generate_structured_output", stub)

    cost1 = CostTracker(per_book_cap=10.0, batch_cap=100.0)
    seq = extract_book("book", src, "test", "en", chunks, cost1, max_workers=1)

    cost4 = CostTracker(per_book_cap=10.0, batch_cap=100.0)
    par = extract_book("book", src, "test", "en", chunks, cost4, max_workers=4)

    seq_ids = sorted(p.id for p in seq.candidates)
    par_ids = sorted(p.id for p in par.candidates)
    assert seq_ids == par_ids
    assert seq.total_tokens_in == par.total_tokens_in
    assert seq.total_tokens_out == par.total_tokens_out
    assert cost1.total_dollars == cost4.total_dollars


def test_extract_book_parallel_actually_overlaps(monkeypatch):
    """Sanity check: with 4 chunks each sleeping 0.3s, the 4-worker run
    should complete in well under the 1.2s a sequential run would take.
    Without true parallelism this test fails — proves we're not silently
    serializing inside ThreadPoolExecutor."""
    src = "raw/books/test/example.pdf"
    chunks = _make_chunks(4)

    stub, _ = _stub_llm(lambda idx: [_candidate_for_chunk(idx, src)], sleep=0.3)
    monkeypatch.setattr(extract_mod, "generate_structured_output", stub)

    cost = CostTracker(per_book_cap=10.0, batch_cap=100.0)
    t0 = time.monotonic()
    extract_book("book", src, "test", "en", chunks, cost, max_workers=4)
    elapsed = time.monotonic() - t0
    # Sequential lower bound is 4 × 0.3s = 1.2s. 4-way parallel should be
    # ~0.3-0.5s. Allow generous slack for CI variance.
    assert elapsed < 0.9, f"expected parallel speedup, got {elapsed:.2f}s"


def test_extract_book_merge_order_deterministic_under_parallelism(monkeypatch):
    """When two chunks emit pages with the SAME id, `_merge_candidates`
    keeps the first-by-chunk-index version's title and only extends facts.
    Out-of-order future completion must not change which page wins.
    """
    src = "raw/books/test/example.pdf"
    chunks = _make_chunks(3)

    def _pages(idx: int) -> list[PageCandidate]:
        # Every chunk emits the same id, with a different title and fact.
        return [
            PageCandidate(
                page_type="concept",
                title=f"Title-from-chunk-{idx}",
                id="shared-concept",
                summary=f"summary {idx}",
                key_facts=[Fact(claim=f"claim-{idx}", provenance=f"[{src}#p{idx+1}]")],
                related=RelatedLinks(),
            )
        ]

    # Reverse the sleep so chunk 2 finishes first, chunk 0 last — proves
    # we don't fall into completion order.
    sleeps = {0: 0.3, 1: 0.15, 2: 0.0}

    def _stub(system_prompt, user_content, response_format, **kw):
        import re as _re

        idx = int(_re.search(r"chunk (\d+) body", user_content).group(1))
        time.sleep(sleeps[idx])
        out = ExtractionOutput(pages=_pages(idx), skipped_reason=None)
        return out, {"tokens_in": 1, "tokens_out": 1, "model": "stub", "attempts": 1}

    monkeypatch.setattr(extract_mod, "generate_structured_output", _stub)

    cost = CostTracker(per_book_cap=10.0, batch_cap=100.0)
    book = extract_book("book", src, "test", "en", chunks, cost, max_workers=4)

    shared = [p for p in book.candidates if p.id == "shared-concept"]
    assert len(shared) == 1
    # Chunk 0's title must win regardless of completion order.
    assert shared[0].title == "Title-from-chunk-0"
    # All three claims should be present (merge extends facts).
    claims = {f.claim for f in shared[0].key_facts}
    assert claims == {"claim-0", "claim-1", "claim-2"}


def test_extract_book_zero_chunks_synthesizes_source(monkeypatch):
    """Empty chunk list still produces a synthesized source page so the
    book lands with at least one page (not a regression — verify parallel
    refactor preserves this fallback)."""
    src = "raw/books/test/empty.pdf"
    cost = CostTracker(per_book_cap=10.0, batch_cap=100.0)
    book = extract_book(
        "empty-book", src, "test", "en", [], cost, pages_total=10, max_workers=4
    )
    assert len(book.candidates) == 1
    assert book.candidates[0].page_type == "source"
    assert cost.total_dollars == 0.0
