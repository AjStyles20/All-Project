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
