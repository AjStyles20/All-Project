# Feature 015A — Defense Playback & Session Review Controls

## Problem statement
During oral-defense rehearsal, users may miss or partially understand a spoken reviewer question, need a slower or faster listening pace, or want to revisit earlier turns and feedback. A one-shot speech control and an unstructured turn list make that review less usable, especially for longer multi-turn sessions.

## Scope
Feature 015A adds bounded playback and review controls without changing the authority of the defense-session engine.

### Question playback
- Play / Replay the visible authoritative reviewer question.
- Pause active speech when supported by the current playback path.
- Resume paused speech when supported.
- Stop and clear active speech.
- Select one of four bounded playback rates: 0.75×, 1×, 1.25×, 1.5×.
- Server audio applies rate changes to the current HTML audio object.
- Browser speech applies the selected rate when an utterance starts. A rate change during active browser speech is applied on replay rather than pretending all browsers can safely retime an in-progress utterance.

### Session review navigation
- Previous/Next navigation moves only among turns that already exist in the session.
- Navigation uses stable in-page turn anchors and does not create, skip, answer, or mutate a defense turn.
- Unanswered-current-question blocking remains authoritative.
- New follow-up generation remains a separate explicit session action after the current turn is answered and evaluated.

## Security and claim boundaries
- No autoplay.
- No new external service, credential, or network destination.
- Browser speech still uses the visible reviewer question as its source.
- Server TTS remains optional and preserved.
- Playback controls do not modify question text, evidence, answers, evaluations, reviewer role, turn ordering, or session state.
- Previous/Next is review navigation, not examiner progression.
- No objective claim is made that playback controls improve educational outcomes without separate study evidence.

## Accessibility rationale
- Adjustable pacing can help users who need slower or faster spoken delivery.
- Written question text remains available at all times and remains authoritative.
- Controls use native buttons/select elements and status messages remain exposed through the existing live region.

## Verification requirements
Automated verification must confirm:
- explicit user action remains required before speech starts;
- no autoplay path exists;
- pause/resume/stop handlers are present;
- only allowlisted playback rates are accepted;
- browser and server playback paths use the selected bounded rate;
- Previous/Next exists only as navigation among existing turns;
- the existing unanswered-turn and explicit-follow-up gates remain present.

Live AJ-device verification should confirm:
- Play / Replay speaks the reviewer question;
- Pause suspends playback;
- Resume continues playback;
- Stop interrupts playback;
- at least two speed settings produce observably different pacing;
- Previous/Next moves between existing turns without generating a new question.
