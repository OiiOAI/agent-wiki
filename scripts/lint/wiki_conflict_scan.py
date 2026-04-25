"""Wiki-internal conflict scan.

After S6's merge step the obvious cross-book collisions (same `id`) are
already collapsed. What this script catches is the *residual* shape:

  C1. **same title, different slug** — two pages with the same title
      (case-insensitive, whitespace-normalized). Likely candidates for
      manual merge or aliasing.
  C2. **alias collision** — page A's alias is page B's title (or another
      page's alias). The alias resolution is ambiguous.
  C3. **near-duplicate slugs** — slug pairs differing only in trivial
      noise (`-the-`, `-a-`, hyphenation). Likely the LLM emitted two
      slugs for the same concept across books.

Output: `tmp/conflict_report.md` + JSON dump. Read-only — no autofix.

Usage:
    .venv/bin/python -m scripts.lint.wiki_conflict_scan
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WIKI_ROOT = REPO_ROOT / "wiki"
TMP_DIR = REPO_ROOT / "tmp"

sys.path.insert(0, str(REPO_ROOT))
from scripts.ingest.conflict_check import (  # noqa: E402
    WikiIndexEntry,
    load_wiki_index,
    _norm,
)


def _slug_key(slug: str) -> str:
    """Strip noise to expose near-duplicate slugs.

    Drops leading/trailing 'the-' / 'a-' / 'an-', collapses repeated
    hyphens, removes parenthetical content.
    """
    s = slug.lower()
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"[-_]+", "-", s).strip("-")
    for pre in ("the-", "a-", "an-"):
        if s.startswith(pre):
            s = s[len(pre):]
        if s.endswith("-" + pre.rstrip("-")):
            s = s[: -len(pre)]
    return s


def find_same_title(index: list[WikiIndexEntry]) -> dict[str, list[WikiIndexEntry]]:
    by_title: dict[str, list[WikiIndexEntry]] = defaultdict(list)
    for e in index:
        by_title[_norm(e.title)].append(e)
    return {t: v for t, v in by_title.items() if len(v) > 1}


def find_alias_collisions(index: list[WikiIndexEntry]) -> list[tuple[str, list[WikiIndexEntry]]]:
    """For each alias appearing in any page, list all pages that claim it
    (as own title or as alias). Singleton owners are filtered out."""
    by_token: dict[str, list[WikiIndexEntry]] = defaultdict(list)
    for e in index:
        by_token[_norm(e.title)].append(e)
        for a in e.aliases:
            by_token[_norm(a)].append(e)
    collisions: list[tuple[str, list[WikiIndexEntry]]] = []
    for token, owners in by_token.items():
        # dedup by id since same page can appear via title+alias both
        uniq = list({(o.id, o.path): o for o in owners}.values())
        if len(uniq) > 1:
            collisions.append((token, uniq))
    return collisions


def find_near_duplicate_slugs(index: list[WikiIndexEntry]) -> dict[str, list[WikiIndexEntry]]:
    by_key: dict[str, list[WikiIndexEntry]] = defaultdict(list)
    for e in index:
        slug = Path(e.path).stem
        by_key[_slug_key(slug)].append(e)
    return {k: v for k, v in by_key.items() if len(v) > 1 and len({e.id for e in v}) > 1}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args(argv)

    print("[conflict_scan] loading wiki index...", flush=True)
    index = load_wiki_index(WIKI_ROOT)
    if args.limit:
        index = index[: args.limit]
    print(f"[conflict_scan] {len(index)} pages indexed", flush=True)

    same_title = find_same_title(index)
    alias_coll = find_alias_collisions(index)
    near_dup = find_near_duplicate_slugs(index)

    print(f"\n[conflict_scan] results:")
    print(f"  C1 same-title (different slug):       {len(same_title)} groups")
    print(f"  C2 alias collisions (≥2 owners):      {len(alias_coll)} tokens")
    print(f"  C3 near-duplicate slugs:              {len(near_dup)} groups")

    # MD report
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    md = ["# Wiki Conflict Scan", "",
          f"Pages indexed: **{len(index)}**.", "",
          "## C1. Same title, different slug", "",
          f"_{len(same_title)} groups._", ""]
    for title, ents in sorted(same_title.items())[:60]:
        md.append(f"- **{title}**")
        for e in ents:
            md.append(f"  - `{e.path}` (id={e.id})")
    md.append("")
    md.append("## C2. Alias collisions (token claimed by ≥2 pages)")
    md.append("")
    md.append(f"_{len(alias_coll)} tokens._")
    md.append("")
    for token, owners in sorted(alias_coll, key=lambda kv: kv[0])[:60]:
        md.append(f"- **{token}** — {len(owners)} owners")
        for o in owners:
            md.append(f"  - `{o.path}` (title={o.title!r})")
    md.append("")
    md.append("## C3. Near-duplicate slugs")
    md.append("")
    md.append(f"_{len(near_dup)} groups (after stripping `the-/a-/an-`, parens, hyphen noise)._")
    md.append("")
    for key, ents in sorted(near_dup.items())[:60]:
        md.append(f"- **{key}**")
        for e in ents:
            md.append(f"  - `{e.path}` (title={e.title!r})")
    md_out = TMP_DIR / "conflict_report.md"
    md_out.write_text("\n".join(md) + "\n", encoding="utf-8")

    json_out = TMP_DIR / "conflict_report.json"
    json_out.write_text(
        json.dumps(
            {
                "same_title": {
                    t: [{"id": e.id, "path": e.path, "title": e.title} for e in ents]
                    for t, ents in same_title.items()
                },
                "alias_collisions": [
                    {
                        "token": t,
                        "owners": [
                            {"id": e.id, "path": e.path, "title": e.title}
                            for e in ents
                        ],
                    }
                    for t, ents in alias_coll
                ],
                "near_duplicate_slugs": {
                    k: [{"id": e.id, "path": e.path, "title": e.title} for e in ents]
                    for k, ents in near_dup.items()
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"\n[conflict_scan] reports written:")
    print(f"  {md_out.relative_to(REPO_ROOT)}")
    print(f"  {json_out.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
