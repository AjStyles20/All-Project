# P014 / P005 — Passes 002–003: Prior-Art Attack and Final Research Gate

Date: 2026-09-10

## Final decision

**KILL AS A RESEARCH-NOVELTY CANDIDATE.**

The project remains potentially valuable as an engineering/portfolio implementation, but the investigated contribution is too heavily occupied to defend as the primary novel FYP research contribution.

## Pass 002 — Evidence-bounded interactive diagnosis

The surviving Pass 001 direction was tested against current work on agentic root-cause analysis (RCA), competing hypotheses, dynamic evidence collection, tool use and hypothesis validation.

### Findings

1. Tool-using LLM RCA agents already dynamically collect additional diagnostic information such as logs, metrics, databases and external diagnostic-service results.
2. Multi-agent RCA systems already ground hypotheses in retrieved evidence and validate hypotheses by executing dynamic tests against runtime data.
3. Recent RCA work already explores tree-structured search over multiple root-cause hypotheses, with agents iteratively collecting evidence and directing search toward candidate causes.

### Claims rejected

P014 cannot claim novelty merely from:
- multiple competing RCA hypotheses;
- agentic incident diagnosis;
- dynamic retrieval of diagnostic evidence;
- diagnostic tool invocation;
- runtime hypothesis validation;
- branching diagnostic paths;
- logs/metrics fusion;
- iterative diagnosis updates;
- grounding intended to reduce LLM hallucination.

### Provisional reframe

A narrower H6 was retained temporarily:

> Can an automated incident-diagnosis system determine when available evidence is insufficient to justify a causal conclusion, abstain from declaring a root cause, and identify missing evidence required to resolve competing explanations?

This reframed P014 from maximizing RCA accuracy toward evidence sufficiency, epistemic stopping and causal-claim governance.

## Pass 003 — Abstention, evidence sufficiency and unresolved diagnosis

H6 was then attacked directly against prior work and current systems involving explicit abstention, evidence-grounded RCA and insufficient-evidence handling.

### Findings

The remaining design space is also occupied by work that treats ambiguous or insufficient evidence as a reason to abstain from causal attribution. Evidence-grounded agentic RCA also already performs iterative hypothesis generation, testing, rejection and evidence collection. Current RCA tooling additionally demonstrates confidence/abstention concepts and withholding attribution when evidence is insufficient.

Therefore, the proposed combination:

`competing hypotheses -> evidence acquisition -> discrimination/validation -> evidence-sufficiency decision -> verified cause OR unresolved/abstain`

is not sufficiently defensible as the project's novel research contribution.

## Why the project is being killed rather than narrowed again

Further narrowing is technically possible (for example cost-sensitive abstention, telemetry-coverage-aware identifiability, formal evidence thresholds, counterfactual evidence acquisition, calibrated uncertainty, multi-fault abstention or causal-claim certification). However, repeatedly adding constraints after each prior-art collision risks manufacturing novelty rather than identifying a natural research gap.

P014 has now failed three adversarial gates:

- **Pass 001:** conventional AIOps/log RCA is extremely crowded.
- **Pass 002:** tool-using agents, competing hypotheses and dynamic hypothesis validation are already established.
- **Pass 003:** explicit abstention/evidence-sufficiency ideas are also occupied.

## Final classification

- Research novelty: **KILL**
- Engineering value: **HIGH / potentially impressive portfolio system**
- FYP shortlist status: **REMOVE FROM RESEARCH-NOVELTY SHORTLIST**
- Implementation status: **PARK unless independently desired as a software project**

## Potential engineering architecture (non-novelty claim)

Incident ingestion (logs / metrics / traces)
-> evidence extraction
-> hypothesis generation
-> diagnostic tool execution
-> evidence validation
-> VERIFIED CAUSE or UNRESOLVED + missing evidence.

## Research references examined in Pass 002

- Roy et al. (2024), *Exploring LLM-Based Agents for Root Cause Analysis*, FSE Companion.
- Fu et al. (2025), *Leveraging multi-agent framework for root cause analysis*, Complex & Intelligent Systems.
- Naakka, Wang & Mantyla (2026), *LATS-RCA: Language Agent Tree Search for Root Cause Analysis in Microservices*.

## Portfolio consequence

P014/P005 is closed at the research gate. Continue the portfolio sequence with the next untouched candidate rather than spending additional novelty-research budget on this project.
