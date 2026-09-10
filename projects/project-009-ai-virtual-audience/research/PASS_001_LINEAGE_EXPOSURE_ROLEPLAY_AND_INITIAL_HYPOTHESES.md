# P012 — Interactive AI Virtual Audience
## Pass 001 — Lineage, Exposure, Roleplay, and Initial Hypotheses

Date: 2026-09-10
Canonical ID: P012
Previous ID: P009

## Original concept
A configurable simulated audience environment intended to help users practise speeches, presentations, interviews and related high-pressure communication situations. Users may create audience members/personas, choose scenario type and setting, deliver content, receive questions/reactions and repeat practice. The intended benefit includes confidence building, public-speaking practice, communication skills and reduced fear/nervousness. Clinical claims are not assumed.

## Pass 001 decision
MORE RESEARCH / EVIDENCE BUILD.

The generic product idea is heavily occupied. Virtual public-speaking exposure, interview simulation, configurable scenarios, AI personas, audience questions, performance feedback and multi-persona roleplay are established in research and current products.

## Historical and academic lineage
Virtual-reality exposure therapy for public-speaking anxiety is mature. Randomized trials from 2009 onward found VR-based interventions can reduce public-speaking anxiety; later consumer/self-guided and 360-degree approaches reported sustained improvements. A 2026 systematic review and meta-analysis of 13 randomized controlled trials found self-guided VRET associated with significant reduction in public-speaking anxiety, while effects for broader social-anxiety outcomes were less certain and heterogeneous.

Research has also manipulated audience properties directly. Self-guided virtual-audience systems have varied audience size and reaction to create graded social threat. A 2026 randomized-trial protocol specifically tests graded interviewer reactions versus automated voice-prompt control, showing that responsive social-emotional audience behaviour is itself an active research variable rather than a novel concept.

Therefore novelty claims around virtual audiences, exposure, realistic reactions, graded difficulty, confidence building or anxiety reduction are not available without a much narrower experimental contribution.

## Commercial collision
Current products overlap strongly with the original feature set.

Yoodli supports configurable AI roleplays for presentations, interviews, sales and other high-stakes conversations; custom personas and scenarios; dynamic follow-up questions; screen sharing; custom rubrics; pressure/challenging interruptions; and multi-persona roleplays such as interview panels and group presentations.

VirtualSpeech supports virtual public-speaking environments and live audience-question practice.

Hence these product claims are not novel:
- customizable virtual audience;
- interview setting;
- company-presentation setting;
- AI interviewer;
- AI audience questions;
- dynamic follow-up questions;
- multiple AI personas/panels;
- speech/presentation analytics;
- pressure or hostile/challenging audience behaviour;
- confidence/public-speaking practice through repeated simulation.

## Clinical boundary
The platform may be useful for confidence-building or communication practice, but it must not be presented as treating anxiety disorders, psychological conditions or low self-esteem unless clinical evidence, appropriate supervision and regulatory/ethical requirements are satisfied.

For an undergraduate software/FYP project, the safer primary framing is communication-skills training and simulated practice, with public-speaking anxiety measures used only as research outcomes where ethically appropriate—not as a medical-treatment claim.

## Initial novelty threats
1. Generic virtual audience is old.
2. VR public-speaking exposure is old.
3. Audience realism/reaction manipulation is studied.
4. AI interviews are commercially mature.
5. AI follow-up questions are commercially mature.
6. Configurable scenarios/personas are mature.
7. Multi-persona roleplay is commercially available.
8. Automatic speech-delivery feedback is mature.

## Surviving candidate hypotheses

### H1 — Adaptive Audience Challenge Calibration
A simulated audience could adjust social/interaction challenge based on demonstrated user performance rather than using a fixed scenario. This survives only provisionally because adaptive exposure and difficulty calibration are established broadly.

### H2 — Transfer-Calibrated Practice
Instead of optimizing only in-simulation confidence or speech scores, evaluate whether practice with a simulated audience improves performance when assistance and familiar audience cues are removed in a later unseen scenario. This shifts the outcome from platform engagement to transfer.

### H3 — Audience-Model Fidelity vs Training Utility
Investigate which audience behaviours materially improve learning/transfer: attentive, distracted, skeptical, interruptive, supportive, hostile, expert-questioning, panel disagreement, etc. Generic audience realism is not novel, but a controlled comparison of behaviour realism versus training utility may be defensible if prior art does not already establish the same evaluation.

### H4 — Evidence-Bounded Audience Questioning
Audience agents could generate questions only from the user's uploaded presentation/material and their assigned stakeholder roles, with explicit unsupported/unknown handling. This would reduce arbitrary questions and make evaluation possible, but grounded Q&A and role-conditioned agents are already mature technologies; this is at most a supporting mechanism unless a stronger experimental gap is found.

### H5 — Stressor-to-Skill Matching
The platform could diagnose performance weaknesses and select audience stressors specifically intended to train those weaknesses—for example interruption handling, hostile questioning, eye-contact pressure, uncertainty, time pressure or panel disagreement. This is potentially interesting but threatened by adaptive tutoring, exposure-therapy personalization and commercial roleplay systems.

## Strongest current research direction
The strongest current direction is not “build a realistic AI audience.” It is to study whether a controlled audience-challenge policy improves later independent communication performance better than static or user-chosen simulation.

Candidate research question:

> Can an adaptive virtual-audience challenge policy improve transfer to unseen presentation/interview scenarios while avoiding excessive user distress or overfitting to familiar audience behaviours, compared with fixed and self-selected audience simulations?

This is provisional and must be attacked directly in Pass 002.

## Candidate baselines
- B0: record-yourself / no simulated audience.
- B1: static neutral audience.
- B2: fixed challenging audience.
- B3: user-selected difficulty/audience.
- B4: adaptive challenge policy based on prior performance.

## Candidate outcomes
Communication performance:
- response relevance/completeness;
- speech structure;
- fluency/disfluency;
- response latency;
- handling of interruptions/questions;
- independent evaluator score;
- unseen-scenario transfer.

User-state outcomes, with ethical caution:
- self-reported confidence;
- perceived difficulty;
- subjective anxiety/arousal if approved for study.

System outcomes:
- adaptation accuracy/appropriateness;
- question grounding;
- scenario consistency;
- latency and cost.

## Feasibility
A non-VR web prototype is feasible on modest hardware using browser audio/video, speech-to-text, configurable 2D/3D avatars, an LLM/API for role-conditioned dialogue, deterministic scenario/rubric logic and a lightweight backend/database. Full immersive VR is not necessary to test the core research question.

## Pass 002 requirement
Directly attack adaptive challenge calibration, graduated exposure, adaptive virtual audiences, difficulty personalization, stress inoculation, transfer-of-training and real-world/generalization evaluation. If the exact adaptation/transfer contribution is already established, do not manufacture novelty by adding more persona attributes.
