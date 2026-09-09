# Project Research Dossier Template

> Purpose: establish what is known, what exists, what is missing, what is feasible, and what can defensibly be claimed before substantial implementation.

## 0. Dossier Control
- Project ID:
- Working title:
- Research status: NOT STARTED / DISCOVERY / SCREENING / EVIDENCE BUILD / GAP REVIEW / FEASIBILITY REVIEW / DECISION READY
- Last updated:
- Research lead:
- Decision authority: AJ
- Search cutoff date:
- Known unresolved questions:

## 1. Project Identity
### 1.1 One-sentence concept
### 1.2 Intended users/stakeholders
### 1.3 Intended context of use
### 1.4 Candidate value proposition
### 1.5 Explicit non-goals
### 1.6 Terms requiring operational definitions

## 2. Problem Investigation
Do not begin from the proposed feature set. Establish the problem independently.

- Who experiences the problem?
- What task/outcome is difficult today?
- What evidence establishes that the problem exists?
- How severe/frequent/costly is it?
- How is it currently handled?
- What is unsatisfactory about current approaches?
- Are there contexts where the proposed solution would not be desirable?
- What evidence would falsify or substantially weaken the problem statement?

### Candidate problem statement
UNDER REVIEW until supported.

## 3. Historical / Intellectual / Technical Lineage
Research as far back as the genuine lineage warrants. Do not force arbitrary century coverage.

| Period/date | Development/work | People/org | Contribution | Relation to project | Evidence | Confidence |
|---|---|---|---|---|---|---|

Required synthesis:
- Foundational ideas
- Transitional technologies/methods
- Modern enabling technologies
- Current state of practice
- Discontinuities: ideas that look similar but are not actually ancestral

## 4. Search Protocol and Search Log
Record enough information to reproduce important searches.

| Search ID | Date | Tool/database/source class | Exact query/strategy | Scope/filters | Results screened | Included | Excluded reason summary | Notes |
|---|---|---|---|---|---:|---:|---|---|

Source classes to consider where applicable:
- peer-reviewed literature
- books/theses/technical reports
- standards/specifications
- official government/regulatory sources
- patents
- commercial products and official documentation
- open-source repositories
- datasets/benchmarks
- credible practitioner/industry evidence
- historical archives

## 5. Evidence Matrix
Prefer one row per material source-and-claim when a source supports several materially different claims.

| Evidence ID | Source | Date | Source type | Claim/finding | Method/evidence | Population/context | Limitations | Project relevance | Supports/challenges | Quality/confidence | Locator |
|---|---|---|---|---|---|---|---|---|---|---|---|

## 6. Prior-Art Register
### 6.1 Academic/research systems
| ID | System/work | Date | What it does | Evidence | Similarity | Key differences | Limitations | Novelty threat |
|---|---|---|---|---|---|---|---|---|

### 6.2 Commercial/current products
Same fields. Verify against official/current material when possible.

### 6.3 Open-source implementations
Record repository, activity/status, architecture where evidenced, feature overlap, license, limitations, and exact inspected revision/date when material.

### 6.4 Patents/standards/regulation/platform rules
Only where relevant. Separate existence of a patent from validity, enforceability, freedom-to-operate, or infringement conclusions.

## 7. Counterevidence and Novelty-Threat Register
Actively search for evidence that weakens the project case.

| Threat ID | Counterexample/evidence | Threatened claim | Severity | Resolution/status | Consequence |
|---|---|---|---|---|---|

Questions:
- Who already solves this?
- What work is closest to the proposed differentiator?
- Has the proposed combination already been implemented?
- Has a similar approach failed or produced weak/null results?
- Is the apparent gap merely a terminology/search gap?
- Is the proposed novelty only implementation detail?

## 8. Gap Analysis
A gap is not simply “I did not find a paper/product.” Characterize the reason and evidence boundary.

For each candidate gap:
- Gap statement
- Evidence showing what exists
- Evidence showing the boundary/absence/limitation
- Type: knowledge / evidence / population-context / capability / integration / usability / accessibility / security-privacy / cost-deployment / evaluation / other
- Could the gap be caused by insufficient search coverage?
- Could the gap be unimportant to users?
- Does filling it require new research, new engineering, or merely configuration/integration?
- Confidence: HIGH / MEDIUM / LOW

## 9. Claim Registry
| Claim ID | Claim | State | Supporting evidence | Contrary evidence | Scope/boundary | Allowed wording |
|---|---|---|---|---|---|---|

States: UNDER REVIEW / VERIFIED / SUPPORTED / PARTIAL / UNSUPPORTED / CONTRADICTED / SUPERSEDED.

Never upgrade claim strength merely because multiple sources repeat the same unsupported assertion.

## 10. Differentiation / Novelty Case
### 10.1 Closest comparators
### 10.2 Feature/capability comparison matrix
### 10.3 Candidate differentiators
### 10.4 Differentiators rejected after prior-art review
### 10.5 Narrow defensible novelty statement
Use bounded wording such as “Within the reviewed evidence…” rather than universal claims unless exhaustive evidence justifies them.

## 11. Feasibility Investigation
### Technical
- architecture candidates
- hardware/OS/browser/platform constraints
- data availability/quality
- model/algorithm requirements
- latency/performance/storage
- interoperability/standards
- offline/network requirements
- testing/observability

### Resource
- development time
- hardware
- cloud/API/provider costs
- licenses
- datasets
- skills/learning burden
- maintenance burden

### Feasibility experiments
| Experiment | Question | Method | Acceptance criterion | Result | Evidence | Decision impact |
|---|---|---|---|---|---|---|

## 12. Security, Privacy, Safety, Accessibility and Ethics
Scope to the project, but never omit relevant trust boundaries.

- assets and sensitive data
- actors/roles
- trust boundaries
- abuse/misuse cases
- authentication/authorization needs
- data minimization/retention/deletion
- encryption/secrets
- injection/untrusted-input risks
- dependency/supply-chain risks
- model/AI-specific risks
- privacy/consent
- safety risks
- accessibility requirements
- fairness/bias
- human oversight and appeal
- applicable regulation/policy

Security implementation does not equal security verification.

## 13. Evaluation Plan
Before implementation, define how success would be demonstrated.

- research questions/hypotheses where applicable
- baseline/comparator
- metrics and why they measure the intended construct
- qualitative evaluation
- datasets/participants/tasks
- acceptance thresholds and their justification
- threats to validity
- reproducibility
- negative/adversarial tests
- what results would count as failure

## 14. Contradictions and Unresolved Evidence
| Conflict ID | Source/evidence A | Source/evidence B | Nature of conflict | Possible explanation | Resolution status |
|---|---|---|---|---|---|

Never silently harmonize credible conflicting evidence.

## 15. Rejected Alternatives
| Alternative | Why considered | Evidence | Why rejected/deferred | Revisit condition |
|---|---|---|---|---|

## 16. Known Limitations and Unknowns
Explicitly list what research has not established.

## 17. Research Coverage Audit
Before DECISION READY, answer:
- Were synonyms and alternative terminology searched?
- Was historical lineage checked?
- Were academic and non-academic implementations checked where relevant?
- Were commercial/current products checked?
- Was open source checked?
- Were patents/standards/regulation checked where relevant?
- Was counterevidence actively searched?
- Were important findings independently corroborated where reasonable?
- Were source quality and dates assessed?
- Were contradictions retained and addressed?
- Are novelty statements bounded by actual search coverage?
- Are feasibility and resource constraints evidenced?
- Are security/privacy/ethics/accessibility risks addressed?
- Is the proposed evaluation capable of falsifying success claims?

## 18. Decision Brief
### Evidence-supported problem
### State of the art
### Closest prior art
### Remaining defensible gap
### Proposed contribution
### Feasibility
### Principal risks
### Unresolved questions
### Recommendation: GO / PARK / KILL / MORE RESEARCH
### Confidence: HIGH / MEDIUM / LOW
### Conditions before implementation

## 19. Handoff
Record exactly what the next researcher/architect/engineer should inspect first and what must not be assumed.
