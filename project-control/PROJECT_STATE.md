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
- **Web UI slice 1 (candidate flow)**: PR #25 **merged 2026-10-30** (`748685d`). Semantic HTML/CSS/plain JS at `/ui` (DR-017), browser-verified (TE-015).
- **Web UI slice 2 (examiner and administrator)**: PR #27 **merged** (`40ae970`). Browser-verified (TE-016).
- **FD-07 User Management**: PR #28 **merged** (`1ceaab1`). Status: IMPLEMENTED / UNIT + API TESTED / **LIVE VERIFIED on MySQL 8.4.9** (disposable instance, TE-017). Account model awaiting AJ review (DR-019).
- **FD-08 Login protection and account audit trail**: PR #29 **merged** (`fe31072`). Status: IMPLEMENTED / UNIT + API TESTED / **LIVE VERIFIED on MySQL 8.4.9** (disposable instance, TE-018). Policy awaiting AJ review (DR-020). See `documentation/FD08_LOGIN_PROTECTION_AUDIT_DESIGN.md`.

- **P007 School Point & Digital Economy System** (DR-021, product build): PR #30 **merged** (`7844277`). Ledger, scenarios S0–S8, audit engines B0–B4, evaluation harness, dashboard. Synthetic data only, no sign-in. Benchmark rule met (TE-019), but the scenarios and B4 were written by the same agent, so this is not evidence the audit works on real schools. See `projects/project-004-school-points-economy/docs/RESULTS.md`.

- **P009 Personal Screen Memory System** (DR-021, product build): PR #31 **merged** (`179d737`). Privacy/security model committed before capture code. Windows recorder (selective policy B4, exclusions, DPAPI encryption, retention, deletion), local dashboard, offline policy comparison (TE-020). Live capture NOT verified (the development session saw a locked desktop). No study with people. See `projects/project-006-screen-memory/docs/EVALUATION.md`.

- **P010 Intelligent Online Chess Platform** (DR-021, product build): PR #32 **merged** (`240c51e`). In-house rules engine (perft-verified), two-player games with spectators and chat, contextual arbiter B4 against four baselines (TE-021). Text chat stands in for voice; no accounts; games in memory. Rule met, but B4 misses 22 % of severe cases on held-out paraphrases. See `projects/project-005-intelligent-chess-platform/docs/EVALUATION.md`.

- **P004 Internet Compression and Optimization Proxy** (DR-021, product build): PR #33 **merged** (`55d2fb1`). Formal specification committed before code. Origin-controlled gateway with security invariants S1–S10, policies B0–B4, generated corpus, benchmark (TE-022). All predeclared thresholds met (B4 3 regressions vs ≥147), but the network is modelled and B4's verification cost was not counted. See `projects/project-012-internet-compression-proxy/docs/RESULTS.md`.

- **P006 AI Virtual Classroom / Personal Learning World** (DR-021, product build; research verdict PARK unchanged): PR #34 **merged** (`ae0fcf8`). Pass 017 Phases 1–2: APLDG trust kernel and PGAIC mastery kernel, SQL JOIN course, single-user app; all automatic Pass 017 §14 gates pass (TE-023). No language model connected; simulated learners only. See `projects/project-002-ai-virtual-classroom/docs/RESULTS.md`.

- **P011 Source-Grounded AI Defense Simulator** (DR-021, product build; research verdict PARK / merged with P001 unchanged): PR #35 **merged** (`4552a18`). Document upload (TXT/MD/DOCX/PPTX/PDF), rule-based findings, four reviewer roles, grounded questions, criterion feedback, local app (TE-024). Rules reach 99 % of planted issues on dev wording but only 17 % on held-out wording (random: 15 %). See `projects/project-001-ai-defense-simulator/docs/RESULTS.md`.

- **P002 Educational Language Model From Scratch** (DR-021; build regardless, outside FYP competition): PR #36 **merged** (`445d77c`). Tier A: NumPy Transformer with hand-written, gradient-checked backward pass, BPE tokenizer, hand-written CC0 corpus (TE-025). Finding: naive misconception-contrast pretraining made the model prefer misconceptions (37.5 % vs 90 %). See `projects/project-003-small-educational-language-model/docs/RESULTS.md`.

- **P014 Fantasy Action RPG** (DR-021; creative project, research verdict unchanged): PR #37 **merged** (`a2765a5`). Original browser game *Lanterns of Brinewold*: four-hero party, one region, one quest chain, boss with telegraphed attack; all names, story and dialogue original (`docs/IP_NOTES.md`). Tested by unit tests, a scripted playthrough and a browser check (TE-026). Balance tuned with a bot only; no human playtest yet.

- **P005 Automated Log Analysis and Root-Cause Assistance** (DR-021; research verdict KILL unchanged, engineering build): PR #38 **merged** (`213fbfd`). Local CLI: parsing with secret redaction, incident onset, competing hypotheses with typed claim states and file:line evidence, discriminating checks, UNRESOLVED/INSUFFICIENT abstention, VERIFIED only by recorded human checks, HTML report (TE-027). On 240 synthetic incidents: unsupported assertions 9.6 % vs 40–60 % for baselines; abstains on 25 % of answerable cases.

- **P008 StartupMatch** (DR-021; research verdict KILL unchanged, product build): PR #39 **merged** (`d92226f`). Two-sided web app: transparent per-criterion matching (unknown ≠ zero), declared-vs-revealed thesis warnings, deal provenance and staleness flags, intro workflow with contact privacy, accounts with scrypt and CSRF guard (TE-028). No accuracy claim; profiles not identity-verified.

- **P012 Interactive AI Virtual Audience** (DR-021; research verdict KILL unchanged, product build): branch `p012-virtual-audience`, draft PR. Browser-only *Rehearsal Room*: panel with moods, interruptions, follow-ups and time pressure, text-based delivery measures, local practice journey with next-drill suggestion (TE-029). Practice only, no clinical claims; does not duplicate P011's document-grounded questions.

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
- **#25**, **#27** P001 web UI slices 1 and 2. **Merged** (`748685d`, `40ae970`).
- **#28** P001 FD-07 user management. **Merged** (`1ceaab1`).
- **#29** P001 FD-08 login protection and audit trail. **Merged** (`fe31072`).
- **#30** P007 School Points first version (DR-021). **Merged** (`7844277`).
- **#31** P009 Screen Memory first version (DR-021). **Merged** (`179d737`).
- **#32** P010 Chess first version (DR-021). **Merged** (`240c51e`).
- **#33** P004 Compression Gateway first version (DR-021). **Merged** (`55d2fb1`).
- **#34** P006 Learning World first version (DR-021). **Merged** (`ae0fcf8`).
- **#35** P011 Defence Practice first version (DR-021). **Merged** (`4552a18`).
- **#36** P002 Educational LM Tier A (DR-021). **Merged** (`445d77c`).
- **#37** P014 Lanterns of Brinewold (DR-021). **Merged** (`a2765a5`).
- **#38** P005 Log root-cause tool (DR-021). **Merged** (`213fbfd`).
- **#39** P008 StartupMatch (DR-021). **Merged** (`d92226f`).
- P012 Rehearsal Room (DR-021): branch `p012-virtual-audience`, draft PR, awaiting AJ.
- **#1–#16** are historical branches from the earlier Source-Grounded AI Defense Simulator lineage (now canonical P011 per `CANONICAL_PROJECT_INDEX.md`). They are still open and reported mergeable. Whether to close or keep them is AJ's decision.

## Current Work
1. ~~Live-MySQL evidence for FD-01/FD-02 and merge of PR #19~~. Done 2026-10-29 (TE-005, TE-007; merged `aefc0a8`). Optional: repeat the live run on AJ's own configured server.
2. ~~FD-03/FD-04/FD-05 merge; DR-013 ECC approval~~. Done 2026-10-29. FD-06 (evidence bridge) is open with DR-015/DR-016 applied. Real institutional ethics approval is required before any real student is bridged. Next: a lightweight web UI.
3. Prepare pilot and method-freeze materials without treating development fixtures as independent ground truth.
4. **P003 external evaluation, blocked on AJ:** an OpenAI key in AJ's environment plus a model choice and cost approval for the frozen B2 runs; genuinely independent human reviewers; then the locked comparative analysis (DR-018 forbids simulating these).

### Superseded current-work list (2026-09-20)
1. Keep P001 on its separate implementation branch until the agreed merge gate. *(PR #17 has since merged.)*
2. Complete governance/documentation synchronization and remaining M6 hardening.
