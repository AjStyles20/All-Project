# P002 Research Pass 011 — Personal Learning World and Social-System Reframe

## Status
CONCEPT REFRAME / SOCIAL-LEARNING PRIOR-ART ATTACK. No implementation approval and no final novelty claim.

## Trigger
AJ clarified an important origin condition: the concept was initially intended primarily for one learner — effectively a private learning world — rather than first as an institutional multi-user virtual classroom. This materially changes the design question.

The system should not assume that real classmates, a school deployment, or a large user population are prerequisites. It should investigate a spectrum from a private persistent learning world populated by AI roles, through optional real-human peer connection, to a broader learning society/campus.

## Evidence found in this pass
1. Current research already goes beyond one-to-one tutoring. A 2026 controlled study titled *Beyond the AI Tutor: Social Learning With LLM Agents* compares tutor and LLM-peer configurations; in its convergent problem-solving experiment (N=315), the tutor+peer condition achieved the highest unassisted test accuracy. This is direct prior art against claiming that adding AI classmates to a solo learner is itself novel.
2. A CHI 2026 study of the AI virtual peer “Saya” used a synthetic student in real elementary classrooms and reported increased student speaking time. The system included teacher-controlled speech acts such as probe, summarize and intentionally incorrect answer. Synthetic peers are therefore established design territory.
3. AgentSchool (2026) models cognitively growable student agents, adaptive teacher agents, formal/informal learning settings and social phenomena including clique formation and opinion-leader emergence. A simulated educational society is therefore a serious novelty threat.
4. A 2026 systematic review synthesized 46 empirical studies of AI agents in computer-supported collaborative learning. Social facilitation, cognitive scaffolding and instructional orchestration are established research categories.
5. Research on synthetic relationships with social pedagogical agents reports social presence, affective support, trust and rapport, but notes that much evidence is short-duration and tells us less about whether synthetic relationships remain useful and healthy over weeks in real settings.
6. Current work on socially embedded virtual learning simulations shows that social embedding is itself an experimental design variable, not merely a visual feature.
7. AI-powered metaverse/lifelong-learning concepts already exist. Therefore a virtual campus/metaverse appearance is not a novelty claim.

## Core reframe: three operating modes, one architecture
P002 should be investigated as a **Personal Learning World with optional social expansion**, not as a mandatory multi-user classroom.

### Mode A — Private World
One human learner. The world may contain AI teacher, tutor, classmates/peers, mentor, debate opponent, librarian/researcher, project teammate, examiner and facilitator roles. The learner can study alone while still receiving structured social/collaborative experiences.

This preserves AJ's original motivation and creates a meaningful use case for learners who are isolated, studying asynchronously, lack available peers, or simply want a private rehearsal/study environment.

### Mode B — Hybrid World
One learner plus selected real peers, with AI filling missing roles. Examples:
- two humans + AI facilitator;
- one human + AI study group;
- human group + AI evidence checker;
- human peer tutoring + AI observer/scaffolder;
- real friend joins a project room while AI handles source verification.

### Mode C — Learning Society / Campus
Multiple humans and AI roles coexist in persistent rooms/communities. This introduces messaging, groups, study matching, clubs, collaborative artifacts, governance, moderation, reputation, contribution attribution and potentially verifiable records.

Mode C must not be required for the private-world product to function.

## Virtual world as an interaction model, not decoration
Candidate spaces should alter permissions, pedagogy and assistance policy rather than merely change backgrounds:
- Library: source retrieval, evidence inspection, research.
- Classroom: structured lessons and discussion.
- Study Hall: focused practice and assistance budgeting.
- Common Room: informal social/peer interaction.
- Debate Hall: evidence-bounded disagreement and argumentation.
- Project Room: collaborative artifacts, attribution and peer review.
- Tutor Office: intensive one-to-one assistance.
- Lab: coding/simulation/experimentation.
- Exam Hall: controlled assistance or no-AI evaluation.
- Clubs/communities: interest-driven learning and optional human networking.

A lightweight 2D/2.5D browser representation is sufficient to test the interaction model; VR is not assumed.

## New candidate innovation portfolio

### S01 — Synthetic Social Learning World
A solo learner can summon an AI study group with deliberately differentiated epistemic and pedagogical roles. Novelty threat is HIGH: LLM peers, virtual students and multi-agent classrooms already exist. The surviving question is whether a persistent private world can deliver useful social-learning mechanisms without pretending synthetic relationships are equivalent to human friendship.

### S02 — Human/AI Role Substitution Matrix
The same activity can operate with different mixtures of humans and AI. If a real peer is unavailable, an AI can temporarily occupy a role; when a human joins, the AI can step back into facilitator/evidence-checker mode. This could make the architecture robust to group size from one human upward.

Research question: can social-learning activity structures remain pedagogically coherent as human/AI composition changes?

### S03 — Complementary Peer Matchmaking
For real users, match peers by complementary competencies, goals, availability, preferred study style and safety constraints rather than popularity. Example: learner A can teach Python while learner B can teach calculus. AI can scaffold the reciprocal tutoring session.

Novelty state: UNKNOWN/PARTIAL; peer recommendation/matching is established generally and requires direct educational prior-art attack.

### S04 — Contribution-Centric Epistemic Reputation
Avoid a permanent global “student score.” Attach trust/evidence state primarily to contributions: supported sources, peer challenges, teacher endorsement, unresolved contradiction, revalidation date and provenance. Reputation should not become a social-credit mechanism.

Novelty state: UNKNOWN. Must compare with Stack Overflow/Wikipedia/open-science reputation and educational peer-assessment systems.

### S05 — Community Knowledge Forge
Humans and agents can propose explanations, examples and corrections, but community content moves through evidence attachment, contradiction detection, review and promotion before becoming trusted course knowledge. This joins social collaboration to the Epistemic Trust Layer.

Novelty state: UNKNOWN/PARTIAL. Wiki/community knowledge systems are mature; AI-mediated authority promotion and dependency invalidation need attack.

### S06 — Social-Epistemic Firewall
Informal chat is allowed to be informal. However, statements from common rooms, AI classmates or users do not silently become authoritative instructional content. Promotion from conversation to trusted knowledge requires provenance/evidence and policy.

This extends I02 from agent-to-agent trust to human+AI social knowledge flows.

### S07 — Deliberate Productive Disagreement
A debate opponent or AI peer may intentionally disagree, make a plausible error or defend an alternate interpretation for learning purposes. The system must mark the epistemic role of such statements so staged disagreement cannot poison canonical knowledge.

Novelty threat: Saya already includes an “incorrect answer” speech act; broad pedagogical disagreement is not novel. The potential contribution is integration with authority/provenance enforcement and subsequent learner verification.

### S08 — Social Presence Without Deception
AI peers can have persistent identities/personas and relational continuity, but the UI/policy should not misrepresent them as humans. The system should investigate healthy boundaries, user control, memory visibility/deletion and whether long-term synthetic social presence helps or harms learning.

This is especially important if the product begins as “my own world.”

### S09 — Knowledge Git for a Community
Course/source changes trigger impact analysis across AI lessons, community notes, shared explanations, quizzes, discussions and project artifacts. A contribution can be current, stale, disputed or superseded.

This joins I11/I12 with social collaboration.

### S10 — Learning Network That Optimizes for Learning, Not Engagement
If a social feed/discovery layer exists, ranking should prioritize relevance, evidence quality, learning goals, diversity of useful perspectives and learner wellbeing rather than raw watch time, likes or addictive engagement.

Novelty state: conceptual hypothesis. Requires recommender-system and digital-wellbeing prior-art review.

## Cryptography/blockchain position after social reframe
The social/campus mode creates stronger legitimate trust problems than the private mode: multiple users can author artifacts, assess work, endorse knowledge and issue records. Useful primitives may include:
- content hashes for artifact/version identity;
- digital signatures for teacher/institution endorsement;
- Merkle structures for efficient tamper evidence;
- verifiable credentials for portable achievements;
- selective disclosure for privacy;
- cryptographic commitments for assessment receipts.

Blockchain remains conditional. It becomes reasonable only if independent parties need shared verification without trusting one platform operator. A private single-user world has almost no justification for blockchain.

## Cross-domain innovation map for Pass 012+
Research should deliberately inspect mechanisms from:
- old-school classroom practice: study circles, peer teaching, oral defense, apprenticeship, clubs, debating societies, office hours;
- libraries: curation, provenance, cataloguing, reference service;
- scientific communities: citation, peer review, replication, correction/retraction;
- open-source software: version control, pull requests, issue discussion, contribution attribution, maintainership;
- multiplayer games: party formation, quests, role complementarity, persistent spaces, cooperative progression;
- social networks: discovery and communities, while explicitly rejecting engagement-maximization defaults;
- healthcare teams: escalation, handoff, audit trails, multidisciplinary roles;
- cybersecurity: identity, authorization, zero trust, abuse containment;
- distributed systems/cryptography: signatures, commitments, append-only records, consensus only when justified;
- governance: moderation, appeal, community rules, delegated authority;
- psychology/sociology: belonging, peer effects, social presence, dependency, group dynamics, parasocial/synthetic relationships;
- accessibility: equivalent non-voice/non-avatar participation and low-bandwidth modes.

## Revised architectural hypothesis — research only
P002 becomes a **Trustworthy Personal Learning World and Optional Learning Society** with:
1. World/Experience Plane — persistent spaces and activities.
2. Human Social Plane — optional peers, groups, messaging, matching and collaboration.
3. Agent Social Plane — teacher/tutor/peer/facilitator/examiner/research roles.
4. Knowledge Plane — authoritative materials and community artifacts.
5. Epistemic Plane — evidence, authority, transformations, disputes, provenance and stale-state propagation.
6. Pedagogical Plane — learner state, policies, assistance control and decision provenance.
7. Security/Governance Plane — identities, permissions, moderation, privacy and human override.
8. Evaluation Plane — learning, independent competence, social-learning value, trust calibration, cost/latency and harms.
9. Optional Verification Plane — signatures/Merkle/verifiable credentials; blockchain only under a demonstrated decentralized trust model.

## Critical research questions
1. For one human learner, do synthetic classmates add measurable learning value over a strong tutor, or only atmosphere/social presence?
2. Does a persistent private learning world improve adherence, motivation or retention without creating unhealthy dependency?
3. Can the same pedagogical activity degrade gracefully from human group -> hybrid group -> solo+AI group?
4. Can informal social knowledge remain useful without contaminating trusted instructional knowledge?
5. Can AI peers challenge and make pedagogical errors without confusing source authority?
6. Does real-peer matchmaking produce reciprocal learning rather than popularity/status dynamics?
7. Can a virtual-world interaction model justify its UI complexity compared with conventional pages/chat?
8. Which social functions should never be delegated to AI?

## Decision impact
P002 remains **MORE RESEARCH — CONDITIONAL GO CANDIDATE**.

This reframe does not weaken the earlier trust/provenance work; it gives it a broader reason to exist. In a private world, it governs interactions among AI roles. In a hybrid/social world, it also governs how human conversation and community artifacts can influence trusted knowledge.

The original single-user motivation must remain a first-class product requirement. Do not let later institutional/social expansion erase it.

## Next pass
Pass 012 should be a cross-domain mechanism harvest and adversarial prior-art matrix focused on the private-world/social-world distinction. It should specifically attack S02, S04, S05, S06, S08, S09 and S10, and test whether the personal-world concept can remain valuable even if no other human ever joins.