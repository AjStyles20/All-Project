# M4 Audit and Traceability Checkpoint

**Project:** P001 — Intelligent Coding Examination Platform  
**Research mechanism:** Evidence-Gap-Driven Programming Competence Verification (EGPCV)  
**Implementation branch:** `p001-egpcv-implementation`

## Checkpoint decision

M4 is implementation-complete for the current bounded CC3 / EG-T3 research slice and may proceed to M5 baseline implementation.

This is a software-engineering checkpoint, not scientific validation of EGPCV.

## Implemented M4 controls

1. Append-oriented audit events record evidence-state, gap, probe-selection, probe-result and control-decision events.
2. Candidate-by-candidate probe audit records why each bounded candidate was selected or rejected.
3. Probe selection minimizes burden only after admissibility and potential sufficiency.
4. Used probes are tracked per verification run and cannot be selected repeatedly in the same run.
5. A general Stop Rule supports:
   - CONTINUE_VERIFICATION;
   - VERIFICATION_COMPLETE; and
   - HUMAN_REVIEW_REQUIRED.
6. CONTRADICTED evidence does not become an automatic misconduct, cheating or failure decision.
7. Verification runs persist method/configuration versions, start/end state, used probes and final disposition.
8. The B4 orchestrator connects evidence evaluation, gap detection, probe selection, verification evidence, state update, stopping, persistence and audit.
9. Negative-control and exhaustion paths are represented in automated tests.

## Verified execution checkpoint

GitHub Actions workflow **P001 EGPCV Tests**, run **#82** (run ID `35507906289`), completed successfully for commit `bbe4aa141e1c0039f918d71c62b77b01ba40180e`.

Result:

```text
58 passed in 0.76s
```

This establishes that the automated software tests in the tested scope passed. It does **not** establish research effectiveness, expert agreement, fairness, superiority over B0–B3, or external validity.

## Remaining limitations carried forward

- Current executable evidence rules are deliberately narrow and centered on CC3 Test Design / EG-T3.
- VP-CC3-03 is catalogued as potentially sufficient but does not yet have a frozen executable response rubric.
- Final CC1–CC6 ontology and support rules remain subject to assessor/pilot validation.
- PARTIAL versus UNRESOLVED remains a development operationalization, not a scientifically validated boundary.
- Examination Capability Contract (ECC), integrity-observation workflow, process capture and full examination product remain later work.
- B0–B3 comparison engines are not yet implemented.
- No experimental claim that B4 is better than any baseline is permitted at this checkpoint.

## M5 entry condition

M5 may implement B0–B3 only under the frozen baseline contracts:

- **B0:** final submission + ordinary tests/rubric.
- **B1:** B0 + controlled exam process/event evidence, no targeted verification.
- **B2:** B1 + generic fixed viva/code explanation.
- **B3:** evidence-centered competence model without targeted verification.
- **B4:** full EGPCV evidence model + gap-driven targeted verification.

The same eligible case and underlying evidence should be used across baselines wherever the experimental contract requires comparability.
