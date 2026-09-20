# P003 — B2 Prompt and Frozen-Packet Serialization Contract v1

## Status
**FROZEN BEFORE REAL B2 GENERATION.**

## Purpose
B2 is the ungated LLM/RAG explanation baseline. It must receive the same material case information as B3 without receiving B3's transition labels, stopping state, prohibited outputs, reviewer judgments, or later evaluation outcomes.

## System prompt
The frozen system prompt instructs the model to:
- use only the supplied packet;
- assess the stated Nigerian target and horizon;
- distinguish facts, uncertainty, counterevidence and inference;
- not invent evidence, numerical magnitude, probability, causal certainty or sources;
- explicitly allow insufficiency/abstention.

This is intentionally fair to B2. The experiment is not designed to induce hallucination.

## Serialization
The user prompt is generated deterministically from the immutable packet. It includes evidence provenance summaries, counterevidence and exclusions/unknowns.

It does not expose ETEC transition labels or expected stopping behavior.

## Experimental integrity
The exact serialized prompt used for every real run must be preserved inside its B2RunRecord. Packet hash and run hash together establish which evidence and wording produced each response.

## Run plan
For each admitted case:
1. freeze/verify packet;
2. deterministically serialize packet;
3. create at least three predeclared B2 generations under the same packet version;
4. preserve every raw response;
5. extract atomic claims without support labels;
6. blind baseline identity before independent review.

No real generation has been executed by this commit.
