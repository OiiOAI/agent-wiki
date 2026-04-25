"""Phase G: batch dry-run report generator.

Walks `tmp/ingest_staging/<book_stem>/` and emits one `tmp/ingest_report.md`
that the user can read before approving Phase H (the real commit).
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path


@dataclass
class BookReport:
    book_stem: str
    discipline: str
    pages_staged: int = 0
    conflicts: int = 0
    failures: list[str] = field(default_factory=list)
    cost_dollars: float = 0.0
    status: str = "ok"  # 'ok' | 'failed' | 'empty'


def _count_pages(book_dir: Path) -> int:
    if not book_dir.is_dir():
        return 0
    return sum(1 for _ in book_dir.rglob("*.md"))


def build_report(
    staging_root: Path,
    cost_summary: dict,
    failures_path: Path | None = None,
    conflicts: dict[str, int] | None = None,
    expected_books: list[str] | None = None,
    output_path: Path | None = None,
) -> Path:
    """Build the batch report. Returns the path written."""
    output_path = output_path or staging_root.parent / "ingest_report.md"
    conflicts = conflicts or {}

    books: list[BookReport] = []
    for book_dir in sorted(p for p in staging_root.iterdir() if p.is_dir()):
        stem = book_dir.name
        spend = cost_summary.get("books", {}).get(stem, {})
        books.append(
            BookReport(
                book_stem=stem,
                discipline="",  # filled by caller if available
                pages_staged=_count_pages(book_dir),
                conflicts=conflicts.get(stem, 0),
                cost_dollars=float(spend.get("dollars", 0.0)),
                status="ok" if _count_pages(book_dir) > 0 else "empty",
            )
        )

    # Mark expected-but-missing books as failed.
    seen = {b.book_stem for b in books}
    for stem in expected_books or []:
        if stem not in seen:
            books.append(BookReport(book_stem=stem, discipline="", status="failed"))

    total_pages = sum(b.pages_staged for b in books)
    total_conflicts = sum(b.conflicts for b in books)
    total_dollars = cost_summary.get("total_dollars", 0.0)
    failed_count = sum(1 for b in books if b.status == "failed")

    lines = [
        f"# Ingest Dry-run Report ({date.today().isoformat()})",
        "",
        "## Summary",
        "",
        f"- Books evaluated: {len(books)}",
        f"- Pages staged: {total_pages}",
        f"- Conflicts detected: {total_conflicts}",
        f"- Failures: {failed_count}",
        f"- Total cost: ${total_dollars:.2f}",
        "",
        "## Per-book breakdown",
        "",
        "| Book | Pages | Conflicts | Cost | Status |",
        "|------|------:|----------:|-----:|--------|",
    ]
    for b in sorted(books, key=lambda x: x.book_stem):
        lines.append(
            f"| {b.book_stem} | {b.pages_staged} | {b.conflicts} | "
            f"${b.cost_dollars:.3f} | {b.status} |"
        )

    if failures_path and failures_path.exists():
        lines += ["", "## Failures detail", "", failures_path.read_text(encoding="utf-8")]

    report_text = "\n".join(lines) + "\n"
    output_path.write_text(report_text, encoding="utf-8")

    # Sidecar: the sha256 the user must cite via --approved-by to authorize commit.
    sha = hashlib.sha256(report_text.encode("utf-8")).hexdigest()
    output_path.with_suffix(".sha256").write_text(sha)
    return output_path


def report_sha(path: Path) -> str:
    return hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
