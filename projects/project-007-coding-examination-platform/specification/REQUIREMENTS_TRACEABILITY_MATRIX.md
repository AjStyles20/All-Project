# P001 Requirements Traceability Matrix (RTM) — v1.0

A **Requirements Traceability Matrix (RTM)** connects the research problem to software behavior, tests and eventual experimental evidence. A test passing verifies implemented behavior; it does not by itself validate a research hypothesis.

| ID | Requirement | Research relevance | Current implementation | Verification/evidence status |
|---|---|---|---|---|
| FR-01 | Programming Case Management | common experimental case | domain + persistence | implemented/tested |
| FR-02 | Competence Claim Management | bounded competence model | domain + persistence | implemented/tested |
| FR-03 | Claim Applicability | prevents irrelevant claims becoming gaps | domain invariants + persistence | implemented/tested |
| FR-04 | Evidence Management | evidence-centered assessment | domain + persistence | implemented/tested |
| FR-05 | Claim-Evidence Mapping | trace evidence to claims | persistence | implemented/tested |
| FR-06 | Evidence-State Evaluation | RQ2/RQ3 mechanism | EvidenceEvaluator, currently bounded CC3 path | implemented/tested for current scope |
| FR-07 | Evidence-Gap Detection | core EGPCV mechanism | GapDetector, currently EG-T3 | implemented/tested for current scope |
| FR-08 | Verification Probe Repository | frozen candidate probes | development probe catalogue | implemented for CC3 development set |
| FR-09 | Probe Admissibility | prevents irrelevant verification | ProbeSelector | implemented/tested |
| FR-10 | Bounded-Minimum Probe Selection | residual contribution | sufficiency/admissibility then burden selection | implemented/tested for CC3 |
| FR-11 | Probe Result Management | acquire independent evidence | structured CC3 response model | implemented/tested for VP-CC3-02 |
| FR-12 | Evidence Update | verification changes evidence state | VerificationWorkflow + persistence E2E | implemented/tested |
| FR-13 | Stop Rule | avoid unnecessary verification | current CC3 supported/continue control | partial; general rule pending |
| FR-14 | Human Escalation | safe abstention | no-adequate-probe path | implemented/tested in selector scope |
| FR-15 | ECC Management | policy-aware examination interpretation | not implemented | pending |
| FR-16 | Programming-Process Capture | B1/B2/B3/B4 evidence | not implemented | pending |
| FR-17 | Integrity Observation Management | competence/integrity separation | conceptual boundary only | pending |
| FR-18 | Authorized Exception Handling | accessibility/policy correctness | not implemented | pending |
| FR-19 | Evidence Provenance | auditability | partial EvidenceItem metadata | partial |
| FR-20 | B0 Engine | comparison baseline | not implemented | pending |
| FR-21 | B1 Engine | comparison baseline | not implemented | pending |
| FR-22 | B2 Engine | fixed-viva comparison | not implemented | pending |
| FR-23 | B3 Engine | evidence-model comparison | not implemented | pending |
| FR-24 | B4 EGPCV Engine | primary method | first CC3 vertical slice | implemented/tested for bounded scope |
| FR-25 | Method Configuration Versioning | reproducibility | not implemented | pending |
| FR-26 | Experiment Management | B0–B4 evaluation | not implemented | pending |
| FR-27 | Independent Assessor Judgments | non-circular reference | specification only | pending |
| FR-28 | Audit Trace | defense/reproducibility | state/evidence history partial | M4 next |
| FR-29 | Lecturer Review | human authority | not implemented | deferred |
| FR-30 | Examination Workflow | implementation vehicle | not implemented | deferred |

## Non-functional requirements

| ID | Requirement | Current status |
|---|---|---|
| NFR-01 | Explainability | rationales present in evaluator/selector/state records; expand in M4 |
| NFR-02 | Reproducibility | versioned branch/tests; method configuration pending |
| NFR-03 | Traceability | partial; RTM + persistent state/evidence; M4 next |
| NFR-04 | Data Integrity | SQLite constraints, foreign keys, duplicate/rollback tests |
| NFR-05 | Modularity | domain/persistence/services/tests separated |
| NFR-06 | Resource-conscious execution | lightweight Python/SQLite; no GPU/LLM required |
| NFR-07 | Privacy/data minimization | design boundary; full policy pending |
| NFR-08 | Accessibility awareness | authorized-exception design pending |
| NFR-09 | Restricted untrusted-code execution | not implemented; required before real candidate code execution |
| NFR-10 | Recoverability | transaction rollback tested; broader recovery pending |
| NFR-11 | Configuration immutability | domain records immutable; experiment configuration pending |
| NFR-12 | Human authority over consequential misconduct decisions | governing design rule; integrity module pending |

## Verified software checkpoint

GitHub Actions run #26 executed the P001 test suite on 20 September 2026: **37 passed, 0 failed**. This establishes software verification only for the tested development scope.

## Research evidence still required

The RTM must eventually connect B0–B4 runs to independent assessor/reference judgments and experimental outcomes such as agreement, unresolved-claim reduction, verification questions/time, unnecessary-verification rate, false integrity escalation and examiner review effort. No superiority result exists yet.
