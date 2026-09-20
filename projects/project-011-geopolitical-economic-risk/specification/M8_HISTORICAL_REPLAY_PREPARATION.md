# P003 M8 — Historical Replay Preparation

## Status

**PREPARATION ONLY — NO HISTORICAL CASE HAS BEEN ADMITTED YET.**

M7 infrastructure is CI-verified. M8 begins source/data qualification before case selection. No real event may enter the frozen historical evaluation merely because it is famous or convenient.

## M7 verification

GitHub Actions P003 ETEC Tests run #43: **31 passed, 0 failed in 0.09s**.

This closes the bounded B0-B3 comparison infrastructure. It does not show that B3 outperforms B2.

## Qualified data-source families

### 1. UN Comtrade — direct trade exposure

Role: T2 EXPOSURE and selected event/product exposure reconstruction.

Required frozen query metadata:
- reporter;
- partner;
- trade flow;
- period;
- product classification and edition;
- commodity/HS code;
- retrieval date;
- API/query mode;
- raw response snapshot/hash;
- publication/data-availability metadata where obtainable.

Important: reporter/partner/flow/period/product parameters are part of the evidence definition. Classification conversions must not be silently mixed.

### 2. Central Bank of Nigeria (CBN) — macro/external-sector context

Potential roles: exchange-rate regime/context, external trade aggregates, reserves, balance of payments, commodity prices and other macro series where relevant to a specific case.

Required metadata:
- exact series/table;
- frequency;
- units;
- observation period;
- publication/retrieval date;
- bulletin/database vintage;
- methodological/regime notes where applicable.

A CBN macro series is not automatically evidence of a causal domestic-transmission edge.

### 3. National Bureau of Statistics (NBS) — Consumer Price Index/outcome context

Potential role: later observed consumer-price outcomes where the historical case actually targets a CPI category or aggregate.

Required metadata:
- report/release;
- CPI classification/category;
- base/methodology applicable to the period;
- observation period;
- release date;
- frozen source snapshot/hash.

CPI weights measure expenditure importance; they must not be treated as causal pass-through coefficients.

## Concordance requirement

The chain HS product → industry/activity → Nigerian sector/use relationship → COICOP/consumer category must be explicit when a claim crosses those classifications.

For every mapping preserve:
- source and taxonomy/version;
- mapping type (one-to-one, one-to-many, many-to-one);
- ambiguity;
- reviewer decision where required;
- confidence/limitations.

No invented HS→industry→COICOP bridge is admissible.

## Historical case admission manifest

A candidate case is admitted only if all mandatory fields can be frozen:

1. case identifier and mechanism family;
2. authoritative event source and event date/scope;
3. information cutoff;
4. affected product/route identifier known by cutoff;
5. Nigeria exposure data available at cutoff or reproducibly reconstructable without later leakage;
6. required concordances documented;
7. target local outcome stated before inspecting the outcome used for scoring;
8. outcome/reference evidence independent of B3;
9. counterevidence search plan;
10. B0-B3 equivalent-information plan;
11. negative-control status/mechanism-diversity rationale;
12. data-vintage/revision policy.

If a mandatory link cannot be frozen, the case is rejected or used only at the strongest admissible upstream transition.

## Anti-leakage rule

Later-released or revised observations may be used to evaluate a historical warning, but they may not be inserted into the simulated information set available at the historical cutoff.

## Next research action

Create a candidate-case manifest using authoritative event issuers and source-qualified economic data. Candidate families remain hypotheses for selection, not admitted cases. Selection must be completed before outcome scoring and must include at least one negative control.
