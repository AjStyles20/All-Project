# P001 M8 — Assessor Judgment Ingestion Contract v1

Purpose: define how actual independent assessor responses are represented after blinded administration. The software must not invent missing judgments, convert construction expectations into human judgments, or silently reconcile disagreement.

Required fields mirror the response form: assessor code, case ID, evidence state, three CC3 dimension judgments, rationale, boundary confidence/ambiguity, additional-evidence requirement, human-review concern, and independence confirmation.

Rules: assessor code is non-identifying; independence confirmation is mandatory; a non-confident judgment must name the ambiguous boundary; requested additional evidence must be described; a human-review concern must include its reason. Comparison requires two distinct assessor codes for the same case.

Comparison output is descriptive only: exact state agreement and agreement count across the three CC3 dimensions. It does not choose a winner, manufacture consensus, or replace the preserved original responses. Chance-corrected agreement statistics remain deferred until sample/category distribution justifies them.

This contract creates no assessor data. It becomes populated only from responses actually supplied by independent assessors.
