# P003 — ETEC Implementation Entry Contract

**Canonical ID:** P003  
**Historical directory:** project-011-geopolitical-economic-risk  
**Project:** Geopolitical Risk to Economic Impact Forecasting and Warning System  
**Implementation branch:** p003-etec-implementation  
**Authority:** DR-008 residual contribution boundary + DR-010 staged implementation authorization + formal ETEC experiment specification.

## 1. Contribution boundary

The implementation must evaluate the surviving residual contribution:

**typed transmission-edge evidence sufficiency + weakest-link downstream claim progression.**

Generic evidence contracts, RAG grounding, provenance, knowledge graphs, contradiction handling, abstention, geopolitical-risk scoring, and LLM explanations are prior-art territory and are not claimed as the contribution.

## 2. Research mechanism

The Economic Transmission Evidence Contract (ETEC) constrains progression through:

EVENT → EXPOSURE → DOMESTIC TRANSMISSION → LOCAL OUTCOME → MAGNITUDE → CALIBRATED FORECAST

A downstream claim may not be stronger than the weakest required preceding transition. Missing, stale, contested, insufficient, or contradicted required evidence must cap, downgrade, recompute, or stop progression according to the frozen transition rules.

## 3. Initial transition scope

The first implementation slice is deterministic and bounded. It must represent transition classes T1–T6 and edge states:

VERIFIED, SUPPORTED, CONDITIONAL, CONTESTED, STALE, INSUFFICIENT, CONTRADICTED.

It must not use an LLM to decide whether a mandatory edge is satisfied.

## 4. First vertical slice

Build only enough domain machinery to demonstrate:

1. a verified event;
2. a measurable Nigeria exposure;
3. a missing product-to-sector/domestic-transmission mapping;
4. weakest-link evaluation;
5. mandatory stop at exposure;
6. an auditable explanation naming the missing transition/evidence.

This is the F1 Missing-Link falsification fixture. Passing it demonstrates implementation of the contract rule, not the scientific contribution.

## 5. Evidence and provenance

Every accepted evidence object must preserve at minimum:
- evidence identifier;
- transition/edge to which it applies;
- source class/authority tier;
- source reference;
- observation/publication timestamp where available;
- data vintage/version;
- geography;
- economic identifiers/classification version where applicable;
- validity horizon/staleness metadata;
- content hash or frozen snapshot reference where practical.

No evidence may be silently synthesized from an LLM narrative.

## 6. Initial output classes

The implementation must distinguish at least:
- VERIFIED EVENT ONLY;
- EXPOSURE IDENTIFIED;
- TRANSMISSION SUPPORTED;
- MECHANISM-SUPPORTED SCENARIO;
- MODEL ESTIMATE;
- CALIBRATED FORECAST;
- ABSTAIN / INSUFFICIENT EVIDENCE.

The exact label names may be normalized in code, but their semantic ordering and evidence boundary must remain explicit.

## 7. Mandatory invariants

- No transition may be skipped.
- No numerical magnitude may be released unless model-estimate eligibility is satisfied.
- No calibrated-forecast label may be released without its validation requirement.
- Counterevidence is state-changing evidence, not commentary.
- Staleness must be capable of invalidating dependent progression.
- Contradiction must remain visible.
- Retrieved text is untrusted input.
- Construction fixtures are not historical validation evidence.
- A passing software test is not proof that ETEC improves warning quality.

## 8. Baseline preservation

Future comparative implementation must preserve:
- B0 — News/GPR signal;
- B1 — verified event + direct Nigeria exposure;
- B2 — LLM/RAG explanation from equivalent retrieved evidence;
- B3 — ETEC;
- B4 — optional validated econometric/model comparator only where eligible.

The first deterministic slice does not need to implement B0–B4 yet, but its data model must not make those comparisons impossible.

## 9. Implementation technology

Python-first, lightweight and locally executable. Start with domain objects and deterministic services before FastAPI/UI/database integration. SQLite remains a candidate for later persistence; no database choice is required for the first pure-domain slice.

## 10. Deferred

Do not initially build live news monitoring, automated event extraction, arbitrary web retrieval, universal HS concordance, live UN Comtrade integration, LLM/RAG, econometric forecasting, investment/trading actions, multi-country support, or a heavy frontend.

## 11. Verification order

M0 — implementation-entry contract  
M1 — core transition/evidence domain model  
M2 — weakest-link progression evaluator  
M3 — F1 missing-link vertical slice + audit trace  
M4 — counterevidence/staleness/contradiction recomputation  
M5 — F2–F8 deterministic falsification fixtures where applicable  
M6 — persistence/reproducibility package  
M7 — B0–B3 comparative runner  
M8 — historical replay preparation  
M9 — independent domain/reviewer validation  
M10 — frozen historical evaluation

## 12. Entry decision

**AUTHORIZED FOR M1 CORE DOMAIN IMPLEMENTATION on branch p003-etec-implementation.**

This authorization follows DR-010 and the completed P001 research-critical checkpoint. It does not authorize broader product scope or scientific claims.
