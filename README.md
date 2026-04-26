# agent-wiki

A reproducible pipeline that turns a folder of PDFs / EPUBs into a
linked, provenance-anchored Markdown knowledge base — Karpathy's
*"LLM Wiki"* idea, fully automated.

> **Status**: Battle-tested on a 196-book corpus (165 ok, $104 spend,
> 8,249 wiki pages, 95 unit tests green). See
> [`docs/usecases/query-exercise-and-brain.md`](docs/usecases/query-exercise-and-brain.md)
> for an end-to-end query walkthrough using real output.

---

## What it does

```
your folder of books              wiki/
─────────────────────             ─────────────────────────────────
~/Library/                        wiki/
├─ neuroscience/                  ├─ entities/      (people, organs)
│  ├─ Spark.pdf          ──┐      ├─ concepts/      (BDNF, working memory)
│  └─ Behave.pdf           ├─►    ├─ topics/        (cross-cutting themes)
├─ philosophy/             │      ├─ sources/       (one per book)
│  └─ 道德经.epub          │      ├─ analyses/      (durable arguments)
└─ economics/              │      ├─ index.md       (master catalog)
   └─ Capitalism.pdf    ───┘      └─ log.md         (operational history)
```

Each wiki page carries:
- **YAML frontmatter** (id, title, tags, related-page links)
- **Provenance anchors** like `[raw/.../Spark.pdf#p43]` — every claim is
  clickable back to the source page
- **Explicit `Inference:` / `Uncertain:` markers** — agent never silently
  blends opinion into facts
- **Cross-page `[[wiki-links]]`** — the same concept appearing in 8
  books becomes one merged page with all 8 books' provenance

---

## Quick start (5 commands)

### Prerequisites

```bash
# macOS
brew install python@3.12 poppler pandoc          # required
brew install ocrmypdf tesseract-lang ghostscript  # optional, for scanned PDFs

# Ubuntu / Debian
sudo apt install python3.12 poppler-utils pandoc  # required
sudo apt install ocrmypdf tesseract-ocr-chi-sim ghostscript  # optional
```

Python 3.10+ required (developed on 3.12 / 3.14).

### Easiest path — interactive wizard

```bash
git clone https://github.com/<you>/agent-wiki && cd agent-wiki
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m scripts.ingest.setup           # ← does the rest, asks 6 questions
```

The wizard checks system deps, copies + opens `.env`, probes the LLM,
takes your books folder (offering to copy + beautify filenames + classify
into disciplines), runs the first book as a trial, and lands it into `wiki/`.
Press `Ctrl-C` anytime — progress persists to `tmp/setup_state.json` and
re-running resumes where you left off.

### Manual path

```bash
# 1. clone + install
git clone https://github.com/<you>/agent-wiki && cd agent-wiki
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. configure your LLM
cp .env.example .env
# edit .env — uncomment one of the four provider blocks (Claude /
# Minimax / OpenAI proxy / local), fill in the key

# 3. verify install (133 unit tests, no LLM needed)
bash scripts/run_tests.sh

# 4. preview your corpus (no LLM cost)
python -m scripts.ingest.auto_ingest --books-dir ~/Library/Books --dry-discover

# 5. process the first 3 books
python -m scripts.ingest.auto_ingest \
    --books-dir ~/Library/Books \
    --limit 3                          # try 3 first to gauge cost

# 5. inspect output, then commit
ls tmp/ingest_staging/                  # staged pages (no git impact yet)
cat tmp/ingest_report.md                # cost + per-book breakdown
python -m scripts.ingest.commit_batch   # land into wiki/ + per-book git commit
```

That's it. Each book becomes one git commit; rolling back a bad ingest
is one `git revert`.

---

## How `--books-dir` works

Point at any folder. Two layouts work:

```
# Flat — no categories
~/Library/
├─ Spark.pdf
├─ 道德经.epub
└─ Capitalism.pdf
# All books get discipline=`general` (override with --default-discipline)
```

```
# Nested — first subdirectory becomes the discipline tag
~/Library/
├─ neuroscience/Spark.pdf      # discipline=neuroscience
├─ philosophy/道德经.epub        # discipline=philosophy
└─ economics/Capitalism.pdf    # discipline=economics
```

Discipline only affects logging / reports — it doesn't change extraction
quality or wiki structure.

---

## LLM choice

`scripts/ingest/llm_client.py` talks to **any Anthropic-compatible
Messages API**. We've tested:

| Provider | Cost (per 196-book run) | Notes |
|---|---|---|
| Claude (Sonnet 4.5) | est. $400-600 | best quality, especially CJK |
| Minimax M2.7-highspeed | **$104 actual** | very cheap, strong Chinese, what we used |
| OpenAI gpt-4o (via LiteLLM proxy) | est. $300-500 | requires gateway shim |
| Local Qwen2.5-32B (vLLM) | $0 (your hardware) | quality varies; needs proxy |

Switch providers in `.env` — no code change. See
`.env.example` for ready-to-uncomment templates.

---

## Pipeline phases

```
A  pdf_to_md.py        PDF/EPUB → Markdown w/ page anchors
B  chunk.py            semantic chunking with chapter awareness
C  extract.py          chunk + LLM → typed PageCandidate (Pydantic)
D  compile.py          PageCandidate → templated wiki page
E  validate.py         11 SOP invariants per page
F  conflict_check.py   detect collisions vs existing wiki
G  report.py           per-batch dry-run summary
H  commit_batch.py     atomic per-book git commit + index rebuild
```

Phases A–G write only to `tmp/` (gitignored). Nothing touches `wiki/` or
`raw/` until **H**, the only step that needs explicit approval. That's
the rollback boundary — `git reset --hard <tag>^` returns to pre-ingest
state.

Detailed phase contracts live in
[`scripts/ingest/README.md`](scripts/ingest/README.md).

---

## Cost guardrails

`scripts/ingest/cost_tracker.py` enforces:

```bash
python -m scripts.ingest.auto_ingest --books-dir ~/Library \
    --budget 50 --per-book-cap 1.5
```

Breaches raise `BudgetExceeded`; the orchestrator records the failure
in `tmp/ingest_progress.json` and continues with the next book. Default
is uncapped (`math.inf`) — set explicit caps for production runs.

---

## Scanned PDFs

Scanned-image PDFs (no text layer) fail Phase A with `requires manual
OCR`. Two options:

```bash
# Option 1 — ocrmypdf rescue (recommended; ~10 min/book on Apple Silicon)
python -m scripts.ingest.ocr_rescue --timeout-min 30

# Option 2 — marker (PyTorch ML, multi-GB; opt-in via env)
ENABLE_MARKER_OCR=1 python -m scripts.ingest.auto_ingest ...
```

`ocr_rescue` writes OCR'd PDFs to `tmp/ocr_cache/`, then re-runs Phases
A-E with provenance pinned to the original `raw/` path so wiki anchors
still point users at the source file.

---

## Schema and protocol

Two files define the contract:

- [`schema/WIKI_SOP.md`](schema/WIKI_SOP.md) — page types, frontmatter
  fields, provenance format, the 11 invariants
- [`schema/AGENT_PROTOCOL.md`](schema/AGENT_PROTOCOL.md) — agent's role,
  query-mode, response structure, non-negotiable rules

`scripts/ingest/validate.py` mechanically enforces every invariant; new
checks should be added there + tested in `scripts/tests/test_validate.py`.

---

## Lint your wiki

```bash
.venv/bin/python -m scripts.lint.wiki_lint              # 11 invariants × N pages
.venv/bin/python -m scripts.lint.wiki_conflict_scan     # find residual same-title / alias-collision
```

Both are read-only. Reports land in `tmp/lint_report.md` and
`tmp/conflict_report.md`.

---

## Using with Claude Code

This repo is built to be maintained by an LLM agent. With Claude Code:

1. Settings hook (`scripts/hooks/block_raw_edits.py`) prevents `Write`/
   `Edit` against `raw/` — the agent must `cp` to add new sources.
2. [`CLAUDE.md`](CLAUDE.md) and [`schema/prompts/`](schema/prompts/)
   route the agent into the correct mode (ingest / lint / query / setup)
   based on user intent.

You don't need Claude Code to run the pipeline — every phase is a
plain CLI. See [`USAGE.md`](USAGE.md) for the non-agent path.

---

## Layout

```
agent-wiki/
├─ raw/              # immutable source materials (gitignored: raw/books/)
├─ wiki/             # generated knowledge base (commit per book)
├─ schema/           # SOP, protocol, prompts, page templates
├─ scripts/
│  ├─ ingest/        # pipeline phases A-H (Python)
│  ├─ lint/          # wiki-wide lint + conflict scan
│  ├─ hooks/         # Claude Code PreToolUse hook (raw/ guard)
│  └─ tests/         # 95 unit tests, all mock the LLM
├─ tmp/              # all intermediates (gitignored)
├─ docs/usecases/    # worked examples
└─ requirements.txt
```

---

## License

MIT — see [`LICENSE`](LICENSE).

> **Source material disclaimer**: the MIT license covers the pipeline
> code only. Users are solely responsible for the copyright/licensing
> status of materials they place under `raw/`. The pipeline produces
> derivative works (summaries, extracted facts) subject to fair-use
> and contractual limits of the underlying sources.
