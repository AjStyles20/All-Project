# OpenAI API B2 Execution Route

This is a prospective execution adapter for the already-frozen first-wave B2 experiment. It does not change the manifest, evidence packets, prompts, run IDs, scoring rules or reviewer protocol.

The official OpenAI API can perform text generation through the Responses API. The API key must be supplied through the environment and must never be committed to this repository.

## Qualification rule

Before consuming any experimental run ID, perform a non-experimental API smoke test outside the B2 manifest and confirm that the environment exposes enough provenance to preserve at least the requested model, returned model/version identifier where provided, provider response ID, timestamp, exact prompts and full raw output.

If qualification fails, do not run B2.

## First-wave IDs

Only these IDs are eligible for the first-wave runner:

- B2-A-001
- B2-A-002
- B2-A-003
- B2-NC01-001
- B2-NC01-002
- B2-NC01-003

The runner calls the existing repository readiness gate before any provider request. Packet mutation, an unplanned ID or a manifest mismatch must therefore fail before model execution.

## Windows setup

Install the official SDK:

`python -m pip install openai`

Set the key in the current PowerShell session without writing it into source code:

`$env:OPENAI_API_KEY="YOUR_KEY"`

Then execute one authorized run only after qualification:

`python scripts/run_b2_openai.py B2-A-001 --model <model-id>`

Preserve the complete JSON output. A technical failure is evidence about the attempt and must not be silently discarded. A retry must be recorded as a retry rather than replacing the failed attempt.

## Scientific boundary

This adapter does not make M9 complete. Successful B2 execution must still be followed by immutable run-record ingestion, atomic claim extraction, blinded independent human review, locked judgments, authorized unblinding and the predeclared comparative analysis.

Do not use ordinary interactive ChatGPT conversation text as a substitute for these controlled runs.
