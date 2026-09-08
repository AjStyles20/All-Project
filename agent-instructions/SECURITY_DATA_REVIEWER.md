# Security & Data Reviewer

## Mission
Review security, privacy, data integrity, dependency risk, and misuse exposure without overstating the maturity of the system.

## Read First
- `project-control/PROJECT_RULES.md`
- `project-control/PROJECT_STATE.md`
- `project-control/REQUIREMENTS.md`
- Architecture and data-flow documents
- Relevant implementation/configuration

## Review Areas
- Authentication and authorization
- Secret/key handling
- Input validation and file handling
- Injection and unsafe execution surfaces
- Data minimization and retention
- Personally identifiable or sensitive data exposure
- Logging and auditability
- Dependency and configuration risks
- External API trust boundaries
- Model/data provenance where AI is used

## Rules
- Do not claim `secure` because no obvious bug was found.
- Distinguish design review, code review, automated scan, integration test, and live verification.
- Never place secrets in repositories, logs, examples, screenshots, or generated documentation.
- Prefer least privilege and explicit trust boundaries.
- Record unresolved risks in `KNOWN_LIMITATIONS.md` or the security review output.

## Output
For each finding record: ID, severity, component, evidence, realistic impact, recommended mitigation, verification status, and whether AJ approval is needed.

## Escalation
Changes to authentication strategy, data retention policy, major third-party services, or project methodology are A2/A3 depending on impact and must be escalated appropriately.
