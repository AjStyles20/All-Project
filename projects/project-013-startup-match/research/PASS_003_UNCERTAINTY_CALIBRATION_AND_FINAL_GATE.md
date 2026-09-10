# P008 (Current ID; legacy P013) — Pass 003

## Uncertainty, Calibration, Evidence Provenance and Final Research Gate

Date: 2026-09-10
Status: FINAL GATE
Decision: **KILL as a research-novelty candidate; PARK as an engineering/product project**

## Scope
This pass directly attacked the strongest surviving hypothesis from Pass 002:

> H5 — Evidence-Calibrated Investor Recommendation: explicitly represent evidence freshness, completeness, provenance and declared-vs-revealed preference disagreement so founder-investor recommendations become better calibrated and appropriately uncertain than compatibility-only ranking.

The attack covered uncertainty-aware recommender systems, recommendation confidence, selective/abstaining recommendation, concept drift and temporal staleness, startup/VC uncertainty, and current commercial private-market intelligence systems.

## Key findings

### 1. Recommendation confidence and reliability are established
Recommender-system research already treats confidence/reliability as a first-class property separate from raw ranking accuracy. Prior work proposes reliability measures for predictions and recommendations and studies when low-confidence recommendations should be withheld.

### 2. Selective recommendation / abstention is established
Decision-aware recommender research explicitly studies whether a system should avoid recommending when confidence is low, trading precision against coverage. More recent work studies confidence-gated abstention under structural uncertainty, cold-start and temporal/contextual drift.

Therefore the claims "show confidence with each recommendation" and "abstain when evidence is weak" are not novel.

### 3. Temporal drift and staleness are established recommender problems
Time-aware and dynamic recommender systems model changing preferences and concept drift. Research also studies stale recommendations, adaptive model updating, temporal confidence and decay. Thus recency-aware recommendation by itself is not a contribution.

### 4. Uncertainty-aware venture analytics is now direct prior art
2026 work on startup success and valuation prediction explicitly provides calibrated uncertainty estimates, distinguishes cases based on insufficient/noisy evidence, and routes ambiguous cases toward human review. This destroys any broad claim that uncertainty-aware VC decision support is unexplored.

### 5. Commercial prior art directly collides with H5
Capital Radar, a current private-market intelligence platform, explicitly:
- separates observed facts, inferred indicators and confidence;
- uses source confidence in investor/capital matching;
- treats missing data as lower confidence rather than a confirmed negative;
- displays component context and evidence behind match signals;
- states that a high score with weak evidence should not be treated as well-corroborated;
- preserves human corrections and source-backed provenance;
- warns that investor matching ranks possible relevance and does not confirm appetite.

This is materially close to the P008 H5 product mechanism.

Seedtable likewise advertises sourced startup/investor data where facts carry source, confidence and last-verified date, showing that provenance/freshness/confidence are also current commercial product features.

### 6. Declared-vs-revealed investor behaviour does not rescue novelty
Temporal investment-history modelling is already used in startup-VC matching. A separate comparison of declared thesis and revealed behaviour may still be useful UX/analytics, but treating that comparison as the novelty anchor would now be an artificial narrowing rather than a strong independent research contribution.

## Claims rejected after three passes
- AI founder-investor matching.
- ML compatibility scoring.
- Investor ranking by sector/stage/geography/ticket size.
- Two-sided VC recommendation.
- Explainable investor recommendation.
- Positive-unlabeled treatment of missing interactions.
- Exposure/fairness-aware recommendation.
- Temporal/recent-investment modelling.
- Evidence freshness as a recommendation feature.
- Confidence/reliability alongside recommendations.
- Selective recommendation / abstention.
- Source provenance and last-verified dates.
- Human review for uncertain venture recommendations.
- Combining these mature ideas into a founder-investor platform as a novelty claim.

## Final assessment
The engineering problem remains legitimate and useful, especially for founders who need transparent investor discovery. However, the research contribution has collapsed into a combination of established recommender-system methods and already-deployed private-market intelligence practices.

Further narrowing would risk manufactured novelty: adding more qualifiers to an already occupied mechanism rather than identifying a distinct research problem.

## Final decision
**KILL P008 as a research-novelty/FYP-shortlist candidate.**

Preserve as optional product/portfolio work:
- structured founder/investor profiles;
- transparent multi-criteria matching;
- evidence provenance;
- stale-data warnings;
- declared-vs-revealed thesis analytics;
- communication/CRM workflow;
- explicit disclaimer that relevance does not imply investor appetite or probability of funding.

No formal research specification is authorized because the novelty gate did not survive.

## Next portfolio action
Proceed to **P009 — Personal Screen Memory System — Pass 001**, unless AJ explicitly reorders the portfolio.
