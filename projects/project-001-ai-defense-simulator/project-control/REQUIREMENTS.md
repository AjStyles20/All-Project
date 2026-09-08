# Project 001 Requirements

Statuses: PROPOSED / APPROVED / IMPLEMENTED / VERIFIED / REJECTED / PARKED

## Functional Requirements

| ID | Requirement | Priority | Status | Acceptance evidence |
|---|---|---:|---|---|
| FR-001 | User can provide presentation/defense source materials for a practice session. | Must | PROPOSED | Valid supported file ingested and visible to retrieval pipeline. |
| FR-002 | System can generate questions grounded in supplied materials and distinguish grounded from general questions. | Must | PROPOSED | Retrieval/context trace and verification tests. |
| FR-003 | User can select or configure panel/audience personas. | Must | PROPOSED | Persona configuration changes generated questioning behavior without changing project facts. |
| FR-004 | User can answer questions in an interactive practice session. | Must | PROPOSED | End-to-end session test. |
| FR-005 | System records a session transcript/history. | Must | PROPOSED | Persisted session can be reopened or summarized. |
| FR-006 | System produces feedback using explicit, explainable criteria rather than unexplained scores. | Must | PROPOSED | Feedback output maps to rubric criteria and evidence from response. |
| FR-007 | Microphone/speech input can be supported if architecture and environment make it practical. | Should | PROPOSED | Successful speech-to-text integration test; otherwise feature remains unavailable, not simulated. |
| FR-008 | Text-to-speech or spoken panel questions may be supported after core text workflow works. | Could | PROPOSED | Verified TTS integration. |

## Non-Functional Requirements

| ID | Requirement | Priority | Status |
|---|---|---:|---|
| NFR-001 | No fabricated citations, metrics, user data, session results, or system capabilities. | Must | APPROVED |
| NFR-002 | Core behavior must remain understandable and defendable by AJ. | Must | APPROVED |
| NFR-003 | The UI must be keyboard-accessible and must not rely only on color to communicate state. | Must | APPROVED |
| NFR-004 | Sensitive uploaded materials must not be exposed through logs or public repository commits. | Must | APPROVED |
| NFR-005 | The prototype should run on modest development hardware where feasible; heavy local AI models are not assumed. | Should | APPROVED |
| NFR-006 | Implementation status and testing evidence must remain synchronized with documentation. | Must | APPROVED |

## Academic / Evaluation Requirements

| ID | Requirement | Status |
|---|---|---|
| AR-001 | Literature review must precede strong novelty claims. | APPROVED |
| AR-002 | Comparable systems must be analyzed using an evidence matrix. | APPROVED |
| AR-003 | Any scoring/evaluation method must define what it measures and what it does not measure. | APPROVED |
| AR-004 | Claims about confidence, learning outcomes, or presentation improvement require evidence beyond model-generated feedback. | APPROVED |
| AR-005 | Chapter/methodology documentation must describe the implemented architecture, not an intended one. | APPROVED |

## Scope Rule
Requirements remain PROPOSED until research/architecture review or explicit AJ approval. The existence of this file does not mean every proposed feature will be implemented.
