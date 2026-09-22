# P001 — Intelligent Coding Examination Platform

> Historical repository identity: **Project 007**. The folder name is preserved for provenance under canonical renumbering.

## Research contribution
The research-critical contribution is **Evidence-Gap-Driven Programming Competence Verification (EGPCV)**: map admissible evidence to bounded competence claims, identify unresolved evidence gaps, and select the lowest-burden additional independent verification from a frozen set only after the candidate is admissible, potentially sufficient, executable, and unused.

Adaptive viva, browser coding, online judging, process logging, proctoring signals and generic code-conditioned questioning are not claimed as inventions.

## B0-B4 experiment
- **B0:** final submission + ordinary tests/rubric.
- **B1:** B0 + controlled process/event evidence.
- **B2:** B1 + pre-frozen generic fixed viva; not gap-selected.
- **B3:** evidence-centered competence model without targeted verification.
- **B4:** full EGPCV with gap-driven targeted verification.

All methods are compared on the same eligible case/claim under frozen evidence-access boundaries. Fixed-viva evidence is B2-only; targeted-verification evidence is B4-only. A negative or mixed result is valid science.

## Current implementation
Research-critical implementation is active on `p001-egpcv-implementation` through draft PR #17.

Implemented scope includes:
- domain model, invariants and SQLite persistence;
- append-only evidence-state history;
- bounded CC3 Test Design evaluator and EG-T3 gap detector;
- auditable B4 probe selection and verification;
- executable-probe safeguard;
- generic stop rule and human-review terminal state;
- immutable audit trace and probe-candidate dispositions;
- B0-B3 engines with distinct evidence boundaries;
- non-adaptive B2 fixed-viva development contract;
- verification burden kept as question count, measured time and complexity rather than a composite score;
- persistent experiment runs and frozen B0-B4 method/configuration versions;
- persistent method observations and independent assessor reference judgments;
- automatic B0-B3 comparative execution;
- bounded B4 integration into the same experiment;
- experiment completeness gate requiring B0-B4 plus independent reference;
- formal development → pilot → method freeze → held-out final-evaluation protocol.

Latest directly verified software checkpoint: **GitHub Actions run #159 on 20 September 2026 — 98 passed, 0 failed in 1.57 seconds**.

This is software verification for the development scope, not evidence that EGPCV is scientifically superior.

## Current bounded B4 slice
The implemented research slice is **Competence Claim 3 (CC3): Test Design** with **EG-T3: Missing Independent Test Design Evidence**.

`VP-CC3-02` has a frozen executable development evaluator. `VP-CC3-03` may be potentially sufficient but currently has no frozen executable evaluator; it is therefore rejected as `REJECTED_NOT_EXECUTABLE`. If no adequate executable unused probe remains, the system returns `HUMAN_REVIEW_REQUIRED`.

## Integrity boundary
Observation does not automatically imply misconduct. Competence evidence and integrity observations are separate. Consequential integrity decisions require authorized human review under the applicable **Examination Capability Contract (ECC)**.

## Research protocol
See `specification/FORMAL_RESEARCH_EXPERIMENT_SPECIFICATION.md`.

Development fixtures may be used to debug the mechanism but are not independent ground truth. Final comparative evidence requires frozen methods/configurations, assessor rubric, corpus, evidence rules and outcome calculations, followed by held-out evaluation.

## Deliberately deferred
Full registration/payment/course management, webcam proctoring, AI-code detection, browser lockdown, full IDE functionality, live invigilation, broad multi-language support and production deployment are not current priorities.

## Scientific status
The final CC1-CC6 ontology, PARTIAL/UNRESOLVED boundary, final probe catalogue, assessor agreement procedure, final corpus/sample size, thresholds, accessibility validation, ECC implementation and held-out final evaluation remain pending. No authorship-proof, AI-use-proof, perfect cheating-detection, lecturer-replacement or complete-programming-competence claim is authorized.
