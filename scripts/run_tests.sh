#!/usr/bin/env bash
# Runs L1-L3 unit tests (no LLM). L4+ tests live alongside but are skipped
# by this entrypoint; invoke pytest directly on scripts/tests/test_e2e_*.py
# when you want them.
set -euo pipefail

cd "$(dirname "$0")/.."
export PYTHONPATH="${PYTHONPATH:-}:$(pwd)"

# Prefer the repo venv if it exists — system python3 may lack pytest/pypinyin.
if [ -x ".venv/bin/python" ]; then
    PY=.venv/bin/python
else
    PY=python3
fi

echo "==> Running L1-L3 unit tests (no LLM required)"
"$PY" -m pytest \
    scripts/tests/test_chunk.py \
    scripts/tests/test_schemas.py \
    scripts/tests/test_compile.py \
    scripts/tests/test_validate.py \
    scripts/tests/test_conflict_check.py \
    scripts/tests/test_gate.py \
    scripts/tests/test_extract.py \
    scripts/tests/test_pdf_to_md.py \
    scripts/tests/test_import_books.py \
    scripts/tests/test_setup.py \
    -v "$@"
