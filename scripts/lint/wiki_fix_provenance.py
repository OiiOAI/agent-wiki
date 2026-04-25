"""Backfix truncated/malformed provenance anchors in committed wiki pages.

The LLM occasionally truncates long Chinese book filenames mid-string
(e.g. drops 14 chars from the middle of a 200-char title), producing
paths that look plausible but don't exist on disk. This script walks
`wiki/`, collects every `[raw/...]` reference, and rewrites the
unique-best match against the actual `raw/books/` filesystem.

Match strategy (in order of confidence):
  1. exact path exists → no-op
  2. exact basename match in raw/ → snap to that path
  3. suffix similarity (last 40 chars of basename match exactly) AND
     unique → snap to that path
  4. low-confidence (multiple suffix matches, or short suffix) → log
     and leave alone

Also normalizes a small set of LLM anchor-format slips:
  - `#p108,115`     → `#p108-p115`
  - `#p560-#p602`   → `#p560-p602`
  - `#L47, #L53`    → flagged but not auto-merged (would change
                      surrounding text)

Usage:
    .venv/bin/python -m scripts.lint.wiki_fix_provenance [--dry-run]
                                                          [--write]
                                                          [--limit N]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WIKI_ROOT = REPO_ROOT / "wiki"
RAW_BOOKS = REPO_ROOT / "raw" / "books"
TMP_DIR = REPO_ROOT / "tmp"

PAGE_TYPE_DIRS = ("entities", "concepts", "topics", "sources", "analyses", "conflicts")

# Loose regex matches anything that looks like provenance — including
# malformed ones, so we can repair them.
_LOOSE_PROV_RE = re.compile(r"\[raw/[^\n]+?\.(?:pdf|epub|md|txt)[^\n]*?\]")
_STRICT_PROV_RE = re.compile(
    r"\[raw/[^\n]+?\.(?:pdf|epub|md|txt)"
    r"#(?:p\d+(?:-p?\d+)?|L\d+(?:-L?\d+)?)\]"
)
_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

# Anchor-format normalizers.
_COMMA_RANGE_RE = re.compile(r"#(p|L)(\d+),\s*(p|L)?(\d+)\]")
_DOUBLE_HASH_RANGE_RE = re.compile(r"#(p|L)(\d+)-#(p|L)(\d+)\]")


def _build_path_index() -> dict[str, list[Path]]:
    """basename → [paths] (list because rare collisions across disciplines).

    We index every file under raw/ (not just raw/books/) so the older
    `raw/inbox/...` references still resolve.
    """
    idx: dict[str, list[Path]] = defaultdict(list)
    raw = REPO_ROOT / "raw"
    if not raw.is_dir():
        return idx
    for p in raw.rglob("*"):
        if p.is_file() and p.suffix.lower() in (".pdf", ".epub", ".md", ".txt"):
            idx[p.name].append(p)
    return idx


def _build_suffix_index(path_index: dict[str, list[Path]], suffix_len: int = 40) -> dict[str, list[Path]]:
    """suffix(last N chars of basename) → [paths]. For fuzzy match."""
    sfx: dict[str, list[Path]] = defaultdict(list)
    for name, paths in path_index.items():
        if len(name) >= suffix_len:
            sfx[name[-suffix_len:]].extend(paths)
    return sfx


def _resolve_path(
    emitted_path: str,
    path_by_basename: dict[str, list[Path]],
    suffix_index: dict[str, list[Path]],
    *,
    suffix_len: int = 40,
) -> tuple[str | None, str]:
    """Try to map a (possibly broken) emitted path to an existing one.

    Returns (resolved_relative_path | None, reason).
    """
    abs_target = REPO_ROOT / emitted_path
    if abs_target.exists():
        return emitted_path, "exact"
    emitted_name = Path(emitted_path).name
    # 2. exact basename match
    if emitted_name in path_by_basename:
        cands = path_by_basename[emitted_name]
        if len(cands) == 1:
            return str(cands[0].relative_to(REPO_ROOT)), "basename"
        return None, f"basename-ambiguous ({len(cands)})"
    # 3. suffix match (last N chars)
    if len(emitted_name) >= suffix_len:
        key = emitted_name[-suffix_len:]
        cands = suffix_index.get(key, [])
        if len(cands) == 1:
            return str(cands[0].relative_to(REPO_ROOT)), "suffix"
        if len(cands) > 1:
            return None, f"suffix-ambiguous ({len(cands)})"
    return None, "no-match"


def _fix_anchor_format(anchor: str) -> tuple[str, bool]:
    """Normalize known LLM slips that the strict validator rejects.

    We deliberately do NOT touch `#p1-228]` (no leading p on the second
    number) because the strict regex accepts it via `-p?\\d+` — touching
    it would just churn 9k pages without changing any lint outcome.
    """
    fixed = _COMMA_RANGE_RE.sub(r"#\g<1>\g<2>-\g<3>\g<4>]", anchor)
    fixed = _DOUBLE_HASH_RANGE_RE.sub(r"#\g<1>\g<2>-\g<3>\g<4>]", fixed)
    return fixed, fixed != anchor


def _walk_pages() -> list[Path]:
    pages: list[Path] = []
    for sub in PAGE_TYPE_DIRS:
        d = WIKI_ROOT / sub
        if not d.is_dir():
            continue
        pages.extend(sorted(d.glob("*.md")))
    return pages


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true", default=True,
                    help="default; print plan only")
    ap.add_argument("--write", action="store_true",
                    help="actually rewrite wiki files (overrides --dry-run)")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args(argv)
    write = args.write

    print("[fix_provenance] indexing raw/...", flush=True)
    path_idx = _build_path_index()
    sfx_idx = _build_suffix_index(path_idx)
    print(f"[fix_provenance] {sum(len(v) for v in path_idx.values())} files indexed", flush=True)

    pages = _walk_pages()
    if args.limit:
        pages = pages[: args.limit]

    stats: Counter[str] = Counter()
    rewrites_per_page: dict[str, list[tuple[str, str]]] = {}
    for p in pages:
        try:
            txt = p.read_text(encoding="utf-8")
        except OSError:
            continue
        # Operate on body only — never touch frontmatter. Single-quoted
        # YAML escapes apostrophes by doubling (`Descartes''`); rewriting
        # those to a single `'` in the YAML breaks the parser. The body
        # has no such escape — apostrophes are literal.
        m_fm = _FRONTMATTER_RE.match(txt)
        if m_fm:
            head, body = txt[: m_fm.end()], txt[m_fm.end():]
        else:
            head, body = "", txt
        new_body = body
        rewrites: list[tuple[str, str]] = []
        # Process unique refs only — multiple occurrences get the same fix.
        seen: set[str] = set()
        for m in _LOOSE_PROV_RE.finditer(body):
            ref = m.group(0)
            if ref in seen:
                continue
            seen.add(ref)
            # Step 1: anchor-format fix
            fixed_ref, fmt_changed = _fix_anchor_format(ref)
            # Step 2: path resolution
            inner = fixed_ref.strip("[]")
            path_part, sep, anchor = inner.partition("#")
            resolved, reason = _resolve_path(path_part, path_idx, sfx_idx)
            path_changed = False
            if resolved and resolved != path_part:
                fixed_ref = f"[{resolved}#{anchor}]" if sep else f"[{resolved}]"
                path_changed = True

            stats[reason] += 1
            if fmt_changed:
                stats["format_fixed"] += 1
            if path_changed:
                stats["path_fixed"] += 1
            if fmt_changed or path_changed:
                new_body = new_body.replace(ref, fixed_ref)
                rewrites.append((ref, fixed_ref))

        if rewrites and new_body != body:
            rewrites_per_page[str(p.relative_to(REPO_ROOT))] = rewrites
            if write:
                p.write_text(head + new_body, encoding="utf-8")

    # Report
    print(f"\n[fix_provenance] rewrites planned in {len(rewrites_per_page)} pages")
    for k, v in stats.most_common():
        print(f"  {k:30s} {v}")

    TMP_DIR.mkdir(parents=True, exist_ok=True)
    out = TMP_DIR / "fix_provenance_report.json"
    out.write_text(
        json.dumps(
            {
                "stats": dict(stats),
                "rewrites_per_page": {k: v for k, v in rewrites_per_page.items()},
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"\n[fix_provenance] report written: {out.relative_to(REPO_ROOT)}")
    if not write:
        print("[fix_provenance] DRY RUN — pass --write to actually modify wiki files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
