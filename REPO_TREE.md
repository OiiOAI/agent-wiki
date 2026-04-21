# REPO_TREE.md

```text
project/
  raw/
    inbox/
    assets/
    archive/
  wiki/
    index.md
    log.md
    entities/
    concepts/
    topics/
    sources/
    analyses/
    dashboards/
    conflicts/
  schema/
    WIKI_SOP.md
    AGENT_PROTOCOL.md
    prompts/
      setup.md
      ingest.md
      query.md
      lint.md
```

## Notes

- `raw/inbox/` stores newly added source material waiting for ingest.
- `raw/assets/` stores local images, PDFs, or attachments referenced by raw notes.
- `raw/archive/` stores already-processed or retired raw material when you want operational separation.
- `wiki/index.md` is the first routing file the agent should read.
- `wiki/log.md` is the append-only audit trail.
- `wiki/entities/` stores named things.
- `wiki/concepts/` stores abstract ideas.
- `wiki/topics/` stores broader synthesized clusters.
- `wiki/sources/` stores source-summary pages.
- `wiki/analyses/` stores durable query outputs.
- `wiki/dashboards/` stores navigation pages and status overviews.
- `wiki/conflicts/` stores unresolved disagreements.
- `schema/` stores the stable operating rules and task prompts.
```
