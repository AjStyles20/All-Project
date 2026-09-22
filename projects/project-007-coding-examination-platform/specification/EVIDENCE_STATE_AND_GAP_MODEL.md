# P001 Evidence State and Gap Model — Development Specification v1.0

## Purpose

This document defines how P001 separates evidence, claim applicability, evidence state and evidence gaps. It is a development specification pending independent assessor/pilot validation.

## Evidence state

A REQUIRED competence claim may have one of four evidence states:

- **SUPPORTED** — available admissible evidence satisfies the current bounded support rule.
- **PARTIAL** — relevant evidence supports part of the bounded claim but does not satisfy the complete support rule.
- **UNRESOLVED** — evidence is insufficient to determine support or contradiction.
- **CONTRADICTED** — material admissible evidence conflicts with the bounded claim under a frozen contradiction rule.

NOT_APPLICABLE is not an evidence state.

## Evidence gaps

An **Evidence Gap** is the specific missing, incomplete, contradictory or assistance-dependent information preventing defensible resolution of a REQUIRED competence claim.

Development taxonomy:

- **EG-T1 — Missing Independent Explanation**
- **EG-T2 — Missing Execution Reasoning**
- **EG-T3 — Missing Independent Test Design**
- **EG-T4 — Missing Debugging Evidence**
- **EG-T5 — Missing Independent Modification**
- **EG-T6 — Incomplete Evidence**
- **EG-T7 — Contradictory Evidence**
- **EG-T8 — Assistance-Dependent Evidence**

Assistance-dependent evidence does not by itself establish incompetence or misconduct.

## Current implemented path

The first verified development path is:

CC3 REQUIRED + supplied execution/test evidence only → UNRESOLVED → EG-T3 → targeted verification.

The current CC3 structured development rubric operationalizes PARTIAL for software testing, but its scientific validity remains pending.

## State-history rule

State transitions are appended as history rather than overwriting prior records where practical. A later SUPPORTED state does not erase that the claim was previously UNRESOLVED.

## Abstention

If no adequate admissible probe exists, or if consequential contradiction cannot be resolved safely by the bounded automated mechanism, the method may return HUMAN_REVIEW_REQUIRED.
