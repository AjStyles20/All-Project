# P007 / Legacy P004 — School Point & Digital Economy System

## Pass 004 — Formal Research and Experimental Specification

**Date:** 2026-09-10  
**Portfolio ID:** P007  
**Legacy ID / directory mapping:** P004  
**Research gate:** CONDITIONAL GO TO FORMAL SPECIFICATION

## 1. Frozen research-facing title

**Design and Evaluation of an Evidence-Aware Governance Audit System for Fairness and Incentive Integrity in School Reward Economies**

This title is provisional for portfolio comparison and may later be shortened for an academic submission, but its research meaning is frozen unless an explicit decision record changes it.

## 2. Problem statement

Digital school reward/token systems can record points, balances, redemptions and issuer activity, but aggregate dashboards alone may not distinguish normal heterogeneity from policy outcomes that warrant governance review. Simple disparity or anomaly signals can also be misinterpreted as proof of bias, misconduct or gaming when contextual evidence is incomplete.

The research problem is therefore not how to build a school point system. It is how to audit reward-policy outcomes using transaction-level evidence while preserving uncertainty and avoiding unsupported governance claims.

## 3. Primary research question

**RQ1:** Can a contextual, transaction-level reward-policy audit detect predefined fairness disparities and incentive-gaming patterns in a school reward economy more reliably than ordinary aggregate reporting, static thresholds, or disparity-only monitoring, while reducing unsupported fairness/gaming conclusions?

## 4. Secondary research questions

**RQ2:** Does adding contextual exposure/opportunity information reduce false fairness signals relative to disparity-only monitoring?

**RQ3:** Can the audit identify proxy-optimizing reward behaviour that satisfies the formal earning rule but diverges from the policy's intended educational objective?

**RQ4:** When evidence is incomplete, can the audit appropriately return `INSUFFICIENT CONTEXT` rather than forcing a fairness or misconduct interpretation?

## 5. Frozen hypothesis

### H5 — Contextual Reward-Policy Outcome Audit

A contextual transaction-level governance audit will outperform simpler baselines on a combined objective consisting of:

1. detecting injected reward-policy failure modes;
2. limiting false-positive governance signals under legitimate heterogeneous conditions; and
3. limiting unsupported fairness/gaming claims when contextual evidence is insufficient.

This is the surviving bounded hypothesis from Passes 001–003.

### Null hypothesis

**H0:** The contextual audit does not provide a material improvement over simpler baselines once false positives and unsupported claims are included in the evaluation.

If H0 cannot be rejected under the predefined experiment, P007 must not claim the proposed audit mechanism is superior.

## 6. Explicit non-claims

P007 does **not** claim to invent:

- school token economies;
- digital points, balances or reward stores;
- educational gamification;
- fairness or equity analysis;
- anomaly detection;
- algorithmic fairness monitoring;
- reward-hacking / Goodhart-style failure concepts;
- human oversight;
- PBIS acknowledgements or equity practices;
- school-economy planning;
- blockchain-based educational rewards.

The candidate contribution is a bounded design-and-evaluation of a contextual governance audit in a school reward-economy setting.

## 7. System boundary

### In scope

- school-defined reward policies;
- point issuance and redemption transactions;
- issuer identity/role;
- student/class/group context where ethically and legally appropriate;
- eligibility/exposure/opportunity information;
- policy versioning;
- reason/category metadata;
- contextual audit logic;
- fairness disparity signals;
- incentive-integrity signals;
- uncertainty/insufficient-context state;
- human-review evidence package;
- experiment and evaluation framework.

### Out of scope

- automatic discipline;
- automatic accusations of teacher bias or student cheating;
- automated moral ranking of students;
- replacing school leadership judgment;
- facial recognition or biometric monitoring;
- unrestricted student-to-student currency transfer;
- cryptocurrency/NFT/blockchain architecture unless later evidence creates a concrete requirement;
- psychological diagnosis;
- claims of causal discrimination based only on statistical disparity.

## 8. Canonical audit output states

The audit must use three primary states:

1. **NO MATERIAL SIGNAL** — no predefined policy-governance condition detected above the configured evidence threshold.
2. **GOVERNANCE SIGNAL** — evidence warrants human review, but the output is not a misconduct, discrimination or causal verdict.
3. **INSUFFICIENT CONTEXT** — an observed difference exists, but available evidence is inadequate to justify a governance interpretation.

The prototype must never collapse these into binary `FAIR/UNFAIR` output.

## 9. Canonical evidence vocabulary

- **OBSERVATION:** directly present in the ledger/context data.
- **DISPARITY:** measurable difference between defined populations/conditions.
- **ANOMALY:** statistically unusual pattern relative to a specified baseline.
- **POLICY-OBJECTIVE DEVIATION:** behaviour that satisfies or exploits the formal reward rule while diverging from the stated objective under the experiment's known ground truth.
- **GOVERNANCE SIGNAL:** review-worthy evidence without causal/misconduct conclusion.
- **INSUFFICIENT CONTEXT:** evidence cannot distinguish relevant competing explanations.
- **VERIFIED EXPERIMENT CONDITION:** injected/labelled condition known by construction in the synthetic or controlled benchmark.

## 10. Minimum data schema

### RewardTransaction
- transaction_id
- student_id (pseudonymous in research datasets)
- issuer_id
- policy_id
- policy_version
- action_type: EARN / REDEEM / REVERSE
- category
- amount
- reason_code
- timestamp
- approval_status if applicable

### StudentContext
- student_id
- class/group
- relevant eligibility flags
- opportunity/exposure counts by policy/category
- optional protected/sensitive attributes only when ethically justified for controlled fairness experiments

### IssuerContext
- issuer_id
- role
- class/activity exposure
- permitted policy scope

### RewardPolicy
- policy_id
- version
- earning rule
- intended objective
- eligible population
- earning opportunity definition
- point amount/range
- validity period

### RewardCatalogue
- reward_id
- point_cost
- availability
- category
- stock/limit if applicable

## 11. Controlled benchmark scenarios

The initial research benchmark must contain labelled synthetic/controlled scenarios. Real student data is not required to establish the first research result.

### S0 — Normal heterogeneous operation
Natural variation across teachers/classes/categories without injected unfairness or gaming.

### S1 — Unequal earning opportunity
One group receives systematically fewer eligible earning opportunities while individual behaviour is otherwise comparable.

### S2 — Systematic issuer disparity
An issuer applies the same formal policy differently across comparable groups under controlled conditions.

### S3 — Legitimate high issuance
An issuer awards substantially more points because verified exposure/opportunity is genuinely higher. This is a critical false-positive control.

### S4 — Proxy / incentive gaming
Participants optimize a low-cost proxy that satisfies the formal earning rule while reducing alignment with the intended educational objective.

Example: a policy rewards number of completed books, while agents/students maximize very short qualifying books.

### S5 — Category concentration
A reward category dominates issuance and systematically advantages students with access to that category.

### S6 — Missing context
Observed disparity is present, but key eligibility/exposure data is deliberately removed. Correct output should tend toward `INSUFFICIENT CONTEXT`, not an accusation.

### S7 — Economy imbalance
Excessive issuance, low redemption, reward scarcity or unsustainable outstanding balances. This remains supporting instrumentation rather than the primary novelty claim.

### S8 — Multi-condition case
Two or more conditions occur simultaneously, testing whether the audit over-simplifies the situation into a single explanation.

## 12. Baselines

### B0 — Aggregate dashboard
Counts, averages, totals, rankings and simple charts only. No automated governance interpretation.

### B1 — Static threshold rules
Configured limits such as issuer-rate thresholds, category concentration limits or disparity thresholds.

### B2 — Generic statistical anomaly detection
Unsupervised/outlier-based detection over transaction features without explicit policy-context reasoning.

### B3 — Disparity-only fairness monitoring
Group-level disparity metrics without opportunity/exposure context.

### B4 — P007 contextual governance audit
Combines policy metadata, transaction history, opportunity/exposure context, disparity/anomaly evidence and uncertainty rules to produce bounded audit states and human-review evidence.

B4 must not receive privileged access to the synthetic ground-truth labels used for evaluation.

## 13. Primary evaluation metrics

### M1 — Failure-mode detection recall
Proportion of injected S1/S2/S4/S5 governance conditions correctly surfaced for review.

### M2 — False-positive rate
Proportion of normal/legitimate cases, especially S0 and S3, incorrectly surfaced as governance concerns.

### M3 — Unsupported-claim rate
Proportion of outputs that imply causal unfairness, misconduct or gaming beyond what the available evidence supports.

This metric is mandatory and must not be replaced by ordinary classification accuracy.

### M4 — Appropriate-insufficiency rate
For S6 and other deliberately underdetermined cases, proportion correctly assigned `INSUFFICIENT CONTEXT`.

### M5 — Incorrect-insufficiency rate
Proportion of identifiable injected conditions incorrectly withheld as insufficient context.

### M6 — Time/evidence-to-detection
Number of transactions/events or elapsed simulated time required before a reliable governance signal appears.

### M7 — Review-evidence completeness
Whether the output exposes the observations, relevant comparison, missing context and non-claims needed for human review.

### M8 — Computational cost
Runtime, memory and storage footprint for the audit workload.

## 14. Composite success rule

B4 is not considered successful merely because it maximizes recall.

A successful result requires a meaningful improvement over at least B1 and B3 on a predeclared combined evaluation that includes:

- detection recall;
- false-positive rate;
- unsupported-claim rate; and
- appropriate-insufficiency rate.

A model that finds more anomalies by making more unsupported accusations fails the research objective.

Exact numerical superiority margins are to be fixed before running the final experiment, after a small pilot is used only for scale estimation—not for tuning the final test threshold to guarantee a win.

## 15. Falsification criteria

The research hypothesis should be treated as falsified or unsupported if any of the following occurs:

1. B4 does not materially outperform B1/B3 on the combined objective.
2. B4's improved recall is purchased through materially worse false-positive or unsupported-claim rates.
3. Context features fail to reduce incorrect interpretation in S3/S6.
4. The audit cannot distinguish proxy-gaming scenarios from legitimate high performance better than simple baselines.
5. Results depend on benchmark leakage, privileged ground-truth labels, or scenario rules unavailable to a deployed system.
6. The claimed effect disappears under reasonable variations in class size, issuance rate, group composition or noise.

A negative result remains academically reportable; it must not be rewritten into a success claim.

## 16. Experimental design safeguards

- Define scenario generator independently from B4 decision logic where practical.
- Separate development/pilot scenarios from final evaluation seeds.
- Use multiple random seeds.
- Include legitimate heterogeneity controls.
- Include missing-data conditions.
- Keep all policy rules and injected conditions versioned.
- Record every threshold and parameter used by each baseline.
- Do not tune on final-test labels.
- Preserve raw synthetic benchmark data and generated audit outputs.
- Report failures and ambiguous cases, not only successful examples.

## 17. Human-review evaluation

If human evaluation is feasible, reviewers should receive audit evidence without being told the injected scenario label and answer bounded questions such as:

1. Is review warranted?
2. Does the evidence support a causal/misconduct conclusion?
3. What additional context is needed?
4. Is the explanation understandable enough to investigate?

The prototype should evaluate decision support, not reviewer agreement with a predetermined accusation.

## 18. Ethics, privacy and safeguarding constraints

- Prefer synthetic data for initial research.
- Pseudonymize identifiers in any later real-world pilot.
- Collect only data required for the defined audit question.
- Do not expose sensitive subgroup statistics to unauthorized users.
- Do not rank students morally or socially.
- Do not infer protected characteristics.
- Any use of protected/sensitive attributes for fairness evaluation must be explicitly justified, access-controlled and ethically approved where required.
- Audit signals must not automatically trigger punishment, public labeling or reward removal.
- Preserve appeal/review paths for any operational deployment.
- Distinguish data quality problems from behavioural conclusions.

## 19. Feasible implementation architecture

A lightweight implementation is sufficient:

`Policy configuration + synthetic scenario generator -> relational transaction store -> feature/context extraction -> baseline/audit engines -> audit evidence package -> evaluation harness -> reviewer dashboard`

Suggested implementation candidates:
- Python for data generation/audit/evaluation;
- SQLite or PostgreSQL for ledger storage;
- pandas/numpy/scipy/scikit-learn for lightweight statistical baselines;
- FastAPI or Flask for an optional API;
- simple HTML/CSS/JS or Streamlit for a research dashboard.

Heavy GPU training is not required for the core experiment. The project can be executed on low-resource hardware if datasets are kept appropriately bounded.

## 20. Research artifact checklist

Before implementation is declared research-ready, create and freeze:

1. scenario-generation specification;
2. synthetic data schema;
3. policy definitions and intended objectives;
4. baseline definitions;
5. metric formulas;
6. threshold-selection procedure;
7. pilot/final-test split procedure;
8. random-seed policy;
9. audit-output schema;
10. claim/non-claim statement;
11. ethics/privacy statement;
12. reproducibility instructions.

## 21. Research claim allowed if experiment succeeds

A defensible claim would be of the form:

> In the defined synthetic/controlled school reward-economy benchmark, the contextual governance-audit approach improved detection of predefined policy failure modes while reducing unsupported governance conclusions relative to the specified simpler baselines.

The wording must remain tied to the benchmark and measured results.

## 22. Claims not allowed even after a positive experiment

Do not claim:
- the system proves discrimination;
- the system detects all unfairness;
- the system prevents cheating;
- the system makes a school reward economy fair;
- the system is universally applicable to all schools;
- the system is production-ready without live validation;
- the method is the first or unique unless a separate exhaustive novelty standard is actually met.

## 23. Current decision

**CONDITIONAL GO TO RESEARCH IMPLEMENTATION DESIGN.**

The project has passed the broad novelty-screening stage only in the bounded H5 form. The next work should be a reproducible benchmark/scenario specification and audit-engine design, not another feature-expansion exercise.

P007 remains parked from full product implementation until portfolio comparison or explicit authorization. Research prototyping may proceed only within the frozen experimental boundary above.
