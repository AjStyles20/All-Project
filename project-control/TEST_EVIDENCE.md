# Test Evidence

All verification evidence should be reproducible where practical. Do not record a PASS without the test, environment, and observed result.

## Test Record Template

### TE-XXX — Test name
- Date:
- Requirement(s):
- Feature/subsystem:
- Test type: Unit / Integration / Live / User / Accessibility / Security / Regression
- Environment:
- Preconditions:
- Procedure:
- Expected result:
- Observed result:
- Status: PASS / FAIL / PARTIAL / NOT RUN
- Evidence:
- Performed by:
- Notes:

---

### TE-001 — GitHub repository access
- Date: 2026-09-08
- Requirement(s): R-013
- Feature/subsystem: Connected technical workspace
- Test type: Live
- Environment: ChatGPT GitHub connector
- Procedure: Query authenticated repository list and retrieve `AjStyles20/All-Project`; then create repository files.
- Expected result: Repository is visible and write operations succeed.
- Observed result: Repository was visible with write/admin permissions and file creation returned successful commit SHAs.
- Status: PASS
- Performed by: ChatGPT

### TE-002 — Google Drive account connection
- Date: 2026-09-08
- Requirement(s): R-013
- Feature/subsystem: Academic/supporting workspace
- Test type: Live
- Environment: ChatGPT Google Drive connector
- Procedure: Query connected Drive profile.
- Expected result: Connected profile is returned successfully.
- Observed result: Connected profile returned successfully.
- Status: PASS
- Performed by: ChatGPT

### TE-003 — Work orchestration
- Status: NOT RUN

### TE-004 — Codex shared-state handoff
- Status: NOT RUN

### TE-005 — Feature 011 Windows regression suite
- Date: 2026-09-08
- Feature/subsystem: Project 001 — Multi-Provider AI Foundation
- Test type: Regression / User
- Environment: Windows 10, Python 3.14, project `.venv`, branch `p001/feature-multi-provider-ai`
- Preconditions: Groq selected as runtime AI provider; OpenAI disabled.
- Procedure: Run `python -m pytest -q`.
- Expected result: Existing and Feature 011 tests pass without failures.
- Observed result: `126 passed, 2 warnings in 56.90s`.
- Status: PASS
- Evidence: User-supplied PowerShell output in verification session.
- Performed by: AJ
- Notes: Warnings are existing Starlette/AnyIO deprecation warnings; no test failures.

### TE-006 — Feature 011 Groq grounded question generation
- Date: 2026-09-08
- Feature/subsystem: Project 001 — Groq question generation
- Test type: Live / User / Integration
- Environment: Windows local Uvicorn at `127.0.0.1:8000`; `P001_AI_PROVIDER=groq`; model `openai/gpt-oss-20b`; OpenAI disabled.
- Preconditions: Workspace `Test 001` contains extracted `Computer Networks - Complete Study Guide.pdf`.
- Procedure: Generate a technical-review question for topic `TCP reliability mechanisms` with hybrid requested while semantic embeddings are unavailable.
- Expected result: Application truthfully falls back to lexical retrieval, sends bounded evidence to Groq, returns one grounded question, persists it, and displays provenance.
- Observed result: Generated question: `What reliability mechanisms does TCP use to ensure ordered, error-free delivery, as described in the evidence?` Retrieval shown as lexical. Evidence displayed from the uploaded PDF with page provenance including pages 7 and 6.
- Status: PASS
- Evidence: User-supplied browser screenshots and page text.
- Performed by: AJ
- Notes: Semantic retrieval remained `not configured`, as required by the Feature 011 contract.

### TE-007 — Feature 011 Groq answer evaluation
- Date: 2026-09-08
- Feature/subsystem: Project 001 — Groq answer evaluation
- Test type: Live / User / Integration
- Environment: Same environment as TE-006.
- Preconditions: Grounded question from TE-006 exists with authoritative evidence references.
- Procedure: Submit answer `I am not sure.` for qualitative feedback.
- Expected result: Groq returns all five required qualitative feedback categories, evidence references validate, result persists, and no numeric grade is invented.
- Observed result: Evaluation persisted and displayed with summary plus `source_content_correctness`, `completeness`, `evidence_use`, `reasoning_clarity`, and `uncertainty_unsupported_statements`; evaluator identity displayed as `groq / openai/gpt-oss-20b`; no overall numeric score was claimed.
- Status: PASS
- Evidence: User-supplied browser screenshot and rendered evaluation text.
- Performed by: AJ

### TE-008 — Feature 011 sanitized provider failure behavior
- Date: 2026-09-08
- Feature/subsystem: Project 001 — Provider error handling
- Test type: Live / Security
- Environment: Windows local Uvicorn during Groq verification.
- Procedure: Observe application behavior for failed live question-provider requests before successful generation.
- Expected result: User-facing failure is sanitized and does not disclose credential or remote response body.
- Observed result: Application displayed only `Question provider failed`; Uvicorn showed the redirect/error flow and no API key or remote provider body.
- Status: PASS
- Evidence: User-supplied browser screenshot and PowerShell output.
- Performed by: AJ
- Notes: Exact upstream failure cause was not established from the sanitized application output and is not inferred.

### TE-009 — Feature 011 GitHub CI and dependency audit
- Date: 2026-09-08
- Feature/subsystem: Project 001 — Multi-Provider AI Foundation
- Test type: CI / Regression / Security
- Environment: GitHub Actions, Ubuntu 24.04, Python 3.12.14
- Procedure: Compile application/tests, run full pytest suite, run `pip-audit -r requirements.txt`.
- Expected result: Compilation succeeds, all tests pass, dependency audit reports no known vulnerabilities.
- Observed result: `126 passed, 2 warnings in 2.68s`; `No known vulnerabilities found`.
- Status: PASS
- Evidence: GitHub Actions workflow run 34272670176, job `test-and-audit`.
- Performed by: GitHub Actions

### TE-010 — Feature 012 Windows regression suite
- Date: 2026-09-09
- Feature/subsystem: Project 001 — Groq bounded multi-turn defense
- Test type: Regression / User
- Environment: Windows 10, Python 3.14, project `.venv`, branch `p001/feature-groq-multiturn`
- Preconditions: `P001_AI_PROVIDER=groq`, Groq key present, model `openai/gpt-oss-20b`, OpenAI disabled.
- Procedure: Run `python -m pytest -q` after switching to Feature 012 branch.
- Expected result: Existing and Feature 012 tests pass without failures.
- Observed result: `130 passed, 2 warnings in 44.30s`.
- Status: PASS
- Evidence: User-supplied PowerShell output.
- Performed by: AJ
- Notes: Same existing Starlette/AnyIO deprecation warnings; no test failures.

### TE-011 — Feature 012 live bounded-session setup and answer evaluation
- Date: 2026-09-09
- Feature/subsystem: Project 001 — Groq bounded multi-turn defense
- Test type: Live / User / Integration
- Environment: Windows local Uvicorn at `127.0.0.1:8000`; Groq selected; OpenAI disabled.
- Preconditions: Workspace `Test 001` with extracted Computer Networks source; Feature 012 branch active.
- Procedure: Start a bounded defense session for `TCP reliability mechanisms`, technical reviewer, maximum 5 turns; open Turn 1; submit answer `It uses reliability, congestion control, and flow control mechanisms.`; allow Groq evaluation to persist.
- Expected result: Session starts, Turn 1 is attached, follow-up remains blocked until an answer exists, answer evaluation succeeds, and the session remains active awaiting an explicit follow-up request.
- Observed result: Session page showed `Status: active`, `Maximum turns: 5`, Turn 1 with `Answer this question`, and `Answer the current question before requesting a follow-up.` before answering. After submission, Groq qualitative evaluation persisted and correctly identified that the answer conflated reliability with congestion/flow control and omitted sequence numbers, ACKs, and retransmission timers.
- Status: PASS
- Evidence: User-supplied browser screenshots and Uvicorn/PowerShell logs.
- Performed by: AJ
- Notes: This verifies session creation, turn gating, and evaluation. It does NOT yet verify a Groq-generated Turn 2 follow-up.

### TE-012 — Feature 012 live Groq follow-up generation
- Date: 2026-09-09
- Feature/subsystem: Project 001 — Groq bounded multi-turn defense
- Test type: Live / User / Integration
- Environment: Same as TE-011.
- Preconditions: TE-011 completed; current session remains active; Turn 1 has a persisted evaluation.
- Procedure: Return to the defense-session page and request the next follow-up.
- Expected result: Groq generates one bounded evidence-grounded Turn 2 follow-up (or explicitly completes the session), with allowed follow-up type and preserved parent/evidence provenance.
- Observed result: Not yet supplied.
- Status: NOT RUN
- Evidence: —
- Performed by: AJ
