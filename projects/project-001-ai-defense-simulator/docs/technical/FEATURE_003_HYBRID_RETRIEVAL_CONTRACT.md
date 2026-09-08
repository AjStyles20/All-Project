# Feature 003 Contract — Hybrid Retrieval Foundation

## Status
APPROVED FOR BOUNDED EXECUTION

## Purpose
Extend the existing verified SQLite FTS5 lexical retrieval with an optional semantic-vector retrieval layer while preserving inspectability, source provenance, and graceful operation when no embedding provider is configured.

## Platform / Stack
- Primary language: Python
- Backend: FastAPI
- Persistence: SQLite
- Delivery platform: web application
- Frontend impact: none required for this feature
- React: not required

## Required Behavior
1. Existing FTS5 lexical retrieval remains functional and independently inspectable.
2. Introduce an `EmbeddingProvider` interface so semantic retrieval is not hard-coded to one model/vendor.
3. Store embedding metadata separately from source chunk truth, including provider/model/version where available.
4. Hybrid ranking must expose component scores or enough metadata to explain why a result was returned.
5. When no semantic provider is configured, the system must continue operating in lexical-only mode and explicitly report that semantic retrieval is unavailable/not configured.
6. No fake or deterministic test vector may be represented as a real semantic embedding in production state.
7. Tests may use a deterministic fake provider strictly as test infrastructure.
8. Semantic retrieval must never remove source document ID, filename, locator, chunk ID, or retrieved source text from the result contract.

## Out of Scope
- Selecting a commercial embedding provider as mandatory default.
- Downloading a large local embedding model automatically.
- Dedicated vector database.
- LLM question generation.
- Answer evaluation.
- Reranking with an LLM/cross-encoder.
- UI redesign.

## Data / Persistence Requirements
Semantic index records should be tied to:
- chunk ID
- content hash
- embedding provider
- embedding model/version identifier
- vector dimension
- serialized vector representation or provider-appropriate storage
- created/updated timestamp where practical

Stale embeddings must be detectable when chunk content hash or provider/model identity changes.

## Hybrid Ranking
The first implementation should use an explicit, testable merge of lexical and semantic candidate scores rather than an opaque black-box retrieval service.

Candidate strategy:
- obtain top lexical candidates from FTS5;
- obtain top semantic candidates from the configured embedding layer;
- normalize component ranks/scores;
- combine using configurable weights;
- return component provenance such as lexical rank, semantic similarity, and final score.

Exact weighting is an A2 implementation parameter and must be documented and tested. It must not be described as optimal without evaluation evidence.

## Verification Requirements
- lexical-only regression suite remains passing;
- provider-not-configured path is explicit and functional;
- deterministic fake-provider test proves semantic candidate ordering and hybrid merge behavior;
- stale embedding detection is tested;
- workspace isolation remains intact;
- provenance survives both lexical and hybrid paths;
- malformed/mismatched vector dimensions fail safely;
- no external provider is claimed live without a verified real request.

## Completion Boundary
Feature 003 is considered implemented when hybrid-retrieval infrastructure and test-provider verification exist. It is considered LIVE VERIFIED for semantic retrieval only after at least one real embedding provider/model has been configured and successfully exercised with recorded evidence.
