# Feature 013 — Groq Speech-to-Text Contract

## Purpose
Add an optional Groq speech-to-text adapter to the existing microphone-answer workflow without removing the preserved OpenAI transcription adapter or weakening the provider-neutral speech safety boundary.

## Provider selection
`P001_SPEECH_PROVIDER` accepts only:
- `auto` (default)
- `groq`
- `openai`
- `disabled`

In `auto`, Groq STT is selected when the active text provider is Groq. Otherwise, the existing OpenAI STT adapter is used only when OpenAI is explicitly enabled and configured.

Groq configuration:
- `P001_GROQ_API_KEY` — required when Groq STT is selected; environment only.
- `P001_GROQ_TRANSCRIPTION_MODEL` — optional; default `whisper-large-v3-turbo`.
- `P001_GROQ_TIMEOUT_SECONDS` — reuses the bounded Groq provider timeout configuration.

## Fixed external boundary
Groq STT uses only the fixed base `https://api.groq.com/openai/v1` and the fixed path `/audio/transcriptions`. No arbitrary provider URL is accepted.

## Existing microphone safety contract preserved
- Recording is user-initiated.
- Stop recording does not transmit audio.
- Transcription is a separate explicit user action.
- Transcript populates the answer box only; it never auto-submits an answer.
- Raw audio is not persisted by Project 001.
- Server enforces the existing 10 MiB maximum audio payload, below Groq free-tier file limits.
- Only the provider-neutral audio media-type allowlist is accepted.
- Workspace/question ownership and provenance are checked before provider transmission.
- Transcript length and shape are validated before returning to the browser.
- Provider errors are sanitized; raw provider response bodies and credentials are not returned.

## Scope exclusions
Feature 013 does not add:
- reviewer TTS through Groq;
- live streaming transcription;
- speaker identification;
- emotion, confidence, accent, pronunciation, or identity scoring;
- automatic answer submission;
- audio persistence;
- semantic embeddings.

## Verification gates
1. Unit/security tests for fixed endpoint, multipart request, invalid response handling, provider error sanitization, media-type validation, and provider selection.
2. Full regression suite and dependency audit in GitHub CI.
3. Local Windows/Python 3.14 regression suite.
4. Live browser microphone test with explicit record → stop → transcribe flow.
5. Verify transcript appears in the editable text answer box and is not submitted automatically.

Until gate 4-5 pass, Groq STT is implemented and CI-verified only, not live-browser verified.
