# Literature Screening — Project 001

## Scope
First-pass screening of literature relevant to public-speaking simulation, automated feedback, grounded question generation, and AI-assisted educational/review systems. This is not yet a systematic review.

## Evidence Themes

### 1. Simulated public-speaking practice is a legitimate research area
Recent and prior studies support the use of virtual or simulated audiences for public-speaking practice and anxiety-related interventions. Examples reviewed include work on VR public-speaking training, self-guided exposure, randomized controlled trials, and presentation-skill platforms.

**What this supports**
- simulation-based practice is technically and academically plausible
- repeated practice can be studied using measurable outcomes
- user experience, presence, anxiety, delivery, and performance can be evaluated separately

**What this does NOT support**
- claiming Project 001 will improve confidence or reduce anxiety without its own evaluation
- claiming VR is required for the MVP
- claiming automated feedback is objectively correct

### 2. Delivery metrics are already established in existing systems
Research and commercial systems commonly examine speaking pace, filler words, pitch/prosody, gaze/eye contact, body language, and related delivery features.

**Project implication**
Delivery analytics should be treated as a known supporting feature, not the core research novelty.

### 3. Automatic question generation is an established NLP research area
Automatic question generation has a substantial literature, including neural and LLM-based methods. Current discovery results confirm that question generation itself is not novel.

**Project implication**
The value must come from the grounding, review context, question strategy, traceability, or evaluation workflow—not merely generating questions with an LLM.

### 4. Retrieval-grounded educational question answering is an active area
Recent RAG research in educational contexts evaluates grounding LLM responses in external learning materials to improve fidelity and reduce unsupported output.

**Project implication**
A RAG-style architecture is technically defensible for grounding questions and feedback in user-provided materials, but its actual retrieval method and evaluation must be tested rather than assumed.

## Research Risk Identified
The initial concept overlaps strongly with existing commercial presentation-coaching systems. Therefore, Project 001 must avoid novelty claims based on:
- virtual audiences
- speech feedback
- AI follow-up questions
- uploaded slides
- interview simulation
- generic roleplay

## Candidate Research Focus
A stronger research/engineering focus is:

> How can an AI review simulator use a user's own source artifacts to generate traceable, role-specific challenge questions and evidence-aware feedback for technical presentations, vivas, defenses, and professional reviews?

Potential evaluation dimensions:
- grounding correctness
- question relevance
- source traceability
- coverage of important project claims/requirements
- hallucination rate
- persona differentiation
- usefulness ratings from users/reviewers
- repeat-session improvement in answer completeness or evidence use

## Current Status
- Public-speaking simulation evidence: SUPPORTED as background
- Automatic question generation: SUPPORTED as established prior art
- RAG for grounding: SUPPORTED as an established architectural approach, implementation-specific effectiveness not yet verified
- Project 001 novelty: UNDER REVIEW
- Confidence/anxiety improvement claim: UNSUPPORTED for Project 001
- Objective presentation-quality scoring claim: UNSUPPORTED for Project 001

## Next Research Actions
1. Expand comparable-system review beyond the first three products.
2. Screen papers specifically on AI oral-exam/viva/interview simulation.
3. Define a claim-safe research gap.
4. Design an evaluation protocol for grounding and question quality.
5. Keep delivery analytics secondary unless evidence justifies a stronger role.