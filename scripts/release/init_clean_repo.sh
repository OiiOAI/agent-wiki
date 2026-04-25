#!/usr/bin/env bash
# Create a release/clean branch with the wiki reset to a minimal demo state.
#
# Idempotent within reason — running twice just deletes the branch and
# recreates it from the current HEAD. Refuses to run if there are
# uncommitted changes (use `git stash` first).
#
# Usage:
#   bash scripts/release/init_clean_repo.sh [branch-name]
#
# After:
#   git push origin <branch-name>
#   # optional: set as default branch on your host

set -euo pipefail

BRANCH="${1:-release/clean}"
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

# 1. Safety: clean working tree only.
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "ERROR: uncommitted changes. Stash or commit before running." >&2
    git status --short
    exit 1
fi

# 2. Drop and recreate branch.
if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
    git branch -D "$BRANCH"
fi
git checkout -b "$BRANCH"

# 3. Reset wiki page directories.
for sub in entities concepts topics sources analyses conflicts; do
    if [ -d "wiki/$sub" ]; then
        find "wiki/$sub" -type f -name "*.md" -delete
    fi
done

# 4. Reset index.md and log.md to skeletons.
cat > wiki/index.md <<'EOF'
# index.md

This file is the master catalog of the wiki. Read this file first before routing a query or deciding which pages to edit.

## Entities

<!-- Add one line per entity page -->
- _None yet._

## Concepts

<!-- Add one line per concept page -->
- _None yet._

## Topics

<!-- Add one line per topic page -->
- _None yet._

## Sources

<!-- Add one line per source page -->
- _None yet._

## Analyses

<!-- Add one line per analysis page -->
- _None yet._

## Dashboards

- [[Wiki Health Dashboard]] — Operational overview, backlog, and maintenance status.

## Conflicts

<!-- Add one line per conflict page -->
- _None yet._

## Entry format

Use one stable line per durable page:

```text
- [[Page Name]] — One-line summary.
```

## Maintenance rules

1. Update this file after every ingest that creates, merges, deprecates, or renames a durable page.
2. Remove stale references when pages are deprecated.
3. Keep summaries short, factual, and stable.
4. Do not list transient scratch notes here.
EOF

cat > wiki/log.md <<'EOF'
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
EOF

# 5. Wipe tmp/ — no intermediates ship publicly.
rm -rf tmp/
mkdir -p tmp/
touch tmp/.gitkeep

# 6. Verify tests still pass.
echo
echo "==> Verifying 95-test suite still passes on clean state..."
if [ -x ".venv/bin/python" ]; then
    PY=".venv/bin/python"
else
    PY="python3"
fi
"$PY" -m pytest scripts/tests/ -q --no-header

# 7. Commit.
git add -A
git commit -m "release: clean state for public fork

- wiki/{entities,concepts,topics,sources,analyses,conflicts}/ emptied
- wiki/index.md and log.md reset to skeleton
- tmp/ purged
- pipeline, schema, prompts, templates, and 95-test suite preserved

Run init_clean_repo.sh whenever you want to refresh this branch from
the current master.
"

echo
echo "==> Branch $BRANCH ready. Push with:"
echo "    git push origin $BRANCH"
