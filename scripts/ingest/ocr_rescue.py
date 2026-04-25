"""S5-FAIL recovery — OCR scanned PDFs, then re-run the ingest pipeline.

Reads `tmp/ingest_progress.json` for entries with `status == "failed"`,
runs `ocrmypdf` on each (caching to `tmp/ocr_cache/<stem>.pdf`), and then
invokes the same Phase A-E pipeline as `auto_ingest`, but pointing
pdf_to_md at the OCR'd file. Provenance still records the *original*
`raw/books/...` path so anchors in the wiki point users at the source.

OCR settings:
  -l chi_sim+chi_tra+eng     # most failed books are Chinese; English fallback
  --skip-text                 # tolerant when partial text already present
  --jobs 4                    # respect 4-core machine
  --output-type pdf           # don't bloat with PDF/A
  --quiet
  timeout per book: configurable (default 30 min) — kill if scanned book is huge

Usage:
    .venv/bin/python -m scripts.ingest.ocr_rescue [--limit N] [--timeout-min M]
                                                  [--start-from <stem>]
                                                  [--ocr-only]   # skip ingest
                                                  [--ingest-only] # skip OCR
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TMP = REPO_ROOT / "tmp"
OCR_CACHE = TMP / "ocr_cache"
PROGRESS_PATH = TMP / "ingest_progress.json"
OCR_LOG_DIR = TMP / "ingest_log"

sys.path.insert(0, str(REPO_ROOT))
from scripts.ingest import chunk as chunk_mod  # noqa: E402
from scripts.ingest import compile as compile_mod  # noqa: E402
from scripts.ingest import extract as extract_mod  # noqa: E402
from scripts.ingest import pdf_to_md  # noqa: E402
from scripts.ingest.cost_tracker import CostTracker  # noqa: E402
from scripts.ingest.smoke_l6 import _log_line  # noqa: E402
from scripts.ingest.validate import validate_page  # noqa: E402


@dataclass
class RescueResult:
    stem: str
    source_path: str
    ocr_status: str = "pending"  # pending | cached | ocr_ok | ocr_timeout | ocr_failed
    ocr_elapsed_sec: float = 0.0
    ocr_output: str = ""
    ingest_status: str = "skipped"  # skipped | ok | failed | budget_exceeded
    candidate_count: int = 0
    staging_files: int = 0
    validation_errors: int = 0
    cost_dollars: float = 0.0
    chunk_count: int = 0
    pages_total: int | None = None
    error: str = ""
    extras: dict = field(default_factory=dict)


def _ocrmypdf_run(src: Path, dst: Path, timeout_s: int, log_path: Path) -> tuple[str, float]:
    """Run ocrmypdf in its own process group with a hard timeout.

    Returns ("ocr_ok"|"ocr_timeout"|"ocr_failed", elapsed_seconds).
    Output PDF is only kept on success.
    """
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        return ("cached", 0.0)
    cmd = [
        "ocrmypdf",
        "-l", "chi_sim+chi_tra+eng",
        "--skip-text",                 # tolerant of mixed text/scan PDFs
        "--jobs", "4",
        "--output-type", "pdf",
        "--quiet",
        str(src), str(dst),
    ]
    _log_line(log_path, f"OCR: starting ({timeout_s}s timeout) — {src.name}")
    t0 = time.monotonic()
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    try:
        out, _ = proc.communicate(timeout=timeout_s)
        elapsed = time.monotonic() - t0
        if proc.returncode == 0:
            _log_line(log_path, f"OCR: ok in {elapsed:.0f}s")
            return ("ocr_ok", elapsed)
        # ocrmypdf returns non-zero on partial/no improvements too — keep
        # the file if it was produced and is non-trivial.
        if dst.exists() and dst.stat().st_size > 1024:
            _log_line(log_path, f"OCR: partial (rc={proc.returncode}) kept; {elapsed:.0f}s")
            return ("ocr_ok", elapsed)
        msg = (out or b"").decode("utf-8", errors="replace")[-400:]
        _log_line(log_path, f"OCR: FAILED rc={proc.returncode} | tail: {msg}")
        if dst.exists():
            dst.unlink()
        return ("ocr_failed", elapsed)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), 9)
        except (ProcessLookupError, PermissionError, OSError):
            pass
        elapsed = time.monotonic() - t0
        _log_line(log_path, f"OCR: TIMEOUT after {elapsed:.0f}s")
        if dst.exists():
            dst.unlink()
        return ("ocr_timeout", elapsed)


def _reingest_from_ocr(
    stem: str,
    original_source_rel: str,
    ocr_pdf: Path,
    cost: CostTracker,
    log_path: Path,
) -> RescueResult:
    """Run Phases A-E against the OCR'd PDF, but record provenance using
    the ORIGINAL source_rel so wiki links point at raw/books/."""
    res = RescueResult(stem=stem, source_path=original_source_rel)
    md_cache = TMP / "md_cache_ocr"
    staging_root = TMP / "ingest_staging"
    md_cache.mkdir(parents=True, exist_ok=True)

    try:
        _log_line(log_path, f"Phase A: converting OCR'd {ocr_pdf.name}")
        meta = pdf_to_md.convert_to_markdown(ocr_pdf, cache_dir=md_cache)
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
        _log_line(log_path, f"Phase B done: {len(chunks)} chunks")

        # Discipline = first dir under raw/books/ in the original path.
        disc = Path(original_source_rel).relative_to("raw/books").parts[0]
        _log_line(log_path, f"Phase C: extracting ({len(chunks)} LLM calls)")
        extraction = extract_mod.extract_book(
            book_stem=stem,
            source_path=original_source_rel,  # provenance points at raw/, not OCR cache
            discipline=disc,
            language=meta.language,
            chunks=chunks,
            cost=cost,
            pages_total=meta.pages_total,
        )
        res.candidate_count = len(extraction.candidates)
        _log_line(log_path, f"Phase C done: {res.candidate_count} candidates")

        if extraction.candidates:
            # Clear any stale per-book staging from a previous failed run.
            book_staging = staging_root / stem
            if book_staging.exists():
                shutil.rmtree(book_staging)

            anchor = (
                f"[{original_source_rel}#p1-{meta.pages_total}]"
                if meta.pages_total
                else f"[{original_source_rel}#L1-L1]"
            )
            _log_line(log_path, "Phase D: compiling to staging")
            written = compile_mod.write_staging(
                book_stem=stem,
                candidates=extraction.candidates,
                source_provenance=anchor,
                staging_root=book_staging,
            )
            res.staging_files = len(written)
            _log_line(log_path, f"Phase D done: {len(written)} staging files")

            _log_line(log_path, "Phase E: validating")
            source_text = text
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
                err_total += len(errs)
            res.validation_errors = err_total
            _log_line(log_path, f"Phase E done: {err_total} errors")

        spend = cost.books.get(stem)
        if spend is not None:
            res.cost_dollars = round(spend.dollars, 4)
        res.ingest_status = "ok"
    except Exception as e:
        res.ingest_status = "failed"
        res.error = f"{type(e).__name__}: {e}"
        _log_line(log_path, f"INGEST ERROR: {res.error}")
    return res


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--start-from", type=str, default=None)
    ap.add_argument("--timeout-min", type=int, default=30)
    ap.add_argument("--ocr-only", action="store_true")
    ap.add_argument("--ingest-only", action="store_true")
    args = ap.parse_args(argv)

    if not shutil.which("ocrmypdf"):
        print("[ocr_rescue] ocrmypdf not in PATH — install via brew first", file=sys.stderr)
        return 2

    OCR_CACHE.mkdir(parents=True, exist_ok=True)
    OCR_LOG_DIR.mkdir(parents=True, exist_ok=True)

    progress = json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))
    failed = [b for b in progress["books"] if b.get("status") == "failed"]

    if args.start_from:
        for i, b in enumerate(failed):
            if b.get("stem") == args.start_from or b.get("book_stem") == args.start_from:
                failed = failed[i:]
                break
    if args.limit:
        failed = failed[: args.limit]

    print(f"[ocr_rescue] processing {len(failed)} failed books "
          f"(ocr_only={args.ocr_only}, ingest_only={args.ingest_only}, "
          f"timeout={args.timeout_min}min)", flush=True)

    cost = CostTracker(per_book_cap=float("inf"), batch_cap=float("inf"))
    results: list[RescueResult] = []
    for i, b in enumerate(failed, start=1):
        stem = b.get("stem") or b.get("book_stem")
        source_rel = b["source_path"]
        src = REPO_ROOT / source_rel
        ocr_pdf = OCR_CACHE / f"{src.stem}.pdf"
        log_path = OCR_LOG_DIR / f"{stem}.ocr.log"
        _log_line(log_path, f"--- rescue {stem} ---")

        print(f"[{i}/{len(failed)}] {stem}", flush=True)

        result = RescueResult(stem=stem, source_path=source_rel)
        # Phase OCR
        if not args.ingest_only:
            if not src.exists():
                result.ocr_status = "ocr_failed"
                result.error = f"source not found: {source_rel}"
                results.append(result)
                print(f"  ! source not found", flush=True)
                continue
            t0 = time.monotonic()
            status, elapsed = _ocrmypdf_run(src, ocr_pdf, args.timeout_min * 60, log_path)
            result.ocr_status = status
            result.ocr_elapsed_sec = round(elapsed, 1)
            print(f"  OCR  {status:12s}  {elapsed:6.0f}s  "
                  f"{ocr_pdf.stat().st_size/1024/1024:.1f}M" if ocr_pdf.exists()
                  else f"  OCR  {status:12s}  {elapsed:6.0f}s", flush=True)
            if status not in ("ocr_ok", "cached"):
                results.append(result)
                continue
        else:
            if not ocr_pdf.exists():
                result.ocr_status = "missing"
                results.append(result)
                continue
            result.ocr_status = "cached"

        # Phase ingest
        if not args.ocr_only:
            ingest_res = _reingest_from_ocr(stem, source_rel, ocr_pdf, cost, log_path)
            # Carry over OCR fields, replace rest from ingest_res
            ingest_res.ocr_status = result.ocr_status
            ingest_res.ocr_elapsed_sec = result.ocr_elapsed_sec
            result = ingest_res
            print(f"  INGEST {result.ingest_status:6s}  pages={result.staging_files}  "
                  f"val_errs={result.validation_errors}  ${result.cost_dollars:.4f}",
                  flush=True)

        results.append(result)

        # Persist after each book so a crash doesn't lose state.
        rescue_path = TMP / "ocr_rescue_progress.json"
        rescue_path.write_text(
            json.dumps(
                {
                    "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "results": [asdict(r) for r in results],
                    "total_cost_dollars": round(cost.total_dollars, 4),
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    # Summary.
    ocr_ok = sum(1 for r in results if r.ocr_status in ("ocr_ok", "cached"))
    ingest_ok = sum(1 for r in results if r.ingest_status == "ok")
    print(f"\n[ocr_rescue] DONE: OCR ok={ocr_ok}/{len(results)}; "
          f"ingest ok={ingest_ok}/{len(results)}; "
          f"cost ${cost.total_dollars:.2f}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
