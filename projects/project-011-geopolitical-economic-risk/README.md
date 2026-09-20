# P003 — Geopolitical Risk to Economic Impact Forecasting & Warning System

> Historical repository directory: `project-011-geopolitical-economic-risk` (legacy P011). Canonical portfolio ID: **P003**.

## Current status

**IMPLEMENTATION ACTIVE / M9 READY-BLOCKED ON EXTERNAL EVIDENCE**

P003 has passed the portfolio implementation gate under DR-010 and has progressed through the deterministic research-critical implementation, historical replay preparation, frozen comparative evidence packets, B2 experiment preparation, and independent-review integrity infrastructure.

The latest verified automated test state before this README consolidation is **88 passed, 0 failed**. Passing tests establish software behavior only; they do not establish the scientific contribution.

## Problem

Geopolitical events can generate plausible narratives about downstream Nigerian economic effects even when one or more transmission links are weak, missing, stale, contested or contradicted. The project therefore does **not** attempt to build a universal geopolitical price predictor.

It asks whether explicit, typed evidence requirements can constrain how far a downstream economic claim is allowed to progress.

## Surviving contribution boundary

The research contribution under test is:

**typed transmission-edge evidence sufficiency + weakest-link downstream claim progression.**

The implementation architecture is called the **Economic Transmission Evidence Contract (ETEC)**.

Generic Retrieval-Augmented Generation (RAG), provenance, evidence contracts, knowledge graphs, contradiction handling, abstention and geopolitical-risk scoring are not claimed as novel by themselves.

## Core rule

> The maximum strength of an economic claim is capped by the weakest required evidentiary link.

The claim ladder is:

```text
EVENT
  ↓ T1
EVENT VERIFIED
  ↓ T2
EXPOSURE MEASURED
  ↓ T3
TRANSMISSION SUPPORTED
  ↓ T4
SCENARIO SUPPORTED
  ↓ T5
MODEL ESTIMATE ELIGIBLE
  ↓ T6
CALIBRATED FORECAST
```

Required edge states include `VERIFIED`, `SUPPORTED`, `CONDITIONAL`, `CONTESTED`, `STALE`, `INSUFFICIENT`, and `CONTRADICTED`.

Counterevidence is state-changing evidence. It can downgrade an edge and force dependent claims to be recomputed.

## Baselines

- **B0 — News/GPR:** geopolitical/news-intensity signal without a Nigeria-specific evidence chain.
- **B1 — Event + Exposure:** verified event plus direct Nigeria exposure, without downstream evidence contracts.
- **B2 — LLM/RAG Explanation:** a language-model explanation generated from equivalent frozen evidence.
- **B3 — ETEC:** typed transition contracts, provenance, counterevidence and structural abstention.
- **B4 — Optional quantitative comparator:** only when an independently validated econometric/model baseline is actually applicable.

The central historical comparison is B2 versus B3, but no empirical superiority result currently exists because the real B2 execution and independent review stages remain external dependencies.

## Implementation checkpoints

Completed software/research preparation includes:

- M0 — implementation-entry contract;
- M1 — immutable transition/evidence domain model;
- M2 — weakest-link progression evaluator;
- M3 — F1 missing-link vertical slice and audit trace;
- M4 — counterevidence, staleness and contradiction recomputation;
- M5 — deterministic F1–F8 falsification contracts;
- M6 — canonical replay persistence and SHA-256 integrity;
- M7 — bounded B0–B3 comparative infrastructure;
- M8 — historical replay preparation and frozen case-set registry;
- M9 — software-side reviewer/evaluation protocol ready, but external evidence incomplete.

M10 frozen historical evaluation has not been completed.

## Frozen historical case set

### Candidate A — Russia/Ukraine wheat disruption
R2 historical reconstruction. Reaches T4 with a bounded directional wheat-flour/bread/cereal cost-pressure scenario. T5/T6 are withheld. Later outcomes may be directionally consistent but do not establish exclusive causality.

### NC-01 — Russian urea direct-exposure negative control
R2 negative control for the narrow question of material direct Russian urea dependence. The reconstructed direct Russian urea exposure is non-zero but negligible; B3 stops at T2 rather than converting a dramatic global event into a material local warning.

### Candidate B — Red Sea/Suez disruption
Stress case. T1 is supported but Nigeria-specific route/product exposure remains insufficient, so progression stops at T2. It is not an admitted outcome-comparison case.

### Candidate C — October 2023 FX restriction removal
Stress case. T2 is supported but T3 remains `CONDITIONAL` and therefore non-passing. T4+ are withheld.

### Candidate D — 2022 refined-fuel/PMS subsidy-fiscal channel
Mechanism-diverse prospective replication/extension. R2 reconstruction reaches T4 with a bounded fiscal-burden scenario. Later evidence is directionally consistent, but exclusive war causality and numerical forecasting remain prohibited. Candidate D is separate from the original first-wave B2 experiment.

## First-wave B2 experiment

The six predeclared runs remain **NOT RUN**:

```text
B2-A-001
B2-A-002
B2-A-003
B2-NC01-001
B2-NC01-002
B2-NC01-003
```

The experiment manifest, frozen packet hashes, prompt serialization, execution gate, immutable run record, atomic-claim provenance, blinding, reviewer-package hashing, reviewer judgment locking and comparative-analysis authorization gate are implemented.

A connected Hugging Face Jobs route was smoke-tested without consuming an experimental run. Execution was rejected with HTTP 402 Payment Required. No other currently exposed connector qualified as a controlled text-generation endpoint under the frozen provenance requirements.

## Independent review

After real B2 outputs exist:

```text
raw B2 response
      ↓
atomic claim extraction
      ↓
blind claim identity
      ↓
frozen reviewer package
      ↓
independent reviewer judgments
      ↓
pre-unblinding SHA-256 lock
      ↓
analysis authorization
      ↓
unblind
      ↓
UDCR / agreement / abstention analysis
```

**UDCR** means **Unsupported Downstream Claim Rate**.

At least two independent reviewers are preferred under the frozen protocol. No human judgments have yet been collected, so M9 is not scientifically complete.

## Claims currently prohibited

Do not claim that:
- B3 empirically outperforms B2;
- P003 has a lower empirical UDCR than the language-model baseline;
- inter-rater reliability is acceptable;
- the system has validated forecasting accuracy;
- it establishes geopolitical-economic causality;
- it produces universally valid Nigerian or global forecasts;
- M9 or M10 is complete.

## Technology and scope

The implementation is Python-first and deliberately lightweight. Domain rules are deterministic and server-authoritative before any optional language-model assistance. The bounded prototype is Nigeria-focused and prioritizes historical replay over live monitoring.

The project excludes automated trading/investment actions, universal causal prediction and unsupported numerical forecasts.

## Key specifications

Start with:
- `specification/IMPLEMENTATION_ENTRY_CONTRACT.md`
- `specification/FORMAL_RESEARCH_EXPERIMENT_SPECIFICATION.md`
- `specification/FALSIFICATION_CONTRACT_MATRIX.md`
- `specification/M8_HISTORICAL_CASE_SET_REGISTRY_V1.md`
- `specification/B2_EXPERIMENT_MANIFEST_V1.md`
- `specification/M9_EXTERNAL_EVIDENCE_READINESS_AUDIT_V1.md`
- `specification/REAL_B2_EXECUTION_HANDOFF_V1.md`
- `specification/EXTERNAL_MODEL_EXECUTION_ROUTE_AUDIT_V1.md`

## Next legitimate transition

Do not add evaluation infrastructure merely for completeness.

The next experimental transition is to obtain access to a qualifying controlled model-execution environment, run the six frozen first-wave B2 generations without result-aware tuning, preserve immutable raw records, and then obtain independent blinded human judgments.

Until that happens, P003 is **externally evidence-blocked, not engineering-blocked**, at M9.
