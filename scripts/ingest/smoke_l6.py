"""L6 smoke test runner — 5 diverse books end-to-end (dry-run only).

Books are hand-picked in `_BOOKS` below to probe different stress axes:
  * short English trade book   (Atomic Habits)
  * long English academic       (Kandel, Principles of Neural Science 6e, full)
  * pure Chinese EPUB           (道德经 annotated)
  * non-PDF EPUB                (Algorithms to Live By)
  * likely-scanned Chinese PDF  (历史山水渔樵 by 赵汀阳)

Runs Phases A→E (no conflict_check, no commit). Writes:
  tmp/ingest_log/<stem>.log          per-book stdout/stderr
  tmp/ingest_staging/<stem>/*.md     rendered staging pages
  tmp/l6_progress.json               live progress (updated after each book)
  tmp/l6_smoke_report.md             final summary

Usage:
    python -m scripts.ingest.smoke_l6

Expected budget: $5-10. Safety cap: $15 batch / $5 per book.
Expected runtime: ~2 hours (Kandel 212 MB PDF dominates).
"""
from __future__ import annotations

import json
import sys
import time
import traceback
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

from . import chunk as chunk_mod
from . import compile as compile_mod
from . import extract as extract_mod
from . import pdf_to_md
from .cost_tracker import BudgetExceeded, CostTracker
from .validate import validate_page

REPO_ROOT = Path(__file__).resolve().parents[2]

_BOOKS: list[tuple[str, str]] = [
    (
        "atomic-habits",
        "raw/books/productivity/Atomic Habits_ The life - changing million copy bestseller - James Clear.pdf",
    ),
    (
        "kandel-neural-science-6e",
        "raw/books/neuroscience/Eric Kandel PRINCIPLES OF NEURAL SCIENCE Sixth Edition - Eric R Kandel; John Koester; Sarah Mack; Steven Siegelbaum.pdf",
    ),
    (
        "daodejing",
        "raw/books/philosophy/道德经(精) - 中华经典名著全本全注全译.epub",
    ),
    (
        "algorithms-to-live-by",
        "raw/books/strategy/Algorithms_to_Live_By.epub",
    ),
    (
        "lishi-shanshui-yuqiao",
        "raw/books/philosophy/历史山水渔樵 - 赵汀阳.pdf",
    ),
]


@dataclass
class BookResult:
    stem: str
    source_path: str
    status: str = "pending"  # pending | ok | failed | budget_exceeded
    error: str = ""
    converter: str = ""
    language: str = ""
    pages_total: int | None = None
    chunk_count: int = 0
    candidate_count: int = 0
    page_types: dict[str, int] = field(default_factory=dict)
    staging_files: int = 0
    validation_errors: int = 0
    validation_problem_pages: list[str] = field(default_factory=list)
    cost_dollars: float = 0.0
    llm_calls: int = 0
    tokens_in: int = 0
    tokens_out: int = 0
    elapsed_sec: float = 0.0


def _log_line(log_path: Path, msg: str) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.utcnow().isoformat(timespec='seconds')}Z] {msg}\n")


def _process_one(
    stem: str,
    source_rel: str,
    cost: CostTracker,
    staging_root: Path,
    md_cache_dir: Path,
    log_path: Path,
) -> BookResult:
    res = BookResult(stem=stem, source_path=source_rel)
    t0 = time.time()
    src = REPO_ROOT / source_rel
    if not src.exists():
        res.status = "failed"
        res.error = f"source not found: {source_rel}"
        res.elapsed_sec = time.time() - t0
        _log_line(log_path, f"ERROR: {res.error}")
        return res

    try:
        _log_line(log_path, f"Phase A: converting {src.name}")
        meta = pdf_to_md.convert_to_markdown(src, cache_dir=md_cache_dir)
        res.converter = meta.converter
        res.language = meta.language
        res.pages_total = meta.pages_total
        _log_line(
            log_path,
            f"Phase A done: converter={meta.converter} lang={meta.language} "
            f"pages_total={meta.pages_total}",
        )

        text = Path(meta.cache_path).read_text(encoding="utf-8")
        _log_line(log_path, f"Phase B: chunking {len(text):,} chars")
        chunks = chunk_mod.semantic_chunking(text)
        res.chunk_count = len(chunks)
        _log_line(
            log_path,
            f"Phase B done: {len(chunks)} chunks; total words "
            f"{sum(c.word_count for c in chunks):,}",
        )

        disc = src.relative_to(REPO_ROOT / "raw" / "books").parts[0]
        _log_line(log_path, f"Phase C: extracting ({len(chunks)} LLM calls incoming)")
        extraction = extract_mod.extract_book(
            book_stem=stem,
            source_path=source_rel,
            discipline=disc,
            language=meta.language,
            chunks=chunks,
            cost=cost,
            pages_total=meta.pages_total,
        )
        res.candidate_count = len(extraction.candidates)
        for c in extraction.candidates:
            res.page_types[c.page_type] = res.page_types.get(c.page_type, 0) + 1
        _log_line(
            log_path,
            f"Phase C done: {len(extraction.candidates)} candidates "
            f"(types: {res.page_types})",
        )

        if extraction.candidates:
            anchor = (
                f"[{source_rel}#p1-{meta.pages_total}]"
                if meta.pages_total
                else f"[{source_rel}#L1-L1]"
            )
            _log_line(log_path, "Phase D: compiling to staging")
            written = compile_mod.write_staging(
                book_stem=stem,
                candidates=extraction.candidates,
                source_provenance=anchor,
                staging_root=staging_root / stem,
            )
            res.staging_files = len(written)
            _log_line(log_path, f"Phase D done: {len(written)} staging files")

            _log_line(log_path, "Phase E: validating")
            source_text = Path(meta.cache_path).read_text(encoding="utf-8")
            err_pages: list[str] = []
            err_total = 0
            existing_ids: set[str] = set()
            for p in written:
                md = p.read_text(encoding="utf-8")
                errs = validate_page(
                    md,
                    existing_ids=existing_ids,
                    source_text=source_text,
                    page_path=str(p),
                )
                if errs:
                    err_pages.append(p.name)
                    err_total += len(errs)
            res.validation_errors = err_total
            res.validation_problem_pages = err_pages
            _log_line(
                log_path,
                f"Phase E done: {err_total} errors across {len(err_pages)} pages",
            )

        spend = cost.books.get(stem)
        if spend is not None:
            res.cost_dollars = round(spend.dollars, 4)
            res.llm_calls = spend.llm_calls
            res.tokens_in = spend.tokens_in
            res.tokens_out = spend.tokens_out
        res.status = "ok"
    except BudgetExceeded as e:
        res.status = "budget_exceeded"
        res.error = str(e)
        _log_line(log_path, f"BUDGET: {e}")
    except Exception as e:
        res.status = "failed"
        res.error = f"{type(e).__name__}: {e}"
        _log_line(log_path, f"ERROR: {type(e).__name__}: {e}")
        _log_line(log_path, traceback.format_exc())

    res.elapsed_sec = round(time.time() - t0, 2)
    _log_line(
        log_path,
        f"--- done {stem}: status={res.status} elapsed={res.elapsed_sec}s "
        f"cost=${res.cost_dollars}",
    )
    return res


def _write_progress(progress_path: Path, results: list[BookResult], cost: CostTracker) -> None:
    progress_path.parent.mkdir(parents=True, exist_ok=True)
    progress_path.write_text(
        json.dumps(
            {
                "updated": datetime.utcnow().isoformat(timespec="seconds") + "Z",
                "books": [asdict(r) for r in results],
                "total_cost_dollars": round(cost.total_dollars, 4),
                "batch_cap": cost.batch_cap,
            },
            indent=2,
            ensure_ascii=False,
        )
    )


def _render_report(
    report_path: Path, results: list[BookResult], cost: CostTracker, started: datetime
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# L6 Smoke Report")
    lines.append("")
    lines.append(f"- Started: {started.isoformat(timespec='seconds')}Z")
    lines.append(
        f"- Finished: {datetime.utcnow().isoformat(timespec='seconds')}Z"
    )
    ok = [r for r in results if r.status == "ok"]
    failed = [r for r in results if r.status != "ok"]
    clean = [r for r in ok if r.validation_errors == 0]
    lines.append(
        f"- Books: {len(ok)}/{len(results)} ok; "
        f"{len(clean)}/{len(results)} validated clean; {len(failed)} failed"
    )
    lines.append(f"- Total cost: ${cost.total_dollars:.4f}")
    lines.append(f"- Batch cap: ${cost.batch_cap:.2f}")
    lines.append("")
    lines.append("## Per-book breakdown")
    lines.append("")
    lines.append(
        "| Book | Status | Converter | Lang | Pages | Chunks | Pages out | Val errors | Cost | Time |"
    )
    lines.append(
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|"
    )
    for r in results:
        pages_total = r.pages_total if r.pages_total is not None else "-"
        lines.append(
            f"| {r.stem} | {r.status} | {r.converter or '-'} | {r.language or '-'} | "
            f"{pages_total} | {r.chunk_count} | {r.staging_files} | "
            f"{r.validation_errors} | ${r.cost_dollars:.4f} | {r.elapsed_sec:.0f}s |"
        )
    lines.append("")
    lines.append("## Page type distribution")
    lines.append("")
    for r in results:
        if r.page_types:
            types_str = ", ".join(f"{k}={v}" for k, v in sorted(r.page_types.items()))
            lines.append(f"- `{r.stem}`: {types_str}")
        else:
            lines.append(f"- `{r.stem}`: (no pages produced)")
    lines.append("")
    if failed:
        lines.append("## Failures")
        lines.append("")
        for r in failed:
            lines.append(f"### `{r.stem}` — {r.status}")
            lines.append("")
            lines.append(f"Source: `{r.source_path}`")
            lines.append("")
            lines.append(f"```\n{r.error}\n```")
            lines.append("")
    problem_books = [r for r in ok if r.validation_problem_pages]
    if problem_books:
        lines.append("## Validation issues")
        lines.append("")
        for r in problem_books:
            lines.append(
                f"- `{r.stem}`: {r.validation_errors} errors on "
                f"{len(r.validation_problem_pages)} pages: "
                f"{', '.join(r.validation_problem_pages)}"
            )
        lines.append("")
    lines.append("## Reviewer checklist")
    lines.append("")
    lines.append(
        "- [ ] Spot-check 3 pages per book — do facts line up with the source?"
    )
    lines.append(
        "- [ ] Provenance anchors clickable back to `raw/books/…`?"
    )
    lines.append(
        "- [ ] Any `Inference:` / `Uncertain:` labels misapplied?"
    )
    lines.append(
        "- [ ] Scanned Chinese book — did the pipeline fail gracefully?"
    )
    lines.append(
        "- [ ] Cost within budget (expected $5-10)."
    )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    started = datetime.utcnow()
    tmp = REPO_ROOT / "tmp"
    staging_root = tmp / "ingest_staging"
    md_cache_dir = tmp / "md_cache"
    log_dir = tmp / "ingest_log"
    progress_path = tmp / "l6_progress.json"
    report_path = tmp / "l6_smoke_report.md"

    staging_root.mkdir(parents=True, exist_ok=True)
    md_cache_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    cost = CostTracker(per_book_cap=5.0, batch_cap=15.0)

    print(
        f"L6 smoke starting {started.isoformat(timespec='seconds')}Z — "
        f"{len(_BOOKS)} books, batch cap ${cost.batch_cap:.2f}",
        flush=True,
    )
    results: list[BookResult] = []
    for i, (stem, source_rel) in enumerate(_BOOKS, start=1):
        print(f"\n[{i}/{len(_BOOKS)}] {stem} ← {source_rel}", flush=True)
        log_path = log_dir / f"{stem}.log"
        _log_line(log_path, f"--- begin {stem} ({source_rel}) ---")
        res = _process_one(
            stem=stem,
            source_rel=source_rel,
            cost=cost,
            staging_root=staging_root,
            md_cache_dir=md_cache_dir,
            log_path=log_path,
        )
        results.append(res)
        _write_progress(progress_path, results, cost)
        print(
            f"    → {res.status}  elapsed {res.elapsed_sec:.0f}s  "
            f"cost ${res.cost_dollars:.4f}  pages={res.staging_files}  "
            f"val_errs={res.validation_errors}",
            flush=True,
        )

    cost.save(tmp / "l6_cost_summary.json")
    _render_report(report_path, results, cost, started)
    print(f"\nL6 smoke done. Report: {report_path}")
    print(f"Total cost: ${cost.total_dollars:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
