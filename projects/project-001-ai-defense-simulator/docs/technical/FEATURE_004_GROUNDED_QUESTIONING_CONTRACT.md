# Feature 004 Contract — Source-Grounded Question Generation

## Status
APPROVED FOR BOUNDED EXECUTION

## Purpose
Generate review/defense questions from retrieved user-supplied evidence while preserving source provenance and treating retrieved content as untrusted data rather than trusted instructions.

## Required Behavior
1. Introduce a provider-neutral `QuestionGenerator` interface; no vendor/model is mandatory.
2. No real LLM provider is configured by default.
3. When no provider is configured, the API must explicitly report question generation as unavailable rather than fabricate a question.
4. Question generation receives bounded evidence from one workspace only.
5. Retrieved document text must be clearly delimited and labelled as untrusted evidence in provider requests.
6. Retrieved text must not be able to redefine system policy, permissions, reviewer role, tool access, or output contract.
7. Every stored/generated question must preserve:
   - workspace ID
   - question ID
   - reviewer role
   - question text
   - evidence chunk IDs
   - document IDs / filenames / locators
   - retrieval mode/status
   - provider/model metadata when configured
   - creation timestamp
8. Reviewer role is selected from an allowlist for this feature.
9. Provider output is validated for type and length before persistence/return.
10. The application must not present generated questions as factually correct merely because a model produced them.

## Reviewer Roles (initial allowlist)
- technical
- methodology
- evidence
- security_privacy
- product_usability

## Security Requirements
- workspace existence/scoping enforced before retrieval/generation;
- topic/query and generated question lengths bounded;
- retrieved evidence count and per-chunk text size bounded;
- no secrets/system prompts included in returned provenance;
- provider failures return controlled errors without stack traces;
- indirect prompt-injection strings in uploaded evidence are treated as data and cannot alter the wrapper instruction;
- deterministic fake provider may be used only in tests and must be marked test-only;
- no external tool/action execution from model output.

## Retrieval Dependency
Feature 004 uses the existing lexical/hybrid retrieval layer. If semantic retrieval is not configured, lexical retrieval may still supply evidence. The response must disclose the effective retrieval mode.

## Out of Scope
- answer evaluation;
- automatic grading;
- speech input/output;
- multi-turn follow-up logic;
- autonomous web/tool access;
- real provider selection or API-key onboarding;
- claim that generated questions improve defense performance.

## Verification Gate
- no-provider path returns explicit unavailable state;
- fake-provider generation preserves provenance;
- reviewer-role allowlist enforced;
- workspace isolation enforced;
- indirect prompt-injection fixture does not alter trusted request wrapper;
- provider output length/type validation fails closed;
- no evidence/source metadata is lost;
- full prior regression suite remains passing;
- dependency audit remains passing.

## Completion Boundary
Feature 004 is IMPLEMENTED/CI VERIFIED when the interface, safe request construction, provenance storage, API path, and test-provider verification pass. It is LIVE VERIFIED for AI question generation only after a real provider/model is configured and a recorded real request succeeds.
