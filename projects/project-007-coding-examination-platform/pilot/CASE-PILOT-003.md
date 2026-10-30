# CASE-PILOT-003 — Evidence Bundle v1.0

**Corpus:** PILOT-CC3-v1-candidate
**Claim:** CC3 — Test Design
**Status:** constructed dry-run boundary case; not real-student evidence.

## Frozen task

Use the same `count_even(values)` specification and submitted artifact family as CASE-PILOT-001 so that assessor attention remains on the evidence-state boundary rather than task complexity.

## Independent response condition

The exact frozen constructed response shown to the assessor is:

> Input: `[2, 3]`. Expected output: `2`. Reason: this checks that the function can handle both an even and an odd number.

The input is relevant, but the expected output is incorrect (`count_even([2, 3])` should return `1`). The response therefore intentionally contains meaningful but incomplete/incorrect evidence. This explanatory construction note must be hidden from the assessor until after independent judgment.

The literal response above is frozen for v1.0 and must not be edited after an assessor judgment.

## Intended stress

This case is designed to test whether assessors can operationally distinguish meaningful but incomplete independent test-design evidence (candidate PARTIAL) from evidence too weak to resolve anything (UNRESOLVED).

## Rule

The label PARTIAL is a construction expectation only. Assessors must independently judge the frozen response using the candidate rubric and may disagree. Any disagreement is preserved as pilot evidence about rubric clarity.

## Safety/provenance

This is a constructed response, not a quotation or observation from a student.
