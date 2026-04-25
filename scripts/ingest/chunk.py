"""Phase B: split a converted markdown document into LLM-sized chunks.

Strategy (chapter-first; chunks never cross a chapter boundary):
  1. Detect chapter boundaries with `_CHAPTER_RE` (markdown headers + Chapter/
     Part/Section + Chinese `第X章/节/篇/部`).
  2. Group paragraphs into chapters. Everything before the first heading goes
     into an implicit preamble "chapter".
  3. For each chapter, emit 1+ sub-chunks capped by `max_words`. A chapter
     smaller than `max_words` becomes one sub-chunk. A larger chapter is
     split at paragraph boundaries until each sub-chunk fits.
  4. Tiny trailing sub-chunks (< `min_chunk_words`) are merged into the
     previous sub-chunk of the SAME chapter — never across chapter
     boundaries. That way a downstream extractor never sees two different
     chapters' text fused into one LLM prompt.

`max_words` default is 30_000. Minimax M2.7-highspeed has a 256K-token
context; 30K English words (~40K tokens) or 30K CJK chars leaves generous
room for the system prompt, JSON schema, and structured output.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

_CHAPTER_RE = re.compile(
    r"^(?:#{1,6}\s+.+"
    r"|Chapter\s+\d+"
    r"|Part\s+[IVX\d]+"
    r"|Section\s+\d+"
    r"|第[一二三四五六七八九十百千]+[章节篇部])\s*.*$",
    re.IGNORECASE,
)

_PAGE_MARKER_RE = re.compile(r"<!--\s*PAGE:(\d+)\s*-->")


@dataclass
class Chunk:
    text: str
    index: int
    start_line: int
    end_line: int
    start_page: int | None = None
    end_page: int | None = None
    word_count: int = 0
    tags: list[str] = field(default_factory=list)


def _count_words(text: str) -> int:
    ascii_words = len(re.findall(r"[A-Za-z]+", text))
    cjk_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    return ascii_words + cjk_chars


def _last_page_in(text: str) -> int | None:
    matches = list(_PAGE_MARKER_RE.finditer(text))
    return int(matches[-1].group(1)) if matches else None


def _first_page_in(text: str) -> int | None:
    m = _PAGE_MARKER_RE.search(text)
    return int(m.group(1)) if m else None


def _split_paragraphs(text: str) -> list[tuple[int, int, str]]:
    """Split raw text into (start_line, end_line, body) paragraphs.

    A paragraph is a maximal run of non-blank lines; blank lines are separators.
    Line numbers are 1-indexed.
    """
    paragraphs: list[tuple[int, int, str]] = []
    lines = text.splitlines()
    buf: list[str] = []
    buf_start: int | None = None
    for i, line in enumerate(lines, start=1):
        if line.strip() == "":
            if buf:
                paragraphs.append((buf_start or i, i - 1, "\n".join(buf)))
                buf = []
                buf_start = None
            continue
        if buf_start is None:
            buf_start = i
        buf.append(line)
    if buf:
        paragraphs.append((buf_start or len(lines), len(lines), "\n".join(buf)))
    return paragraphs


def _is_chapter_paragraph(body: str) -> bool:
    lines = body.splitlines()
    if not lines:
        return False
    return bool(_CHAPTER_RE.match(lines[0]))


def _group_into_chapters(
    paragraphs: list[tuple[int, int, str]],
) -> list[list[tuple[int, int, str]]]:
    """Partition paragraphs so each sub-list is one chapter.

    A chapter begins at a paragraph matching `_CHAPTER_RE`, or at the start
    of the document. Paragraphs before the first heading form an implicit
    preamble chapter.
    """
    chapters: list[list[tuple[int, int, str]]] = [[]]
    for para in paragraphs:
        _, _, body = para
        if _is_chapter_paragraph(body) and chapters[-1]:
            chapters.append([para])
        else:
            chapters[-1].append(para)
    return [c for c in chapters if c]


def _split_chapter(
    chapter_paras: list[tuple[int, int, str]],
    max_words: int,
    chapter_hint: str | None,
    start_index: int,
) -> list[Chunk]:
    """Pack a single chapter's paragraphs into sub-chunks ≤ max_words.

    Never crosses chapter boundaries (caller guarantees that). If a single
    paragraph exceeds max_words it gets its own chunk unsplit — splitting
    mid-paragraph is not supported because it would orphan sentences.
    """
    sub_chunks: list[Chunk] = []
    cur_lines: list[str] = []
    cur_start_line: int | None = None
    cur_end_line: int | None = None
    cur_words = 0

    def emit() -> None:
        nonlocal cur_lines, cur_start_line, cur_end_line, cur_words
        if not cur_lines:
            return
        body = "\n".join(cur_lines).rstrip()
        if not body.strip():
            cur_lines = []
            cur_start_line = cur_end_line = None
            cur_words = 0
            return
        sub_chunks.append(
            Chunk(
                text=body,
                index=start_index + len(sub_chunks),
                start_line=cur_start_line or 1,
                end_line=cur_end_line or 1,
                start_page=_first_page_in(body),
                end_page=_last_page_in(body),
                word_count=cur_words,
                tags=[chapter_hint] if chapter_hint else [],
            )
        )
        cur_lines = []
        cur_start_line = cur_end_line = None
        cur_words = 0

    for start, end, body in chapter_paras:
        pwords = _count_words(body)
        if cur_words + pwords > max_words and cur_words > 0:
            emit()
        if cur_start_line is None:
            cur_start_line = start
        cur_end_line = end
        cur_lines.append(body)
        cur_words += pwords
    emit()
    return sub_chunks


def semantic_chunking(
    text: str,
    max_words: int = 30_000,
    min_chunk_words: int = 300,
) -> list[Chunk]:
    """Chapter-first chunking. See module docstring."""
    paragraphs = _split_paragraphs(text)
    if not paragraphs:
        return []

    chapters = _group_into_chapters(paragraphs)

    chunks: list[Chunk] = []
    for chapter_paras in chapters:
        first_body = chapter_paras[0][2]
        chapter_hint: str | None = None
        if _is_chapter_paragraph(first_body):
            chapter_hint = first_body.splitlines()[0].strip()[:80]

        sub_chunks = _split_chapter(
            chapter_paras,
            max_words=max_words,
            chapter_hint=chapter_hint,
            start_index=len(chunks),
        )

        # Merge a tiny trailing sub-chunk into the previous one, but ONLY
        # within this chapter. Never fuse across chapters.
        if len(sub_chunks) >= 2 and sub_chunks[-1].word_count < min_chunk_words:
            last = sub_chunks.pop()
            prev = sub_chunks[-1]
            prev.text = prev.text + "\n\n" + last.text
            prev.end_line = last.end_line
            prev.end_page = last.end_page or prev.end_page
            prev.word_count += last.word_count

        chunks.extend(sub_chunks)

    # Reindex so final indices are dense and monotonic regardless of merges.
    for i, c in enumerate(chunks):
        c.index = i

    return chunks
