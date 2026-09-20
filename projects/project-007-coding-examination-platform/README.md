# P001 — Intelligent Coding Examination Platform

> Historical repository identity: **Project 007**. The folder name is preserved for provenance under the canonical renumbering.

## Research contribution

The current research-critical contribution is **Evidence-Gap-Driven Programming Competence Verification (EGPCV)**: map available evidence to bounded programming-competence claims, identify unresolved evidence gaps, and select the lowest-burden admissible additional independent verification from a frozen candidate set when further evidence is justified.

Adaptive viva, browser coding, online judging, process logging, proctoring signals and generic code-conditioned questioning are not claimed as inventions.

## Experimental structure

- **B0 — Baseline 0:** final submission + ordinary tests/rubric.
- **B1 — Baseline 1:** B0 + controlled examination process/event logging; no targeted verification.
- **B2 — Baseline 2:** B1 + generic fixed viva/code explanation.
- **B3 — Baseline 3:** evidence-centered competence model without targeted verification.
- **B4 — Baseline/Method 4:** full EGPCV; evidence model + gap-driven targeted verification.

A negative or mixed result is scientifically valid. A working prototype does not prove that B4 is superior.

## Current implementation stage

Research-critical implementation is active on `p001-egpcv-implementation` and reviewed through draft PR #17.

Current verified software checkpoint:
- bounded domain model and SQLite persistence;
- append-only evidence-state history interface;
- CC3 Test Design evidence evaluation;
- EG-T3 evidence-gap detection;
- admissibility/sufficiency-before-burden probe selection;
- structured VP-CC3-02 development response evaluation;
- persistent CASE-DEV-003 B4 vertical slice;
- guard/constraint/rollback tests.

GitHub Actions run #26 on 20 September 2026 executed the current P001 suite successfully: **37 passed, 0 failed**. This is software verification for the tested development scope, not research validation.

## Integrity boundary

An observed event is not automatically misconduct. Competence evidence and integrity observations remain separate. Consequential misconduct decisions require authorized human review under the applicable **Examination Capability Contract (ECC)**.

## Deliberately deferred

The research-critical prototype does not currently prioritize full registration, payments, course management, webcam proctoring, AI-code detection, full browser lockdown, full IDE functionality, live invigilation, multi-language breadth or production deployment.

## Scientific status

The competence ontology, support rules, assessor protocol, final probe library, B2 fixed viva, held-out evaluation corpus and numerical decision thresholds still require pilot/independent validation. No experimental superiority, authorship-proof or perfect cheating-detection claim is authorized.
