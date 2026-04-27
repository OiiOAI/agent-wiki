# AGENTS.md — handoff for downstream agents

You are an agent reading an **agent-wiki**: a Karpathy-style LLM Wiki
implementation. Thousands of small, interlinked Markdown pages, each
carrying YAML frontmatter and provenance anchors that point back to
the source PDFs/EPUBs in `raw/`. This file is the only one you need
to read to start answering queries — there is no required prior
knowledge of the project's pipeline, schemas, or scripts.

If you can run Python, also see [`scripts/query/wiki_query.py`](../scripts/query/wiki_query.py)
for a 0-LLM helper API. Otherwise, plain `cat` / `grep` / `rg` is
enough.

---

## What's in this wiki

```
wiki/
├─ index.md            ← human-readable master catalog (every page in one list)
├─ AGENTS.md           ← THIS FILE
├─ AGENTS_INDEX.json   ← machine-readable index (slug → path/title/summary/tags)
├─ log.md              ← append-only operational history
├─ entities/           ← people, organizations, named things, specific drugs/regions
├─ concepts/           ← named concepts (BDNF, working memory, OODA loop, etc.)
├─ topics/             ← cross-cutting themes that span concepts
├─ sources/            ← one page per ingested book/article (front-matter source)
├─ analyses/           ← durable arguments / synthesis pages (rare; opinionated)
├─ conflicts/          ← pages tracking contradictions across sources
└─ dashboards/         ← operator overviews (you can usually ignore these)
```

**Page count by type**: see `wiki/AGENTS_INDEX.json#page_count` (regenerated
on every batch commit).

---

## Frontmatter at a glance

Every page has YAML frontmatter at the top, between `---` delimiters:

```yaml
---
id: bdnf
title: BDNF
type: concept
status: draft                 # draft | active | deprecated | conflicted
created: '2026-04-23'
updated: '2026-04-25'
sources:                      # one or more provenance anchors
  - '[raw/books/health/Spark.pdf#p1-228]'
  - '[raw/books/neuroscience/Genius Foods - Max Lugavere.pdf#p1-562]'
confidence: high              # low | medium | high
tags: [neuroscience, neurotrophin, exercise, learning]
aliases: [brain-derived-neurotrophic-factor]
related:
  broader: [neurotrophin]
  narrower: [tropomyosin-receptor-kinase-b]
  adjacent: [bdnf-val66met, hippocampus]
  concepts: [neuroplasticity, neurogenesis]
---
```

Fields that always exist: `id`, `title`, `type`, `status`, `created`,
`updated`, `sources`, `tags`, `related`. Type-specific fields:
- `entity`: also has `aliases`, `canonical`, `confidence`
- `concept` / `topic`: `confidence`
- `source`: `source_kind` (book/paper/article/...), `source_path`,
  `source_author`, `source_date`, `reliability`
- `analysis`: `question`
- `conflict`: `conflict_scope`, `affected_pages`

---

## Page body structure

Below the frontmatter, every page follows this skeleton:

```markdown
# Title

## Summary
One-paragraph plain-prose overview. Self-contained.

## Key facts
- Each bullet is one atomic claim, ending with a provenance anchor:
  [raw/books/<discipline>/<book>.pdf#p<N>]
- Multiple anchors are independent; the same fact can cite several.

## Inferences        (optional)
- Inference: explicit synthesis the original source didn't make
  directly, prefixed with `Inference:`. Use sparingly.

## Uncertainties     (optional)
- Uncertain: things the page doesn't know or where sources disagree,
  prefixed with `Uncertain:`.

## Related pages     (optional)
- Broader: [[parent-concept]]
- Narrower: [[sub-concept]]
- Adjacent: [[sibling-concept]]
- Concepts: [[some-other-page]]
- Entities: [[some-person]]

## Provenance        (optional, source pages)
- Primary source: [raw/.../book.pdf#p1-300]
- Additional source: [raw/.../other.pdf#p1-150]

## Change notes      (rare)
- 2026-04-25 — merged contributions from `book-stem`.
```

---

## Citation conventions you MUST follow

When you write an answer that draws from this wiki:

1. **Every factual claim cites at least one provenance anchor** in the
   form `[raw/<path>#p<N>]` (page) or `[raw/<path>#L<n>-<m>]` (line).
   Multiple sources for the same claim → list them all separated by `;`.
2. **Synthesis is marked**. If you combine two facts to derive a third,
   prefix the derived claim with `Inference:`. Never silently blend.
3. **Unknowns are marked**. If the wiki doesn't say, prefix the
   statement with `Uncertain:` and offer what you'd need to look up to
   resolve it. Don't guess silently.
4. **External / pre-trained knowledge is marked**. If you use anything
   that's NOT in the wiki, prefix with `Guess:` and explain it's not
   sourced.
5. **Wikilinks** like `[[BDNF]]` resolve to a page title or alias. If
   the target doesn't exist (dangling link), say so — these are the
   wiki's own outstanding refs, by design.

---

## 5-step query workflow

Given a user question:

### Step 1 — Probe the index
```bash
grep -i "<keyword>" wiki/index.md
# or, if you can run Python:
.venv/bin/python -c "from scripts.query.wiki_query import search; \
    [print(h.slug, h.score) for h in search('<keyword>', limit=5)]"
```
Find candidate page slugs.

### Step 2 — Read the candidate page(s)
```bash
cat wiki/concepts/<slug>.md
```
Look at `## Summary` first (paragraph overview), then `## Key facts`
for atomic claims with provenance.

### Step 3 — Expand laterally
Follow `[[wikilinks]]` in `## Related pages` and inside the body.
1-hop neighbors usually answer "what's related"; 2-hop is rarely
needed unless the user asked for a synthesis.

### Step 4 — Verify against raw (when stakes are high)
For numeric / quoted / contested claims, open the raw source:
```bash
# The provenance anchor [raw/.../Spark.pdf#p43] tells you exactly which
# page. Use pdftotext / your reader to confirm the wiki claim.
pdftotext -l 43 -f 43 raw/books/health/Spark.pdf -
```

### Step 5 — Compose the answer using the response template (below)

---

## Response template

Always structure substantive answers like this. Adapt headers if a
section is empty (don't force).

```markdown
## Facts (with sources)
- <claim>. [raw/<path>#p<N>]
- <claim>. [raw/<path>#p<N>; raw/<other>#p<M>]

## Judgment / synthesis
- Inference: <derived claim>. Built from [raw/A#p1] + [raw/B#p2].

## Uncertain
- Uncertain: <thing the wiki doesn't say>. To resolve: <what you'd
  look up>.

## Guess (outside the wiki)
- Guess: <pre-trained knowledge>, NOT in this wiki. <caveat>.

## Suggested next pages
- [[related-concept-1]] — for <reason>
- [[related-entity]] — for <reason>
```

---

## Worked example

**User question**: "锻炼对大脑有什么具体的影响？BDNF 是什么？跟海马体的关系？"

**Step 1**:
```bash
$ grep -i "BDNF\|hippocampus\|exercise" wiki/index.md | head -5
- [[BDNF]] — Brain-derived neurotrophic factor is a protein...
- [[Hippocampus]] — A subcortical structure critical for...
- [[Spark The Revolutionary New Science of Exercise]] — ...
- [[Neurogenesis]] — The creation of new neurons...
```

**Step 2**: read `wiki/concepts/bdnf.md`. Summary says: "BDNF is a
neurotrophin that supports survival of existing neurons and stimulates
growth of new ones; concentrated in the hippocampus and cortex."
Key facts include:
- "Exercise raises BDNF levels in the hippocampus by ~3x in mice
  models. [raw/books/health/Spark.pdf#p43]"

**Step 3**: follow `[[hippocampus]]`, `[[neurogenesis]]`,
`[[exercise-bdnf]]`. Each adds detail.

**Step 4**: confirm the 3× claim in `Spark.pdf` page 43 if user asked
for the exact number.

**Step 5**: write the answer:

```markdown
## Facts
- BDNF (Brain-derived neurotrophic factor) is a protein that supports
  neuron survival and stimulates new neuron growth, concentrated in
  the hippocampus. [raw/books/health/Spark.pdf#p41]
- Aerobic exercise increases BDNF levels in the hippocampus
  approximately 3× in rodent models. [raw/books/health/Spark.pdf#p43]
- BDNF action in the hippocampus drives the formation of new
  neurons, a process called neurogenesis. [raw/books/health/Genius Foods - Max Lugavere.pdf#p26]

## Judgment
- Inference: Exercise → BDNF → hippocampal neurogenesis is the
  proximate mechanism the wiki names for "exercise improves
  learning." Built from the BDNF page + the neurogenesis page.

## Uncertain
- Uncertain: the exact human dose-response (intensity × duration)
  isn't quantified in the cited pages. To resolve: cross-check
  Ratey's primary citations in chapter 2 of `Spark.pdf`.
```

---

## What NOT to do

- **Don't modify `raw/`**. The hook `scripts/hooks/block_raw_edits.py`
  enforces this; assume any edit there is a bug.
- **Don't merge / delete / rename wiki pages without approval.**
  These are high-risk in the project's SOP. Propose, don't act.
- **Don't import knowledge from outside the wiki without marking it
  `Guess:`**. The wiki's value is its grounded provenance; mixing
  ungrounded claims poisons that.
- **Don't fabricate provenance.** If you can't find a source for a
  claim, say `Uncertain:` rather than inventing an anchor.
- **Don't trust dangling `[[wikilinks]]` as facts.** They're the
  wiki's own outstanding refs — placeholders for future ingest.

---

## Bonus: programmatic access

If your environment can run Python in this repo's venv:

```python
from scripts.query.wiki_query import find_page, read_page, search, neighbors

# Find a page by title, slug, or alias
p = find_page("BDNF")
print(p.summary)              # one-paragraph overview
for f in p.key_facts:
    print(f.claim, "→", f.provenance)

# Substring search across title + summary + key_facts
for hit in search("hippocampus exercise", limit=5):
    print(hit.slug, hit.score, hit.snippet)

# Walk the related-pages graph
for n in neighbors("bdnf", depth=1):
    print(n.slug, n.title)
```

Zero external API calls. Pure filesystem + frontmatter parsing.

---

## File-system shortcuts

- All page paths are relative to repo root.
- `wiki/AGENTS_INDEX.json` is the fastest lookup. Schema:
  ```json
  {"pages": [{"slug","title","type","path","summary","tags","aliases",
              "related_count","fact_count","source_count"}, ...],
   "by_slug": {slug → index},
   "by_alias": {alias → slug},
   "by_tag": {tag → [slug, ...]},
   "page_count": int}
  ```
- It's regenerated on every batch commit; safe to rely on for the
  current snapshot.

If you got here without prior context, you're done. Start at Step 1
of the workflow above.
