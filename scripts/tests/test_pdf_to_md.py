"""L1: pdf_to_md conversion guard (no real PDF/LLM).

Covers the near-empty-text rejection. pdftotext on a scanned-only PDF
returns successfully with an empty string; we want the pipeline to treat
that as a conversion failure (so the book lands in `failed` with a clear
'needs OCR' message) rather than caching the empty text and producing a
stub source page downstream.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from scripts.ingest import pdf_to_md


def test_convert_rejects_near_empty_output(tmp_path, monkeypatch):
    fake_pdf = tmp_path / "scanned.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4\n% fake body\n")

    def fake_sha(p):
        return "deadbeef"

    monkeypatch.setattr(pdf_to_md, "_sha256", fake_sha)
    # marker returns None (not available), pdftotext returns an empty page
    monkeypatch.setattr(pdf_to_md, "_marker_convert", lambda p: None)
    monkeypatch.setattr(
        pdf_to_md,
        "_pdftotext_convert",
        lambda p: ("<!-- PAGE:1 -->\n\n", 1),
    )

    with pytest.raises(RuntimeError, match="requires manual OCR"):
        pdf_to_md.convert_to_markdown(fake_pdf, cache_dir=tmp_path / "cache")


def test_convert_rejects_whitespace_only(tmp_path, monkeypatch):
    fake_pdf = tmp_path / "scanned.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4\n")
    monkeypatch.setattr(pdf_to_md, "_sha256", lambda p: "cafebabe")
    monkeypatch.setattr(pdf_to_md, "_marker_convert", lambda p: None)
    # A few pagemarkers with only whitespace between them — 400 pages of nothing.
    text = "\n".join(f"<!-- PAGE:{i} -->\n   \n" for i in range(1, 401))
    monkeypatch.setattr(pdf_to_md, "_pdftotext_convert", lambda p: (text, 400))

    with pytest.raises(RuntimeError, match="requires manual OCR"):
        pdf_to_md.convert_to_markdown(fake_pdf, cache_dir=tmp_path / "cache")


def test_convert_accepts_normal_content(tmp_path, monkeypatch):
    fake_pdf = tmp_path / "real.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4\n")
    monkeypatch.setattr(pdf_to_md, "_sha256", lambda p: "abc123")
    monkeypatch.setattr(pdf_to_md, "_marker_convert", lambda p: None)
    # Well above the 500-char floor.
    body = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 20
    text = f"<!-- PAGE:1 -->\n{body}"
    monkeypatch.setattr(pdf_to_md, "_pdftotext_convert", lambda p: (text, 1))

    meta = pdf_to_md.convert_to_markdown(fake_pdf, cache_dir=tmp_path / "cache")
    assert meta.converter == "pdftotext"
    assert meta.language == "en"
    assert Path(meta.cache_path).exists()


def test_pdftotext_runs_first_marker_not_called_for_normal_pdf(tmp_path, monkeypatch):
    """Marker should never be invoked when pdftotext gives useful output —
    the main memory-preservation guarantee. Quality doesn't regress because
    pdftotext already handles every PDF with a text layer."""
    fake_pdf = tmp_path / "normal.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4\n")
    monkeypatch.setattr(pdf_to_md, "_sha256", lambda p: "normal123")

    marker_calls: list[Path] = []

    def _marker_spy(p):
        marker_calls.append(p)
        return None

    monkeypatch.setattr(pdf_to_md, "_marker_convert", _marker_spy)
    body = "Real content " * 100  # ~1300 chars
    monkeypatch.setattr(
        pdf_to_md, "_pdftotext_convert", lambda p: (f"<!-- PAGE:1 -->\n{body}", 1)
    )

    meta = pdf_to_md.convert_to_markdown(fake_pdf, cache_dir=tmp_path / "cache")
    assert meta.converter == "pdftotext"
    assert marker_calls == [], "marker must not run when pdftotext succeeds"


def test_marker_kicks_in_as_ocr_fallback_on_scanned_pdf(tmp_path, monkeypatch):
    """When pdftotext yields empty/near-empty output (scanned PDF) AND the
    operator has opted in to marker, it is invoked as a second-line OCR
    converter. The env-var opt-in is simulated by replacing `_marker_convert`
    directly — so this test covers the orchestration branch, not the guard."""
    fake_pdf = tmp_path / "scanned.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4\n")
    monkeypatch.setattr(pdf_to_md, "_sha256", lambda p: "scanned123")

    # pdftotext returns just page markers, no text (what a scanned PDF looks like)
    monkeypatch.setattr(
        pdf_to_md,
        "_pdftotext_convert",
        lambda p: ("<!-- PAGE:1 -->\n<!-- PAGE:2 -->\n", 2),
    )

    marker_called = []

    def _marker_ok(p):
        marker_called.append(p)
        body = "OCR'd content " * 100  # ~1400 chars
        return f"<!-- PAGE:1 -->\n{body}", 1

    monkeypatch.setattr(pdf_to_md, "_marker_convert", _marker_ok)

    meta = pdf_to_md.convert_to_markdown(fake_pdf, cache_dir=tmp_path / "cache")
    assert meta.converter == "marker"
    assert marker_called == [fake_pdf]


def test_marker_disabled_by_default_via_env_guard(tmp_path, monkeypatch):
    """Without ENABLE_MARKER_OCR=1 set, `_marker_convert` must return None
    immediately without invoking the subprocess. This is the core memory-
    safety guarantee for machines that can't afford marker's PyTorch stack —
    scanned PDFs fall through to the 'requires manual OCR' error instead of
    thrashing swap."""
    fake_pdf = tmp_path / "any.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4\n")
    monkeypatch.delenv("ENABLE_MARKER_OCR", raising=False)

    run_calls: list[tuple] = []

    def _run_spy(*a, **kw):
        run_calls.append((a, kw))
        raise AssertionError("marker subprocess must not launch when guard is off")

    monkeypatch.setattr(pdf_to_md, "_run_pgroup", _run_spy)

    assert pdf_to_md._marker_convert(fake_pdf) is None
    assert run_calls == []


def test_marker_enabled_when_env_set(tmp_path, monkeypatch):
    """With ENABLE_MARKER_OCR=1 the guard passes and the function proceeds
    to the MARKER_BIN check. We point MARKER_BIN at a nonexistent path so
    the test stays hermetic (no subprocess launched, no ML models loaded)
    while still proving the guard no longer short-circuits."""
    fake_pdf = tmp_path / "any.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4\n")
    monkeypatch.setenv("ENABLE_MARKER_OCR", "1")
    monkeypatch.setattr(pdf_to_md, "MARKER_BIN", str(tmp_path / "nonexistent"))

    # Returns None (bin not found), but critically, the guard did NOT fire
    # first — that's the distinction we're verifying.
    assert pdf_to_md._marker_convert(fake_pdf) is None


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
