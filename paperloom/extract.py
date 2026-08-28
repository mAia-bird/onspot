"""Pull a short text preview out of a file, to feed the classifier.

Standard library only, best-effort by design:

  * plain-text formats (txt, md, csv, json, html, …) are read directly;
  * PDFs get a best-effort text extraction (works well for "digital" PDFs with
    a text layer; a pure scan yields little — see the README note on vision);
  * images and unknown binaries return no text, so classification falls back to
    the file name (or a vision model, if one is configured).

Nothing here needs the network or any third-party package.
"""
from __future__ import annotations

import re
import zlib
from pathlib import Path

TEXT_SUFFIXES = {".txt", ".md", ".markdown", ".csv", ".tsv", ".json", ".log",
                 ".html", ".htm", ".xml", ".rtf", ".ini", ".yaml", ".yml"}
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
PREVIEW_CHARS = 4000

_PDF_TEXT_OP = re.compile(rb"\((?:\\.|[^\\()])*\)|\<[0-9A-Fa-f\s]+\>")


def _decode_pdf_string(token: bytes) -> str:
    if token.startswith(b"<"):  # hex string
        hexs = re.sub(rb"\s+", b"", token[1:-1])
        try:
            return bytes.fromhex(hexs.decode("ascii")).decode("latin-1", "ignore")
        except ValueError:
            return ""
    body = token[1:-1]
    body = body.replace(b"\\(", b"(").replace(b"\\)", b")").replace(b"\\\\", b"\\")
    body = body.replace(b"\\n", b"\n").replace(b"\\r", b"\r").replace(b"\\t", b"\t")
    return body.decode("latin-1", "ignore")


def _extract_pdf(path: Path, limit: int = PREVIEW_CHARS) -> str:
    """Best-effort PDF text: inflate Flate streams, read text-showing operators."""
    try:
        data = path.read_bytes()
    except OSError:
        return ""
    chunks: list[bytes] = []
    # Decompress every FlateDecode stream we can find; also keep raw streams.
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", data, re.S):
        raw = m.group(1)
        try:
            chunks.append(zlib.decompress(raw))
        except zlib.error:
            chunks.append(raw)
    if not chunks:
        chunks = [data]

    out: list[str] = []
    for blob in chunks:
        for tok in _PDF_TEXT_OP.findall(blob):
            s = _decode_pdf_string(tok)
            if s.strip():
                out.append(s)
        if sum(len(x) for x in out) > limit:
            break
    text = " ".join(out)
    text = re.sub(r"[ \t]+", " ", text).strip()
    return text[:limit]


def extract_preview(path: Path, limit: int = PREVIEW_CHARS) -> str:
    """Return a text preview of ``path`` for classification (may be empty)."""
    suffix = path.suffix.lower()
    if suffix in TEXT_SUFFIXES:
        try:
            return path.read_text(encoding="utf-8", errors="ignore")[:limit].strip()
        except OSError:
            return ""
    if suffix == ".pdf":
        return _extract_pdf(path, limit)
    return ""  # images / unknown binaries: no cheap text


def is_image(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_SUFFIXES
