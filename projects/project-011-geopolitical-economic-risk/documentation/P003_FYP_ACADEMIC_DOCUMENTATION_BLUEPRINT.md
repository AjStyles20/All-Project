# P003 — FYP Academic Documentation Blueprint

**Project:** Geopolitical Risk to Economic Impact Forecasting & Warning System  
**Canonical ID:** P003  
**Purpose:** Define the academic report structure without presenting unfinished experiments as completed results.

## Documentation rule

The report must distinguish four evidence classes throughout:

1. **Established literature/background** — claims supported by cited external sources.
2. **Project design/implementation** — what P003 specifies or implements.
3. **Observed project evidence** — actual software tests, frozen historical reconstructions and completed experimental observations.
4. **Pending evidence** — planned B2 executions, independent reviewer judgments and M10 comparative results.

Do not move a statement from class 4 to class 3 merely because the software for collecting it exists.

---

# Chapter One — Introduction

## 1.1 Background of the Study
Build the argument from:
- geopolitical events can propagate through trade, commodity, logistics, policy and financial channels;
- downstream national effects depend on country-specific exposure and domestic transmission;
- language models and narrative systems can produce plausible explanations even where evidentiary links are incomplete;
- reliable warning therefore requires explicit separation of verified events, measured exposure, supported transmission, bounded scenarios and quantitative forecasts.

External citations are required here. Do not derive general geopolitical/economic facts from P003 fixtures alone.

## 1.2 Problem Statement
Core project problem:

> Existing geopolitical-economic narratives can move from a real international event to a specific Nigerian economic consequence without making every required transmission link explicit or evidentially sufficient. This creates a risk that fluent or high-salience explanations overstate what the available evidence can support.

Then identify the technical/research problem: how to constrain downstream claim progression when required evidence is missing, stale, conditional, contested or contradicted.

## 1.3 Aim
Suggested academic aim:

> To design and evaluate an evidence-constrained geopolitical-to-economic warning framework that governs downstream Nigerian economic claims using typed transmission-edge evidence requirements and weakest-link claim progression.

## 1.4 Objectives
1. Define typed evidence requirements for event verification, Nigerian exposure, domestic transmission, bounded scenarios and quantitative forecast eligibility.
2. Implement deterministic weakest-link progression that prevents mandatory transitions from being skipped.
3. Implement counterevidence, contradiction and staleness handling that can downgrade and recompute dependent claims.
4. Construct reproducible historical replay cases and negative/stress controls.
5. Compare the evidence-constrained method with simpler baselines, including an LLM/RAG explanation baseline, using predeclared claim-quality and abstention measures.
6. Evaluate reviewer agreement and unsupported downstream claims using independent blinded judgment.

Objectives 5–6 remain **evaluation objectives**, not completed findings.

## 1.5 Research Questions
RQ1. Can typed transmission-edge requirements reliably stop downstream claim progression when mandatory Nigerian exposure or transmission evidence is insufficient?

RQ2. Does counterevidence, contradiction or staleness cause the expected downgrade/recomputation of dependent claims?

RQ3. Under equivalent frozen evidence, does B3 ETEC produce a lower Unsupported Downstream Claim Rate (UDCR) than B2 LLM/RAG explanation?

RQ4. Does structural abstention reduce false local warnings on negative-control pathways without eliminating useful supported scenarios?

RQ5. Can independent reviewers reproducibly judge the support state of the resulting downstream claims?

RQ3–RQ5 are not yet answered empirically.

## 1.6 Research Hypotheses
Do not invent significance tests before the final sample/evaluation design justifies them.

Mechanism hypothesis:
- H1: Mandatory typed-edge insufficiency will cap progression at the weakest required transition in the deterministic implementation.

Comparative hypothesis:
- H2: B3 will produce a lower UDCR than B2 under the frozen historical comparison.

Negative-control hypothesis:
- H3: B3 will not release a material local downstream warning where the required Nigerian exposure edge is insufficient.

H2 remains untested.

## 1.7 Scope
- Nigeria as initial target country.
- Bounded geopolitical/trade disruption families.
- Product/sector/fiscal pathways where evidence can be represented explicitly.
- Historical replay before live monitoring.
- Directional scenarios separated from numerical estimates.
- No automated trading/investment action.
- No universal causal or price-prediction claim.

## 1.8 Significance
Frame significance around research/engineering value:
- makes evidence gaps explicit;
- distinguishes narrative plausibility from admissible claim strength;
- preserves provenance and historical replay;
- makes abstention a testable output;
- provides a falsifiable mechanism rather than an unrestricted prediction product.

Do not say the system has already improved real-world forecasting accuracy.

## 1.9 Definition of Key Terms
Include:
- ETEC — Economic Transmission Evidence Contract
- LLM — Large Language Model
- RAG — Retrieval-Augmented Generation
- UDCR — Unsupported Downstream Claim Rate
- HS — Harmonized System
- COICOP — Classification of Individual Consumption According to Purpose
- PMS — Premium Motor Spirit
- R1/R2 replay
- structural abstention
- counterevidence
- weakest-link progression

---

# Chapter Two — Literature Review

Chapter Two must be literature-driven, not repository-driven.

## 2.1 Conceptual Review
Cover:
- geopolitical risk and economic transmission;
- trade exposure and supply-chain transmission;
- commodity/energy transmission;
- country-specific vulnerability;
- scenario analysis versus forecasting;
- uncertainty and calibration;
- evidence provenance;
- counterevidence/contradiction;
- abstention/selective prediction;
- LLM/RAG factual grounding and unsupported inference.

## 2.2 Theoretical / Analytical Foundations
Potential foundations to examine and cite rather than merely assert:
- economic transmission-channel reasoning;
- weakest-link/dependency logic;
- evidence/provenance models;
- uncertainty-aware decision support;
- selective prediction/abstention.

Only retain theories that the literature actually supports as relevant to the final model.

## 2.3 Empirical Review
Organize empirical studies by what they actually evaluate:
- geopolitical-risk indices and economic outcomes;
- event/news-to-market/economic forecasting;
- supply-chain/trade exposure systems;
- country-specific shock transmission;
- LLM/RAG economic or risk-analysis systems;
- evidence-grounded/abstaining decision-support systems.

For each study capture:
author/year, context, data, method, target, evaluation, findings, limitations, relevance to P003.

## 2.4 Prior-Art Attack
Document why the following cannot be claimed as novelty by themselves:
- knowledge graphs;
- RAG;
- provenance;
- evidence contracts;
- contradiction handling;
- abstention;
- geopolitical-risk scoring.

## 2.5 Research Gap
The gap must be written cautiously:

> The project investigates whether a domain-specific combination of typed economic transmission-edge sufficiency and weakest-link downstream claim progression can provide a more disciplined evidence boundary for Nigeria-specific geopolitical-economic claims than a narrative explanation baseline.

Do not write “no previous system has ever done this” unless the literature review can actually support that global claim.

## 2.6 Conceptual Framework
Present:

```text
Geopolitical Event
       ↓
Event Verification
       ↓
Nigeria Exposure
       ↓
Domestic Transmission
       ↓
Bounded Local Scenario
       ↓
Model Eligibility
       ↓
Calibrated Forecast
```

with counterevidence/staleness/contradiction feeding back into edge states and recomputation.

---

# Chapter Three — Methodology / System Design

Chapter Three can now be drafted substantially because the mechanism and experiment contract are frozen.

## 3.1 Research Design
Describe a design-and-evaluation study combining:
- deterministic software verification;
- historical replay;
- comparative baseline evaluation;
- blinded independent claim review.

Do not describe pending human review as already performed.

## 3.2 System Architecture
Document:
- evidence objects;
- typed transitions T1–T6;
- edge states;
- progression evaluator;
- recomputation service;
- audit trace;
- replay persistence;
- baseline runner;
- comparative evidence packets;
- B2 run records;
- review/blinding pipeline.

## 3.3 Transition Contracts
Give T1–T6 in full with admissibility/failure behavior.

## 3.4 Data Sources and Selection
Document the planned/used source families and source hierarchy. For each historical case distinguish actual evidence used from general planned sources.

## 3.5 Historical Case Selection
Use the frozen Registry v1:
- Candidate A;
- NC-01;
- Candidate B;
- Candidate C;
- Candidate D as prospective extension.

Explain anti-selection rules.

## 3.6 Baselines
Define B0–B4 and why each exists.

## 3.7 Falsification Tests
Document F1–F8 as predeclared attacks, not merely ordinary unit tests.

## 3.8 Evaluation Metrics
Define:
- UDCR;
- structural-abstention quality;
- false local-warning behavior;
- provenance completeness;
- counterevidence sensitivity;
- contradiction correctness;
- reviewer agreement;
- pathway coverage;
- magnitude error only where T5/T6 eligibility exists.

## 3.9 Reviewer Protocol
Describe:
raw response → atomic claims → blinding → reviewer package → independent labels → locked judgments → unblinding → metrics.

## 3.10 Reproducibility
Describe information cutoffs, packet hashes, replay hashes, exact prompts, provider/model metadata and immutable raw responses.

## 3.11 Security / Integrity
Cover prompt injection, manipulated evidence, duplicate sources, stale revisions, mapping tampering, credential handling and unauthorized state mutation.

## 3.12 Ethical / Decision Boundary
No automated trading; no unsupported consequential economic recommendation; explicit uncertainty and abstention; reviewer privacy/pseudonymous identifiers where appropriate.

---

# Chapter Four — Implementation, Results and Evaluation

This chapter must be split into **completed** and **pending** evidence.

## 4.1 Implementation Environment
Document Python-first architecture, repository branch, domain modules and test workflow.

## 4.2 Deterministic Implementation Results
May report verified software behavior:
- T1–T6 representation;
- weakest-link stopping;
- recomputation;
- F1–F8 contracts;
- persistence/hash integrity;
- packet/manifests;
- reviewer-integrity gates.

Current verified suite at this blueprint freeze: **88 passed, 0 failed**.

## 4.3 Historical Replay Preparation Results
Report only the bounded case states:
- A reaches T4, T5/T6 withheld;
- NC-01 stops at T2 for material direct-exposure claim;
- B stops at insufficient T2;
- C stops at conditional/non-passing T3;
- D reaches T4 as prospective extension, T5/T6 withheld.

## 4.4 B0–B3 Infrastructure
Explain that existing B2 placeholder behavior is infrastructure only and cannot be used as empirical B2 evidence.

## 4.5 External Comparative Experiment
**PENDING.**

Do not populate a results table with fabricated B2 outputs.

When available, this section will contain:
- six first-wave B2 runs;
- atomic claim counts;
- blinded reviewer labels;
- reviewer agreement;
- B2/B3 UDCR;
- abstention/coverage;
- negative-control behavior.

## 4.6 Interpretation
Until 4.5 is complete, restrict conclusions to engineering/reproducibility behavior and historical-case admissibility states.

---

# Chapter Five — Summary, Conclusion and Recommendations

A final Chapter Five must wait for the comparative evidence.

A provisional structure may be prepared:

## 5.1 Summary
Summarize problem, mechanism, implementation and completed evaluation.

## 5.2 Findings
Separate:
- software findings;
- historical replay findings;
- comparative empirical findings.

The third category is currently pending.

## 5.3 Conclusion
Do not conclude B3 superiority until H2/RQ3 is actually evaluated.

Current provisional conclusion:
the research-critical mechanism and evaluation infrastructure are sufficiently implemented and frozen to permit a controlled empirical test.

## 5.4 Limitations
Expected limitations include:
- small bounded historical case set;
- R2 reconstruction/vintage limitations;
- Nigeria-only scope;
- source/concordance quality;
- external model-provider reproducibility;
- human-review subjectivity;
- no T5/T6 numerical calibration in admitted cases.

## 5.5 Recommendations / Future Work
Possible future work only after results:
- broader prospective case registry;
- stronger historical-vintage recovery;
- additional independent reviewers;
- cross-country replication;
- quantitative models where T5/T6 eligibility is defensible;
- live monitoring after historical evaluation.

---

# Appendices

Recommended appendices:
- transition contract table;
- evidence schema;
- F1–F8 matrix;
- frozen case registry;
- B2 manifests;
- prompt template;
- reviewer label definitions;
- sample blinded reviewer package;
- test/CI evidence;
- relevant architecture diagrams;
- decision lineage DR-010;
- prohibited-claims/current-boundary statement.

---

# Writing freeze map

## Safe to draft now
- most of Chapter One, subject to literature citations;
- Chapter Two structure, but substantive content requires rigorous cited literature;
- most of Chapter Three;
- Chapter Four implementation and deterministic results;
- historical case-state reporting;
- limitations already established by design.

## Must remain provisional/pending
- claims that B3 outperforms B2;
- empirical UDCR result;
- inter-rater agreement result;
- completed human-validation methodology wording;
- final answer to RQ3–RQ5;
- final H2 conclusion;
- final Chapter Five findings/conclusion.

## Required next academic work
The next documentation stage should be **source-grounded Chapter One and Chapter Two literature work**, followed by conversion of the frozen system/experiment specification into formal Chapter Three prose. Do not write a final Chapter Four/Five around results that do not yet exist.
