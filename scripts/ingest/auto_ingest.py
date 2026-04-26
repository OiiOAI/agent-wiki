"""S5 orchestrator — full-batch dry-run for all books under raw/books/.

Walks `raw/books/**/*.{pdf,epub}`, processes Phases A→E for each book,
writes staging under `tmp/ingest_staging/<stem>/`, tracks live progress
in `tmp/ingest_progress.json`, and emits `tmp/ingest_report.md` at the
end (the review gate before Phase H commit).

Resumable: on re-launch, any book already in status=ok is skipped.
At 196 books × ~27 min/avg ≈ 3-4 days of wall time, the user may stop
and restart; this loses at most the in-flight book.

Safety:
  * No budget caps by default (per user direction 2026-04-23 — uncapped).
    Pass `--budget` / `--per-book-cap` to re-enable if you ever want them.
  * Phase A-E only; does NOT touch wiki/ or raw/
  * SIGINT saves progress before exit

Usage:
    python -m scripts.ingest.auto_ingest               # run pending
    python -m scripts.ingest.auto_ingest --limit 5     # smoke
    python -m scripts.ingest.auto_ingest --disc philosophy
    python -m scripts.ingest.auto_ingest --dry-discover
"""
from __future__ import annotations

import argparse
import json
import math
import re
import signal
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

from .cost_tracker import CostTracker
from .smoke_l6 import BookResult, _log_line, _process_one

REPO_ROOT = Path(__file__).resolve().parents[2]

# L6 covered these filenames; reuse the exact stems so S5 skips them cleanly
# and the staging layout stays stable for conflict-check / commit.
_L6_STEMS: dict[str, str] = {
    "Atomic Habits_ The life - changing million copy bestseller - James Clear.pdf": "atomic-habits",
    "Eric Kandel PRINCIPLES OF NEURAL SCIENCE Sixth Edition - Eric R Kandel; John Koester; Sarah Mack; Steven Siegelbaum.pdf": "kandel-neural-science-6e",
    "道德经(精) - 中华经典名著全本全注全译.epub": "daodejing",
    "Algorithms_to_Live_By.epub": "algorithms-to-live-by",
    "历史山水渔樵 - 赵汀阳.pdf": "lishi-shanshui-yuqiao",
}


@dataclass
class BatchState:
    started: str = ""
    updated: str = ""
    batch_cap: float = math.inf
    per_book_cap: float = math.inf
    total_cost_dollars: float = 0.0
    total_books: int = 0
    books: list[dict] = field(default_factory=list)

    @classmethod
    def load(cls, path: Path) -> "BatchState | None":
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        bs = cls()
        bs.__dict__.update(data)
        return bs

    def save(self, path: Path) -> None:
        self.updated = datetime.utcnow().isoformat(timespec="seconds") + "Z"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.__dict__, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )


def _derive_stem(path: Path) -> str:
    """Turn a filename into a stable, unique slug.

    - lowercase
    - keep a-z, 0-9, and CJK; everything else becomes `-`
    - collapse/strip `-`
    - truncate to 60 chars
    Hand-assigned L6 stems win.
    """
    if path.name in _L6_STEMS:
        return _L6_STEMS[path.name]
    name = path.stem.lower()
    name = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", name)
    name = re.sub(r"-+", "-", name).strip("-")
    if not name:
        name = "untitled"
    return name[:60]


def discover_books(
    repo_root: Path,
    disc_filter: str | None = None,
    books_dir: Path | None = None,
    default_discipline: str = "general",
) -> list[tuple[str, str]]:
    """Return [(stem, source_rel_path), ...] for every PDF/EPUB under `books_dir`.

    By default `books_dir = repo_root/raw/books`, which is the in-repo
    convention used by this project's authors. External users can point
    `--books-dir` at any folder (e.g. `~/Documents/Library`); when the
    folder does NOT live under `repo_root/raw/books`, paths recorded in
    progress.json/provenance use the **absolute** path.

    Discipline assignment:
      - if `books_dir` has subdirectories, the first dir component under
        `books_dir` is treated as the discipline (preserves the original
        layout convention);
      - if a book sits at the top level of `books_dir` with no parent
        category, `default_discipline` is used.

    Dedupes by stem; collisions get a `-<discipline>` or numeric suffix.
    """
    if books_dir is None:
        books_dir = repo_root / "raw" / "books"
    books_dir = books_dir.resolve()
    inside_repo = books_dir.is_relative_to(repo_root)

    files: list[Path] = []
    for ext in ("*.pdf", "*.epub"):
        files.extend(books_dir.rglob(ext))
    files = sorted(files)
    seen: set[str] = set()
    out: list[tuple[str, str]] = []
    for p in files:
        rel_under_books = p.relative_to(books_dir)
        disc = rel_under_books.parts[0] if len(rel_under_books.parts) > 1 else default_discipline
        if disc_filter and disc != disc_filter:
            continue
        # Source paths recorded in provenance: relative to repo_root when
        # the books live inside the repo, absolute otherwise. Either form
        # is round-trippable when the orchestrator joins with repo_root.
        rel = str(p.relative_to(repo_root)) if inside_repo else str(p)
        stem = _derive_stem(p)
        candidate = stem
        suffix = 2
        while candidate in seen:
            candidate = f"{stem}-{disc}" if suffix == 2 else f"{stem}-{suffix}"
            suffix += 1
        seen.add(candidate)
        out.append((candidate, rel))
    return out


def _already_done(entry: dict) -> bool:
    return entry.get("status") == "ok" and entry.get("staging_files", 0) > 0


def _load_or_init(
    progress_path: Path,
    books: list[tuple[str, str]],
    batch_cap: float,
    per_book_cap: float,
) -> BatchState:
    existing = BatchState.load(progress_path)
    if existing:
        known = {b["stem"] for b in existing.books}
        for stem, src in books:
            if stem not in known:
                existing.books.append(asdict(BookResult(stem=stem, source_path=src)))
        existing.total_books = len(existing.books)
        existing.batch_cap = batch_cap
        existing.per_book_cap = per_book_cap
        return existing
    return BatchState(
        started=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        batch_cap=batch_cap,
        per_book_cap=per_book_cap,
        total_books=len(books),
        books=[asdict(BookResult(stem=s, source_path=src)) for s, src in books],
    )


def _seed_from_l6(state: BatchState, l6_progress: Path) -> int:
    """If L6 staging + progress exist, fold those 5 books' status in so S5
    skips them and inherits their cost in the total.

    Returns count of books seeded.
    """
    if not l6_progress.exists():
        return 0
    try:
        l6 = json.loads(l6_progress.read_text(encoding="utf-8"))
    except Exception:
        return 0
    l6_by_stem = {b["stem"]: b for b in l6.get("books", [])}
    seeded = 0
    for entry in state.books:
        if entry["status"] == "ok":
            continue
        if entry["stem"] in l6_by_stem:
            l6_entry = l6_by_stem[entry["stem"]]
            if l6_entry.get("status") == "ok" and l6_entry.get("staging_files", 0) > 0:
                for k in (
                    "status", "converter", "language", "pages_total",
                    "chunk_count", "candidate_count", "page_types",
                    "staging_files", "validation_errors",
                    "validation_problem_pages", "cost_dollars",
                    "llm_calls", "tokens_in", "tokens_out", "elapsed_sec",
                ):
                    if k in l6_entry:
                        entry[k] = l6_entry[k]
                state.total_cost_dollars += float(l6_entry.get("cost_dollars", 0.0))
                seeded += 1
    return seeded


def _render_report(report_path: Path, state: BatchState) -> None:
    lines: list[str] = []
    lines.append("# Ingest Dry-run Report (S5 — full batch)")
    lines.append("")
    lines.append(f"- Started: {state.started}")
    lines.append(f"- Finished/updated: {state.updated}")
    ok = [b for b in state.books if b["status"] == "ok"]
    clean = [b for b in ok if b.get("validation_errors", 0) == 0]
    failed = [b for b in state.books if b["status"] == "failed"]
    budget = [b for b in state.books if b["status"] == "budget_exceeded"]
    pending = [b for b in state.books if b["status"] == "pending"]
    lines.append(
        f"- Books: {len(ok)}/{state.total_books} ok; "
        f"{len(clean)}/{state.total_books} validated clean; "
        f"{len(failed)} failed; {len(budget)} budget_exceeded; "
        f"{len(pending)} pending"
    )
    lines.append(f"- Total cost: ${state.total_cost_dollars:.4f}")
    lines.append(
        f"- Batch cap: {'uncapped' if math.isinf(state.batch_cap) else f'${state.batch_cap:.2f}'}"
    )
    lines.append(
        f"- Per-book cap: {'uncapped' if math.isinf(state.per_book_cap) else f'${state.per_book_cap:.2f}'}"
    )
    lines.append("")

    # per-discipline rollup
    lines.append("## Per-discipline rollup")
    lines.append("")
    lines.append("| Discipline | Ok | Clean | Failed | Pending | Cost |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    disc_roll: dict[str, dict] = {}
    for b in state.books:
        sp = b["source_path"]
        parts = sp.split("/")
        disc = parts[2] if len(parts) >= 3 and sp.startswith("raw/books/") else "?"
        d = disc_roll.setdefault(
            disc, {"ok": 0, "clean": 0, "failed": 0, "pending": 0, "cost": 0.0}
        )
        if b["status"] == "ok":
            d["ok"] += 1
            if b.get("validation_errors", 0) == 0:
                d["clean"] += 1
        elif b["status"] == "failed":
            d["failed"] += 1
        elif b["status"] == "pending":
            d["pending"] += 1
        d["cost"] += b.get("cost_dollars", 0.0) or 0.0
    for disc in sorted(disc_roll):
        d = disc_roll[disc]
        lines.append(
            f"| {disc} | {d['ok']} | {d['clean']} | {d['failed']} | "
            f"{d['pending']} | ${d['cost']:.2f} |"
        )
    lines.append("")

    lines.append("## Per-book breakdown")
    lines.append("")
    lines.append(
        "| Book | Status | Lang | Chunks | Pages out | Val errors | Cost | Time |"
    )
    lines.append("|---|---|---|---:|---:|---:|---:|---:|")
    for b in state.books:
        lines.append(
            f"| {b['stem']} | {b['status']} | {b.get('language') or '-'} | "
            f"{b.get('chunk_count', 0)} | {b.get('staging_files', 0)} | "
            f"{b.get('validation_errors', 0)} | "
            f"${b.get('cost_dollars', 0):.4f} | "
            f"{b.get('elapsed_sec', 0):.0f}s |"
        )
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

    if budget:
        lines.append("## Budget-exceeded")
        lines.append("")
        for b in budget:
            lines.append(
                f"- `{b['stem']}` — {b.get('error', '(no detail)')} "
                f"(spent ${b.get('cost_dollars', 0):.4f})"
            )
        lines.append("")

    val_problem = [b for b in ok if b.get("validation_errors", 0) > 0]
    if val_problem:
        lines.append("## Validation issues (need human review)")
        lines.append("")
        for b in val_problem:
            pp = b.get("validation_problem_pages", []) or []
            tail = f" … +{len(pp)-5} more" if len(pp) > 5 else ""
            lines.append(
                f"- `{b['stem']}` — {b['validation_errors']} errors on "
                f"{len(pp)} pages: {', '.join(pp[:5])}{tail}"
            )
        lines.append("")

    lines.append("## Reviewer checklist (before S6 commit)")
    lines.append("")
    lines.append("- [ ] Failure pattern review — systematic by format/language/size?")
    lines.append("- [ ] Spot-check 10 random books — facts line up with source?")
    lines.append("- [ ] Provenance anchors clickable to `raw/books/…`?")
    lines.append("- [ ] Total cost within $500 cap.")
    lines.append("- [ ] Conflict-check pass before Phase H (separate step).")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--budget", type=float, default=math.inf, help="batch $ cap (default: uncapped)")
    ap.add_argument("--per-book-cap", type=float, default=math.inf, help="per-book $ cap (default: uncapped)")
    ap.add_argument("--limit", type=int, default=None, help="only process first N pending")
    ap.add_argument("--disc", type=str, default=None, help="only process this discipline")
    ap.add_argument(
        "--books-dir",
        type=str,
        default=None,
        help=(
            "scan this folder for PDF/EPUB instead of raw/books/. The "
            "first subdirectory component is treated as the 'discipline'; "
            "files at the top level use --default-discipline."
        ),
    )
    ap.add_argument(
        "--default-discipline",
        type=str,
        default="general",
        help="discipline label for books at the top level of --books-dir",
    )
    ap.add_argument(
        "--dry-discover", action="store_true",
        help="print discovered books and exit, do not run pipeline",
    )
    args = ap.parse_args(argv)

    tmp = REPO_ROOT / "tmp"
    staging_root = tmp / "ingest_staging"
    md_cache_dir = tmp / "md_cache"
    log_dir = tmp / "ingest_log"
    progress_path = tmp / "ingest_progress.json"
    report_path = tmp / "ingest_report.md"
    l6_progress_path = tmp / "l6_progress.json"

    staging_root.mkdir(parents=True, exist_ok=True)
    md_cache_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    books_dir = Path(args.books_dir).expanduser().resolve() if args.books_dir else None
    books = discover_books(
        REPO_ROOT,
        disc_filter=args.disc,
        books_dir=books_dir,
        default_discipline=args.default_discipline,
    )
    if args.dry_discover:
        for stem, src in books:
            print(f"{stem}\t{src}")
        print(f"\n{len(books)} books discovered", file=sys.stderr)
        return 0

    state = _load_or_init(progress_path, books, args.budget, args.per_book_cap)
    seeded = _seed_from_l6(state, l6_progress_path)
    if seeded:
        print(f"[auto_ingest] seeded {seeded} books from L6 (skip + inherit cost)")
    state.save(progress_path)

    cost = CostTracker(per_book_cap=args.per_book_cap, batch_cap=args.budget)

    # SIGINT: save progress and exit clean.
    def _on_sigint(signum, frame):
        print("\n[auto_ingest] SIGINT — saving progress and exiting", flush=True)
        state.total_cost_dollars = round(
            state.total_cost_dollars + cost.total_dollars, 4
        )
        state.save(progress_path)
        _render_report(report_path, state)
        sys.exit(130)

    signal.signal(signal.SIGINT, _on_sigint)

    pending_all = [b for b in state.books if not _already_done(b)]
    pending = pending_all[: args.limit] if args.limit is not None else pending_all

    budget_str = "uncapped" if math.isinf(args.budget) else f"${args.budget:.2f}"
    pbc_str = "uncapped" if math.isinf(args.per_book_cap) else f"${args.per_book_cap:.2f}"
    print(
        f"[auto_ingest] {len(pending_all)} pending in state "
        f"(processing {len(pending)} this run); "
        f"already ok: {state.total_books - len(pending_all)}; "
        f"budget {budget_str}; per-book cap {pbc_str}; "
        f"prior cost ${state.total_cost_dollars:.2f}",
        flush=True,
    )
    if not pending:
        if not state.books:
            # No discovery hits at all — most likely a fresh clone where
            # raw/books/ is empty and no --books-dir was supplied.
            scanned = (
                Path(args.books_dir).expanduser().resolve()
                if args.books_dir
                else REPO_ROOT / "raw" / "books"
            )
            print(
                f"[auto_ingest] No books found under {scanned}.",
                flush=True,
            )
            print("Did you mean to point at a different folder?", flush=True)
            print(
                "  python -m scripts.ingest.auto_ingest --books-dir ~/MyBooks",
                flush=True,
            )
            print("Or run the guided setup:", flush=True)
            print("  python -m scripts.ingest.setup", flush=True)
            return 0
        print("[auto_ingest] nothing to do — all books processed.", flush=True)
        _render_report(report_path, state)
        return 0

    stop_reason: str | None = None
    # Effective budget for this invocation is batch_cap minus already-spent.
    remaining_budget = max(args.budget - state.total_cost_dollars, 0.0)
    cost.batch_cap = remaining_budget

    for i, entry in enumerate(pending, start=1):
        # Recheck before each book in case resume started over-budget.
        effective_total = state.total_cost_dollars + cost.total_dollars
        if effective_total >= args.budget:
            stop_reason = (
                f"batch cap ${args.budget} reached "
                f"(effective total ${effective_total:.4f})"
            )
            print(f"[auto_ingest] STOP: {stop_reason}", flush=True)
            break

        stem = entry["stem"]
        source_rel = entry["source_path"]
        log_path = log_dir / f"{stem}.log"
        _log_line(log_path, f"--- begin {stem} ({source_rel}) ---")
        budget_disp = "∞" if math.isinf(args.budget) else f"${args.budget:.2f}"
        print(
            f"\n[{i}/{len(pending)}] {stem} ← {source_rel} "
            f"(total spent ${effective_total:.2f}/{budget_disp})",
            flush=True,
        )
        t_start = time.time()
        res = _process_one(
            stem=stem,
            source_rel=source_rel,
            cost=cost,
            staging_root=staging_root,
            md_cache_dir=md_cache_dir,
            log_path=log_path,
        )
        entry.update(asdict(res))
        state.total_cost_dollars = round(
            state.total_cost_dollars + res.cost_dollars, 4
        )
        # Only count the book once: subtract it from cost tracker so the
        # in-memory remaining_budget isn't double-counted.
        state.save(progress_path)
        # Also render a report each iteration so the user can peek mid-run.
        _render_report(report_path, state)
        elapsed = time.time() - t_start
        print(
            f"    → {res.status}  elapsed {elapsed:.0f}s  "
            f"cost ${res.cost_dollars:.4f}  pages={res.staging_files}  "
            f"val_errs={res.validation_errors}",
            flush=True,
        )

    state.save(progress_path)
    _render_report(report_path, state)
    print(f"\n[auto_ingest] done. Report: {report_path}")
    print(f"[auto_ingest] Total cost: ${state.total_cost_dollars:.4f}")
    if stop_reason:
        print(f"[auto_ingest] Stopped early: {stop_reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
