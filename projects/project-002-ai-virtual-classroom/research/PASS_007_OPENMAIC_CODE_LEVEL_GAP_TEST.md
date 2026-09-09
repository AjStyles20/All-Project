# Project 002 — Research Pass 007
## OpenMAIC Code-Level Gap Test: Provenance, Pedagogical Constraints, and Trust Boundaries

**Date:** 2026-09-09
**Status:** EVIDENCE BUILD / CODE-LEVEL PRIOR-ART REVIEW
**Decision:** MORE RESEARCH — no implementation approval and no novelty conclusion.

## Purpose
Pass 006 identified cross-agent epistemic provenance and inspectable pedagogical governance as the strongest surviving candidate directions. This pass tests those directions against current OpenMAIC source code rather than product descriptions alone.

## 1. Scope and evidence discipline
This pass inspected current OpenMAIC code/search results at commit `29735f10d0081859ac3db1a50a0cc92f46436004` surfaced by the connected GitHub repository. It also reviewed current release information. Findings describe inspected code only; absence from the searched files is not proof that a capability does not exist elsewhere.

Labels used:
- **VERIFIED FACT** — directly supported by inspected source/release material.
- **REASONED INFERENCE** — follows from inspected design but requires broader verification.
- **UNKNOWN** — not established by this pass.
- **NOVELTY THREAT** — prior art materially overlaps a candidate P002 contribution.

## 2. OpenMAIC already has machine-checked pedagogical structure
**VERIFIED FACT / NOVELTY THREAT.**

OpenMAIC's `lib/server/agent-runtime/skills.ts` explicitly separates a model-visible `SKILL.md` pedagogical/instructional contract from an optional `outline-constraints.json` structural contract. The code documents three stages:
1. agent skill discovery/invocation;
2. skill body plus rendered constraints passed into outline generation;
3. post-generation machine checking of the returned outline, with violations returned as diagnostics.

The `OutlineConstraints` interface supports scene-count bounds, allowed scene types, first-scene type, type-mix floors/ceilings, required/allowed widget types, required widget-outline fields, and a no-consecutive-same-widget rule.

### Consequence
P002 cannot claim novelty merely from:
- pedagogy represented outside a hidden system prompt;
- machine-checkable teaching constraints;
- structural validation of generated lesson plans;
- reusable pedagogical skills;
- diagnostics when generated structure violates constraints.

The surviving question must be narrower: whether P002 can make **instructional decisions and evidence dependencies inspectable at runtime**, not merely constrain the generated lesson structure.

## 3. OpenMAIC already has explicit source-grounding workflows
**VERIFIED FACT / MAJOR NOVELTY THREAT.**

The current `deep-research` skill requires research-first course construction for externally checkable/current facts. It instructs the agent to:
- begin with session materials;
- split a topic into research facets;
- search within a bounded budget;
- fetch and read sources;
- maintain a running **claim → source ledger**;
- cross-check conflicts;
- refuse to silently average or resolve genuine source conflicts;
- place sourced facts and attribution into page briefs;
- pass sourced facts through `generate_scene.materialFacts`;
- avoid inventing sources/citations/publication dates.

The skill explicitly states that only ledgered claims may enter the course as researched facts and that a load-bearing single-source claim should be softened, attributed, or dropped.

### Consequence
The earlier candidate differentiator "course facts have provenance" is too broad. OpenMAIC has an explicit claim-to-source ledger and source-grounded generation workflow.

## 4. OpenMAIC also has a factual-verification workflow
**VERIFIED FACT / NOVELTY THREAT.**

The `fact-check` skill scans completed course content for high-signal factual risks, checks user materials first, uses web research for selected current/disputed/specialist claims, distinguishes inconclusive verification from falsity, preserves approved-input boundaries, and requires user choice before changing approved inputs that conflict with external evidence.

### Consequence
P002 cannot claim novelty from "fact checking generated lessons," "checking hallucinations," "preserving uploaded materials as an authority boundary," or "human approval before overriding an approved source" by themselves.

## 5. OpenMAIC has explicit prompt-injection treatment for materials
**VERIFIED FACT / SECURITY NOVELTY THREAT.**

`lib/server/agent-runtime/material-tools.ts` treats fetched/extracted material as untrusted content. Material text returned to the model is wrapped in a random-nonce fence with an explicit policy that text inside is data rather than instructions. The implementation checks that the nonce does not occur in the payload before using it. The code comments explicitly identify unfenced material text as a prompt-injection channel.

The same source also documents session-scoped material access and fail-closed behavior for missing/invisible material IDs. Search results additionally show explicit handling of user-authored skills as low-priority untrusted guidance.

### Consequence
P002 cannot use basic "uploaded documents are treated as untrusted" or "prompt injection is considered" as novelty. These remain mandatory security requirements.

## 6. OpenMAIC has meaningful ownership and storage boundaries
**VERIFIED FACT.**

Current material code describes extracted text stored in a hash-addressed asset registry under a per-session principal. Session-material resolution is scoped so foreign/stale asset references fail rather than resolving another session's content. Current release notes also describe owner-scoped resources, server-backed persistence, runtime/document/asset stores, and recent security fixes for path containment and stored HTML sanitization.

### Consequence
Tenant/session isolation, safe material storage, path containment, sanitization, and owner scoping are baseline architecture/security requirements rather than P002 differentiators.

## 7. What remains unproven in OpenMAIC
The source review weakens several P002 ideas, but it does **not** yet establish the following.

### 7.1 Cross-agent epistemic lineage
**UNKNOWN.**

The deep-research workflow has a claim-to-source ledger for course construction, but this pass did not establish a durable runtime graph such as:

`source fragment -> claim -> agent A statement -> agent B transformation -> learner response -> assessment claim`

where each downstream factual assertion carries machine-inspectable evidence lineage and uncertainty across agent-to-agent dialogue.

Important distinction: a course-generation ledger is not automatically the same thing as runtime cross-agent provenance.

This remains a candidate gap, **not a novelty claim**.

### 7.2 Runtime pedagogical decision trace
**UNKNOWN / NARROWED.**

OpenMAIC clearly has machine-checked structural pedagogical constraints. This pass did not establish that each runtime decision — e.g. why a teacher withheld an answer, chose a hint, called on a peer, escalated difficulty, remediated a misconception, or allowed progression — is represented as an inspectable decision record tied to pedagogical policy, learner state, and evidence.

This is narrower than "inspectable pedagogy" and should be researched as **runtime pedagogical decision provenance**.

### 7.3 Epistemic separation between agents
**UNKNOWN.**

This pass did not establish whether one agent's unsupported generated statement can later be consumed by another agent as if it were authoritative course evidence, nor whether agent-to-agent claims carry authority labels that prevent conversational hearsay from becoming source truth.

This is now a high-priority technical question.

### 7.4 Learner-agency safeguards as enforceable policy
**PARTIAL / UNKNOWN.**

Current OpenMAIC has pedagogical skills, quizzes, fact checking, and constraints. This pass did not establish a general enforceable policy layer for learner-first attempts, staged hint budgets, delayed answers, required justification, post-assistance independence tests, or measured offloading/overreliance.

However, absence has not been proven. Search the code and research literature further before treating this as a gap.

## 8. Updated candidate contribution
The candidate P002 contribution must now be narrower than Pass 006:

> Investigate whether a learning environment can preserve machine-inspectable epistemic lineage across multi-agent interactions, separate source authority from agent-generated conversational claims, expose runtime pedagogical decision provenance, and preserve learner agency — then demonstrate whether those mechanisms improve reliability and learning relative to a strong source-grounded single-agent tutor.

**State:** UNVERIFIED HYPOTHESIS. This is not yet a novelty statement.

## 9. Proposed technical objects for gap testing
Do not implement these yet. They define what to search for in prior art.

Potential evidence/provenance model:
- `SourceArtifact`
- `SourceFragment`
- `EvidenceAssertion`
- `AgentClaim`
- `ClaimTransformation`
- `AuthorityClass`
- `UncertaintyState`
- `PedagogicalDecision`
- `LearnerAttempt`
- `AssistanceEvent`
- `AssessmentObservation`

Candidate invariant:

> No agent-generated factual claim becomes authoritative evidence merely because another agent repeated, summarized, or transformed it.

Candidate pedagogical invariant:

> Assistance escalation must be attributable to an explicit policy/learner-state condition, and independent performance after assistance must remain measurable.

These are architecture hypotheses to investigate, not approved design.

## 10. Security implications discovered from competitor code
OpenMAIC's current code/release history demonstrates that a serious implementation in this space must treat security as continuous rather than a one-time checklist. Relevant observed controls/issues include:
- untrusted-material prompt-injection framing;
- session/owner scoping;
- fail-closed material lookup;
- path-containment hardening;
- stored-HTML sanitization;
- SSRF/credential-forwarding fixes;
- sandbox tightening for interactive content.

For P002, the threat model must eventually include at minimum:
- malicious uploaded educational material;
- indirect prompt injection;
- cross-workspace/learner data leakage;
- source-authority spoofing;
- agent-to-agent trust escalation;
- malicious generated interactive HTML/code;
- SSRF/external fetch abuse;
- model/provider secret leakage;
- unauthorized teacher/admin actions;
- poisoned retrieval/evidence;
- fabricated provenance links;
- assessment manipulation;
- resource exhaustion/cost abuse.

## 11. Updated novelty-threat register
### Now materially weakened or rejected as standalone differentiators
- multi-agent classroom;
- uploaded-material grounding;
- claim-to-source ledger during course research;
- factual verification/fact-checking;
- machine-checkable lesson/pedagogy structure;
- reusable teaching skills;
- source conflict handling;
- human approval around source conflicts;
- untrusted-document prompt-injection framing;
- session-scoped materials;
- owner-scoped persistence;
- local/cloud provider flexibility.

### Still under adversarial review
- durable cross-agent claim/evidence lineage;
- authority-preserving agent-to-agent communication;
- runtime pedagogical decision provenance;
- enforceable learner-agency/anti-offloading policy;
- evaluation against an equivalent strong single-agent baseline;
- low-resource trustworthy degradation where provenance/governance remains intact.

## 12. Evaluation consequence
If these candidate mechanisms survive prior-art review, evaluation must separate at least two questions:

1. **Epistemic reliability:** Does provenance-aware multi-agent interaction reduce unsupported claim propagation, source laundering, contradiction, or evidence loss compared with ordinary multi-agent and single-agent systems?
2. **Educational value:** Does governed multi-role interaction improve retention, transfer, independent performance, source-verification behavior, or calibrated reliance enough to justify additional complexity/cost?

A system can succeed on one and fail on the other. Both results must be reportable.

## 13. Kill / reframe criteria strengthened
P002 should be parked or reframed if deeper review shows that current systems already implement and evaluate the same cross-agent epistemic lineage and runtime pedagogical-decision mechanisms, or if those mechanisms add engineering complexity without measurable reliability/learning benefit.

It should also be reframed if the strongest contribution becomes an infrastructure/provenance framework rather than a "virtual classroom" product. The research question has priority over preserving the original product label.

## 14. Next research targets
1. Search OpenMAIC code specifically for claim IDs, citation/source IDs in generated scenes, agent-message provenance, authority labels, evidence graphs, and runtime decision logs.
2. Inspect the actual multi-agent orchestration state/message schema to see what information agents pass to one another.
3. Inspect generation scene schemas to determine whether citations/provenance are first-class data or rendered text only.
4. Search other educational multi-agent systems for epistemic/provenance graphs and pedagogical decision traces.
5. Search broader multi-agent/RAG research outside education for provenance-preserving agent communication; a contribution need not be novel globally merely because education products lack it.
6. Investigate standards/provenance models (e.g. general data provenance) before inventing a custom representation.
7. Continue learner-agency/cognitive-offloading evidence review and define measurable outcomes.
8. Do not implement until these searches materially reduce the UNKNOWN fields.

## 15. Current decision
**MORE RESEARCH.**

Pass 007 significantly raises the bar again. OpenMAIC already implements more evidence discipline, pedagogical constraint checking, source grounding, prompt-injection handling, and fact verification than product-level inspection revealed. The strongest surviving P002 direction is therefore not generic provenance or inspectable pedagogy; it is the much narrower question of **cross-agent epistemic lineage plus runtime pedagogical decision provenance**, coupled with measurable learner-agency outcomes.
