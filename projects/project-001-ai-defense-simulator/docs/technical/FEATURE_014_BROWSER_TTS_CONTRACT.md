# Feature 014 — Zero-Cost Browser Reviewer TTS Contract

## Purpose
Provide optional reviewer-question speech without requiring a paid external TTS provider, while preserving the existing OpenAI server TTS implementation for future use.

## Selection behavior
- When server TTS is configured, Project 001 attempts the existing server-generated audio path first.
- If server TTS is unavailable and the browser exposes the Web Speech synthesis API, the written reviewer question is spoken locally by the browser/device speech engine.
- If neither path is available, speech controls fail closed and the visible written question remains fully usable.

## Trust and authority boundary
- The visible written reviewer question is authoritative.
- Browser speech is only a rendering of that visible question text; it does not create or alter question content.
- No reviewer speech starts automatically.
- Speech starts only after the explicit **Listen to reviewer** action.
- **Stop audio** cancels local browser speech and stops server audio.
- The browser fallback does not send question text to a Project 001 TTS provider.
- Browser/device speech voices are platform-dependent and are not claimed to be identical across browsers or operating systems.

## Existing OpenAI TTS preserved
Feature 014 does not delete or replace Feature 010. The existing fixed server speech endpoint, provider adapter, voice configuration, size limits, and sanitized error behavior remain available whenever OpenAI TTS is configured.

## Scope exclusions
Feature 014 does not add:
- voice cloning;
- examiner identity simulation;
- emotion or personality inference;
- guaranteed offline voice availability;
- guaranteed voice quality or accent;
- autoplay;
- audio persistence;
- speech scoring.

## Verification gates
1. Static/regression tests confirm local speech invocation is reachable only from the explicit Listen control.
2. Stop cancels local speech.
3. Existing server TTS path remains present.
4. Full regression suite and dependency audit pass.
5. AJ live browser verification confirms Listen produces audible reviewer speech and Stop interrupts it.

Until gate 5 passes, Feature 014 is implemented/CI-verified only, not live-browser verified.
