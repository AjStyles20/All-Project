# P003 M8 — Candidate A Replay-Mode Decision

## Decision

**Candidate A will not be represented as a strict 24-February-2022 real-time replay using the currently retrieved 2021 UN Comtrade wheat figures.**

It is retained as a **retrospective evidence reconstruction candidate** unless a separately archived, date-stamped source proves that the required Nigeria/product exposure values were available at the simulated decision cutoff.

## Why

UN Comtrade's current documentation states that:
- annual country submissions arrive on varying schedules;
- provisional observations may later be revised;
- the API exposes the latest available reported dataset;
- only one current version is retained rather than a permanent archive of every earlier version;
- publication-date/data-availability metadata can be queried.

The UN 2021 International Trade Statistics Yearbook states that its country tables/data reflect merchandise-trade statistics available in UN Comtrade by the **end of June 2022**. This is useful evidence that 2021 data existed by that later point, but it does not establish that the exact Nigeria/product observations used in this candidate were available on 24 February 2022.

Therefore using today's 2021 values while claiming they were known on 24 February would risk look-ahead/vintage leakage.

## Research consequence

Two replay modes are now formally distinguished:

### Mode R1 — Strict cutoff-safe historical replay
Every evidence item used to release a claim must have demonstrable availability at or before the information cutoff. Later observations may score the warning but cannot enter its information set.

### Mode R2 — Retrospective evidence reconstruction
Historical event/exposure/mechanism data may be reconstructed from later-accessed archival datasets. Every such item retains its reference period and retrieval/publication limitations. R2 can test pathway logic and evidence sufficiency retrospectively, but cannot support claims about what a real-time system could have known at the original event date.

R1 and R2 results must never be pooled as though they answer the same question.

## Candidate A state

- T1 event: admissible anchor.
- T2 wheat exposure: strong retrospective evidence, but current retrieved values are not proven cutoff-safe for 24 February 2022.
- T3 milling/bakery mechanism: plausible and independently documented, with important counterchannels.
- T4 local scenario: still withheld.
- Outcome: Bread and cereals remains the mechanism-aligned outcome family, but scoring horizon is not frozen.

## Additional counterevidence retained

USDA/FAS Lagos later documented that Nigerian wheat millers diversified import sources because of the Russia–Ukraine crisis. This supports treating substitution as a material pathway modifier rather than assuming a fixed Russia/Ukraine-to-Nigeria pass-through.

## Next gate

Before any T4 release:
1. define a predeclared scenario statement;
2. define a defensible lag/horizon without outcome optimization;
3. freeze required counterevidence fields;
4. decide whether Candidate A remains R2 or can be upgraded to R1 with genuinely cutoff-safe archived evidence;
5. keep B0-B3 inputs equivalent within whichever replay mode is used.

No forecast-performance claim is authorized by this decision.
