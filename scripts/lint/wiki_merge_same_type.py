"""Merge C1 same-title clusters (same-type and cross-type).

Default mode: only same-type groups (safe — no schema-field leakage
risk). Pass --include-cross-type to also process cross-type groups
(entity↔concept, concept↔topic, etc.) — the canonical's TYPE wins
and any fields foreign to that type's schema are dropped post-merge.

Always skips concept↔source groups (different SOP roles — concept
describes the idea, source is the book metadata).

Canonical-pick heuristic:
  1. Larger content wins (longer body — more facts already accumulated).
  2. Ties broken by shortest slug (avoids `bicycle-exercise` over
     `bicycle`; `bernard-katz` over `katz-bernard`).
  3. Final tie-break by alphabetical slug.

Reuses commit_batch._merge_pages and the link-rewrite logic from
wiki_merge_dups.py.
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
from scripts.ingest.schemas import OPTIONAL_FIELDS, REQUIRED_FIELDS  # noqa: E402


def _sanitize_frontmatter(page) -> None:
    """Cross-type merges can drag fields from the duplicate's type into the
    canonical's frontmatter (e.g. entity's `canonical: true` leaking onto
    a concept). Strip anything not in the canonical type's allowed set.

    Mutates `page.frontmatter` in place. Always preserves `id` since it's
    universal but not in the schema-field tables.
    """
    ptype = page.frontmatter.get("type")
    if ptype not in REQUIRED_FIELDS:
        return
    allowed = REQUIRED_FIELDS[ptype] | OPTIONAL_FIELDS.get(ptype, set()) | {"id"}
    foreign = [k for k in page.frontmatter if k not in allowed]
    for k in foreign:
        page.frontmatter.pop(k, None)


def _content_size(path: Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return 0


def main(write: bool = False, include_cross_type: bool = False) -> int:
    report = json.loads((REPO_ROOT / "tmp" / "conflict_report.json").read_text())
    same_title = report["same_title"]

    # Filter
    groups: list[tuple[str, list[dict]]] = []
    skipped_cross = 0
    skipped_concept_source = 0
    for title, ents in same_title.items():
        types = {e["path"].split("/")[1] for e in ents}
        # Always skip concept↔source: SOP roles differ (idea vs book metadata)
        if "sources" in types and "concepts" in types:
            skipped_concept_source += 1
            continue
        if len(types) == 1:
            groups.append((title, ents))
        elif include_cross_type:
            groups.append((title, ents))
        else:
            skipped_cross += 1

    print(f"[merge_same_type] {len(groups)} groups to process; "
          f"skipped {skipped_cross} cross-type (re-run with --include-cross-type), "
          f"{skipped_concept_source} concept↔source (always skip)")

    plan = []
    for title, ents in groups:
        # Rank candidates
        def rank(e):
            path = REPO_ROOT / e["path"]
            slug = Path(e["path"]).stem
            return (
                -_content_size(path),    # larger first (negative for ascending)
                len(slug),                # shorter slug first
                slug,                     # alphabetical
            )
        sorted_ents = sorted(ents, key=rank)
        canonical = sorted_ents[0]
        duplicates = sorted_ents[1:]
        plan.append({
            "title": title,
            "canonical": canonical["path"],
            "duplicates": [d["path"] for d in duplicates],
            "canonical_size": _content_size(REPO_ROOT / canonical["path"]),
            "dup_sizes": [_content_size(REPO_ROOT / d["path"]) for d in duplicates],
        })

    plan_path = REPO_ROOT / "tmp" / "c1_same_type_plan.json"
    plan_path.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"plan written: {plan_path.relative_to(REPO_ROOT)}")

    # Show a sample
    print(f"\nfirst 8 of {len(plan)}:")
    for p in plan[:8]:
        print(f"  {p['title']!r}: canonical={Path(p['canonical']).stem}"
              f" ({p['canonical_size']}B) ← {[Path(d).stem for d in p['duplicates']]}")

    if not write:
        print(f"\nDRY RUN. Pass --write to execute.")
        return 0

    # Execute merges
    print(f"\n[merge_same_type] executing {len(plan)} merges")
    today = "2026-05-05"
    rewrites: list[tuple[re.Pattern, str]] = []
    deleted: list[Path] = []

    for entry in plan:
        canonical_path = REPO_ROOT / entry["canonical"]
        canonical_text = canonical_path.read_text(encoding="utf-8")
        canonical_page = _parse_page(canonical_text)
        canonical_slug = Path(entry["canonical"]).stem
        canonical_title = canonical_page.frontmatter.get("title") or canonical_slug

        for dup_path in entry["duplicates"]:
            dup_full = REPO_ROOT / dup_path
            if not dup_full.exists():
                continue
            dup_text = dup_full.read_text(encoding="utf-8")
            dup_page = _parse_page(dup_text)
            dup_slug = Path(dup_path).stem
            dup_title = dup_page.frontmatter.get("title") or dup_slug

            book_stem = f"merged-from-{dup_slug}"
            canonical_page = _merge_pages(canonical_page, dup_page, book_stem, today)
            # Drop fields foreign to canonical type's schema (cross-type merges).
            _sanitize_frontmatter(canonical_page)
            deleted.append(dup_full)

            # Slug-based wikilink rewrite
            rewrites.append((
                re.compile(r"\[\[" + re.escape(dup_slug) + r"\]\]"),
                f"[[{canonical_slug}]]",
            ))
            # Title-based wikilink rewrite (only if titles differ — usually
            # same-type-same-title means identical title, so this is a no-op,
            # but covers caps/whitespace variants like "Acetylcholine" vs
            # "acetylcholine")
            if dup_title != canonical_title:
                rewrites.append((
                    re.compile(r"\[\[" + re.escape(dup_title) + r"\]\]"),
                    f"[[{canonical_title}]]",
                ))

        canonical_path.write_text(_render_page(canonical_page), encoding="utf-8")

    print(f"  merged content into {len(plan)} canonical pages")

    # Apply link rewrites across wiki/ (skip files about to be deleted)
    deleted_set = set(deleted)
    files_touched = 0
    total_subs = 0
    for p in WIKI_ROOT.rglob("*.md"):
        if p.name == "AGENTS.md" or p in deleted_set:
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

    # Delete duplicates
    for f in deleted:
        if f.exists():
            f.unlink()
    print(f"  deleted {len(deleted)} duplicate files")

    return 0


if __name__ == "__main__":
    import sys as _sys
    write = "--write" in _sys.argv
    include_cross = "--include-cross-type" in _sys.argv
    raise SystemExit(main(write=write, include_cross_type=include_cross))
