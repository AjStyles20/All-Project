# P002 Research Pass 015 — Decision Matrix and Convergence

## Status
CONVERGENCE / CONDITIONAL GO. This is not implementation approval and not a final novelty claim.

## Purpose
Passes 001–014 progressively attacked broad P002 claims and expanded the search beyond AI tutoring into provenance, security, human–AI collaboration, social learning, software engineering, safety engineering, cryptography and virtual-world interaction. This pass stops feature expansion and classifies the remaining mechanisms using YES / PARTIAL / NO / UNKNOWN.

Definitions:
- YES: strong evidence that the broad mechanism already exists; do not claim it as P002 novelty.
- PARTIAL: important components/prior art exist, but the exact P002 intersection or enforcement/evaluation contract remains incompletely matched.
- NO: reviewed evidence currently gives a defensible basis that a directly comparable mechanism was not found. This is not proof of universal absence.
- UNKNOWN: evidence is insufficient; further targeted search required.

## Current evidence update
- IntelliCode (EACL 2026) already provides multi-agent tutoring, centralized/versioned learner state, mastery estimates, misconceptions, graduated hinting, curriculum selection, spaced repetition, engagement monitoring and auditable state updates. These are baseline/prior art, not P002 novelty.
- OpenMAIC already covers immersive multi-agent learning, generated courses, uploaded materials, durable sessions, skills, provider-neutral infrastructure, interactive content and substantial provenance/security-related engineering discovered in earlier passes.
- ASTRA provides trace-ready multi-agent tutoring/collaboration evaluation schemas and participation-balanced synthetic benchmarking; generic traceability is therefore not enough.
- A large field experiment on AI assistance and student agency found that learners could become reliant on AI and performance changed when support was removed. This supports withdrawal/independence testing as a real educational problem.
- OECD's 2025 education-AI report explicitly recommends exposing assistance level, periodic unscaffolded exit checks, fading and feeding independent checks into teacher dashboards. Therefore these individual mechanisms are not novel by themselves.
- A 2026 two-year Khanmigo trial across 18 middle schools found modest achievement effects and low substantive tutor engagement, with gains resembling ordinary Khan Academy practice without AI. This strengthens the requirement that P002 must demonstrate value beyond merely adding an AI tutor.

## Decision matrix

| Mechanism / claim | Status | Reason |
|---|---|---|
| AI tutor / teacher persona | YES | Mature and crowded. |
| Multi-agent AI classroom | YES | OpenMAIC, SimClass and other systems. |
| AI classmates / peers | YES | Existing social-learning and virtual-peer work. |
| Uploaded-material RAG tutoring | YES | Current systems already implement it. |
| Centralized/versioned learner model | YES | IntelliCode directly implements this. |
| Mastery/misconception tracking | YES | Long ITS history plus current LLM tutors. |
| Graduated hints / fading | YES | Established pedagogy and current systems/policy guidance. |
| Generic learner independence / AI withdrawal testing | YES | Existing empirical studies and current policy recommendations. |
| Generic provenance / trace logging | YES | Agent tracing, ASTRA, OpenMAIC and provenance research. |
| Generic claim→source ledger | YES | Current agent systems already do this. |
| Machine-checkable pedagogical constraints | YES | OpenMAIC skills/runtime constraints and adjacent systems. |
| Zero-trust identities / least privilege for agents | YES | Established security engineering. |
| Blockchain credentials / learning records | YES | Crowded educational blockchain/verifiable-credential prior art. |
| Personal learning environment/world | YES | Established PLE and AI-PLE research direction. |
| Community knowledge building | YES | Established knowledge-building/CSCL tradition. |
| Human–AI collaborative learning | YES | Active hybrid-intelligence literature. |
| Virtual educational campus/metaverse | YES | Existing virtual-world/metaverse education work. |
| Role-based human/AI collaboration | YES/PARTIAL | Role allocation exists; machine-enforced substitutable role contracts across private/hybrid/social modes need closer comparison. |
| Assistance provenance linked to later independent mastery | PARTIAL | Assistance logging, fading and withdrawal exist; a unified policy/event/evidence contract remains incompletely matched. |
| Learning near-miss as structured event affecting mastery/reverification | PARTIAL | Confidence/process assessment and misconception handling exist; exact operational combination needs more direct search. |
| Evidence-closed Knowledge Issue lifecycle | PARTIAL | Question tracking/mastery/reverification concepts exist separately; persistent issue closure requiring independent evidence remains a product/research candidate, not established novelty. |
| Policy-semantic virtual spaces | PARTIAL/UNKNOWN | Context-aware permissions and educational virtual spaces exist; whether location-as-policy bundle adds measurable value is unproven. |
| Cross-agent authority preservation across transformed claims | PARTIAL | Generic semantic provenance and inter-agent tracing exist; education-specific runtime authority invariants remain incompletely matched. |
| Active contradiction/dependency propagation into generated instructional artifacts | PARTIAL | Truth maintenance/data lineage exist; direct modern LLM-learning implementation remains incompletely matched. |
| Joined epistemic + pedagogical + outcome graph | PARTIAL | Each component has prior art; the integrated enforcement/evaluation graph is not yet established as novel. |
| Human↔AI occupant substitution under stable role contracts with pedagogical evaluation | PARTIAL/UNKNOWN | Hybrid role allocation exists; longitudinal/equivalent-role substitution and handoff evaluation remains undersearched. |

## What does NOT survive as novelty
P002 must not claim novelty because it has:
- multiple AI teachers/classmates;
- RAG;
- uploaded documents;
- speech;
- virtual rooms;
- gamification;
- learner models;
- hints;
- mastery tracking;
- provenance logs;
- blockchain;
- community features;
- AI/human collaboration;
- adaptive curricula;
- teacher dashboards.

These can still be valuable product features.

## Three contribution candidates selected for final attack

### Candidate A — Authority-Preserving Learning Dependency Graph
Research hypothesis:
A learning system can make source authority machine-enforceable across human and AI transformations, prevent repetition from laundering unsupported claims into trusted knowledge, and actively invalidate/flag downstream instructional artifacts when upstream evidence is contradicted, changed or superseded.

Minimum technical contribution if retained:
1. typed knowledge/evidence objects;
2. authority classes separate from confidence;
3. transformation lineage;
4. cross-agent/human reuse rules;
5. contradiction/supersession propagation;
6. downstream impact analysis;
7. behavioral enforcement, not decorative logging;
8. adversarial source-laundering tests.

Status: PARTIAL — strongest computer-science architecture candidate.

### Candidate B — Policy-Governed Assistance-to-Independence Contract
Research hypothesis:
A tutor should not infer mastery from assisted success. Every material intervention is authorized by explicit pedagogical policy, assistance intensity is recorded, suspicious/near-miss success can trigger re-verification, and mastery requires later independent evidence under reduced or removed assistance.

Important qualification:
Fading, unscaffolded checks and withdrawal evaluation are established. P002's possible contribution is therefore not those techniques individually. It would have to be the enforceable event/state contract joining policy authorization, assistance provenance, mastery claims, near-miss evidence and later independent verification.

Status: PARTIAL — strongest educational/evaluation candidate.

### Candidate C — Substitutable Human/AI Learning Role Contracts
Research hypothesis:
Learning roles are first-class policy objects rather than fixed AI personas. A role defines purpose, authority, capabilities, privacy access, tools, evidence obligations and handoff rules; either a human or AI may occupy the role where permitted. The system can transition from AJ's private AI-populated world to mixed human–AI groups without changing the underlying learning activity, and can evaluate when AI substitution helps or harms learning/social outcomes.

Status: PARTIAL/UNKNOWN — strongest product/social-systems candidate, but requires more direct hybrid-intelligence prior-art search.

## Relationship among A, B and C
These candidates are complementary but separable.

A governs what can be trusted.
B governs how much cognitive work the system is allowed to perform and what counts as learner mastery.
C governs who/what may perform a learning/social role.

Together they produce a concise control model:

WHO may act? -> Role Contract (C)
WHAT may be treated as knowledge? -> Authority/Dependency Graph (A)
HOW much may the system help, and DID the learner actually learn? -> Assistance-to-Independence Contract (B)

This is substantially stronger than defining P002 by its user interface.

## Product vision retained
The product may still be a Personal Learning World that can expand into a hybrid learning society:
- private world: AJ + AI occupants;
- hybrid world: AJ + invited humans + AI occupants/facilitators;
- social world: human communities with bounded AI roles.

The product can include classrooms, library, study hall, labs, project rooms, debates, messaging, community knowledge, speech and optional spatial UI. None of these is automatically a research contribution.

## Virtual-world decision
Do not make the spatial campus part of the research core yet.

Prototype later only if a cheap experiment can compare:
A. ordinary navigation/tabs;
B. semantic spatial rooms whose location changes policy, privacy, assistance and agent behavior.

Retain only if it improves measurable navigation comprehension, rule awareness, social presence, motivation or learning without disproportionate complexity/accessibility cost.

## Blockchain/cryptography decision
Blockchain remains REJECTED as a default core dependency.

Cryptographic primitives remain available where justified:
- content hashes for artifact identity/versioning;
- signatures for endorsements/assessment receipts;
- hash chains/Merkle structures for tamper evidence;
- verifiable credentials for portable achievements where needed.

Only reconsider a blockchain if a concrete multi-party trust model requires verification without a shared trusted authority and simpler signed/append-only mechanisms fail that requirement.

## Evaluation contract before implementation
Any later prototype must support falsification, not only demonstration.

Baseline 1: strong source-grounded single-agent tutor.
Baseline 2: equivalent tutor with ordinary logs but without Candidate A enforcement.
Baseline 3 where relevant: fixed AI-role multi-agent system without Candidate C substitution.

Candidate A tests:
- unsupported-claim laundering across agents;
- paraphrase/summarization lineage preservation;
- conflicting source propagation;
- superseded-source impact analysis;
- malicious uploaded-source contamination;
- false provenance-link injection.

Candidate B tests:
- assisted vs independent performance;
- retention after delay;
- transfer to new problems;
- false-mastery rate;
- near-miss detection precision/recall where ground truth can be established;
- assistance intensity and time-to-independent-success;
- accessibility exceptions and policy fairness.

Candidate C tests:
- human/AI handoff continuity;
- role-policy violations;
- learning outcome by occupant configuration;
- social presence and participation balance;
- inappropriate AI substitution;
- privacy/authority leakage during role changes;
- cost/latency versus benefit.

## Decision
P002 receives a CONDITIONAL GO FOR ONE FINAL RESEARCH GATE.

This does NOT authorize implementation.

The project is no longer searching broadly for features. The next pass must directly try to falsify Candidates A, B and C using the strongest adjacent prior art and, if needed, source/code inspection. After that:
- retain at most 2 research contributions;
- demote the rest to product features or future work;
- write a bounded novelty statement only for surviving intersections;
- produce the first architecture decision record;
- then decide GO/PARK/KILL for implementation.

## Current recommendation
Candidate A currently has the best fit for a defensible Computer Science contribution because it can be specified as data structures, invariants, propagation algorithms, trust boundaries and adversarial tests.

Candidate B has the clearest educational value but substantial component prior art; it is strongest as an integrated evaluation/control contract paired with A.

Candidate C best preserves the original 'my own world' vision and enables social expansion, but currently carries the highest novelty uncertainty. It may become a product differentiator rather than the thesis/research contribution.

## Next pass
Pass 016 — Final Falsification Gate:
1. Attack Candidate A against truth-maintenance, provenance, data-lineage, claim graphs, multi-agent trust and current educational provenance systems.
2. Attack Candidate B against mastery learning, scaffolding/fading, help-seeking models, process assessment, AI-assistance disclosure and withdrawal/transfer research.
3. Attack Candidate C against hybrid-intelligence role allocation, mixed human/AI teams, substitutable agents, collaborative-learning orchestration and handoff systems.
4. Produce SURVIVES / DEMOTE / KILL for each.
5. Select at most two contribution candidates.
6. No implementation until this gate is complete.