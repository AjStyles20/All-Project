# Feature 007 Contract — Secure Optional Real-Provider Adapter

## Status
APPROVED FOR BOUNDED EXECUTION (A2)

## Purpose
Add the first production-shaped external AI adapter without changing Project 001's provider-neutral architecture or requiring external AI for basic application startup/document retrieval.

## First Adapter
OpenAI API, selected as the first optional adapter after a 2026-09-08 provider review.

Trusted server defaults when explicitly enabled:
- question/evaluation model: `gpt-5.6-luna`
- embedding model: `text-embedding-3-small`

Both remain overridable through trusted environment configuration.

## Interfaces Implemented
- `EmbeddingProvider`
- `QuestionGenerator`
- `AnswerEvaluator`

The adapter must fit the existing interfaces. Business/retrieval/evaluation code must not import vendor-specific response objects.

## Security Requirements
1. Provider disabled by default.
2. API key read only from `P001_OPENAI_API_KEY` in server environment.
3. Explicit enabling flag required: `P001_OPENAI_ENABLED=1`.
4. If enabled without a key, startup/configuration must fail explicitly rather than silently downgrade while claiming configured AI.
5. Fixed HTTPS provider host; normal users cannot supply outbound URLs.
6. No provider tools, web search, file search, code execution, computer use, MCP, or function tools in Project 001 calls.
7. Responses request uses `store: false` where supported to minimize provider-side application response storage.
8. External calls use bounded timeouts.
9. No unbounded automatic retry loops.
10. Provider HTTP/body failures map to controlled exceptions and must not expose API keys or raw Authorization material.
11. Inputs remain bounded by existing Project 001 evidence/topic/answer limits.
12. Evaluation uses structured JSON-schema output plus existing local validation. Provider schema compliance is not trusted as the sole validation boundary.
13. Embedding response count/dimensions/finite values remain locally validated by the existing embedding layer.
14. Provider/model metadata may be persisted; API secrets must never be persisted.
15. No browser form or API route accepts an API key.
16. Application remains usable for workspace/document/lexical operations when provider is disabled.

## Configuration
- `P001_OPENAI_ENABLED` — `0`/unset by default; `1` enables configuration.
- `P001_OPENAI_API_KEY` — required only when enabled.
- `P001_OPENAI_TEXT_MODEL` — optional trusted override; default `gpt-5.6-luna`.
- `P001_OPENAI_EMBEDDING_MODEL` — optional trusted override; default `text-embedding-3-small`.
- `P001_OPENAI_TIMEOUT_SECONDS` — optional bounded trusted override.

No API base URL override is exposed in this first adapter. This avoids turning configuration/user input into an SSRF-capable arbitrary outbound destination. Additional providers get explicit adapters.

## Provider Request Design
### Questions
- trusted application policy sent separately from evidence content;
- question topic/reviewer/evidence serialized as untrusted input;
- plain text output only;
- output revalidated by existing `validate_generated_question` path.

### Evaluation
- trusted evaluator policy sent separately;
- question/answer/evidence serialized as untrusted input;
- structured JSON schema requires exactly the five approved qualitative feedback categories/status vocabulary;
- parsed response converted into existing `EvaluationResult` / `FeedbackItem` types;
- existing local validation runs before persistence.

### Embeddings
- bounded list of strings sent to embeddings endpoint;
- float embeddings only;
- count and dimensions validated locally.

## Verification
Without a real API key, CI must verify using `httpx.MockTransport` or equivalent:
- key absent/disabled configuration behavior;
- enabled-without-key failure;
- fixed endpoint usage;
- Authorization header presence without leaking it to error strings/logs;
- timeout configuration bounds;
- question payload separates trusted instructions and untrusted evidence;
- `store: false` and no tools in generation/evaluation calls;
- structured evaluation schema requested;
- successful response parsing;
- malformed JSON/output fails closed;
- HTTP 401/429/500 fail with controlled errors;
- embedding result count/dimension validation remains intact;
- complete existing regression suite passes;
- dependency audit passes.

## Live Verification Boundary
Mocked CI verifies the adapter implementation, not OpenAI availability or account configuration. `LIVE VERIFIED` requires an actual authenticated request using authorized credentials. Secret material must never be copied into test evidence, logs, screenshots, commits, or conversation messages.
