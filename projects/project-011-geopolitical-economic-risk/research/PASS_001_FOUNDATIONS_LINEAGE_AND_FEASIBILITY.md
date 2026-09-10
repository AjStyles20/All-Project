# P003 (canonical; legacy directory P011) — Pass 001: Foundations, Lineage and Feasibility

## Control
- Canonical portfolio ID: **P003**
- Legacy repository directory: `project-011-geopolitical-economic-risk`
- Project: Geopolitical Risk → Economic Impact System
- Stage: DISCOVERY / FOUNDATIONS / PRIOR-ART THREAT MAPPING
- Implementation authorization: **NO**
- Decision: **MORE RESEARCH — HIGH-POTENTIAL, HIGH-CAUSALITY-RISK CANDIDATE**

## 1. User-originated aim
Monitor national and global political events—tariffs, sanctions, elections, export restrictions, conflict and related shocks—and warn users about plausible downstream economic effects in their own country, such as price pressure, shortages, trade disruption and currency effects.

## 2. First falsification result
The broad claim `geopolitical events affect economies and can be measured/forecast` is established prior art. It cannot be the contribution.

Established lines include:
- newspaper-derived geopolitical-risk indices;
- macroeconomic impulse-response analysis of geopolitical shocks;
- sanctions and tariff models;
- multi-country/multi-sector input-output and general-equilibrium propagation;
- supply-chain vulnerability/risk ranking;
- commodity/energy-market event monitoring and forecasting;
- country/region-specific geopolitical-risk indices.

Therefore P003 must not become a generic news sentiment dashboard or a GPR-index clone.

## 3. Historical and methodological anchors
### 3.1 Geopolitical Risk Index
Caldara and Iacoviello's GPR framework counts newspaper coverage of adverse geopolitical events/tensions and has a long historical series. This establishes automated media-derived geopolitical-risk measurement as prior art.

### 3.2 Economic transmission is established
Federal Reserve analysis of the Russia–Ukraine war links elevated geopolitical risk to weaker global activity and higher inflation, alongside commodity and financial-market disruption.

### 3.3 Sanctions/trade shocks can be propagated structurally
Published work uses multi-country, multi-sector models with input-output and multinational-production linkages to quantify sanctions. Other recent work models geopolitical risk and sanctions as productivity/import-price or tariff shocks. This means `event -> economic model -> quantified effect` is also not novel in the abstract.

### 3.4 Country specificity matters
Recent euro-area work shows that a global/US-centric geopolitical-risk index can understate region-specific risk and economic effects. Country/region-local perception and exposure therefore cannot safely be inferred from one global score.

## 4. Key conceptual distinction
P003 must separate four layers:

1. **Observed event** — what is credibly known to have happened or been announced.
2. **Exposure** — how the target country/sector depends on affected countries, products, routes, currencies, finance or commodities.
3. **Transmission mechanism** — the economically plausible pathway (trade cost, import restriction, commodity supply, shipping disruption, financial channel, expectations, etc.).
4. **Outcome/scenario** — estimated or forecast price, availability, output, inflation, FX or sector effects with uncertainty and time horizon.

An LLM-generated narrative must never collapse these layers into an unsupported causal statement.

## 5. Candidate architecture concept — Economic Impact Pathway Graph (research hypothesis)
Represent each warning as a provenance-bearing pathway rather than a headline sentiment score.

Candidate node types:
- geopolitical event;
- actor/country;
- policy instrument (tariff, sanction, quota, export ban, capital restriction);
- commodity/product;
- trade partner;
- transport route/chokepoint;
- domestic sector;
- imported intermediate;
- exchange-rate/financial variable;
- consumer category;
- observed economic indicator;
- forecast/scenario.

Candidate edges:
- TARGETS;
- RESTRICTS_EXPORT_OF;
- RAISES_TRADE_COST_OF;
- SUPPLIES;
- IMPORT_DEPENDENT_ON;
- INPUT_TO;
- ROUTED_THROUGH;
- EXPOSES;
- MAY_PRESSURE_PRICE_OF;
- MAY_REDUCE_AVAILABILITY_OF;
- MAY_PRESSURE_CURRENCY_VIA;
- SUPPORTED_BY;
- CONTRADICTED_BY.

Every inferential edge requires evidence type, provenance, confidence/uncertainty and horizon.

Novelty status: **UNKNOWN**. Knowledge graphs, supply-chain graphs and causal/economic networks are established; the exact user-facing event-to-country pathway representation requires adversarial prior-art search.

## 6. Why a single GPR score is insufficient
Aggregate GPR indices are useful research indicators but do not identify all event-specific downstream pathways. Region-specific research also shows geographic/media perspective matters. A user asking `What could this tariff do to food prices in Nigeria?` needs exposure and mechanism evidence, not merely a global risk index value.

## 7. Candidate contribution hypotheses
### H1 — Country-Specific Event-to-Impact Pathway
Given a verified geopolitical event and a target country, construct an auditable pathway through trade/supply/financial exposure to bounded downstream economic scenarios.

Threat: supply-chain risk platforms, economic models and knowledge-graph systems may already do this.

### H2 — Evidence-Calibrated Warning Rather Than Point Prediction
Produce warnings whose strength depends on event credibility, exposure evidence, mechanism support, historical/model evidence and horizon; preserve disagreement and missing links.

Threat: scenario-analysis/risk-intelligence products may already provide uncertainty and analyst reasoning.

### H3 — Localized Downstream Relevance
Translate upstream geopolitical shocks into target-country/sector/household-relevant categories (e.g. imported fuel, fertilizer, wheat, electronics, transport inputs) using measurable exposure rather than generic global sentiment.

Threat: trade vulnerability and input-output models already localize shocks quantitatively.

### H4 — Forecast-versus-Scenario Separation
Where causal identification is weak, return scenarios rather than fake forecasts. Distinguish conditional `if X persists and exposure remains Y` from statistically validated prediction.

This may be primarily a trustworthiness/product architecture rather than standalone novelty.

## 8. Strong novelty threats found immediately
- GPR measurement is mature prior art.
- Sanctions/tariff macroeconomic modeling is mature.
- Global value-chain/input-output shock propagation is mature.
- Country/sector vulnerability ranking exists.
- Commodity/energy geopolitical monitoring with NLP/LLMs exists.
- Region-specific GPR measurement exists.

Therefore none of those features alone can justify P003.

## 9. Causality guardrails
The project must not infer `event caused outcome` merely because:
- they co-occurred;
- news sentiment changed first;
- a commodity price moved after an event;
- an LLM generated a plausible story;
- historical correlation is positive.

Required labels:
- VERIFIED EVENT;
- VERIFIED EXPOSURE;
- SUPPORTED MECHANISM;
- REASONED SCENARIO;
- MODEL ESTIMATE;
- FORECAST;
- UNKNOWN/INSUFFICIENT EVIDENCE;
- CONTRADICTED.

## 10. Data families to investigate
- official sanctions/tariff/export-control sources;
- GDELT/news event feeds, with source-quality controls;
- UN Comtrade / BACI / WTO / World Bank trade data;
- OECD inter-country input-output data where licensing/access permits;
- commodity and energy price series;
- exchange-rate, CPI/PPI and macro indicators;
- shipping/chokepoint/route data where feasible;
- country-specific import dependency and sector input structure;
- historical geopolitical event datasets.

No source should be assumed available/licensed until verified.

## 11. Feasibility tiers
### Tier A — defensible prototype
- bounded event taxonomy (e.g. sanctions, tariffs, export restrictions, conflict-driven trade disruption);
- one target country initially;
- selected commodities/sectors;
- verified public data;
- pathway/scenario engine;
- historical backtests/case studies;
- no claim of universal economic forecasting.

### Tier B — broader research system
- multiple countries;
- richer input-output/trade network;
- probabilistic forecasts where validated;
- automated event extraction/entity resolution;
- continuously updated exposure graph.

Tier B should not be attempted until Tier A research shows measurable value.

## 12. Evaluation skeleton
Historical-event backtests should ask:
- Was the event identified correctly and at the correct time?
- Was the affected country/product/sector exposure identified?
- Were proposed transmission mechanisms economically defensible?
- Did the system distinguish direct from indirect exposure?
- Were predicted directions/time horizons calibrated?
- Did uncertainty increase when evidence was missing/conflicting?
- How often did warnings become false alarms?
- How does the pathway approach compare with a simple GPR/sentiment baseline?
- How does it compare with trade-exposure-only baselines?

Candidate cases should include different mechanisms, not only wars.

## 13. Security/misinformation requirements
- News/event text is untrusted input.
- Multiple-source corroboration or authoritative-source precedence is required for consequential event claims.
- Prompt injection in retrieved articles must not alter system policy/tool behavior.
- Source timestamps, revisions and retractions must be preserved.
- User-visible pathways must expose provenance.
- Forecast outputs must not be presented as financial advice or certainty.
- Manipulated/duplicated media coverage must not mechanically amplify risk scores.

## 14. Kill/reframe criteria
Reframe or demote if:
1. direct prior art already provides auditable event→exposure→mechanism→localized impact pathways with comparable uncertainty;
2. required trade/input-output data cannot support target-country resolution;
3. historical backtests cannot beat simple exposure/GPR baselines on useful warning quality;
4. event extraction uncertainty dominates the pipeline;
5. causal claims cannot be bounded without turning the system into generic news summarization;
6. the system's apparent intelligence comes mainly from LLM narrative generation rather than measurable economic evidence.

## 15. Next pass
**Pass 002 — Direct Prior-Art Attack on Event-to-Country Economic Impact Pathways.**

Search:
- geopolitical risk intelligence platforms;
- supply-chain geopolitical risk graphs;
- sanctions/tariff propagation systems;
- event knowledge graphs for economic forecasting;
- country-specific commodity/import vulnerability;
- GDELT + trade network economic prediction;
- causal/event-driven macro forecasting;
- commercial products (Bloomberg/Refinitiv/S&P/Prewave/Everstream/Interos and others only after verified);
- open-source repositories and datasets.

Build a matrix distinguishing:
- event detection;
- source verification;
- exposure mapping;
- transmission mechanism;
- country localization;
- sector/household localization;
- causal identification;
- scenario vs forecast;
- uncertainty;
- provenance;
- historical validation.

## 16. Decision
**MORE RESEARCH — HIGH-POTENTIAL, HIGH-CAUSALITY-RISK CANDIDATE.**

The project survives Pass 001, but not as a generic geopolitical-risk predictor. The strongest current direction is an evidence-grounded, country-specific **event → exposure → transmission mechanism → bounded impact scenario** system whose uncertainty and provenance remain visible.