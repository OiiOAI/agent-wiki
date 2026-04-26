"""Interactive setup wizard — `python -m scripts.ingest.setup`.

The shortest path from a fresh clone to the first wiki page committed.
Six steps, each optional / interruptible (Ctrl-C exits cleanly without
losing earlier work). State persists to `tmp/setup_state.json` so a
re-run resumes after the last completed step.

Designed for a user who has just run `pip install -r requirements.txt`
and may have never read the README. We do every check the CLI assumes
the user has already done:

  1. system deps (python ≥ 3.10, pdftotext, pandoc; warn on ocrmypdf)
  2. .env exists + required keys present (offers to copy + open in $EDITOR)
  3. LLM connectivity probe (tiny prompt, ~$0.001)
  4. books-dir selection (with discover preview)
  5. trial run — limit=1 by default, or dry-discover only
  6. commit to wiki/ (optional, prompts y/N)

We deliberately do NOT show a cost-confirmation prompt before every run
— per-book / batch caps are the budget mechanism. Wizard's trial run
caps per-book at $1 to be safe.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable

from pydantic import BaseModel

REPO_ROOT = Path(__file__).resolve().parents[2]
TMP = REPO_ROOT / "tmp"
STATE_PATH = TMP / "setup_state.json"
ENV_PATH = REPO_ROOT / ".env"
ENV_EXAMPLE = REPO_ROOT / ".env.example"


# ----- helpers --------------------------------------------------------


def _say(msg: str = "") -> None:
    """Single output point so tests can capture cleanly."""
    print(msg, flush=True)


def _ask(prompt: str, default: str | None = None) -> str:
    """Like input() but with a default value shown in [brackets]."""
    suffix = f" [{default}]" if default else ""
    try:
        ans = input(f"{prompt}{suffix}: ").strip()
    except EOFError:
        return default or ""
    return ans or (default or "")


def _yes_no(prompt: str, default: bool = False) -> bool:
    suffix = " [Y/n]" if default else " [y/N]"
    ans = _ask(prompt + suffix, default="").strip().lower()
    if not ans:
        return default
    return ans in ("y", "yes")


def _section(title: str) -> None:
    _say()
    _say(f"━━━ {title} ━━━")


# ----- state ----------------------------------------------------------


@dataclass
class SetupState:
    deps_ok: bool = False
    env_ok: bool = False
    llm_ok: bool = False
    books_dir: str | None = None
    trial_done: bool = False
    committed: bool = False
    notes: list[str] = field(default_factory=list)


def _load_state() -> SetupState:
    if not STATE_PATH.exists():
        return SetupState()
    try:
        return SetupState(**json.loads(STATE_PATH.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, OSError, TypeError):
        return SetupState()


def _save_state(state: SetupState) -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(
        json.dumps(asdict(state), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


# ----- step 1: system deps -------------------------------------------


def step_check_deps(state: SetupState) -> bool:
    _section("Step 1/6 — System dependencies")
    issues: list[str] = []

    py_major, py_minor = sys.version_info[:2]
    if (py_major, py_minor) < (3, 10):
        issues.append(
            f"Python {py_major}.{py_minor} too old (need ≥ 3.10). "
            "Install python@3.12 via your package manager."
        )
    else:
        _say(f"  ✓ Python {py_major}.{py_minor}")

    for tool, install_hint in [
        ("pdftotext", "macOS: brew install poppler  |  Linux: apt install poppler-utils"),
        ("pandoc",    "macOS: brew install pandoc   |  Linux: apt install pandoc"),
    ]:
        path = shutil.which(tool)
        if path:
            _say(f"  ✓ {tool} ({path})")
        else:
            issues.append(f"Missing `{tool}`. Install: {install_hint}")

    if not shutil.which("ocrmypdf"):
        _say(
            "  · ocrmypdf not found (only needed for scanned PDFs). "
            "Install later if you hit a `requires manual OCR` error."
        )
    else:
        _say(f"  ✓ ocrmypdf ({shutil.which('ocrmypdf')})")

    if issues:
        _say()
        for i in issues:
            _say(f"  ✗ {i}")
        _say()
        _say("Fix the above and rerun: python -m scripts.ingest.setup")
        return False

    state.deps_ok = True
    return True


# ----- step 2: .env ---------------------------------------------------


REQUIRED_ENV_KEYS = ("ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL", "LLM_MODEL")


def _read_env_file(path: Path) -> dict[str, str]:
    """Tiny .env parser (we don't want to require python-dotenv at module
    top — it's already used downstream by llm_client, but this keeps
    setup importable even if dotenv isn't installed)."""
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, _, v = line.partition("=")
        v = v.strip().strip('"').strip("'")
        out[k.strip()] = v
    return out


def step_env_setup(state: SetupState, *, edit_in_editor: bool = True) -> bool:
    _section("Step 2/6 — `.env` credentials")

    if not ENV_PATH.exists():
        if not ENV_EXAMPLE.exists():
            _say(f"  ✗ Neither .env nor .env.example found at {REPO_ROOT}")
            return False
        shutil.copy(ENV_EXAMPLE, ENV_PATH)
        _say(f"  · Copied {ENV_EXAMPLE.name} → {ENV_PATH.name}")
        _say("  · Open it now and uncomment ONE provider block (Claude / Minimax / etc.)")
        if edit_in_editor:
            editor = os.environ.get("EDITOR", "vi")
            try:
                subprocess.run([editor, str(ENV_PATH)], check=False)
            except FileNotFoundError:
                _say(f"  · Editor `{editor}` not found. Edit {ENV_PATH} manually, then press Enter.")
                _ask("Press Enter when done")
        else:
            _ask(f"Edit {ENV_PATH} in another terminal, then press Enter")

    env = _read_env_file(ENV_PATH)
    missing = [k for k in REQUIRED_ENV_KEYS if not env.get(k)]
    if missing:
        _say()
        _say(f"  ✗ Missing required keys in .env: {', '.join(missing)}")
        _say(f"  Edit {ENV_PATH} and set:")
        for k in missing:
            hint = {
                "ANTHROPIC_API_KEY":  "your provider's API key (e.g. sk-ant-... for Claude)",
                "ANTHROPIC_BASE_URL": "endpoint URL (e.g. https://api.anthropic.com)",
                "LLM_MODEL":          "model name (e.g. claude-sonnet-4-5, MiniMax-M2.7-highspeed)",
            }[k]
            _say(f"    {k}=<{hint}>")
        return False

    _say(f"  ✓ All required keys present")
    _say(f"  · Provider: {env.get('ANTHROPIC_BASE_URL', '?')}")
    _say(f"  · Model:    {env.get('LLM_MODEL', '?')}")
    state.env_ok = True
    return True


# ----- step 3: LLM probe ---------------------------------------------


class _Ping(BaseModel):
    ok: bool
    note: str


def step_probe_llm(state: SetupState) -> bool:
    _section("Step 3/6 — LLM connectivity")
    _say("  · Sending a 1-token probe to verify auth + endpoint...")

    # Import here so step 1 can fail without dragging the LLM SDK in.
    from .llm_client import generate_structured_output

    t0 = time.monotonic()
    try:
        parsed, usage = generate_structured_output(
            system_prompt="Return JSON {\"ok\": true, \"note\": \"hi\"}.",
            user_content="ping",
            response_format=_Ping,
            max_tokens=64,
        )
    except Exception as e:
        _say(f"  ✗ LLM call raised: {type(e).__name__}: {e}")
        _say("    Common causes:")
        _say("      • Wrong ANTHROPIC_BASE_URL → verify provider's docs")
        _say("      • Bad ANTHROPIC_API_KEY → regenerate in provider's dashboard")
        _say("      • Network blocked → check VPN / firewall")
        return False
    elapsed = time.monotonic() - t0

    if parsed is None:
        _say(f"  ✗ LLM returned no parseable JSON in {elapsed:.1f}s.")
        _say("    The provider responded but the content didn't validate.")
        _say("    Often means the model name is unknown to the provider — check LLM_MODEL.")
        return False

    _say(f"  ✓ LLM ok ({usage.get('model','?')}, {elapsed:.1f}s, "
         f"~{usage.get('tokens_in',0)+usage.get('tokens_out',0)} tokens)")
    state.llm_ok = True
    return True


# ----- step 4: books-dir ---------------------------------------------


def step_pick_books_dir(state: SetupState) -> bool:
    _section("Step 4/6 — Books folder")
    from .auto_ingest import discover_books
    from .import_books import (
        BookEntry,
        beautify_filename,
        classify_books,
        detect_layout,
        import_books,
    )

    # 4a. Pick source folder
    while True:
        default = state.books_dir or str(REPO_ROOT / "raw" / "books")
        raw = _ask("Path to your PDF/EPUB folder", default=default)
        src_root = Path(raw).expanduser().resolve()

        if not src_root.exists():
            if _yes_no(f"  · {src_root} doesn't exist. Create it?", default=True):
                src_root.mkdir(parents=True, exist_ok=True)
                _say(f"  · Created {src_root}")
                _say(f"  · Now copy at least one .pdf or .epub into it, then press Enter.")
                _ask("Press Enter when ready")
            else:
                continue

        try:
            books = discover_books(REPO_ROOT, books_dir=src_root)
        except Exception as e:
            _say(f"  ✗ discover_books failed: {e}")
            continue

        if not books:
            _say(f"  · {src_root} has no .pdf or .epub files.")
            _say(f"    Add some, then press Enter to rescan.")
            if _yes_no("Re-scan now?", default=True):
                continue
            return False

        # Resolve sizes via either repo-relative or absolute paths
        def _src_path(rel_or_abs: str) -> Path:
            p = Path(rel_or_abs)
            return p if p.is_absolute() else (REPO_ROOT / rel_or_abs)

        total_mb = sum(
            _src_path(src).stat().st_size for _, src in books if _src_path(src).exists()
        ) / 1024 / 1024
        disciplines = sorted({Path(src).parent.name for _, src in books[:50]})
        _say(f"  ✓ Found {len(books)} books ({total_mb:.1f} MB)")
        _say(f"  · Discipline subfolders (sampled): "
             f"{', '.join(disciplines[:8])}{' …' if len(disciplines) > 8 else ''}")
        break

    # 4b. Direct vs import?
    inside_repo = src_root.is_relative_to(REPO_ROOT)
    if inside_repo and src_root == REPO_ROOT / "raw" / "books":
        _say(f"  · Source is already raw/books/ — no import needed.")
        state.books_dir = str(src_root)
        return True

    _say()
    _say("  Two options:")
    _say("    direct = use this folder directly (no copy; provenance points here)")
    _say("    import = copy into raw/books/ with name cleanup + discipline tag (recommended)")
    mode = _ask("Choose direct / import", default="import").lower()
    if mode.startswith("d"):
        state.books_dir = str(src_root)
        return True

    # 4c-4d. Beautify + classify
    src_paths = [_src_path(src) for _, src in books]
    layout = detect_layout(src_root)
    if layout == "subdir":
        _say(f"  · Source has subdirectories — using each subdir name as discipline.")
        plan_mode = "subdir"
        default_disc = "general"
    else:
        _say()
        _say("  How should books be classified into disciplines?")
        _say("    default = put all in one discipline (e.g. 'general' or 'mybooks')")
        _say("    manual  = ask per book (slow for >10 books)")
        cls = _ask("Choose default / manual", default="default").lower()
        if cls.startswith("m"):
            plan_mode = "manual"
            default_disc = _ask("Fallback discipline name", default="general")
        else:
            plan_mode = "default"
            default_disc = _ask("Discipline name for all books", default="general")

    plan = classify_books(
        src_paths,
        mode=plan_mode,
        default=default_disc,
        src_root=src_root,
        ask=_ask if plan_mode == "manual" else None,
    )

    # 4e. Preview + confirm
    _say()
    _say("  Preview (first 5):")
    for e in plan[:5]:
        same = "  (unchanged)" if e.beautified == e.src.name else ""
        _say(f"    {e.src.name[:60]:60s}  →  {e.discipline}/{e.beautified}{same}")
    if len(plan) > 5:
        _say(f"    ... and {len(plan) - 5} more")

    if not _yes_no(f"  Copy {len(plan)} books into {REPO_ROOT}/raw/books/?", default=True):
        _say("  · Skipped. Using source folder directly.")
        state.books_dir = str(src_root)
        return True

    dest_root = REPO_ROOT / "raw" / "books"
    copied, skipped, total_bytes = import_books(
        plan,
        dest_root,
        on_progress=lambda i, n, e: (
            _say(f"    [{i}/{n}] {e.discipline}/{e.beautified[:60]}")
            if i % 10 == 0 or i == n
            else None
        ),
    )
    _say(f"  ✓ Imported {copied} new ({skipped} skipped as duplicates), "
         f"{total_bytes/1024/1024:.1f} MB")
    state.books_dir = str(dest_root)
    return True


# ----- step 5: trial run ---------------------------------------------


def step_trial_run(state: SetupState) -> bool:
    _section("Step 5/6 — Trial run")
    _say("  Options:")
    _say("    1 = process the first 1 book (recommended; ~$0.30, ~5 min)")
    _say("    3 = process the first 3 books (~$1, ~15 min)")
    _say("    d = dry-discover only (no LLM spend; just lists what would run)")
    choice = _ask("Choose 1 / 3 / d", default="1").lower()

    from .auto_ingest import main as auto_ingest_main

    if choice == "d":
        rc = auto_ingest_main(["--books-dir", state.books_dir, "--dry-discover"])
        return rc == 0

    n = 3 if choice == "3" else 1
    rc = auto_ingest_main([
        "--books-dir", state.books_dir,
        "--limit", str(n),
        "--per-book-cap", "1",
    ])
    if rc != 0:
        _say(f"  ✗ Trial run exited with code {rc}. Check tmp/ingest_log/ for details.")
        return False
    state.trial_done = True
    return True


# ----- step 6: commit -------------------------------------------------


def step_commit(state: SetupState) -> bool:
    _section("Step 6/6 — Commit to wiki/")
    if not _yes_no("Land staged pages into wiki/ + create per-book git commits?", default=True):
        _say(f"  · Skipped. Staged pages are at: tmp/ingest_staging/")
        _say(f"  · Run later: python -m scripts.ingest.commit_batch")
        return True

    from .commit_batch import main as commit_main

    rc = commit_main([])
    if rc != 0:
        _say(f"  ✗ commit_batch exited with code {rc}.")
        return False
    state.committed = True
    return True


# ----- summary --------------------------------------------------------


def step_summary(state: SetupState) -> None:
    _section("Done — what next?")
    wiki = REPO_ROOT / "wiki"
    md_count = sum(1 for _ in wiki.rglob("*.md")) if wiki.is_dir() else 0
    _say(f"  · wiki/ now contains {md_count} markdown pages.")
    _say()
    _say("  Full unattended run:")
    _say(f"    nohup python -m scripts.ingest.auto_ingest \\")
    _say(f"        --books-dir {state.books_dir} --budget 50 \\")
    _say(f"        > tmp/run.log 2>&1 &")
    _say()
    _say("  Periodic health check:")
    _say("    python -m scripts.lint.wiki_lint")
    _say()
    _say("  Deeper docs:")
    _say("    docs/快速上手.md   — Chinese tutorial (this wizard's full reference)")
    _say("    USAGE.md          — phase-by-phase API recipes")
    _say()


# ----- driver ---------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    state = _load_state()
    steps: list[tuple[str, Callable[[SetupState], bool], bool]] = [
        ("deps", step_check_deps, state.deps_ok),
        ("env",  step_env_setup,  state.env_ok),
        ("llm",  step_probe_llm,  state.llm_ok),
        ("dir",  step_pick_books_dir, bool(state.books_dir)),
        ("trial", step_trial_run, state.trial_done),
        ("commit", step_commit, state.committed),
    ]

    _say("agent-wiki interactive setup")
    _say(f"State: {STATE_PATH.relative_to(REPO_ROOT)}  "
         f"(delete it to restart from scratch)")

    try:
        for name, fn, already_done in steps:
            if already_done:
                _say(f"  · skipping {name} (already done in earlier run)")
                continue
            ok = fn(state)
            _save_state(state)
            if not ok:
                return 1
        step_summary(state)
        return 0
    except KeyboardInterrupt:
        _save_state(state)
        _say()
        _say("[setup] Interrupted. Progress saved; rerun to resume.")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
