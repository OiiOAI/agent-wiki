# BOOTSTRAP_RUNBOOK.md

## Purpose

This pack contains three copy-paste startup prompts for the first operational cycle of the repository:
1. initial setup check,
2. first ingest,
3. first lint.

## Recommended order

1. Run `first_setup_prompt.md`.
2. Confirm structure is correct.
3. Put at least one source into `raw/inbox/`.
4. Run `first_ingest_prompt.md`.
5. Review the changes.
6. Run `first_lint_prompt.md`.

## Expected result

After this cycle, the repository should have:
- validated structure,
- first durable wiki pages,
- updated `wiki/index.md`,
- at least one ingest entry in `wiki/log.md`,
- one lint record documenting structural quality.
