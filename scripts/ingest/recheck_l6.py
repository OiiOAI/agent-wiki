"""Re-validate all L6 staging outputs after the runner completes.

Context: the in-flight L6 runner imported `validate_page` at launch time,
before the provenance-regex bug fix for paths-with-spaces. So its in-log
error counts over-report — book filenames with spaces (Atomic Habits,
Kandel, 道德经, 历史山水渔樵) have provenance anchors that the old regex
rejected. This script re-runs validation with the current (fixed) regex
and rewrites `tmp/l6_smoke_report.md` + `tmp/l6_progress.json` in place.

Usage:
    python -m scripts.ingest.recheck_l6
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from .validate import validate_page

REPO_ROOT = Path(__file__).resolve().parents[2]


def _find_md_cache(book_source_path: str) -> Path | None:
    """`raw/books/<disc>/<book>.pdf` → `tmp/md_cache/<stem>.md`."""
    src = Path(book_source_path)
    cache = REPO_ROOT / "tmp" / "md_cache" / f"{src.stem}.md"
    return cache if cache.exists() else None


_TYPE_DIRS = {
    "concepts": "concept",
    "entities": "entity",
    "topics": "topic",
    "sources": "source",
    "analyses": "analysis",
    "conflicts": "conflict",
}


def _count_page_types(staging_root: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for dirname, type_name in _TYPE_DIRS.items():
        subdir = staging_root / dirname
        if not subdir.exists():
            continue
        n = sum(1 for _ in subdir.glob("*.md"))
        if n:
            counts[type_name] = n
    return counts


def _revalidate_book(stem: str, source_rel: str) -> dict:
    staging = REPO_ROOT / "tmp" / "ingest_staging" / stem
    if not staging.exists():
        return {
            "stem": stem,
            "staging_files": 0,
            "validation_errors": 0,
            "validation_problem_pages": [],
            "per_page": {},
            "page_types": {},
        }
    pages = sorted(staging.rglob("*.md"))

    cache = _find_md_cache(source_rel)
    source_text = cache.read_text(encoding="utf-8") if cache else ""

    existing_ids: set[str] = set()
    err_total = 0
    problem_pages: list[str] = []
    per_page: dict[str, list[str]] = {}
    for p in pages:
        md = p.read_text(encoding="utf-8")
        errs = validate_page(
            md, existing_ids=existing_ids, source_text=source_text, page_path=str(p)
        )
        if errs:
            problem_pages.append(p.name)
            per_page[p.name] = [str(e) for e in errs]
            err_total += len(errs)
    return {
        "stem": stem,
        "staging_files": len(pages),
        "validation_errors": err_total,
        "validation_problem_pages": problem_pages,
        "per_page": per_page,
        "page_types": _count_page_types(staging),
    }


def main() -> int:
    progress_path = REPO_ROOT / "tmp" / "l6_progress.json"
    report_path = REPO_ROOT / "tmp" / "l6_smoke_report.md"
    if not progress_path.exists():
        print(f"missing {progress_path}", file=sys.stderr)
        return 1

    prog = json.loads(progress_path.read_text(encoding="utf-8"))
    updated_books: list[dict] = []
    revalidation: list[dict] = []
    for b in prog["books"]:
        fresh = _revalidate_book(b["stem"], b["source_path"])
        b["validation_errors"] = fresh["validation_errors"]
        b["validation_problem_pages"] = fresh["validation_problem_pages"]
        b["staging_files"] = fresh["staging_files"]
        if fresh["page_types"]:
            b["page_types"] = fresh["page_types"]
        updated_books.append(b)
        revalidation.append(fresh)

    prog["books"] = updated_books
    prog["revalidated_at"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    progress_path.write_text(
        json.dumps(prog, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Rewrite the report with the fresh counts.
    lines: list[str] = []
    lines.append("# L6 Smoke Report (re-validated)")
    lines.append("")
    lines.append(
        f"- Re-validated at: {prog['revalidated_at']} "
        f"(provenance regex fix applied post-run)"
    )
    ok = [b for b in updated_books if b["status"] == "ok"]
    clean = [b for b in ok if b["validation_errors"] == 0]
    failed = [b for b in updated_books if b["status"] != "ok"]
    lines.append(
        f"- Books: {len(ok)}/{len(updated_books)} ok; "
        f"{len(clean)}/{len(updated_books)} validated clean; {len(failed)} failed"
    )
    lines.append(f"- Total cost: ${prog['total_cost_dollars']:.4f}")
    lines.append(f"- Batch cap: ${prog['batch_cap']:.2f}")
    lines.append("")
    lines.append("## Per-book breakdown")
    lines.append("")
    lines.append(
        "| Book | Status | Converter | Lang | Pages | Chunks | Pages out | Val errors | Cost | Time |"
    )
    lines.append(
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|"
    )
    for b in updated_books:
        pages_total = b.get("pages_total") if b.get("pages_total") is not None else "-"
        lines.append(
            f"| {b['stem']} | {b['status']} | {b.get('converter') or '-'} | "
            f"{b.get('language') or '-'} | {pages_total} | {b.get('chunk_count', 0)} | "
            f"{b['staging_files']} | {b['validation_errors']} | "
            f"${b.get('cost_dollars', 0):.4f} | {b.get('elapsed_sec', 0):.0f}s |"
        )
    lines.append("")
    lines.append("## Page type distribution")
    lines.append("")
    for b in updated_books:
        pt = b.get("page_types", {})
        if pt:
            types_str = ", ".join(f"{k}={v}" for k, v in sorted(pt.items()))
            lines.append(f"- `{b['stem']}`: {types_str}")
        else:
            lines.append(f"- `{b['stem']}`: (no pages produced)")
    lines.append("")

    problem_books = [b for b in ok if b["validation_problem_pages"]]
    if problem_books:
        lines.append("## Validation issues (post-fix)")
        lines.append("")
        for b in problem_books:
            lines.append(
                f"### `{b['stem']}` — {b['validation_errors']} errors across "
                f"{len(b['validation_problem_pages'])} pages"
            )
            for r in revalidation:
                if r["stem"] == b["stem"]:
                    for name, errs in r["per_page"].items():
                        lines.append(f"- **{name}**")
                        for e in errs[:5]:
                            lines.append(f"  - `{e}`")
                        if len(errs) > 5:
                            lines.append(f"  - … +{len(errs) - 5} more")
                    break
            lines.append("")

    if failed:
        lines.append("## Failures")
        lines.append("")
        for b in failed:
            lines.append(f"### `{b['stem']}` — {b['status']}")
            lines.append("")
            lines.append(f"Source: `{b['source_path']}`")
            lines.append("")
            lines.append(f"```\n{b.get('error', '')}\n```")
            lines.append("")

    lines.append("## Reviewer checklist")
    lines.append("")
    lines.append("- [ ] Spot-check 3 pages per book — do facts line up with the source?")
    lines.append("- [ ] Provenance anchors clickable back to `raw/books/…`?")
    lines.append("- [ ] Any `Inference:` / `Uncertain:` labels misapplied?")
    lines.append("- [ ] Scanned Chinese book — did the pipeline fail gracefully?")
    lines.append("- [ ] Cost within budget (expected $5-10).")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"re-validated report: {report_path}")
    print(f"total errors (post-fix): {sum(b['validation_errors'] for b in updated_books)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
