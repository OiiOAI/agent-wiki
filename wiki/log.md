# log.md

This file is the append-only operational history of the wiki.

## [2026-04-10 14:36] setup | initial repository skeleton
- Trigger: Initial repository bootstrap.
- Sources: None.
- Files created:
  - `wiki/index.md`
  - `wiki/log.md`
  - directory skeleton under `raw/`, `wiki/`, and `schema/`
- Files modified: None.
- Files deprecated: None.
- Notes: Repository initialized with empty section structure and starter operational files.
- Outstanding issues:
  - `schema/WIKI_SOP.md` should be copied in if not already present.
  - `schema/AGENT_PROTOCOL.md` should be copied in if not already present.
  - task prompt files should be placed under `schema/prompts/`.

## Log entry template

```text
## [YYYY-MM-DD HH:MM] operation | short title
- Trigger:
- Sources:
- Files created:
- Files modified:
- Files deprecated:
- Notes:
- Outstanding issues:
```

## Rules

1. Append new entries; do not rewrite history except for obvious formatting fixes.
2. Record every ingest, major query-save, lint pass, merge, rename, rollback, or schema change.
3. Keep titles short and parseable.
4. If an operation is uncertain or partially failed, state that explicitly.
