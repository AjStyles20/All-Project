# P003 — Real B2 Execution Handoff v1

## Status
**EXTERNAL EXECUTION HANDOFF — NO MODEL OUTPUTS RECORDED HERE.**

M9 software readiness is closed. The next scientific action is to execute the predeclared B2 runs in a controlled model environment and preserve the returned metadata and raw text.

## First-wave runs — execute before analysis
- B2-A-001
- B2-A-002
- B2-A-003
- B2-NC01-001
- B2-NC01-002
- B2-NC01-003

Use `P003-B2-MANIFEST-v1`. For every run, call the repository's `prepare_run(...)` gate first and use the returned frozen system prompt and user prompt unchanged.

## Second wave — keep separate
- B2-D-001
- B2-D-002
- B2-D-003

Use `P003-B2-SECOND-WAVE-MANIFEST-v1`. Do not pool these into the original six-run first wave.

## Required execution record
For each attempted run preserve:
- predeclared run ID;
- packet ID and packet SHA-256;
- provider;
- requested model identifier;
- model identifier/version returned by provider where available;
- provider response ID/request ID where available;
- execution timestamp;
- exact system prompt;
- exact user prompt;
- temperature/top-p or other sampling controls actually supported;
- seed only if the provider/model actually supports and returns/accepts one; otherwise record `UNSUPPORTED/NOT_SET`, never invent it;
- completion status/error;
- complete raw response text.

## Important API compatibility rule
Do not require a `seed` parameter from an execution provider unless that provider/model documents support for it. Reproducibility here means preserving the exact request, returned model metadata, raw response, packet hash and run lineage; it does not mean claiming bit-for-bit deterministic generation.

## OpenAI Responses API note
Current official Responses API documentation exposes model, instructions/input, temperature, top_p, metadata and response identifiers/status. The execution adapter should record only controls actually exposed by the selected endpoint/model and preserve the response object metadata needed for traceability.

## Failure handling
A technical failure is not silently replaced or deleted.
Record the attempted run ID, provider/model, timestamp, request configuration, error/status and whether a retry occurred. A retry must receive a distinct attempt record while retaining the originally predeclared experimental run identity.

## No-analysis rule during execution
Do not inspect early generations and then:
- alter prompts;
- change packet evidence;
- change model/settings for later runs;
- discard an inconvenient valid generation;
- add a new favourable case;
- modify claim-label definitions.

If an execution defect forces a protocol change, stop the affected wave, version the amendment, document the reason and determine which runs must be restarted.

## After execution
1. Build immutable `B2RunRecord` objects.
2. Verify hashes and preserve raw outputs.
3. Extract atomic claims without support labels.
4. Validate claim source spans against raw responses.
5. Blind claims.
6. Generate/hash reviewer packages.
7. Obtain independent reviews.
8. Lock reviewer batches before unblinding.
9. Pass the comparative-analysis authorization gate.
10. Only then calculate the predeclared comparative metrics.

## Scientific boundary
Completion of model calls alone does not establish B2-vs-B3 performance. It only satisfies the missing model-output component of the evaluation evidence chain.
