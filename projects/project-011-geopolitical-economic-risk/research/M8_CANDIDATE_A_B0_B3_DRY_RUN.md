# P003 M8 — Candidate A Same-Information B0-B3 Dry Run

## Status
**DRY RUN ONLY. B2 IS NOT YET A REAL LLM/RAG BASELINE.**

Candidate A now has a same-case comparison fixture:

| Baseline | Bounded output |
|---|---|
| B0 News/GPR signal | VERIFIED_EVENT_ONLY |
| B1 Event + Exposure | EXPOSURE_IDENTIFIED |
| B2 Narrative placeholder | MECHANISM_SUPPORTED_SCENARIO |
| B3 ETEC | MECHANISM_SUPPORTED_SCENARIO; stops before T5 |

This table is a structural dry run, not an empirical performance result.

The important current observation is not that B3 is "better" than B2. In this case the frozen B2 placeholder and B3 can reach the same broad directional scenario class. B3 differs by carrying typed evidence transitions, counterevidence constraints, provenance/auditability and an explicit T5 ceiling.

## What remains before comparative evidence exists
1. Replace B2 placeholder with a frozen real LLM/RAG procedure.
2. Define an independent reference judgment for unsupported downstream claims.
3. Have reviewers judge claims without using B3 as the answer key.
4. Add multiple mechanism-diverse historical cases and at least one negative control.
5. Predeclare unsupported-claim and structural-abstention scoring.

Until those are done, no B3-vs-B2 superiority claim is permitted.
