# P005 — Automated Log Analysis & Root-Cause Assistance Tool

## Pass 001 — Foundations, AIOps Lineage and Feasibility

Canonical portfolio ID: **P005**. Legacy directory ID: P014.

## Decision
**MORE RESEARCH — LEGITIMATE PROBLEM, EXTREMELY CROWDED PRIOR ART. NO IMPLEMENTATION.**

## Original problem
Parse heterogeneous logs, identify anomalous events, correlate evidence across time/components, and assist operators in identifying plausible root causes faster.

## Evidence summary

### 1. The problem is established, not speculative
Cloud-native/microservice systems create difficult anomaly detection and root-cause-localization problems because failures propagate through service dependencies and emit heterogeneous telemetry. Surveys already organize mature families of anomaly detection and RCA techniques.

### 2. Log parsing/anomaly detection are mature research areas
LogPAI exposes public datasets and toolkits for log parsing and anomaly detection. Contemporary work includes statistical, deep-learning, Transformer and LLM approaches. Therefore log parsing, anomaly detection, clustering, summarization, and basic failure prediction cannot be claimed as novel merely because AI is used.

### 3. Log-based RCA itself is direct prior art
LogRCA (2024) explicitly targets root-cause identification from distributed-service logs and seeks a minimal set of log lines describing a root cause. It was evaluated on 44.3M production log lines and 80 expert-labelled failures. Thus 'find the root cause from logs' is already a direct research contribution family.

### 4. Multimodal observability + causal/topological RCA is established
Modern AIOps combines logs, metrics, traces, events and topology. Commercial platforms such as Dynatrace automatically correlate events and traverse causal topology to rank root-cause candidates. Splunk AI SRE similarly correlates metrics/logs/traces and provides suspected root causes and remediation guidance. Therefore combining multiple telemetry modalities, dependency graphs, event correlation, and natural-language RCA is not novel by itself.

### 5. LLM-assisted operations is already crowded
A 2026 systematic review of LLM-based log analysis identified 145 papers across logging tasks including parsing, anomaly detection, failure prediction, RCA and summarization. Current research explicitly discusses prompting, retrieval grounding, fine-tuning, agents and verification. Commercial systems already provide AI troubleshooting and generated remediation guidance.

## Claims killed immediately
The following are not defensible standalone novelty claims:
- AI/ML log parser;
- log anomaly detector;
- log clustering/template extraction;
- automated incident correlation;
- log-based root-cause analysis;
- graph/topology-based root-cause localization;
- logs + metrics + traces fusion;
- LLM explanation of incidents;
- RAG over logs/runbooks;
- AI-generated remediation suggestions;
- 'chat with your logs';
- confidence score attached to an LLM diagnosis.

## Critical distinction
A fluent diagnosis is not a verified cause. P005 must distinguish:
1. **OBSERVATION** — directly present telemetry/event evidence;
2. **CORRELATION** — temporal/statistical/topological association;
3. **HYPOTHESIS** — candidate explanation consistent with evidence;
4. **DISCRIMINATING TEST** — observation/query/test that could strengthen or weaken a hypothesis;
5. **VERIFIED CAUSE** — cause supported by an explicit verification result or known incident ground truth;
6. **UNRESOLVED** — evidence is insufficient or competing hypotheses remain.

No language model may promote a hypothesis to VERIFIED CAUSE merely through persuasive reasoning.

## Surviving hypotheses for adversarial testing

### H1 — Evidence-Bounded Diagnostic Hypothesis Set
Instead of returning one confident 'root cause', maintain ranked competing hypotheses, each linked to supporting evidence, contradicting evidence, assumptions and unresolved gaps.

Novelty status: UNKNOWN. Bayesian diagnosis, fault trees, causal graphs, differential diagnosis and AIOps candidate ranking are major threats.

### H2 — Discriminating-Evidence Acquisition
Given competing root-cause hypotheses, identify the smallest/lowest-cost next query, telemetry inspection or safe diagnostic test expected to distinguish among them.

Example:
- H1 database connection exhaustion;
- H2 downstream network failure;
- H3 bad deployment configuration.
Rather than generate a paragraph, the system proposes the next evidence request that most separates H1/H2/H3.

Novelty status: UNKNOWN; active diagnosis, troubleshooting decision trees, information-gain testing and agentic observability are direct threats.

### H3 — Diagnosis Provenance and Claim-State Control
Every diagnostic statement carries source telemetry, time window, service/entity scope, transformation/query provenance and claim state. Contradictory evidence can downgrade a hypothesis; stale evidence cannot silently support a current diagnosis.

Novelty status: likely supporting architecture rather than standalone contribution.

### H4 — Ground-Truth-Aware Diagnostic Abstention
When evidence cannot distinguish plausible hypotheses, explicitly output UNRESOLVED and state what evidence is missing instead of selecting the most fluent explanation.

Novelty status: likely trustworthiness mechanism, not standalone novelty.

## Candidate research direction
**Evidence-Bounded Interactive Root-Cause Investigation**

Candidate flow:

`incident -> observations -> candidate hypotheses -> supporting/contradicting evidence -> unresolved distinctions -> next discriminating evidence/test -> hypothesis update -> verified cause OR unresolved`

This is deliberately different from:

`logs -> LLM -> root-cause paragraph`

The contribution, if any survives, must be in the investigation/control mechanism rather than generic AI analysis.

## Evaluation requirements
Eventually compare against at least:
- B0 keyword/rule-based log triage;
- B1 anomaly + temporal correlation;
- B2 LLM/RAG diagnosis from incident context;
- B3 graph/topology-aware candidate ranking where feasible;
- B4 proposed evidence-bounded interactive investigation.

Metrics should include:
- Top-1 / Top-k root-cause localization;
- unsupported-cause assertion rate;
- time/steps to verified diagnosis;
- evidence precision/relevance;
- ability to preserve competing hypotheses;
- contradiction sensitivity;
- abstention quality;
- diagnostic query/test cost;
- provenance completeness;
- robustness to irrelevant/noisy logs;
- robustness to missing telemetry;
- operator usefulness where human evaluation is used.

## Data feasibility
Potential public evidence families include LogHub/LogPAI and microservice/AIOps benchmark datasets. A decisive later pass must verify which datasets contain actual incident/root-cause ground truth rather than anomaly labels only. Synthetic fault injection may supplement but must never be represented as production ground truth.

## Security requirements
Logs are untrusted input. Event text, stack traces and retrieved runbooks can contain attacker-controlled strings. Requirements include:
- prompt-injection isolation;
- no tool authority from log text;
- secret/token/PII redaction;
- least-privilege telemetry access;
- tenant/source isolation;
- query and resource limits;
- safe parsing of large/malformed logs;
- no automatic remediation without explicit authorization and independent safety controls;
- immutable provenance for evidence used in a diagnosis.

## Kill/reframe criteria
P005 should be parked/killed as a research contribution if direct prior art already provides comparable competing-hypothesis tracking + evidence provenance + discriminating next-test selection + explicit unresolved outcomes; if suitable ground-truth datasets cannot evaluate the mechanism; if B4 reduces to ordinary LLM tool use; or if improvements only occur on artificial faults with privileged ground truth unavailable in realistic operation.

## Next pass
**Pass 002 — Direct Prior-Art Attack on Evidence-Bounded Interactive Diagnosis, Competing Hypotheses and Discriminating Test Selection.**

Research active diagnosis, fault localization, troubleshooting agents, Bayesian/fault-tree diagnosis, information-gain test selection, causal intervention, SRE copilots/agents, observability vendors, and open-source incident agents. Build a mechanism-level prior-art matrix and aggressively attempt to kill H1-H4.
