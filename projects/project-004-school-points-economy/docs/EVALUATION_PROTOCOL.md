# P007 evaluation protocol

Implements Pass 004 §11–§16. Fixed before the final run (commit `c174ed2`).

## 1. Benchmark
`p007/benchmark.py`: 60 students in two neutral groups (A, B), four issuers, three policies (reading, with pages as the objective measure; participation; service), and a reward catalogue. Each student's engagement is drawn independently of group, so groups differ only where a scenario injects a difference.

| Scenario | Injected | Ground truth |
|---|---|---|
| S0 | Nothing | No condition |
| S1 | Group B gets half the participation opportunities | `OPPORTUNITY_GAP` |
| S2 | Issuer T2 awards group B at half the rate per opportunity | `ISSUER_DISPARITY` |
| S3 | Issuer T3 runs 4× the participation sessions for everyone | No condition (false-positive control) |
| S4 | A quarter of students log 3× as many very short books | `PROXY_GAMING` |
| S5 | Service is the dominant category and only group A can earn it | `CATEGORY_CONCENTRATION` |
| S6 | S1, with every opportunity count removed | Expect `INSUFFICIENT CONTEXT` |
| S7 | Small catalogue, almost no redemptions | `ECONOMY_IMBALANCE` |
| S8 | S2 and S4 together | Both |

The audits receive a `Dataset` only; ground truth is returned separately and never stored by the API.

## 2. Seeds
- Pilot: seeds 0–4, used only to check that the harness runs.
- Final: seeds 1000–1019, run once with the thresholds in `p007/audit.py` `THRESHOLDS` as committed in `c174ed2`.
- Robustness (falsification criterion 6): the final seeds again with 15 and 60 students per group.

## 3. Metrics
For each engine over all scenario × seed cases:

- A signal **surfaces** a condition if its kind is in that condition's accepted set (`ACCEPTED` in `p007/evaluation.py`). Generic kinds count: a group disparity or an outlier pointing at the right place earns credit even when the engine cannot say why.
- **M1 recall** = surfaced conditions / injected conditions.
- **M2 false-positive rate** = S0 and S3 cases with any governance signal / S0 and S3 cases.
- **M3 unsupported-claim rate** = governance signals whose kind matches no injected condition in that case / all governance signals. In S6 every governance signal is unsupported, because the scenario is deliberately underdetermined.
- **M4 appropriate insufficiency** = S6 cases with at least one `INSUFFICIENT CONTEXT` finding and no governance signal / S6 cases.
- **M5 incorrect insufficiency** = injected conditions not surfaced but reported as insufficient context / injected conditions.
- **M8 cost**: total audit seconds and peak memory.
- M6 (time to detection) and M7 (evidence completeness, needs human reviewers) are not measured yet.

## 4. Composite success rule
Against each of B1 and B3, B4 must be at least 0.05 better on at least three of M1, M2, M3, M4, and no more than 0.05 worse on any of them. The hypothesis is **supported on this benchmark** only if both comparisons pass. Implemented in `success_rule()`; tested so that recall bought with more accusations fails it.
