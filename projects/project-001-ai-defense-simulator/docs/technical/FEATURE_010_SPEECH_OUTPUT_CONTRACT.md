# Feature 010 Contract — Optional Reviewer Speech Output

## Status
APPROVED FOR BOUNDED EXECUTION

## Purpose
Allow the user to listen to an already-generated reviewer question while preserving the authoritative visible text, accessibility, provider neutrality, and security/privacy boundaries.

## Platform / Stack
- Python / FastAPI backend
- server-rendered HTML/CSS + bounded external JavaScript
- provider-neutral `SpeechSynthesizer` interface
- optional server-side external TTS adapter

## Core Rules
1. Visible question text remains authoritative and always available.
2. Audio is optional; no workflow requires hearing it.
3. Audio never autoplays.
4. Synthesis starts only after explicit user interaction.
5. The client cannot submit arbitrary text to the TTS endpoint; the server loads the authoritative question text by workspace + question ID.
6. Workspace ownership is checked before synthesis.
7. No TTS provider is configured by default.
8. If no provider exists, return explicit unavailable behavior rather than fabricated audio.
9. Provider credentials remain server-side/environment-only.
10. Generated audio is not persisted by the application in this feature.
11. Provider output size and media type are bounded/validated.
12. Provider failures must not expose credentials or raw upstream error bodies.
13. No voice cloning or user-supplied voice models.
14. Voice selection is server-controlled from a small explicit allowlist.

## Bounds
- input text comes only from stored question text and therefore remains within the existing 1200-character question bound
- maximum generated audio payload: 5 MiB
- initial allowed output media type: `audio/mpeg`
- no arbitrary TTS instructions from client requests
- no arbitrary provider endpoint/base URL

## Accessibility / UX
- textual reviewer question is never replaced by audio
- a textual Listen button initiates synthesis/playback
- a Stop audio control is available after playback begins
- playback state is exposed as text via `aria-live`
- failure leaves the normal text workflow intact

## Provider Direction
Current OpenAI model documentation lists GPT-4o mini TTS as a speech-generation model. The first optional adapter may use it through the fixed server-side audio speech endpoint, while the core remains provider-neutral.

## Out of Scope
- voice cloning
- custom uploaded voices
- impersonation
- realtime speech-to-speech
- emotional/personality inference from the user
- automatic narration of uploaded private documents
- background autoplay
- persistent audio library
- voice-based grading

## Verification Requirements
- provider-not-configured behavior
- cross-workspace question rejection
- server uses authoritative question text rather than client text
- output size/media validation
- fixed provider endpoint under mocked transport
- provider-error secret non-disclosure
- UI contains no autoplay
- synthesis/fetch only under explicit Listen action
- text question remains rendered
- generated blob URLs are revoked when replaced/stopped/unloaded where practical
- full regression suite and dependency audit remain passing

## Completion Boundary
Feature 010 is IMPLEMENTED after provider-neutral synthesis, bounded server endpoint, optional adapter, accessible non-autoplay browser controls, and security tests exist. It is LIVE VERIFIED only after a real provider and browser audio path are exercised on an authorized user device.