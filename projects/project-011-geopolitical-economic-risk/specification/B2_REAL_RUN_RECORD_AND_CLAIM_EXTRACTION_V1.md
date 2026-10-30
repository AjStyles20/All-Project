# P003 — B2 Real Run Record and Atomic Claim Extraction Contract v1

## Status
**FROZEN BEFORE ANY REAL B2 GENERATION.**

The existing B2 adapter is only a placeholder. A real B2 experiment must create an immutable run record.

## Required run record
Preserve:
- run ID;
- evidence packet ID and SHA-256 hash;
- provider, model and model/version identifier;
- execution timestamp;
- exact system and user prompts;
- generation settings available to the researcher, including temperature/seed where applicable;
- complete raw response;
- deterministic run-record hash.

If a provider does not expose a model build, seed or another field, record it explicitly as unavailable rather than inventing a value.

## Atomic claim extraction
Reviewer scoring operates on atomic downstream claims, not an overall impression of the answer.

Each extracted claim must have:
- opaque claim ID;
- originating run ID;
- exact claim text or faithful atomic decomposition;
- claim type;
- a source span traceable to the immutable raw response.

Claim extraction must not rewrite an unsupported claim into a safer claim. Compound claims should be split when they contain independently judgeable propositions.

## Separation of roles
The person/process extracting claims must not assign SUPPORTED/UNSUPPORTED labels during extraction. Evidence judgment happens under the independent-review protocol.

## Multiple generations
The previously frozen B2 contract proposes a minimum of three generations per case to observe variability. Each generation receives the same frozen packet version and has its own immutable run record.

## Anti-cherry-picking
All predeclared generations are retained, including abstentions, weak answers and inconvenient outputs. No rerun may replace an unfavorable generation unless a documented technical failure invalidated the run; the failed record must still be preserved.

## Current boundary
This commit creates recording and validation infrastructure only. No real B2 model has been run and no empirical B2-vs-B3 result exists.
