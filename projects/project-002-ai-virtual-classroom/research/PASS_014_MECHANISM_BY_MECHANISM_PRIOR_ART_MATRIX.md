# P002 Research Pass 014 — Mechanism-by-Mechanism Prior-Art Matrix

## Status
ADVERSARIAL REDUCTION / CONTRIBUTION SELECTION. No implementation approval. No final novelty claim.

## Purpose
Passes 010–013 deliberately expanded P002 beyond a conventional AI classroom, then began cutting weak differentiators. This pass attacks the surviving mechanisms against older AI/education concepts and current human–AI learning research. The objective is not to prove uniqueness from search failure, but to identify which mechanisms remain worth deeper empirical/implementation investigation.

## New prior-art pressure

### Truth-maintenance systems already entered adaptive e-learning
A 2021 adaptive e-learning system explicitly used a justification-based truth-maintenance system to adapt learning content/pathways to student profiles and results. Therefore P002 cannot claim that applying truth maintenance, justifications, or non-monotonic belief revision to education is new.

Implication: Knowledge Git / contradiction propagation must be narrower: source-version changes and claim contradictions should invalidate or flag dependent AI-generated instructional artifacts and cross-agent claims, with inspectable dependency paths. Whether that exact operational intersection exists remains UNKNOWN.

### Context-aware educational access control is old prior art
A 2013 ubiquitous-learning system used context-aware access control with ciphertext-policy attribute-based encryption; later adaptive context-aware access-control work also exists. Therefore changing permissions based on educational context/location is not itself novel.

Implication: a Library/Lab/Exam-Hall metaphor cannot claim novelty from context-dependent permissions. The virtual-space hypothesis survives only if spatial context integrates pedagogical policy, epistemic authority, assistance rules, privacy, and learner behavior in a way that measurably improves comprehension/use of those boundaries over conventional UI controls.

### Hybrid human–AI education is now a substantial field
A 2026 scoping review synthesizing 42 sources describes hybrid-intelligence education around human–AI collaboration, co-evolution, contextual adaptability, cognitive/metacognitive outcomes, educator agency, transparency, ethics and equity. A separate 2026 systematic review reports 62 empirical studies of human–AI collaboration/hybrid intelligence for learning and explicitly notes that unstructured interaction is not necessarily effective.

Implication: Human/AI substitutable roles are not novel merely because humans and agents can share a team. P002 must define machine-readable role contracts, authority/data/tool boundaries, handoff semantics, and an evaluation showing when role substitution improves or harms learning.

### Task-allocation frameworks already distinguish what humans should retain
The 2026 SCAN framework formalizes learner task allocation with GenAI into Substitute, Complement, Aid and Non-negotiable zones, motivated by ZPD, metacognition, cognitive offloading and lifelong learning.

Implication: P002 cannot claim invention of deciding what AI should or should not do for the learner. The stronger candidate is enforceable runtime assistance policy linked to actual learner attempts and later independent-performance evidence.

## Mechanism matrix

| Candidate | Prior art status | P002-specific surviving question | Current disposition |
|---|---|---|---|
| Epistemic Firewall | Generic provenance, source attribution, zero-trust and fact checking established | Can source authority be machine-enforced across transformed educational agent/human claims so repetition cannot launder authority? | STRONG / UNKNOWN |
| Pedagogical Decision Provenance | Explainable/adaptive tutoring, learner-state updates and auditability established | Can each runtime intervention be causally linked to learner evidence + explicit policy + allowed assistance + outcome? | STRONG / PARTIAL |
| Knowledge Git / Contradiction Propagation | Versioning, lineage, TMS and educational TMS established | Can source revisions/contradictions actively invalidate downstream AI lessons, questions, claims and community artifacts? | STRONG / UNKNOWN |
| Assistance Withdrawal / Independence | Scaffolding, fading, cognitive-offloading research and task-allocation frameworks established | Can the system enforce assistance policy and use delayed/no-AI evidence as a first-class mastery signal? | STRONG AS EVALUATION; WEAK AS STANDALONE NOVELTY |
| Human↔AI Role Substitution | Hybrid intelligence and AI teammate roles established | Can stable machine-readable role contracts permit safe human/AI substitution while preserving authority, privacy and pedagogy, and can the system learn when substitution is beneficial? | PARTIAL / UNKNOWN |
| Knowledge Issue Tracker | Questions, misconceptions, mastery learning, issue/workflow systems all established separately | Can a persistent knowledge issue require evidence of independent resolution, reopen after retention failure, and link misconception→assistance→verification history? | PRODUCT-STRONG / NOVELTY UNKNOWN |
| Learning Near-Miss Detector | Process assessment, confidence, misconceptions and knowledge tracing are established | Can suspicious success become an explicit event that blocks premature mastery and schedules re-verification? | PRODUCT/MEASUREMENT CANDIDATE; NOVELTY UNKNOWN |
| Policy-Semantic Virtual Spaces | Virtual learning worlds and context-aware access control established | Does spatial context measurably improve understanding/adherence to epistemic, privacy and assistance boundaries versus ordinary navigation? | PROBATION / LIKELY UX EXPERIMENT |
| Personal Learning Operating World | PLEs, ITSs, AI companions and virtual worlds established | Can it serve as coherent product shell for the stronger mechanisms while remaining valuable to one human? | PRODUCT VISION, NOT CORE NOVELTY |
| Blockchain | Education credentials/provenance and AI provenance crowded | Is there a genuine multi-party distrust problem unsolved more simply by signatures/Merkle/VCs? | OPTIONAL / CURRENTLY REJECT AS CORE |

## Important distinction: product innovation vs research contribution
P002 may be an original and useful product composition without every feature being academically novel. We must not confuse:
- product identity: the personal learning world / optional learning society;
- engineering contribution: reliable integration of provenance, policy, roles and learning state;
- research contribution: a falsifiable mechanism/evaluation whose effect can be compared against strong baselines.

## Provisional top three contribution candidates

### CANDIDATE A — Authority-Preserving Learning Graph
Combine the Epistemic Firewall with active dependency invalidation.

Core invariant:
> No AI-, learner-, or community-generated claim becomes authoritative merely through repetition, summarization, role status, popularity, or downstream reuse.

Required capabilities:
- typed source/claim authority;
- derivation parents across transformations;
- contradiction/supersession state;
- propagation to dependent lessons/questions/explanations/community artifacts;
- explicit uncertainty and unresolved conflict;
- provenance-aware agent boundaries.

Research test: inject unsupported claims, contradictory source updates and paraphrase chains into single- and multi-agent conditions; measure source laundering, unsupported propagation, stale-artifact detection, correction accuracy, latency and cost.

### CANDIDATE B — Policy-Governed Assistance with Independent Mastery
Combine pedagogical-decision provenance, assistance budgets/fading, near-miss detection and AI-withdrawal evaluation.

Core invariant:
> Assisted success must not automatically count as independent mastery.

Required capabilities:
- learner-first attempt capture;
- assistance ladder and policy rules;
- intervention reason trace;
- near-miss events;
- delayed/no-AI verification;
- reopening of apparently mastered concepts;
- accessibility exceptions that are explicit rather than punitive.

Research test: compare unrestricted tutor vs policy-governed tutor under equivalent model/content conditions; evaluate immediate assisted performance, delayed independent performance, transfer, verification behavior, time, frustration, cost and accessibility impact.

### CANDIDATE C — Role-Contract Hybrid Learning World
Separate social/pedagogical roles from their occupants.

Core invariant:
> Human and AI occupants inherit explicit role capabilities and epistemic limits; changing the occupant must not silently change authority or private-data access.

Required capabilities:
- machine-readable role contract;
- human/AI occupant identity;
- tool/data/privacy permissions;
- epistemic authority constraints;
- handoff state;
- collaboration objective;
- reason for AI insertion/removal.

Research test: compare solo+AI, human+AI, and human-human-AI compositions for learning, participation balance, AI reliance, social presence, error propagation, privacy exposure, latency and cost.

## Product-supporting mechanisms
The Knowledge Issue Tracker and Personal Learning Operating World should remain in the product concept even if they fail novelty tests. They provide continuity and make the system useful for a single human—the original product requirement.

Candidate Knowledge Issue lifecycle:
OPEN → WORKING → VERIFYING → RESOLVED → REOPENED.

Closure should require evidence stronger than 'AI supplied an explanation'; independent explanation/application or later verification can be required by policy.

## Virtual world decision gate
Do not build a pixel/3D campus merely for appearance.

Before substantial world implementation, prototype the same policy semantics in two interfaces:
A. conventional tabs/pages;
B. spatial rooms/locations.

Keep the spatial layer only if it materially improves navigation, rule comprehension, social presence, motivation, collaboration, or adherence to assistance/privacy/assessment boundaries enough to justify complexity and accessibility/performance costs.

## Blockchain/cryptography decision
Retain cryptographic primitives as normal engineering tools where justified: hashes, signatures, authenticated records, commitments, content fingerprints, optional verifiable credentials. Blockchain remains unselected. Introduce it only after a trust-model analysis demonstrates independent parties who cannot reasonably trust a shared authority and where a simpler signed append-only system is insufficient.

## Current P002 disposition
MORE RESEARCH — CONDITIONAL GO CANDIDATE.

The project should no longer search for one magical feature nobody has ever imagined. The stronger strategy is to select a small number of mechanisms with documented unresolved problems, implement them rigorously, and evaluate them against credible baselines.

The current best package is:
1. Authority-Preserving Learning Graph;
2. Policy-Governed Assistance + Independent Mastery;
3. Role-Contract Hybrid Learning World.

This package is not yet a novelty claim.

## Pass 015
Construct a decisive YES/PARTIAL/NO/UNKNOWN evidence matrix against named systems and research families. Specifically compare OpenMAIC, SimClass, IntelliCode, OATutor, Khanmigo, learner-state-aware RAG tutors, educational provenance specifications, hybrid-intelligence systems, educational TMS, and relevant knowledge-tracing/process-assessment work against Candidates A–C.

Then make a bounded recommendation:
- GO with 1–3 contribution candidates;
- PARK/reframe P002;
- or MORE RESEARCH only where a concrete unresolved evidence gap remains.
