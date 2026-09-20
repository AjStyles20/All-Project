# P001 Requirements Traceability Matrix (RTM) — v1.1

A **Requirements Traceability Matrix (RTM)** connects the research problem to software behavior, tests and eventual experimental evidence. Passing software tests verifies implemented behavior; it does not validate the research hypothesis.

## Functional requirements

| ID | Requirement | Current implementation | Status / boundary |
|---|---|---|---|
| FR-01 | Programming Case Management | domain + SQLite persistence | IMPLEMENTED / TESTED |
| FR-02 | Competence Claim Management | domain + persistence | IMPLEMENTED / TESTED |
| FR-03 | Claim Applicability | REQUIRED / NOT_APPLICABLE invariants | IMPLEMENTED / TESTED |
| FR-04 | Evidence Management | domain + persistence | IMPLEMENTED / TESTED |
| FR-05 | Claim-Evidence Mapping | persistent links | IMPLEMENTED / TESTED |
| FR-06 | Evidence-State Evaluation | EvidenceEvaluator | IMPLEMENTED / TESTED for bounded CC3 development scope |
| FR-07 | Evidence-Gap Detection | GapDetector | IMPLEMENTED / TESTED for EG-T3 |
| FR-08 | Verification Probe Repository | versioned development catalogue | IMPLEMENTED for CC3 development set; final catalogue not frozen |
| FR-09 | Probe Admissibility | ProbeSelector | IMPLEMENTED / TESTED |
| FR-10 | Bounded-Minimum Probe Selection | admissibility + potential sufficiency + executability + unused + burden ordering | IMPLEMENTED / TESTED for CC3 |
| FR-11 | Probe Result Management | structured CC3 response evaluator | IMPLEMENTED / TESTED for VP-CC3-02; VP-CC3-03 deliberately non-executable |
| FR-12 | Evidence Update | VerificationWorkflow + persistence | IMPLEMENTED / TESTED |
| FR-13 | Stop Rule | generic StopRule with continue/complete/human-review outcomes | IMPLEMENTED / TESTED for current claim-control model |
| FR-14 | Human Escalation | no adequate unused executable probe → HUMAN_REVIEW_REQUIRED | IMPLEMENTED / TESTED |
| FR-15 | Examination Capability Contract (ECC) Management | conceptual/specification boundary only | PENDING; later examination-platform work |
| FR-16 | Programming-Process Capture | baseline accepts process evidence but capture subsystem absent | PENDING; needed before real B1 process collection |
| FR-17 | Integrity Observation Management | competence/integrity separation specified, no module | PENDING |
| FR-18 | Authorized Exception Handling | policy/accessibility concept only | PENDING |
| FR-19 | Evidence Provenance | EvidenceItem source metadata + fixed-viva/targeted-verification separation | SUBSTANTIALLY IMPLEMENTED for research slice; broader ECC/assistance provenance pending |
| FR-20 | B0 Engine | Baseline0Engine / common runner | IMPLEMENTED / TESTED |
| FR-21 | B1 Engine | Baseline1Engine / common runner | IMPLEMENTED / TESTED |
| FR-22 | B2 Engine | non-adaptive fixed-viva boundary + development contract | IMPLEMENTED / TESTED for development comparator; assessor validation pending |
| FR-23 | B3 Engine | evidence-centered non-targeted baseline | IMPLEMENTED / TESTED |
| FR-24 | B4 EGPCV Engine | persistent bounded CC3 orchestrator | IMPLEMENTED / TESTED for CC3/EG-T3 |
| FR-25 | Method Configuration Versioning | experiment-run frozen method/configuration records | IMPLEMENTED / TESTED |
| FR-26 | Experiment Management | persistent runs, B0-B4 observations, completeness gate, B0-B3 execution, B4 integration | IMPLEMENTED / TESTED for development experiment skeleton |
| FR-27 | Independent Assessor Judgments | persistent separate reference judgment with claim/rubric checks | IMPLEMENTED / TESTED as infrastructure; independent human validation pending |
| FR-28 | Audit Trace | immutable state/gap/selection/result/control events + candidate dispositions | IMPLEMENTED / TESTED for bounded B4 slice |
| FR-29 | Lecturer Review | full review interface absent | DEFERRED to later interface/platform milestone |
| FR-30 | Examination Workflow | full candidate/lecturer workflow absent | DEFERRED; not required for M6 research skeleton |

## Non-functional requirements

| ID | Requirement | Current status |
|---|---|
| NFR-01 | Explainability | IMPLEMENTED for current research path through rationales, candidate dispositions and audit events |
| NFR-02 | Reproducibility | SUBSTANTIAL: frozen experiment/method/config versions and formal protocol; final scientific freeze pending |
| NFR-03 | Traceability | IMPLEMENTED for bounded research path; RTM + persistent audit/provenance |
| NFR-04 | Data Integrity | SQLite foreign keys/checks/uniqueness plus rollback/duplicate tests |
| NFR-05 | Modularity | domain/persistence/services/tests separated |
| NFR-06 | Resource-conscious execution | lightweight Python/FastAPI-compatible architecture + SQLite; no GPU/LLM required |
| NFR-07 | Privacy/data minimization | DESIGN BOUNDARY; full operational policy pending |
| NFR-08 | Accessibility awareness | PENDING authorized-exception/accessibility implementation and validation |
| NFR-09 | Restricted untrusted-code execution | PENDING; mandatory before executing real candidate code |
| NFR-10 | Recoverability | PARTIAL: transaction rollback tested; broader operational recovery pending |
| NFR-11 | Configuration immutability | SUBSTANTIAL: frozen per-run method/config versions and immutable domain records |
| NFR-12 | Human authority over consequential misconduct decisions | GOVERNING RULE; integrity workflow implementation pending |

## M6 closure assessment

**M6 — Experiment Runner / Comparative Experiment Infrastructure: COMPLETE FOR THE BOUNDED DEVELOPMENT SKELETON.**

This closure means the software can persist a frozen experiment identity, execute and record distinct B0-B3 baselines, execute the bounded CC3 B4 path, preserve verification provenance boundaries, store separate burden dimensions, record an independent-reference judgment, and refuse experiment completion until B0-B4 plus the reference are present.

It does **not** mean the scientific method is finally validated, the final corpus is frozen, independent assessors have been recruited, real participants have been evaluated, or EGPCV has been shown superior.

## Items intentionally carried beyond M6

The following are not M6 blockers and must not be silently represented as complete:

- ECC implementation and authorized exceptions (FR-15/FR-18);
- real programming-process capture (FR-16);
- integrity-observation workflow (FR-17);
- full lecturer/research interface (FR-29);
- complete examination workflow (FR-30);
- secure execution of untrusted candidate code (NFR-09);
- accessibility validation (NFR-08);
- final competence ontology and scientific PARTIAL/UNRESOLVED boundary;
- final probe catalogue/evaluators;
- assessor protocol validation and inter-rater method;
- pilot-derived corpus size, thresholds and held-out final evaluation.

These belong to M7+ interface/pilot/method-freeze/platform work as appropriate.

## Verified software checkpoint

GitHub Actions run #162 on 20 September 2026 executed the current P001 suite successfully: **98 passed, 0 failed in 1.73 seconds**.

This establishes software verification only for the tested development scope. It is not evidence that B4 is superior or that the research hypothesis is true.

## Research evidence still required

The formal experiment protocol requires development → pilot → method freeze → held-out final evaluation. Final research evidence must connect B0-B4 outputs to genuinely independent assessor judgments and report agreement, unresolved-claim reduction and separate verification-burden dimensions. Contextual outcomes such as unnecessary verification, false integrity escalation, examiner review effort, usability, fairness and accessibility must be measured only where the study design legitimately supports them.
