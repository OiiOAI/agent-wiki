# scripts/ingest — agent-wiki auto-ingest pipeline

Eight phases A→H, each a module you can run standalone. See
`~/.claude/plans/partitioned-bouncing-piglet.md` for the full design; this
README is an operator crib sheet.

## Quick verification

```
pip install -r requirements.txt
bash scripts/run_tests.sh            # L1-L3 unit tests (no LLM, must pass first)
```

## Phase map

| Phase | Module              | Input → Output                                     |
|------:|---------------------|----------------------------------------------------|
| A     | `pdf_to_md.py`      | `raw/books/*.pdf|.epub` → `tmp/md_cache/<stem>.md` |
| B     | `chunk.py`          | md → `List[Chunk]` with page/line anchors          |
| C     | `extract.py`        | Chunk + LLM → `List[PageCandidate]`                |
| D     | `compile.py`        | PageCandidate → `tmp/ingest_staging/<book>/*.md`   |
| E     | `validate.py`       | staged page → `List[ValidationError]`              |
| F     | `conflict_check.py` | staged ⊕ existing wiki → `List[CollisionReport]`   |
| G     | `report.py`         | staging + costs → `tmp/ingest_report.md` (+ sha)   |
| H     | `commit.py`         | staging → `wiki/` + git per-book commit + tag      |

Phases A–G write only under `tmp/` (gitignored); nothing touches `wiki/` or
`raw/` until Phase H. That is the rollback boundary.

## Budget

`cost_tracker.py` enforces:
  * per-book cap $2 (default)
  * batch cap $500 (default)

Breaches raise `BudgetExceeded`; the orchestrator records the failure and
continues with the next book (per user policy decided 2026-04-22).

## Credentials

`llm_client.py` reads `agent-wiki/.env`:
```
ANTHROPIC_API_KEY=...
ANTHROPIC_BASE_URL=https://api.minimaxi.com/anthropic
LLM_MODEL=MiniMax-M2.7-highspeed
```
`.env` is in `.gitignore`. Never commit.

## CLI

```
python -m scripts.ingest.auto_ingest --book raw/books/strategy/Foo.pdf --dry-run
python -m scripts.ingest.auto_ingest --all --dry-run --budget 500
python -m scripts.ingest.auto_ingest --commit --report tmp/ingest_report.md --approved-sha <sha>
```

## Test regime (gates)

L1-L3 (unit, no LLM) → L4 (tiny synthesized PDF) → L5 (Karpathy regression) →
L6 (5 diverse books smoke) → L7 (full 196-book dry-run).

No phase H runs until the L7 report is explicitly approved with
`--approved-sha <report-sha256>`.
