# LLM Wiki Project Pack

This package is a ready-to-use starter repository for a Karpathy-style LLM Wiki.

## Included

- `raw/` — immutable source materials.
- `wiki/` — compiled markdown knowledge layer.
- `schema/` — SOP, agent protocol, prompts, and templates.
- `workspace/` — pre-ingest collection and repair area.
- `reviews/` — review and audit logs.
- `scripts/` — reserved space for automation helpers.

## Recommended first run

1. Put `WIKI_SOP.md` and `AGENT_PROTOCOL.md` under `schema/` (already included here).
2. Put candidate materials into `workspace/intake/` or directly into `raw/inbox/` if already curated.
3. Use `schema/prompts/collect_select.md` for pre-ingest selection.
4. Use `schema/prompts/setup.md` to normalize the repo.
5. Use `schema/prompts/ingest.md` to compile the first source into the wiki.
6. Use `schema/prompts/lint.md` after the first ingest.
