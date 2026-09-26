# Feature 011 Verification Plan — End-to-End Rehearsal Experience

## Scope
Verify that the previously implemented Project 001 capabilities operate as one coherent bounded rehearsal workflow without weakening workspace scoping, provenance checks, provider boundaries, or truthful completion state.

## Required checks
- compile all application and test sources;
- complete regression suite passes;
- dependency audit reports no known vulnerabilities at verification time;
- web session creation lands directly on the authoritative first turn;
- session question route proves workspace + session + question association server-side;
- cross-workspace session/question path tampering fails;
- question page exposes turn/max-turn progress and session return path;
- session answer route keeps feedback in the owning rehearsal flow;
- follow-up web action lands directly on the new authoritative turn;
- session snapshot exposes generated/answered/current-turn state;
- answering the final configured turn marks the session complete without needing another provider decision;
- a completed/exhausted session cannot generate an additional question;
- completion reconciliation is idempotent;
- Features 001–010 remain passing, including speech-input/output security tests.

## Claim boundary
A CI pass establishes D4 integration evidence for the checked-out PR merge ref only. It does not establish AJ-device/browser compatibility, live external-provider quality, educational effectiveness, public deployment security, authentication, or multi-user authorization.
