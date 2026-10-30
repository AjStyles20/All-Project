# P003 — M9 External-Evidence Readiness Audit v1

## Audit conclusion
**M9 STATUS: READY / BLOCKED ON EXTERNAL EVIDENCE.**

The software-side protocol is sufficiently specified to stop adding evaluation infrastructure. M9 is not complete and no scientific B2-vs-B3 result exists.

## Audited chain

### 1. Real B2 execution gate — PASS (software readiness)
A run must be uniquely predeclared and bound to the correct frozen evidence packet SHA-256. The gate returns the frozen system prompt and deterministic packet serialization.

Remaining external dependency: execute the authorized runs using a real model/provider while preserving provider, model, model version, timestamp, temperature, seed/settings, exact prompts and raw response.

### 2. Raw B2 record and atomic-claim provenance — PASS (software readiness)
B2RunRecord preserves execution metadata and raw response. Atomic claims must belong to the run, be nonblank/unique and trace source spans back to preserved raw output.

Residual procedural risk: claim extraction is still a human/research operation and must not introduce support labels during extraction.

### 3. Blinding — PASS (software readiness)
Reviewer-facing blind IDs are deterministic SHA-256-derived identities and do not expose baseline/run identity fields.

Residual operational requirement: the experiment salt and private blind-ID mapping must not be disclosed to reviewers before judgment lock.

### 4. Reviewer package integrity — PASS (software readiness)
Reviewer package is canonically hashed and binds package/protocol/case/evidence packet/blinded claims/instructions. Submissions must cover exactly the frozen claim set with one judgment and non-empty rationale per claim.

External dependency: qualified independent reviewers.

### 5. Pre-unblinding judgment lock — PASS (software readiness)
Each review batch is SHA-256 locked. Mutation after lock invalidates verification.

### 6. Comparative analysis authorization — PASS (software readiness)
Analysis requires two distinct reviewer identities, valid locks and exactly matching blinded claim sets. Raw agreement and Cohen's kappa are calculated only after these integrity checks.

### 7. Scientific-result boundary — PASS
UDCR, abstention quality and B2-vs-B3 conclusions remain unavailable until real model outputs and independent human judgments exist. Deterministic fixtures and CI do not substitute for those observations.

## Explicit loopholes closed
- unplanned B2 run IDs rejected;
- changed packet after manifest freeze rejected;
- baseline-state leakage excluded from B2 serialization;
- raw model output retained;
- claim source provenance checked;
- baseline identity removed from reviewer-facing claim object;
- missing/extra/duplicate reviewer responses rejected;
- reviewer-batch mutation detectable;
- same-reviewer double use rejected by analysis gate;
- mismatched claim coverage rejected;
- Candidate D kept prospective and outside original first wave;
- historical case registry frozen before real comparative outputs.

## Remaining external evidence
### E1 — real B2 first-wave execution
Six predeclared runs:
- B2-A-001
- B2-A-002
- B2-A-003
- B2-NC01-001
- B2-NC01-002
- B2-NC01-003

### E2 — prospective Candidate D B2 execution
Three separately predeclared second-wave runs:
- B2-D-001
- B2-D-002
- B2-D-003

### E3 — independent human review
At least two independent reviewers preferred under the frozen protocol, with reviewer qualification records, complete blinded submissions and pre-unblinding locks.

## Claims prohibited while blocked
Do not claim:
- M9 complete;
- B3 outperforms B2;
- lower empirical Unsupported Downstream Claim Rate (UDCR);
- acceptable inter-rater reliability;
- validated forecasting accuracy;
- causal forecasting ability;
- universal Nigerian/general geopolitical-economic validity.

## Change-control rule
From this audit onward, do not add evaluation infrastructure merely to make the experiment look more complete. A protocol/code change is justified only by:
1. a discovered correctness/integrity defect;
2. an execution requirement exposed by the real external environment; or
3. an explicit versioned methodological amendment made before inspecting affected results.

Any result-aware change must be disclosed and cannot be silently represented as predeclared.

## Next legitimate transition
Acquire E1 through a controlled real model-execution environment. Once raw B2 records exist, extract atomic claims without support scoring, generate the frozen blinded reviewer packages, acquire E3, lock judgments, authorize unblinding, and calculate the predeclared metrics.

Until then, P003 is **externally evidence-blocked, not engineering-blocked**, for M9.
