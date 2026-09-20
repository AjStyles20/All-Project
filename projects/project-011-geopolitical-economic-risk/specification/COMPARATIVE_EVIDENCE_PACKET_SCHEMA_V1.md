# P003 — Frozen Comparative Evidence Packet Schema v1

## Status
**FROZEN BEFORE REAL B2 GENERATION OR HUMAN REVIEW.**

Purpose: guarantee that B2 and B3 comparisons are based on a traceable case information set while keeping reviewer packets blinded.

## Case packet fields
Every experimental case packet must contain:
- packet_id and schema_version;
- case_id and replay_mode (R1/R2);
- information_cutoff/reference boundary;
- frozen target and horizon;
- evidence items with evidence_id, transition relevance, source authority tier, source reference, observed/publication date where known, data vintage, geography, economic identifier/classification, and content summary;
- counterevidence items;
- packet hash;
- explicit exclusions/unknowns.

## Baseline input view
B2 receives the frozen evidence and counterevidence content but not B3 transition states, stopping decisions, prohibited outputs, reviewer labels, or later evaluation outcomes.

B3 receives the same admissible information set through its typed transition representation.

Equivalent information does not require identical serialization; it requires that neither baseline receives a materially informative fact withheld from the other.

## Reviewer view
Reviewer packets contain:
- opaque claim ID;
- atomic claim text;
- replay mode and boundary;
- relevant frozen evidence/counterevidence;
- target/horizon where applicable.

They do not reveal baseline identity or B3's expected transition state.

## Outcome separation
Later outcome observations used to score directional agreement are stored separately from the baseline information packet unless they were genuinely available within the replay boundary.

## Mutation rule
Once a packet is used for a real B2 run, it is immutable. Corrections require a new packet version/hash and rerunning affected comparisons.

## Current packet readiness
Candidate A: research packet content substantially available; needs final machine-readable evidence references/hash.
NC-01: narrow negative-control packet substantially available; needs final machine-readable evidence references/hash.
Candidate B: not ready; Nigeria-specific exposure unresolved.
Candidate C: not ready for downstream comparison; T3 remains conditional.
