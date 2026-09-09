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
- Preconditions: Groq selected; OpenAI disabled.
- Procedure: Run `python -m pytest -q`.
- Expected result: Existing and Feature 012 tests pass without failures.
- Observed result: `130 passed, 2 warnings in 44.30s`.
- Status: PASS
- Evidence: User-supplied PowerShell output.
- Performed by: AJ

### TE-011 — Feature 012 live Groq follow-up generation
- Date: 2026-09-09
- Feature/subsystem: Project 001 — bounded multi-turn defense
- Test type: Live / User / Integration
- Environment: Windows local Uvicorn at `127.0.0.1:8000`; Groq model `openai/gpt-oss-20b`.
- Preconditions: Active defense session for `TCP reliability mechanisms`; Turn 1 answered and evaluated.
- Procedure: Return to the defense-session page and select `Generate evidence-grounded follow-up`.
- Expected result: A second turn is generated from authoritative session context and the session blocks further follow-up until Turn 2 is answered.
- Observed result: Turn 2 was generated with type `challenge_unsupported` and question `Can you clarify why congestion control and flow control are not considered reliability mechanisms according to the evidence?`; rationale was persisted and displayed; the page then displayed `Answer the current question before requesting a follow-up.`
- Status: PASS
- Evidence: User-supplied browser screenshots and Uvicorn log showing POST to `/sessions/.../follow-up` followed by `Follow-up question generated.`
- Performed by: AJ
- Notes: This establishes live provider-backed multi-turn operation. A quality limitation was also discovered: the follow-up phrased a categorical negative more strongly than the evidence directly supports; this is tracked separately and does not invalidate the transport/session/live-integration PASS.

### TE-012 — Feature 012 Turn 2 answer evaluation
- Date: 2026-09-09
- Feature/subsystem: Project 001 — multi-turn evaluation continuity
- Test type: Live / User / Integration
- Environment: Same as TE-011.
- Procedure: Answer Turn 2 and submit for qualitative feedback.
- Expected result: The follow-up question can be answered and evaluated through the same evidence-aware evaluator path.
- Observed result: Turn 2 answer was accepted and evaluated; feedback persisted and displayed.
- Status: PASS
- Evidence: User-supplied screenshots and Uvicorn POST/redirect log for question `14c89793-47b6-4129-b163-3efd49757bed`.
- Performed by: AJ
- Notes: The evaluator/follow-up pair exposed an evidence-framing inconsistency around negative claims. A Groq follow-up grounding guard was added afterward to prevent absence-as-negation reasoning in future follow-ups.

### TE-013 — Feature 015A Windows regression suite
- Date: 2026-09-09
- Feature/subsystem: Project 001 — defense playback and review controls
- Test type: Regression / User
- Environment: Windows 10, Python 3.14, project `.venv`, branch `p001/feature-defense-playback-review`
- Procedure: Run `python -m pytest -q`.
- Expected result: Existing suite plus Feature 015A tests pass without failures.
- Observed result: `146 passed, 2 warnings in 62.97s`.
- Status: PASS
- Evidence: User-supplied PowerShell output.
- Performed by: AJ
- Notes: The two warnings are Starlette/AnyIO deprecation warnings; zero tests failed.

### TE-014 — Feature 015A local playback and rate control
- Date: 2026-09-09
- Feature/subsystem: Project 001 — browser reviewer playback
- Test type: Live / User / Accessibility
- Environment: Windows browser against local Uvicorn at `127.0.0.1:8000`; local browser speech fallback.
- Preconditions: Reviewer question page with written authoritative question; server TTS not required.
- Procedure: Open the question page, inspect Play / Replay, Pause, Resume, Stop and bounded rate options; select `0.75×`; start playback.
- Expected result: Control set is present, no autoplay occurs, and selected rate is applied to browser speech.
- Observed result: UI displayed Play / Replay, Pause, Resume, Stop and rates `0.75×`, `1×`, `1.25×`, `1.5×`; status displayed `Playing reviewer question with local browser speech at 0.75×.`
- Status: PASS
- Evidence: User-supplied browser screenshots.
- Performed by: AJ
- Notes: This record does not by itself verify Pause, Resume, Stop interruption behavior or Previous/Next existing-turn navigation; those remain separate live checks.
