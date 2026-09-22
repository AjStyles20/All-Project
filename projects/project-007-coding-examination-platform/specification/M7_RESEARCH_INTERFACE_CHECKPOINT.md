# P001 M7 Research Interface Checkpoint

**Milestone:** M7 — Minimal Research Interface
**Status:** COMPLETE FOR DEVELOPMENT / NOT YET PILOT-AUTHORIZED
**Scope:** bounded CC3 / EG-T3 research slice.

## 1. Closure conclusion

M7 is complete as a minimal research-facing interface. The implemented surface is sufficient to inspect a persisted comparative experiment, export its machine-readable record, inspect the bounded audit trail, and enter one independently sourced reference judgment under the experiment's frozen claim/rubric constraints.

M7 completion does **not** authorize a real student pilot. Pilot authorization belongs to M8 and requires the entry conditions below.

## 2. Implemented research interface

- GET /health — bounded service health.
- GET /research/experiments/{id} — experiment identity, B0-B4 observations, raw burden, reference status and missing components.
- GET /research/experiments/{id}/export — deterministic machine-readable export.
- GET /research/experiments/{id}/audit — case/claim-bounded decision trace.
- POST /research/experiments/{id}/reference — one independent assessor judgment; claim is experiment-bound, rubric must match, and an existing reference cannot be overwritten through the endpoint.

The interface deliberately does not expose general evidence mutation, method-result editing, misconduct decisions, marks, authentication/course management, or a student examination portal.

## 3. M7 closure evidence

Tests cover truthful incomplete records, machine-readable export, unknown-run 404 behavior, audit claim bounding, reference claim binding, rubric mismatch rejection, and reference overwrite rejection.

GitHub Actions run #198 on 20 September 2026: **107 passed, 0 failed, 2 warnings in 2.06 seconds**.

This is software verification, not research validation.

## 4. M8 pilot entry audit

Required before a real pilot:
1. Select/version the actual pilot corpus; development fixtures cannot silently become pilot evidence.
2. Operationalize the independent Computer Science assessor procedure and preserve disagreement.
3. Version the pilot CC3 rubric, especially PARTIAL versus UNRESOLVED.
4. Check/freeze the pilot B2 fixed-viva wording/order and CC3 scoring rule.
5. Freeze the pilot B4 probe catalogue/evaluator version; VP-CC3-03 remains non-executable unless an evaluator is frozen.
6. Define how verification seconds are measured; missing time is never inferred as zero.
7. Define identifiers, consent/ethics requirements if real students are involved, access, retention and de-identification.
8. Predefine failure/deviation logging for unavailable evaluators, missing evidence, human escalation and assessor disagreement.
9. Do not execute arbitrary untrusted candidate code through this API; secure sandboxing is absent.
10. Predefine pilot descriptive outputs used to decide whether the procedure is clear enough for M9 Method Freeze; do not choose final success thresholds after seeing favorable outcomes.

## 5. Not automatically required for the bounded pilot

A polished student portal, course/payment management, webcam proctoring, automatic cheating detection, AI-code detection, full integrity workflow and multi-language IDE are not required to test bounded EGPCV.

If B1 in the pilot relies on real process evidence, however, an ethically and operationally defined process-capture source must exist. Synthetic development process evidence must not be described as observed student behavior.

## 6. M8 objective

M8 tests whether the **measurement procedure is usable and interpretable**, not whether EGPCV has already won. It should expose assessor/rubric ambiguity, verify that B2 stays fixed, verify that B4 obeys its frozen selection policy, establish reliable burden capture, and confirm that audit/export records reconstruct what happened.

Any material pilot-driven change creates a new version and prevents pre-change pilot runs from being presented as held-out final evidence.

## 7. Gate

**M7 → CLOSED.**

**M8 → PREPARATION AUTHORIZED; real pilot execution remains blocked until the ten pilot-entry requirements above are satisfied or explicitly scoped out with documented rationale.**
