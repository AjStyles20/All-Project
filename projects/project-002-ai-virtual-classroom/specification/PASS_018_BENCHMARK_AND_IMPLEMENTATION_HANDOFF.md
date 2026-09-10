# P002 Pass 018 — Benchmark and Implementation Handoff

## Status
RESEARCH PACKAGE COMPLETE / IMPLEMENTATION DEFERRED / READY FOR FUTURE PHASE 1.

## Decision
P002 has a sufficiently bounded working research theory to pause detailed development planning and move portfolio research to P003. This is not a claim that the mechanisms are proven to work; it means the hypotheses are specific, falsifiable, architecturally feasible, and ready to implement/evaluate when P002 is resumed.

## Selected research kernel
1. Authority-Preserving Learning Dependency Graph (APLDG).
2. Policy-Governed Assistance-to-Independence Contract (PGAIC).

Supporting architecture: Substitutable Human/AI Learning Role Contracts (SHARC).

Product vision: a single-user-first Personal Learning World that may later grow into a human-AI learning society.

## Benchmark domain
Initial benchmark: introductory relational databases, narrowly scoped to SQL JOIN semantics and relational reasoning.

Rationale:
- deterministic examples and expected outputs are easy to construct;
- misconceptions are common and distinguishable;
- source versions can be deliberately contradicted/superseded;
- questions can be evaluated without subjective grading;
- the domain is small enough for a controlled research prototype;
- it supports both factual dependency tests and assistance/mastery tests.

This benchmark is provisional. It may be replaced before implementation if a more defensible domain is selected, but changing it does not change the APLDG/PGAIC research hypotheses.

## Benchmark evidence pack to create when implementation resumes
- authoritative source v1;
- authoritative source v2 containing one deliberate supersession;
- one conflicting lower-authority source;
- source spans with stable IDs;
- canonical claims;
- AI-derived paraphrases;
- deliberately unsupported AI claim;
- lesson artifact depending on claims;
- quiz artifacts depending on claims;
- expected invalidation results;
- learner attempt fixtures at different assistance levels;
- delayed independent verification fixtures.

## Requirement IDs
### APLDG
- APLDG-R01: every knowledge-bearing object has provenance and authority class.
- APLDG-R02: AI transformation cannot increase authority by default.
- APLDG-R03: cross-agent reuse preserves ancestry.
- APLDG-R04: contradiction and supersession are explicit states.
- APLDG-R05: state changes propagate to dependent instructional artifacts.
- APLDG-R06: policy may block/warn on stale, conflicted, or unsupported knowledge.
- APLDG-R07: learner/community assertions require explicit promotion before canonical use.
- APLDG-R08: system can explain why a claim is trusted, unverified, stale, or conflicted.

### PGAIC
- PGAIC-R01: every assessed attempt records assistance exposure.
- PGAIC-R02: assistance escalation must be attributable to policy/evidence.
- PGAIC-R03: assisted task success cannot automatically assert independent mastery.
- PGAIC-R04: mastery evidence distinguishes cognitive help from accessibility accommodation.
- PGAIC-R05: near-miss evidence can trigger reverification.
- PGAIC-R06: independent mastery requires reduced/no-AI verification according to policy.
- PGAIC-R07: delayed evidence may reopen mastery/Knowledge Issues.
- PGAIC-R08: learner can inspect why mastery has its current state.

### Security
- SEC-R01: uploaded/retrieved content is untrusted input.
- SEC-R02: content cannot grant itself authority or tool permissions.
- SEC-R03: model output is schema-validated before state mutation.
- SEC-R04: authorization is server-side and default-deny.
- SEC-R05: secrets remain outside source control.
- SEC-R06: resource/rate limits exist for externally triggered expensive operations.
- SEC-R07: rendered content is safely encoded/sanitized.
- SEC-R08: security claims require independent verification evidence.

## APLDG truth table
| Input condition | Expected result |
|---|---|
| trusted source claim copied verbatim | derived claim retains source ancestry; authority does not exceed source |
| unsupported AI claim repeated by another AI | remains AI-derived/unverified; no authority promotion |
| trusted source v1 superseded by v2 | v1-dependent claims become stale/review-required according to edge semantics |
| trusted sources conflict | affected claim becomes conflicted; no silent winner without explicit policy |
| learner assertion contradicts source | learner assertion remains learner-provided; canonical knowledge unchanged |
| stale claim feeds quiz | quiz marked affected/review-required; not silently treated as current |

## PGAIC truth table
| Attempt | Assistance | Outcome | Expected mastery evidence |
|---|---|---|---|
| correct | none | success | eligible for independent evidence |
| correct | small hint | success | assisted evidence; may be provisional |
| correct | worked solution/direct answer | success | task success only; not independent mastery |
| correct answer + faulty reasoning | any | success | near-miss/reverification |
| assisted success followed by no-AI failure | none on verification | failure | independent mastery not verified/reopened |
| assisted success followed by delayed no-AI success | none on verification | success | eligible for independent/retained mastery |

## Baselines
B0: deterministic question/answer application with no AI.
B1: single-agent source-grounded tutor with ordinary citations.
B2: B1 plus passive provenance display, no active dependency invalidation.
B3: adaptive tutor with hints/mastery but no assistance-to-independence contract.
B4: P002 kernel with APLDG + PGAIC.

## Core experiments
E1 Source laundering: inject unsupported claim and pass through multiple AI roles.
E2 Paraphrase lineage: transform a supported claim multiple times and test ancestry retention.
E3 Supersession: replace source v1 with v2 and measure downstream stale-artifact detection.
E4 Contradiction: seed conflicting trusted evidence and verify explicit conflict handling.
E5 Assistance contrast: same learner answer under L0 and maximum assistance must yield different mastery evidence.
E6 Withdrawal: assisted success followed by no-AI failure must not be classified as independent mastery.
E7 Retention: delayed no-AI verification determines retained mastery/reopening.
E8 Security: malicious uploaded instructions must not promote authority, alter policy, or authorize tools.

## Acceptance gates before product expansion
- deterministic APLDG invariants pass 100% of seeded direct cases;
- seeded contradiction/supersession propagation reaches >=95% precision and recall in controlled fixtures;
- no direct source-authority laundering in controlled tests;
- PGAIC never promotes maximum-help success directly to independent mastery;
- accessibility accommodation is stored separately from cognitive assistance;
- security adversarial fixtures cannot mutate authority/authorization through document text;
- audit view can reconstruct state decisions without exposing hidden model chain-of-thought;
- baseline comparison shows at least one measurable benefit that justifies APLDG or PGAIC complexity.

## Technology decision
Future Phase 1 default:
- Python 3;
- FastAPI;
- SQLite initially;
- SQLAlchemy or equivalent explicit persistence layer;
- server-rendered HTML with light JavaScript;
- pytest;
- provider-neutral AI adapter;
- no graph DB until measured need;
- no React until interaction complexity justifies it;
- no blockchain/VR/social network in research kernel.

## Planned repository structure
```text
project-002-ai-virtual-classroom/
├── README.md
├── research/
├── specification/
│   ├── PASS_018_BENCHMARK_AND_IMPLEMENTATION_HANDOFF.md
│   ├── requirements/
│   │   ├── APLDG_REQUIREMENTS.md
│   │   ├── PGAIC_REQUIREMENTS.md
│   │   └── SECURITY_REQUIREMENTS.md
│   ├── architecture/
│   │   ├── SYSTEM_CONTEXT.md
│   │   ├── DATA_MODEL.md
│   │   ├── STATE_MACHINES.md
│   │   ├── THREAT_MODEL.md
│   │   └── adr/
│   ├── experiments/
│   │   ├── BASELINES.md
│   │   ├── EXPERIMENT_PLAN.md
│   │   └── ACCEPTANCE_CRITERIA.md
│   └── traceability/
│       └── REQUIREMENTS_TRACEABILITY.md
├── benchmark/
│   ├── sources/
│   ├── claims/
│   ├── contradictions/
│   ├── learner-fixtures/
│   └── expected-results/
├── src/
│   └── p002/
│       ├── domain/
│       ├── provenance/
│       ├── mastery/
│       ├── policy/
│       ├── roles/
│       ├── ingestion/
│       ├── providers/
│       ├── persistence/
│       ├── web/
│       └── security/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── adversarial/
│   └── benchmark/
└── docs/
    ├── evaluation/
    ├── reports/
    └── presentations/
```

## ADRs to instantiate on resume
ADR-001 Python/FastAPI research application.
ADR-002 SQLite before graph database.
ADR-003 deterministic policy engine owns authority/mastery state transitions.
ADR-004 provider-neutral AI boundary.
ADR-005 server-rendered UI before React.
ADR-006 no blockchain in research kernel.
ADR-007 single-user-first before social/multi-tenant expansion.

Accepted ADRs should not be silently rewritten; changed decisions should be superseded by a new ADR so rationale/history remain traceable.

## Phase 1 implementation slice when resumed
1. domain enums/types and IDs;
2. SQLite schema/migrations;
3. source + claim registry;
4. typed dependency edges;
5. authority/non-escalation policy;
6. contradiction/supersession propagation;
7. deterministic fixtures/tests;
8. audit query API;
9. only then learner assistance/mastery kernel.

## Portfolio handoff
P002 research is now sufficiently mature to pause without losing direction.

State on pause:
- research theory: bounded and falsifiable;
- novelty: hypothesis only, not final claim;
- architecture: specified at prototype level;
- benchmark: selected provisionally;
- implementation: not started;
- next action on resume: instantiate ADR/requirements files and begin deterministic Phase 1.

Recommended portfolio action: move to P003 research rather than continue expanding P002. Revisit P002 after the portfolio has comparable evidence dossiers for later ranking.
