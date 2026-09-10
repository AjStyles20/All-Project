# P010 — Intelligent Online Chess Platform
## Pass 001 — Lineage, Coaching, Fair Play, and Initial Hypotheses

Date: 2026-09-10
Canonical ID: P010
Previous ID: P005
Decision: MORE RESEARCH / EVIDENCE BUILD

## 1. Original concept boundary
An online chess platform combining play, communication, intelligent assistance, coaching, and analysis. The platform must separate fair-play competitive modes from assistance-permitted learning modes.

## 2. Immediate novelty collisions
The following are established and cannot be novelty claims:
- online chess play, matchmaking, ratings, tournaments, messaging, studies and analysis boards;
- Stockfish/engine analysis;
- post-game move classification and best-move display;
- AI or virtual-coach explanations;
- retrying mistakes, hints, tactical/puzzle training;
- adaptive explanations by player level;
- real-time coaching against a computer opponent;
- explainable chess-engine output;
- ordinary anti-cheat / engine-use prohibition in competitive play.

Commercial collision is strong. Chess.com provides post-game Game Review with coach explanations, key-move retry, hints and best-move lines, and in 2026 offers Play Coach, which gives move-by-move guidance against a virtual coach. Lichess provides Stockfish analysis, studies, interactive lessons, puzzles, opening tools and player insights. DecodeChess explains engine recommendations, threats, plans, concepts and piece functionality, and offers instructional analysis while playing against a computer.

## 3. Academic lineage
Chess tutoring predates modern LLMs. ICONCHESS (1996) and subsequent knowledge-based chess tutors explored high-level strategic advice rather than merely engine search. Work on chess learning has shown that self-explanation and prediction can improve principled understanding among novices. Explainable-AI and intelligent-tutoring research more broadly has studied personalized hints, explanations, learner modelling, adaptive feedback and the 'assistance dilemma'—when and how to help without undermining learning.

A particularly important 2025/2026 field experiment used a custom AI-assisted chess platform with more than 200 chess-club students. Students with unrestricted self-requested AI help learned substantially less than those receiving system-regulated assistance at selected moments. The authors attribute much of the gap to reduced productive struggle and increased reliance on AI. This directly threatens any novelty claim around 'adaptive AI chess coaching' but creates a sharper research problem around intervention policy.

## 4. Fair-play boundary
Competitive online chess generally forbids outside assistance during live play. Chess.com's 2026 Fair Play Policy explicitly prohibits engines, bots, plugins, browser extensions, other people, and automated analysis during ongoing games. Therefore any system that mixes ranked human-vs-human play with live engine/AI guidance must enforce hard mode boundaries.

Required modes should be conceptually separate:
- FAIR PLAY / COMPETITIVE: no engine hints, no AI move advice, no hidden analysis.
- ASSISTANCE-PERMITTED / TRAINING: coaching may be enabled and clearly labeled.
- POST-GAME REVIEW: full engine/XAI analysis allowed after the game ends.

Mode separation is a safety/integrity requirement, not a novelty claim.

## 5. Provisional hypothesis candidates

### H1 — Assistance-Gating for Productive Struggle
A tutoring policy that withholds direct chess assistance while the learner is still productively engaged, but intervenes when evidence suggests unproductive struggle, may improve learning outcomes relative to always-available hints or fixed-timing hints.
Status: SURVIVES PROVISIONALLY, but heavily threatened by general ITS literature and a 2025/2026 chess-specific field experiment.

### H2 — Hint-Ladder Policy Instead of Best-Move Revelation
Use progressively stronger interventions (metacognitive prompt -> strategic concept -> tactical cue -> candidate-move region -> concrete line) rather than immediately revealing the engine-best move. Evaluate learning, dependence, hint consumption and post-assistance transfer.
Status: SURVIVES AS A MECHANISM; hierarchical/scaffolded hints are established in ITS, so novelty must come from a bounded chess-specific evaluation rather than the existence of hint levels.

### H3 — Learner-Weakness-Aware Intervention
Maintain a lightweight learner model over recurring weaknesses (e.g., hanging pieces, missed forcing moves, king safety, tactical motifs, endgame technique) and use it to choose whether/what assistance to provide.
Status: THREATENED. Learner modelling and personalized feedback are mature. Needs direct chess-specific collision search.

### H4 — Fair-Play-Aware Assistance Architecture
Architecturally guarantee that pedagogical assistance is available only in clearly assistance-permitted contexts and cannot leak into competitive games.
Status: IMPORTANT ENGINEERING/INTEGRITY FEATURE, not yet a defensible research contribution.

## 6. Strongest current direction
The most promising research question is not 'Can AI teach chess?' but:

**Can a bounded intervention policy that regulates when and how much engine-grounded help is shown preserve productive struggle and improve post-assistance chess performance relative to self-requested or always-available assistance?**

Possible comparison:
- B0: no assistance during training;
- B1: self-requested full hint/best move;
- B2: fixed-timing assistance;
- B3: adaptive assistance trigger with full hint;
- B4: adaptive assistance trigger + progressive hint ladder.

Potential outcomes:
- independent post-test move quality;
- tactical/theme transfer to unseen positions;
- time-to-solution;
- hint requests and hint depth consumed;
- dependence/overreliance indicators;
- self-explanation quality;
- retention after delay if feasible.

## 7. Threats to novelty
- 'when to help' is the established assistance dilemma in ITS;
- adaptive hint timing is established;
- personalized feedback is established;
- chess-specific regulated-vs-self-regulated AI assistance has now been studied directly;
- progressive hints and self-explanation are established pedagogical mechanisms.

Therefore P010 cannot claim algorithmic novelty merely by combining Stockfish with an LLM coach. Pass 002 must directly attack whether a chess-specific progressive intervention policy, with post-assistance independence as the primary outcome, remains sufficiently differentiated for a bounded FYP contribution.

## 8. Feasibility
High on ordinary hardware. Core stack can be Python + python-chess + Stockfish + Flask/FastAPI/Streamlit/web frontend + SQLite/PostgreSQL. LLM use can be optional/API-based and grounded in engine output. No GPU is required.

## 9. Pass 001 decision
MORE RESEARCH.

Generic intelligent online chess-platform novelty is rejected. AI coach, engine explanations, adaptive level wording, post-game analysis, retries, hints and real-time coaching against a computer are occupied. The only research-worthy path is a tightly evaluated pedagogical intervention policy focused on productive struggle and independent learning, with strict fair-play separation.

Next: Pass 002 — direct prior-art attack on chess assistance timing, progressive hint ladders, learner modelling, productive struggle, overreliance and post-assistance transfer.