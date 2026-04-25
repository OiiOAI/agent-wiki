# Publishing your fork — release checklist

This repo's `master` branch contains the original maintainer's
ingested wiki content (8,000+ pages from a private 196-book corpus).
If you want to publish a fork as a clean template — without the
maintainer's data — follow this checklist.

## Option A — clean release branch (recommended)

Use the included script. It creates an `release/clean` branch that
keeps the pipeline + schema + tests + docs but resets `wiki/` to a
minimal demo state, so users who fork your release see an empty
wiki and the original log/index.

```bash
bash scripts/release/init_clean_repo.sh
git push origin release/clean
```

The script:

1. Checks out a new `release/clean` branch from current HEAD.
2. Removes every page under `wiki/{entities,concepts,topics,sources,analyses,conflicts}/`.
3. Resets `wiki/index.md` and `wiki/log.md` to skeleton form.
4. Wipes `tmp/` and any cached intermediates.
5. Verifies `bash scripts/run_tests.sh` still passes (95 tests, no LLM).
6. Creates one commit: `release: clean state for public fork`.

You then push the branch and (optionally) make it the default in
your hosting provider.

## Option B — manual scrub

If you want full control:

```bash
git checkout -b release/clean
rm -rf wiki/entities/* wiki/concepts/* wiki/topics/* \
       wiki/sources/* wiki/analyses/* wiki/conflicts/*
git checkout HEAD~N -- wiki/index.md wiki/log.md     # before any ingest
rm -rf tmp/
git add -A && git commit -m "release: clean state for public fork"
```

## Pre-publish review

Before pushing publicly, audit:

- [ ] `.env` is **not** present (`.gitignore` covers it but verify)
- [ ] `raw/books/` is gitignored and empty (your books shouldn't ship)
- [ ] `wiki/` contains only schema-template-derived skeletons
- [ ] `tmp/` is gone
- [ ] `git log --all` doesn't expose `.env` history (run
  `git log -p --all | grep -i 'sk-ant\|ANTHROPIC_API_KEY=eyJ'`)
- [ ] Personal paths: `git grep -i "/Users/<your-name>"` returns nothing
- [ ] LICENSE matches your intent (current default: MIT)

## Don't publish if you have

- API keys, ever, in any commit
- Source PDFs/EPUBs that aren't yours to redistribute
- Internal notes / private analyses in `wiki/analyses/`
- IP-sensitive `wiki/conflicts/` pages
