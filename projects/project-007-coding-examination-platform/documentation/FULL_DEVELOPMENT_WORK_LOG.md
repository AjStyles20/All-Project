# P001 Full Development Work Log

## 2026-09-23 — Full-development transition
**Decision:** transition from research-critical vertical-slice implementation to full software-product development while preserving the frozen research experiment.

**Method:** Agile iterative and incremental SDLC with explicit research/change-control gates. The project does not claim formal Scrum.

**Design work opened:** actor model; functional/non-functional requirements; use-case baseline; high-level architecture; candidate-examination activity flow; evidence-gap verification activity flow; logical ERD baseline; submission-to-verification sequence baseline.

**Implementation order:** authentication/RBAC -> operational examination/session/submission domain -> persistence/schema -> APIs -> lightweight UI -> integration/security/system testing -> deployment hardening.

**Documentation rule:** every material increment must update requirements, design/diagrams, RTM, tests/evidence, and this work log.

**Research boundary:** full product development is authorized, but external assessor evidence and frozen experimental definitions remain controlled. Product completeness must not be represented as scientific validation.
