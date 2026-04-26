"""Unit tests for `scripts.ingest.setup` (the interactive wizard).

All external surfaces are mocked: input(), subprocess.run, the LLM
probe, and disk operations route through tmp_path. Tests cover each
step's happy path + the most likely failure modes a fresh user would
hit.
"""
from __future__ import annotations

import io
from pathlib import Path

import pytest

from scripts.ingest import setup as setup_mod
from scripts.ingest.setup import (
    SetupState,
    _read_env_file,
    step_check_deps,
    step_env_setup,
    step_pick_books_dir,
    step_probe_llm,
)


# ---------- _read_env_file -------------------------------------------


def test_read_env_handles_quotes_and_comments(tmp_path: Path) -> None:
    p = tmp_path / ".env"
    p.write_text(
        "# leading comment\n"
        "FOO=bar\n"
        'BAZ="quoted value"\n'
        "QUX='single quoted'\n"
        "EMPTY=\n"
        "\n",
        encoding="utf-8",
    )
    out = _read_env_file(p)
    assert out["FOO"] == "bar"
    assert out["BAZ"] == "quoted value"
    assert out["QUX"] == "single quoted"
    assert out["EMPTY"] == ""


def test_read_env_missing_file_returns_empty(tmp_path: Path) -> None:
    assert _read_env_file(tmp_path / "nope") == {}


# ---------- step_check_deps ------------------------------------------


def test_step_check_deps_passes_when_tools_present(monkeypatch) -> None:
    """All deps present → step returns True, state.deps_ok=True."""
    def _fake_which(tool: str) -> str | None:
        return f"/usr/local/bin/{tool}"
    monkeypatch.setattr(setup_mod.shutil, "which", _fake_which)
    state = SetupState()
    assert step_check_deps(state) is True
    assert state.deps_ok is True


def test_step_check_deps_fails_on_missing_pdftotext(monkeypatch) -> None:
    """Missing pdftotext → step prints fix hint and returns False."""
    def _fake_which(tool: str) -> str | None:
        return None if tool == "pdftotext" else f"/bin/{tool}"
    monkeypatch.setattr(setup_mod.shutil, "which", _fake_which)
    state = SetupState()
    assert step_check_deps(state) is False
    assert state.deps_ok is False


# ---------- step_env_setup -------------------------------------------


def test_step_env_setup_copies_template_when_missing(
    tmp_path: Path, monkeypatch
) -> None:
    """No .env present → wizard copies .env.example, then user fills it
    via $EDITOR (mocked to write the missing keys)."""
    env = tmp_path / ".env"
    env_example = tmp_path / ".env.example"
    env_example.write_text(
        "# template\n# ANTHROPIC_API_KEY=...\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(setup_mod, "ENV_PATH", env)
    monkeypatch.setattr(setup_mod, "ENV_EXAMPLE", env_example)

    def _fake_subprocess(_cmd, **_kw):
        # Simulate the user editing the file
        env.write_text(
            "ANTHROPIC_API_KEY=sk-test\n"
            "ANTHROPIC_BASE_URL=https://api.example.com\n"
            "LLM_MODEL=test-model\n",
            encoding="utf-8",
        )
        class _R:
            returncode = 0
        return _R()
    monkeypatch.setattr(setup_mod.subprocess, "run", _fake_subprocess)

    state = SetupState()
    assert step_env_setup(state) is True
    assert state.env_ok is True
    assert env.exists()


def test_step_env_setup_fails_on_missing_keys(tmp_path: Path, monkeypatch) -> None:
    """Existing .env with placeholders only → step returns False with
    explicit list of which keys are missing."""
    env = tmp_path / ".env"
    env.write_text("# nothing real\n", encoding="utf-8")
    env_example = tmp_path / ".env.example"
    env_example.write_text("", encoding="utf-8")
    monkeypatch.setattr(setup_mod, "ENV_PATH", env)
    monkeypatch.setattr(setup_mod, "ENV_EXAMPLE", env_example)
    state = SetupState()
    assert step_env_setup(state, edit_in_editor=False) is False
    assert state.env_ok is False


# ---------- step_probe_llm -------------------------------------------


def test_step_probe_llm_success(monkeypatch) -> None:
    """Mock generate_structured_output to return a parsed pong."""
    from scripts.ingest import llm_client as llm_mod

    def _fake_call(*_args, response_format, **_kw):
        return response_format(ok=True, note="pong"), {
            "model": "fake", "tokens_in": 5, "tokens_out": 5
        }
    monkeypatch.setattr(llm_mod, "generate_structured_output", _fake_call)
    state = SetupState()
    assert step_probe_llm(state) is True
    assert state.llm_ok is True


def test_step_probe_llm_handles_no_parse(monkeypatch) -> None:
    """Provider responded but content didn't parse → step returns False
    with model-name guidance, doesn't crash."""
    from scripts.ingest import llm_client as llm_mod
    monkeypatch.setattr(
        llm_mod,
        "generate_structured_output",
        lambda *a, **kw: (None, {"model": "wrong-model"}),
    )
    state = SetupState()
    assert step_probe_llm(state) is False
    assert state.llm_ok is False


def test_step_probe_llm_handles_network_exception(monkeypatch) -> None:
    """LLM SDK raises (e.g. wrong base_url) → step prints diagnosis,
    returns False instead of bubbling the exception."""
    from scripts.ingest import llm_client as llm_mod
    def _boom(*a, **kw):
        raise ConnectionError("Could not resolve host")
    monkeypatch.setattr(llm_mod, "generate_structured_output", _boom)
    state = SetupState()
    assert step_probe_llm(state) is False


# ---------- step_pick_books_dir + import path ------------------------


def test_step_pick_books_dir_direct_mode(tmp_path: Path, monkeypatch) -> None:
    """User picks a non-empty external folder + 'direct' mode →
    state.books_dir = source path, no copying happens."""
    src = tmp_path / "books"
    src.mkdir()
    (src / "a.pdf").write_bytes(b"%PDF-1.4 hi")

    inputs = iter([str(src), "direct"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(inputs))

    state = SetupState()
    assert step_pick_books_dir(state) is True
    assert state.books_dir == str(src)


def test_step_pick_books_dir_import_with_default_discipline(
    tmp_path: Path, monkeypatch
) -> None:
    """User picks flat folder + 'import' + 'default' + 'mybooks' + 'y' →
    books copied into raw/books/mybooks/ with beautified names."""
    src = tmp_path / "src"
    src.mkdir()
    (src / "[Series]Capitalism.pdf").write_bytes(b"AAA")
    (src / "Atomic Habits.epub").write_bytes(b"BBB")

    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "raw" / "books").mkdir(parents=True)
    monkeypatch.setattr(setup_mod, "REPO_ROOT", repo)
    # auto_ingest's discover_books reads REPO_ROOT to compute relative
    # paths — patch its module-level constant too.
    from scripts.ingest import auto_ingest as ai_mod
    monkeypatch.setattr(ai_mod, "REPO_ROOT", repo)

    inputs = iter([str(src), "import", "default", "mybooks", "y"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(inputs))

    state = SetupState()
    assert step_pick_books_dir(state) is True
    dest = repo / "raw" / "books"
    files = sorted((dest / "mybooks").glob("*"))
    names = {p.name for p in files}
    assert "Capitalism.pdf" in names         # bracket prefix stripped
    assert "Atomic Habits.epub" in names     # already clean
    assert state.books_dir == str(dest)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
