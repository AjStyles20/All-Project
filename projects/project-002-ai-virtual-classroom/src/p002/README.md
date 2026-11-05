# p002 package (first implementation, 2026-11-05)

Phases 1 and 2 of Pass 017 §15: the deterministic trust and mastery kernels, built and tested before any language model is connected.

| Module | Pass 017/018 |
|---|---|
| `domain.py` | Types: authority, status, edges, assistance ladder L0–L6, mastery and issue states |
| `provenance.py` | APLDG kernel: sources, claims, derivations, promotion, supersession and conflict propagation, explanations |
| `mastery.py` | PGAIC kernel: attempts, help escalation, mastery state machine, near misses, Knowledge Issues |
| `roles.py` | Role contracts; two deterministic AI stand-in roles for the laundering tests (no model connected) |
| `course.py` | The SQL JOIN benchmark course: v1/v2 notes, a forum post with an embedded instruction, an unsupported AI claim, questions with a six-step hint ladder |
| `evaluation.py` | Random-course and simulated-learner evaluation against the §14 gates |
| `app.py`, `static/` | Single-user web app (local only, per-run token) |

The planned split into sub-packages (`domain/`, `provenance/` …) was simplified to one module per area while the code is small.
