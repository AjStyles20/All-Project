# P003 — First B2 Experiment Manifest v1

## Status
**PREDECLARED BEFORE ANY REAL B2 OUTPUT IS GENERATED.**

Manifest ID: `P003-B2-MANIFEST-v1`

## Included cases
1. Candidate A — `P003-A-R2-PKT-v1`
2. NC-01 — `P003-NC01-R2-PKT-v1`

Both are R2 retrospective-reconstruction packets.

## Predeclared generations
Candidate A:
- B2-A-001
- B2-A-002
- B2-A-003

NC-01:
- B2-NC01-001
- B2-NC01-002
- B2-NC01-003

Exactly six first-wave B2 generations are therefore predeclared.

## Binding
Each planned run is bound to the SHA-256 hash of its frozen evidence packet. If a packet changes, the planned run no longer matches that packet and a new manifest/version is required.

## Retention rule
All six valid generations must be retained. Outputs cannot be discarded because they help or hurt B2/B3.

A technical failure may be documented and rerun, but the failed attempt remains in the audit record and does not silently disappear.

## Scoring path
raw response → immutable B2RunRecord → atomic claim extraction → baseline identity blinding → independent claim judgment → UDCR/partial-support/coverage/abstention reporting.

No claim labels are assigned in this manifest.

## Boundary
This manifest authorizes experimental readiness; it does not itself execute a model. No B2 empirical result exists until the six predeclared generations are actually produced and preserved.
