# P007 / Legacy P004 — School Point & Digital Economy System

## Pass 001 — Historical Lineage, Token Economies, Gamification and Initial Feasibility

**Date:** 2026-09-10  
**Portfolio ID:** P007  
**Legacy ID / directory mapping:** P004  
**Decision:** MORE RESEARCH

## Scope
A governed school points/reward economy tied to selected achievements or positive contributions, with controlled earning, accumulation and redemption. This pass tests the generic concept before any implementation or novelty claim.

## Findings

### 1. Generic token-economy mechanism is established
Educational/behavioural token economies long predate modern digital gamification. The generic sequence — desired behaviour/achievement -> token/point -> accumulation -> reinforcement/reward — is established prior art.

A 2022 scoping review by K. Tan, Mathura Kasiveloo and I. Abdullah reviewed 60 articles from 2000–2020 concerning token economies, behaviour management and learning engagement. It also identified social fairness and teacher participation/evaluation as comparatively weaker areas.

### 2. K–12 gamification is crowded
A 2023 systematic review by Dehghanzadeh et al. reviewed 54 empirical K–12 gamification studies. Gamification may improve cognitive, affective and behavioural outcomes, especially engagement/motivation/competitiveness, but neutral or negative effects also occur and outcomes are context-dependent.

Therefore points, badges, leaderboards, balances and ordinary gamification cannot be treated as novel mechanisms.

### 3. Digital school reward platforms already exist
Commercial systems such as PBIS Rewards digitize school token economies with electronic points, balances, school stores/redemption, reporting and related administrative features. A product consisting only of teacher-awarded points, student balances, redemption and dashboards is therefore insufficient as a research contribution.

### 4. Social validity and implementation burden matter
A 2026 registered-report systematic review by Beahm et al. examined 113 token-economy studies in instructional settings; 29 (25.6%) systematically evaluated social validity. Student/parent perceptions were generally positive while teacher perceptions were more mixed, including concerns that implementation fidelity can be time-consuming and challenging.

### 5. Economy/governance risks
A school reward economy can create or expose:
- unequal earning opportunity;
- reward concentration;
- teacher/category issuance imbalance;
- reward inflation or scarcity;
- arbitrary pricing;
- hoarding or unofficial exchange;
- incentive gaming / Goodhart-like effects;
- favoritism or compromised issuer accounts;
- administrative workload;
- privacy/accessibility concerns.

These are research/governance questions, not proof of novelty.

## Rejected novelty claims after Pass 001
Do not claim novelty from:
- digital student points;
- point balances;
- school reward stores;
- badges or leaderboards;
- QR-based award/redemption;
- ordinary transaction histories;
- generic teacher/admin dashboards;
- generic gamification of school behaviour;
- blockchain/cryptocurrency merely because the project is called a digital economy.

## Architecture constraint
Blockchain, cryptocurrency, NFTs and decentralized consensus are excluded unless later evidence establishes a concrete trust requirement that cannot be met by a school-controlled database. The school is ordinarily the central governance authority.

## Provisional surviving hypotheses — NOT YET NOVELTY CLAIMS

### H1 — Opportunity-Normalized Reward Fairness
Investigate whether a school points system can distinguish achievement from unequal opportunity to earn, and detect structural disadvantage without automatically equalizing students or making unsupported fairness claims.

### H2 — Reward-System Fairness Audit
Use transaction/policy evidence to identify governance signals such as unusual class/teacher/category issuance rates, concentration of redemption, or systematically reduced earning opportunity. Signals require human review and are not automatic misconduct verdicts.

### H3 — Incentive-Integrity / Anti-Gaming
Investigate whether earning rules can reduce reward gaming and preserve the intended educational behaviour rather than merely maximizing point-seeking behaviour.

### H4 — Sustainable School-Economy Governance
Investigate measurable indicators and policies for issuance, redemption, scarcity, inequality, workload and incentive stability without pretending the school system is a cryptocurrency market.

## Minimum audit evidence for later prototypes
Any future prototype should preserve at least:
- transaction ID;
- student/account identifier;
- amount;
- earning/redemption reason;
- issuer;
- governing rule/policy version;
- timestamp;
- reversal status;
- approval evidence where required.

This is an engineering baseline, not a novelty claim.

## Evidence discipline
H1–H4 are UNVERIFIED HYPOTHESES. Pass 001 establishes only that generic token economies/gamification are crowded and that fairness, incentive integrity and governance warrant a narrower prior-art attack. No claim that these mechanisms are new has been approved.

## Next research pass
**P007 Pass 002 — Direct Prior-Art Attack on Fairness-Aware Educational Reward Economies, Incentive Gaming and Governance.**

The pass must test whether existing academic/commercial/open-source systems already:
1. measure unequal opportunity to earn rewards;
2. detect teacher/category reward bias or concentration;
3. detect reward gaming/perverse incentives;
4. monitor economy health or reward inflation/scarcity;
5. adapt issuance/redemption policies;
6. implement comparable mechanisms specifically in educational token economies.

If these mechanisms are already comparably established, narrow or kill P007 rather than relabeling established gamification as novelty.

## Key academic evidence used
- K. Tan, Mathura Kasiveloo & I. Abdullah (2022), *Token Economy for Sustainable Education in the Future: A Scoping Review*.
- H. Dehghanzadeh et al. (2023), *Using gamification to support learning in K-12 education: A systematic literature review*, British Journal of Educational Technology, 55, 34–70.
- Lydia A. Beahm, Bryan G. Cook, E. Ingvarsson & Ekemini Eshiett (2026), *The Social Validity of Token Economy Interventions in Instructional Settings: A Registered Report Systematic Review*, Behavioral Disorders, 51, 177–196.

## Current gate
**MORE RESEARCH.** Generic digital points/rewards platform novelty is rejected. Fairness, incentive integrity and governance remain provisional research territory pending Pass 002.
