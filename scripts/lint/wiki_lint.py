"""Wiki-wide lint over `wiki/`.

Re-runs the 11 validate.py invariants across every committed page, plus
two wiki-only checks the staged validator can't make:

  W1. dangling [[wikilink]] — target slug not present anywhere in wiki/
  W2. index drift            — page exists but missing from wiki/index.md
                                (or vice-versa: index lists page that's gone)

Output is a punch list to `tmp/lint_report.md` with per-rule counts and a
sample of offending pages, plus a JSON dump for tooling. Read-only — never
modifies pages. Fix decisions go through the next ingest/lint pass.

Usage:
    .venv/bin/python -m scripts.lint.wiki_lint [--limit N] [--rule R]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
WIKI_ROOT = REPO_ROOT / "wiki"
TMP_DIR = REPO_ROOT / "tmp"
PAGE_TYPE_DIRS = ("entities", "concepts", "topics", "sources", "analyses", "conflicts", "dashboards")

sys.path.insert(0, str(REPO_ROOT))
from scripts.ingest.validate import (  # noqa: E402
    ValidationError,
    validate_page,
)

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
_WIKILINK_RE = re.compile(r"\[\[([^\[\]]*?)\]\]")
# Match `- [[Title]]` lines. Allow `]` characters INSIDE the title as long
# as the line eventually closes with `]]` and the title is balanced w.r.t.
# `[`/`]` (e.g. `[[Lipoprotein(a) [Lp(a)]]]` — title is `Lipoprotein(a) [Lp(a)]`).
_INDEX_LINE_RE = re.compile(r"^- \[\[(.+?)\]\](?:\s|$|\s*—)")


def _walk_wiki_pages() -> list[Path]:
    pages: list[Path] = []
    for sub in PAGE_TYPE_DIRS:
        d = WIKI_ROOT / sub
        if not d.is_dir():
            continue
        pages.extend(sorted(d.glob("*.md")))
    return pages


def _build_lookups(pages: list[Path]) -> tuple[dict[str, Path], set[str]]:
    """Return (slug_to_path, all_titles_lowered).

    slug = file stem (kebab-case for new pages, Title Case for legacy 3).
    Aliases also count as valid wikilink targets.
    """
    slug_to_path: dict[str, Path] = {}
    titles: set[str] = set()
    for p in pages:
        slug_to_path[p.stem.lower()] = p
        try:
            txt = p.read_text(encoding="utf-8")
        except OSError:
            continue
        m = _FRONTMATTER_RE.match(txt)
        if not m:
            continue
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            continue
        title = str(fm.get("title") or p.stem)
        titles.add(title.lower())
        # Aliases (entity pages mostly) are also valid wikilink targets.
        for alias in fm.get("aliases") or []:
            titles.add(str(alias).lower())
        # Sometimes [[page-id]] is used in addition to [[Page Title]].
        if pid := fm.get("id"):
            titles.add(str(pid).lower())
    return slug_to_path, titles


def _check_dangling_links(
    page_path: Path, body: str, valid_targets: set[str], slug_to_path: dict[str, Path]
) -> list[ValidationError]:
    errs: list[ValidationError] = []
    for m in _WIKILINK_RE.finditer(body):
        target = m.group(1).strip()
        if not target:
            continue
        key = target.lower()
        if key in valid_targets:
            continue
        if key in slug_to_path:
            continue
        # Try kebab-case-ifying spaces — many [[Title Words]] correspond to
        # `title-words.md` slugs that we haven't yet stored as titles.
        kebab = re.sub(r"[\s_]+", "-", key)
        kebab = re.sub(r"[^a-z0-9-]", "", kebab)
        if kebab in slug_to_path:
            continue
        errs.append(
            ValidationError(
                "dangling_link",
                f"target [[{target}]] not found in wiki/",
                str(page_path.relative_to(REPO_ROOT)),
            )
        )
    return errs


def _check_index_drift(pages: list[Path]) -> list[ValidationError]:
    """Compare wiki/index.md listings against actual pages on disk.

    Skips fenced code blocks (the index template includes a literal
    ` ```text\n- [[Page Name]] — One-line summary.\n``` ` example) and
    backtick-quoted entries.
    """
    errs: list[ValidationError] = []
    idx_path = WIKI_ROOT / "index.md"
    if not idx_path.exists():
        return [ValidationError("index_drift", "wiki/index.md missing")]
    idx_titles: set[str] = set()
    in_fence = False
    for line in idx_path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = _INDEX_LINE_RE.match(line)
        if m:
            idx_titles.add(m.group(1).lower())

    page_titles: set[str] = set()
    for p in pages:
        if p.parent.name == "conflicts":
            # conflicts have their own index section; treat separately if needed
            continue
        try:
            txt = p.read_text(encoding="utf-8")
        except OSError:
            continue
        m = _FRONTMATTER_RE.match(txt)
        if not m:
            continue
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            continue
        title = str(fm.get("title") or p.stem)
        page_titles.add(title.lower())

    only_in_idx = idx_titles - page_titles
    only_on_disk = page_titles - idx_titles
    for t in sorted(only_in_idx):
        errs.append(
            ValidationError("index_drift", f"index.md lists [[{t}]] but no page found")
        )
    for t in sorted(only_on_disk):
        errs.append(
            ValidationError("index_drift", f"page titled {t!r} on disk but missing from index.md")
        )
    return errs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--limit", type=int, default=None, help="lint first N pages only")
    ap.add_argument("--rule", type=str, default=None, help="only show this rule")
    ap.add_argument("--quiet", action="store_true", help="no per-page progress")
    args = ap.parse_args(argv)

    pages = _walk_wiki_pages()
    if args.limit:
        pages = pages[: args.limit]
    print(f"[wiki_lint] linting {len(pages)} pages", flush=True)

    # Pre-compute id set so check_id_uniqueness doesn't fire on the page itself.
    # We pass empty set and skip uniqueness — every page is "the existing
    # version" in a wiki-wide pass. (uniqueness is a staging-time check.)
    skip_rules = {"id_uniqueness"}

    slug_to_path, valid_targets = _build_lookups(pages)

    all_errs: list[ValidationError] = []
    by_page: dict[str, int] = {}
    for i, p in enumerate(pages):
        try:
            txt = p.read_text(encoding="utf-8")
        except OSError as e:
            all_errs.append(ValidationError("io", str(e), str(p.relative_to(REPO_ROOT))))
            continue
        rel = str(p.relative_to(REPO_ROOT))
        errs = validate_page(
            txt,
            existing_ids=set(),
            page_path=rel,
            repo_root=REPO_ROOT,
        )
        # Strip skipped rules.
        errs = [e for e in errs if e.rule not in skip_rules]
        # Add wiki-only dangling-link check.
        body = txt[_FRONTMATTER_RE.match(txt).end():] if _FRONTMATTER_RE.match(txt) else txt
        errs.extend(_check_dangling_links(p, body, valid_targets, slug_to_path))
        all_errs.extend(errs)
        if errs:
            by_page[rel] = len(errs)
        if not args.quiet and (i + 1) % 500 == 0:
            print(f"  [{i+1}/{len(pages)}] running... {len(all_errs)} errors so far", flush=True)

    # Index drift is a wiki-global check.
    all_errs.extend(_check_index_drift(pages))

    if args.rule:
        all_errs = [e for e in all_errs if e.rule == args.rule]

    rule_counts = Counter(e.rule for e in all_errs)
    print(f"\n[wiki_lint] {len(all_errs)} total errors across {len(by_page)} pages")
    for rule, n in rule_counts.most_common():
        print(f"  {rule:30s} {n:6d}")

    # Write reports.
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    json_out = TMP_DIR / "lint_report.json"
    json_out.write_text(
        json.dumps(
            {
                "summary": dict(rule_counts),
                "errors": [asdict(e) for e in all_errs],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    md_out = TMP_DIR / "lint_report.md"
    by_rule_samples: dict[str, list[ValidationError]] = defaultdict(list)
    for e in all_errs:
        if len(by_rule_samples[e.rule]) < 8:
            by_rule_samples[e.rule].append(e)
    md_lines = [
        "# Wiki Lint Report",
        "",
        f"Pages scanned: **{len(pages)}**.",
        f"Total errors: **{len(all_errs)}** across **{len(by_page)}** pages.",
        "",
        "## Rule rollup",
        "",
        "| Rule | Count |",
        "|---|---:|",
    ]
    for rule, n in rule_counts.most_common():
        md_lines.append(f"| `{rule}` | {n} |")
    md_lines.append("")
    md_lines.append("## Sample (first 8 per rule)")
    md_lines.append("")
    for rule, samples in by_rule_samples.items():
        md_lines.append(f"### `{rule}` ({rule_counts[rule]} total)")
        md_lines.append("")
        for s in samples:
            md_lines.append(f"- {s}")
        md_lines.append("")
    md_lines.append("## Top offending pages")
    md_lines.append("")
    md_lines.append("| Page | Errors |")
    md_lines.append("|---|---:|")
    for path, n in sorted(by_page.items(), key=lambda kv: -kv[1])[:25]:
        md_lines.append(f"| `{path}` | {n} |")
    md_out.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(f"\n[wiki_lint] reports written:")
    print(f"  {json_out.relative_to(REPO_ROOT)}")
    print(f"  {md_out.relative_to(REPO_ROOT)}")
    return 0 if not all_errs else 1


if __name__ == "__main__":
    raise SystemExit(main())
