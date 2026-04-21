# WIKI_SOP.md

## Purpose

This document defines the operating rules for a persistent LLM-maintained wiki built on three layers:
1. `raw/` — immutable source materials.
2. `wiki/` — LLM-written markdown knowledge base.
3. `schema/` — operating rules, prompts, and protocol files.

The system is designed so the wiki becomes a persistent, compounding artifact rather than a query-time reconstruction of raw documents.

## Core principles

1. Raw sources are the source of truth.
2. The wiki is derivative, editable, and always revisable.
3. The agent must behave as a disciplined maintainer, not a generic chatbot.
4. Good answers, once produced, may become durable wiki pages.
5. Every important operation must leave an auditable trail.
6. Rules live in text files, not hidden model memory.
7. The system should remain model-agnostic and portable across agents.

## Directory contract

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
```

### Ownership rules

- `raw/` is read-only for the agent.
- `wiki/` is writable by the agent, subject to this SOP.
- `schema/` is writable only when the user explicitly requests rule changes.

## File conventions

### Markdown

- All durable knowledge files must be plain Markdown.
- Internal links must use Obsidian-compatible wikilinks: `[[Page Name]]`.
- Headings must be stable and descriptive.
- Avoid decorative formatting that harms portability.

### Frontmatter

All wiki pages should begin with YAML frontmatter when practical.

```yaml
---
id: wiki-unique-id
title: Page Title
type: entity|concept|topic|source|analysis|conflict|dashboard
status: draft|active|deprecated|conflicted
created: 2026-04-10
updated: 2026-04-10
sources:
  - raw/path/to/source.md#L10-L42
tags:
  - example
---
```

Required fields for durable pages:
- `title`
- `type`
- `status`
- `created`
- `updated`
- `sources` (may be empty only for structural pages like `index.md`)

## Source and citation policy

1. Raw files are authoritative inputs; wiki pages are compiled interpretations.
2. Every factual claim added to the wiki must be traceable to one or more raw sources.
3. Traceability should be recorded at the smallest practical unit, preferably sentence or bullet level for high-risk material.
4. If exact line anchors are unavailable, cite the nearest stable section or file path.
5. If a claim is inferred rather than directly stated, mark it as `Inference:` and cite the supporting sources.
6. If a claim is uncertain, mark it as `Uncertain:` and do not silently normalize it into fact.
7. If sources conflict, do not collapse them into a single claim unless the user explicitly approves the resolution.

Recommended inline provenance format:

```text
The system updates entity pages incrementally. [raw/sources/karpathy-llm-wiki.md#Architecture]
```

## Naming rules

- One canonical page per concept unless separation is intentional.
- Prefer singular, stable titles: `Transformer`, not `Transformers Overview Notes`.
- Use explicit disambiguation when needed: `Claude (Model)` vs `Claude Code (Tool)`.
- Do not rename high-traffic pages without updating backlinks, `index.md`, and `log.md`.

## Page types

### Entity pages
For named things: people, products, companies, models, tools, books.

### Concept pages
For abstract ideas: retrieval, alignment, fine-tuning, knowledge compilation.

### Topic pages
For broader synthesized areas containing multiple concepts or entities.

### Source pages
For summaries of specific raw inputs.

### Analysis pages
For durable answers generated during queries.

### Conflict pages
For unresolved disagreements between sources or revisions.

### Dashboard pages
For navigational or operational overviews.

## Required special files

### `wiki/index.md`

Purpose:
- Master catalog of the wiki.
- First file the agent should read before routing a query.

Rules:
- Organize by page type.
- Each entry must include page link and a one-line summary.
- Update on every ingest that changes the wiki.
- Remove stale entries when pages are merged, renamed, or deprecated.

Suggested entry format:

```text
- [[Transformer]] — Neural network architecture centered on self-attention.
```

### `wiki/log.md`

Purpose:
- Append-only operational history.

Rules:
- Never rewrite past entries except to correct formatting errors.
- Every ingest, major query-save, lint pass, merge, rename, or rollback gets a log entry.
- Use a stable parseable prefix.

Required heading format:

```text
## [2026-04-10 14:00] ingest | Source Title
```

Log body should record:
- trigger
- files created
- files modified
- files deprecated
- important unresolved issues

## Operation modes

### 1. Setup

Goal:
Create or normalize the project skeleton.

Rules:
- Do not invent domain content during setup.
- Create only structure, rule files, and minimal placeholders.
- If files already exist, inspect before modifying.
- Preserve user-authored material.

Expected outputs:
- directory structure
- `wiki/index.md`
- `wiki/log.md`
- `schema/WIKI_SOP.md`
- `schema/AGENT_PROTOCOL.md`

### 2. Ingest

Goal:
Compile a new raw source into the wiki.

Required sequence:
1. Identify newly added or changed raw files.
2. Read the source fully before editing any wiki page.
3. Extract key facts, concepts, entities, claims, and conflicts.
4. Decide whether to create new pages or update existing ones.
5. Update relevant wiki pages.
6. Update `wiki/index.md`.
7. Append to `wiki/log.md`.

Hard constraints:
- Never modify the raw source.
- Do not perform unrelated cleanup during ingest.
- Do not overwrite a strong existing claim with a weaker new source without flagging the downgrade.
- For high-impact edits touching more than 10 files, produce a proposal first unless the user has enabled autonomous bulk ingest.

### 3. Query

Goal:
Answer a user question against the wiki.

Required sequence:
1. Read `wiki/index.md` first.
2. Retrieve the most relevant pages.
3. Synthesize an answer with explicit provenance.
4. Decide whether the answer has durable value.
5. If yes, save it as an analysis page and update `index.md` and `log.md`.

Durable-save criteria:
Save the answer back into the wiki when at least one condition holds:
- the answer synthesizes multiple pages,
- the answer resolves a recurring question,
- the answer creates a useful comparison or framework,
- the answer exposes a novel connection worth preserving.

### 4. Lint

Goal:
Health-check the wiki and improve structural integrity.

Check for:
- contradictions between pages,
- stale claims superseded by newer sources,
- orphan pages with no inbound links,
- important concepts lacking their own page,
- missing cross-references,
- dangling links,
- missing provenance,
- duplicate or near-duplicate pages,
- index drift,
- frontmatter inconsistencies.

Repair policy:
- Auto-fix only low-risk structural issues.
- For semantic merges, deletions, or conflict resolution, produce a proposal first.
- Preserve disagreement when truth cannot be determined from existing sources.

## Review gates

The agent must stop and request approval before:
- deleting a page,
- merging two non-trivial pages,
- renaming a canonical page,
- modifying `schema/` files,
- touching more than 10 wiki files in one operation,
- replacing a previously sourced claim with an unsourced one,
- resolving a source conflict by choosing one side.

## Rollback and recovery

1. The wiki should be stored in git.
2. Every significant operation should correspond to a commit or at minimum a log entry.
3. If a bad edit is detected, prefer revert or targeted restoration over manual patching.
4. If confidence in the current state is low, create a conflict or repair page before broad edits.

## Model-agnosticity rules

To remain portable across Agent A and Agent B:
- Do not rely on hidden memory.
- Do not rely on proprietary database state.
- Do not require a vendor-specific tool API in core logic.
- Express workflows in plain language and file operations.
- Keep the durable state in markdown, frontmatter, index, and log.

## Search and scale

- At small scale, `wiki/index.md` is the primary router.
- As the wiki grows, external local search tools may be added.
- Any such tool is optional and must not become the only source of durable state.
- Search acceleration must complement, not replace, the wiki files.

## Human role

The human is responsible for:
- curating sources,
- deciding what matters,
- setting analytical priorities,
- reviewing high-risk edits,
- evolving the schema when workflow assumptions change.

## Change management

When changing this SOP:
1. record the reason,
2. note the scope,
3. update dependent protocol or prompt files,
4. append an entry to `wiki/log.md` or a schema changelog.

## Default failure behavior

If the agent cannot determine the correct action:
1. do not guess,
2. do not silently rewrite ambiguous content,
3. output a short uncertainty report,
4. propose the smallest safe next step.
