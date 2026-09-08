# Feature 001 Contract — Document Ingestion + Provenance-Aware Retrieval

## Status
APPROVED FOR IMPLEMENTATION

## Objective
Create the first verifiable vertical slice of Project 001: ingest supported source files, preserve source provenance at chunk level, persist the extracted content in SQLite, and retrieve relevant chunks through inspectable lexical search.

## In Scope
- FastAPI application skeleton.
- SQLite database initialization.
- Workspace and source-document persistence sufficient for this feature.
- File upload validation.
- TXT and Markdown ingestion in the first implementation.
- Parser interface designed so PDF, DOCX, and PPTX can be added without changing the domain model.
- Deterministic text chunking.
- Chunk provenance: source document ID, filename, chunk index, source locator/section when known, content hash, extraction status.
- SQLite FTS5 lexical index where available.
- Retrieval endpoint returning ranked chunks plus provenance.
- Tests for chunking, hashing, persistence, validation, and lexical retrieval.

## Explicitly Out of Scope
- LLM question generation.
- Embedding generation or semantic retrieval.
- External AI provider calls.
- Speech input/output.
- Automated answer evaluation.
- PDF/DOCX/PPTX parsing until the text/Markdown path is independently verified.
- User authentication.
- Multi-user collaboration.

## API Contract
### GET /health
Returns application health and database status without invented provider status.

### POST /api/workspaces
Creates a workspace.

### POST /api/workspaces/{workspace_id}/documents
Multipart upload. Initially accepts `.txt` and `.md` only.

Response must include:
- document ID
- original filename
- content hash
- extraction status
- chunk count
- warnings, if any

### GET /api/workspaces/{workspace_id}/search?q=...
Returns ranked matching chunks with:
- chunk ID
- document ID
- filename
- locator
- chunk index
- excerpt/content
- rank/score where the retrieval implementation exposes one

## Validation Rules
- Reject empty filenames.
- Reject unsupported extensions.
- Reject empty files.
- Apply a configurable upload-size limit.
- Never expose server filesystem paths in API responses.
- Preserve the original filename as metadata but generate internal storage identifiers independently.
- Do not claim content was extracted if parsing fails.

## Chunking Rules — First Implementation
Use deterministic paragraph-aware chunking with a target character size and bounded overlap. The algorithm must be simple enough to explain and deterministic under test.

Every chunk stores:
- stable database ID
- document ID
- ordinal chunk index
- source locator (e.g. `paragraphs 1-4` where applicable)
- text content
- SHA-256 content hash

## Persistence
SQLite tables for this slice:
- `workspaces`
- `source_documents`
- `document_chunks`

FTS virtual table may mirror searchable chunk fields. Schema creation must be idempotent.

## Verification Acceptance Criteria
1. Two identical uploads produce identical document content hashes.
2. Unsupported extensions are rejected.
3. Empty files are rejected.
4. Stored chunks preserve correct document linkage and chunk order.
5. Search results do not cross workspace boundaries.
6. A known fixture query returns the expected relevant chunk.
7. Provenance fields are present for every returned result.
8. Database initialization can be repeated without failure.
9. No external LLM/provider is required for the tests to pass.
10. Documentation does not describe PDF/DOCX/PPTX ingestion as implemented until those parsers are actually added and verified.

## Handoff Requirement
Engineering must report implemented files, tests run, failures encountered, corrections, known limitations, and any architecture deviation. Independent Verification must challenge the slice separately before `VERIFIED` status.
