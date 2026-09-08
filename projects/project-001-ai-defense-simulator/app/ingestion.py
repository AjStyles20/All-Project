from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re

SUPPORTED_EXTENSIONS = {".txt", ".md"}


@dataclass(frozen=True)
class TextChunk:
    index: int
    locator: str
    text: str
    content_hash: str


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def decode_text_file(data: bytes) -> str:
    """Decode UTF-8 text input. Invalid input fails explicitly instead of guessing."""
    return data.decode("utf-8")


def chunk_text(
    text: str,
    *,
    target_chars: int = 1200,
    overlap_chars: int = 150,
) -> list[TextChunk]:
    """Create deterministic paragraph-aware chunks with bounded character overlap."""
    if target_chars <= 0:
        raise ValueError("target_chars must be greater than zero")
    if overlap_chars < 0:
        raise ValueError("overlap_chars cannot be negative")
    if overlap_chars >= target_chars:
        raise ValueError("overlap_chars must be smaller than target_chars")

    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        return []

    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r"\n\s*\n+", normalized)
        if paragraph.strip()
    ]

    staged: list[tuple[int, int, str]] = []
    current: list[str] = []
    current_len = 0
    start_paragraph = 1

    for paragraph_number, paragraph in enumerate(paragraphs, start=1):
        separator_len = 2 if current else 0
        incoming_len = len(paragraph) + separator_len

        if current and current_len + incoming_len > target_chars:
            body = "\n\n".join(current).strip()
            staged.append((start_paragraph, paragraph_number - 1, body))

            # Restrict overlap to the immediately preceding paragraph. This keeps
            # the locator truthful even when the previous chunk contains several
            # short paragraphs; a raw tail of the whole chunk could otherwise
            # include text from an earlier paragraph that the locator omits.
            previous_paragraph = current[-1]
            overlap = previous_paragraph[-overlap_chars:].strip() if overlap_chars else ""
            current = [overlap, paragraph] if overlap else [paragraph]
            current_len = sum(len(item) for item in current) + 2 * (len(current) - 1)
            start_paragraph = paragraph_number - 1 if overlap else paragraph_number
        else:
            if not current:
                start_paragraph = paragraph_number
            current.append(paragraph)
            current_len += incoming_len

    if current:
        body = "\n\n".join(current).strip()
        staged.append((start_paragraph, len(paragraphs), body))

    chunks: list[TextChunk] = []
    for index, (start, end, body) in enumerate(staged):
        locator = f"paragraph {start}" if start == end else f"paragraphs {start}-{end}"
        chunks.append(
            TextChunk(
                index=index,
                locator=locator,
                text=body,
                content_hash=sha256_text(body),
            )
        )
    return chunks
