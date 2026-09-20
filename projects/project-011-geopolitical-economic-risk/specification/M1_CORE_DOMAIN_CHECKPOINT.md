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

## CI status warning

The P003 workflow file exists on the implementation branch, but GitHub did not create a workflow run for the commit that introduced it. Therefore M1 must not be called CI-verified yet. This is an infrastructure issue to resolve before M1 closure.

## M1 closure gate

M1 closes only after the P003 test workflow actually executes on GitHub Actions and the exact pytest result is recorded. A workflow file existing in the repository is not verification.
