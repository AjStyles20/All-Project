# P005 — Automated Log Analysis & Root-Cause Assistance Tool
## Pass 001 — Foundations, Lineage, AIOps Landscape, and Feasibility

> Canonical portfolio ID: P005. Historical directory retains old P014 path for provenance.

## Decision
**MORE RESEARCH — LEGITIMATE PROBLEM, EXTREMELY CROWDED SOLUTION SPACE.**

No implementation is authorized by this pass.

## Original working problem
Parse heterogeneous logs, identify anomalous events, correlate evidence across time/components, and assist operators in identifying plausible root causes faster.

## Foundational lineage
The component ideas are mature prior art:
- log parsing/template mining converts unstructured messages into structured event types; Drain is established online parsing prior art;
- anomaly detection over logs is established, including statistical, sequence, Transformer and newer LLM approaches;
- event correlation and dependency/topology analysis are core AIOps/observability problems;
- root-cause localization in microservices already combines logs, metrics, traces, service topology, graphs and causal reasoning;
- commercial observability platforms already provide automated correlation, anomaly detection and RCA assistance;
- LLM-assisted incident diagnosis/RCA is now active research and product territory.

Therefore none of the following is a defensible novelty claim by itself: automated log parsing; anomaly detection; grouping similar errors; timeline correlation; logs+metrics+traces correlation; dependency graph RCA; causal graph RCA; LLM summaries; LLM-generated root-cause hypotheses; explainable RCA; or an 'AI DevOps assistant'.

## Current observability baseline
OpenTelemetry provides a common telemetry/log model with timestamp, observed timestamp, trace/span context, severity, body, resources, attributes and event names. Its semantic conventions standardize names and meaning across logs, traces, metrics, profiles and resources. A modern project should exploit such structured context rather than pretend all operational evidence is arbitrary text.

This materially raises the baseline: P005 should preserve identifiers, timestamps, service/resource context and trace linkage where available instead of flattening everything into an LLM prompt.

## Academic prior-art threats
### Multi-modal RCA
Nezha (ESEC/FSE 2023) already performs interpretable fine-grained RCA from metrics, traces and logs by transforming heterogeneous observability signals into homogeneous events and mining event graphs; reported average top-1 accuracy is 89.77% on its evaluated microservice applications.

Other recent work includes HeMiRCA and MRCA, which explicitly use heterogeneous/multi-modal observability sources for service/metric-level localization. Chain-of-Event (2024) learns weighted event causal graphs for interpretable RCA. This strongly attacks any novelty claim based on 'correlating logs with other telemetry' or 'building an event graph'.

### Hypothesis and verification
SpecRCA (ICSE 2026) explicitly uses a **hypothesize-then-verify** paradigm: draft candidate root causes, then verify them in parallel. This is a direct threat to a naive contribution framed as 'the LLM proposes a cause and then checks evidence'.

### Contemporary LLM/log systems
Recent 2026 work combines Drain-style parsing, anomaly detection and LLM analysis in real operational log pipelines. Other current research performs topology-aware log-metric correlation before an LLM produces RCA summaries. Thus adding an LLM after parsing/correlation is not enough.

## Core epistemic problem
The most important surviving problem is not producing a plausible explanation. It is preventing the system from presenting a plausible explanation as a verified root cause.

Operational evidence must be typed at minimum as:
1. **OBSERVED** — directly present in telemetry/configuration/change/incident evidence.
2. **CORRELATED** — statistically/temporally/topologically associated but not established causal evidence.
3. **HYPOTHESIZED** — proposed explanation requiring tests.
4. **SUPPORTED** — hypothesis has discriminating supporting evidence but remains revisable.
5. **CONTRADICTED** — evidence conflicts with the hypothesis.
6. **VERIFIED** — cause established under an explicit verification rule or known incident ground truth.
7. **INSUFFICIENT EVIDENCE** — system must abstain from stronger attribution.

A fluent LLM narrative cannot promote a hypothesis between these states.

## Candidate surviving hypotheses
### H1 — Evidence-Bounded Diagnostic Claim State Machine
Every RCA statement is constrained by its evidence state. Candidate causes cannot become 'root cause' merely because an anomaly score, correlation, causal model or LLM ranks them highly.

**Novelty status:** UNKNOWN. General evidence/uncertainty governance exists broadly and must be attacked directly.

### H2 — Discriminating Verification Planner
Instead of merely returning a ranked cause list, the system asks: **what minimum next observation/test would most effectively distinguish the leading hypotheses?** Examples may include checking a deployment/configuration change, querying a trace path, comparing a healthy period, inspecting resource saturation, or checking whether the suspected dependency failed before the symptom.

**Novelty status:** UNKNOWN/HIGH THREAT. SpecRCA already uses hypothesize-then-verify; troubleshooting/diagnostic systems have long used test selection. The exact observability-bounded formulation needs direct prior-art review.

### H3 — Counterevidence-First RCA
The system must actively retrieve evidence that could falsify a leading hypothesis and demote it when contradictory evidence appears. It should not merely collect confirming logs.

**Novelty status:** UNKNOWN. Potentially valuable reliability mechanism but not assumed novel.

### H4 — Evidence Sufficiency / Abstention Gate
When available telemetry cannot distinguish multiple plausible causes, output the ambiguity and required missing evidence instead of selecting a winner.

**Novelty status:** UNKNOWN. Abstention itself is established ML/AI practice; contribution would require domain-specific mechanism and measurable RCA benefit.

## Candidate architecture direction
A provisional pipeline worth investigating is:

`telemetry ingestion -> normalization/provenance -> event/template extraction -> incident window -> anomaly evidence -> topology/trace/time correlation -> candidate hypotheses -> counterevidence retrieval -> discriminating verification plan -> evidence-state update -> operator-facing diagnostic report`

LLMs, if used, may help parse unusual messages, explain evidence, generate candidate hypotheses, propose bounded checks, or summarize findings. They must not self-certify a root cause.

## Evaluation requirements
A future benchmark must use incidents with known/defensible ground truth and compare against meaningful baselines. Candidate measures include:
- top-k root-cause localization accuracy;
- false root-cause assertion rate;
- abstention/selective coverage;
- time/steps to verified diagnosis;
- quality of next diagnostic test selection;
- counterevidence demotion correctness;
- evidence/provenance completeness;
- calibration between claim state and actual correctness;
- robustness to noisy/irrelevant logs;
- robustness to missing modalities;
- cost/latency if an external LLM is used.

## Feasibility
A bounded student prototype is feasible without enterprise-scale infrastructure. It can use public microservice/incident datasets or a deliberately instrumented small microservice testbed, OpenTelemetry-compatible structured signals where possible, Python for ingestion/analysis, conventional parsers/statistics/graphs, and an optional provider-isolated LLM layer.

The project should not attempt to reproduce a full Datadog/Dynatrace/Splunk/New Relic observability platform. A research prototype needs a narrow diagnostic mechanism and controlled incidents.

## Security and privacy gate
Logs routinely contain sensitive identifiers, tokens, URLs, stack traces, infrastructure names and sometimes secrets. Requirements before any implementation include secret/PII redaction, access control, workspace/tenant isolation, prompt-injection treatment for untrusted log text, bounded query/tool authorization, safe file ingestion, resource limits, retention rules, auditability, and preventing model-generated commands from becoming automatic production actions.

## Pass 001 novelty kills
Treat as prior art, not contribution:
- automated log parsing;
- Drain/template mining;
- anomaly detection;
- timeline/event correlation;
- logs + metrics + traces;
- topology-aware correlation;
- event/causal graphs;
- root-cause ranking;
- explainable RCA;
- LLM incident summaries;
- LLM root-cause hypotheses;
- generic hypothesize-then-verify;
- generic AI/AIOps assistant.

## Kill/reframe criteria
P005 should be parked/reframed if direct prior art already provides the same evidence-state + falsification + diagnostic-test-selection mechanism with comparable observability inputs and evaluation; if public/constructible ground truth is too weak for defensible evaluation; if the project reduces to prompt engineering around existing observability data; if the proposed method cannot beat simpler correlation/ranking baselines; or if verification requires production access unavailable to the project.

## Next pass
**Pass 002 — Direct Prior-Art Attack on Evidence-Bounded RCA, Counterevidence, and Diagnostic Test Selection.**

Research targets: automated troubleshooting/test selection, causal diagnosis, fault localization, counterfactual/falsification-based RCA, active diagnosis, LLM RCA agents, incident-management copilots, observability vendors, and open-source RCA systems. The pass should try to kill H1-H4 individually and determine whether a narrower measurable mechanism survives.
