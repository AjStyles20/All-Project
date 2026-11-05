# P007 benchmark results (2026-11-05)

Raw data: `results/final_results.json`, `results/pilot_results.json`. Protocol: `EVALUATION_PROTOCOL.md`.

## Final run (seeds 1000–1019, 9 scenarios, 180 cases per engine)

| Engine | M1 recall | M2 false positives | M3 unsupported claims | M4 appropriate insufficiency |
|---|---|---|---|---|
| B0 totals only | 0.00 | 0.00 | — | 0.00 |
| B1 static thresholds | 0.39 | 0.38 | 0.58 | 0.00 |
| B2 anomaly detection | 0.01 | 0.40 | 0.93 | 0.00 |
| B3 disparity only | 0.57 | 0.30 | 0.41 | 0.00 |
| B4 contextual audit | 1.00 | 0.05 | 0.02 | 1.00 |

Composite rule: B4 better than B1 and better than B3, so **supported on this benchmark**. The same held with 15 students per group (B4: 0.99, 0.08, 0.05, 1.00) and 60 per group (B4: 1.00, 0.00, 0.00, 1.00). B4's two false positives at the default size were in S0 (natural variation). M5 was 0 for every engine.

## What this does and does not show
**Shows:** the ledger, the generator, the five audit methods and the harness work end to end. The baselines fail in the expected ways: static thresholds flag the legitimate busy issuer (S3); disparity-only monitoring accuses when opportunity data is missing (S6) and cannot tell gaming from group differences.

**Does not show** that the contextual audit works on real schools, or even on scenarios it was not designed around:
1. **The same agent wrote both the scenarios and B4.** B4 checks for the very mechanisms the generator injects (opportunity counts, rate per opportunity, pages per award, catalogue capacity). Pass 004 §16 asks for the generator to be defined independently "where practical"; here it was not, so a near-perfect score is expected rather than informative. This is the main threat to validity (falsification criterion 5).
2. The scenarios are clean: one injected effect, large effect sizes, two groups.
3. B4 needed opportunity counts to be recorded at all. Schools may not record them.
4. M6 and M7 were not measured, and no human reviewer has seen the evidence packages.

Per Pass 004 §21–§22 the most that may be claimed is: *in this synthetic benchmark, the contextual audit surfaced the injected conditions with fewer unsupported conclusions than the specified baselines.*

## To make the result informative
- Scenarios written by someone who has not seen B4's logic, including subtle and overlapping effects.
- Smaller effect sizes and more groups.
- Measuring M6 (evidence needed before detection) and M7 with independent reviewers (Pass 004 §17).
