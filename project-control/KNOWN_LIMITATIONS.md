# Known Limitations

## KL-001 — Work orchestration not yet validated
The orchestration design has not yet been exercised through one complete project lifecycle in ChatGPT Work.

Impact: Do not claim autonomous multi-agent coordination is proven.

## KL-002 — Codex handoff protocol not yet validated
Codex has not yet been tested against this exact project-control protocol.

Impact: Engineering handoffs remain a designed workflow until tested.

## KL-003 — Google Drive structure not yet initialized
The Drive connection is live, but the proposed project folder/document structure has not yet been created and validated.

## KL-004 — Repository currently contains only starter-kit infrastructure
No actual Project 001 application has been instantiated yet.

## KL-005 — Human approval remains required for A3 decisions
The system is intentionally not designed to autonomously change project identity, objectives, methodology, core stack, or major scope.


## P001 security gaps to close before public or real-student deployment (2026-11-02)
- ~~Login has no rate limit or lockout (PROJECT_RULES §22).~~ Addressed by FD-08 (merged as PR #29).
- ~~Login timing reveals whether a username exists.~~ Addressed by FD-08 (merged as PR #29).
- ~~Account changes have no audit trail.~~ Addressed by FD-08 (merged as PR #29).
- Still open: no independent security review; one-time passwords are handed over by the administrator; behind a reverse proxy, uvicorn must be configured to trust it or all users share one address for the limits.

See `projects/project-007-coding-examination-platform/documentation/FD07_USER_MANAGEMENT_DESIGN.md` and `FD08_LOGIN_PROTECTION_AUDIT_DESIGN.md`.


## P007 School Points (2026-11-05)
- Demonstration build: synthetic data only, no sign-in, SQLite.
- The benchmark scenarios and the contextual audit were written by the same agent; results do not show the audit works on unseen or real data.
- M6 (time to detection) and M7 (evidence completeness with human reviewers) are not measured.

## P009 Screen Memory (2026-11-05)
- Live recording not verified on a desktop; Windows only.
- Exclusion by program and title cannot catch every sensitive window (46 % of unlisted sensitive visits exposed in simulation).
- No text recognition; search covers window titles and program names.
- The resumption measure is a proxy; real task-resumption performance needs a study with people and ethics approval.

## P010 Chess (2026-11-05)
- Text chat only; no voice. No accounts; games in memory.
- The arbiter's abuse and threat word lists miss unseen phrasings (22 % of severe held-out cases); castling mentions are not parsed.
- No human-review or appeal procedure; rulings are notices only.

## P004 Compression Gateway (2026-11-05)
- Network is modelled, not emulated; B4 predicts with the same formula the benchmark scores with.
- B4's fidelity check (24–56 % of encode time on the development laptop) was not counted in the benchmark; large photos can hit the 5 s limit on low-spec hardware.
- No cache; synthetic corpus; time is the only objective unless the client sends Save-Data.

## P006 Learning World (2026-11-05)
- No language model connected; AI roles are deterministic stand-ins. Phase 3 (retrieval, providers, model-side injection defences) not built.
- One verification check per concept: simulated false mastery 13.9 %.
- Single user, local only; small benchmark course.

## P011 Defence Practice (2026-11-05)
- Rule-based findings do not generalise to new wording (17 % of planted issues on held-out phrasing; random 15 %); no AI provider connected.
- Contradictions inside one paragraph are not detected; feedback is surface-level and is not a grade.
- No speech input or output.

## P002 Educational LM (2026-11-05)
- Tier A only: about 120k parameters, 40 hand-written facts, one domain; memorises a small world. No GPU (Tier B) work.
- Likelihood comparisons are not understanding; the contrast condition saw every misconception string in training.

## P014 Lanterns of Brinewold (2026-11-05)
- No human playtest; balance tuned with a scripted bot. AI companions do not dodge telegraphed attacks.
- No sound; keyboard only; one region.

## P005 Log root-cause tool (2026-11-05)
- Evaluated only on synthetic, self-authored incidents; real incident datasets with known root causes not used.
- Fixed library of eight fault types; logs only (no metrics or traces); no language model.
- Abstains on 25 % of incidents that had one clear cause.
