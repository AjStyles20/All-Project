# Project 001 Provider Selection — 2026-09-08

## Status
A2 implementation decision for the first optional real-provider adapter. Core provider-neutral interfaces remain authoritative and unchanged.

## Decision
Implement OpenAI as the first optional external provider adapter while preserving the ability to add/replace providers later.

Initial defaults when explicitly enabled through trusted environment configuration:
- text generation/evaluation: `gpt-5.6-luna`
- embeddings: `text-embedding-3-small`

These are configuration defaults, not hard-coded architectural dependencies. Model IDs must be overridable through trusted server environment variables.

## Rationale
### Cost
Official OpenAI model documentation checked 2026-09-08 reports:
- `gpt-5.6-luna`: $0.20 per 1M input tokens, $1.20 per 1M output tokens.
- `text-embedding-3-small`: $0.02 per 1M input tokens.

This is appropriate for a cost-sensitive prototype that may generate many short reviewer questions and structured feedback responses.

### Structured output
Current OpenAI model documentation reports structured-output support for GPT-5.6 Luna. Project 001's evaluator benefits from schema-constrained output because its five-category rubric must be validated before persistence.

### Local hardware
External inference avoids requiring a large local model. Project 001 retains a lexical-only/no-provider fallback and does not require AI to start the application.

### Data handling
OpenAI's published enterprise/API privacy information states API business data is not used for training by default. Standard API inputs/outputs are generally removed from OpenAI systems after 30 days unless legally required; eligible customers may request zero-data-retention controls.

This does not mean all uploaded content should be sent automatically. Project 001 will send only the bounded evidence needed for the requested operation, and external-provider use must be visible/configured explicitly.

## Alternatives Reviewed
### Google Gemini
Current Gemini documentation supports JSON-schema structured output and offers free/paid tiers plus text embeddings. It remains a valid future adapter.

Privacy consideration: current Gemini pricing/billing documentation states content in the free tier may be used to improve Google products, whereas paid-service content is not used for product improvement. Because Project 001 can contain private project documents, this is a material default-selection consideration.

### Mistral
Current Mistral documentation provides embedding APIs and structured-output support. It remains a valid future adapter and may be useful where regional inference or alternative pricing is preferred.

## Security Requirements for the First Adapter
- API key only from a trusted server environment variable/secret store.
- Never accept API keys from a normal browser form.
- Never commit `.env` containing real keys.
- Never log Authorization headers/API keys.
- Fixed HTTPS API host in code/configuration; do not let normal users supply arbitrary outbound URLs.
- Explicit connect/read/write/pool timeouts.
- Bound prompt/evidence/output size before requests.
- No provider tools, web search, file search, code execution, computer use, or arbitrary function calls for Project 001 question/evaluation requests.
- Structured-output response is still locally validated; provider schema compliance is not trusted as the only validation layer.
- Provider errors mapped to controlled application errors.
- No automatic retry storm; retries, if used, must be small and bounded.
- Usage/provider/model metadata may be recorded, but secrets and raw Authorization material must not be stored.
- Application remains functional in non-AI lexical/document mode when provider configuration is absent.

## Live Verification Boundary
Implementation with mocked HTTP transport does not establish live-provider success. `LIVE VERIFIED` requires an actual authenticated request using AJ-controlled credentials or another authorized test credential, with secret values kept out of logs/evidence.

## Evidence URLs Checked
- OpenAI GPT-5.6 Luna model documentation
- OpenAI text-embedding-3-small model documentation
- OpenAI enterprise/API privacy documentation
- Google Gemini structured-output documentation
- Google Gemini pricing/billing/data-use documentation
- Mistral embeddings and structured-output documentation

Exact external pricing/features are time-sensitive and must be rechecked before production deployment or major cost claims.
