# P003 (canonical; legacy directory P011) — Pass 003: Local/Household Transmission, Counterevidence and Abstention

## Control
- Canonical portfolio ID: **P003**
- Legacy repository directory: `project-011-geopolitical-economic-risk`
- Stage: ADVERSARIAL GAP REVIEW / LOCAL TRANSMISSION / RELIABILITY
- Implementation authorization: **NO**
- Decision: **MORE RESEARCH — NARROWER EVIDENCE-GATED DIRECTION SURVIVES**

## 1. Research question
After Pass 002 removed generic event monitoring, exposure mapping, supply-chain graphs, sanctions propagation and country-risk scoring as contribution claims, this pass attacks the remaining idea: can P003 defensibly translate a verified geopolitical shock into locally relevant Nigerian/household scenarios while representing counterevidence and refusing unsupported causal links?

## 2. Falsification result
Three components are established prior art and therefore cannot individually constitute novelty:
1. macro/import-price/exchange-rate pass-through into Nigerian prices;
2. supply-chain mitigation through inventories, multi-sourcing, alternate suppliers/routes and resilience strategies;
3. selective prediction/abstention under uncertainty.

The surviving possibility is their **domain-specific composition into a provenance-bearing, evidence-gated transmission system**, but the novelty of that composition remains UNKNOWN and must not yet be claimed.

## 3. Nigeria-specific transmission evidence
Nigeria is a useful initial target because published work directly studies transmission from exchange rates and import prices to domestic prices.

Evidence reviewed includes CBN-hosted work finding incomplete exchange-rate pass-through into CPI, with pass-through higher at import prices and declining along the pricing chain. Recent threshold work reports nonlinear price responses to exchange-rate depreciation rather than one constant coefficient. This means P003 must not use a universal rule such as `10% FX shock -> X% household price increase`.

Required implication: transmission edges need model/source, period, target price category, horizon, uncertainty and applicability conditions.

## 4. Household localization is not a simple final edge
A country-level import shock does not automatically imply a household-level price shock. A defensible chain may require:

`event -> affected traded product -> Nigerian import exposure -> domestic intermediate/final-use mapping -> exchange-rate/freight/inventory/substitution conditions -> consumer category -> bounded scenario`

Potential local endpoints include food, transport, housing/energy, clothing, health and other consumer categories. Official CPI classifications/weights can support category relevance, but CPI weights are not causal pass-through coefficients.

Therefore `consumer basket weight` and `shock transmission coefficient` must remain separate concepts.

## 5. Counterevidence is mandatory
Supply-chain resilience literature establishes that disruption impact can be mitigated by stockpiling/inventory, multi-sourcing, capacity reservation, flexible contracts, backup suppliers and alternative shipment strategies. Consequently a warning engine that only accumulates adverse evidence is structurally biased.

Candidate counterevidence types:
- low measured import dependence;
- diversified source countries;
- qualified alternative suppliers;
- inventory/buffer stocks where credible data exist;
- alternative routes;
- policy exemptions or reversals;
- domestic substitution capacity;
- falling freight/input prices;
- event de-escalation or expiry;
- contradictory authoritative reports;
- historical/model evidence showing weak pass-through.

A pathway score, if later justified, must permit evidence to weaken, suspend or reverse a warning.

## 6. Abstention is not novel
Selective prediction and uncertainty-aware abstention are established ML/LLM research areas, including conformal/risk-controlled approaches. Therefore `the AI says I don't know` is not a contribution.

P003 should instead investigate **structural abstention**: refusal triggered by missing or unsupported economic pathway requirements, not merely by an LLM's self-reported confidence.

Candidate rule:
- no verified event -> no impact pathway;
- no measurable target-country exposure -> stop or return exposure unknown;
- no supported transmission mechanism -> stop before downstream claim;
- no valid magnitude model -> scenario direction only, no point estimate;
- conflicting evidence -> expose contradiction and reduce claim strength;
- stale evidence -> downgrade/recompute;
- unsupported household mapping -> stop at sector/category level.

This is a research hypothesis, not yet a novelty claim.

## 7. Evidence-gated pathway state machine
Candidate states for each edge:
- VERIFIED;
- SUPPORTED;
- CONDITIONAL;
- CONTESTED;
- STALE;
- INSUFFICIENT;
- CONTRADICTED.

Candidate pathway output classes:
- VERIFIED EVENT ONLY;
- EXPOSURE IDENTIFIED;
- MECHANISM-SUPPORTED SCENARIO;
- MODEL ESTIMATE;
- CALIBRATED FORECAST;
- ABSTAIN / INSUFFICIENT EVIDENCE.

The system must never promote a narrative inference into a stronger class merely because an LLM can produce a plausible explanation.

## 8. Threat matrix
| Candidate feature | Prior-art pressure | Status |
|---|---|---|
| Nigeria FX/import-price -> CPI transmission | Strong econometric prior art | NOT NOVEL |
| Household/CPI category mapping | Official statistics + inflation research | NOT NOVEL ALONE |
| Alternative suppliers/inventory mitigation | Mature supply-chain resilience literature/products | NOT NOVEL |
| AI abstention | Mature selective-prediction/UQ literature | NOT NOVEL |
| Provenance-bearing causal/transmission graph | Graph/provenance systems established | HIGH THREAT |
| Evidence-required edge progression | Needs direct domain prior-art attack | SURVIVES / UNKNOWN |
| Counterevidence that can downgrade an active geopolitical-economic warning | Needs direct prior-art attack | SURVIVES / UNKNOWN |
| Structural abstention based on missing economic links rather than model confidence | Needs direct prior-art attack | SURVIVES / UNKNOWN |
| Consumer-facing explanation of exactly where an event->local-impact chain breaks | Needs direct prior-art attack | SURVIVES / UNKNOWN |

## 9. Proposed contribution hypothesis after Pass 003
**Evidence-Gated Economic Transmission with Counterevidence-Aware Abstention**

Given a verified geopolitical event and target country, construct only those event -> exposure -> mechanism -> local-impact edges supported by typed evidence. Track counterevidence and mitigation on the same pathway. If a required link lacks sufficient support, terminate the chain at that point and explain what evidence is missing rather than generating a downstream causal narrative.

Novelty status: **UNKNOWN**.

## 10. Evaluation implications
A future prototype should not be evaluated only on prediction accuracy. Candidate metrics include:
- event verification precision;
- exposure identification precision/recall;
- mechanism support accuracy under expert/ground-truth review;
- unsupported-edge rate;
- false downstream-claim rate;
- abstention precision and coverage;
- warning calibration;
- counterevidence sensitivity;
- time-to-warning;
- direction accuracy where a model estimate is justified;
- provenance completeness;
- historical case-study reconstruction quality;
- comparison against GPR/sentiment-only and exposure-only baselines.

A useful system may deliberately produce fewer warnings if the accepted warnings are substantially better supported.

## 11. Data feasibility questions
Before architecture approval, verify availability, update frequency, licensing and resolution for:
- Nigeria trade/import data by product and partner;
- CPI/category definitions and weights;
- import/producer price indices;
- exchange-rate series;
- commodity prices;
- input-output/use tables sufficient to map imported intermediates to domestic sectors;
- inventory/buffer-stock evidence where relevant;
- shipping/freight/route data;
- authoritative tariff/sanction/export-control events.

Missing inventory or substitution data must not be silently imputed as certainty.

## 12. Security and manipulation threat
Evidence gating creates a new attack surface: an adversary could attempt to manufacture corroborating articles or poison retrieved evidence so that a pathway crosses its release threshold.

Research requirements:
- authoritative-source precedence for legal/policy events;
- source independence checks rather than raw article counts;
- duplicate/syndication detection;
- timestamp/revision/retraction tracking;
- prompt-injection isolation for retrieved text;
- provenance integrity;
- contradiction preservation;
- no tool/action authority granted to retrieved content.

## 13. Kill/reframe criteria added by this pass
Reframe or park the evidence-gated contribution if direct prior art already provides all of the following in a comparable economic/geopolitical system:
1. typed event->exposure->mechanism->local-impact pathways;
2. provenance per inferential edge;
3. explicit counterevidence/mitigation edges that downgrade warnings;
4. structural abstention when a required causal/economic link is missing;
5. user-visible explanation of the broken/missing link;
6. historical validation of warning quality.

Also reframe if Nigeria-relevant data cannot support the resolution required for meaningful local impact claims.

## 14. Next pass
**Pass 004 — Direct Prior-Art Attack on Evidence-Gated Causal Chains, Contradiction Handling and Structural Abstention.**

Search academic, commercial and open-source systems for:
- evidence graphs / argument graphs for economic intelligence;
- provenance-aware causal knowledge graphs;
- supply-chain risk systems with mitigation/counterevidence updates;
- contradiction-aware event intelligence;
- causal claim verification and evidence graphs;
- abstaining economic forecasting / selective forecasting;
- rule/evidence-gated decision support;
- consumer-facing economic shock explanation;
- provenance-aware GDELT/trade-network systems.

Pass 004 must try to kill the surviving composition rather than rename familiar components.

## 15. Decision
**MORE RESEARCH — NARROWER EVIDENCE-GATED DIRECTION SURVIVES.**

Pass 003 removes household localization, mitigation logic and abstention as standalone novelty claims. The remaining research target is the integration of typed economic evidence, counterevidence and structural abstention into an auditable event-to-local-impact pathway. This remains plausible but unverified as a contribution.