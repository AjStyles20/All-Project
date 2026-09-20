# P003 — Independent Claim-Judgment Protocol v1

## Status
**FROZEN BEFORE REAL B2-vs-B3 COMPARATIVE SCORING.**

Purpose: prevent ETEC/B3 from serving as its own answer key.

## Unit of judgment
A **downstream claim** is one atomic proposition asserting a Nigerian exposure, transmission mechanism, local directional outcome, numerical magnitude, probability, or calibrated forecast.

Compound prose must be split into atomic claims before scoring.

## Reviewer evidence packet
For each claim, a reviewer receives:
1. claim text with baseline identity removed;
2. declared information cutoff and replay mode (R1/R2);
3. frozen evidence packet available to that baseline;
4. source/provenance metadata;
5. declared target/horizon where applicable;
6. relevant counterevidence packet.

The reviewer does **not** receive B3's transition state or expected answer.

## Labels
- **SUPPORTED** — evidence available under the declared replay mode is sufficient for the exact claim strength.
- **PARTIALLY_SUPPORTED** — core direction/mechanism has support but wording exceeds evidence or material assumptions remain.
- **UNSUPPORTED** — required evidential link for the exact downstream claim is absent.
- **CONTRADICTED** — admissible evidence materially opposes the claim.
- **INDETERMINATE** — packet is insufficient/ambiguous for a defensible judgment.

INDETERMINATE is not silently counted as SUPPORTED or UNSUPPORTED.

## Unsupported downstream claim rate (UDCR)
Primary comparative metric:

UDCR = number of downstream claims labeled UNSUPPORTED or CONTRADICTED
       / number of downstream claims receiving a determinate label

PARTIALLY_SUPPORTED is reported separately in the primary analysis and included in a sensitivity analysis as an error under a stricter rule.

## Structural abstention judgment
When a baseline withholds a downstream claim, reviewers judge the withheld transition as:
- **APPROPRIATE_ABSTENTION** — available evidence does not justify progression;
- **OVER_ABSTENTION** — available evidence was sufficient for progression;
- **INDETERMINATE_ABSTENTION** — cannot judge.

Correct structural-abstention rate =
APPROPRIATE_ABSTENTION / determinate abstention judgments.

Coverage must be reported alongside abstention quality so a system cannot appear reliable merely by saying nothing.

## False local warning
For a predeclared negative-control case, a **false local warning** occurs when a baseline releases a material Nigerian downstream warning despite the independent packet showing no sufficient Nigeria exposure/transmission pathway.

## Reviewer process
Preferred minimum: two independent reviewers with relevant economics/trade/domain competence.

1. Review independently.
2. Preserve original labels.
3. Measure raw agreement and Cohen's kappa where label counts permit.
4. Discuss disagreements only after independent labels are frozen.
5. Record adjudicated label separately; never overwrite original judgments.
6. If reviewers cannot reproducibly apply the rubric, this threatens the ETEC contribution and triggers reframe/revision before M10.

## Blinding/randomization
- remove baseline IDs and implementation-specific wording where possible;
- randomize claim order;
- do not tell reviewers which claims came from B2 or B3;
- identical claims receive identical evidence packets.

## No outcome leakage
For R1, reviewer support judgments use only evidence available at cutoff. Later outcomes may separately score directional agreement.
For R2, reviewers are told explicitly that the packet is retrospective reconstruction.

## Predeclared comparative interpretation
B3's central reliability contribution is **not demonstrated** unless it reduces UDCR relative to B2 without unacceptable loss of useful coverage and without worse false-local-warning behavior on negative controls.

No single case can establish that result.
