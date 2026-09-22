# P001 M8 — Human Boundary Data-Flow Checkpoint

The first two-case dry-run path is now explicitly separated into four layers: (1) frozen constructed case/evidence; (2) blinded assessor presentation; (3) immutable assessor response capture; and (4) descriptive comparison. No layer is allowed to generate a missing human judgment.

The assessor-response registry is intentionally distinct from the experiment's single independent-reference record. During M8, two assessors may disagree. Their original responses must be preserved before any later protocol decides whether a reference state can be derived. Therefore the software does not automatically convert majority agreement, construction expectation, or B4 output into the reference judgment.

Duplicate case+assessor records are rejected rather than overwritten. One assessor produces no two-assessor comparison. Two distinct assessor responses may be compared descriptively while preserving disagreement.

This checkpoint remains preparation. It records no actual assessor response and supplies no scientific result.
