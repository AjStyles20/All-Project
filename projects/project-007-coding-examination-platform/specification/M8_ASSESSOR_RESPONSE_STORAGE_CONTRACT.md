# P001 M8 — Assessor Response Storage Contract v1

Actual assessor responses are stored as versioned JSON research records using schema M8-ASSESSOR-RESPONSE-v1. File identity is case ID plus non-identifying assessor code. Original records are write-once: an existing case+assessor response must not be overwritten.

Corrections after submission must be preserved as a separately versioned research record or explicit amendment in a later protocol; they must not silently replace the original. The current writer therefore fails on an existing target.

The provided JSON file is a schema/example only. Placeholder values are not observations and must never be committed as if an assessor supplied them.

This storage contract remains separate from experiment reference-judgment persistence. Reference derivation, if justified after independent judgments and ambiguity review, is a later methodological decision.
