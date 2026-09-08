# Feature 009 Contract — Secure Speech Input for Practice Answers

## Status
APPROVED FOR BOUNDED EXECUTION

## Purpose
Allow a user to answer a practice question by microphone while preserving the existing text-answer path, security boundaries, provenance, privacy disclosures, and evidence-aware evaluation workflow.

## Platform / Stack
- Python / FastAPI backend
- server-rendered HTML/CSS + bounded JavaScript for microphone capture
- SQLite for existing answer/evaluation/session persistence
- provider-neutral `SpeechTranscriber` adapter
- text answer remains the authoritative downstream representation after transcription

## Core Privacy Rule
Microphone capture must never start automatically. Recording requires an explicit user gesture and visible recording state. Audio must not be persisted by default. If an external transcription provider is configured, the UI must disclose that captured audio is sent to that provider before the user records/submits it.

## Required Behavior
1. Text answers continue to work unchanged when speech is unavailable.
2. Add an explicit microphone control only when the browser supports required capture APIs.
3. Recording starts only after direct user interaction.
4. Recording has a visible stop/cancel state.
5. Audio is bounded before server processing.
6. Server accepts only an explicit media-type allowlist supported by the configured transcriber.
7. Client-supplied filename/extension is never trusted as proof of media type.
8. Introduce a provider-neutral `SpeechTranscriber` interface.
9. No real transcriber is configured by default.
10. If no transcriber exists, speech endpoint returns an explicit unavailable state; text answers remain usable.
11. Transcription output is bounded, validated plain text.
12. Transcript is returned to the user for review/editing before it is submitted as an answer.
13. Recording/transcription never automatically submits an answer or triggers evaluation.
14. No audio is written to the project SQLite database in this feature.
15. Provider/API secrets remain environment-only.
16. Provider errors do not expose raw bodies, credentials, or internal stack traces.

## Security Bounds
- maximum audio upload: 10 MiB in this feature unless a smaller provider-specific limit is configured
- maximum recording duration in UI: 120 seconds
- accepted initial browser capture types: WebM/Opus where supported; additional types require explicit adapter support and tests
- maximum returned transcript: 8000 characters, matching the existing answer bound
- no user-controlled provider base URL
- no provider tools/actions
- no automatic file-system persistence
- reject empty audio and unsupported/ambiguous content types
- same-origin mutation protections from Feature 006 remain active

## Trust Boundary
Audio bytes, browser metadata, transcript text, and provider output are untrusted data. They cannot redefine system policy, authorize actions, select provider endpoints, access other workspaces, or bypass the existing answer/evaluation validations.

## Accessibility / UX
- microphone is an enhancement, never mandatory
- every microphone action has a textual button/label
- recording state is communicated in text, not color only
- keyboard operation remains available
- transcript can be edited in the normal answer textarea
- text entry remains available if microphone permission is denied or unsupported

## Provider Direction
The first optional provider adapter may use an external transcription service only through trusted server configuration. Current OpenAI model documentation lists `GPT-Transcribe` as a high-accuracy speech-to-text option; exact request schema/endpoint must be verified against current official API documentation before implementation.

## Out of Scope
- realtime streaming transcription
- voice cloning
- speaker identification
- emotion detection
- confidence scoring from voice
- accent grading
- pronunciation grading
- biometric voice identity
- persistent raw audio library
- automatic TTS playback
- public/multi-user recording storage

## Verification Requirements
- no-provider behavior
- explicit recording controls in rendered UI
- text path regression remains passing
- upload size bound
- media-type allowlist
- empty/unsupported audio rejection
- transcript length/type validation
- no raw audio persistence
- provider-secret non-disclosure in errors
- transcription does not auto-submit answer
- cross-workspace answer/evaluation protections remain passing
- dependency audit remains passing

## Completion Boundary
Feature 009 is IMPLEMENTED when browser capture, bounded upload, provider-neutral transcription, transcript review/editing, and security tests exist. It is LIVE VERIFIED only after an authorized transcription provider is configured and exercised with explicit user consent on a real microphone/device.