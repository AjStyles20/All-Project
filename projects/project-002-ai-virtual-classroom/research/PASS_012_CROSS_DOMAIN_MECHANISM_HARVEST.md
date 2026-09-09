# P002 Research Pass 012 — Cross-Domain Mechanism Harvest

## Status
INNOVATION SEARCH / CROSS-DOMAIN TRANSFER / PRIOR-ART AWARE. No implementation approval and no final novelty claim.

## Purpose
P002 began as a private personal learning world for one human learner. Later research expanded it toward optional real classmates, communities and a virtual learning society. This pass deliberately leaves the AI-education feature bubble and asks what mechanisms from older education, apprenticeship, libraries, science, healthcare, multiplayer games, open-source software, social networks, governance, cybersecurity, distributed systems and cryptography could solve real learning/social/trust problems.

A borrowed mechanism is not novel merely because it is transplanted into education. Each remains a hypothesis until direct prior-art, feasibility, safety and evaluation tests are complete.

## External evidence sampled in this pass
1. Communities of practice in healthcare show that communities can support knowledge sharing and applied learning, but they do not become self-sustaining automatically; shared purpose, regular interaction, time and institutional support matter.
2. A healthcare Learning Exchange demonstrated the idea of a community knowledge commons for distributed learning networks.
3. Peer learning in health professions emphasizes reciprocal explanation, feedback, critical thinking and professional identity formation.
4. Multiplayer/virtual-world research has long linked learning to participation in communities of practice; virtual worlds can teach management of social and material resources, not merely subject facts.
5. 2026 socio-educational metaverse research reports that generative AI avatars can increase perceived agency/social realism but introduce unpredictability, trust and expectation-alignment problems.
6. 2026 work already proposes AI-powered metaverse learning and AI-integrated social learning, so 'AI + virtual world + social learning' is not a novelty claim.
7. Earlier MetaEdu prior art already combined AI, blockchain/Web3 and social metaverse learning. Therefore adding blockchain to a virtual classroom is explicitly rejected as standalone novelty.

## Mechanism harvest

### M01 — Apprenticeship: legitimate progression from observation to independent practice
Translate apprenticeship into a progression contract:
Observe -> Explain -> Perform with guidance -> Perform with limited hints -> Perform independently -> Teach another.

P002 implication: mastery is not inferred only from quiz accuracy. The learner should demonstrate increasing independence and eventually explanation/teaching ability.

Connection to existing P002 research: strengthens Assistance Budget + AI-Withdrawal Evaluation.

Novelty state: NOT NOVEL as pedagogy; potentially valuable as a system-wide progression contract.

### M02 — Old classroom: recitation, oral defense and teach-back
Older educational practice often required learners to recite, explain or defend understanding orally. Modern implementation can avoid rote memorization by requiring evidence-backed explanation, counterexample handling and teach-back.

P002 implication: an AI teacher/classmate can ask the learner to defend a claim, explain it differently, identify assumptions or teach a simulated novice.

Research hypothesis: 'ability to teach/explain after assistance withdrawal' may be a stronger independence signal than assisted quiz performance alone.

### M03 — Library: quiet knowledge infrastructure, not just chat
A library is valuable partly because it organizes trusted artifacts and preserves context over time.

P002 implication: the Library zone becomes the canonical evidence space: source versions, annotations, provenance, reading history, disagreements, superseded materials and community annotations. AI conversation cannot silently rewrite library authority.

Connection: Knowledge Git + Epistemic Trust Layer.

### M04 — Scientific community: claims earn trust through evidence, criticism and revision
Science separates a claim from the person making it and permits revision when evidence changes.

P002 implication: community explanations have lifecycle states such as Draft -> Evidence Attached -> Challenged -> Supported -> Teacher Endorsed -> Superseded. Disagreement is represented rather than erased.

Connection: Community Knowledge Forge + Contradiction Propagation Monitor.

### M05 — Healthcare: escalation and scope-of-practice
Clinical teams use role boundaries and escalation because not every participant is authorized to make every decision.

P002 implication: AI roles receive educational scopes. A peer agent may brainstorm but cannot alter canonical course truth; an assessment agent cannot rewrite source materials; high-stakes or ambiguous cases can escalate to a teacher/human authority.

Connection: Zero-Trust Educational Agent Fabric + Teacher-Governed Agent Constitution.

Novelty state: NOT NOVEL as governance/security; strong architecture candidate.

### M06 — Healthcare learning systems: community knowledge commons
Learning health systems use communities to share explicit and tacit knowledge and adapt evidence to practice.

P002 implication: distinguish formal source knowledge from lived/student explanations, examples, misconceptions and strategies. Tacit/community knowledge is useful but never silently promoted to canonical authority.

Potential differentiator: an explicit bridge between canonical knowledge, community knowledge and personal knowledge while preserving authority boundaries.

### M07 — Open-source software: contribution, review, versioning and blame/history
Open-source communities do not merely share files; they expose proposals, review, revisions, authorship and history.

P002 implication: shared notes/explanations/questions can have proposal/review/merge workflows. 'Knowledge blame' should not shame people; it means trace which source/change introduced an assertion and which artifacts depend on it.

Connection: Knowledge Git for community knowledge.

### M08 — Issue trackers: unresolved confusion as a first-class object
In software projects, unresolved problems are not buried in chat; they become trackable issues.

P002 implication: a learner can turn confusion into a Knowledge Issue: question, current understanding, attempted sources, competing explanations, status, helpers, resolution evidence. AI or humans can work the issue, and resolution becomes reusable learning knowledge.

Candidate novelty state: UNKNOWN. Needs direct search for education systems treating confusion/misconceptions as collaborative issue objects.

### M09 — Multiplayer games: roles, quests and interdependence
Good cooperative games give participants different capabilities and create goals that require coordination.

P002 implication: group learning missions should not be five people independently answering the same quiz. Roles could include Investigator, Explainer, Skeptic, Evidence Checker, Builder and Reviewer. Roles may be occupied by humans or AI.

Connection: Human/AI Role Substitution Matrix.

Risk: forced gamification, status competition and superficial points.

### M10 — Multiplayer worlds: meaningful places are permission/state machines
A virtual place can represent a rule context rather than decorative scenery.

P002 zones:
- Library: evidence-first; canonical-source operations.
- Classroom: guided instruction.
- Study Hall: assistance budget/fading.
- Common Room: social conversation with lower epistemic authority.
- Debate Hall: controlled disagreement and evidence challenge.
- Project Room: shared artifacts, review and contribution history.
- Lab: simulations/code/experiments.
- Exam Hall: restricted tools and independent assessment.
- Tutor Office: private learner-state-aware intervention.

Hypothesis: spatial metaphor can make policy boundaries understandable to users. This must be tested against a conventional navigation UI; visual world complexity must earn its cost.

### M11 — Social networks: connection without engagement-maximization
Borrow discovery, profiles, communities and messaging but reject optimization for endless scrolling, outrage or raw popularity.

P002 implication: recommendation objective can optimize for complementary expertise, unresolved learning needs, diversity of explanations, successful peer teaching and learner-controlled interests.

Candidate metric: Learning Utility rather than Engagement Time.

### M12 — Markets/reputation: local contribution credibility, not global human scores
A global student reputation score risks bias, popularity effects and social-credit dynamics.

P002 implication: attach evidence and review state to contributions. If reputation is used, keep it contextual and revocable: 'reliably explains Python recursion with supported examples' rather than 'AJ = 842 trust points'.

### M13 — Democratic governance: communities need rules and appeal
If real humans join, moderation and authority become governance problems.

P002 implication: explicit community constitution, moderation rules, role permissions, appeal paths, transparent policy changes and human override. AI moderation decisions should be reviewable rather than sovereign.

Novelty state: NOT NOVEL as governance; important safety requirement.

### M14 — Distributed systems: eventual consistency and conflict are normal
Different agents/users/devices can hold temporarily different states.

P002 implication: knowledge synchronization must distinguish stale, conflicting and authoritative versions. Offline edits or AI-generated artifacts cannot silently overwrite newer canonical truth.

Connection: low-resource/offline trustworthy degradation + Knowledge Git.

### M15 — Event sourcing: reconstruct why the world reached its current state
Instead of storing only current mastery or current note text, record important state transitions.

P002 implication: reconstruct learner-state changes, source updates, policy decisions, assistance escalation and community artifact revisions without storing unnecessary private chain-of-thought.

Important privacy rule: audit observable decisions/events, not hidden model reasoning.

### M16 — Cryptography: commitments, signatures and content identity
Useful primitives without requiring blockchain:
- content hashes for exact artifact versions;
- digital signatures for endorsements/issuance;
- Merkle roots for compact integrity proofs;
- verifiable credentials for portable achievements;
- selective disclosure where appropriate.

P002 implication: cryptography is infrastructure for integrity and verification, not a marketing feature.

### M17 — Blockchain: only for a demonstrated multi-party trust problem
Prior art already includes AI + blockchain + metaverse/social education. Therefore blockchain is rejected as a novelty shortcut.

Possible future use: multiple independent institutions issue/verify credentials or integrity anchors without trusting one database administrator. Raw student conversations, personal learner state and sensitive educational records should not be placed on a public immutable chain.

### M18 — Personal knowledge management: the world should remember learning, not merely chats
For the original one-user world, long-term value comes from continuity: concepts learned, misconceptions, unresolved questions, source history, projects, goals and evidence of independent mastery.

P002 implication: Personal Knowledge Map connects topics, artifacts, attempts and goals. Memory must distinguish learner-provided facts, inferred learner state and authoritative knowledge.

### M19 — Mentorship: one person can have multiple advisory relationships
A real learner may seek different people for conceptual explanation, challenge, encouragement, career context or technical review.

P002 implication: AI roles should have bounded purposes rather than merely different personalities. Role selection should be task-driven, and the system should prefer one capable agent when multiple roles add no value.

### M20 — Society: serendipitous learning without surveillance
Real campuses create accidental encounters and exposure to adjacent interests.

P002 implication: optional Discovery Square / noticeboard can surface clubs, questions, projects or public learning artifacts based on explicit interests and learning goals, while avoiding invasive behavioral profiling.

### M21 — Research laboratory: hypothesis -> experiment -> evidence -> revision
For STEM/programming topics, learning should produce artifacts and observations, not only dialogue.

P002 implication: Lab missions require prediction before execution, experiment/simulation, observation, explanation and revision. AI can help design experiments but cannot retroactively rewrite the learner's initial prediction.

This creates valuable provenance for learning process without exposing private chain-of-thought.

### M22 — Safety engineering: near-miss learning
Safety-critical industries learn from near misses, not only failures.

P002 implication: record educational near misses such as correct answer with faulty reasoning, unsupported confidence, lucky guesses or source misuse. These can trigger targeted follow-up even when the score is technically correct.

Candidate novelty state: UNKNOWN/PARTIAL in educational AI; deserves targeted search.

## New combined concepts worth attacking

### C1 — Personal Learning Operating World
A persistent private world in which one learner can move among evidence, instruction, practice, debate, projects and assessment while AI roles obey zone-specific authority and pedagogical rules. Real humans are optional extensions, not prerequisites.

### C2 — Human/AI Substitutable Learning Guilds
A learning group defines functional roles rather than fixed 'AI classmates'. Humans or AI can occupy roles depending on availability, but role permissions and epistemic authority remain stable. Research must compare all-AI-support, mixed human/AI and human-heavy configurations.

### C3 — Knowledge Issue Tracker
Confusions, misconceptions and disputed claims become collaborative trackable objects with evidence, attempted resolutions and closure criteria.

### C4 — Evidence-Governed Community Knowledge Forge
Community-created explanations can be proposed, reviewed, challenged, versioned and promoted without confusing popularity with truth.

### C5 — Cognitive Independence Contract
Across the entire world, assistance must eventually produce opportunities for unassisted demonstration. The system measures not just task completion but transfer, teach-back, delayed retention and assistance dependence.

### C6 — Learning Near-Miss Detector
The system distinguishes correct outcome from trustworthy understanding by detecting lucky guesses, unsupported claims, contradictory explanations or excessive assistance and scheduling verification tasks.

### C7 — Policy-Semantic Virtual Campus
Virtual locations are understandable policy contexts. Moving into Exam Hall, Debate Hall or Library changes permissions, assistance and evidence rules. The research question is whether this spatial policy metaphor improves comprehension, engagement and policy compliance enough to justify the added UI complexity.

## Important negative findings / constraints
- AI-powered educational metaverses already exist in the literature.
- AI avatars in socio-educational virtual environments already exist.
- AI + blockchain + social metaverse education has prior art.
- Communities of practice and knowledge commons are established.
- Peer tutoring, cooperative roles, gamification, provenance, versioning, signatures and verifiable credentials are established concepts.

Therefore P002 cannot claim novelty from any ingredient above in isolation.

## Emerging architecture principle
P002 should be designed as a world of **bounded contexts** rather than a collection of screens. Each context defines:
1. who/what may participate;
2. what information has authority;
3. what tools/assistance are allowed;
4. what events are recorded;
5. what privacy boundary applies;
6. how success is evaluated;
7. how the learner exits toward greater independence.

This may connect the social-world concept to the earlier security/provenance/pedagogy research in a coherent way.

## Updated innovation candidates for Pass 013 attack
Highest priority:
1. Knowledge Issue Tracker for misconceptions/confusions.
2. Learning Near-Miss Detector.
3. Human/AI Substitutable Learning Guilds.
4. Policy-Semantic Virtual Campus.
5. Evidence-Governed Community Knowledge Forge.
6. Personal Learning Operating World as a coherent single-user-first architecture.

Retained from earlier passes:
7. Cross-Agent Epistemic Firewall.
8. Pedagogical Decision Provenance.
9. Contradiction Propagation / Knowledge Git.
10. Assistance Budget + independent competence.

## Decision
MORE RESEARCH. CONDITIONAL GO CANDIDATE.

The project has expanded conceptually, but implementation remains blocked until the strongest new candidates are attacked with direct prior-art search. The goal is not maximum feature count. A smaller coherent system with one or two defensible contributions is preferable to an unbuildable metaverse containing every idea.

## Next pass
Pass 013 should adversarially test the six new high-priority concepts. Search education, ITS, CSCL, learning analytics, knowledge management, issue tracking, misconception diagnosis, formative assessment, near-miss/error analysis, mixed human-AI teams, spatial computing/HCI and policy-aware interfaces. Explicitly distinguish 'not found' from 'does not exist'. Then decide which concepts become core, supporting, parked or rejected.