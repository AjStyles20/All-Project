"""Text extraction with provenance (architecture proposal: Document Ingestion).

TXT/Markdown, DOCX and PPTX use only the standard library (they are zip files of XML); PDF
uses pypdf. Uploads are untrusted: size, type, zip-entry count and uncompressed size are
limited, and nothing is written to disk.
"""
import io
import re
import zipfile
from dataclasses import dataclass
from xml.etree import ElementTree

MAX_UPLOAD = 10 * 1024 * 1024
MAX_UNZIPPED = 50 * 1024 * 1024
MAX_ENTRIES = 2000
ALLOWED = {".txt", ".md", ".docx", ".pptx", ".pdf"}

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


class IngestError(Exception):
    pass


@dataclass(frozen=True)
class Piece:
    locator: str     # "paragraph 4", "slide 2", "page 3"
    text: str


def extract(filename: str, data: bytes) -> list[Piece]:
    if len(data) > MAX_UPLOAD:
        raise IngestError("File is larger than 10 MB.")
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED:
        raise IngestError("Supported files: .txt, .md, .docx, .pptx, .pdf")
    if ext in (".txt", ".md"):
        return _text(data)
    if ext == ".pdf":
        return _pdf(data)
    return _office(data, ext)


def _text(data):
    text = data.decode("utf-8", errors="replace")
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    return [Piece(f"paragraph {i}", " ".join(b.split())) for i, b in enumerate(blocks, 1)]


def _pdf(data):
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(data))
        pieces = []
        for n, page in enumerate(reader.pages, 1):
            text = " ".join((page.extract_text() or "").split())
            if text:
                pieces.append(Piece(f"page {n}", text))
        return pieces
    except Exception as exc:
        raise IngestError(f"Could not read this PDF ({type(exc).__name__}).") from exc


def _office(data, ext):
    try:
        archive = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile as exc:
        raise IngestError("This is not a valid Office file.") from exc
    infos = archive.infolist()
    if len(infos) > MAX_ENTRIES or sum(i.file_size for i in infos) > MAX_UNZIPPED:
        raise IngestError("This file expands to more than the allowed size.")
    if ext == ".docx":
        return _paragraphs(archive.read("word/document.xml"), W + "p", W + "t", "paragraph")
    slides = sorted((i.filename for i in infos if re.fullmatch(r"ppt/slides/slide\d+\.xml", i.filename)),
                    key=lambda n: int(re.search(r"(\d+)", n.rsplit("/", 1)[1]).group(1)))
    pieces = []
    for n, name in enumerate(slides, 1):
        root = _parse(archive.read(name))
        text = " ".join(t.text or "" for t in root.iter(A + "t")).strip()
        if text:
            pieces.append(Piece(f"slide {n}", " ".join(text.split())))
    return pieces


def _parse(xml_bytes):
    # Office XML never needs a DTD, so any DOCTYPE or ENTITY declaration is refused outright:
    # that closes external-entity (XXE) and entity-expansion ("billion laughs") attacks
    # without relying on parser defaults.
    upper = xml_bytes.upper()
    if b"<!DOCTYPE" in upper or b"<!ENTITY" in upper:
        raise IngestError("Office files with document type declarations are not accepted.")
    return ElementTree.fromstring(xml_bytes)


def _paragraphs(xml_bytes, para_tag, text_tag, label):
    root = _parse(xml_bytes)
    pieces = []
    for n, p in enumerate(root.iter(para_tag), 1):
        text = "".join(t.text or "" for t in p.iter(text_tag)).strip()
        if text:
            pieces.append(Piece(f"{label} {n}", " ".join(text.split())))
    return pieces


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", text)
    return [p.strip() for p in parts if len(p.strip()) > 3]
