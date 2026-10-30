# P001 Verification Probe Specification — Development Candidate v1.0

## Definition

A **Verification Probe** is a bounded additional question or task intended to acquire independent evidence for a specific Evidence Gap.

The historical source taxonomy contains four core families:
- explain
- predict
- modify
- debug

The current development specialization may use:
- EXPLAIN
- TRACE
- TEST_DESIGN
- DEBUG_DIAGNOSE
- MODIFY
- CONCEPT_CONTRAST

The expanded taxonomy is a proposed specialization, not an original-source claim.

## Selection rule

A probe must first be:
1. applicable to the target competence claim;
2. admissible for the detected gap; and
3. potentially sufficient to resolve or materially reduce that gap.

Only then may burden be minimized.

Conceptually:

V* = argmin Burden(v), for v in the frozen adequate/admissible candidate set.

This is a **bounded minimum**, not a claim of global mathematical optimality.

## Burden reporting

Report separately:
- number of probes/questions;
- verification time;
- complexity (provisional Low/Medium/High or another assessor-reviewed scale).

Do not invent an arbitrary weighted composite burden score before validation.

## Current CC3 development catalogue

- **VP-CC3-01 — Additional input only.** Low burden; admissible to CC3/EG-T3 but not currently treated as potentially sufficient.
- **VP-CC3-02 — Bounded independent test design.** Candidate supplies one important test not already supplied, expected result, and why it is useful. Current first vertical-slice probe.
- **VP-CC3-03 — Comprehensive test suite.** Higher burden; potentially sufficient but no frozen automated response rubric yet.

The current software correctly refuses to process a probe result when that probe lacks a frozen response rubric.

## Stopping/control

- SUPPORTED may terminate verification for the target claim.
- PARTIAL/UNRESOLVED may continue only when an adequate unused probe remains and further verification is justified.
- CONTRADICTED must not be converted automatically into a misconduct verdict.
- No adequate probe may result in HUMAN_REVIEW_REQUIRED.

Exact multi-probe stopping and contradiction policy remain scientific freeze items.
