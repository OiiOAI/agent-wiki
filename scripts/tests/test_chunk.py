"""L1: semantic_chunking — unit, no LLM."""
from __future__ import annotations

import pytest

from scripts.ingest.chunk import Chunk, semantic_chunking


def test_empty_returns_empty() -> None:
    assert semantic_chunking("") == []
    assert semantic_chunking("   \n\n  ") == []


def test_single_short_paragraph_is_one_chunk() -> None:
    text = "This is a short paragraph with a handful of words."
    chunks = semantic_chunking(text, max_words=6000, min_chunk_words=0)
    assert len(chunks) == 1
    assert chunks[0].word_count > 0
    assert chunks[0].start_line == 1


def test_chapter_boundary_forces_new_chunk() -> None:
    big_para = " ".join(["filler"] * 200)
    text = f"{big_para}\n\nChapter 2 The Return\n\nmore content here."
    chunks = semantic_chunking(text, max_words=6000, min_chunk_words=0)
    # Chapter heading should close the previous chunk and open a new one.
    assert len(chunks) == 2
    assert "Chapter 2" in chunks[1].text
    assert "filler" in chunks[0].text


def test_max_words_budget_splits() -> None:
    # 3 paragraphs of ~250 ASCII words each → with max_words=500, expect 2 chunks.
    para = (" ".join(["alpha"] * 250) + ".")
    text = "\n\n".join([para] * 3)
    chunks = semantic_chunking(text, max_words=500, min_chunk_words=0)
    assert len(chunks) >= 2


def test_page_markers_are_preserved() -> None:
    text = (
        "<!-- PAGE:1 -->\n"
        "Intro text here.\n\n"
        "<!-- PAGE:2 -->\n"
        "More content on second page.\n"
    )
    chunks = semantic_chunking(text, max_words=6000, min_chunk_words=0)
    assert chunks[0].start_page == 1
    assert chunks[0].end_page == 2


def test_chinese_chapter_marker() -> None:
    text = "第一章 开篇\n\n" + ("中文段落。" * 300) + "\n\n第二章 承转\n\n结尾。"
    chunks = semantic_chunking(text, max_words=6000, min_chunk_words=0)
    # `第一章` and `第二章` should each begin a new chunk → we get 2 chunks.
    assert len(chunks) == 2
    assert "第一章" in chunks[0].text
    assert "第二章" in chunks[1].text


def test_chunks_have_monotonic_indices_and_lines() -> None:
    text = "\n\n".join([f"paragraph {i} " + "w" * 500 for i in range(10)])
    chunks = semantic_chunking(text, max_words=400, min_chunk_words=0)
    for i in range(1, len(chunks)):
        assert chunks[i].index == i
        assert chunks[i].start_line >= chunks[i - 1].end_line


def test_tiny_trailing_chunk_is_merged() -> None:
    big = " ".join(["word"] * 800) + "."
    small = "tail."
    text = big + "\n\n" + small
    chunks = semantic_chunking(text, max_words=1200, min_chunk_words=50)
    # With min_chunk_words=50, the tail (<50 words) must merge into previous.
    assert len(chunks) == 1
    assert "tail" in chunks[0].text


def test_tiny_trailing_never_crosses_chapter() -> None:
    """A short chapter must NOT be merged into the previous chapter. The
    chapter boundary is a hard wall — extractors see one chapter per chunk."""
    chapter1 = " ".join(["content"] * 500) + "."
    chapter2 = "Chapter 2 Epilogue\n\nThe end."  # tiny — well below min_chunk_words
    text = chapter1 + "\n\n" + chapter2
    chunks = semantic_chunking(text, max_words=6000, min_chunk_words=500)
    assert len(chunks) == 2, (
        f"short Chapter 2 must not be merged into Chapter 1 — got {len(chunks)} chunks"
    )
    assert "content" in chunks[0].text
    assert "Chapter 2" in chunks[1].text
    assert "Chapter 2" not in chunks[0].text


def test_long_chapter_subdivides_within_chapter() -> None:
    """A chapter that exceeds max_words is split into multiple sub-chunks,
    but every sub-chunk must carry the same chapter tag."""
    para = " ".join(["alpha"] * 400) + "."
    text = "Chapter 1 Introduction\n\n" + "\n\n".join([para] * 5)
    chunks = semantic_chunking(text, max_words=800, min_chunk_words=0)
    assert len(chunks) >= 2, "long chapter should subdivide"
    for c in chunks:
        assert c.tags == ["Chapter 1 Introduction"] or c.tags[0].startswith(
            "Chapter 1"
        ), f"sub-chunk lost chapter tag: {c.tags}"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
