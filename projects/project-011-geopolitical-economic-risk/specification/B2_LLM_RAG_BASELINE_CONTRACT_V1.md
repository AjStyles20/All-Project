# P003 — B2 LLM/RAG Baseline Contract v1

## Status
**PROCEDURE FROZEN; NO REAL B2 RUNS EXECUTED YET.**

## Purpose
B2 tests whether a language model given the same frozen evidence can produce persuasive downstream Nigerian economic claims without the explicit typed-edge/weakest-link enforcement used by B3.

B2 is a comparator, not a straw man. It must receive enough evidence to be useful and must not be deliberately prompted to hallucinate.

## Equivalent-information rule
For each case, B2 receives the same admissible case evidence packet available to B3 under the declared replay mode:
- event evidence;
- Nigeria exposure evidence;
- domestic-transmission/mechanism evidence;
- material counterevidence;
- source metadata and dates;
- declared information cutoff/reference boundary.

B2 does **not** receive:
- B3 transition labels/states;
- B3 stopping decision;
- B3 prohibited-output list;
- reviewer labels;
- later evaluation outcomes unavailable under the replay boundary.

## Frozen task prompt

> Using only the supplied evidence packet, explain the likely economic implications for Nigeria. Distinguish what the evidence directly establishes from what is inferred. State material uncertainty and counterevidence. If the evidence is insufficient for a downstream conclusion, say so. Do not invent facts, sources, numerical estimates, probabilities, or causal certainty that are not supported by the packet.

This intentionally gives B2 a fair uncertainty/abstention instruction. B3 must not gain an artificial advantage from B2 being recklessly prompted.

## Retrieval rule
The first controlled comparison uses **frozen packet RAG**, not live web retrieval:
1. case evidence is frozen and versioned;
2. the same packet is supplied to each B2 run;
3. no external search/tool call is allowed during generation;
4. packet hash is recorded.

This isolates reasoning/claim behavior from retrieval drift.

## Generation record
Every B2 generation must preserve:
- provider/model identifier;
- model/version if exposed;
- run timestamp;
- system/developer/user prompt text;
- packet identifier/hash;
- generation parameters exposed by provider;
- complete raw response;
- extracted atomic claims;
- extraction version/reviewer.

If deterministic seeding is unsupported, repeated runs are required and variability must be reported rather than hidden.

## Repetition
Minimum design proposal before M10: **3 independent generations per case** under the same frozen packet/procedure, subject to model/provider feasibility.

The three-run minimum is a design choice for observing output variability, not a statistical-power claim.

## Claim extraction
B2 prose is not scored as one blob. Before reviewer scoring:
1. split into atomic downstream claims;
2. preserve verbatim claim text;
3. classify claim level (event/exposure/transmission/scenario/magnitude/forecast);
4. assign opaque randomized claim IDs;
5. remove baseline/model identity from reviewer packet where possible.

Claim extraction must not rewrite a strong claim into a weaker one.

## Fairness rules
- Same case/replay boundary as B3.
- Same evidence and counterevidence content.
- No outcome-aware prompt tuning.
- No prompt changes after seeing which baseline scores better.
- If prompt changes are scientifically necessary, create a new protocol version and rerun all affected cases.
- Model inference itself never becomes primary evidence for a B3 edge.

## Failure/abstention
If B2 explicitly says evidence is insufficient and withholds a downstream claim, record that as abstention; do not force a claim merely to create contrast with B3.

## Primary comparison
Independent blinded reviewers score atomic B2 and B3 claims using the frozen Independent Claim-Judgment Protocol.

Primary: unsupported downstream claim rate (UDCR).
Also report:
- partially supported rate;
- useful downstream-claim coverage;
- abstention frequency and appropriateness;
- false local warnings on negative controls;
- run-to-run variability for B2.

## Not yet authorized
This contract does not authorize any statement that:
- a particular LLM is unreliable;
- B3 is superior;
- B2 has a measured UDCR;
- three generations are statistically sufficient;
- the result generalizes beyond the evaluated cases/model/procedure.
