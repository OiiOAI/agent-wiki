"""Re-run Phases B→E for a single L6 book after a code change invalidates
its staging output.

Context: Kandel's first L6 pass ran before the streaming + max_tokens=32_768
fix landed in llm_client, so 32 dense chunks got JSON-truncated and only 10
pages made it to staging. This script re-runs chunk→extract→compile→validate
for one stem from smoke_l6._BOOKS, reuses the existing md_cache (Phase A is
expensive), clears that book's staging, and merges fresh counts +
cost/time into tmp/l6_progress.json. Then recheck_l6 can rewrite the
report.

Usage:
    python -m scripts.ingest.rerun_book kandel-neural-science-6e
"""
from __future__ import annotations

import json
import shutil
import sys
import time
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from . import chunk as chunk_mod
from . import compile as compile_mod
from . import extract as extract_mod
from . import pdf_to_md
from .cost_tracker import CostTracker
from .smoke_l6 import _BOOKS, BookResult, _log_line, _process_one
from .validate import validate_page

REPO_ROOT = Path(__file__).resolve().parents[2]


def _find_entry(stem: str) -> tuple[str, str]:
    for s, src in _BOOKS:
        if s == stem:
            return s, src
    raise SystemExit(
        f"stem {stem!r} not in _BOOKS; known: {[s for s, _ in _BOOKS]}"
    )


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if len(argv) != 1:
        print("usage: python -m scripts.ingest.rerun_book <book-stem>", file=sys.stderr)
        return 2
    stem, source_rel = _find_entry(argv[0])

    tmp = REPO_ROOT / "tmp"
    staging_root = tmp / "ingest_staging"
    md_cache_dir = tmp / "md_cache"
    log_dir = tmp / "ingest_log"
    progress_path = tmp / "l6_progress.json"

    # Clear this book's staging so we get a clean reconstruction.
    book_staging = staging_root / stem
    if book_staging.exists():
        shutil.rmtree(book_staging)
        print(f"cleared {book_staging}", flush=True)

    # Use an isolated cost tracker for the rerun — we'll fold the $ into
    # the existing progress total below.
    cost = CostTracker(per_book_cap=5.0, batch_cap=5.0)

    log_path = log_dir / f"{stem}.rerun.log"
    _log_line(log_path, f"--- rerun {stem} at {datetime.utcnow().isoformat()}Z ---")

    res = _process_one(
        stem=stem,
        source_rel=source_rel,
        cost=cost,
        staging_root=staging_root,
        md_cache_dir=md_cache_dir,
        log_path=log_path,
    )
    print(
        f"{stem}: status={res.status} pages={res.staging_files} "
        f"val_errs={res.validation_errors} cost=${res.cost_dollars:.4f} "
        f"elapsed={res.elapsed_sec:.0f}s",
        flush=True,
    )

    # Merge the fresh BookResult into l6_progress.json.
    if progress_path.exists():
        prog = json.loads(progress_path.read_text(encoding="utf-8"))
        for i, b in enumerate(prog["books"]):
            if b["stem"] == stem:
                old_cost = float(b.get("cost_dollars", 0.0))
                # Fold the rerun spend into the batch total so the report
                # truthfully shows what this book actually consumed.
                new_entry = asdict(res)
                new_entry["cost_dollars"] = round(old_cost + res.cost_dollars, 4)
                prog["books"][i] = new_entry
                prog["total_cost_dollars"] = round(
                    float(prog.get("total_cost_dollars", 0.0)) + res.cost_dollars, 4
                )
                break
        prog["reran"] = prog.get("reran", [])
        prog["reran"].append(
            {
                "stem": stem,
                "at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
                "added_cost": round(res.cost_dollars, 4),
            }
        )
        progress_path.write_text(
            json.dumps(prog, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"merged into {progress_path}", flush=True)

    return 0 if res.status == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
