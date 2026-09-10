# P005 — Automated Log Analysis & Root-Cause Assistance Tool

## Pass 001 — Foundations, Historical Lineage, AIOps Landscape, and Feasibility

**Canonical portfolio ID:** P005  
**Legacy directory:** `projects/project-014-log-root-cause/`  
**Track:** GENERAL / PRODUCT SYSTEM  
**Research state:** MORE RESEARCH — CROWDED DOMAIN; EVIDENCE-BOUND DIAGNOSIS DIRECTION SURVIVES  
**Implementation:** NOT AUTHORIZED

## 1. Original problem
Parse heterogeneous logs, identify anomalous events, correlate evidence across time/components, and assist an operator in finding plausible root causes faster.

The problem is real, but nearly every generic component is established prior art. A defensible project cannot be described merely as an AI log analyzer, anomaly detector, root-cause analyzer, or LLM incident assistant.

## 2. Historical and technical lineage

### 2.1 Log parsing is mature
Log parsing converts semi/unstructured messages into templates/events. Drain (ICWS 2017) is a representative online parser using a fixed-depth parse tree. LogPAI's benchmark/toolkit includes Drain, IPLoM, Spell, Logram, NuLog, Brain, DivLog and other parsers and provides public benchmark datasets/results. Drain3 demonstrates a production-oriented evolution.

**Novelty killed:** automatic log parsing, template extraction, streaming parsing, parser benchmarking, and using an LLM merely to parse logs.

### 2.2 Anomaly detection is mature
Statistical, sequence-based, deep-learning, self-supervised and more recent LLM/RAG-assisted log anomaly methods are extensively researched. Current AIOps literature treats anomaly detection as a core established task rather than a new application.

**Novelty killed:** detect unusual logs with ML/AI; assign anomaly scores; learn normal sequences; use an LLM to classify anomalous log messages.

### 2.3 Root-cause analysis is mature
Failure localization and RCA in microservice/cloud systems already use logs, metrics, traces, topology/dependency graphs, correlations, causal inference and multimodal observability. Surveys document a substantial pre-existing body of work.

**Novelty killed:** correlate logs to find root cause; combine logs and metrics; graph-based RCA; rank likely failing services; use AI for root-cause localization.

### 2.4 Observability is multi-signal
Modern observability does not treat logs as sufficient context. OpenTelemetry explicitly supports correlation among logs, traces and metrics, including trace/span context and resource identity. Logs without execution context can be insufficient for distributed execution diagnosis.

Therefore P005 must not assume a log-only explanation can establish causality in a distributed system.

### 2.5 LLM-assisted AIOps is already active prior art
Recent AIOps surveys explicitly cover LLMs/OpsLLMs for failure perception, anomaly detection, RCA, incident reports and assisted remediation. RAG-enhanced diagnosis and natural-language operational assistance are active research areas.

**Novelty killed:** summarize logs with an LLM; ask questions about logs; generate a root-cause explanation; RAG over runbooks/incidents; generate remediation suggestions/runbooks.

## 3. Critical epistemic distinction
P005 must preserve four different states:

1. **OBSERVED EVIDENCE** — directly present in telemetry/artifacts.
2. **CORRELATION** — signals co-vary or occur near each other but causation is unproved.
3. **DIAGNOSTIC HYPOTHESIS** — plausible explanation derived from evidence and system knowledge.
4. **VERIFIED CAUSE** — confirmed by independent evidence, intervention, reproduction, known injected fault, fix-and-recovery evidence, or authoritative incident ground truth.

A fluent explanation cannot promote a hypothesis to VERIFIED CAUSE.

## 4. Failure mode motivating the surviving direction
A generic LLM can receive:

- `database timeout`
- elevated API latency
- pod restart
- memory pressure

and confidently narrate that memory pressure caused the database timeout and API failure. Yet chronology, topology, dependency direction, a deployment event, an upstream network fault, or a shared infrastructure problem may contradict that chain.

The system must therefore answer not only **"What is the likely cause?"** but:

> **"What evidence supports this candidate cause, what evidence contradicts it, what remains unobserved, and what minimum next observation/test would discriminate among competing hypotheses?"**

## 5. Surviving hypotheses

### H1 — Evidence-Bounded Diagnostic Hypothesis Ledger
Represent each root-cause candidate with explicit supporting evidence, contradictory evidence, assumptions, temporal/topological applicability, provenance and verification state.

Novelty: UNKNOWN. Evidence/provenance/explainable RCA are established; direct combination must be attacked.

### H2 — Competing-Hypothesis Diagnosis
Do not force one root cause when telemetry supports multiple explanations. Maintain ranked or partially ordered hypotheses and expose what evidence would distinguish them.

Novelty: UNKNOWN. Differential diagnosis and hypothesis-based debugging have prior art and require direct review.

### H3 — Minimum Discriminating Evidence Recommendation
Rather than immediately generating a fix, identify the smallest safe next observation/test that could materially separate competing hypotheses—for example inspect a trace segment, compare a dependency metric, check deployment chronology, query a particular log source, or reproduce a bounded condition.

This is currently the most interesting research direction, but novelty is UNVERIFIED.

### H4 — Root-Cause Claim Strength Contract
Cap claim strength by evidence state. Example output classes:

`ANOMALY OBSERVED -> CORRELATED SIGNAL -> CANDIDATE CAUSE -> STRONGLY SUPPORTED CAUSE -> VERIFIED CAUSE`

No model confidence score may independently promote the state.

Novelty: UNKNOWN; likely a supporting mechanism rather than standalone contribution.

## 6. Candidate architecture direction
A future bounded system may use:

`telemetry ingestion -> normalization/parsing -> incident window -> evidence graph -> candidate hypotheses -> contradiction search -> discriminating-evidence planner -> human/controlled verification -> disposition`

The LLM, if used, is an assistant for extraction, explanation and hypothesis generation. It is not the authority that determines causal truth.

## 7. Baselines to preserve for eventual evaluation
- **B0:** keyword/rule search and manual inspection.
- **B1:** parser + anomaly detector.
- **B2:** anomaly + correlation/RCA ranking.
- **B3:** LLM/RAG incident explanation from available telemetry.
- **B4:** evidence-bounded competing-hypothesis system with discriminating-evidence recommendations.

B4 must demonstrate measurable diagnostic benefit over B2/B3, not merely longer explanations.

## 8. Evaluation candidates
Potential metrics include:
- Top-1/Top-k root-cause localization accuracy where ground truth exists;
- false causal-claim rate;
- unsupported claim rate;
- contradiction-detection rate;
- calibration/claim-state correctness;
- time or number of observations required to reach verified cause;
- discriminating-test usefulness;
- diagnostic coverage vs abstention;
- provenance completeness;
- operator agreement/usefulness;
- robustness to irrelevant/noisy logs;
- robustness when the true cause is absent from available telemetry.

## 9. Data feasibility
Public log and AIOps datasets exist, including LogHub/LogPAI-style corpora and multi-source datasets containing logs, metrics and traces. This makes a bounded prototype feasible without proprietary production telemetry.

However, log parsing/anomaly datasets alone are insufficient for the strongest hypothesis because many do not contain reliable causal ground truth or the interventions needed to verify competing diagnoses. Pass 002 must investigate datasets with injected/known faults, topology and multimodal telemetry.

## 10. Security and safety gate
Operational telemetry can contain credentials, tokens, personal data, internal hostnames, paths, database details and proprietary code/context. Future requirements must include:
- secret/PII detection and redaction before external model calls;
- strict tenant/workspace isolation;
- prompt-injection treatment for log/runbook/retrieved content;
- bounded file/input sizes and parser resource limits;
- authorization on telemetry sources and remediation tools;
- immutable provenance for evidence used in a diagnosis;
- no autonomous destructive remediation in the first system;
- explicit approval before any action that changes infrastructure;
- safe handling of malicious log content and untrusted structured fields.

## 11. Claims killed in Pass 001
Do not use any of the following as novelty claims:
- AI-powered log analyzer;
- automatic log parser;
- ML log anomaly detector;
- logs + metrics + traces dashboard;
- event correlation;
- graph-based root-cause localization;
- AI/LLM root-cause explanation;
- RAG over historical incidents/runbooks;
- AI-generated remediation/runbook;
- explainable RCA in generic form.

## 12. Kill/reframe criteria
P005 should be parked/reframed if direct prior art already provides substantially all of:
1. explicit competing causal hypotheses;
2. support and contradiction provenance per hypothesis;
3. causal claim-strength states separated from model confidence;
4. automatic identification of missing evidence;
5. recommendation of minimum discriminating observations/tests;
6. promotion to verified cause only through independent confirmation;
7. measurable reduction in unsupported/incorrect causal conclusions versus standard RCA/LLM baselines.

It should also be parked if public datasets cannot evaluate these mechanisms credibly without manufacturing favorable ground truth.

## 13. Pass 001 decision
**MORE RESEARCH — CROWDED DOMAIN; EVIDENCE-BOUND DIAGNOSIS DIRECTION SURVIVES.**

The original engineering problem is feasible but not novel. The strongest surviving direction is not automated root-cause prediction; it is an evidence-bounded diagnostic workflow that maintains competing hypotheses and seeks the next discriminating evidence before escalating causal claims.

## 14. Required Pass 002
**Direct Prior-Art Attack on Evidence-Bounded / Competing-Hypothesis RCA.**

Research must explicitly inspect:
- hypothesis-driven debugging and differential diagnosis;
- causal graphs and counterfactual RCA;
- fault localization with interventions;
- active diagnosis / active testing / information-gain fault isolation;
- observability vendors' RCA evidence and next-step recommendations;
- LLM agents that call diagnostic tools;
- incident investigation copilots;
- known-fault and multimodal AIOps datasets;
- whether minimum discriminating evidence is already standard prior art.

No implementation until this attack is complete.