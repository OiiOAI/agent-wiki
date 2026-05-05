"""Merge near-duplicate `the-X` pages into their canonical `X` siblings.

Reads `tmp/c3_merge_plan.json` (produced by triage step) and for each
group:
  1. Reuses `commit_batch._merge_pages` to fold the duplicate's
     frontmatter + body sections into the canonical.
  2. Rewrites every `[[the-X]]` / `[[The X]]` wikilink across all of
     `wiki/` to point at the canonical slug/title.
  3. Deletes the duplicate file.

Pure-text merging — no LLM call. Idempotent: rerunning is a no-op
once the duplicate file is gone.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WIKI_ROOT = REPO_ROOT / "wiki"

sys.path.insert(0, str(REPO_ROOT))
from scripts.ingest.commit_batch import (  # noqa: E402
    _merge_pages,
    _parse_page,
    _render_page,
)


def _slug_of(path: str) -> str:
    return Path(path).stem


def _build_link_rewrites(merges: list[dict]) -> list[tuple[re.Pattern, str]]:
    """For each merge, build regex pairs that rewrite link targets to
    the canonical slug / title."""
    rewrites: list[tuple[re.Pattern, str]] = []
    for m in merges:
        canonical_slug = _slug_of(m["canonical"])
        canonical_path = REPO_ROOT / m["canonical"]
        canonical_text = canonical_path.read_text(encoding="utf-8")
        canonical_page = _parse_page(canonical_text)
        canonical_title = canonical_page.frontmatter.get("title") or canonical_slug

        for dup_path in m["duplicates"]:
            dup_slug = _slug_of(dup_path)
            dup_full = REPO_ROOT / dup_path
            if not dup_full.exists():
                continue
            dup_text = dup_full.read_text(encoding="utf-8")
            dup_page = _parse_page(dup_text)
            dup_title = dup_page.frontmatter.get("title") or dup_slug

            # Slug form: [[the-X]] → [[X]]
            rewrites.append((
                re.compile(r"\[\[" + re.escape(dup_slug) + r"\]\]"),
                f"[[{canonical_slug}]]",
            ))
            # Title form: [[The X Title]] → [[Canonical Title]]
            if dup_title != canonical_title:
                rewrites.append((
                    re.compile(r"\[\[" + re.escape(dup_title) + r"\]\]"),
                    f"[[{canonical_title}]]",
                ))
    return rewrites


def main() -> int:
    plan = json.loads((REPO_ROOT / "tmp" / "c3_merge_plan.json").read_text())
    merges = plan["merges"]
    print(f"[merge_dups] {len(merges)} merge groups to process")

    today = "2026-05-05"

    # Step 1: do all merges
    deleted_files: list[Path] = []
    for m in merges:
        canonical_path = REPO_ROOT / m["canonical"]
        canonical_text = canonical_path.read_text(encoding="utf-8")
        canonical_page = _parse_page(canonical_text)

        for dup_path in m["duplicates"]:
            dup_full = REPO_ROOT / dup_path
            if not dup_full.exists():
                print(f"  SKIP missing: {dup_path}")
                continue
            dup_text = dup_full.read_text(encoding="utf-8")
            dup_page = _parse_page(dup_text)
            book_stem = f"merged-from-{_slug_of(dup_path)}"
            canonical_page = _merge_pages(
                canonical_page, dup_page, book_stem, today
            )
            deleted_files.append(dup_full)

        # Write merged result back to canonical path
        canonical_path.write_text(_render_page(canonical_page), encoding="utf-8")
        print(f"  merged → {m['canonical']} (folded {len(m['duplicates'])} dups)")

    # Step 2: rewrite wikilinks across all of wiki/
    rewrites = _build_link_rewrites(merges)
    print(f"\n[merge_dups] applying {len(rewrites)} link-rewrite rules")
    files_touched = 0
    total_subs = 0
    for p in WIKI_ROOT.rglob("*.md"):
        if p.name in ("AGENTS.md",):
            continue
        if p in deleted_files:
            continue
        try:
            txt = p.read_text(encoding="utf-8")
        except OSError:
            continue
        new = txt
        for pat, repl in rewrites:
            new, n = pat.subn(repl, new)
            total_subs += n
        if new != txt:
            p.write_text(new, encoding="utf-8")
            files_touched += 1
    print(f"  rewrote {total_subs} links across {files_touched} files")

    # Step 3: delete dup files
    print(f"\n[merge_dups] deleting {len(deleted_files)} duplicate files")
    for f in deleted_files:
        if f.exists():
            f.unlink()
            print(f"  deleted {f.relative_to(REPO_ROOT)}")

    print(f"\n[merge_dups] done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
