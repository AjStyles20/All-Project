# P002 Research Pass 010 — Innovation Search and Cross-Domain Synthesis

## Status
INNOVATION SEARCH / ADVERSARIAL PRIOR-ART TEST. No implementation approval and no final novelty claim.

## Purpose
Earlier passes deliberately attacked broad novelty claims around AI tutors, multi-agent classrooms, RAG, pedagogical agents, provenance, learner state, auditability, and blockchain. This pass switches from only eliminating claims to deliberately generating useful system-level differentiators by combining unresolved educational problems with mechanisms from provenance systems, zero-trust security, event sourcing, cryptographic verification, and learner-agency research.

The rule remains: a combination is not novel merely because its ingredients come from different fields. Every candidate below is a research hypothesis until prior-art and feasibility tests survive.

## Evidence constraints from this pass
- A 2026 scoping review of 123 studies reports a dual pattern: scaffolded/augmentation-oriented GenAI can support learner agency, while replacement-oriented use is associated with cognitive offloading, dependence, uncritical uptake, and weakened judgement. This supports making learner independence a first-class evaluation target, not a cosmetic feature.
- A 2026 systematic review of 53 agentic-AI-in-education studies reports major methodological weaknesses including synthetic/small benchmarks, unfair baselines, little longitudinal authentic-classroom testing, cognitive-offloading risk, and need for human oversight. This strengthens the case for strong single-agent baselines and withdrawal/independent-performance evaluation.
- Current zero-trust multi-agent engineering already uses per-agent identities, least privilege, tenant isolation and explicit authorization. Therefore 'zero trust for agents' is not itself novel; education-specific application must solve a demonstrated threat.
- Blockchain educational credentialing is already crowded in 2026: verifiable credentials, privacy-preserving credential architectures, permissioned chains, revocation, and microcredentials exist. Blockchain cannot be the novelty simply by being added to P002.
- Blockchain-backed AI provenance also exists outside education, including Merkle-style provenance DAGs and off-chain policy evaluation/on-chain enforcement. Therefore tamper-evident AI logs are prior art.
- A 2026 open learning-provenance specification (SLPT) explicitly models human judgment/cognitive delegation in AI-mediated education. Therefore 'learning provenance' and attempts to distinguish cognition from delegation are also prior art requiring direct comparison.

## Candidate innovation portfolio

### I01 — Epistemic Trust Layer (ETL)
Every knowledge-bearing object receives an authority class rather than being treated as equivalent text. Candidate classes:
- AUTHORITATIVE_SOURCE
- SOURCE_DERIVED_CLAIM
- AI_INFERENCE
- AI_GENERATED_EXAMPLE
- LEARNER_CLAIM
- UNVERIFIED_EXTERNAL_CLAIM
- CONFLICTED_CLAIM
- SUPERSEDED_CLAIM

A claim carries source/evidence identifiers, transformation parents, producing agent, uncertainty/verification state, and policy constraints. Agent repetition must not upgrade authority.

Research value: operationalize provenance as an epistemic control plane rather than only an audit log.

Novelty state: UNKNOWN/PARTIAL. Agent provenance and claim-level provenance are established; the educational authority semantics and enforcement intersection require direct prior-art testing.

### I02 — Cross-Agent Epistemic Firewall
Before one educational agent can reuse another agent's factual statement as instructional knowledge, the receiving boundary checks authority/provenance. Unsupported generated text may remain conversational context but cannot silently enter the trusted knowledge pool.

Possible enforcement rules:
1. Source-derived factual claims require evidence IDs.
2. AI inference retains derivation parents and never becomes SOURCE merely through repetition.
3. Conflicted claims cannot be presented as settled without policy-approved resolution.
4. Agent-generated examples are explicitly non-authoritative.
5. Learner claims cannot contaminate canonical course knowledge.

Novelty state: UNKNOWN. Zero-trust agent authorization exists; semantic/epistemic trust enforcement across educational agents needs deeper search.

### I03 — Pedagogical Decision Provenance (PDP)
Record why assistance changed, not merely what the model said.

Example event chain:
LearnerAttempt -> MisconceptionEvidence -> LearnerStateUpdate -> PolicyRule -> AllowedAssistanceLevel -> EvidenceSelection -> AgentAction -> LearnerResponse -> Outcome.

This separates model generation from pedagogical authorization. A teacher can inspect whether an intervention followed policy.

Novelty state: PARTIAL/UNKNOWN. Auditable learner-state updates and instructor-centered pedagogical traces exist. Need to test whether runtime policy-to-action causal provenance is already implemented comparably.

### I04 — Assistance Budget / Cognitive Autonomy Controller
Assistance is a managed resource rather than unlimited chat. Candidate ladder:
Socratic probe -> micro-hint -> conceptual hint -> source pointer -> worked substep -> full explanation.

The controller can require learner-first attempts, justification, reflection, or source inspection before escalation. The budget may adapt by mastery, task stakes, accessibility needs, and teacher policy.

Important: this is not a punitive token counter. It is a pedagogical control intended to preserve productive effort while permitting accessibility and remediation.

Novelty state: PARTIAL. Graduated hints/scaffolding are established. A longitudinal, policy-governed assistance budget tied to independent-performance evaluation may remain a useful integration hypothesis.

### I05 — Independence / AI-Withdrawal Evaluation
Evaluate two distinct constructs:
A. assisted performance;
B. retained independent competence after assistance is reduced/removed.

Candidate metrics include retention, transfer, no-AI task performance, verification behavior, calibration, time-to-independent-success, assistance escalation depth, and relapse after delay.

Novelty state: NOT NOVEL as an evaluation principle; potentially important as a mandatory system-level evaluation contract. Do not market it as invented by P002.

### I06 — Learning Trust Graph
A typed event/claim graph joins epistemic lineage and pedagogy without pretending they are the same thing.

Possible node types:
SourceArtifact, SourceFragment, EvidenceAssertion, AgentClaim, ClaimTransformation, LearnerClaim, LearnerAttempt, Misconception, PedagogicalPolicy, PedagogicalDecision, AssistanceEvent, AssessmentObservation, VerificationEvent.

Possible edges:
supports, derives_from, contradicts, paraphrases, generated_by, observed_in, triggered, authorized_by, assessed_by, supersedes.

This graph should support questions such as:
- Which source ultimately supports this teacher statement?
- Which agent introduced the unsupported transformation?
- Why was a full answer withheld?
- Did the learner later solve the concept independently?

Novelty state: UNKNOWN/PARTIAL. Typed provenance graphs are established outside education; the joined epistemic-pedagogical-outcome graph needs direct comparison with learning provenance specifications and agent tracing systems.

### I07 — Teacher-Governed Agent Constitution
Teachers configure bounded policies rather than editing giant prompts: authoritative sources, allowed external search, assistance escalation, assessment rules, role permissions, age/safety settings, model/provider boundaries, and when human review is mandatory.

Novelty state: PARTIAL. Teacher controls and machine-checkable constraints exist. The contribution would have to be stronger policy semantics/enforcement/evaluation, not a settings screen.

### I08 — Zero-Trust Educational Agent Fabric
Each agent receives explicit identity, least-privilege capabilities and scoped data access. Example: a peer agent may discuss a current topic but cannot read private assessment history; an assessment agent may access rubric and submission but cannot modify canonical materials.

Security value: limits lateral movement, accidental disclosure, cross-role leakage and tool abuse.

Novelty state: NOT NOVEL as security architecture. Potentially valuable engineering requirement for P002; no novelty claim unless education-specific threat/evaluation contributes something new.

### I09 — Verifiable Learning Record Layer (optional blockchain candidate)
Keep raw learner conversations and personal data off-chain. For selected records, produce signed/hash commitments covering assessment result, policy/model version, evidence/provenance root and issuer identity. Verification can begin with ordinary digital signatures/Merkle roots. Blockchain is introduced only if multiple mutually distrustful issuers/verifiers create a demonstrated decentralization requirement.

Decision rule: blockchain must beat a signed append-only log or verifiable-credential architecture on an explicit trust model. Otherwise reject blockchain.

Novelty state: crowded prior art. Low probability as core novelty; possible optional infrastructure feature only.

### I10 — Tamper-Evident AI Assessment Receipt
For consequential AI-assisted assessment, generate a privacy-conscious receipt containing hashes/identifiers for submission version, rubric version, evidence set, model/provider/version where available, policy version, decision trace and human overrides. The receipt is independently verifiable without exposing the learner's full private conversation.

Novelty state: UNKNOWN/PARTIAL. AI provenance and credential integrity are established separately; educational assessment receipt intersection requires prior-art search.

### I11 — Contradiction Propagation Monitor
When sources conflict or an agent transformation contradicts a trusted claim, downstream claims become flagged rather than silently remaining trusted. The system can show which lessons/questions/feedback were affected and require regeneration/review.

Novelty state: UNKNOWN. This may be a more useful differentiator than generic citation display because it treats provenance as active dependency management.

### I12 — Knowledge Git / Versioned Course Truth
Treat authoritative course knowledge and derived instructional artifacts as versioned dependencies. When a lecturer updates a source, identify affected derived claims, generated lessons, quizzes and prior explanations. Mark them stale until revalidated.

Novelty state: UNKNOWN/PARTIAL. Versioning and data lineage are established generally; educational claim invalidation across agent-generated artifacts needs research.

### I13 — Evidence-Bounded Role Disagreement
AI classmates/teacher roles may disagree pedagogically, but factual disagreement must expose evidence and authority state. The classroom can deliberately stage debates while preventing role-play from being mistaken for canonical truth.

Novelty state: UNKNOWN. Could turn multi-agent diversity from interface theatre into a controlled epistemic learning mechanism.

### I14 — Cost/Latency/Trust-Aware Agent Router
Use multiple agents only when expected educational value justifies extra latency, cost and error surface. A single tutor is the default baseline; multi-role orchestration must earn activation based on task type/pedagogical policy.

Novelty state: likely NOT NOVEL as routing/optimization; potentially important to falsify the assumption that more agents are better.

### I15 — Provenance-Aware Offline/Low-Resource Degradation
When cloud generation is unavailable, retain local source search, evidence display, learner attempts, policy enforcement and queued synchronization. The UI must explicitly distinguish locally verified/source-grounded functions from unavailable generative capabilities.

Novelty state: UNKNOWN/PARTIAL. Low-resource RAG exists. Preservation of trust/provenance semantics through offline degradation needs targeted research.

## Ranked candidates for deeper attack
Tier A — strongest research candidates, not novelty claims:
1. I02 Cross-Agent Epistemic Firewall.
2. I03 Pedagogical Decision Provenance.
3. I06 Learning Trust Graph.
4. I11 Contradiction Propagation Monitor.
5. I12 Knowledge Git / dependency invalidation.
6. I04 + I05 combined: Assistance Budget evaluated by independent competence.

Tier B — important system requirements that may support the contribution:
7. I01 Epistemic Trust Layer.
8. I07 Teacher-Governed Agent Constitution.
9. I08 Zero-Trust Educational Agent Fabric.
10. I15 Low-resource trustworthy degradation.

Tier C — useful but currently weak as core novelty:
11. I10 Assessment Receipt.
12. I13 Evidence-Bounded Role Disagreement.
13. I14 Cost/latency-aware routing.
14. I09 Blockchain/verifiable records.

## Blockchain decision
Blockchain is not selected as a core technology at this stage.

Reason:
1. 2026 educational blockchain literature already covers credentials, transcript verification, privacy-preserving verifiable credentials, permissioned/public hybrid chains, revocation and microcredentials.
2. Blockchain-backed AI provenance already exists outside education.
3. A blockchain cannot validate whether an AI claim was true at ingestion; it can make a bad record tamper-evident.
4. Educational privacy/deletion and operational complexity create additional burdens.
5. The trust problem may be solved more simply with signed records, append-only event logs, Merkle trees and verifiable credentials.

Blockchain remains an optional candidate only after a trust-boundary analysis demonstrates multiple parties who cannot rely on a common authority.

## Proposed P002 architecture hypothesis — v0.1 (research only)
P002 could be reframed as a Trustworthy Agentic Learning Environment with five planes:

1. Knowledge Plane — approved materials, retrieval and source authority.
2. Epistemic Plane — claims, derivations, conflicts, transformations and trust states.
3. Pedagogical Plane — learner state, explicit policies, assistance controller and pedagogical decision provenance.
4. Agent Plane — teacher/tutor/peer/assessment agents with scoped identities/capabilities.
5. Evaluation Plane — assisted performance, independent performance, retention, transfer, verification behavior, cost, latency and error propagation.

Optional Verification Plane — signed/Merkle/verifiable records; blockchain only if justified later.

## Candidate research contribution wording — NOT YET APPROVED
'An evidence- and policy-governed multi-agent learning architecture that prevents AI-generated conversational claims from silently acquiring source authority, records the provenance of pedagogical interventions, propagates source contradictions through derived instructional artifacts, and evaluates assistance against retained independent competence rather than assisted task performance alone.'

This wording must not be used as a novelty claim until Tier-A candidates survive direct prior-art search.

## Falsification tests
P002 should be PARKED or substantially reframed if research establishes any of the following:
- an existing educational system already combines equivalent cross-agent authority enforcement, pedagogical-decision provenance, dependency invalidation and learner-independence evaluation;
- a simpler single-agent tutor achieves equivalent learning/independence with materially lower cost, latency and error surface;
- epistemic lineage cannot be implemented reliably enough to affect behavior rather than merely produce decorative logs;
- assistance-budget controls harm accessibility or learning without measurable independence benefit;
- the proposed graph/audit mechanisms create privacy or operational burdens disproportionate to value.

## Next pass
Pass 011 should adversarially search the six Tier-A candidates across education AND adjacent fields. In particular:
- active provenance/dependency invalidation;
- truth-maintenance systems and belief revision;
- data lineage impact analysis;
- epistemic trust/authority propagation in multi-agent systems;
- pedagogical policy engines and explainable adaptive tutoring;
- fading/scaffolding/assistance withdrawal and independent competence;
- existing learning-provenance standards such as SLPT.

No coding until that attack is complete.