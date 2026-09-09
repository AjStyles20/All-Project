# Feature 012 — Groq Bounded Multi-Turn Defense Sessions

## Purpose

Extend the existing bounded defense-session engine so the selected Groq text provider can generate evidence-grounded follow-up questions without replacing the existing session, provenance, evaluation, or OpenAI implementations.

## Scope

When `P001_AI_PROVIDER=groq`, Groq may provide:

1. the initial source-grounded reviewer question;
2. qualitative answer evaluation;
3. bounded follow-up generation for an active defense session.

The existing OpenAI follow-up adapter remains preserved and is selected when OpenAI is the active text provider.

## Existing session constraints retained

- Default maximum session length: 5 turns.
- Hard maximum: 10 turns.
- A follow-up cannot be generated until the current question has an answer evaluation.
- Follow-up types remain allowlisted to:
  - `probe_missing`
  - `challenge_unsupported`
  - `clarify_reasoning`
  - `request_evidence`
  - `deepen_topic`
  - `complete`
- `complete` must contain no question.
- The server independently reloads authoritative session, question, evaluation, evidence, workspace ownership, and provenance before a follow-up is generated or persisted.
- Session state is rechecked immediately before persistence to detect stale/concurrent turn changes.

## Groq provider boundary

- Fixed base: `https://api.groq.com/openai/v1`.
- Fixed path: `/chat/completions`.
- No arbitrary provider URL is accepted.
- Groq API credentials remain environment-only.
- The selected bounded model and timeout reuse Feature 011 Groq settings.
- No tools, browsing, code execution, MCP, or external actions are configured.

## Prompt-trust boundary

The trusted follow-up policy is sent as the system message.

The following are serialized into a separate untrusted user-data envelope:

- session and turn identifiers;
- reviewer role and topic;
- prior question;
- prior user answer;
- qualitative feedback;
- source evidence and provenance.

Instructions or role changes embedded in the prior answer, feedback, or source evidence are data and must not override the trusted system policy.

## Structured output

Groq follow-up output must conform to a strict JSON Schema containing exactly:

- `follow_up_type` — one allowlisted type;
- `rationale` — concise text;
- `question` — string or null.

Provider output still passes through the application-level `validate_followup_result` gate before persistence. Malformed JSON, unknown types, an invalid question, or a non-null question for `complete` fails closed.

## Truthful capability reporting

Feature 012 adds Groq follow-up generation only. It does not add:

- semantic embeddings;
- speech transcription;
- reviewer TTS;
- public/multi-user production hardening;
- unlimited conversation.

## Verification requirements

Feature 012 can be marked live-verified only after:

1. automated tests and dependency audit pass;
2. AJ pulls the Feature 012 branch on the Windows/Python environment;
3. a real Groq-backed defense session starts from uploaded evidence;
4. AJ answers the first question and receives evaluation;
5. a real Groq follow-up is generated from the authoritative answer/evaluation/evidence context;
6. the follow-up remains grounded in visible source evidence;
7. the maximum-turn and completion behavior remains bounded;
8. no credential or remote provider body is exposed on provider failure.

CI verification alone is not live-provider verification.
