# P003 — Comparative Analysis Authorization Gate v1

## Purpose
The system must not calculate reviewer agreement or proceed toward B2-vs-B3 claim-quality analysis from incomplete, mismatched or mutable reviewer evidence.

## Required conditions
The gate requires:
1. two distinct reviewer identities;
2. both review batches verify against their SHA-256 pre-unblinding locks;
3. both reviewers cover exactly the same blinded claim IDs.

Only after these conditions pass may reviewer agreement be calculated.

## Metrics exposed at this gate
- raw reviewer agreement;
- Cohen's kappa where mathematically defined.

Unsupported Downstream Claim Rate (UDCR) is a later post-unblinding metric. This module exposes a helper but cannot establish that supplied claims were legitimately unblinded; the experiment operator must preserve the frozen blind-ID mapping and analysis lineage.

## Deliberate non-claims
Passing this gate does not prove:
- reviewer independence or domain expertise;
- scientific validity of the judgments;
- B3 superiority over B2;
- statistical generalisability;
- completion of M9.

It proves only that the software-side integrity prerequisites for comparative analysis have been satisfied.
