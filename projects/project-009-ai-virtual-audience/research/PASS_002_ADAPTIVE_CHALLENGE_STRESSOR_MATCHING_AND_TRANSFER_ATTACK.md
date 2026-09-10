# P012 — Interactive AI Virtual Audience
## Pass 002 — Adaptive Challenge, Stressor Matching, and Transfer Attack

**Canonical ID:** P012 (previously P009)
**Project:** Interactive AI Virtual Audience
**Date:** 2026-09-10
**Research state:** EVIDENCE BUILD
**Decision:** MORE RESEARCH

## 1. Corrected project premise
AJ's original concept is a configurable simulated audience for speeches, presentations, interviews and other high-pressure communication situations. The product goal is repeated practice that improves confidence and communication ability. Clinical treatment claims are not assumed.

Pass 001 already rejected generic novelty claims around virtual audiences, AI interviewers, presentation simulators, configurable personas, audience questions, multi-persona panels, generic confidence training and generic speech analytics.

The strongest remaining directions entering Pass 002 were adaptive audience challenge, stressor-to-skill matching and transfer to unseen scenarios.

## 2. Prior-art attack: graded and adaptive exposure
Graded exposure is mature. Prior public-speaking VRET work has varied audience size and social threat across sessions. Self-guided systems have allowed participants to increase audience size, audience reaction, prompts and self-salience. Personalized exposure based on real-time arousal and physiological measurements has also been studied.

A 2021 AIIDE framework explicitly proposed automated personalized virtual-reality exposure therapy using physiological measurements, machine learning and experience-driven procedural content generation, including fear of public speaking as a target domain.

Therefore the following cannot be claimed as novel:
- gradually increasing audience difficulty;
- adapting social threat to anxiety/arousal;
- user-controlled exposure progression;
- physiological personalization;
- generic 'AI chooses the right difficulty'.

## 3. Prior-art attack: audience attitude and stressor manipulation
Audience behaviour is already an experimental variable. Existing work has compared supportive versus unsupportive/hostile audiences, manipulated audience size and attitude, and measured subjective, behavioural and physiological responses. A 2026 Scientific Reports study showed that unsupportive virtual audiences induce greater negative affect, arousal, anxiety and social/cognitive effort. A 2026 Behaviour & Information Technology study manipulated audience size and encouraging/critical attitude.

Therefore the following are not novel:
- supportive versus hostile audiences;
- larger versus smaller audiences;
- audience distraction/negative evaluation as stressors;
- audience realism as a mechanism for inducing anxiety;
- measuring heart rate or self-reported nervousness during exposure.

## 4. Prior-art attack: adaptive AI interview and coaching systems
Current interview simulators already adapt question difficulty to responses, follow up on weak answers, personalize by role/seniority and produce structured performance feedback. 2026 VR public-speaking research also reports performance-contingent LLM-driven coaching and longitudinal follow-up.

Therefore generic adaptive questioning, adaptive difficulty, personalized coaching, competency scoring and weak-answer follow-up cannot support novelty.

## 5. Transfer/generalization is established, but incompletely aligned
Transfer from simulated practice to later real or in-vivo performance is not a new idea. Public-speaking VR studies have evaluated subsequent real-world or Zoom presentations, and VRET trials have explicitly included transitions to in-vivo practice and follow-up outcomes. A 2023 Scientific Reports experiment found that supportive virtual-audience practice affected later instructor-rated speaker confidence in a real university-course presentation.

Therefore 'we test whether VR practice transfers to the real world' is itself not novel.

However, targeted search in this pass did not identify a direct study of the exact conjunction below:

1. infer a user's specific communication-performance weakness;
2. select a corresponding audience stressor rather than a generic harder/easier level;
3. train under that stressor;
4. evaluate performance on a deliberately unfamiliar audience/scenario where the training controller is absent;
5. compare against static, self-selected and generic adaptive-audience baselines.

This is a NOT-FOUND result, not proof of uniqueness.

## 6. Hypothesis migration

### H1 — Adaptive audience challenge calibration
**Status: DEMOTED / not novelty.**
Adaptive exposure and adaptive interview difficulty are already established.

### H2 — Transfer-calibrated practice
**Status: SURVIVES AS EVALUATION REQUIREMENT, not sufficient novelty.**
Transfer testing is established, but is necessary to prevent misleading in-simulation success claims.

### H3 — Audience-model fidelity versus training utility
**Status: DEMOTED.**
Audience realism, social presence, supportive/unsupportive behaviour and design variables are already well studied. Could remain a secondary factor.

### H4 — Evidence-bounded audience questioning
**Status: SUPPORTING ARCHITECTURE.**
Grounded questioning is useful but RAG/grounded Q&A is mature.

### H5 — Stressor-to-skill matching
**Status: SURVIVES, NARROWED.**
The surviving direction is not generic adaptation to anxiety. It is performance-deficit-specific selection of a social/interaction stressor, followed by evaluation on unseen transfer tasks.

Examples:
- interruption-recovery weakness -> controlled interruption stressor;
- weak response to challenge -> skeptical follow-up stressor;
- disorganized answers under pressure -> time-pressure + follow-up stressor;
- poor handling of expert scrutiny -> evidence-demanding expert persona;
- panel-turn-taking difficulty -> multi-persona panel stressor.

The system must not infer clinical diagnoses.

## 7. Candidate H6 — Transfer-Constrained Stressor Matching
**UNVERIFIED HYPOTHESIS**

> A communication-practice system that selects audience stressors from observed performance deficits may improve performance on unseen high-pressure speaking scenarios relative to static, self-selected and generic difficulty-adaptive virtual audiences, without causing unacceptable degradation in task completion or user-reported tolerability.

The contribution would be a bounded training-policy evaluation, not invention of virtual audiences, exposure therapy, adaptive difficulty, AI interviewing or public-speaking feedback.

## 8. Candidate baselines
- **B0:** solo recording / no audience.
- **B1:** static neutral audience.
- **B2:** static challenging audience.
- **B3:** self-selected difficulty/audience.
- **B4:** generic adaptive difficulty based on overall performance or self-rated difficulty.
- **B5:** proposed weakness-to-stressor matching policy.

B5 must not receive privileged knowledge of the final transfer task.

## 9. Candidate weakness/stressor taxonomy
A bounded implementation should avoid vague psychological labels and use observable communication-performance variables.

Potential weakness classes:
- W1: interruption recovery;
- W2: answer organization under time pressure;
- W3: handling skeptical/challenging questions;
- W4: evidence/justification under scrutiny;
- W5: multi-person turn-taking;
- W6: latency/freezing after unexpected questions;
- W7: maintaining topic relevance after conversational disruption.

Potential stressors:
- S1: mid-speech interruption;
- S2: rapid follow-up;
- S3: skeptical audience reaction;
- S4: evidence-demanding expert question;
- S5: multi-person panel;
- S6: strict time limit;
- S7: unexpected but scenario-relevant question.

## 10. Evaluation requirement: unseen transfer
The main outcome must not be performance inside the same adaptive simulator.

A valid evaluation should include an unseen transfer condition varying several dimensions:
- different audience identities/voices;
- different question wording;
- different topic or role context;
- different ordering of stressors;
- removal of adaptation/coaching during final test.

Primary metrics could include:
- independent performance rating;
- interruption-recovery success;
- answer relevance/completeness;
- response latency;
- task-specific communication errors;
- transfer gain from pre-test to unseen post-test.

Secondary metrics:
- self-rated confidence;
- perceived difficulty;
- tolerability;
- willingness to repeat practice.

## 11. Falsification conditions
H6 fails if:
1. B5 does not outperform B3/B4 on unseen transfer;
2. gains are confined to familiar training scenarios;
3. inferred weaknesses are unstable or poorly reproducible;
4. generic adaptive difficulty performs equally well;
5. stressor matching increases distress/tolerability problems without transfer benefit;
6. the policy depends on labels unavailable during real use;
7. results disappear under paraphrased questions/new audience identities;
8. evaluation relies only on LLM self-scoring without independent or rubric-based validation.

## 12. Clinical and ethical boundary
The project should be framed as communication practice and high-pressure interaction training. It should not claim diagnosis or treatment of social anxiety disorder, low self-esteem or other mental-health conditions without clinical design, oversight and validation.

If anxiety/confidence measures are included, they should be secondary outcomes or user-experience variables unless appropriate clinical research governance is established.

## 13. Feasibility
A non-VR web prototype is sufficient for the research question. Candidate implementation:
- browser microphone/camera optional;
- speech-to-text;
- scenario manager;
- multiple audience personas;
- deterministic weakness/stressor taxonomy;
- LLM for dialogue generation constrained by persona/scenario/source material;
- simple performance feature extraction;
- policy controller choosing stressors;
- database for sessions and evaluation data.

No GPU is required. VR, photorealistic avatars, gaze tracking and physiological sensors are optional extensions, not prerequisites.

## 14. Pass 002 conclusion
Generic adaptive audience difficulty does not survive novelty attack. Transfer-to-real-world evaluation is important but already established. The strongest remaining candidate is **H6 — Transfer-Constrained Stressor Matching**, where observable communication deficits determine which audience interaction stressor is selected and success is judged on unseen independent scenarios.

**Decision: MORE RESEARCH.**

Pass 003 must directly search for adaptive social-skills/public-speaking systems that diagnose skill-specific weaknesses and prescribe matched virtual stressors, as well as transfer-of-training, stress inoculation, deliberate practice and adaptive scenario-selection literature. If direct collision is found, P012 should be killed rather than narrowed artificially.
