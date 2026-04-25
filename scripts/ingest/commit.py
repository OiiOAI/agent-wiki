"""Phase H: per-book commit of staged pages into wiki/ + git trail.

Invoked only after the user explicitly approves the dry-run report. Each
book is one atomic git commit so individual bad ingests can be reverted.
"""
from __future__ import annotations

import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from .report import report_sha


class NotApprovedError(Exception):
    """Raised when --approved-by / --approved-sha check fails."""


def verify_approval(report_path: Path, approved_sha: str) -> None:
    actual = report_sha(report_path)
    if actual != approved_sha:
        raise NotApprovedError(
            f"report sha mismatch: actual={actual!r} approved={approved_sha!r}"
        )


def _run_git(args: list[str], cwd: Path) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True)


def commit_book(
    book_stem: str,
    staging_book_dir: Path,
    wiki_root: Path,
    repo_root: Path,
    log_entry: str,
    *,
    index_update: str | None = None,
) -> None:
    """Move staged pages from `staging_book_dir/<type>/*.md` into
    `wiki_root/<type>/`. Append `log_entry` to wiki/log.md. Optionally
    replace the wiki/index.md block provided in `index_update` (caller
    responsible for constructing it with surrounding anchor comments).
    """
    moved: list[Path] = []
    for src in staging_book_dir.rglob("*.md"):
        rel = src.relative_to(staging_book_dir)
        dst = wiki_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        moved.append(dst)

    log_path = wiki_root / "log.md"
    log_path.write_text(
        log_path.read_text(encoding="utf-8").rstrip() + "\n\n" + log_entry.rstrip() + "\n",
        encoding="utf-8",
    )

    if index_update is not None:
        idx_path = wiki_root / "index.md"
        idx_path.write_text(index_update, encoding="utf-8")

    _run_git(["add", str(log_path)], repo_root)
    if index_update is not None:
        _run_git(["add", str(wiki_root / "index.md")], repo_root)
    for p in moved:
        _run_git(["add", str(p)], repo_root)
    _run_git(["commit", "-m", f"ingest: {book_stem}"], repo_root)


def tag_batch(repo_root: Path, tag: str | None = None) -> str:
    tag = tag or f"ingest-batch-{datetime.now():%Y%m%d-%H%M}"
    _run_git(["tag", tag], repo_root)
    return tag
