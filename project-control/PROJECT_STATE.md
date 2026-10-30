# Project State

## Project Identity
- Project name: AJ Project OS
- Project type: Research-first final-year-project portfolio and implementation workspace
- Project owner: AJ
- Last verified date: 2026-10-29 (P001 implementation/PR status; research sections unchanged since 2026-09-20)
- Repository: AjStyles20/All-Project
- Default branch: main

## Canonical Portfolio State
Canonical identity is controlled by `project-control/CANONICAL_PROJECT_INDEX.md`. Historical folder numbers are preserved for provenance.

Independent FYP survivors after the completed research and comparative selection work remain P001, P003, P004, P007, P009 and P010. P011 remains parked as an independent FYP because its evidence-gap verification mechanism collides with P001. P006 remains parked as an independent FYP.

## Current Implementation Decision
Decision Record DR-010 prospectively supersedes the earlier implementation prohibition after completion of the comparative selection work.

- **P001 — Intelligent Coding Examination Platform:** first research-critical implementation target.
- **P003 — Geopolitical Economic Risk to Economic Impact Forecasting & Warning:** second implementation target.
- P003's internal implementation is complete and on main (PR #18, `71f890a`, DR-018); AJ directed the move to P003 on 2026-10-30. Its remaining work is external (see below).
- P004, P007, P009 and P010 remain survivors/reserves; no full implementation is authorized merely by survivor status.

## P001 Current State
Historical GitHub folder: `projects/project-007-coding-examination-platform`.
Research-critical implementation: branch `p001-egpcv-implementation`, PR #17, **merged into main on 2026-09-22** (merge commit `cb29f06…`). Latest main CI: run #292, success, head `2596768…`.

Full-product layer (MySQL, per the MySQL technology decision in `documentation/DATABASE_TECHNOLOGY_DECISION_MYSQL.md`):
- **FD-01 Identity/RBAC** — on main. Live MySQL test passed on 2026-10-29 (MySQL 8.4.9 disposable local instance; see TE-005).
- **FD-02 Examination & Question Management** — PR #19 **merged into main on 2026-10-29** (merge commit `aefc0a8`), with policy per DR-011. Status: IMPLEMENTED / UNIT + API TESTED / **LIVE VERIFIED on MySQL 8.4.9** (disposable local instance, 2026-10-29; AJ's own server not used). As of 2026-10-29 it includes examiner list/read/update/detach endpoints, compare-and-set lifecycle transitions, DRAFT-guarded SQL, and a scheduling-requires-a-question rule (A2, awaiting AJ review). See `documentation/FD02_EXAMINATION_QUESTION_DESIGN.md`.
- **FD-03 Candidate Assignment, Session & Response Capture**: branch `p001-fd03-candidate-sessions`, PR #20 **merged into main on 2026-10-29** (`2be8416`); policy per DR-011. Status: IMPLEMENTED / UNIT + API TESTED / **LIVE VERIFIED on MySQL 8.4.9** (disposable local instance, 2026-10-29). Four policy points await AJ. See `documentation/FD03_CANDIDATE_SESSION_DESIGN.md`.
- **FD-04 Examiner Review & Marking**: PR #21 **merged into main on 2026-10-29** (`6e50711`). Status: IMPLEMENTED / UNIT + API TESTED / **LIVE VERIFIED on MySQL 8.4.9** (disposable instance, TE-009). EGPCV evidence registration is deferred until the ECC exists. Marking policy is set by DR-012 (weighted %, mark history, explicit release); live-verified again after DR-012 (TE-010). See `documentation/FD04_REVIEW_MARKING_DESIGN.md`.
- **ECC specification v1.0**: **APPROVED by AJ on 2026-10-29 (DR-013)** with Q1–Q5 resolved, via PR #22. It is not yet implemented. It unblocks FD-05 (ECC management); FD-06 (evidence bridge) needs an explicit question → case research link.
- **FD-05 ECC Management**: PR #23 **merged into main on 2026-10-29** (`4065605`). Status: IMPLEMENTED / UNIT + API TESTED / **LIVE VERIFIED on MySQL 8.4.9** (disposable instance, TE-011). Scheduling now requires a contract. Exception extra time extends that candidate's deadline (DR-014, TE-012). See `documentation/FD05_CAPABILITY_CONTRACT_DESIGN.md`.
- **FD-06 Evidence Bridge**: PR #24 **merged into main on 2026-10-29** (`5b59707`). Status: IMPLEMENTED / UNIT + API TESTED / **LIVE VERIFIED on MySQL 8.4.9** with a temporary SQLite research store (TE-013). Governed by DR-015 (ethics reference + opt-in, random codes, admin-only links) and DR-016 (deletion on withdrawal; research store outside the app, TE-014). **No real student bridged**; that needs real ethics approval. See `documentation/FD06_EVIDENCE_BRIDGE_DESIGN.md`.
- **Web UI slice 1 (candidate flow)**: branch `p001-ui-candidate`, draft PR. Semantic HTML/CSS/plain JS at `/ui` (DR-017), browser-verified (TE-015).
- **Web UI slice 2 (examiner and administrator)**: branch `p001-ui-examiner-admin`, draft PR stacked on #25. Browser-verified (TE-016). Not available in the API or UI: user accounts/directory and an administrator list of examinations.

Residual contribution: **Evidence-Gap-Driven Programming Competence Verification (EGPCV)**, narrowed to competence-gap-driven bounded minimum independent evidence acquisition rather than generic adaptive viva, browser coding, proctoring, or code-conditioned questioning.

Implemented research-critical scope includes:
- M1 core domain model and SQLite persistence;
- M2 bounded CC3 Test Design evidence evaluator and EG-T3 gap detector;
- M3 B4 targeted-verification vertical slice;
- M4 immutable audit/traceability and generic stop/human-review control;
- M5 distinct B0-B3 baseline engines, B2 fixed-viva development comparator, evidence-leakage controls, separate burden dimensions, and method/reference records;
- M6 persistent experiment identity, frozen B0-B4 method/configuration versions, per-method observations, independent reference judgments, experiment completeness gate, automatic B0-B3 execution, and bounded B4 integration;
- formal B0-B4 development research experiment specification.

Latest directly verified GitHub Actions checkpoint: **run #159 — 98 passed, 0 failed, 1.57s** at commit `a2a7bb6...`. This is software verification only; it is not scientific validation.

## P001 Scientific Status
Development mechanics are implemented for the bounded CC3/EG-T3 slice. VP-CC3-02 is the currently executable targeted development probe. VP-CC3-03 is potentially sufficient but not executable and is therefore rejected rather than used as an automated fallback.

The final competence ontology, PARTIAL/UNRESOLVED boundary, final probe library, assessor reliability method, corpus/sample size, participants if any, numerical thresholds, accessibility validation, Examination Capability Contract implementation, secure untrusted-code execution, and held-out final evaluation remain unfrozen or pending.

No superiority, authorship, AI-use detection, perfect cheating detection, lecturer replacement, or complete programming-competence claim is established.

## Historical P011 Warning
Historical Source-Grounded AI Defense Simulator / canonical P011 test claims must not be transferred to P001. Any historical approximately-146-test claim belongs to a different implementation lineage and remains separate from the verified P001 suite.

## Open Pull Requests (observed 2026-10-29)
- **#19** P001 FD-02. **Merged 2026-10-29** (`aefc0a8`).
- **#20** P001 FD-03. **Merged 2026-10-29** (`2be8416`).
- **#21** P001 FD-04. **Merged 2026-10-29** (`6e50711`).
- **#22** ECC spec v1.0. **Merged 2026-10-29** (`5f8a235`).
- **#23** P001 FD-05. **Merged 2026-10-29** (`4065605`).
- **#24** P001 FD-06. **Merged 2026-10-29** (`5b59707`).
- **#18** P003 ETEC implementation. **Merged 2026-10-30** (`71f890a`). **#26** P003 tests on pushes to main. **Merged 2026-10-30** (`3dc01fc`).
- **#25** P001 web UI slice 1 (candidate). Draft, awaiting AJ.
- P001 web UI slice 2 (examiner and administrator): draft PR stacked on #25.
- **#1–#16** are historical branches from the earlier Source-Grounded AI Defense Simulator lineage (now canonical P011 per `CANONICAL_PROJECT_INDEX.md`). They are still open and reported mergeable. Whether to close or keep them is AJ's decision.

## Current Work
1. ~~Live-MySQL evidence for FD-01/FD-02 and merge of PR #19~~. Done 2026-10-29 (TE-005, TE-007; merged `aefc0a8`). Optional: repeat the live run on AJ's own configured server.
2. ~~FD-03/FD-04/FD-05 merge; DR-013 ECC approval~~. Done 2026-10-29. FD-06 (evidence bridge) is open with DR-015/DR-016 applied. Real institutional ethics approval is required before any real student is bridged. Next: a lightweight web UI.
3. Prepare pilot and method-freeze materials without treating development fixtures as independent ground truth.
4. **P003 external evaluation, blocked on AJ:** an OpenAI key in AJ's environment plus a model choice and cost approval for the frozen B2 runs; genuinely independent human reviewers; then the locked comparative analysis (DR-018 forbids simulating these).

### Superseded current-work list (2026-09-20)
1. Keep P001 on its separate implementation branch until the agreed merge gate. *(PR #17 has since merged.)*
2. Complete governance/documentation synchronization and remaining M6 hardening.
