# P003 — Supervisor and Defense Master Brief

**Project:** Geopolitical Risk to Economic Impact Forecasting & Warning System  
**Canonical ID:** P003  
**Implementation architecture:** Economic Transmission Evidence Contract (ETEC)  
**Current state:** implementation active; historical-case design frozen; M9 software ready; real B2 execution and independent human review pending.

---

## 1. Executive summary

P003 investigates a reliability problem in geopolitical-economic warning systems: a verified geopolitical event can be transformed into a persuasive local economic narrative even when one or more links between the event and the claimed Nigerian outcome are missing, stale, conditional, contested or contradicted.

The project does not attempt to solve universal geopolitical forecasting. Instead, it tests a narrower mechanism:

**typed transmission-edge evidence sufficiency + weakest-link downstream claim progression.**

The system represents a geopolitical-to-economic pathway as a sequence of evidence-dependent transitions. A downstream claim may progress only as far as its weakest mandatory evidentiary link permits. Missing or adverse evidence therefore causes the system to stop, downgrade, recompute or abstain rather than allowing narrative plausibility to substitute for evidence.

The architecture used to implement this rule is the **Economic Transmission Evidence Contract (ETEC)**.

The implementation has passed its deterministic software/falsification checkpoints and historical replay preparation. The comparative empirical stage is not complete because the frozen B2 language-model baseline has not yet been executed in a qualifying controlled environment and no independent human reviewer judgments have yet been collected.

---

## 2. The problem being investigated

A geopolitical event can be real while a downstream economic claim about Nigeria is poorly supported.

For example, the following reasoning is not automatically valid:

```text
Major international disruption
        ↓
global prices/trade affected
        ↓
Nigeria must be materially exposed
        ↓
a Nigerian sector must be affected
        ↓
consumer/fiscal outcome must follow
        ↓
a numerical forecast can be produced
```

Each arrow is a separate evidentiary claim.

P003 asks whether explicitly typing and testing those arrows can reduce unsupported downstream claims without eliminating useful warnings.

---

## 3. Research question

The bounded research question is:

> Can typed transmission-edge evidence requirements and weakest-link claim progression reduce unsupported geopolitical-to-economic downstream claims, relative to a language-model explanation baseline using equivalent frozen evidence, while preserving useful Nigeria-specific warnings and appropriate structural abstention?

This question is deliberately narrower than asking whether artificial intelligence can predict the Nigerian economy.

---

## 4. What is being contributed

### Contribution under test

**Typed transmission-edge evidence sufficiency + weakest-link downstream claim progression.**

The contribution is not simply:
- using a Large Language Model (LLM);
- Retrieval-Augmented Generation (RAG);
- storing provenance;
- using a knowledge graph;
- detecting contradictions;
- abstaining when uncertain;
- creating an evidence contract.

Those ideas have substantial prior-art pressure.

The research contribution is the domain-specific mechanism that constrains **how far an economic claim may progress through typed transmission edges**, with downstream claim strength capped by the weakest mandatory edge.

### ETEC's role

ETEC is the implementation architecture for the contribution. It operationalizes evidence objects, transition rules, edge states, counterevidence, recomputation, provenance and structural abstention.

---

## 5. Claim progression model

The progression ladder is:

```text
EVENT
  │
  │ T1 — verify the event
  ▼
EVENT VERIFIED
  │
  │ T2 — establish target-country exposure
  ▼
EXPOSURE MEASURED
  │
  │ T3 — establish domestic transmission
  ▼
TRANSMISSION SUPPORTED
  │
  │ T4 — establish bounded directional scenario
  ▼
SCENARIO SUPPORTED
  │
  │ T5 — establish quantitative-model eligibility
  ▼
MODEL ESTIMATE ELIGIBLE
  │
  │ T6 — establish out-of-sample/calibration evidence
  ▼
CALIBRATED FORECAST
```

### T1 — Event verification
Requires evidence for the actor, action, scope, timing and affected entity/product/route where relevant.

### T2 — Exposure
Requires compatible target-country exposure evidence. A global event alone cannot establish Nigerian exposure.

### T3 — Domestic transmission
Requires an explicit economic linkage from the exposed product/route to the Nigerian sector, use, consumer category or fiscal mechanism being claimed.

### T4 — Scenario
Requires a supported direction/mechanism, material counterevidence assessment, horizon and assumptions.

### T5 — Model-estimate eligibility
Requires an independently specified quantitative model matching the target variable, regime, horizon and inputs, with documented estimation/training data and validation.

### T6 — Calibrated forecast
Requires sufficient time-respecting/out-of-sample validation and uncertainty/calibration evidence.

Failure at T5 therefore does not erase a supported T4 scenario; it prohibits promotion of that scenario into a numerical model estimate.

---

## 6. Edge states

Required pathway edges can be:

- **VERIFIED**
- **SUPPORTED**
- **CONDITIONAL**
- **CONTESTED**
- **STALE**
- **INSUFFICIENT**
- **CONTRADICTED**

The current conservative progression logic treats only the required passing states as sufficient for continued progression.

Counterevidence is not stored as decorative commentary. If credible counterevidence changes an edge state, dependent downstream progression is recomputed.

---

## 7. Example of weakest-link reasoning

Suppose a trade restriction is verified and Nigerian imports of the affected product are measurable, but there is no defensible product-to-domestic-sector linkage.

```text
T1 Event verification             SUPPORTED
T2 Nigerian exposure              SUPPORTED
T3 Domestic transmission          INSUFFICIENT
T4 Local directional scenario     NOT REACHED
T5 Numerical model                NOT REACHED
T6 Calibrated forecast            NOT REACHED
```

The correct P003 output is therefore an exposure-level result plus an explanation of the missing T3 evidence—not a plausible downstream story invented by the system.

---

## 8. Baselines

The experiment separates several levels of reasoning.

### B0 — News / Geopolitical Risk signal
Represents geopolitical/news salience without a Nigeria-specific evidence chain.

### B1 — Event + Exposure
Uses a verified event and direct Nigerian exposure but does not require downstream transmission contracts.

### B2 — LLM/RAG Explanation
A language model receives equivalent frozen evidence and is asked to explain plausible Nigerian consequences under a fixed prompt.

This is the critical narrative baseline because it tests whether fluent reasoning produces claims that exceed the supplied evidence.

### B3 — ETEC
Uses typed transition contracts, provenance, counterevidence, weakest-link progression and structural abstention.

### B4 — Optional quantitative/econometric comparator
Permitted only where a genuinely applicable validated model exists. It is not automatically present for every historical case.

---

## 9. Main evaluation metric

**UDCR — Unsupported Downstream Claim Rate**

For determinate independently reviewed downstream claims:

```text
UDCR =
(UNSUPPORTED claims + CONTRADICTED claims)
------------------------------------------------
all determinate downstream claims
```

`INDETERMINATE` judgments are not silently counted as supported or unsupported.

A lower B3 UDCR than B2 is a predeclared central acceptance condition. That result has **not yet been measured**.

Other measures include structural-abstention quality, false local-warning behavior on negative controls, provenance completeness, counterevidence sensitivity, contradiction handling, reviewer agreement, pathway coverage and reproducibility.

---

## 10. Falsification suite

The implementation includes eight deterministic attacks.

| Test | Attack | Required behavior |
|---|---|---|
| F1 | Missing domestic-transmission link | Stop at exposure and identify T3 |
| F2 | Counterevidence reversal | Downgrade and recompute |
| F3 | Contradictory event evidence | Expose contradiction and withhold downstream claim |
| F4 | Staleness | Expired required evidence blocks progression |
| F5 | Narrative/LLM temptation | Persuasive narrative cannot replace a missing edge |
| F6 | Negative control | No material Nigerian exposure means no local downstream warning |
| F7 | Model-eligibility trap | No T5 means no numerical estimate/calibrated forecast |
| F8 | Revision/vintage trap | Later evidence cannot silently rewrite historical replay |

Passing these tests establishes enforcement of the software contract. It does not establish that historical economic judgments are scientifically correct.

---

## 11. Historical case design

The case set was frozen before real B2 execution and human outcome judgment to reduce case-selection bias.

### Candidate A — Russia/Ukraine wheat disruption

Role: positive downstream-capable historical case.

The R2 reconstruction supports progression through T4 for a bounded scenario involving upward pressure on Nigerian wheat-flour and bread/cereal costs, conditional on supplier substitution, exchange rates, inventories/contracts, domestic supply, logistics and policy intervention.

T5 and T6 remain withheld. Later observations may be directionally consistent with the scenario but cannot establish exclusive causality.

### NC-01 — Russian urea direct-exposure negative control

Role: negative control.

The narrow question is whether geopolitical salience should trigger a warning based on material direct Russian urea dependence.

The reconstruction found non-zero but negligible direct Russian urea exposure for the narrow pathway. The expected B3 behavior is therefore to stop rather than convert the global fertilizer shock into an unsupported local direct-exposure warning.

The case does not claim that Nigeria was unaffected by global fertilizer prices, gas/feedstock channels, other fertilizers or indirect trade.

### Candidate B — Red Sea/Suez disruption

Role: missing-exposure stress case.

The global disruption is supported, but sufficient Nigeria-specific route/product exposure has not been established. Progression therefore stops at T2 rather than inferring Nigerian exposure from broad Africa/global shipping effects.

### Candidate C — October 2023 foreign-exchange restriction removal

Role: conditional-transmission stress case.

Exposure evidence can pass T2, but the domestic-transmission edge remains conditional/non-passing. T4 and later claims are therefore withheld.

### Candidate D — 2022 refined-fuel/PMS subsidy-fiscal channel

Role: mechanism-diverse prospective replication/extension.

The R2 reconstruction supports a bounded T4 scenario: an external increase in imported refined-fuel/Premium Motor Spirit (PMS) costs can place upward pressure on the fiscal burden of maintaining regulated PMS prices, conditional on the subsidy regime remaining and subject to crude-oil revenue, production, exchange-rate, volume and policy counterchannels.

Later observations are directionally consistent with that bounded scenario, but exclusive war causality and numerical forecast claims are prohibited.

Candidate D remains a prospective second-wave case and is not retroactively pooled into the original first-wave experiment.

---

## 12. R1 and R2 replay meaning

Historical replay must distinguish what was genuinely knowable at the event cutoff from evidence reconstructed later.

**R1** would require evidence demonstrably available by the historical information cutoff.

**R2** is a retrospective reconstruction where the relevant historical observation is reconstructed from current or later-accessed records but exact publication/vintage availability at the historical cutoff cannot be fully established.

The admitted comparison cases currently rely on R2 where specified. This limitation must remain visible.

---

## 13. Data and evidence families

The design uses or anticipates:
- UN Comtrade trade observations;
- Central Bank of Nigeria (CBN) macroeconomic/external-sector evidence;
- Nigerian statistical/CPI material;
- explicit classification/concordance evidence;
- documented sector/use relationships;
- authoritative event/policy sources;
- relevant commodity/freight information where a case requires it.

A product classification cannot be freely converted into a household or sector claim. The intended transformation is explicit:

```text
HS product
   ↓
industry/activity classification
   ↓
Nigerian sector/use relationship
   ↓
COICOP / consumer category
```

where **HS** means Harmonized System and **COICOP** means Classification of Individual Consumption According to Purpose.

Ambiguous mappings require review and cannot silently support magnitude claims.

---

## 14. Evidence provenance and reproducibility

Evidence objects preserve relevant provenance such as:
- evidence identifier;
- transition;
- source authority class;
- source reference;
- publication/observation time;
- retrieval time;
- information vintage;
- geography;
- product/classification scope;
- validity/staleness information;
- limitations;
- frozen snapshot/hash where practical.

Historical replay records are canonically serialized and SHA-256 hashed so that later mutation can be detected.

---

## 15. Implementation architecture

The implementation is Python-first and deliberately lightweight.

Major domain components include:
- evidence and transition models;
- progression evaluator;
- recomputation logic;
- audit trace;
- deterministic historical fixtures;
- persistence/replay integrity;
- B0–B3 baseline adapters;
- comparative evidence packets;
- B2 experiment manifests;
- deterministic B2 prompt serialization;
- immutable B2 run records;
- atomic-claim provenance validation;
- reviewer blinding;
- reviewer package hashing;
- reviewer judgment locking;
- reviewer agreement utilities;
- comparative-analysis authorization gate.

The deterministic ETEC rules—not an LLM—decide whether mandatory evidence edges pass.

---

## 16. Implementation milestones

```text
M0  Entry contract                         CLOSED
M1  Core evidence/transition domain        CLOSED
M2  Weakest-link progression               CLOSED
M3  F1 missing-link vertical slice         CLOSED
M4  Recompute/counterevidence/staleness     CLOSED
M5  F1–F8 deterministic contracts          CLOSED
M6  Replay persistence/reproducibility      CLOSED
M7  B0–B3 comparison infrastructure        CLOSED (software boundary)
M8  Historical replay/case registry        CLOSED
M9  Independent evaluation                 READY / EXTERNALLY BLOCKED
M10 Frozen historical evaluation           NOT COMPLETE
```

The latest verified automated test state at the time of this brief is **88 passed, 0 failed**.

---

## 17. M9 external-evidence pipeline

The intended empirical chain is:

```text
Frozen B2 manifest + packet hash
              ↓
controlled real model execution
              ↓
immutable raw B2 record
              ↓
atomic claim extraction
              ↓
claim blinding
              ↓
frozen reviewer package
              ↓
independent reviewer judgments
              ↓
pre-unblinding SHA-256 judgment lock
              ↓
analysis authorization
              ↓
unblinding
              ↓
UDCR + agreement + abstention analysis
```

The software rejects unplanned B2 run IDs, mutated evidence packets, incomplete reviewer submissions, duplicate reviewer responses, post-lock judgment changes, same-reviewer double use and mismatched claim sets.

---

## 18. Why M9 is blocked

The six frozen first-wave B2 runs are:

```text
B2-A-001
B2-A-002
B2-A-003
B2-NC01-001
B2-NC01-002
B2-NC01-003
```

They have not been executed.

A non-experimental attempt to qualify the connected Hugging Face Jobs environment was rejected before execution with HTTP 402 Payment Required. No B2 run ID or frozen prompt was consumed.

No other currently exposed connector qualified as a controlled text-generation endpoint with the provenance required by the frozen experiment.

No independent human reviewer judgments have been collected.

Therefore P003 is **externally evidence-blocked, not engineering-blocked**, at M9.

---

## 19. What has actually been demonstrated

The project has demonstrated in software that:
- mandatory transitions can be represented explicitly;
- weakest-link progression can stop at the correct missing edge;
- counterevidence can trigger recomputation;
- stale and contradictory evidence can prevent progression;
- a T4 scenario cannot automatically become a numerical T5/T6 forecast;
- historical replay records can be integrity-hashed;
- comparative evidence packets can be frozen;
- B2 experimental runs can be bound to predeclared packet hashes/prompts;
- reviewer claims can be blinded;
- reviewer packages and judgments can be integrity-locked;
- analysis can be blocked until reviewer evidence is complete and immutable.

These are engineering/reproducibility results.

---

## 20. What has not been demonstrated

The project has **not** yet demonstrated:
- that B3 has a lower empirical UDCR than B2;
- that independent experts agree sufficiently on the claim labels;
- that structural abstention preserves enough useful coverage;
- validated numerical forecasting accuracy;
- calibrated probability forecasting;
- exclusive causal attribution of historical Nigerian outcomes;
- universal generalization across geopolitical events, products, sectors or countries.

These are scientific boundaries, not missing claims to be filled with assumptions.

---

## 21. Security and integrity

Relevant threats include manipulated/fabricated source material, syndicated duplicates, prompt injection, stale/revised datasets, identifier tampering, unauthorized state mutation, leaked credentials, hallucinated evidence and malicious concordance changes.

Controls include server-authoritative transition logic, source hierarchy, untrusted-content isolation, provenance/audit records, versioned evidence/mappings, explicit staleness, reproducible packet hashes and human review for ambiguous/consequential claims.

The project does not authorize automated trading or consequential financial actions.

---

## 22. Expected examiner questions

### “Is ETEC itself your novelty?”
Not in the generic sense. Evidence contracts, provenance, RAG, abstention and graph-based reasoning have prior art. The contribution under test is the narrower typed transmission-edge sufficiency and weakest-link downstream progression mechanism in this geopolitical-to-economic setting.

### “Why not simply ask an LLM?”
That is precisely why B2 exists. A language model can produce a coherent explanation, but the research question is whether explicit evidence-edge requirements reduce unsupported downstream claims relative to that narrative baseline.

### “Does the system predict prices?”
Not generally. A supported T4 directional scenario is different from a T5 quantitative estimate and a T6 calibrated forecast. Numerical output is prohibited unless the relevant model-evidence gates are satisfied.

### “Why Nigeria?”
The experiment is deliberately bounded to one target-country context so that exposure, classifications, transmission evidence and outcomes can be examined explicitly rather than hiding uncertainty behind a universal architecture.

### “Why do some cases stop early?”
Stopping is part of the mechanism being tested. If Nigeria-specific exposure or domestic transmission is insufficient, producing a stronger claim would violate the research contract.

### “Are your historical cases proof that the method works?”
No. They establish a frozen evaluation design and exercise different progression states. Comparative scientific evidence still requires real B2 outputs and independent judgments.

### “Why only a few cases?”
The current experiment is a bounded undergraduate research test across deliberately different pathway states. It is not a population-level statistical generalization study.

### “Why can't you say Candidate A proves causality?”
Because directional consistency after the event does not isolate the geopolitical event from exchange rates, substitution, inventories, domestic supply, policy and other confounders.

### “What happens if B3 does not beat B2?”
The central reliability contribution is not demonstrated under the frozen acceptance criterion. The project must report that result and be reframed rather than changing the experiment after seeing the outcome.

### “What if reviewers disagree?”
Reviewer agreement is itself measured. Disagreement cannot be silently resolved in B3's favour. Poor reproducibility of link/claim judgments is a predeclared reframe/kill condition.

### “Why is M9 unfinished?”
The controlled B2 execution environment and independent human review are external evidence dependencies. The software required to preserve and evaluate those observations is ready, but the observations themselves must not be fabricated.

---

## 23. Defense-safe one-minute explanation

P003 is not designed to predict every economic consequence of geopolitics. It investigates whether a system can prevent unsupported downstream claims by requiring explicit evidence for each economic transmission step. I model the pathway from a verified geopolitical event through Nigerian exposure, domestic transmission and a bounded local scenario, with numerical forecasts allowed only when additional model-validation requirements are satisfied. The key rule is that the strength of the final claim cannot exceed the weakest required evidence link. I implemented this as the Economic Transmission Evidence Contract and tested the software against missing links, counterevidence, contradictions, stale evidence, negative controls and model-eligibility traps. Historical cases are frozen for evaluation, but I do not yet claim that ETEC empirically outperforms the language-model baseline because the controlled B2 generations and independent human judgments are still pending.

---

## 24. Current conclusion

P003 has moved beyond an idea or generic AI product. It is now a bounded, falsifiable research system with a defined contribution hypothesis, deterministic implementation, adversarial software tests, frozen historical case design, reproducibility controls and a predeclared external evaluation procedure.

The correct current conclusion is **not** “ETEC has been scientifically proven.”

It is:

> The research-critical mechanism and evaluation infrastructure have been implemented and frozen sufficiently to permit a controlled empirical test. The decisive B2-vs-B3 comparative evidence remains pending external model execution and independent human review.

That distinction must remain intact in the report and defense.
