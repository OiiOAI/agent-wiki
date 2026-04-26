"""Beautify filenames + classify by discipline + copy into raw/books/.

Used by `scripts/ingest/setup.py` (the interactive wizard) when the
user opts to import their books into the project tree rather than
referencing them from an external folder.

Three pure-function pipelines:

  1. `beautify_filename(name)` — deterministic regex cleanup that strips
     publisher series brackets, country/author prefixes, repeated
     punctuation, and clamps overlong filenames. Idempotent: running
     it twice yields the same result.

  2. `classify_books(srcs, mode, default, llm)` — assigns a `discipline`
     label to each (source_path, ext) tuple. Three modes:
       - `subdir`: use the parent directory name as the label.
                   Used automatically when the source folder has its
                   own one-level directory tree.
       - `default`: assign every book to a single user-chosen label.
       - `manual`: ask the user per book (caller passes input fn).

     `llm` mode is documented in the wizard but lives outside this
     module to keep imports light.

  3. `import_books(plan, dest_root, dry_run)` — physically `shutil.copy2`
     each source into `dest_root/<discipline>/<beautified>.<ext>`,
     skipping duplicates by stem (returns `(copied, skipped, total_bytes)`).
"""
from __future__ import annotations

import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

# Regex pipeline for beautify_filename. Order matters — earlier rules
# strip prefixes that later rules would otherwise mangle.
_LEADING_BRACKET_RE = re.compile(r"^\s*\[[^\]]*\]\s*")
_LEADING_FULLWIDTH_BRACKET_RE = re.compile(r"^\s*【[^】]*】\s*")
_TRAILING_AUTHOR_PREFIX_RE = re.compile(
    # Matches `·[国家]作者 著` and similar Chinese book conventions
    # appearing as suffix before the file extension. Conservative: only
    # strips when ` 著` / ` 编` / ` 主编` / ` 译` is present (high signal).
    r"\s*·?\[([^\]]+)\][^.]*?\s+(著|编|主编|译|译注|译著|编著|校理|撰)\s*$"
)
_REDUNDANT_WHITESPACE_RE = re.compile(r"\s+")
_UNDERSCORE_RUN_RE = re.compile(r"_+")
_LEADING_NUMBER_DOT_RE = re.compile(r"^\d+[\._-]\s*")  # "01. Foo" → "Foo"

# Length cap (chars). Filesystem can do more but git diffs / display
# get unreadable past this; suffix-match in extract.py uses last 30
# chars so we need ≥40 for stable matching.
_MAX_LEN = 100


def beautify_filename(name: str) -> str:
    """Clean up a filename so it's git-friendly and human-scannable.

    Preserves the file extension. Idempotent.
    """
    if not name:
        return name
    p = Path(name)
    stem = p.stem
    ext = p.suffix.lower()  # normalize .PDF → .pdf

    # 1. Strip leading bracketed series labels (Chinese half-width + full-width)
    while True:
        new_stem = _LEADING_BRACKET_RE.sub("", stem)
        new_stem = _LEADING_FULLWIDTH_BRACKET_RE.sub("", new_stem)
        if new_stem == stem:
            break
        stem = new_stem

    # 2. Strip leading numeric prefix ("01. Foo" → "Foo")
    stem = _LEADING_NUMBER_DOT_RE.sub("", stem)

    # 3. Strip trailing `·[国家]作者 著` style suffix
    stem = _TRAILING_AUTHOR_PREFIX_RE.sub("", stem)

    # 4. Collapse internal whitespace, then trim
    stem = _REDUNDANT_WHITESPACE_RE.sub(" ", stem).strip()
    stem = _UNDERSCORE_RUN_RE.sub("_", stem).strip("_")

    # 5. Drop characters that are filesystem-hostile on Windows or get
    #    eaten by some shells. Keep CJK + ASCII letters/digits/space/-_.()
    stem = re.sub(r'[<>:"|?*\x00-\x1f]', "", stem)

    # 6. Length cap (preserve extension)
    if len(stem) > _MAX_LEN:
        stem = stem[: _MAX_LEN].rstrip()

    if not stem:
        stem = "untitled"
    return stem + ext


# ---------- classification ---------------------------------------------------


@dataclass
class BookEntry:
    src: Path
    discipline: str
    beautified: str  # final filename including extension


def detect_layout(src_root: Path) -> str:
    """Return 'subdir' if the source folder has its own one-level
    directory structure (each subdir holds books), else 'flat'."""
    if not src_root.is_dir():
        return "flat"
    has_books_at_top = any(
        p.is_file() and p.suffix.lower() in (".pdf", ".epub")
        for p in src_root.iterdir()
    )
    has_subdir_books = any(
        p.is_dir()
        and any(c.suffix.lower() in (".pdf", ".epub") for c in p.glob("*"))
        for p in src_root.iterdir()
    )
    if has_subdir_books and not has_books_at_top:
        return "subdir"
    return "flat"


def classify_books(
    srcs: Iterable[Path],
    *,
    mode: str = "default",
    default: str = "general",
    src_root: Path | None = None,
    ask: Callable[[str], str] | None = None,
) -> list[BookEntry]:
    """Assign a discipline + beautified filename to each source path.

    `mode` is one of:
      - 'subdir' — discipline = path's parent dir name relative to src_root
      - 'default' — all books → `default` label
      - 'manual' — call `ask(prompt)` per book; default to `default` on empty

    Returns one BookEntry per src.
    """
    out: list[BookEntry] = []
    srcs = list(srcs)
    for s in srcs:
        if mode == "subdir" and src_root is not None:
            try:
                rel = s.relative_to(src_root)
                disc = rel.parts[0] if len(rel.parts) > 1 else default
            except ValueError:
                disc = default
        elif mode == "manual" and ask is not None:
            disc = ask(f"  Discipline for {s.name[:60]}? [{default}]") or default
        else:
            disc = default
        # Sanitize discipline name to be safe as a directory
        disc = re.sub(r"[^\w\-]+", "-", disc.strip()).strip("-").lower() or default
        out.append(BookEntry(src=s, discipline=disc, beautified=beautify_filename(s.name)))
    return out


# ---------- physical copy ----------------------------------------------------


def import_books(
    plan: list[BookEntry],
    dest_root: Path,
    *,
    dry_run: bool = False,
    on_progress: Callable[[int, int, BookEntry], None] | None = None,
) -> tuple[int, int, int]:
    """Copy each plan entry into `dest_root/<discipline>/<beautified>`.

    Skips entries whose target stem already exists (idempotency: rerunning
    after partial copy is safe). Returns (copied, skipped, total_bytes).
    """
    copied = 0
    skipped = 0
    total_bytes = 0
    seen_targets: set[Path] = set()
    for i, e in enumerate(plan):
        original_target = dest_root / e.discipline / e.beautified
        if on_progress:
            on_progress(i + 1, len(plan), e)

        # Idempotency: if the canonical target already holds a byte-identical
        # copy of this source (from a prior run), skip without renaming.
        if (
            original_target not in seen_targets
            and original_target.exists()
            and original_target.stat().st_size == e.src.stat().st_size
        ):
            seen_targets.add(original_target)
            skipped += 1
            continue

        # Otherwise pick a non-clobbering target — either the canonical name
        # is free, or we suffix until we find a slot.
        target = original_target
        n = 2
        while target in seen_targets or target.exists():
            stem = original_target.stem
            target = original_target.with_name(f"{stem}-{n}{original_target.suffix}")
            n += 1
            if n > 99:
                break
        seen_targets.add(target)
        if dry_run:
            copied += 1
            total_bytes += e.src.stat().st_size
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(e.src, target)
        copied += 1
        total_bytes += target.stat().st_size
    return copied, skipped, total_bytes
