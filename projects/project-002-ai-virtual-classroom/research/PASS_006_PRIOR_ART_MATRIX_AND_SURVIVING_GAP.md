# Project 002 — Research Pass 006
## Prior-Art Matrix, Stronger Novelty Threats, and Surviving-Gap Review

**Date:** 2026-09-09
**Status:** EVIDENCE BUILD / ADVERSARIAL GAP REVIEW
**Decision:** MORE RESEARCH — no implementation approval and no uniqueness claim.

## Purpose
This pass compares the surviving Project 002 hypothesis against the strongest prior art located so far, with particular attention to OpenMAIC's rapidly expanding current implementation. The goal is to identify which candidate differentiators remain plausible, which have been weakened, and what must be verified before Project 002 can receive a GO decision.

## 1. Material update: OpenMAIC moved again
Current public OpenMAIC material dated 2026-08-27 documents v1.0 with an agent workbench, durable course-building sessions, uploaded documents/audio/video, web-search material, course-level planning, component editing, reusable skills, provider-neutral capabilities, persistence, owner-scoped resources, and ownership restrictions on mutations. This is substantially broader than the version considered in earlier passes.

Direct repository inspection in the preceding pass already verified multi-agent classrooms, AI teachers/classmates, slides, quizzes, simulations, PBL, whiteboards, TTS, multiple providers and local providers. Current public repository/product material adds stronger course-authoring and state-management overlap.

**Novelty consequence:** Project 002 must not rely on course generation, editable AI-generated lessons, durable sessions, teacher-style configuration, local/cloud provider choice, document/media ingestion, agent rosters, or basic ownership controls as primary differentiators.

## 2. Important correction: inspectable pedagogy is under stronger threat
A recent independent source audit of a pinned OpenMAIC source tree reports that OpenMAIC represents teaching styles using prose instructions plus structural constraint sidecars that the runtime can check. This is not treated as primary evidence yet because the audit is third-party rather than our own pinned code inspection, but it creates a serious novelty threat to the candidate idea of "pedagogy as inspectable policy rather than hidden prompts."

**State:** NOVELTY THREAT — REQUIRES DIRECT CODE VERIFICATION.

**Required action:** inspect OpenMAIC's current skill/constraint/evaluation implementation directly before claiming that Project 002 uniquely makes pedagogy inspectable or machine-constrained.

## 3. Another stronger threat: provenance + pedagogical safeguards are not empty territory
Recent educational-AI work includes systems explicitly combining instructor-approved retrieval, pedagogical strategy selection, claim-level verification, and overreliance controls. EduGuard (2026 preprint) is especially relevant in programming education. A 2026 Frontiers study also compares a prompt-only tutor against an integrated learner-state-aware RAG tutor with pedagogical scaffolding.

These do not automatically duplicate Project 002, but they weaken any standalone claim based on:
- source-grounded RAG;
- pedagogical strategy selection;
- claim verification;
- learner-state-aware tutoring;
- overreliance controls;
- scaffolding instead of direct answers.

**State:** SUPPORTED NOVELTY THREAT; deeper primary-paper extraction required.

## 4. Prior-art capability matrix
Legend: **Y** = clearly established in evidence reviewed; **P** = partial/related; **U** = unknown/not yet verified; **N/A** = not central to that system. This matrix is an evidence map, not a product-quality ranking.

| Capability / research concern | OpenMAIC / MAIC | SimClass | OATutor | Khanmigo | Recent safeguarded RAG tutors | P002 surviving hypothesis |
|---|---:|---:|---:|---:|---:|---:|
| AI teacher/tutor | Y | Y | Y | Y | Y | Not differentiating |
| AI peers/classmates | Y | Y | U | N/A | N/A | Not differentiating |
| Multi-agent classroom/orchestration | Y | Y | N/A | U | U | Not differentiating |
| User/course material grounding | Y | P | Y/P | Y/P | Y | Not differentiating |
| Slides/quizzes/interactive activities | Y | P | P | P | U | Not differentiating |
| Speech / TTS | Y | P | P | U | U | Not differentiating |
| Local-provider option | Y | U | P | N/A | U | Not differentiating |
| Learner/adaptive state | P/Y | P | Y | P | Y/P | Not differentiating alone |
| Pedagogical constraints/policies | P/Y — direct audit pending | P | Y/P | P | Y/P | Candidate only if materially stronger/inspectable |
| Claim/source provenance visible across every role | U | U | U | U | P | Candidate gap, NOT established |
| Cross-agent prevention of unsupported claim inheritance | U | U | N/A | N/A | U | Candidate gap, NOT established |
| Explicit anti-offloading policy | U/P | U | P | Y/P | Y | Not differentiating alone |
| Independent post-assistance competence evaluation | U | U | U | U | U | Candidate research mechanism |
| Strong single-agent baseline comparison | U | U | N/A | N/A | P | Candidate evaluation contribution |
| Teacher-inspectable reason for each pedagogical transition | P/U | U | P/U | P/U | P/U | Candidate under direct prior-art threat |
| Trustworthy degraded/offline mode with explicit capability state | P | U | P | N/A | U | Candidate only if defined/tested narrowly |
| Human-governed autonomy boundaries | P | P | P | Y | P | Not differentiating alone |

The matrix intentionally uses U rather than N when absence has not been established. Search failure is not proof of absence.

## 5. What currently survives the adversarial comparison
The broad product does not survive as novelty. A narrower *combination plus evaluation protocol* may still survive:

> A multi-role educational environment in which source-grounded claims remain provenance-bound across agent boundaries; pedagogical actions are governed by explicit inspectable policy; assistance is constrained to preserve learner agency; and the entire multi-role mechanism is evaluated against an equivalently capable single-agent tutor for retention, transfer, independent performance, verification behavior, latency, cost and error surface.

This remains a **RESEARCH HYPOTHESIS**, not a novelty statement.

The potentially defensible contribution may therefore be less about inventing a virtual classroom and more about a **trust and evaluation architecture for agentic learning environments**.

## 6. Why learner agency remains central
A 2026 scoping review synthesizing 123 studies describes a dual pattern: scaffolded/augmentation-oriented GenAI use is associated with self-regulation, self-efficacy, feedback literacy and reflective engagement, while replacement-oriented use is associated with cognitive offloading, overreliance, dependence, uncritical uptake and weakened judgement. The review explicitly warns that these are heterogeneous configurative patterns rather than causal effect estimates.

A separate 2026 systematic review of 53 agentic-AI-in-education studies reports methodological weaknesses including small synthetic benchmarks, unfair baseline comparisons, and severe lack of longitudinal authentic-classroom testing, while highlighting cognitive offloading and human oversight.

**Implication:** Project 002 should treat strong baselines, independent competence and longitudinal/retention-oriented outcomes as core research design requirements rather than optional evaluation polish.

## 7. Product safety/governance comparison
Current Khanmigo guidance is useful as a state-of-practice benchmark. It explicitly tells learners to check multiple sources, frames the tutor as helping rather than completing work, uses moderation, and gives connected teachers/parents visibility into student interactions. Educator guidance warns about hallucinations, discourages PII in prompts, requires human review, and states that AI should not be the sole basis for student-performance decisions.

**Implication:** Project 002 cannot claim human-in-the-loop, anti-cheating guidance, moderation, privacy warnings, or educator oversight as novel. They are baseline governance expectations if the product serves learners, especially minors.

## 8. Stronger kill criteria after Pass 006
P002 should be PARKED or reframed if direct source inspection establishes that current OpenMAIC/adjacent systems already provide all of the following to a comparable degree:
1. machine-enforced/inspectable pedagogical policies;
2. role-by-role source provenance with cross-agent trust-boundary enforcement;
3. explicit anti-offloading assistance modes;
4. human-governed autonomy and ownership controls;
5. rigorous evaluation against strong single-agent baselines on retained independent competence.

Even if some implementation difference remains, P002 should also be parked if its additional multi-agent complexity cannot justify its cost, latency, attack surface and cognitive burden.

## 9. Next verification targets
1. Directly inspect OpenMAIC current source for skills, constraint sidecars, evaluation rules, source/provenance representation, ownership boundaries, prompt/data trust boundaries and agent-to-agent message handling.
2. Extract the full MAIC/JCST evaluation design and determine what was actually measured in the reported 700+ student validation.
3. Deep-read EduGuard and adjacent safeguarded RAG tutoring work for claim-level verification and overreliance controls.
4. Inspect AgentSchool and other open-source multi-agent education code for learner-state and experiment instrumentation.
5. Build a security/data-flow threat model: untrusted uploads, prompt injection, retrieval poisoning, cross-role contamination, cross-user leakage, provider exposure, moderation, minors, retention and deletion.
6. Build a feasibility/cost model suitable for modest hardware and Nigerian connectivity assumptions only if Nigeria is selected as a target context.
7. Conduct patent searching with a proper patent source before making patent-landscape conclusions.
8. Validate the actual user problem with learners/educators before treating classroom simulation as desirable.

## 10. Current decision
**MORE RESEARCH.**

Project 002 is still alive, but the surviving contribution is becoming narrower. Current evidence suggests that the defensible research direction, if one survives, is likely to center on **cross-agent epistemic provenance + pedagogical governance + learner-agency preservation + rigorous baseline evaluation**, rather than the virtual-classroom interface itself.
