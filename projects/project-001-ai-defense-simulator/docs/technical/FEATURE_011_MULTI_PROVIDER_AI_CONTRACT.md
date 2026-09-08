# Feature 011 — Multi-Provider AI Foundation

## Purpose

Allow Project 001 to use a selectable text-generation provider without making the application dependent on one vendor or weakening the existing provider-security boundary.

## Supported selections

`P001_AI_PROVIDER` is allowlisted to:

- `disabled`
- `openai`
- `groq`

If `P001_AI_PROVIDER` is unset, the pre-Feature-011 `P001_OPENAI_ENABLED` behavior is preserved for backward compatibility.

## OpenAI preservation

The existing OpenAI adapters are retained. Feature 011 does not delete, replace, redirect, or convert the OpenAI integration. Existing OpenAI environment configuration can be used again when API credit/access is available.

OpenAI-backed embeddings, multi-turn follow-up, speech-to-text, and text-to-speech remain separate existing capabilities. Feature 011 does not claim that Groq replaces these yet.

## Groq scope

Groq currently supplies:

1. source-grounded reviewer question generation;
2. structured qualitative answer evaluation.

Default text model: `openai/gpt-oss-20b`.

The Groq adapter uses a fixed service base and fixed chat-completions path. An arbitrary provider URL cannot be supplied through configuration.

## Groq environment configuration

Required when Groq is selected:

- `P001_AI_PROVIDER=groq`
- `P001_GROQ_API_KEY=<secret>`

Optional bounded settings:

- `P001_GROQ_TEXT_MODEL`
- `P001_GROQ_TIMEOUT_SECONDS` (2–60 seconds)

Secrets must remain outside tracked source files and documentation.

## Security contract

- Retrieved document evidence, questions, and user answers are untrusted data.
- Trusted policy is sent separately from untrusted review/evaluation context.
- No Groq tools, browsing, code execution, or external actions are configured.
- Provider base URL is not user-configurable.
- Provider errors are sanitized; remote response bodies and credentials are not surfaced to application users.
- Malformed or missing provider output fails closed.
- Evaluation uses a strict JSON Schema and still passes through the application’s existing local validation before persistence.
- Workspace/evidence ownership and provenance validation remain server-side application responsibilities and are unchanged.

## Retrieval behavior

Feature 011 does not add a Groq embedding adapter. Therefore when Groq is selected alone:

- lexical retrieval remains available;
- a requested hybrid search may truthfully fall back to lexical according to the existing retrieval contract;
- semantic retrieval must not be represented as configured unless a real embedding provider is present.

## Non-goals for this feature

- Groq speech transcription;
- Groq or third-party text-to-speech;
- Groq multi-turn follow-up generation;
- automatic provider failover;
- arbitrary OpenAI-compatible base URLs;
- public/multi-user production hardening.

These require separate implementation and verification.

## Verification requirements

Before Feature 011 can be considered live-verified:

1. automated tests and dependency audit pass;
2. AJ configures a Groq key locally without exposing it in chat/source control;
3. a real grounded question is generated from an uploaded source;
4. provenance remains visible and correct;
5. a real answer evaluation succeeds and its evidence references validate;
6. provider failure behavior is observed without credential leakage.

CI verification alone is implementation verification, not live-provider verification.

## Live verification record — 2026-09-08

Status: **LIVE VERIFIED for the Feature 011 scope defined above.**

Observed on AJ's Windows 10 development machine using Python 3.14 and the project virtual environment:

- `python -m pytest -q` completed with **126 passed, 2 warnings**.
- GitHub Actions CI completed with **126 passed, 2 warnings**.
- `pip-audit` reported **No known vulnerabilities found**.
- Runtime provider selection showed `groq / openai/gpt-oss-20b` for question generation and answer evaluation while OpenAI was disabled.
- Semantic retrieval remained truthfully **not configured**.
- A live source-grounded technical-review question was generated from `Computer Networks - Complete Study Guide.pdf` for the topic `TCP reliability mechanisms`.
- The generated question used lexical retrieval and displayed page-level evidence provenance from the uploaded PDF, including pages 7 and 6.
- A live answer (`I am not sure.`) was submitted and Groq returned the five required qualitative feedback categories with evidence references; the evaluation was persisted and displayed successfully.
- Earlier live provider failures were surfaced only as the sanitized application message `Question provider failed`; no credential or remote response body was displayed by the application.

This verification does **not** extend to semantic embeddings, Groq multi-turn follow-up, speech transcription, reviewer TTS, public deployment, authentication/authorization, or production hardening.