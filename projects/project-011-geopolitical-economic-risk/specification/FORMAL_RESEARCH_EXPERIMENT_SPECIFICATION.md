# P003 (canonical; legacy directory P011) — Formal Research & Experiment Specification

## Control
- Canonical portfolio ID: **P003**
- Project: **Geopolitical Risk → Economic Impact Forecasting & Warning System**
- Legacy repository directory: `project-011-geopolitical-economic-risk`
- Specification status: **RESEARCH GATE LOCKED / READY TO PARK**
- Implementation authorization: **NO**
- Primary contribution hypothesis: **Economic Transmission Evidence Contract (ETEC)**

## 1. Research objective
Evaluate whether a domain-specific evidence contract can reduce unsupported geopolitical-to-economic claims while preserving useful Nigeria-specific warnings. P003 does not claim superior universal forecasting. It tests whether explicit evidence requirements can govern how a claim progresses from an event to exposure, domestic transmission, a bounded scenario, and—only where independently justified—a quantitative estimate.

## 2. Core invariant
**The maximum strength of an economic claim is capped by the weakest required evidentiary link.**

No narrative fluency, model confidence, news volume, or LLM output may override this rule.

## 3. ETEC claim ladder
1. `EVENT_VERIFIED`
2. `EXPOSURE_MEASURED`
3. `TRANSMISSION_SUPPORTED`
4. `SCENARIO_SUPPORTED`
5. `MODEL_ESTIMATE_ELIGIBLE`
6. `CALIBRATED_FORECAST`

Failure of a required transition terminates progression or returns a weaker claim class. Stages may not be skipped.

## 4. Evidence object schema
Every accepted evidence object must record at minimum:
- `evidence_id`
- `evidence_type`
- `source_id`
- `source_authority_tier`
- `source_url_or_dataset_reference`
- `publication_or_observation_time`
- `retrieval_time`
- `information_vintage`
- `country_scope`
- `product_or_classification_scope`
- `sector_or_consumer_scope` where applicable
- `claim_supported`
- `direction` (`supports`, `weakens`, `contradicts`, `context_only`)
- `valid_from` / `valid_until` where applicable
- `method_or_model_reference`
- `uncertainty_or_limitations`
- immutable/hash snapshot reference where practical for experiments.

Unknown fields that matter to admissibility must remain UNKNOWN rather than be silently imputed.

## 5. Transition contracts
### T1 — Event → EVENT_VERIFIED
Admissible evidence: authoritative government/regulator/international-organization announcement or independently corroborated high-quality reporting where no authoritative source is available.

Required: event identity, actor, action, scope, effective/announcement date, affected product/entity/route where relevant, provenance, and status.

Failure/contradiction: `CONTESTED_EVENT` or abstain.

### T2 — EVENT_VERIFIED → EXPOSURE_MEASURED
Admissible evidence: compatible trade/exposure observations, primarily product/partner trade data for the prototype.

Required: target country, compatible product classification, reporter/partner/flow, period/vintage, exposure measure and denominator. Direct exposure must not be presented as total upstream exposure.

Failure: stop at verified event and report exposure unavailable/insufficient.

### T3 — EXPOSURE_MEASURED → TRANSMISSION_SUPPORTED
Admissible evidence: documented concordance, input-output/use relationship, published sector evidence, or another explicit economic linkage.

Required: source product, destination sector/category, mapping method, applicability period/geography, limitations.

Failure: stop at exposure. An LLM may explain the missing evidence but may not create the edge.

### T4 — TRANSMISSION_SUPPORTED → SCENARIO_SUPPORTED
Required: economically supported direction/mechanism plus evaluation of material counterevidence. The scenario must state horizon and assumptions.

Failure: return transmission evidence without downstream directional claim.

### T5 — SCENARIO_SUPPORTED → MODEL_ESTIMATE_ELIGIBLE
Required: independently specified model with matching target variable, regime, horizon and input definitions; documented training/estimation data; validation procedure; applicable uncertainty.

Failure: scenario only. No numerical magnitude.

### T6 — MODEL_ESTIMATE_ELIGIBLE → CALIBRATED_FORECAST
Required: out-of-sample or time-respecting validation sufficient for the stated forecast claim, plus uncertainty/calibration evidence.

Failure: retain model estimate/research output but prohibit calibrated-forecast label.

## 6. Edge state model
Each pathway edge has one of:
- `VERIFIED`
- `SUPPORTED`
- `CONDITIONAL`
- `CONTESTED`
- `STALE`
- `INSUFFICIENT`
- `CONTRADICTED`

Counterevidence is not commentary. It can change an edge state and must trigger recomputation of dependent claims.

Examples:
- alternative-source diversification may weaken an exposure/risk edge;
- an exemption/reversal may invalidate an event scope;
- a stale trade observation may downgrade exposure confidence;
- a regime change may invalidate model eligibility.

## 7. Source hierarchy
Prototype source priority:
1. authoritative legal/policy issuers and official statistics;
2. international statistical organizations and central banks;
3. peer-reviewed/reputable academic evidence for mechanisms/models;
4. high-quality independent reporting for event corroboration/context;
5. commercial/open-source intelligence as supplementary evidence;
6. model/LLM inference only as a proposal/explanation layer, never primary evidence for a required economic edge.

Source count is not authority. Syndicated duplicates must not be treated as independent corroboration.

## 8. Prototype data plan
Primary data families:
- **UN Comtrade:** Nigeria goods trade by reporter/partner/flow/period/HS product. Preserve query parameters, classification edition, retrieval date and a frozen result snapshot. Note that Comtrade data can be revised, so reproducible experiments cannot rely only on a later live query.
- **CBN:** exchange-rate and relevant macro/external-sector series. Preserve exact series definitions and FX regime context.
- **Nigeria CPI/statistical material:** preserve CPI methodology/vintage and COICOP mapping; expenditure weights indicate relevance, not causal pass-through.
- **Sector linkage evidence:** documented Nigerian input-output/use relationships and explicit concordances. Do not invent HS→industry→COICOP mappings.
- **Commodity/event data:** authoritative policy-event sources and commodity/freight series where the selected case requires them.

Private inventories, contracts, hedges and supplier qualification are UNKNOWN unless credible evidence is available.

## 9. Concordance strategy
Mappings must be explicit transformations, not free-text semantic guesses.

Target chain where evidence permits:
`HS product → industry/activity classification → Nigerian sector/use relationship → COICOP/consumer category`

Every mapping records source taxonomy/version, mapping type (`direct`, `many_to_one`, `one_to_many`, `manual_reviewed`), confidence/ambiguity and reviewer decision. Ambiguous mappings cannot support magnitude claims without review.

## 10. Historical case-selection protocol
Select 3–5 cases only after a case manifest confirms:
- authoritative event date and scope;
- plausible affected product/route identifiable before outcome observation;
- Nigeria exposure data available around the information cutoff;
- at least one measurable outcome or expert/econometric comparator;
- sufficient historical evidence to reconstruct what was knowable at the time;
- diversity across transmission mechanisms;
- at least one negative control.

Candidate families remain:
A. Russia/Ukraine-related fertilizer/grain/energy restrictions/disruptions;
B. oil/geopolitical shock with competing Nigerian channels;
C. Red Sea/shipping disruption;
D. strategic export-control/tariff shock;
E. high-news-intensity negative control with negligible relevant Nigerian exposure.

Case selection must not be based on which cases make ETEC look successful.

## 11. Time-respecting replay
Each case receives an `information_cutoff`. Only evidence published/observable by that cutoff may enter the simulated warning. Later observations are outcome/evaluation data only.

Because upstream datasets may be revised, experiments must freeze retrieved data and metadata used during the replay. If the historically published vintage cannot be recovered, that limitation must be reported and sensitivity-tested rather than concealed.

## 12. Baselines
- **B0 News/GPR:** geopolitical/news-intensity signal without Nigerian evidence chain.
- **B1 Event+Exposure:** verified event and direct Nigeria exposure, no downstream evidence contract.
- **B2 LLM/RAG Explanation:** same retrieved evidence supplied to a language model instructed to explain Nigerian consequences; measures persuasive unsupported inference.
- **B3 ETEC:** full transition contracts, provenance, counterevidence and structural abstention.
- **B4 optional econometric/model baseline:** only for cases with an applicable validated quantitative model.

All baselines receive equivalent information cutoffs where technically possible.

## 13. Primary metrics
Primary:
- unsupported downstream claim rate;
- correct structural-abstention rate;
- false local-warning rate on negative controls;
- provenance completeness;
- event/exposure verification precision;
- counterevidence sensitivity;
- contradiction-handling correctness;
- claim-strength calibration against expert/econometric evidence;
- reproducibility from frozen evidence.

Secondary:
- pathway coverage;
- time to warning;
- user comprehension;
- directional outcome agreement when direction is admissible;
- magnitude error only when T5/T6 eligibility is satisfied.

## 14. Acceptance / kill thresholds
Exact statistical confidence intervals will depend on final case/sample size, but the following pre-implementation gates are locked:

### Mandatory acceptance conditions
- **0 tolerance** for knowingly skipped mandatory ETEC transitions in deterministic tests.
- **0 tolerance** for a numerical magnitude generated when T5 is not satisfied.
- **100% expected abstention** on engineered missing-link unit/integration fixtures.
- **100% expected recomputation** in deterministic counterevidence and staleness fixtures.
- **100% provenance linkage** for evidence objects used to release a claim in the controlled prototype tests.
- In historical cases, B3 must show a lower unsupported downstream-claim rate than B2; otherwise the central reliability contribution is not demonstrated.
- Negative-control false local warnings must not exceed the simpler B1/B2 baselines; a failure to improve warrants reframe/park.

### Kill/reframe conditions
Reframe or kill ETEC as the principal contribution if:
- expert reviewers cannot reproducibly determine whether required links are satisfied;
- ETEC does not reduce unsupported downstream claims versus B2;
- structural abstention removes so much useful coverage that the system provides no meaningful decision support;
- concordance/data quality makes target-country transmission mostly arbitrary;
- counterevidence cannot materially change dependent outputs;
- time-respecting replay cannot be reproduced from available data;
- a directly comparable prior system is found implementing substantially the same domain contract and evaluation contribution.

## 15. Falsification suite
- **F1 Missing-link:** remove product→sector mapping; expected stop at exposure.
- **F2 Counterevidence reversal:** add credible diversification/mitigation; expected dependent downgrade/recompute.
- **F3 Contradictory event:** conflicting authoritative evidence; expected contested state/reduced claim strength.
- **F4 Staleness:** expire time-sensitive evidence; expected recomputation/withholding.
- **F5 LLM temptation:** persuasive narrative but missing required edge; expected abstention.
- **F6 Negative control:** dramatic global event but negligible relevant Nigerian exposure; expected no material local warning.
- **F7 Model-eligibility trap:** provide scenario evidence but no applicable validated magnitude model; expected no number.
- **F8 Revision/vintage trap:** change a later data revision; expected historical replay remains tied to frozen experimental evidence rather than silently changing.

## 16. Security threat model
Assets: evidence integrity, policy/transition rules, frozen datasets, provenance, API credentials, reviewer decisions and experiment results.

Threats:
- fabricated/manipulated news;
- duplicate/syndicated reports masquerading as corroboration;
- prompt injection in retrieved content;
- event/product/country identifier tampering;
- stale/revised data silently changing results;
- unauthorized mutation of evidence/transition states;
- API credential leakage;
- resource exhaustion/external API abuse;
- LLM hallucination promoted to evidence;
- malicious concordance/mapping changes.

Required controls before any live prototype claim:
- server-authoritative validation and transition logic;
- source authority tiers/allowlists for official event verification;
- untrusted-content isolation;
- least-privilege credentials and secrets outside source;
- rate/resource limits, timeouts and explicit provider failure states;
- provenance/audit log for accepted evidence and state changes;
- versioned mappings/rules/datasets;
- no automated trading or consequential financial action;
- human review for ambiguous mappings and contested consequential claims.

## 17. Reproducibility package
Every historical experiment must be reproducible from:
- case manifest;
- information cutoff;
- frozen evidence/data snapshots or hashes;
- dataset/query metadata;
- taxonomy/concordance versions;
- ETEC rules/version;
- baseline configuration;
- model/provider/version if B2 or B4 uses one;
- random seeds where applicable;
- expected/observed outputs;
- evaluation labels and reviewer protocol.

## 18. First implementation scope — only if later authorized
If P003 is selected after portfolio comparison:
- Python-first backend;
- Nigeria only;
- bounded event types: sanctions, export restrictions, tariffs, major trade-route disruptions;
- bounded HS product set selected for data quality;
- deterministic ETEC engine before optional LLM assistance;
- historical replay before live monitoring;
- server-rendered/lightweight web UI unless complexity later justifies heavier frontend;
- SQLite/PostgreSQL selected at architecture stage based on deployment needs;
- no universal price predictor;
- no automated investment/trading advice.

This section is a scope boundary, **not implementation authorization**.

## 19. Research gate
**P003 STATUS: FORMAL SPECIFICATION COMPLETE — PARK FOR PORTFOLIO COMPARISON.**

Research has established a bounded, falsifiable contribution candidate and a feasible evaluation path. Further broad novelty searching is lower-value than comparing P003 against the other portfolio candidates. Implementation remains prohibited until AJ explicitly selects/authorizes the project after portfolio review.

## 20. Next portfolio action
Proceed to **P004 — Internet Compression & Optimization Proxy**, beginning with Pass 001: historical lineage, problem legitimacy, modern protocol constraints, existing products/open-source systems, and direct novelty threats. No P004 implementation before its research gate.