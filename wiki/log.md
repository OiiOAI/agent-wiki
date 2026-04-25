# log.md

This file is the append-only operational history of the wiki.

## [release] clean state

- Trigger: Public release initialization — wiki content reset.
- Sources: None.
- Files created: None (skeleton only).
- Files modified: `wiki/index.md`, `wiki/log.md`.
- Files deprecated: None.
- Notes: Pipeline, schema, and tests preserved; ingest content cleared
  so a fresh user starts with an empty knowledge base. Run
  `python -m scripts.ingest.auto_ingest --books-dir <your-folder>`
  to begin populating.
