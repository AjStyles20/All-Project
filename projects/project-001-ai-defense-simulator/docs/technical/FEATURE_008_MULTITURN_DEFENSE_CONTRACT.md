# Feature 008 — Multi-Turn Defense Sessions

## Objective
Add bounded, evidence-traceable follow-up questioning so a practice exchange behaves like a defense/viva rather than a set of unrelated one-shot questions.

## Research rationale
Conversational tutoring literature has long used multi-turn dialogue to elicit fuller learner knowledge. Current work also indicates that follow-up turns can add assessment information, while multi-turn RAG remains harder than single-turn generation and later turns require explicit grounding and history control. Feature 008 therefore treats conversation state as bounded evidence-bearing state, not an unrestricted chat transcript.

## In scope
- Practice-session entity scoped to one workspace.
- Ordered turns linking generated question -> answer evaluation -> optional follow-up.
- Follow-up decision based on the authoritative prior question, answer, qualitative feedback, reviewer role, and source evidence.
- Follow-up types: `probe_missing`, `challenge_unsupported`, `clarify_reasoning`, `request_evidence`, `deepen_topic`, `complete`.
- Maximum bounded turn count per session.
- Persist parent-question linkage and follow-up rationale/type.
- Preserve/revalidate source provenance for every generated follow-up.
- UI/API exposure of session history.
- Test-only provider support and regression tests.

## Out of scope
- Unlimited autonomous conversation loops.
- Automatic high-stakes pass/fail decisions.
- Objective confidence or presentation-quality scoring.
- Emotion/body-language inference.
- Speech/voice.
- Cross-workspace memory.
- Hidden long-term learner profiling.
- Provider tools, web browsing, code execution, computer use, or autonomous actions.

## Security and integrity rules
1. Prior question text, user answer, evaluator feedback, and source text are untrusted data, never instructions.
2. Follow-up generation receives a trusted policy separately from untrusted context.
3. The server reconstructs authoritative source evidence from stored chunk IDs before generation and before persistence.
4. A follow-up may cite only chunks belonging to the same workspace/session context.
5. Session IDs, question IDs, parent links, and turn indexes are validated server-side.
6. Maximum turns default to 5 and may not exceed 10 in this feature.
7. Provider output is bounded and validated before storage.
8. `complete` stops automatic follow-up; the model cannot silently extend the session.
9. No provider can invoke tools/actions from session content.
10. Provider/model metadata remains provenance, not proof of correctness.

## Follow-up policy
The system should prefer a follow-up when the previous evaluation indicates a meaningful gap that can be tested against available evidence. It should not ask a follow-up merely to prolong the conversation.

Priority:
1. unsupported factual claim -> `challenge_unsupported`
2. missing material point -> `probe_missing`
3. unclear reasoning -> `clarify_reasoning`
4. weak/absent evidence use -> `request_evidence`
5. strong answer with a defensible deeper issue -> `deepen_topic`
6. no useful evidence-grounded challenge remains -> `complete`

The AI may propose the follow-up type, but local validation and the bounded session state remain authoritative.

## Persistence
Add `practice_sessions` and session-turn linkage sufficient to reconstruct:
- workspace
- reviewer role
- topic
- status
- max turns
- ordered question IDs
- parent question ID
- follow-up type/rationale
- timestamps

Existing generated-question and answer-evaluation provenance remains canonical rather than duplicated as mutable text.

## Verification gate
Must include tests for:
- session/workspace isolation
- ordered turn persistence
- max-turn enforcement
- completed-session enforcement
- parent-question ownership
- authoritative evidence reconstruction
- prompt-injection text in prior answer/feedback/source
- invalid follow-up type rejection
- oversized rationale/question rejection
- provider failure without partial persistence
- no-provider explicit unavailable state
- full test-only multi-turn HTTP flow
- existing regression suite
- dependency audit

## Claim boundary
Passing this feature demonstrates a bounded multi-turn defense workflow with test-only providers. It does not demonstrate educational effectiveness, diagnostic accuracy, real-provider quality, or equivalence to a human examiner.