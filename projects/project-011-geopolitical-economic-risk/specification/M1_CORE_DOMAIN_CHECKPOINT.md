# P003 M1 — Core Domain Checkpoint

## Scope

M1 implements the first bounded Economic Transmission Evidence Contract (ETEC) domain model. It is software infrastructure for later falsification experiments; it is not historical or scientific validation.

## Implemented domain concepts

- TransitionClass T1–T6
- EdgeState: VERIFIED, SUPPORTED, CONDITIONAL, CONTESTED, STALE, INSUFFICIENT, CONTRADICTED
- OutputClass from abstention through calibrated forecast
- SourceAuthorityTier
- EconomicCase
- EvidenceItem
- TransitionAssessment
- time-respecting evidence validation
- sequential weakest-link output cap

## Current deterministic fixtures

The first tests require:
1. missing T3 domestic-transmission evidence caps output at EXPOSURE_IDENTIFIED;
2. a later T4 assessment cannot skip missing T3;
3. a CONTESTED required edge stops progression;
4. T6 cannot release a forecast when T5 model eligibility is insufficient;
5. evidence after the historical information cutoff is rejected.

## CI verification

GitHub Actions P003 ETEC Tests run #5 executed successfully after fixing the project-root import path in CI.

Verified result: **5 passed, 0 failed in 0.01s**.

The preceding run #3 failed during collection with `ModuleNotFoundError: No module named 'app'`; this was a CI path/configuration defect, not a domain-test failure. Commit `1449d3479600c1a7fd207134bb2529ff494fa205` sets the project root on `PYTHONPATH` and invokes pytest as a module.

## M1 closure gate

**M1 CLOSED for the bounded core-domain slice.** The five frozen deterministic tests execute successfully in GitHub Actions. This proves only that the implemented invariants behave as tested; it does not establish historical validity or scientific superiority of ETEC.
