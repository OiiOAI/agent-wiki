"""S6-2 — commit only the OCR-rescued books to wiki/ + git.

Difference from commit_batch.py: instead of walking the entire
ingest_progress.json list, this script reads
`tmp/ocr_rescue_progress.json` and processes only the books with
`ingest_status == "ok"` plus the optional smoke-test book passed
via --include-stem.

Reuses commit_batch's merge logic, log entry format, and per-book
git commit. Final step: rebuild wiki/index.md and tag the batch.

Usage:
    .venv/bin/python -m scripts.ingest.commit_ocr_batch \\
        [--include-stem <smoke-test-stem>] \\
        [--dry-run] [--no-tag]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TMP = REPO_ROOT / "tmp"
WIKI_ROOT = REPO_ROOT / "wiki"

sys.path.insert(0, str(REPO_ROOT))
from scripts.ingest.commit_batch import (  # noqa: E402
    _append_log,
    _git_commit_book,
    _log_entry,
    _process_book,
    _rebuild_index,
)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-tag", action="store_true")
    ap.add_argument(
        "--include-stem",
        action="append",
        default=[],
        help="extra stem(s) to include (e.g. smoke-test books)",
    )
    ap.add_argument("--tag", type=str, default=None)
    args = ap.parse_args(argv)

    rescue_path = TMP / "ocr_rescue_progress.json"
    rescue = json.loads(rescue_path.read_text(encoding="utf-8"))
    ok_books = [
        (r["stem"], r["source_path"])
        for r in rescue["results"]
        if r["ingest_status"] == "ok"
    ]
    # Manual extras (smoke-test books not in ocr_rescue_progress.json).
    if args.include_stem:
        # Look up source_path from main ingest_progress.json.
        main = json.loads((TMP / "ingest_progress.json").read_text(encoding="utf-8"))
        stem_to_src = {b.get("stem") or b.get("book_stem"): b["source_path"] for b in main["books"]}
        for s in args.include_stem:
            if s in stem_to_src:
                ok_books.insert(0, (s, stem_to_src[s]))
            else:
                print(f"[commit_ocr_batch] WARN: --include-stem {s!r} not found in main progress", file=sys.stderr)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"[commit_ocr_batch] processing {len(ok_books)} OCR-rescued books "
          f"(dry_run={args.dry_run})", flush=True)

    total_created = 0
    total_merged = 0
    skipped = 0
    for i, (book_stem, source_path) in enumerate(ok_books, start=1):
        res = _process_book(book_stem, today, dry_run=args.dry_run)
        if res.skipped_no_staging:
            skipped += 1
            print(f"  [{i}/{len(ok_books)}] {book_stem} — SKIP (no staging dir)", flush=True)
            continue
        total_created += len(res.created)
        total_merged += len(res.merged)
        print(
            f"  [{i}/{len(ok_books)}] {book_stem[:55]:55s} — "
            f"+{len(res.created)} new, ~{len(res.merged)} merged",
            flush=True,
        )
        if args.dry_run:
            continue

        log_path = _append_log(_log_entry(book_stem, res, today, source_path))
        touched = res.created + res.merged + [log_path]
        _git_commit_book(book_stem, touched)

    print(
        f"[commit_ocr_batch] done: +{total_created} new, ~{total_merged} merged across "
        f"{len(ok_books) - skipped} books ({skipped} skipped)",
        flush=True,
    )

    if args.dry_run:
        return 0

    # Rebuild index (uses current wiki state — all 165 + 29 new).
    new_index = _rebuild_index()
    idx_path = WIKI_ROOT / "index.md"
    idx_path.write_text(new_index, encoding="utf-8")
    subprocess.run(["git", "add", str(idx_path)], cwd=REPO_ROOT, check=True)
    subprocess.run(
        ["git", "commit", "-m", "ingest: rebuild index after OCR-rescue batch"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    )
    print("[commit_ocr_batch] index.md rebuilt + committed", flush=True)

    if not args.no_tag:
        tag = args.tag or f"ingest-batch-ocr-{datetime.now():%Y%m%d-%H%M}"
        subprocess.run(["git", "tag", tag], cwd=REPO_ROOT, check=True)
        print(f"[commit_ocr_batch] tagged {tag}", flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
