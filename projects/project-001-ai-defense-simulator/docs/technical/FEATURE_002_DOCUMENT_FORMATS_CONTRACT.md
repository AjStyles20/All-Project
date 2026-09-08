# Feature 002 — Document Format Expansion Contract

## Goal
Extend Project 001 ingestion beyond UTF-8 TXT/Markdown so the system can ingest the document types most likely to contain presentation and review material while preserving truthful source provenance.

## In Scope
- PDF text extraction using `pypdf`
- DOCX paragraph extraction using `python-docx`
- PPTX slide text extraction using `python-pptx`
- source locators preserved as:
  - PDF: `page N`
  - DOCX: `paragraph N`
  - PPTX: `slide N`
- existing TXT/Markdown ingestion retained
- deterministic chunk hashing retained
- workspace-scoped lexical retrieval retained
- malformed accepted-format files fail explicitly with HTTP 422
- encrypted PDFs are rejected rather than silently misprocessed

## Out of Scope
- OCR for scanned/image-only PDFs
- extraction of images, charts, diagrams, speaker notes, comments, or embedded media
- exact visual-layout reconstruction
- DOCX physical page-number reconstruction
- password-protected Office files
- semantic/vector retrieval
- LLM question generation or answer evaluation

## Provenance Rules
A stored chunk must never claim a locator that is more precise than the parser can support.

- PDF text is associated with the page from which it was extracted.
- PPTX text is associated with its source slide.
- DOCX is associated with document paragraph order; physical page boundaries are not claimed because Word pagination is renderer-dependent and not reliably available from the file structure alone.
- Empty pages/slides/paragraphs may be skipped, but no content from one page/slide is relabeled as another.

## Accepted File Types
`.txt`, `.md`, `.pdf`, `.docx`, `.pptx`

## Acceptance Criteria
1. Valid PDF with extractable text uploads successfully and search results retain a `page N` locator.
2. Valid DOCX uploads successfully and search results retain a `paragraph N` locator.
3. Valid PPTX uploads successfully and search results retain a `slide N` locator.
4. Feature 001 TXT/Markdown tests continue to pass.
5. Invalid PDF/DOCX/PPTX input returns a controlled extraction failure rather than creating a false successful document.
6. Files with no extractable text return HTTP 422.
7. No external AI provider is required.
8. Full test suite passes before merge consideration.

## Verification Boundary
Passing extraction tests does not establish OCR support, fidelity for complex layouts, or comprehensive support for every legal PDF/DOCX/PPTX construct. Those claims require separate evidence.