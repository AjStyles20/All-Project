# Research Pass 008 — Cross-Agent Provenance Prior-Art Test

Date: 2026-09-09
Status: EVIDENCE BUILD / ADVERSARIAL GAP TEST
Decision effect: P002 remains MORE RESEARCH. No implementation approval.

## Purpose

Test the strongest surviving P002 candidate gap against provenance research outside education. The candidate is not generic citation/RAG provenance, but semantic lineage as claims and evidence are transformed, stored, communicated, challenged, and reused across multiple AI agents and pedagogical decisions.

## Key finding

The broader LLM-agent field has independently identified essentially the same underlying technical problem. Therefore P002 must NOT claim invention of cross-agent provenance, claim-level provenance, execution provenance, evidence graphs, provenance-bearing memory, or typed trace graphs.

However, the reviewed 2026 survey also states that robust semantic provenance across transformations and multi-agent communication remains open. This keeps alive a narrower *application/research integration hypothesis*: whether an education-specific implementation can operationalize these emerging provenance ideas together with pedagogical governance and learner-independence evaluation in a way not already demonstrated by close educational prior art.

This is a candidate gap only, not a novelty conclusion.

## Evidence reviewed

### 1. Wang et al. (2026), From Agent Traces to Trust
Full-paper review (arXiv 2606.04990v4) establishes:
- execution provenance as a typed graph spanning retrieved evidence, tool outputs, memory, observations, intermediate claims, actions, inter-agent messages and final outputs;
- evidence tracing as the evidence-support projection of that broader provenance graph;
- relations such as SUPPORT, CONTRADICT, DEPEND-ON, UPDATE, INVALIDATE and TRIGGER;
- explicit recognition that chronological logging is not equivalent to semantic provenance;
- claim-level provenance and semantic provenance across transformations as open problems;
- explicit concern for evidence that is paraphrased, summarized, aggregated, compressed into memory, passed through tools, or reused by another agent;
- multi-agent provenance as an unresolved responsibility/lineage problem, including tracking which agent introduced an unsupported claim, which failed to verify it, and which message propagated it;
- provenance-bearing memory, runtime recovery, privacy-aware audit infrastructure and full-stack provenance benchmarks as open research areas.

Novelty consequence: the conceptual graph Source -> Claim -> Transformation -> Agent Message -> Downstream Claim is NOT uniquely ours. The field already articulates this class of representation and open problem.

### 2. ProvenanceGuard (2026)
Current research treats source attribution as an independent factuality axis and detects cross-source conflation using stable tool/source identifiers and per-claim verification. This further weakens any generic claim that source-aware claim verification is novel.

Boundary: this is MCP/tool-source factuality work, not evidence that education-specific cross-agent pedagogical lineage is solved.

### 3. GenProve (ACL 2026)
Fine-grained generation-time provenance distinguishes relations such as quotation, compression and inference at sentence level. This threatens a simplistic proposal to classify only whether a generated statement has a citation.

Boundary: fine-grained generated-text provenance is adjacent prior art; it does not by itself establish end-to-end multi-agent pedagogical lineage.

### 4. GAVEL (Findings ACL 2026)
Multi-agent evidence-grounded fact-checking binds atomic subclaims to explicit evidence units and mechanically validates evidence identifiers/spans. This is direct evidence that multi-agent systems can enforce evidence contracts rather than rely on free-form citations.

Boundary: fact-checking is a different task from adaptive education, but the provenance mechanism is relevant prior art.

### 5. Educational trace evidence
ASTRA (Computers & Education: AI, 2026) introduces a trace-ready schema for multi-agent tutoring/collaborative programming and emphasizes reproducible analysis of interaction, participation and verification. Educational Process Mining also models multi-entity learning events. These findings weaken any claim that trace-based multi-agent educational analysis itself is new.

## Updated claim states

| Claim | State | Reason |
|---|---|---|
| Cross-agent provenance is a new problem invented by P002 | CONTRADICTED | 2026 provenance literature explicitly identifies multi-agent provenance and semantic transformation lineage. |
| Typed provenance graphs for agents are novel to P002 | CONTRADICTED | Existing survey/framework literature describes typed execution/evidence graphs. |
| Claim-level source attribution is novel to P002 | CONTRADICTED | Existing attribution/provenance systems address claim-level support and source ownership. |
| Provenance-bearing memory is novel to P002 | CONTRADICTED | Existing literature explicitly studies/frames it, though it remains underdeveloped. |
| Robust semantic provenance across transformed inter-agent claims is fully solved | UNSUPPORTED / CONTRADICTED BY REVIEW | The reviewed survey explicitly describes it as an open problem. |
| Education-specific integration of cross-agent semantic provenance + pedagogical-decision provenance + learner-independence evaluation is an established gap | UNDER REVIEW | No reviewed evidence yet establishes absence or uniqueness of this combination. |

## Revised surviving hypothesis

P002 should no longer be framed as inventing provenance technology.

A defensible research direction, if it survives further prior-art review, may instead be:

> Apply and evaluate provenance-aware agent architecture in an educational multi-role environment where source authority, AI-derived claims, inter-agent transformations, pedagogical decisions, and learner outcomes remain explicitly distinguishable and auditable.

The potential contribution would need to come from the education-specific architecture/evaluation and empirical result, not from claiming ownership of generic provenance concepts.

## Required falsification tests before GO

1. Determine whether OpenMAIC structurally carries source/evidence IDs through inter-agent messages and transformed claims, rather than only maintaining source ledgers around course generation.
2. Search educational systems specifically for claim graphs, semantic provenance, evidence contracts, provenance-bearing learner models/memory, and pedagogical-decision audit trails.
3. Determine whether any educational system already combines these with multi-role interaction and controlled comparison against a strong single-agent tutor.
4. Inspect ASTRA's actual trace schema and evaluation boundary; do not infer more than the paper establishes.
5. Compare generic provenance mechanisms (e.g. claim/evidence graphs and source-aware verification) against what P002 would need; reuse established ideas rather than relabeling them as novelty.
6. Define a falsifiable educational contribution. If the only remaining distinction is implementation packaging/UI, downgrade novelty and consider PARK or portfolio-only implementation.
7. Preserve privacy/security implications: provenance traces can contain learner data, source content, agent messages, model/tool outputs and potentially sensitive history. Trace minimization, access control, retention and selective disclosure must be designed before implementation.

## Decision

MORE RESEARCH.

P002 remains alive, but the novelty boundary is narrower. The strongest current direction is no longer "cross-agent provenance" by itself. It is the possible education-specific integration and evaluation of provenance-aware multi-agent pedagogy while preserving learner agency. That must now survive direct educational prior-art and implementation-level comparison.
