# P003 — Independent Reviewer Blinding Contract v1

## Purpose
Prepare B2/B3 atomic claims for independent judgment without revealing which baseline produced the claim.

## Reviewer-visible fields
- blind claim ID;
- atomic claim text;
- claim type;
- the frozen evidence material required by the reviewer protocol.

## Hidden until judgments are locked
- B0/B1/B2/B3 identity;
- original run ID where it reveals baseline identity;
- generation index;
- expected ETEC state;
- construction expectation;
- aggregate comparative metrics;
- other reviewers' judgments.

## Identity rule
A blinded ID is deterministically derived from a frozen experiment salt plus the original claim ID using SHA-256 and exposes no baseline label. The mapping must be preserved privately for later scoring.

## Judgment labels
Use the already frozen atomic labels:
SUPPORTED, PARTIALLY_SUPPORTED, UNSUPPORTED, CONTRADICTED, INDETERMINATE.

No label is assigned by this blinding code.

## Independence rule
Prefer at least two reviewers. Reviewers should judge independently before seeing agreement statistics or each other's labels.

## Unblinding
Unblind only after reviewer judgments for the batch are locked. Then join blind IDs back to the preserved mapping and calculate the predeclared metrics.

## Boundary
Software blinding improves experimental hygiene but does not create independent human evidence. M9 remains incomplete until actual independent judgments are obtained.
