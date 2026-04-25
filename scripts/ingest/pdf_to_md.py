"""Phase A: PDF/EPUB → Markdown with page anchors.

Strategy:
  1. marker_single  — best fidelity, emits page markers (converted to
                      `<!-- PAGE:N -->`).
  2. pdftotext -layout — tolerant fallback; pages separated by form feed (\\f),
                         we rewrite each form feed as `<!-- PAGE:N -->`.
  3. pandoc -t plain — EPUB / other text formats; no page concept, so we emit
                       no page markers (line anchors only).

Cache key is `<stem>.md` in `tmp/md_cache/`. A `<stem>.meta.json` records
converter / sha256 / pages_total / language. Rerunning with the same input
reuses the cache.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

MARKER_BIN = os.environ.get(
    "MARKER_BIN",
    "/Users/moondy/Library/Python/3.10/bin/marker_single",
)
PDFTOTEXT_BIN = shutil.which("pdftotext") or "pdftotext"
PANDOC_BIN = shutil.which("pandoc") or "pandoc"

# Marker loads multi-GB ML models per invocation. Lowering the cap from
# 900s to 600s trims the worst-case memory footprint when a scanned book
# refuses to converge, without affecting quality — by 10 minutes marker
# has either succeeded or is going to OOM the machine.
_MARKER_TIMEOUT_S = 600


def _run_pgroup(
    cmd: list[str],
    *,
    timeout: int,
    capture: bool = True,
) -> subprocess.CompletedProcess:
    """Run `cmd` in its own process group and guarantee teardown.

    `subprocess.run(timeout=...)` only SIGKILLs the direct child PID; any
    grandchildren become orphans that keep RAM (and, for marker, GPU/CPU)
    allocated. Worse, if the PARENT gets SIGINT'd while blocked in
    `subprocess.run`'s internal wait, the default code path never kills
    the child at all — exactly how we ended up with a 77-min marker
    zombie holding the machine hostage.

    This helper uses Popen + start_new_session and wraps communicate() in
    try/except BaseException so every exit path (timeout, KeyboardInterrupt,
    SystemExit, arbitrary error) SIGKILLs the whole group before bubbling.
    """
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
        return subprocess.CompletedProcess(
            cmd, proc.returncode, stdout=stdout, stderr=stderr
        )
    except BaseException:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except (ProcessLookupError, PermissionError, OSError):
            pass
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            pass
        raise


@dataclass
class ConversionMeta:
    converter: str  # 'marker' | 'pdftotext' | 'pandoc'
    pages_total: int | None
    sha256: str
    language: str  # 'en' | 'zh' | 'unknown'
    source_path: str
    cache_path: str


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _detect_language(text: str) -> str:
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    latin = len(re.findall(r"[A-Za-z]", text))
    if cjk == 0 and latin == 0:
        return "unknown"
    return "zh" if cjk > latin else "en"


def _marker_convert(src: Path) -> tuple[str, int] | None:
    """Run marker_single, return (markdown_text_with_page_markers, pages_total).

    Opt-in via `ENABLE_MARKER_OCR=1`. Marker loads multi-GB PyTorch models
    that thrash swap on a 16GB machine even as a lone process, and its
    Chinese OCR quality is poor. Default off — scanned PDFs fail cleanly
    with 'requires manual OCR' instead, letting the user route them to an
    external OCR tool.
    """
    if os.environ.get("ENABLE_MARKER_OCR", "0") != "1":
        return None
    if not Path(MARKER_BIN).exists():
        return None
    with tempfile.TemporaryDirectory(prefix="marker-") as td:
        try:
            _run_pgroup(
                [MARKER_BIN, str(src), "--output_dir", td, "--disable_tqdm"],
                timeout=_MARKER_TIMEOUT_S,
                capture=False,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return None
        except subprocess.CalledProcessError:
            return None
        stem = src.stem
        md_files = list(Path(td).rglob(f"{stem}.md"))
        if not md_files:
            md_files = list(Path(td).rglob("*.md"))
        if not md_files:
            return None
        text = md_files[0].read_text(encoding="utf-8", errors="replace")
        pages_seen: set[int] = set()

        def _sub(m: re.Match) -> str:
            n = int(m.group(1))
            pages_seen.add(n)
            return f"<!-- PAGE:{n} -->"

        text = re.sub(r"\{(\d+)\}-{3,}", _sub, text)
        if not pages_seen:
            json_files = list(Path(td).rglob(f"{stem}.json"))
            if json_files:
                try:
                    data = json.loads(json_files[0].read_text(encoding="utf-8"))
                    pages_total = len(data.get("pages", [])) or None
                    if pages_total:
                        return text, pages_total
                except (json.JSONDecodeError, OSError):
                    pass
            return None
        return text, max(pages_seen)


def _pdftotext_convert(src: Path) -> tuple[str, int] | None:
    try:
        result = _run_pgroup(
            [PDFTOTEXT_BIN, "-layout", str(src), "-"],
            timeout=600,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None
    if result.returncode != 0:
        return None
    raw = result.stdout.decode("utf-8", errors="replace")
    pages = raw.split("\f")
    out_lines: list[str] = []
    for i, page in enumerate(pages, start=1):
        if not page.strip():
            continue
        out_lines.append(f"<!-- PAGE:{i} -->")
        out_lines.append(page.rstrip())
    return "\n".join(out_lines), max(1, len(pages))


def _pandoc_convert(src: Path) -> tuple[str, int] | None:
    try:
        result = _run_pgroup(
            [PANDOC_BIN, "-t", "plain", "--wrap=none", str(src)],
            timeout=600,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.decode("utf-8", errors="replace"), 0


def _usable_char_count(text: str) -> int:
    """Count non-whitespace chars outside of <!-- PAGE:N --> markers."""
    return len(re.sub(r"<!-- PAGE:\d+ -->", "", text).strip())


def convert_to_markdown(
    src: Path,
    cache_dir: Path,
    *,
    force: bool = False,
) -> ConversionMeta:
    """Convert `src` to markdown, caching the output.

    Returns `ConversionMeta`. Raises `RuntimeError` if all converters fail.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_md = cache_dir / f"{src.stem}.md"
    cache_meta = cache_dir / f"{src.stem}.meta.json"

    src_sha = _sha256(src)

    if not force and cache_md.exists() and cache_meta.exists():
        try:
            meta = json.loads(cache_meta.read_text())
            if meta.get("sha256") == src_sha:
                return ConversionMeta(**meta)
        except (json.JSONDecodeError, OSError, TypeError):
            pass

    ext = src.suffix.lower()
    result: tuple[str, int] | None = None
    converter = ""
    if ext == ".pdf":
        # Try pdftotext first: fast (~seconds), tiny memory, handles every
        # PDF that has an embedded text layer — which is the overwhelming
        # majority. Marker is opt-in (ENABLE_MARKER_OCR=1) because its
        # PyTorch model alone can thrash a 16GB machine.
        result = _pdftotext_convert(src)
        converter = "pdftotext"
        if result is None or _usable_char_count(result[0]) < 500:
            marker_result = _marker_convert(src)
            if marker_result is not None:
                result = marker_result
                converter = "marker"
    elif ext == ".epub":
        result = _pandoc_convert(src)
        converter = "pandoc"
    else:
        result = _pandoc_convert(src)
        converter = "pandoc"

    if result is None:
        raise RuntimeError(f"no converter succeeded for {src}")

    text, pages_total = result
    # Sanity floor: if every converter produced essentially no text (e.g.,
    # scanned PDF where marker OCR also failed), raise so the book lands
    # in `failed` with a clear 'needs OCR' message rather than silently
    # caching an empty file and producing a stub-only wiki page downstream.
    usable_chars = _usable_char_count(text)
    if usable_chars < 500:
        raise RuntimeError(
            f"{converter} extracted only {usable_chars} usable chars from "
            f"{src.name} (pages_total={pages_total}) — likely a scanned/"
            f"image-only PDF that requires manual OCR"
        )
    lang = _detect_language(text)
    cache_md.write_text(text, encoding="utf-8")
    meta = ConversionMeta(
        converter=converter,
        pages_total=pages_total or None,
        sha256=src_sha,
        language=lang,
        source_path=str(src),
        cache_path=str(cache_md),
    )
    cache_meta.write_text(
        json.dumps(meta.__dict__, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return meta
