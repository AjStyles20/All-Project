# P002 Research Pass 009 — Decisive Intersection Gap Test

Date: 2026-09-09
Status: EVIDENCE BUILD / GAP REVIEW
Decision after this pass: MORE RESEARCH, narrowing toward a conditional GO candidate; implementation remains locked.

## Question
Does a defensible gap remain at the intersection of multi-agent education, cross-agent epistemic lineage, pedagogical-decision provenance, learner-state provenance, and preservation/evaluation of learner independence?

## Findings

### 1. Multi-agent tutoring plus auditable learner state is already prior art
IntelliCode (EACL 2026 System Demonstrations) uses a centralized, versioned learner state containing mastery estimates, misconceptions, review schedules and engagement signals. Six specialized pedagogical agents operate over shared state under a single-writer policy. The authors describe auditable mastery updates, graduated hints and curriculum adaptation. Therefore P002 must not claim novelty from multi-agent tutoring, persistent/versioned learner state, auditable mastery updates, specialized pedagogical roles, or graduated hints alone.

Evidence boundary: published system demonstration; reported validation uses simulated learners, so this does not establish real-student learning gains.

### 2. Learner-state-aware pedagogical RAG is already prior art
A 2026 Frontiers study compares a prompt-only tutor with an integrated learner-state-aware RAG tutor. It explicitly discusses controlled tutoring behavior, auditability and internal evidence/trace artifacts. The study also states that it did not collect student learning outcomes and that scripted learners were used. Thus learner-state-aware RAG, pedagogical control and audit traces cannot by themselves be P002 novelty.

### 3. Independent performance after AI removal is becoming an explicit evaluation target
Recent 2026 research distinguishes AI-supported performance from competence retained when support is removed. An eight-week writing study used an independent no-AI posttest and found that the condition producing the strongest AI-supported products did not produce the strongest independent no-AI profile; bounded support with reflection had the more favorable independent profile. The authors caution about class-level allocation and limited near-transfer scope.

Separate 2026 work distinguishes dependent offloading (AI substitutes for thinking) from autonomous offloading (AI scaffolds while cognitive agency remains with the user). This supports treating learner independence as a measurable design/evaluation dimension, but not as a P002 invention.

### 4. Generic agent provenance and cross-agent lineage are not P002 inventions
The 2026 survey "From Agent Traces to Trust" explicitly defines execution provenance across retrieved evidence, tools, memory, intermediate claims, actions and inter-agent messages. It identifies semantic provenance across transformations and multi-agent provenance as open research problems. It specifically calls for tracking how claims/evidence/messages/errors propagate across agents and for distinguishing provenance of user input, retrieved evidence, tool output, observation, reflection and other-agent messages.

Therefore P002 must not claim invention of typed provenance graphs, evidence tracing, claim-level provenance, cross-agent provenance, provenance-bearing memory, or responsibility attribution.

### 5. OpenMAIC code inspection: agent dispatch is structurally rich, but the inspected call-agent boundary does not establish semantic claim-lineage propagation
Current OpenMAIC source has a director loop and a call-agent tool. The call-agent input schema inspected in `lib/chat/pi/tools/call-agent.ts` includes an `agentId` and an `instruction` string. The runtime also supports request-scoped evidence attachments and scene evidence metadata, and other inspected parts of OpenMAIC have strong source grounding, untrusted-material fencing, claim/source ledgers, fact checking and structural pedagogy constraints.

However, this inspection does NOT yet establish a typed claim/evidence lineage object that accompanies every child-agent utterance and survives paraphrase/aggregation through subsequent agents. Absence from the inspected schema is not proof of absence elsewhere in the repository. Status remains PARTIAL / UNKNOWN pending targeted schema/event-store inspection.

## Novelty threats strengthened by this pass
The following are rejected as standalone novelty claims:
- multi-agent educational tutoring;
- centralized/versioned learner models;
- auditable mastery-state updates;
- specialized pedagogical agents;
- graduated hints;
- learner-state-aware RAG;
- pedagogical audit traces in general;
- evaluating cognitive offloading or independent no-AI performance in general;
- cross-agent provenance or typed provenance graphs in general.

## Candidate intersection that still survives — UNDER REVIEW
A narrower systems-and-evaluation contribution may remain if P002 can combine all of the following in one educational architecture and demonstrate why the combination matters:

1. **Authority-aware epistemic lineage** — distinguish authoritative source fragments, learner statements, model inferences, other-agent claims, memory summaries and external/tool evidence.
2. **Transformation-aware propagation** — when one agent paraphrases, combines, challenges or contradicts another agent's claim, preserve the derivation/support relation rather than reducing everything to plain conversation text.
3. **Runtime pedagogical-decision provenance** — record not merely the tutor response but the learner-state evidence, pedagogical policy/rule, selected intervention and resulting state transition that caused a hint/challenge/remediation/advance decision.
4. **Learner-agency controls** — staged assistance, learner-first attempts, reflection/justification, source inspection and assistance fading are explicit policies rather than optional prompt wording.
5. **Independent-learning evaluation** — compare supported performance with performance after assistance is removed; include retention/near transfer and, where feasible, delayed/farther transfer.
6. **Strong baseline comparison** — compare against a high-quality single-agent source-grounded tutor using equivalent material/model capability, not against no tutor or a deliberately weak baseline.
7. **Failure-oriented evaluation** — measure unsupported-claim propagation, source-authority corruption, learner-state corruption, inappropriate pedagogical interventions, latency/cost and recovery behavior.

No reviewed source currently proves that this exact intersection is absent from all existing systems. This is therefore a candidate gap, not a novelty statement.

## Falsifiable GO test
P002 should receive a research GO only if subsequent evidence supports all of these:
- a systematic prior-art search does not reveal an existing educational system substantially implementing the complete intersection above;
- the architecture can be reduced to an explainable prototype feasible on AJ's hardware/development constraints, using external model APIs only where justified;
- provenance overhead is bounded enough for interactive tutoring;
- a controlled evaluation can compare multi-role and single-agent conditions without changing multiple confounds at once;
- the project can measure learner-independent performance rather than only satisfaction or immediate answer quality;
- security/privacy design can prevent untrusted educational material or one agent's unsupported output from silently becoming authoritative state.

## PARK/KILL triggers
PARK or reframe if:
- targeted search finds a mature educational system already combining transformation-aware cross-agent claim lineage, pedagogical-decision provenance and learner-independence evaluation;
- multi-agent interaction cannot be isolated experimentally from UI/model/prompt differences;
- provenance becomes merely logging/citations rather than machine-checkable lineage;
- the remaining contribution is mainly avatars, classroom aesthetics, personas or feature aggregation;
- expected evaluation cannot test independent learning within realistic project constraints.

KILL the multi-agent classroom contribution if a strong single-agent tutor achieves comparable learning/independence outcomes with materially lower complexity, cost, latency and error-propagation risk, unless the multi-agent architecture demonstrates another independently valuable and evidenced function.

## Current decision
**MORE RESEARCH — CONDITIONAL GO CANDIDATE, NOT IMPLEMENTATION APPROVAL.**

The project has survived broad feature novelty attacks, but only as a substantially narrower research problem. The next pass should inspect OpenMAIC message/event/state persistence for typed evidence lineage, inspect IntelliCode's full architecture/evaluation limitations, search specifically for educational epistemic/decision provenance systems, and turn the surviving intersection into a prior-art comparison table with explicit YES / PARTIAL / NO / UNKNOWN cells.
