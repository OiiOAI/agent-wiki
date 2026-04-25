# USAGE — running agent-wiki without Claude Code

Every phase of the pipeline is a plain Python CLI. You do not need
Claude Code, the Anthropic SDK app, or any agent framework — only an
LLM API endpoint and the system dependencies in
[`README.md#prerequisites`](README.md#prerequisites).

This file is the recipe book. For background and design, see
[`README.md`](README.md) and [`scripts/ingest/README.md`](scripts/ingest/README.md).

---

## 1. End-to-end (single command)

```bash
python -m scripts.ingest.auto_ingest \
    --books-dir ~/Library/Books        # any folder of PDFs/EPUBs
    [--limit 5]                        # try 5 first
    [--disc neuroscience]              # filter by subdir name
    [--budget 50]                      # batch $ cap
    [--per-book-cap 2]                 # per-book $ cap
```

Writes:
- `tmp/md_cache/<stem>.md` — converted markdown (cached, reuse on rerun)
- `tmp/ingest_staging/<stem>/` — staged wiki pages (no git impact)
- `tmp/ingest_progress.json` — per-book status + cost
- `tmp/ingest_report.md` — human-readable summary
- `tmp/ingest_log/<stem>.log` — per-book trace

Then:

```bash
python -m scripts.ingest.commit_batch [--dry-run] [--limit N]
```

Walks staging in progress.json order, copies non-colliding pages,
**merges** colliding ones (same `id` from a different book → union of
sources/facts/related-links), creates one `git commit` per book, and
tags the batch.

---

## 2. Phase-by-phase (when you need granularity)

### Phase A — PDF/EPUB → Markdown

```python
from scripts.ingest import pdf_to_md
meta = pdf_to_md.convert_to_markdown(
    Path("~/Library/Spark.pdf").expanduser(),
    cache_dir=Path("tmp/md_cache"),
)
print(meta.cache_path, meta.pages_total, meta.language)
```

Tries `pdftotext -layout` first (fast, tiny RAM); marker (PyTorch OCR)
opt-in via `ENABLE_MARKER_OCR=1`; pandoc for EPUB.

### Phase B — Semantic chunking

```python
from scripts.ingest import chunk
text = Path(meta.cache_path).read_text()
chunks = chunk.semantic_chunking(text)   # ~6000 word chunks, chapter-aware
```

### Phase C — Extract structured candidates

```python
from scripts.ingest.extract import extract_book
from scripts.ingest.cost_tracker import CostTracker
cost = CostTracker(per_book_cap=2.0, batch_cap=100.0)
extraction = extract_book(
    book_stem="spark",
    source_path="raw/books/health/Spark.pdf",
    discipline="health",
    language="en",
    chunks=chunks,
    cost=cost,
    pages_total=meta.pages_total,
)
print(f"{len(extraction.candidates)} pages")
```

Parallel by default (`INGEST_PARALLEL_CHUNKS=4`).

### Phase D — Compile to staged markdown

```python
from scripts.ingest import compile as compile_mod
written = compile_mod.write_staging(
    book_stem="spark",
    candidates=extraction.candidates,
    source_provenance=f"[{source_path}#p1-{meta.pages_total}]",
    staging_root=Path("tmp/ingest_staging/spark"),
)
```

### Phase E — Validate (11 SOP invariants)

```python
from scripts.ingest.validate import validate_page
errs = validate_page(
    md_text=Path(written[0]).read_text(),
    existing_ids=set(),
    source_text=text,
    page_path=str(written[0]),
)
```

### Phase H — Commit

```python
from scripts.ingest.commit_batch import _process_book
_process_book(book_stem="spark", today="2026-04-25", dry_run=False)
```

---

## 3. OCR rescue for scanned PDFs

```bash
python -m scripts.ingest.ocr_rescue \
    [--limit N] \
    [--start-from <book_stem>] \
    [--timeout-min 30] \
    [--ocr-only]      # write OCR'd PDFs but don't reingest
    [--ingest-only]   # reingest from existing OCR cache
```

Reads `tmp/ingest_progress.json` for `status=="failed"` books, OCRs to
`tmp/ocr_cache/<stem>.pdf` (using `ocrmypdf -l chi_sim+chi_tra+eng`),
then reruns Phases A–E. Provenance is **pinned to the original `raw/`
path** so wiki anchors still point users at the source file (not the
OCR cache).

---

## 4. Lint and conflict scan

Run periodically to catch regressions:

```bash
python -m scripts.lint.wiki_lint                # 11 invariants × every page
python -m scripts.lint.wiki_conflict_scan       # residual collisions after merge
```

Both are **read-only**. Output to `tmp/lint_report.md` and
`tmp/conflict_report.md`.

---

## 5. Resuming an interrupted run

The orchestrator persists `tmp/ingest_progress.json` after every book.
Re-running with the same `--books-dir` skips books with `status=="ok"`
and continues from the next pending entry. Send `SIGINT` (Ctrl-C) at
any time — it saves before exit.

To force a redo of a single book:

```bash
python -m scripts.ingest.rerun_book <book_stem>
```

(Reuses Phase A cache, clears that book's staging, re-runs B–E.)

---

## 6. Inspecting cost / model usage

```bash
.venv/bin/python -c "
import json
p = json.load(open('tmp/ingest_progress.json'))
total_in = sum(b.get('tokens_in',0) for b in p['books'])
total_out = sum(b.get('tokens_out',0) for b in p['books'])
print(f'tokens in:  {total_in:,}')
print(f'tokens out: {total_out:,}')
print(f'cost:       \${p[\"total_cost_dollars\"]:.2f}')
"
```

---

## 7. Clearing state for a fresh run

```bash
rm -rf tmp/                             # all intermediates
git reset --hard <ingest-batch-tag>^    # roll back wiki/ commits (safe — tagged)
```

---

## 8. Programmatic embedding

The pipeline has no global state. You can import any phase and run it
inside a Jupyter notebook, a web service, or another orchestrator:

```python
import asyncio
from scripts.ingest.auto_ingest import discover_books, _process_one
from scripts.ingest.cost_tracker import CostTracker
from pathlib import Path

books = discover_books(
    repo_root=Path("/path/to/agent-wiki"),
    books_dir=Path("/my/books"),
    default_discipline="general",
)
cost = CostTracker(per_book_cap=2.0, batch_cap=50.0)
for stem, src_rel in books:
    res = _process_one(
        stem=stem,
        source_rel=src_rel,
        cost=cost,
        staging_root=Path("/tmp/staging"),
        md_cache_dir=Path("/tmp/md"),
        log_path=Path(f"/tmp/{stem}.log"),
    )
    print(stem, res.status, res.staging_files, f"${res.cost_dollars:.2f}")
```

---

## 9. Where things live

| What | Path |
|---|---|
| Pipeline code | `scripts/ingest/` |
| Lint code | `scripts/lint/` |
| Tests (no LLM) | `scripts/tests/` — `bash scripts/run_tests.sh` |
| SOP / agent rules | `schema/WIKI_SOP.md`, `schema/AGENT_PROTOCOL.md` |
| Page templates | `schema/templates/` |
| Sample wiki output | `wiki/` (after first ingest) |
| All intermediates | `tmp/` (gitignored) |
| Per-book commit history | `git log` after Phase H |
