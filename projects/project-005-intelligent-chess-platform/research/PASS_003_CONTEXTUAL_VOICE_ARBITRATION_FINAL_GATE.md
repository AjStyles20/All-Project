# P010 — Pass 003: Contextual Voice Arbitration Final Gate

## Scope
This pass attacks the corrected P010 concept: a voice-enabled online chess platform with an automated arbiter/moderator whose rulings depend on speech content, board state, speaker role, game phase, match contract and evidence confidence.

## Prior-art collisions
- Generic online chess platforms are established.
- Voice/video interaction around chess is established.
- Real-time voice toxicity moderation is established in online games.
- Context-aware and multimodal content moderation are established.
- Automated/assisted sports officiating and appeal/accountability concerns are established.
- Chess fair-play detection and explainable evidence systems are established.
- FIDE online regulations already treat microphones, cameras, approved applications, outside assistance, player conduct, sanctions and appeals as legitimate arbiter concerns.

Therefore none of the following is a novelty claim: voice chat, video chat, speech-to-text, profanity/toxicity detection, automated warnings/mutes, chess rules QA, generic anti-cheat detection, use of board state, or use of multiple contextual features in classification.

## Surviving bounded research problem
The remaining defensible problem is not moderation in general, but game-state-grounded adjudication of live chess speech under explicit match policies.

A spoken utterance can change meaning depending on:
- who said it (player, opponent, spectator/third party);
- when it was said (before, during, after game; whose move);
- current board state and legal moves;
- the declared match contract;
- recent conversation history;
- evidence quality and uncertainty.

Example: “Knight f6 is weak” can be ordinary banter in one contract, strategic assistance in another, irrelevant after the game, or evidence of third-party coaching when spoken by another person during play.

## Frozen candidate hypothesis H5
**H5 — Contextual Voice Arbitration:** incorporating chess-board state, speaker role, game phase and explicit match rules into live-speech adjudication can improve classification of permitted conduct, misconduct, prohibited assistance and uncertain cases while reducing false penalties relative to generic speech-only moderation.

## Proposed decision states
- NO VIOLATION
- CONDUCT WARNING
- POSSIBLE RULE VIOLATION
- HIGH-CONFIDENCE VIOLATION
- INSUFFICIENT EVIDENCE
- ESCALATE / HUMAN REVIEW

The system must not equate a classifier score with certain cheating.

## Candidate baselines
- B0: keyword/rule-list moderation.
- B1: speech-only classifier.
- B2: speech + conversation history.
- B3: speech + board state.
- B4: speech + board state + speaker role + game phase + match contract + calibrated abstention.

## Candidate evaluation classes
- C0 normal conversation
- C1 competitive banter
- C2 abusive conduct
- C3 threat/severe harassment
- C4 self-description of own position
- C5 opponent-directed strategic suggestion
- C6 third-party move assistance
- C7 collusive communication
- C8 post-game analysis
- C9 uncertain / insufficient context

## Primary metrics
- macro F1 and per-class precision/recall;
- false-penalty rate (mandatory);
- missed severe-violation rate;
- appropriate abstention rate;
- incorrect abstention rate;
- policy-consistency across match contracts;
- ruling latency.

False-penalty rate is mandatory because an arbiter that catches violations while wrongly sanctioning legitimate speech is not acceptable.

## Match-contract model
The same speech or tool use may be allowed or prohibited depending on a predeclared contract, for example:
- strict competitive;
- social competitive;
- open assistance;
- training/analysis.

The research contribution is not that multiple modes exist, but whether explicit policy context measurably improves adjudication quality and reduces unsupported sanctions.

## Evidence discipline
Potential ruling chain:
1. OBSERVED — transcript/speaker/timestamp.
2. DERIVED — speech refers to a board square, piece, legal candidate move, or current game event.
3. POLICY MATCH — relevant match rule and applicability.
4. INFERRED — possible assistance/misconduct interpretation.
5. RULING — action, abstention, or escalation with confidence/evidence record.

## Privacy and governance
Voice may expose identity, accent, emotion, household speech, minors and other private information. Prefer ephemeral audio processing and retention of only policy-relevant evidence where technically and legally appropriate. Consent, retention, deletion, appeals and safeguarding must be specified before human deployment.

## Falsification conditions
H5 fails if:
1. contextual B4 does not materially outperform speech-only or simpler contextual baselines;
2. false penalties remain unacceptably high;
3. gains come mainly from obvious keywords rather than board/policy context;
4. performance collapses on ambiguous or paraphrased chess speech;
5. match-policy changes produce inconsistent rulings;
6. abstention does not improve safety of uncertain decisions;
7. the benchmark is constructed so narrowly that the result cannot support the claimed bounded use case.

## Novelty boundary
Targeted search did not identify a directly matching system or study whose central evaluation task is live chess-voice adjudication grounded jointly in board state, speaker role, game phase and explicit match contract with false-penalty and abstention metrics. This is not proof of uniqueness. The contribution should be framed as a bounded domain-specific design/evaluation study rather than invention of contextual moderation.

## Final Pass 003 decision
**CONDITIONAL GO TO FORMAL SPECIFICATION; PARKED FOR PORTFOLIO COMPARISON.**

A formal next pass, if authorized, should freeze the benchmark scenarios, policy contracts, annotation protocol, ambiguity rules, baselines, metrics, acceptable false-penalty thresholds, ASR error handling, human-review procedure, privacy/ethics controls and implementation limits before coding.
