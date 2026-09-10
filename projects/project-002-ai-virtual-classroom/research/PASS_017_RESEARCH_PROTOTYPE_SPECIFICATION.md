# P002 Research Pass 017 — Research Prototype Specification

## Status
ARCHITECTURE / EXPERIMENT SPECIFICATION AFTER CONDITIONAL GO.

This pass converts Pass 016 into a buildable and falsifiable research prototype. It does not authorize the full Personal Learning World, social network, virtual campus, blockchain layer, or production deployment.

## 1. Prototype objective
Build the smallest system capable of testing two co-primary research hypotheses:

A. Authority-Preserving Learning Dependency Graph (APLDG): educational claims and derived artifacts can retain explicit epistemic authority and transformation lineage, while contradiction/supersession actively affects dependent outputs.

B. Policy-Governed Assistance-to-Independence Contract (PGAIC): successful AI-assisted task completion must remain distinguishable from independently demonstrated mastery, with assistance provenance and later reduced/no-AI verification.

Supporting architecture: machine-readable role contracts may assign bounded functions to AI or human occupants, but role substitution is not claimed as core novelty.

## 2. Scope boundary
### In prototype
- one bounded course/topic;
- authoritative source ingestion;
- typed claims;
- claim-source and claim-claim dependencies;
- AI transformations with lineage;
- at least two AI roles for source-laundering tests;
- contradiction and supersession states;
- one or more derived lesson/question artifacts;
- active stale/conflict propagation;
- learner attempts;
- explicit assistance ladder;
- assistance provenance;
- assisted/provisional/independent mastery distinction;
- reduced/no-AI verification;
- Knowledge Issue lifecycle;
- trust/mastery audit views;
- deterministic security/policy checks around LLM use.

### Explicitly out of prototype
- 3D/VR campus;
- public social network;
- blockchain;
- credentials;
- emotion/body-language inference;
- automated high-stakes grading;
- permanent social reputation;
- large autonomous agent society;
- native mobile/desktop apps;
- production-scale multi-tenancy.

## 3. Functional requirements
### FR-A — Evidence and authority
A01. Every ingested source receives a stable source/version ID, content hash, origin metadata, trust/approval state, and ingestion timestamp.
A02. Every factual claim used by the learning runtime has a stable claim ID and an authority class.
A03. A claim may cite one or more evidence spans/sources.
A04. AI-generated claims default to GENERATED/UNVERIFIED and cannot silently become AUTHORITATIVE.
A05. Paraphrase, summary, aggregation, inference, contradiction, correction, and supersession are explicit transformation/dependency edge types.
A06. Agent-to-agent transfer preserves claim identity or derivation ancestry.
A07. Repetition by another agent cannot increase authority without an explicit promotion rule backed by eligible evidence/human approval.
A08. Source supersession triggers downstream impact analysis.
A09. Conflicting trusted evidence produces CONFLICTED state unless a defined adjudication rule resolves it.
A10. Derived lessons/questions/feedback retain dependency links to claims used to construct them.
A11. A dependent artifact can be CURRENT, REVIEW_REQUIRED, STALE, CONFLICTED, or INVALID according to deterministic policy.
A12. The UI can answer: Why is this claim trusted? Where did it come from? What transformed it? What depends on it? Why is this artifact stale/conflicted?

### FR-B — Assistance and mastery
B01. Every assessable learner attempt has an attempt ID, task/concept IDs, timestamp, response, outcome, confidence where collected, and assistance exposure.
B02. Assistance is represented by explicit levels rather than a binary AI-used flag.
B03. Assistance escalation is governed by policy and logged with reason/evidence.
B04. Accessibility accommodations are recorded separately from cognitive assistance and must not reduce mastery merely because accommodation was used.
B05. Correct outcomes after substantial cognitive assistance do not automatically assert independent mastery.
B06. Contradictory reasoning, unsupported evidence, guessing indicators, or answer/reason mismatch may create a NEAR_MISS event.
B07. Mastery evidence has provenance to attempts and assistance exposure.
B08. Mastery states distinguish at minimum UNKNOWN, ASSISTED_SUCCESS, PROVISIONAL, VERIFYING, INDEPENDENT, and REOPENED.
B09. Independent mastery requires an eligible reduced/no-AI verification attempt under configured policy.
B10. Delayed verification can preserve, downgrade, or reopen mastery/Knowledge Issues.
B11. UI must show assisted performance separately from independently verified performance.

### FR-C — Knowledge Issues
C01. Learner confusion/misconception can create a persistent Knowledge Issue.
C02. States: OPEN -> WORKING -> VERIFYING -> RESOLVED, with RESOLVED -> REOPENED permitted.
C03. Closing requires evidence specified by policy, not merely an AI explanation.
C04. Issue history preserves explanations attempted, assistance, relevant claims/sources, verification attempts, and reopening reason.

### FR-D — Role contracts
D01. Role contract defines role purpose, occupant type, permitted tools, data scope, epistemic authority ceiling, and allowed actions.
D02. AI role cannot exceed its authority ceiling through prompt output.
D03. At least two AI roles are implemented solely to test cross-agent claim transfer/source laundering.
D04. Role handoff must not erase claim/evidence lineage.

## 4. Non-functional requirements
N01. Explainability: trust/mastery decisions expose deterministic reasons and relevant IDs.
N02. Reproducibility: seeded test scenarios can be replayed.
N03. Auditability: security/policy events are append-oriented and timestamped.
N04. Performance: ordinary local prototype interactions should remain usable on modest hardware; expensive AI operations must be optional/provider-adapted.
N05. Portability: core policy/graph/mastery logic must not depend on one LLM vendor.
N06. Graceful degradation: deterministic kernel remains inspectable when no LLM provider is configured.
N07. Accessibility: keyboard operation, semantic HTML, readable status text, no color-only meaning; speech is optional enhancement.
N08. Low bandwidth: no heavy 3D/frontend framework required for the kernel prototype.

## 5. Proposed technology selection
### Application
- Python 3.12+ where available; remain compatible with a practical supported Python 3.x baseline.
- FastAPI for HTTP/application API and server-side orchestration.
- Jinja2/server-rendered HTML plus modest vanilla JavaScript/HTMX-style interactions if needed; React is not justified for the research kernel.
- SQLite for the prototype, using foreign keys, transactions, indexes and FTS5 where useful.
- SQLAlchemy 2.x or equivalent explicit repository layer to keep storage replaceable.
- Pydantic for typed boundaries/schema validation.
- pytest for unit/integration/security regression tests.

### AI/provider boundary
Define provider interfaces for generation/structured extraction. Core graph authority, state transitions, authorization, invalidation and mastery decisions MUST be deterministic application code, never delegated solely to an LLM.

### Why not a graph database initially
The prototype graph is bounded and requires transactional relational data, auditable edge types, reproducible tests and easy local operation. SQLite adjacency/edge tables are sufficient. A graph DB is reconsidered only if measured traversal/query complexity justifies it.

### Why not React initially
The research questions concern trust dependencies and mastery validity, not frontend framework complexity. Server-rendered pages reduce implementation/security burden and fit modest hardware. React remains an optional later product decision.

## 6. Logical architecture
1. Source Registry
2. Content Extraction/Chunk Registry
3. Claim Registry
4. Transformation + Dependency Graph
5. Authority Policy Engine
6. Conflict/Supersession Propagation Engine
7. Derived Artifact Registry
8. Learner Event Store
9. Assistance Policy Engine
10. Mastery Evidence Engine
11. Verification/Reverification Scheduler
12. Knowledge Issue Service
13. Role Contract/Authorization Service
14. Provider Adapter Layer
15. Audit/Explainability Service
16. Server-rendered Web UI

Rule: LLM output enters the system as untrusted/generated data until deterministic validation/promotion policy permits stronger status.

## 7. Core data model
### Source
id, title, source_type, origin, version_label, sha256, approval_state, authority_class, created_at, supersedes_source_id nullable.

### SourceSpan
id, source_id, locator/page/section, extracted_text, hash.

### Claim
id, canonical_text, claim_type, authority_class, status, created_by_type, created_by_id, created_at.

Suggested authority classes:
- CANONICAL_APPROVED
- TRUSTED_REFERENCE
- HUMAN_ASSERTION
- AI_DERIVED
- COMMUNITY_ASSERTION
- UNVERIFIED

Status is separate from authority:
- CURRENT
- UNVERIFIED
- CONFLICTED
- STALE
- SUPERSEDED
- REJECTED

### EvidenceLink
claim_id, source_span_id, relation (SUPPORTS/CONTRADICTS/QUALIFIES), strength/verification metadata.

### ClaimEdge
from_claim_id, to_claim_id, transformation_type, actor_role_id, model/provider metadata where applicable, created_at.
Transformation types: PARAPHRASE, SUMMARY, INFERENCE, AGGREGATION, CORRECTION, CONTRADICTION, SUPERSESSION, REUSE.

### LearningArtifact
id, artifact_type, content/version, status, created_at.

### ArtifactDependency
artifact_id, claim_id, dependency_type, required_authority_threshold.

### RoleContract
id, name, purpose, occupant_type, authority_ceiling, permissions, tool_scope, data_scope.

### LearnerAttempt
id, learner_id, task_id, concept_id, response, outcome, reasoning, confidence, started_at, submitted_at.

### AssistanceEvent
id, attempt_id, level, assistance_type, policy_reason, content_reference, actor_role_id, timestamp.

Proposed cognitive assistance ladder:
L0 none
L1 metacognitive prompt
L2 conceptual cue
L3 targeted hint
L4 partial procedure/example
L5 worked reasoning scaffold
L6 direct solution/answer

Accessibility support is a separate field/category and not mapped automatically to L1-L6.

### MasteryEvidence
id, learner_id, concept_id, attempt_id, evidence_type, assistance_level, score, eligible_for_independent_mastery, timestamp.

### MasteryState
learner_id, concept_id, state, confidence/score if used, last_verified_at, next_verification_at, reason.

### KnowledgeIssue
id, learner_id, concept_id, description, state, opened_at, resolved_at nullable, reopen_count.

### AuditEvent
id, event_type, actor, object_type/id, deterministic_reason_code, safe_metadata, timestamp.

## 8. Authority state machine
Claim creation -> UNVERIFIED by default for AI/community/learner assertions.

Eligible evidence/policy may promote authority only through an explicit transition service. No model response can write authority directly.

Source update paths:
CURRENT SOURCE -> SUPERSEDED SOURCE
-> traverse supported claims
-> mark affected claim state STALE or REVIEW_REQUIRED according to dependency semantics
-> traverse derived claims/artifacts
-> recompute status
-> surface impact report.

Conflict path:
Trusted Source A SUPPORTS Claim X + Trusted Source B CONTRADICTS Claim X
-> Claim X = CONFLICTED
-> dependent artifact policy evaluated
-> artifact may become REVIEW_REQUIRED/CONFLICTED/INVALID
-> no silent winner unless explicit adjudication policy/human decision exists.

Non-escalation invariant:
authority(derived claim) <= maximum authority permitted by derivation policy and evidence; repetition/paraphrase alone cannot increase authority.

## 9. Mastery state machine
UNKNOWN
-> ASSISTED_SUCCESS when task success depends on assistance above independent threshold
-> PROVISIONAL when evidence is promising but independent verification is outstanding
-> VERIFYING when a reduced/no-AI check is scheduled/active
-> INDEPENDENT when eligible verification criteria pass
-> REOPENED when delayed retention/transfer/contradictory evidence invalidates prior confidence.

A learner may move UNKNOWN -> PROVISIONAL/VERIFYING directly after strong low/no-assistance evidence depending on policy.

Critical invariant:
Task outcome and mastery classification are separate variables.

## 10. Knowledge Issue state machine
OPEN -> WORKING -> VERIFYING -> RESOLVED
RESOLVED -> REOPENED -> WORKING

Resolution policy should require evidence such as independent explanation/application or eligible verification, not AI acknowledgement.

## 11. Threat model
### Assets
- authoritative course material and source integrity;
- learner private data/history;
- mastery records;
- role permissions;
- provider credentials;
- claim/lineage graph integrity;
- assessment/verification integrity;
- audit evidence.

### Adversaries/failure sources
- malicious uploaded document;
- prompt injection embedded in sources;
- malicious/curious user in later multi-user mode;
- compromised or hallucinating model/provider;
- poisoned community content;
- unauthorized role/agent;
- application bug;
- stale source data;
- accidental learner misinformation;
- resource-exhaustion input.

### Required controls
- uploaded/retrieved content treated as untrusted data, not instructions;
- file type/size/count/resource limits and safe extraction;
- SHA-256 source integrity metadata;
- server-side prompt construction;
- structured output/schema validation;
- least-privilege role/tool authorization in application code;
- no secrets in repository/client;
- parameterized ORM/query usage;
- output escaping/sanitization;
- CSRF/session/CORS protections as applicable to chosen deployment;
- rate/resource limits;
- explicit tenant isolation before multi-user release;
- deterministic authority/mastery transitions;
- human approval for high-impact knowledge promotion where policy requires;
- safe error handling;
- audit logs that avoid unnecessary private content;
- dependency review and pinned/reproducible environment strategy;
- adversarial tests for direct/indirect prompt injection, RAG poisoning, source laundering, authorization bypass and cross-user leakage before any social release.

Security rationale: OWASP explicitly treats indirect prompt injection and RAG poisoning as practical risks and recommends segregating untrusted content, least privilege, validation and adversarial testing. NIST's GenAI profile treats provenance as useful for tracing origin/history and downstream accountability. These are baseline controls, not P002 novelty.

## 12. Experiment design
### Experiment A — Authority/dependency enforcement
Construct a controlled source corpus containing:
- supported facts;
- one intentionally unsupported AI assertion;
- one source version update;
- one explicit contradiction between trusted sources;
- paraphrase/summary/inference transformations;
- derived lesson/question artifacts.

Conditions:
A0 single-agent grounded tutor, citations only.
A1 provenance display but no active authority/invalidation policy.
A2 P002 APLDG enabled.

Primary technical outcomes:
- source-laundering detection rate;
- lineage retention rate after transformations;
- contradiction detection/propagation precision and recall;
- stale artifact detection precision/recall;
- false invalidation rate;
- explanation completeness;
- latency/token/storage overhead.

### Experiment B — Assistance/mastery validity
Create concept tasks with staged assistance and later reduced/no-AI checks.

Conditions:
B0 ordinary adaptive/help-enabled tutor treating correct task completion as performance evidence.
B1 assistance logged but no mastery contract.
B2 P002 PGAIC enabled.

Outcomes:
- assisted task success;
- independent verification success;
- delayed retention/transfer where feasible;
- false mastery rate, operationalized against later independent check;
- near-miss detection precision on seeded scenarios;
- assistance escalation depth;
- rate of mastery reopening after failed verification.

Important: an initial prototype can validate system behavior with seeded/simulated scenarios. Claims about improved human learning require a later ethically designed human evaluation and cannot be inferred from software tests alone.

## 13. Baseline fairness
All compared systems should use the same source corpus, tasks, provider/model where practical, temperature/configuration, retrieval limits and evaluation cases. P002 must not receive privileged information unavailable to baselines except the mechanism being tested.

## 14. Acceptance criteria for prototype gate
### APLDG gate
- 100% of seeded direct source-laundering cases prevented from automatic authority escalation;
- >=95% expected lineage edges retained in deterministic seeded transformations; semantic/LLM extraction cases reported separately;
- >=95% precision and recall for deterministic seeded contradiction/supersession propagation cases;
- no silent conflict resolution in seeded trusted-source conflicts;
- every displayed trust state has a machine-readable reason and inspectable path;
- false invalidation rate measured and <=5% on the deterministic benchmark before broader experimentation.

### PGAIC gate
- correct L0 and correct L6 attempts produce distinguishable mastery evidence in 100% of deterministic policy tests;
- no L6 direct-solution success can automatically produce INDEPENDENT mastery under default policy;
- all assistance escalations record policy reason and exposure;
- accessibility accommodation alone never lowers mastery in policy regression tests;
- failed withdrawal verification can reopen/downgrade state correctly in 100% of state-machine tests;
- every mastery state exposes its evidence trail.

### Security gate
- authorization tests cover all state-changing endpoints;
- direct/indirect prompt-injection fixtures cannot directly modify policy/authority/mastery state;
- malformed model outputs fail closed at typed boundaries;
- uploaded content cannot invoke tools or bypass role authorization;
- secrets absent from committed source;
- dependency and static/security checks documented;
- no claim of production security until deployment-specific verification exists.

## 15. Phased implementation plan
### Phase 0 — Specification lock
- convert this pass into formal requirements/test IDs;
- choose one narrow learning topic and controlled corpus;
- create architecture decision records;
- define benchmark fixtures before feature coding.

### Phase 1 — Deterministic trust kernel
- Source/Span/Claim/Edge schema;
- authority classes/statuses;
- promotion/non-escalation rules;
- contradiction/supersession propagation;
- artifact dependency invalidation;
- audit/explainability queries;
- tests first/alongside implementation.

Exit: APLDG seeded tests pass without any LLM requirement.

### Phase 2 — Deterministic mastery kernel
- attempts;
- assistance events/ladder;
- mastery evidence/state machine;
- Knowledge Issues;
- verification/reopening;
- accessibility separation;
- tests.

Exit: PGAIC deterministic state/policy tests pass.

### Phase 3 — Source-grounded tutor integration
- document ingestion/extraction;
- retrieval;
- provider interface;
- structured claim extraction/generation;
- two bounded AI roles;
- role contracts;
- cross-agent lineage/source-laundering scenarios;
- prompt-injection defenses.

Exit: model/provider cannot bypass deterministic kernel invariants.

### Phase 4 — Research UI
- personal workspace;
- source/claim explorer;
- trust badge + Why? path;
- lesson/question flow;
- assistance controls/history;
- assisted vs independent mastery dashboard;
- Knowledge Issues;
- audit/impact report.

Exit: user can inspect rather than merely be told trust/mastery state.

### Phase 5 — Baseline/evaluation harness
- A0/A1/A2 and B0/B1/B2 configurations;
- reproducible benchmark cases;
- metrics export;
- latency/cost measurements;
- security regression suite;
- results documentation.

Exit: evidence supports GO/REFRAME/PARK decision for each contribution.

### Phase 6 — Only after kernel evidence
Consider product expansion: richer AI roles, human collaboration, community layer, low-bandwidth/offline work, voice, optional spatial interface. Each requires separate requirements/security/UX review.

## 16. Proposed repository implementation structure
projects/project-002-ai-virtual-classroom/
- README.md
- research/
- docs/
  - architecture/
  - threat-model/
  - evaluation/
- app/
  - domain/
  - policies/
  - services/
  - providers/
  - repositories/
  - web/
  - templates/
  - static/
- migrations/
- tests/
  - unit/
  - integration/
  - security/
  - benchmarks/
- fixtures/
  - sources/
  - benchmark_cases/
- scripts/

Exact layout may change through an explicit architecture decision before coding.

## 17. Key invariants to encode as tests
I01 AI output cannot directly set authoritative status.
I02 Repetition/paraphrase cannot by itself raise authority.
I03 Conflict between qualifying trusted evidence cannot silently disappear.
I04 Superseded evidence triggers deterministic downstream impact recomputation.
I05 Artifact status is derived from dependencies/policy, not LLM opinion.
I06 Role authorization is enforced outside prompts.
I07 Correct answer and independent mastery are not synonymous.
I08 Assistance exposure is immutable/auditable enough for the prototype evaluation.
I09 Accessibility support is not automatically cognitive assistance.
I10 Mastery can be reopened by later contradictory performance.
I11 Untrusted retrieved/uploaded content cannot directly cause tool/action authorization.
I12 Baseline and P002 evaluation cases use equivalent source/task inputs.

## 18. Kill/reframe gates carried forward
A must be reframed/parked if direct equivalent prior art is found, semantic lineage is too unreliable, invalidation false positives are unacceptable, or a citations-only baseline provides equivalent practical value.

B must be reframed/parked if assistance provenance does not improve validity of mastery classification over a simpler independent-test design, if near-miss signals are too unreliable, or if the policy penalizes legitimate accessibility/support needs.

The overall prototype should be parked if complexity/security/privacy burden overwhelms the measurable educational/research value.

## 19. Decision after Pass 017
GO to Phase 0 specification lock and Phase 1 deterministic trust-kernel planning.

This is not unrestricted implementation approval. The full Personal Learning World remains the product vision, while the next engineering work is deliberately limited to the research kernel and its verification harness.

## 20. Immediate next pass
Pass 018 should perform the Phase 0 lock:
- choose the narrow benchmark learning domain/corpus;
- convert requirements/invariants into traceable IDs;
- write ADRs for FastAPI/SQLite/server-rendered UI/relational graph/provider boundary;
- define benchmark fixtures and expected truth tables;
- define the first implementation slice and test plan;
- update project-control state before code begins.
