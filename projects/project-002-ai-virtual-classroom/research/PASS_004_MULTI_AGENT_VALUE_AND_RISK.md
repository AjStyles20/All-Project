# Project 002 — Research Pass 004: Multi-Agent Value, Pedagogical Agents, and Cognitive Risk

## Status
EVIDENCE BUILD / ADVERSARIAL GAP REVIEW. This file extends `RESEARCH_DOSSIER.md`; it does not approve implementation or establish novelty.

## Central question
Does an AI teacher plus simulated AI classmates create educational value beyond a simpler, well-designed single AI tutor, or does it mainly add interface realism, latency, cost, inconsistency, and additional hallucination surface?

**Current answer:** UNKNOWN IN GENERAL. Evidence supports educational agents and AI-supported collaborative learning in some contexts, but the evidence reviewed does not justify a general claim that a multi-agent virtual classroom is superior to a single-agent tutor.

## Evidence added in this pass

### 1. AI agents in collaborative learning are established prior art
A 2026 systematic review by Ba, Shi, Wu, and Lu synthesized 46 empirical studies published from 2014–2025 on AI agents in computer-supported collaborative learning. The review reports agent functions including cognitive scaffolding, social facilitation, and instructional orchestration. Cognitive gains were reported consistently across the reviewed corpus, while behavioral, social, and emotional outcomes were more context-dependent.

**Implication:** collaborative agents, group facilitation, and orchestration are not Project 002 novelty. The open question is comparative value and design quality.

**Claim state:** VERIFIED at systematic-review level.

### 2. K–12 ITS evidence remains positive but conditional
Létourneau et al. (2025) reviewed 28 K–12 ITS studies involving 4,597 students. Effects on learning/performance were generally positive, but were mitigated when ITS were compared against non-intelligent tutoring systems. The authors call for longer interventions, larger/diverse samples, and ethical investigation.

**Implication:** adding more AI/intelligence is not itself evidence of educational superiority. Project 002 needs an active comparator, not a weak no-support baseline.

**Claim state:** VERIFIED.

### 3. Pedagogical/virtual characters can help, but effects are moderated
A 2013 meta-analysis of 43 pedagogical-agent studies (3,088 participants) reported a small statistically significant learning effect and important moderators. A 2025 K–12 meta-analysis reported positive learning and motivation effects for virtual characters, while not finding significant effects for several other outcomes such as cognitive load in the reported synthesis. Other recent meta-analytic work continues to show that cognitive-load effects depend on role, appearance, subject, media combination, duration, and pacing.

**Implication:** an avatar, peer, teacher character, voice, or visible classroom role is not a universal learning mechanism. Project 002 should treat embodiment and persona as experimentally optional layers whose value must be measured.

**Claim state:** SUPPORTED by multiple meta-analytic/review sources; applicability depends on population/task/design.

### 4. Pedagogical alignment matters more than “having a chatbot”
A 2026 meta-analysis/research synthesis on educational chatbots reports that learning performance varies with pedagogical approach and chatbot role. This reinforces a design principle already emerging in Project 002: role labels and personality prompts are insufficient. Agent behavior should be constrained by explicit instructional functions and learning-state transitions.

**Implication:** candidate differentiation should focus on inspectable pedagogical orchestration rather than the number of agents.

**Claim state:** SUPPORTED.

### 5. Multi-agent educational systems are advancing quickly
SimClass (NAACL 2025) already provides a multi-agent classroom simulation with representative classroom roles, automatic classroom control, real-user participation, and teacher-student/student-student interaction. SAGE (AAAI 2026) adds a compositional multi-agent framework for structured collaborative problem solving, combining pedagogical reasoning with autonomous dialogue and reporting real-student evaluation. AgentSchool (2026 preprint) proposes cognitively growable student agents with knowledge graphs, misconceptions, adaptive teachers, and longer-horizon social simulation.

**Implication:** the novelty window around “multi-agent AI classroom” is narrowing rapidly. Project 002 cannot depend on multi-agent architecture, classroom simulation, differentiated student personas, misconception modeling, adaptive teacher roles, or pedagogical orchestration alone as a durable novelty claim.

**Claim state:** SimClass and SAGE are VERIFIED from published venues; AgentSchool is PREPRINT / UNDER REVIEW and must not be weighted equivalently to peer-reviewed evidence.

### 6. Cognitive offloading and agentic autonomy are release-level research risks
A 2026 systematic review of agentic AI in education synthesizing 53 studies identifies methodological weaknesses in current research, including small synthetic benchmarks, weak/unfair baseline comparisons, and lack of longitudinal authentic-classroom testing. It also highlights risks around cognitive offloading, epistemic lock-in, and the need for human oversight.

**Implication:** Project 002 should not optimize for autonomous agent activity. It should optimize for learning. More autonomy is not automatically better. Human/teacher control, learner-first attempts, staged assistance, source verification, reflection, and independent post-assistance testing are candidate safeguards.

**Claim state:** VERIFIED at systematic-review level for the cited synthesis; causal magnitude of individual risks remains context-dependent.

## Adversarial novelty update
The following are now explicitly rejected as standalone novelty claims:
- multiple AI agents;
- AI teacher plus AI students;
- classroom simulation;
- peer-like educational agents;
- collaborative problem-solving agents;
- pedagogical role assignment;
- adaptive teacher agents;
- misconception-aware simulated students;
- conversational tutoring;
- avatars/virtual characters;
- source/RAG-grounded tutoring;
- learner modeling and adaptive sequencing;
- open-source adaptive tutoring;
- speech/TTS as an educational interface.

These capabilities may still be useful components. They simply cannot carry the novelty argument by themselves.

## Stronger candidate research directions — still hypotheses
1. **Provenance-preserving multi-role classroom:** every instructional claim from teacher/peer/tutor roles remains traceable to authoritative learner/course sources, with explicit distinction between sourced content, pedagogical inference, and model-generated simulation.
2. **Inspectable pedagogical state machine:** role behavior is governed by visible instructional objectives, learner state, evidence, and transition rules rather than opaque persona prompts.
3. **Comparator-first multi-agent evaluation:** the project is designed from the beginning to test multi-agent classroom interaction against a strong single-agent tutor using the same model, sources, task, and assistance budget.
4. **Anti-offloading learning protocol:** learner-first attempts, staged hints, explanation requirements, uncertainty/source checks, delayed assistance, and independent post-support assessment are built into the interaction protocol.
5. **Teacher-governed autonomy:** instructors can bound what agents may explain, ask, simulate, assess, or infer, and can inspect why an intervention occurred.
6. **Low-resource trustworthy degradation:** unavailable model/provider functions fail visibly while source-grounded learning and local material access remain usable; stale/model-only information is never presented as authoritative course evidence.
7. **Evidence-aware classroom simulation:** simulated peer misconceptions or viewpoints are explicitly labeled as simulations and cannot silently become factual evidence.

None is yet a proven gap or final contribution.

## Minimum evaluation needed if Project 002 reaches implementation
A credible evaluation should avoid a weak “system vs nothing” comparison. Candidate design:

- Condition A: learning materials without AI assistance.
- Condition B: strong single-agent source-grounded tutor.
- Condition C: Project 002 multi-role classroom using the same underlying model/source corpus where possible.
- Optional Condition D: multi-role classroom with anti-offloading safeguards disabled/enabled, if ethically and practically justified.

Measure at minimum:
- immediate learning;
- delayed retention;
- transfer to novel problems;
- independent performance after AI removal;
- factual/source accuracy;
- learner verification behavior;
- calibration/uncertainty handling;
- cognitive load;
- engagement/motivation;
- time on task;
- model calls/token/cost/latency;
- teacher/user control burden;
- accessibility failures;
- overreliance indicators.

Predefine primary outcomes and avoid selecting only favorable metrics after results are known.

## Kill / park criteria strengthened in this pass
Consider PARK or KILL if rigorous comparison shows that:
- multi-agent interaction does not materially outperform a strong single-agent tutor on the chosen educational objective;
- gains are limited to engagement/novelty while retention/transfer/independent performance do not improve;
- additional agents materially increase hallucination, inconsistency, latency, cost, or cognitive distraction without compensating benefit;
- the remaining contribution is only UI theater or persona styling;
- the claimed gap is already directly occupied by SimClass/SAGE/other systems after feature-level comparison;
- safe provenance and role isolation cannot be maintained;
- required provider/hardware costs make the intended deployment context unrealistic.

## Research still required before a novelty statement
- Full feature/evaluation extraction for SimClass and SAGE.
- Direct inspection of their available source code where accessible.
- Stronger search for direct single-agent vs multi-agent educational comparisons.
- Teachable-agent and learning-by-teaching primary studies.
- Negative/null pedagogical-agent studies and publication-bias evidence.
- Longitudinal studies of AI tutoring and dependency.
- Additional commercial systems beyond Khanmigo.
- More open-source systems with code-level inspection.
- Patent landscape for multi-agent tutoring/classroom simulation.
- Privacy, minors, education-record, accessibility, and regional regulatory constraints once intended users/deployment region are bounded.
- Cost and latency modeling using realistic class/session sizes.
- User/problem validation: identify who specifically needs a simulated classroom rather than a tutor and what measurable problem it solves.

## Decision after Pass 004
**MORE RESEARCH.** Project 002 remains alive, but its defensible contribution is becoming narrower and more testable. That is a positive outcome of the research process, not a weakness.
