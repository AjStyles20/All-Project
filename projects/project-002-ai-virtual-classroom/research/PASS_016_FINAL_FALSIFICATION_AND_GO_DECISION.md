# P002 Research Pass 016 — Final Falsification and GO Decision

## Status
FINAL PRE-IMPLEMENTATION FALSIFICATION / CONDITIONAL GO.

This pass attacks the three survivors from Pass 015. It does not claim that individual ingredients are unprecedented. The decision is whether P002 now has a bounded, testable systems contribution worth prototyping.

## Candidates under attack
A. Authority-Preserving Learning Dependency Graph (APLDG)
B. Policy-Governed Assistance-to-Independence Contract (PGAIC)
C. Substitutable Human/AI Learning Role Contracts (SHARC)

## New evidence pressure
### Human-AI collaboration is crowded and role allocation is not novel
2026 work increasingly treats human-AI collaboration as explicit task/decision-right allocation. A systematic review of human-AI teams covers task allocation, communication, interaction and augmentation. Education-specific work likewise distributes teaching/cognitive/social presence across teachers and AI, and medical-education work proposes explicit Automate/Augment/Reserve/Monitor task allocation. Therefore generic role allocation, human-AI teaming, or substitutable work allocation cannot be P002's primary novelty.

### Role ambiguity is itself a documented problem
Recent higher-education research frames unclear task allocation, decision authority, verification, authorship and accountability as human-AI role ambiguity. This supports explicit role contracts as governance infrastructure, but also weakens novelty claims around simply clarifying roles.

### Multi-agent systems can preserve epistemic agency
A 2026 STEM study reports a personalized multi-agent system supporting students' epistemic cognition while preserving high epistemic agency. Therefore P002 cannot claim that multi-agent learning plus epistemic agency is new.

### AI use can degrade into delegation/copying
2026 work on elementary online learning reports that lower-achieving learners more often transitioned into writing down AI outputs, while self-regulated-learning plus human-in-the-loop support reduced counterproductive AI delegation. Other 2026 work argues that short-run productivity gains can hide longer-run costs to learning and skill development. This strengthens B as an engineering/evaluation problem but does not make assistance fading or human oversight novel.

### Trace-based multi-agent evaluation is emerging
ASTRA provides a trace-ready schema for multi-agent tutoring/collaboration and reproducible interaction/participation/verification analysis. Therefore traces/auditability alone cannot be claimed as novel.

## Candidate A — Authority-Preserving Learning Dependency Graph
### Falsification question
Does prior art already provide an educational runtime in which source authority, AI transformations, agent-to-agent reuse, contradictions/supersession, and downstream instructional dependencies are machine-enforced as one active graph?

### What is already prior art
- provenance graphs and claim/source lineage;
- RAG citations and fact checking;
- truth-maintenance systems;
- data lineage/dependency impact analysis;
- OpenMAIC source-first research/fact checking and machine-checkable skill constraints;
- learning provenance specifications;
- agent trace/audit frameworks.

### Surviving intersection
The reviewed evidence has not yet established an equivalent educational runtime that simultaneously enforces:
1. authority classes for knowledge-bearing objects;
2. non-escalation of authority through AI repetition/paraphrase;
3. transformation lineage across agents;
4. contradiction/supersession propagation;
5. downstream impact marking for lessons, questions, feedback and community artifacts;
6. runtime blocking/warning policies based on those states.

This is an absence-within-reviewed-evidence result, not proof that no such system exists.

### Prototype falsification tests
A1 Source laundering: unsupported AI claim repeated by several agents must not become authoritative.
A2 Paraphrase lineage: transformed claim retains derivation ancestry.
A3 Source update: superseded source marks dependent claims/artifacts stale.
A4 Contradiction: conflicting trusted evidence propagates CONFLICTED state rather than silent resolution.
A5 Learner contamination: learner assertion cannot enter canonical knowledge without explicit verification/promotion.
A6 Trace query: system can explain why a displayed factual claim is trusted, disputed, stale or unverified.

### Decision
YES — PRIMARY RESEARCH CANDIDATE, with novelty wording strictly bounded to the reviewed intersection and prototype behavior.

## Candidate B — Policy-Governed Assistance-to-Independence Contract
### Falsification question
Does prior art already make assistance authorization, assistance exposure, near-miss handling and later unassisted competence one enforceable lifecycle rather than separate pedagogical recommendations?

### What is already prior art
- scaffolding and graduated hints;
- mastery learning;
- knowledge tracing;
- learner-state-aware adaptation;
- fading/withdrawal of support;
- self-regulated learning interventions;
- process/trace assessment;
- assisted versus unassisted testing as an evaluation idea;
- concern about cognitive offloading and overreliance.

### Surviving intersection
The possible contribution is not any individual technique. It is a machine-enforced lifecycle:
LearnerAttempt -> Evidence -> Policy -> AuthorizedAssistance -> AssistanceExposure -> Outcome -> NearMiss/ConfidenceEvidence -> ProvisionalMastery -> Reduced/No-AI Verification -> RetainedMastery or Reopen.

A mastery state must therefore carry assistance provenance. Heavy assistance can produce task success without automatically producing an independent-mastery claim.

### Prototype falsification tests
B1 Same correct answer under zero help vs full worked solution produces different mastery evidence.
B2 Assistance escalation must be attributable to explicit policy/learner evidence.
B3 Correct answer with contradictory reasoning triggers near-miss/reverification rather than unconditional mastery increase.
B4 Learner can pass assisted task and fail withdrawal check; system must distinguish those states.
B5 Accessibility accommodations must not be misclassified as cognitive dependency.
B6 Delayed verification can reopen a previously resolved knowledge issue.

### Decision
YES — CO-PRIMARY RESEARCH CANDIDATE, but contribution must be described as lifecycle integration/enforcement/evaluation, not invention of scaffolding or mastery assessment.

## Candidate C — Substitutable Human/AI Learning Role Contracts
### Falsification question
Is a machine-readable role contract whose occupant may be human or AI sufficiently distinct from existing task-allocation, hybrid-intelligence and agent-role frameworks?

### Evidence pressure
Current human-AI literature already addresses task allocation, communication, authority, accountability, shared agency, distributed facilitation and role ambiguity. Education-specific systems distribute teacher/AI functions. The conceptual space is crowded.

### What remains useful
Role contracts remain valuable product architecture because they can specify:
- occupant type;
- permissions and tools;
- data scope/privacy;
- epistemic authority;
- responsibilities;
- pedagogical purpose;
- handoff rules;
- accountability/verification requirements.

They preserve the original private-world vision: AI can occupy missing roles when AJ is the only human, while humans can later replace AI occupants without changing the learning workflow.

### Decision
PARTIAL — DEMOTE FROM CORE RESEARCH CONTRIBUTION TO SUPPORTING ARCHITECTURE/PRODUCT DIFFERENTIATOR unless later direct prior art reveals a sharper testable gap.

## Final research contribution selection
### Contribution 1 — Authority-Preserving Learning Dependency Graph
Research question:
Can an educational AI environment reduce source laundering and stale/contradicted instructional artifacts by enforcing semantic authority and active dependency propagation across source, AI, learner and community claims?

### Contribution 2 — Assistance-to-Independence Contract
Research question:
Can an AI learning environment improve the validity of mastery claims by recording assistance provenance, governing escalation and requiring reduced/no-AI verification before independent mastery is asserted?

These two contributions interact but remain independently testable.

## Product architecture retained, but not claimed as novelty
- personal learning world;
- optional human social layer;
- AI teachers/tutors/classmates;
- human/AI role contracts and handoff;
- Knowledge Issues;
- community knowledge forge;
- source-grounded lessons/Q&A;
- voice where feasible;
- learner state;
- Library/Study Hall/Lab/Debate Hall/Project Room concepts;
- optional 2D campus only after UX value is demonstrated;
- low-bandwidth/offline degradation where feasible;
- cryptographic integrity primitives where justified.

## Explicitly rejected as core novelty
- generic RAG;
- multiple AI agents/personas;
- AI classmates;
- adaptive tutoring;
- learner modeling;
- graduated hints;
- virtual/metaverse classroom;
- blockchain credentials/provenance;
- generic provenance/audit logs;
- generic human-AI collaboration;
- generic role allocation;
- generic personal learning environment;
- generic community knowledge building.

## Bounded novelty statement — research hypothesis, not final claim
Within the evidence reviewed through Pass 016, P002's strongest defensible contribution hypothesis is the integration of (1) an authority-preserving educational dependency graph that prevents AI-mediated repetition or transformation from silently upgrading epistemic authority and actively propagates contradictions/supersession to dependent instructional artifacts, with (2) a policy-governed assistance lifecycle in which mastery claims retain assistance provenance and require evidence of reduced/no-AI competence before being classified as independent mastery.

This wording MUST remain 'within reviewed evidence' until implementation and final literature review are complete.

## Architecture consequence
The research prototype should not begin as a giant virtual campus. Build the trust/learning kernel first.

Core kernel:
1. Source/Evidence Registry
2. Claim + Transformation Graph
3. Authority/Conflict Policy Engine
4. Artifact Dependency/Invalidation Engine
5. Learner Attempt/Event Store
6. Assistance Policy Engine
7. Mastery Evidence Ledger
8. Withdrawal/Reverification Scheduler
9. Knowledge Issue lifecycle
10. Explainability/Audit views

Supporting application:
11. Source-grounded tutor
12. Role-contract runtime
13. Personal learning workspace
14. Optional social/community layer after core verification
15. Optional spatial campus only after comparative UX test

## Security/privacy gates
Before multi-user/social deployment:
- tenant/user isolation;
- explicit authorization for source, learner-state and assessment access;
- untrusted-upload handling and prompt-injection tests;
- role/tool least privilege;
- safe rendering/output encoding;
- rate/resource limits;
- secrets outside source;
- deletion/export/retention policy;
- audit events without leaking private conversation content;
- community moderation/abuse controls;
- no permanent social-credit-style learner reputation;
- accessibility accommodations separated from assistance-dependence scoring.

## Implementation decision
CONDITIONAL GO.

Meaning:
- GO for a bounded research prototype of A + B.
- GO for C as supporting architecture, not research novelty.
- NO GO for building the full social/virtual campus yet.
- NO GO for blockchain as a default dependency.
- NO final novelty claim until prototype evaluation and final prior-art refresh.

## Minimum viable research prototype
A first defensible prototype should demonstrate one narrow course/topic with:
- uploaded authoritative source set;
- typed claims and transformations;
- at least two AI roles to test cross-agent source laundering;
- contradiction/supersession propagation;
- one generated lesson/question artifact with dependency invalidation;
- assistance ladder with explicit policy;
- learner attempts and assistance provenance;
- assisted vs independent mastery states;
- delayed/reduced-assistance verification;
- Knowledge Issue reopen/resolve lifecycle;
- audit/explanation views.

## Baselines
At minimum compare against:
1. single-agent source-grounded tutor without authority/dependency enforcement;
2. same tutor with ordinary citations/provenance display but no active invalidation;
3. adaptive assistance without independence contract;
4. P002 kernel with A+B enabled.

## Evaluation targets
Technical:
- source-laundering detection rate;
- lineage retention under paraphrase/agent transfer;
- contradiction propagation precision/recall on seeded cases;
- stale-artifact detection;
- policy compliance;
- authorization/security tests;
- latency/cost overhead.

Learning/evaluation validity:
- assisted task success;
- reduced/no-AI success;
- delayed retention;
- transfer;
- false mastery rate;
- near-miss recovery;
- assistance escalation depth;
- learner verification behavior.

Usability:
- can the learner explain why a claim is trusted?
- can the learner distinguish assisted from independent mastery?
- does provenance overwhelm or help?

## Kill/reframe criteria
Reframe or park the contribution if:
- a direct prior-art system is found implementing equivalent A or B behavior;
- semantic lineage is too unreliable to drive policy safely;
- active invalidation creates unacceptable false alarms;
- assistance provenance does not improve mastery validity beyond simpler assessment;
- users cannot understand the trust/mastery states;
- privacy/security burden outweighs educational value;
- a much simpler single-agent baseline achieves equivalent outcomes.

## Final Pass 016 verdict
P002 survives the research attack, but in a narrower and more defensible form.

Product vision: Personal Learning World that can later become a human-AI learning society.
Research kernel: Authority-preserving knowledge dependencies + assistance-to-independence mastery.
Supporting architecture: substitutable human/AI role contracts.
Decision: CONDITIONAL GO TO ARCHITECTURE/PROTOTYPE PLANNING, not yet unrestricted implementation.

## Next step
Pass 017 should convert this decision into a Research Prototype Specification: requirements, threat model, data model, state machines, experiment design, baselines, measurable acceptance criteria, technology selection and phased implementation plan. No full-campus/social implementation until the kernel passes verification.