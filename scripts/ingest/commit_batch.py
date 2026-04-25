"""S6 — Phase H: batch commit staged pages into wiki/ + per-book git trail.

Walks `tmp/ingest_progress.json` in completion order, for each `ok` book:

  1. Walk `tmp/ingest_staging/<book>/<type>/<slug>.md`.
  2. For each page:
     - If `wiki/<type>/<slug>.md` does not exist → fresh copy.
     - If it does exist → MERGE (frontmatter sources/tags/related list-union;
       body key_facts/inferences/uncertainties append-with-dedup; preserve
       first book's title + summary; append change-note line).
  3. Append a structured entry to `wiki/log.md`.
  4. `git add` all touched paths + `git commit -m "ingest: <book_stem>"`.

After all books: rebuild `wiki/index.md` by scanning final wiki/ tree, then
`git tag ingest-batch-<YYYYMMDD-HHMM>`.

Usage:
    python -m scripts.ingest.commit_batch [--dry-run] [--limit N] [--no-tag]
                                          [--start-from <book_stem>]

`--dry-run` prints planned actions without writing anything or invoking git.

Idempotency: if a book's staging dir is missing, it's silently skipped (the
book may have already been committed in a previous interrupted run). Rerun
safe — pages already present are detected and the merge path takes over.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
STAGING_ROOT = REPO_ROOT / "tmp" / "ingest_staging"
WIKI_ROOT = REPO_ROOT / "wiki"
PROGRESS_PATH = REPO_ROOT / "tmp" / "ingest_progress.json"

PAGE_TYPE_DIRS = ("entities", "concepts", "topics", "sources", "analyses")

_FM_SPLIT_RE = re.compile(r"^---\s*\n", re.MULTILINE)
_SECTION_RE = re.compile(r"^(## .+)$", re.MULTILINE)


# ---------- page parsing / rendering ---------------------------------------


@dataclass
class ParsedPage:
    frontmatter: dict
    title_line: str  # the "# Title" header line (or empty if missing)
    sections: dict[str, str]  # section header → body text (header excluded)
    section_order: list[str]   # preserves original order


def _parse_page(md_text: str) -> ParsedPage:
    """Split a compiled wiki page into frontmatter + section dict.

    Preserves section order so we can re-emit in the same shape.
    """
    parts = _FM_SPLIT_RE.split(md_text, maxsplit=2)
    if len(parts) >= 3 and parts[0].strip() == "":
        fm_raw, body = parts[1], parts[2]
        fm = yaml.safe_load(fm_raw) or {}
    else:
        fm, body = {}, md_text
    body = body.lstrip("\n")

    # Pull the leading "# Title" line if present.
    title_line = ""
    if body.startswith("# "):
        nl = body.find("\n")
        title_line = body[: nl if nl != -1 else len(body)]
        body = body[nl + 1:] if nl != -1 else ""

    # Split body into ## sections preserving order.
    chunks = _SECTION_RE.split(body)
    # `chunks` alternates: [pre, header1, content1, header2, content2, ...]
    sections: dict[str, str] = {}
    order: list[str] = []
    pre = chunks[0].strip("\n")
    if pre:
        # rare: content before any ## header — preserve under empty key
        sections[""] = pre
        order.append("")
    for i in range(1, len(chunks), 2):
        header = chunks[i].strip()
        content = chunks[i + 1] if i + 1 < len(chunks) else ""
        sections[header] = content.strip("\n")
        order.append(header)

    return ParsedPage(
        frontmatter=fm,
        title_line=title_line,
        sections=sections,
        section_order=order,
    )


def _render_page(page: ParsedPage) -> str:
    fm_text = yaml.safe_dump(
        page.frontmatter,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )
    out = ["---", fm_text.rstrip(), "---", ""]
    if page.title_line:
        out.append(page.title_line)
        out.append("")
    for header in page.section_order:
        if header == "":
            out.append(page.sections[header])
            out.append("")
            continue
        out.append(header)
        out.append("")
        out.append(page.sections[header])
        out.append("")
    return "\n".join(out).rstrip() + "\n"


# ---------- merge logic ----------------------------------------------------


def _list_union_preserve_order(a: list, b: list) -> list:
    seen = set()
    out = []
    for item in (*a, *b):
        key = item if isinstance(item, str) else json.dumps(item, sort_keys=True)
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def _merge_related(a: dict | None, b: dict | None) -> dict:
    a = a or {}
    b = b or {}
    keys = ("broader", "narrower", "adjacent", "concepts", "topics", "entities")
    out: dict = {}
    for k in keys:
        merged = _list_union_preserve_order(a.get(k) or [], b.get(k) or [])
        if merged:
            out[k] = merged
    return out


def _merge_frontmatter(existing: dict, new: dict, today: str) -> dict:
    """Existing wins on identity fields; lists/dicts union; updated → today."""
    merged = dict(existing)  # shallow copy
    list_fields = ("sources", "aliases", "tags")
    for f in list_fields:
        merged[f] = _list_union_preserve_order(
            existing.get(f) or [], new.get(f) or []
        )
    if "related" in existing or "related" in new:
        merged["related"] = _merge_related(
            existing.get("related"), new.get("related")
        )
    merged["updated"] = today
    # preserve any source-page extras that existed already; add missing ones
    # only when existing didn't set them (e.g., reliability)
    for k, v in new.items():
        if k in merged:
            continue
        merged[k] = v
    return merged


_FACT_LINE_RE = re.compile(r"^\s*-\s*(.+?)(?:\s*\[raw/.+?\])?\s*$")


def _claim_key(line: str) -> str:
    """Strip provenance bracket so we can dedup on the claim text alone."""
    m = _FACT_LINE_RE.match(line)
    return (m.group(1) if m else line).strip().lower()


def _merge_bullet_section(existing_body: str, new_body: str) -> str:
    """Append bullet lines from `new_body` not already in `existing_body`.

    Dedup is by claim text (strip [raw/...] bracket) for key_facts; for
    inferences/uncertainties, the whole stripped line is the key.
    """
    if not new_body.strip():
        return existing_body
    if not existing_body.strip():
        return new_body
    existing_lines = existing_body.splitlines()
    seen = {_claim_key(l) for l in existing_lines if l.strip().startswith("-")}
    appended = list(existing_lines)
    for line in new_body.splitlines():
        if not line.strip().startswith("-"):
            continue
        if _claim_key(line) in seen:
            continue
        seen.add(_claim_key(line))
        appended.append(line)
    return "\n".join(appended)


_RELATED_LINE_RE = re.compile(r"^\s*-\s*([A-Za-z]+):\s*\[\[([^\]]+)\]\]\s*$")
_RELATED_LABEL_ORDER = ("Broader", "Narrower", "Adjacent", "Concepts", "Topics", "Entities")


def _parse_related_body(body: str) -> dict[str, list[str]]:
    """Parse a `## Related pages` body into `{label: [slug, ...]}`.

    Compile.py emits more labels in the body than frontmatter.related
    captures (concept pages have Concepts/Entities in body but only
    broader/narrower/adjacent in frontmatter), so the body is the
    source of truth for cross-book merge purposes.
    """
    out: dict[str, list[str]] = {label: [] for label in _RELATED_LABEL_ORDER}
    for line in body.splitlines():
        m = _RELATED_LINE_RE.match(line)
        if not m:
            continue
        label, slug = m.group(1), m.group(2).strip()
        if label not in out:
            out[label] = []
        if slug not in out[label]:
            out[label].append(slug)
    return out


def _merge_related_bodies(existing_body: str, new_body: str) -> str:
    """Union the parsed related labels, preserving original label order."""
    a = _parse_related_body(existing_body)
    b = _parse_related_body(new_body)
    merged: dict[str, list[str]] = {}
    seen_labels = list(a.keys()) + [k for k in b if k not in a]
    for label in seen_labels:
        union: list[str] = []
        for slug in (*a.get(label, []), *b.get(label, [])):
            if slug not in union:
                union.append(slug)
        if union:
            merged[label] = union
    lines: list[str] = []
    for label in _RELATED_LABEL_ORDER:
        for slug in merged.get(label, []):
            lines.append(f"- {label}: [[{slug}]]")
    for label in merged:
        if label in _RELATED_LABEL_ORDER:
            continue
        for slug in merged[label]:
            lines.append(f"- {label}: [[{slug}]]")
    return "\n".join(lines)


def _merge_provenance_section(existing_body: str, merged_sources: list) -> str:
    """Re-emit `## Provenance` block: keep first line shape, add Additional source lines."""
    if not merged_sources:
        return existing_body
    lines = [f"- Primary source: {merged_sources[0]}"]
    for extra in merged_sources[1:]:
        lines.append(f"- Additional source: {extra}")
    return "\n".join(lines)


def _merge_pages(existing: ParsedPage, new: ParsedPage, book_stem: str, today: str) -> ParsedPage:
    """Combine `existing` (in wiki/) with `new` (from staging) per book."""
    merged_fm = _merge_frontmatter(existing.frontmatter, new.frontmatter, today)
    merged_sections = dict(existing.sections)
    merged_order = list(existing.section_order)

    # Append new key_facts / inferences / uncertainties via dedup union.
    bullet_sections = ("## Key facts", "## Inferences", "## Uncertainties")
    for header in bullet_sections:
        new_body = new.sections.get(header, "")
        if not new_body.strip():
            continue
        if header in merged_sections:
            merged_sections[header] = _merge_bullet_section(
                merged_sections[header], new_body
            )
        else:
            merged_sections[header] = new_body
            # insert before Provenance/Change notes if possible
            insert_at = len(merged_order)
            for tail in ("## Related pages", "## Provenance", "## Change notes"):
                if tail in merged_order:
                    insert_at = min(insert_at, merged_order.index(tail))
            merged_order.insert(insert_at, header)

    # Merge `## Related pages` body directly — it's the source of truth
    # because compile.py emits more labels in body than frontmatter captures.
    new_related_body = new.sections.get("## Related pages", "")
    existing_related_body = existing.sections.get("## Related pages", "")
    if new_related_body.strip() or existing_related_body.strip():
        merged_related = _merge_related_bodies(existing_related_body, new_related_body)
        if merged_related:
            if "## Related pages" not in merged_sections:
                merged_order.insert(
                    merged_order.index("## Provenance")
                    if "## Provenance" in merged_order
                    else len(merged_order),
                    "## Related pages",
                )
            merged_sections["## Related pages"] = merged_related

    # Refresh provenance to list all merged sources.
    if "## Provenance" in merged_sections:
        merged_sections["## Provenance"] = _merge_provenance_section(
            merged_sections["## Provenance"], merged_fm.get("sources") or []
        )

    # Change notes: append a line for this merge.
    note = f"- {today} — merged contributions from `{book_stem}`."
    if "## Change notes" in merged_sections:
        body = merged_sections["## Change notes"].rstrip()
        if note not in body:
            merged_sections["## Change notes"] = body + "\n" + note
    else:
        merged_sections["## Change notes"] = note
        if "## Change notes" not in merged_order:
            merged_order.append("## Change notes")

    return ParsedPage(
        frontmatter=merged_fm,
        title_line=existing.title_line or new.title_line,
        sections=merged_sections,
        section_order=merged_order,
    )


# ---------- per-book commit ------------------------------------------------


@dataclass
class BookCommitResult:
    book_stem: str
    created: list[Path] = field(default_factory=list)
    merged: list[Path] = field(default_factory=list)
    skipped_no_staging: bool = False


def _walk_book_pages(staging_book_dir: Path) -> Iterable[tuple[Path, str]]:
    for type_dir in PAGE_TYPE_DIRS:
        d = staging_book_dir / type_dir
        if not d.is_dir():
            continue
        for md in sorted(d.glob("*.md")):
            yield md, type_dir


def _process_book(
    book_stem: str,
    today: str,
    *,
    dry_run: bool,
    virtual_written: set[Path] | None = None,
) -> BookCommitResult:
    """Process one book's staged pages.

    `virtual_written`: when supplied (dry-run mode), tracks paths that earlier
    books in this batch would have written, so collision detection accurately
    reflects what will happen in a real run from the same starting wiki state.
    """
    res = BookCommitResult(book_stem=book_stem)
    staging_dir = STAGING_ROOT / book_stem
    if not staging_dir.is_dir():
        res.skipped_no_staging = True
        return res

    for staged_md, type_dir in _walk_book_pages(staging_dir):
        dst = WIKI_ROOT / type_dir / staged_md.name
        new_text = staged_md.read_text(encoding="utf-8")
        already_present = dst.exists() or (
            virtual_written is not None and dst in virtual_written
        )
        if not already_present:
            if not dry_run:
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_text(new_text, encoding="utf-8")
            if virtual_written is not None:
                virtual_written.add(dst)
            res.created.append(dst)
            continue
        # MERGE path
        if not dry_run:
            existing = _parse_page(dst.read_text(encoding="utf-8"))
            new = _parse_page(new_text)
            merged = _merge_pages(existing, new, book_stem, today)
            dst.write_text(_render_page(merged), encoding="utf-8")
        res.merged.append(dst)
    return res


def _log_entry(book_stem: str, res: BookCommitResult, today: str, source_path: str | None) -> str:
    lines = [
        f"## [{today}] ingest | {book_stem}",
        f"- Trigger: S6 batch commit (Phase H of {Path(__file__).parent.name} pipeline).",
        f"- Sources: {source_path or 'raw/books/<see staging>'}",
    ]
    if res.created:
        lines.append("- Files created:")
        for p in res.created:
            lines.append(f"  - `{p.relative_to(REPO_ROOT)}`")
    if res.merged:
        lines.append("- Files merged (extended):")
        for p in res.merged:
            lines.append(f"  - `{p.relative_to(REPO_ROOT)}`")
    lines.append("- Files deprecated: None.")
    lines.append(
        f"- Notes: {len(res.created)} new + {len(res.merged)} merged. "
        f"Auto-generated from staged extraction; verify outliers in next lint pass."
    )
    return "\n".join(lines) + "\n"


def _append_log(entry: str) -> Path:
    log_path = WIKI_ROOT / "log.md"
    cur = log_path.read_text(encoding="utf-8").rstrip()
    log_path.write_text(cur + "\n\n" + entry, encoding="utf-8")
    return log_path


def _git_commit_book(book_stem: str, paths: list[Path]) -> None:
    args = ["git", "add"] + [str(p) for p in paths]
    subprocess.run(args, cwd=REPO_ROOT, check=True)
    subprocess.run(
        ["git", "commit", "-m", f"ingest: {book_stem}"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    )


# ---------- index rebuild --------------------------------------------------


SECTION_TITLES = {
    "entities": "Entities",
    "concepts": "Concepts",
    "topics": "Topics",
    "sources": "Sources",
    "analyses": "Analyses",
}

# Singular forms for the "Add one line per <X> page" comment in index.md.
SECTION_SINGULAR = {
    "entities": "entity",
    "concepts": "concept",
    "topics": "topic",
    "sources": "source",
    "analyses": "analysis",
}


def _summary_for(page: ParsedPage) -> str:
    body = page.sections.get("## Summary", "").strip()
    if not body:
        return ""
    # First sentence-ish; cap at 200 chars.
    first_para = body.split("\n\n")[0].strip()
    first_para = re.sub(r"\s+", " ", first_para)
    if len(first_para) > 200:
        first_para = first_para[:197].rstrip() + "..."
    return first_para


def _rebuild_index() -> str:
    sections: dict[str, list[str]] = {k: [] for k in SECTION_TITLES}
    for type_dir, title in SECTION_TITLES.items():
        d = WIKI_ROOT / type_dir
        if not d.is_dir():
            continue
        for md in sorted(d.glob("*.md")):
            try:
                page = _parse_page(md.read_text(encoding="utf-8"))
            except Exception:
                continue
            page_title = page.frontmatter.get("title") or md.stem
            summary = _summary_for(page)
            line = f"- [[{page_title}]] — {summary}" if summary else f"- [[{page_title}]]"
            sections[type_dir].append(line)

    out = [
        "# index.md",
        "",
        "This file is the master catalog of the wiki. Read this file first before routing a query or deciding which pages to edit.",
        "",
    ]
    for type_dir, title in SECTION_TITLES.items():
        out.append(f"## {title}")
        out.append("")
        out.append(f"<!-- Add one line per {SECTION_SINGULAR[type_dir]} page -->")
        if sections[type_dir]:
            out.extend(sections[type_dir])
        else:
            out.append("- _None yet._")
        out.append("")
    out.extend(
        [
            "## Dashboards",
            "",
            "- [[Wiki Health Dashboard]] — Operational overview, backlog, and maintenance status.",
            "",
            "## Conflicts",
            "",
            "<!-- Add one line per conflict page -->",
            "- _None yet._",
            "",
            "## Entry format",
            "",
            "Use one stable line per durable page:",
            "",
            "```text",
            "- [[Page Name]] — One-line summary.",
            "```",
            "",
            "## Maintenance rules",
            "",
            "1. Update this file after every ingest that creates, merges, deprecates, or renames a durable page.",
            "2. Remove stale references when pages are deprecated.",
            "3. Keep summaries short, factual, and stable.",
            "4. Do not list transient scratch notes here.",
            "",
        ]
    )
    return "\n".join(out)


# ---------- CLI ------------------------------------------------------------


def _load_ok_books() -> list[tuple[str, str | None]]:
    """Return (book_stem, source_path) for each ok book in progress order."""
    p = json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))
    out: list[tuple[str, str | None]] = []
    for b in p["books"]:
        if b.get("status") == "ok":
            stem = b.get("book_stem") or b.get("stem")
            out.append((stem, b.get("source_path")))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true", help="plan only, no writes/commits")
    ap.add_argument("--limit", type=int, default=None, help="process first N ok books")
    ap.add_argument("--start-from", type=str, default=None, help="resume from this book_stem")
    ap.add_argument("--no-tag", action="store_true", help="skip final git tag")
    ap.add_argument("--tag", type=str, default=None, help="override default tag name")
    args = ap.parse_args(argv)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    books = _load_ok_books()
    if args.start_from:
        for i, (b, _) in enumerate(books):
            if b == args.start_from:
                books = books[i:]
                break
        else:
            print(f"[commit_batch] start-from {args.start_from!r} not found", file=sys.stderr)
            return 2
    if args.limit is not None:
        books = books[: args.limit]

    print(
        f"[commit_batch] processing {len(books)} ok books "
        f"(dry_run={args.dry_run})",
        flush=True,
    )

    total_created = 0
    total_merged = 0
    skipped = 0
    virtual_written: set[Path] | None = set() if args.dry_run else None
    for i, (book_stem, source_path) in enumerate(books, start=1):
        res = _process_book(
            book_stem, today, dry_run=args.dry_run,
            virtual_written=virtual_written,
        )
        if res.skipped_no_staging:
            skipped += 1
            print(f"  [{i}/{len(books)}] {book_stem} — SKIP (no staging dir)", flush=True)
            continue
        total_created += len(res.created)
        total_merged += len(res.merged)
        print(
            f"  [{i}/{len(books)}] {book_stem} — "
            f"+{len(res.created)} new, ~{len(res.merged)} merged",
            flush=True,
        )
        if args.dry_run:
            continue

        log_path = _append_log(_log_entry(book_stem, res, today, source_path))
        touched = res.created + res.merged + [log_path]
        _git_commit_book(book_stem, touched)

    print(
        f"[commit_batch] done: +{total_created} new, ~{total_merged} merged across "
        f"{len(books) - skipped} books ({skipped} skipped)",
        flush=True,
    )

    if args.dry_run:
        return 0

    # Final: rebuild index + commit + tag.
    new_index = _rebuild_index()
    idx_path = WIKI_ROOT / "index.md"
    idx_path.write_text(new_index, encoding="utf-8")
    subprocess.run(["git", "add", str(idx_path)], cwd=REPO_ROOT, check=True)
    subprocess.run(
        ["git", "commit", "-m", "ingest: rebuild index after batch"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    )
    print("[commit_batch] index.md rebuilt + committed", flush=True)

    if not args.no_tag:
        tag = args.tag or f"ingest-batch-{datetime.now():%Y%m%d-%H%M}"
        subprocess.run(["git", "tag", tag], cwd=REPO_ROOT, check=True)
        print(f"[commit_batch] tagged {tag}", flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
