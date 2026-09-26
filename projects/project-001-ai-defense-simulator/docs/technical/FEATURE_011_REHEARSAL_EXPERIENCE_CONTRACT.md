# Feature 011 — End-to-End Rehearsal Experience

## Objective
Turn the verified Project 001 capabilities into one coherent, bounded defense/viva rehearsal flow without weakening provenance, security, or claim discipline.

## User flow
1. Start a defense session from a workspace using a topic, reviewer role, retrieval mode, and bounded turn count.
2. Land directly on the active turn rather than manually navigating through a history page first.
3. Read the reviewer question and its source evidence; optionally listen to reviewer speech.
4. Answer by text or optional microphone transcription, review/edit the transcript, then submit.
5. Review qualitative evidence-aware feedback.
6. Continue the same session with an evidence-grounded follow-up when configured.
7. Stop automatically at provider completion or the configured maximum turn count.
8. Return to a session summary showing progress, answered/unanswered state, and links to every turn.

## Security and trust boundaries
- Existing workspace scoping and provenance verification remain mandatory.
- No new authentication claim is introduced; this remains a local/single-user prototype until authentication/authorization is implemented and independently verified.
- Session identifiers never authorize cross-workspace access.
- User answers, retrieved evidence, generated questions, feedback, transcripts, and provider outputs remain untrusted data.
- No client-provided arbitrary provider endpoint, model instruction, TTS text, or tool instruction is accepted.
- Existing same-origin request guard, TrustedHostMiddleware, CSP, bounded uploads, provider timeouts, and controlled error responses remain regression gates.
- Session state transitions are server authoritative.
- Maximum turns remain hard-bounded to 10.
- Completion must not create additional questions.
- Public/multi-user deployment remains blocked on authentication, authorization, secure session management, HTTPS, CSRF strategy for authenticated cookie flows, rate limiting, and deployment verification.

## UX requirements
- Current turn and progress are immediately visible.
- Primary action is unambiguous: answer current turn, continue, or review completed session.
- Written question and feedback remain available even when speech features are unavailable.
- Speech remains opt-in and non-autoplay.
- Status is not conveyed by color alone.
- Keyboard operation and semantic labels remain required.
- Provider-not-configured states must degrade honestly rather than fabricate behavior.

## Acceptance criteria
- Session creation redirects to the first question while preserving a route back to the session.
- Question pages can identify when they belong to a rehearsal session and show turn/max-turn progress.
- After answer evaluation, the user can return to the owning session without searching manually.
- Session page identifies the current actionable turn and completion state.
- Maximum-turn completion is enforced server-side even if a provider would otherwise continue.
- Cross-workspace session/question association attempts fail.
- Existing question, evaluation, follow-up, speech-input, speech-output, provenance, and security regression tests continue to pass.
- New tests cover navigation/state behavior and maximum-turn completion.

## Not in scope
- Accounts/login or multi-user authorization.
- Public deployment.
- Automated objective grading.
- Emotion recognition or body-language scoring.
- Voice cloning.
- Realtime speech-to-speech.
- VR/3D audience.

## Definition of done for this feature
D4 Integrated in CI when the complete regression suite and dependency audit pass on the PR merge ref. D5 Live verified requires AJ-controlled browser/device rehearsal and, where used, credentialed provider checks. D6 documentation alignment follows independent verification.