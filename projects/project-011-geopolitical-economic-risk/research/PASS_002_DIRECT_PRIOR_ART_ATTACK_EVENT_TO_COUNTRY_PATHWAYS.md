# P003 (canonical; legacy directory P011) — Pass 002: Direct Prior-Art Attack on Event-to-Country Economic Impact Pathways

## Control
- Canonical portfolio ID: **P003**
- Legacy repository directory: `project-011-geopolitical-economic-risk`
- Project: Geopolitical Risk → Economic Impact System
- Research stage: PRIOR-ART ATTACK / GAP REVIEW
- Implementation authorization: **NO**
- Decision after this pass: **MORE RESEARCH — PROMISING ONLY IF THE CONTRIBUTION IS NARROWER THAN ENTERPRISE SUPPLY-CHAIN EVENT IMPACT MAPPING**

## 1. Question attacked
Does P003 still have a defensible research contribution if current products and research already perform real-time geopolitical-event monitoring, supplier/network exposure mapping, sanctions/trade-risk scoring, disruption propagation, scenario simulation, and country/sector impact analysis?

## 2. Major result
The simple idea `detect geopolitical event -> map exposure -> warn affected users` is already substantially covered by existing commercial and research systems, especially in enterprise supply-chain risk.

The remaining opportunity, if any, must therefore be narrower and more rigorously defined. It likely cannot be claimed merely from:
- real-time geopolitical news monitoring;
- supply-chain graph mapping;
- sanctions or tariff exposure;
- country-level geopolitical risk scores;
- commodity risk analysis;
- alternative supplier recommendations;
- event-specific risk alerts;
- impact simulation;
- graph-based sanction propagation;
- AI/NLP extraction of geopolitical events.

## 3. Direct commercial prior-art threats

### 3.1 Interos
Interos markets a supply-chain risk intelligence platform that maps and monitors extended supplier networks and scores multiple risk classes, including geopolitical and restrictions risk. Its `itracing` positioning explicitly promises to show what is at risk and what it means for products, revenue, and compliance. It also advertises assessment of supplier/geographic concentration and sanctions/trade restrictions.

**Threat to P003:** very high for any claim framed as `external geopolitical event -> network exposure -> operational/business impact`.

### 3.2 Everstream Analytics
Everstream describes a platform that maps companies, locations, shipments, lanes, and materials, continuously monitors global events, and connects external events to the specific suppliers, sites, materials, products, and lanes relevant to a client. It combines AI/NLP, predictive modeling, analysts, and proprietary data, and advertises real-time alerting, risk assessment, and predictive supply-chain intelligence.

**Threat to P003:** extremely high for generic `event relevance to a user's supply chain` and `event -> affected material/site/lane` novelty claims.

### 3.3 Sayari
Sayari exposes corporate, ownership, trade, sanctions, export-control, forced-labor, and supply-chain relationships in a unified risk model. It emphasizes tracing risk through indirect ownership and supplier networks rather than screening only direct counterparties.

**Threat to P003:** high for network-based sanctions exposure, indirect supplier relationships, and compliance-oriented geopolitical risk pathways.

## 4. Open-source prior-art threats

### 4.1 GDELT itself
GDELT already provides a global event database and Global Knowledge Graph extracted from world news, including actors, locations, themes and contextual information. This makes `news -> structured geopolitical event graph` established infrastructure rather than a contribution.

### 4.2 SupplySeer
The open-source SupplySeer repository contains an experimental geopolitical-risk module and a GDELT monitor. The code defines queries for supply disruption, geopolitical conflict, infrastructure disruption, trade restrictions and natural disasters; it can monitor countries/commodities and analyze route/supply-chain risk. Its tutorial demonstrates conflict scenarios, affected commodities, sanctions, alternative sources, route risk, lead-time impact and cost-impact values.

Important limitation observed in the tutorial: some impact values and sanction parameters are manually supplied as scenario configuration. This means the existence of an `impact report` is not evidence that the numerical effects are empirically identified. That is relevant to P003's guardrail against invented precision.

### 4.3 World Monitor
World Monitor's current repository exposes country intelligence, sanctions scoring, chokepoint intelligence, strategic-product trade data, route exploration, scenario APIs, supply-chain country-product endpoints and multi-sector cost-shock functionality. Its changelog also documents methodology-versioning and cases where fabricated attribution was removed in favor of authoritative entity resolution.

**Threat to P003:** high. A public/open system already integrates geopolitical, trade, shipping, country-risk, commodity and scenario functionality. This materially weakens any novelty claim based on dashboard breadth or `global event + country/trade context` alone.

## 5. Academic prior-art threats

### 5.1 Bilateral conflict risk and trade
Recent work constructs monthly bilateral conflict indicators from GDELT and decomposes hostility into kinetic conflict, military posture, sanctions-context tensions and routine diplomacy, then estimates differentiated trade effects. This is a direct threat to simple event-type-specific trade-impact claims.

### 5.2 Sanctions and general-equilibrium / trade-network propagation
Published research simulates energy sanctions and countersanctions with multi-region economic models and quantifies changes in output, inflation and trade diversion. Other studies measure regional sanctions exposure from foreign-trade dependence and import concentration.

**Threat:** `sanction -> trade dependence -> macro/sector outcome` is established.

### 5.3 Geoeconomic graph models
A 2025/2026 geoeconomic intelligence paper proposes a directed weighted global trade graph with country-level economic, political and sentiment features, graph neural networks, sanction-impact simulation and friend-shoring prediction.

**Threat:** very high to any novelty claim based only on graph representation plus sanction propagation.

### 5.4 Country/region exposure and supply-chain concentration
Research already quantifies country/region vulnerability using trade concentration, bilateral exposure, input dependence, sanctions risk and network concentration metrics.

**Threat:** high to H3 if `localized relevance` only means computing import dependence or concentration.

## 6. Mechanism matrix

| Prior art/system | Event detection | Source verification | Exposure mapping | Transmission mechanism | Country localization | Sector/product localization | Scenario/forecast | Uncertainty/provenance | Historical validation | Main threat |
|---|---|---|---|---|---|---|---|---|---|---|
| GDELT | Strong | Limited by source/data model | Partial | No economic mechanism by itself | Strong geography | Theme/entity level | No | Source/time metadata | Event-data research | kills event-graph novelty |
| Interos | Strong | Proprietary | Strong multi-tier | Operational risk logic | Strong | Strong | Risk/predictive | Proprietary scoring | Commercial evidence not fully public | kills enterprise event→impact novelty |
| Everstream | Strong + human validation | Strong advertised | Strong network/digital twin | Operational/logistics pathways | Strong | Strong | Predictive alerts | Human + data-source context | Commercial claims; public methodology limited | strongest enterprise threat |
| Sayari | Event/list updates | Primary-source emphasis | Strong ownership/trade graph | Compliance/exposure pathways | Strong | Supplier/product/trade | Risk scoring | Audit-ready evidence | Enforcement/compliance use | kills sanctions-network novelty |
| SupplySeer | GDELT-based | Weak/experimental | Commodity/route level | Rule/config-based | Moderate | Strong commodities/routes | Scenario values | Limited | Not established | shows easy prototype is already open source |
| World Monitor | Strong multi-source | Improving/versioned | Trade/route/country | Scenario/cost-shock functions | Strong | Products/sectors/routes | Scenario + risk | Methodology versioning | Mixed/open | kills dashboard-breadth novelty |
| GDELT bilateral conflict/trade research | Strong structured event data | Human-calibrated indicator | Bilateral trade | Econometric gravity channel | Strong | Trade layer | Estimated effect | Statistical inference | Historical panel | kills event-type→trade claim |
| Sanctions/CGE literature | Event/policy given | High for policy scenario | Country/sector IO/trade | Explicit economic model | Strong | Strong | Scenario/model estimate | Model assumptions | Scenario/historical calibration | kills sanctions propagation novelty |
| GNN geoeconomic framework | Multimodal inputs | Unknown/partial | Global trade graph | Learned graph propagation | Strong | Strategic trade | Simulation/prediction | Needs scrutiny | Limited | kills graph+AI framing |

## 7. H1–H4 reassessment

### H1 — Country-Specific Event-to-Impact Pathway
**Status after attack: PARTIALLY SURVIVES, BUT GENERIC VERSION IS FALSIFIED.**

Commercial supply-chain platforms already connect events to affected suppliers/materials/routes/products, while economic research already models country/sector transmission. H1 can survive only if the pathway is materially different from enterprise supply-chain impact mapping.

Candidate surviving distinction:
- public-interest / country-and-household interpretation rather than enterprise-owned supplier network;
- explicit separation of observed event, measured exposure, supported mechanism, conditional scenario and forecast;
- every edge of the pathway carries evidence and uncertainty visible to the user;
- downstream outcomes expressed in country-relevant consumer/sector categories without pretending causal certainty.

Novelty: **UNKNOWN**.

### H2 — Evidence-Calibrated Warning
**Status: PROMISING AS TRUSTWORTHINESS ARCHITECTURE; STANDALONE NOVELTY WEAK/UNKNOWN.**

Commercial products already validate alerts and rank relevance. The potentially defensible part is not `confidence score`, but explicit evidence-state transitions and refusal to assign a strong warning when one of the required links is missing.

Candidate mechanism:
`event credibility × exposure evidence × mechanism evidence × horizon/model evidence`, with missing components lowering the claim class rather than being silently imputed by an LLM.

### H3 — Localized Downstream Relevance
**Status: NARROWED HEAVILY.**

Country and sector localization are established. H3 only remains interesting if localization reaches a useful downstream level that existing macro/supply-chain systems do not typically expose to ordinary users—for example:
- household consumption categories;
- locally meaningful imported inputs;
- likely pressure on transport/fuel/food/electronics categories;
- affected domestic industries;
while preserving evidence boundaries.

This must be tested against consumer-price pass-through and household-expenditure literature before it can survive.

### H4 — Forecast-vs-Scenario Separation
**Status: RETAIN AS A REQUIRED DESIGN PRINCIPLE, NOT A NOVELTY CLAIM.**

This is a trustworthiness invariant. P003 must clearly distinguish:
- observed fact;
- measured exposure;
- estimated historical association;
- conditional scenario;
- statistical forecast;
- unsupported/unknown.

## 8. Strongest new novelty threat
The combination of Everstream/Interos/Sayari on the commercial side, plus World Monitor/SupplySeer/GDELT on the open-source side, means that **`geopolitical intelligence + supply chain graph + event alerts + localized impact` is too crowded to be the core contribution.**

If P003 remains a research project, it must move away from `better geopolitical dashboard` and toward a sharply evaluable evidence/impact mechanism.

## 9. New candidate contribution direction
### Evidence-Bounded Local Economic Transmission Graph (working hypothesis)
Given a verified geopolitical event and a target country, construct only those downstream economic pathways for which each transition is backed by an identified data source or model, and explicitly stop the chain when evidence is insufficient.

Example:
`export restriction announced`
→ VERIFIED EVENT
`Nigeria imports affected HS product from restricted source`
→ VERIFIED EXPOSURE
`product is an input into domestic fertilizer/food/logistics sector`
→ SUPPORTED TRANSMISSION LINK
`historical/model evidence indicates cost pass-through under comparable shocks`
→ MODEL-SUPPORTED SCENARIO
`magnitude forecast unavailable`
→ DO NOT INVENT POINT FORECAST

This mechanism differs from a generic alerting platform only if the system can be evaluated on **pathway validity, evidence completeness, abstention quality and calibrated claim strength**.

## 10. Possible research contribution candidates after Pass 002

### C1 — Evidence-Gated Transmission Pathway
Each edge must satisfy an evidence rule before downstream propagation continues. Unsupported edges cause an explicit `INSUFFICIENT EVIDENCE` stop rather than LLM completion.

### C2 — Claim-Class Separation
The system has distinct output classes for fact, exposure, supported mechanism, scenario, model estimate and forecast. UI and API prevent one class from silently becoming another.

### C3 — Household/Consumer Relevance Layer
Map sector/product shocks to target-country consumer categories or household-relevant exposures using official trade, input-output, CPI weight or expenditure data. This requires direct prior-art review next.

### C4 — Counterevidence-Aware Pathways
Store contradictory evidence and mitigation/substitution evidence—for example alternative suppliers, inventories, policy intervention or low import dependence—so warnings can weaken or close rather than only escalate.

C1–C4 are **hypotheses**, not novelty claims.

## 11. Evaluation requirements sharpened
Future experiments must compare against strong baselines:
- B0: headline/GPR risk score only;
- B1: event + direct bilateral trade exposure;
- B2: enterprise-style rule-based event relevance mapping;
- B3: pathway model without evidence gating;
- B4: evidence-gated pathway model;
- B5: evidence-gated + counterevidence/mitigation.

Metrics should include:
- event precision/recall where automated extraction is used;
- exposure-link precision;
- mechanism-link agreement with expert/economic evidence;
- unsupported-edge rate;
- abstention precision/utility;
- false-warning rate;
- direction accuracy where outcomes are measurable;
- calibration by claim class;
- time-to-warning;
- pathway completeness;
- reviewer agreement;
- provenance completeness;
- performance against simple trade-exposure and GPR baselines.

## 12. Security and misinformation implications from prior art
- High-volume media signals require deduplication and source-quality controls.
- News repetition must not be counted as independent corroboration.
- Official sanctions/tariff/export-control sources should outrank secondary reports for policy facts.
- Retrieved news is untrusted and may contain prompt injection or misinformation.
- Entity resolution must fail closed where identity is ambiguous.
- A malformed or adversarial article must not create a high-confidence economic pathway.
- Historical revisions and source timestamps must remain visible.

## 13. Kill/reframe criteria updated
P003 should be PARKED/REFRAMED if any of the following occur:
1. direct prior art is found that already performs evidence-gated event→exposure→mechanism→consumer/country outcome pathways with comparable provenance and abstention;
2. official/public data cannot support the required country/sector/consumer linkage at useful resolution;
3. expert review shows pathway edges are too subjective to label reproducibly;
4. the evidence-gated system does not reduce unsupported warnings relative to simpler baselines;
5. household/localization claims require so many assumptions that they collapse into generic narrative;
6. end-user usefulness does not exceed a normal geopolitical news + trade-exposure dashboard;
7. the system's numerical outputs are mostly manually configured or LLM-generated rather than empirically grounded.

## 14. Decision
**MORE RESEARCH — PROMISING, BUT THE EASY NOVELTY STORY IS DEAD.**

P003 survives only in a narrower form. Commercial and open systems already cover much of the event-monitoring, supply-chain mapping, sanctions exposure and predictive-alert space. The strongest remaining direction is an **evidence-bounded local economic transmission mechanism** whose key behavior is not simply prediction, but explicit stopping/abstention when an event-to-impact chain cannot be supported.

## 15. Next pass
**Pass 003 — Local/Household Transmission, Counterevidence and Abstention Prior Art.**

Directly investigate:
- import-price pass-through to CPI/PPI;
- commodity and exchange-rate pass-through in Nigeria and comparable emerging markets;
- household expenditure/CPI basket localization;
- input-output mapping from imported intermediate to consumer category;
- substitution, inventories and alternative suppliers as counterevidence;
- causal graph / evidence graph systems with explicit abstention;
- uncertainty calibration and selective prediction;
- whether existing economic-warning systems already expose these chains to ordinary users.

The goal of Pass 003 is to decide whether C1/C3/C4 can be turned into one falsifiable contribution or should be demoted.