"""Unit tests for `scripts.ingest.import_books`.

Covers:
  - beautify_filename: leading [bracket], 【fullwidth】, ·[author] suffix,
    whitespace collapse, length cap, idempotency, extension preservation
  - detect_layout: subdir vs flat
  - classify_books: subdir / default / manual modes, slug sanitization
  - import_books: copy + dedup-on-stem-collision + dry-run + skip identical
"""
from __future__ import annotations

from pathlib import Path

import pytest

from scripts.ingest.import_books import (
    BookEntry,
    beautify_filename,
    classify_books,
    detect_layout,
    import_books,
)


# ---------- beautify_filename ----------------------------------------


def test_beautify_strips_leading_halfwidth_bracket() -> None:
    assert (
        beautify_filename("[当代经济学系列丛书]微观经济学.pdf")
        == "微观经济学.pdf"
    )


def test_beautify_strips_leading_fullwidth_bracket() -> None:
    assert (
        beautify_filename("【二十世纪文库】人力投资 - 舒尔茨.pdf")
        == "人力投资 - 舒尔茨.pdf"
    )


def test_beautify_strips_chained_brackets() -> None:
    """Some books have both bracket types stacked in the prefix."""
    assert (
        beautify_filename("[A][B]【C】Real Title.pdf")
        == "Real Title.pdf"
    )


def test_beautify_strips_trailing_author_suffix() -> None:
    assert (
        beautify_filename("资本主义与自由·[美]米尔顿·弗里德曼 著.pdf")
        == "资本主义与自由.pdf"
    )


def test_beautify_collapses_whitespace() -> None:
    assert (
        beautify_filename("Foo    Bar     Baz.pdf")
        == "Foo Bar Baz.pdf"
    )


def test_beautify_strips_leading_number_dot() -> None:
    assert beautify_filename("01. Chapter One.pdf") == "Chapter One.pdf"
    assert beautify_filename("1_Foo.epub") == "Foo.epub"


def test_beautify_normalizes_extension_case() -> None:
    assert beautify_filename("Foo.PDF").endswith(".pdf")
    assert beautify_filename("Bar.EPUB").endswith(".epub")


def test_beautify_caps_length_preserving_extension() -> None:
    long = "A" * 200 + ".pdf"
    out = beautify_filename(long)
    assert len(out) <= 105
    assert out.endswith(".pdf")


def test_beautify_idempotent() -> None:
    """Running the function twice on its own output must produce the
    same result — important when the wizard might rerun on a partial
    import."""
    src = "[丛书名]Some Book - 作者 著.pdf"
    once = beautify_filename(src)
    twice = beautify_filename(once)
    assert once == twice


def test_beautify_empty_stem_falls_back_to_untitled() -> None:
    """Pathological case: filename is *only* a bracketed prefix.
    We must not return just `.pdf` — the file would silently overwrite
    every other empty-stem book during copy."""
    assert beautify_filename("[].pdf") == "untitled.pdf"


def test_beautify_filesystem_hostile_chars_dropped() -> None:
    assert beautify_filename('Foo<>:"|?*Bar.pdf') == "FooBar.pdf"


def test_beautify_preserves_cjk_and_ascii_mix() -> None:
    assert beautify_filename("道德经 - Tao Te Ching.epub") == "道德经 - Tao Te Ching.epub"


# ---------- detect_layout --------------------------------------------


def test_detect_layout_flat(tmp_path: Path) -> None:
    (tmp_path / "a.pdf").write_bytes(b"%PDF")
    (tmp_path / "b.epub").write_bytes(b"x")
    assert detect_layout(tmp_path) == "flat"


def test_detect_layout_subdir(tmp_path: Path) -> None:
    (tmp_path / "neuroscience").mkdir()
    (tmp_path / "neuroscience" / "spark.pdf").write_bytes(b"%PDF")
    (tmp_path / "philosophy").mkdir()
    (tmp_path / "philosophy" / "tao.epub").write_bytes(b"x")
    assert detect_layout(tmp_path) == "subdir"


def test_detect_layout_mixed_returns_flat(tmp_path: Path) -> None:
    """When both top-level books AND subdir books exist, treat as flat
    (subdir mode would orphan the top-level books). Flat → user picks
    a default discipline label that covers everything."""
    (tmp_path / "loose.pdf").write_bytes(b"%PDF")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "x.pdf").write_bytes(b"%PDF")
    assert detect_layout(tmp_path) == "flat"


# ---------- classify_books -------------------------------------------


def test_classify_subdir_uses_parent_dir_name(tmp_path: Path) -> None:
    n = tmp_path / "neuroscience"
    n.mkdir()
    (n / "spark.pdf").write_bytes(b"%PDF")
    plan = classify_books([n / "spark.pdf"], mode="subdir", src_root=tmp_path)
    assert plan[0].discipline == "neuroscience"
    assert plan[0].beautified == "spark.pdf"


def test_classify_default_assigns_one_label() -> None:
    plan = classify_books(
        [Path("/tmp/a.pdf"), Path("/tmp/b.epub")],
        mode="default",
        default="mybooks",
    )
    assert all(e.discipline == "mybooks" for e in plan)


def test_classify_manual_uses_callback() -> None:
    answers = iter(["philosophy", ""])  # second book → fallback
    plan = classify_books(
        [Path("/tmp/a.pdf"), Path("/tmp/b.epub")],
        mode="manual",
        default="general",
        ask=lambda _prompt: next(answers),
    )
    assert plan[0].discipline == "philosophy"
    assert plan[1].discipline == "general"


def test_classify_sanitizes_discipline_to_filesystem_safe_slug() -> None:
    plan = classify_books(
        [Path("/tmp/a.pdf")],
        mode="default",
        default="My Disc/With Bad Chars!",
    )
    assert "/" not in plan[0].discipline
    assert "!" not in plan[0].discipline
    assert plan[0].discipline == "my-disc-with-bad-chars"


# ---------- import_books ---------------------------------------------


def test_import_books_copies_into_disciplined_tree(tmp_path: Path) -> None:
    src = tmp_path / "src.pdf"
    src.write_bytes(b"hello world")
    dest = tmp_path / "out"
    plan = [BookEntry(src=src, discipline="philosophy", beautified="cleaned.pdf")]

    copied, skipped, total = import_books(plan, dest)

    assert copied == 1
    assert skipped == 0
    assert (dest / "philosophy" / "cleaned.pdf").exists()
    assert (dest / "philosophy" / "cleaned.pdf").read_bytes() == b"hello world"
    # Original untouched
    assert src.read_bytes() == b"hello world"


def test_import_books_dedups_on_target_collision(tmp_path: Path) -> None:
    """Two source books beautify to the same target name. Second gets
    a numeric suffix instead of clobbering the first."""
    a = tmp_path / "a.pdf"; a.write_bytes(b"AAA")
    b = tmp_path / "b.pdf"; b.write_bytes(b"BBB")
    dest = tmp_path / "out"
    plan = [
        BookEntry(src=a, discipline="d", beautified="same.pdf"),
        BookEntry(src=b, discipline="d", beautified="same.pdf"),
    ]
    copied, _, _ = import_books(plan, dest)
    assert copied == 2
    # Both files should land, with suffix on the second
    files = sorted((dest / "d").glob("*.pdf"))
    assert len(files) == 2
    assert {f.read_bytes() for f in files} == {b"AAA", b"BBB"}


def test_import_books_skips_byte_identical_existing(tmp_path: Path) -> None:
    """Idempotency: rerunning after partial copy doesn't re-copy."""
    src = tmp_path / "x.pdf"; src.write_bytes(b"data")
    dest = tmp_path / "out"
    plan = [BookEntry(src=src, discipline="d", beautified="x.pdf")]
    import_books(plan, dest)
    copied, skipped, _ = import_books(plan, dest)
    assert copied == 0
    assert skipped == 1


def test_import_books_dry_run_writes_nothing(tmp_path: Path) -> None:
    src = tmp_path / "x.pdf"; src.write_bytes(b"data")
    dest = tmp_path / "out"
    plan = [BookEntry(src=src, discipline="d", beautified="x.pdf")]
    copied, skipped, total = import_books(plan, dest, dry_run=True)
    assert copied == 1
    assert not (dest / "d" / "x.pdf").exists()


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
