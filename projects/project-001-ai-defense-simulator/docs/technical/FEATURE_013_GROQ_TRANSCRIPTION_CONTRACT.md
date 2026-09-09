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

## Verification result — 2026-09-09
- GitHub CI: PASS — `141 passed, 2 warnings`; dependency audit reported no known vulnerabilities.
- AJ Windows/Python 3.14: PASS — `141 passed, 2 warnings in 71.80s`.
- Live browser microphone recording: PASS.
- Stop-recording consent boundary: PASS — UI reported recording stopped and required the separate **Transcribe recording** action before upload.
- Live Groq transcription request: PASS — application log recorded `POST .../transcriptions` with HTTP `200 OK`.
- Transcript-to-editable-answer behavior: PASS — returned text populated the answer textarea for review/editing.
- No automatic answer submission: PASS — transcription completion did not trigger the separate `/answers` route; submission occurred only after the user explicitly selected **Submit for feedback**.
- Raw audio persistence claim remains unchanged: application response/path does not persist raw audio.

Observed transcription-quality limitation during the live test: a spoken answer intended to contain terms equivalent to `sequence numbers` and `retransmission timers` was transcribed as `sequential numbers` and `transmission timelines`. This does not invalidate the transport/consent integration, but it demonstrates that STT output must remain editable and must not be treated as authoritative user intent without review.

Feature 013 is therefore **LIVE VERIFIED for the bounded local prototype workflow**, not verified for universal transcription accuracy, all microphones/browsers, noisy environments, or production deployment.
