# P003 (canonical; legacy directory P011) — Pass 005: Data Feasibility, Historical Backtest Design and Decisive Contribution Test

## Control
- Canonical portfolio ID: **P003**
- Legacy repository directory: `project-011-geopolitical-economic-risk`
- Stage: DATA FEASIBILITY / EVALUATION DESIGN / DECISIVE RESEARCH GATE
- Implementation authorization: **NO**
- Decision: **CONDITIONAL GO TO FORMAL SPECIFICATION — RESEARCH CONTRIBUTION TESTABLE, BUT MAGNITUDE FORECASTING MUST REMAIN OPTIONAL**

## 1. Decisive question
Can the surviving Economic Transmission Evidence Contract (ETEC) be instantiated and empirically tested with real Nigerian economic data without relying on an LLM to invent missing causal links?

Pass 005 finds that the answer is **yes for an evidence-gated scenario/decision-support prototype**, but **not uniformly yes for high-resolution quantitative forecasting**. The available data are sufficient to test event verification, trade exposure, sector linkage, provenance, structural abstention, counterevidence and bounded scenario generation. They are not sufficient to justify universal product-to-household point forecasts.

## 2. Verified data feasibility
### 2.1 International trade exposure — FEASIBLE
UN Comtrade exposes goods trade by reporter, partner, flow, period, classification and commodity code, including HS classifications and annual/monthly frequencies where reported. This is sufficient for reproducible measures such as:
- Nigeria import value by HS product and partner;
- partner concentration;
- source-country share;
- pre/post-event trade diversion;
- alternative-source evidence;
- event-product exposure checks.

Limitations: reporting lags, revisions, classification-version mapping, missing monthly detail for some observations, and the need to distinguish direct imports from deeper upstream dependencies.

### 2.2 Exchange rates and macro series — FEASIBLE
The Central Bank of Nigeria publishes exchange rates and a statistics database spanning external, monetary, fiscal and real-sector series. This supports historical FX context and selected macroeconomic outcome validation.

Caution: official FX regime changes and multiple historical market rates mean series definitions must be versioned; the system must not splice incompatible regimes without documentation.

### 2.3 Consumer prices / household relevance — FEASIBLE WITH VERSIONING
Nigeria's CPI was rebased using updated expenditure information. Current official/statistical material reports a 2023 weight reference period, 2024 price reference period and COICOP 2018 structure with 13 divisions and 934 product varieties. This makes household-category relevance testable.

Critical rule: CPI weights indicate expenditure importance; they are **not pass-through coefficients**. A high basket weight cannot justify a large event impact estimate.

Historical backtests spanning a rebasing boundary must preserve the CPI vintage/methodology applicable at the time rather than pretending the series is structurally unchanged.

### 2.4 Domestic sector transmission — FEASIBLE AT COARSER RESOLUTION
Published Nigerian input-output work demonstrates that a symmetric input-output representation can be constructed and used to identify backward/forward sector linkages. Reported key sectors include crop/animal production, food manufacturing, refined petroleum, chemicals, transport and others.

This supports sector-level transmission experiments, but it does not automatically provide a current, high-frequency HS-code-to-household transmission matrix. Mapping from traded product to domestic industry and then consumer category remains a controlled modelling step requiring explicit concordances and provenance.

### 2.5 Inventory, substitution and route counterevidence — PARTIAL
Alternative suppliers can be approximated from trade-partner diversification and observed post-event trade diversion. Some commodity, route and policy evidence is publicly available. However, real-time private inventories, firm contracts, supplier qualification, hedges and proprietary logistics exposure are often unavailable.

Therefore absence of mitigation evidence must be represented as **UNKNOWN**, not as zero mitigation.

## 3. Data feasibility verdict by ETEC transition
| Transition | Feasibility | Maximum defensible default |
|---|---|---|
| Event -> verified policy/shock | HIGH for sanctions, tariffs, export controls and official actions with authoritative sources | VERIFIED EVENT |
| Event -> Nigerian trade exposure | HIGH for HS-level direct trade where Comtrade data exist | VERIFIED/MEASURED EXPOSURE |
| Trade product -> Nigerian domestic sector | MEDIUM | SUPPORTED SECTOR LINK, provenance required |
| Sector -> consumer/CPI category | MEDIUM | SUPPORTED RELEVANCE, not magnitude |
| Exposure -> price/output magnitude | LOW-MEDIUM and shock-specific | MODEL ESTIMATE only where a validated model exists |
| Counterevidence from alternative suppliers | MEDIUM | MEASURED DIVERSIFICATION / observed substitution |
| Counterevidence from inventories/contracts | LOW from public data | UNKNOWN unless sourced |
| Point forecast of household price impact | LOW as a universal feature | ABSTAIN by default |

## 4. ETEC formal claim ladder
The prototype must enforce a monotonic evidence contract:

1. **EVENT VERIFIED** — authoritative evidence establishes the event.
2. **EXPOSURE MEASURED** — target-country/product exposure is measured with compatible trade data.
3. **TRANSMISSION SUPPORTED** — a documented economic linkage connects exposure to a domestic sector/category.
4. **SCENARIO SUPPORTED** — direction/mechanism is supported, with counterevidence disclosed.
5. **MODEL ESTIMATE ELIGIBLE** — a validated model exists for the relevant variable, horizon and regime.
6. **CALIBRATED FORECAST** — only after out-of-sample validation supports forecast claims.

A claim may not skip a required stage. If a required stage fails, the pathway terminates or returns a weaker class.

**Weakest-link rule:** the maximum output strength is capped by the weakest required evidentiary link.

## 5. Historical backtest design
Backtests must be **time-respecting**. The system may use only evidence that would have been available by the simulated decision date. Later outcome data are used only for evaluation.

### Candidate case family A — Russia/Ukraine shock and trade restrictions (2022 onward)
Test channels such as fertilizer, wheat/grains, energy/freight and selected imported inputs. Questions:
- Did the system verify the relevant restriction/disruption rather than infer it from headlines?
- Was Nigeria materially exposed to the affected product/source at that time?
- Did alternative suppliers or trade diversion weaken the pathway?
- Did the system stop before unsupported household magnitude claims?

### Candidate case family B — global oil/geopolitical shock
Nigeria is both oil-export exposed and domestically vulnerable to fuel/FX/fiscal transmission. This is a useful adversarial case because a naive system may assume higher oil prices are simply beneficial or harmful. ETEC must represent competing channels rather than collapse them into one sentiment score.

### Candidate case family C — Red Sea / shipping disruption (2023–2024)
Test freight/route exposure and whether evidence supports a Nigeria-specific downstream pathway. This is a strong abstention case if route-level or product-level exposure cannot be established.

### Candidate case family D — export-control / tariff shock affecting a strategic traded input
Select an event with an authoritative announcement and observable HS-level trade exposure. Prefer cases where alternative supplier data are measurable so counterevidence can be evaluated.

### Candidate case family E — negative-control event
Include at least one highly publicized geopolitical event for which Nigeria has little measurable exposure to the affected product/channel. A good system should **not** manufacture a local warning merely because global news intensity is high.

Final case selection requires a separate case manifest recording event date, authoritative event source, affected products/actors, information cutoff, datasets and expected evaluation window.

## 6. Baselines
- **B0 — News/GPR baseline:** geopolitical-news intensity or generic risk signal with no explicit Nigerian exposure chain.
- **B1 — Event + exposure:** verified event plus direct Nigerian trade exposure, without evidence-contract gating downstream.
- **B2 — LLM/RAG explanation:** retrieved evidence supplied to an LLM asked to explain likely Nigerian effects; this baseline tests persuasive unsupported inference.
- **B3 — ETEC:** evidence-contract progression, counterevidence, provenance and structural abstention.

Optional B4: conventional econometric/model baseline for cases where a validated outcome model exists. B4 is not required for every shock.

## 7. Primary evaluation metrics
The contribution should be judged primarily on **epistemic reliability**, not on producing the largest number of predictions.

Primary metrics:
- unsupported downstream claim rate;
- correct abstention rate on deliberately incomplete pathways;
- false local-warning rate on negative controls;
- provenance completeness;
- event/exposure verification precision;
- counterevidence sensitivity (does new mitigating evidence actually downgrade dependent conclusions?);
- contradiction handling;
- claim-strength calibration against expert/econometric evidence;
- reproducibility from frozen data snapshots.

Secondary metrics:
- time to warning;
- pathway coverage;
- user comprehension of why a warning was issued or stopped;
- directional outcome agreement where a directional scenario is justified;
- magnitude error only for cases explicitly eligible for model estimation.

## 8. Falsification experiments
### F1 — Missing-link test
Remove the product-to-sector mapping while leaving event and exposure evidence intact. Expected ETEC behavior: stop at exposure. Failure: downstream sector/consumer claim appears anyway.

### F2 — Counterevidence reversal test
Introduce credible alternative-supplier/diversification evidence after an exposure warning. Expected: dependent pathway weakens/recomputes. Failure: original warning remains unchanged.

### F3 — Contradictory-source test
Provide conflicting authoritative evidence about event scope/status. Expected: pathway becomes contested and claim strength falls. Failure: system silently chooses whichever source supports the warning.

### F4 — Staleness test
Expire a time-sensitive exposure/mitigation observation. Expected: affected edge becomes stale and downstream conclusions are recomputed or withheld.

### F5 — LLM temptation test
Provide retrieved text that strongly suggests an economic narrative but lacks a required quantitative/structural link. Expected: ETEC abstains at the missing edge even if the LLM can write a plausible continuation.

### F6 — Negative-control geopolitical event
Use a high-news-intensity event with negligible measured Nigerian exposure. Expected: no material local-impact warning.

## 9. Security / evidence integrity requirements before implementation
ETEC depends on evidence integrity, so the prototype must treat external text and feeds as untrusted.

Minimum requirements:
- source allowlists/authority tiers for legal-policy event verification;
- retrieved content cannot modify system rules or tool permissions;
- duplicate/syndicated news does not count as independent corroboration;
- immutable or hash-addressed evidence snapshot references for experiments where practical;
- server-side validation of event/product/country identifiers;
- provenance for every accepted edge;
- explicit timestamp and data-vintage metadata;
- contradiction and retraction handling;
- secrets outside source control;
- least-privilege external API credentials;
- resource/rate limits and external-service timeout handling;
- no consequential automated trading/investment action in the research prototype.

## 10. What Pass 005 kills
The following project descriptions are now rejected:
- `AI predicts how geopolitical events affect Nigeria` — too broad and overclaims causality.
- universal household-price prediction — unsupported by available data/model coverage.
- one global geopolitical score mapped directly to Nigerian outcomes — invalid localization.
- LLM-generated causal chains as evidence — unacceptable.
- treating missing inventory/substitution evidence as absence of mitigation — invalid.
- treating CPI weights as shock coefficients — invalid.

## 11. Surviving contribution candidate
### Economic Transmission Evidence Contract (ETEC)
A domain-specific evidence contract for geopolitical-to-economic decision support that constrains progression from verified event to measured exposure, supported domestic transmission, local scenario and quantitative estimate. Each transition has explicit admissibility/provenance requirements; counterevidence can invalidate or downgrade dependent conclusions; missing required links cause structural abstention; and output strength cannot exceed the weakest required evidence state.

This is still a **bounded research contribution hypothesis**, not a claim that no comparable system exists anywhere.

## 12. Decisive research-gate result
ETEC passes the **feasibility/testability gate** for a prototype because:
1. authoritative geopolitical/policy events can be frozen and verified;
2. HS-level Nigerian trade exposure can be measured with public international trade data;
3. CBN provides exchange-rate and macroeconomic series;
4. Nigeria's CPI structure permits household-category relevance analysis when methodology/vintage are preserved;
5. published Nigerian input-output work demonstrates sector linkage modelling is possible;
6. negative controls, missing-link tests and counterevidence tests do not require perfect forecasting data;
7. the central hypothesis can therefore be falsified empirically.

The gate is **conditional**, because detailed real-time inventories, proprietary supply chains and universal pass-through models are unavailable. The architecture must treat those as unknown rather than fabricate them.

## 13. Formal scope recommendation
For the first research prototype, restrict P003 to:
- Nigeria as target country;
- a bounded set of geopolitical economic events (sanctions/export restrictions/tariffs/major trade-route disruptions);
- a bounded HS product set chosen for data quality and economic relevance;
- sector/category scenario outputs;
- explicit counterevidence;
- structural abstention;
- historical replay/backtesting.

Do **not** make live investment advice, automated trading, universal commodity forecasting or arbitrary-event causal prediction part of the research contribution.

## 14. Next action
**GO TO FORMAL RESEARCH/EXPERIMENT SPECIFICATION, THEN PARK P003 FOR PORTFOLIO COMPARISON.**

The next document should lock:
- ETEC schema and transition contracts;
- evidence/source hierarchy;
- case-selection protocol;
- frozen historical information cutoffs;
- HS/industry/COICOP concordance strategy;
- B0–B3 baseline implementations;
- exact metrics and acceptance/kill thresholds;
- security threat model;
- reproducibility package.

No implementation should begin until that specification is approved.

## 15. Decision
**CONDITIONAL GO TO FORMAL SPECIFICATION.**

P003 is technically feasible as an evidence-bounded geopolitical-economic decision-support research prototype. Its defensible contribution is not superior geopolitical prediction; it is the testable discipline imposed on how economic impact claims are allowed to strengthen, weaken, or stop as evidence changes.