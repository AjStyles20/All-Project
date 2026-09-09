# Project 002 — Research Pass 005
## Competition, Governance, Open-Source Prior Art, and Product Reframing

**Date:** 2026-09-09
**Status:** EVIDENCE BUILD / ADVERSARIAL PRIOR-ART REVIEW
**Decision:** MORE RESEARCH — no implementation approval and no novelty conclusion.

## Purpose
This pass tests whether Project 002 still has a defensible reason to exist after examining current open-source classroom systems, peer-reviewed multi-agent classroom work, governance/privacy guidance, and adjacent educational-agent implementations. It deliberately searches for systems that could invalidate broad novelty claims.

## 1. Strongest new novelty threat: OpenMAIC
Direct repository inspection of the current OpenMAIC project shows a materially broader overlap with Project 002 than the earlier SimClass paper alone suggested.

OpenMAIC describes itself as an open-source multi-agent interactive classroom. Its documented current feature set includes:
- turning a topic or attached reference materials into a lesson;
- AI teachers and AI classmates interacting in real time;
- generated slides and quizzes;
- interactive HTML simulations;
- project-based learning activities;
- whiteboard interaction;
- text-to-speech and speech-related provider support;
- discussion/roundtable/Q&A modes;
- responsive use across devices;
- export of classroom content;
- multiple cloud LLM providers;
- local-provider options including Ollama/Lemonade;
- an access-code authentication mechanism;
- classroom export/import;
- interactive 3D, games, mind maps, and browser programming in its newer releases.

**Evidence state:** VERIFIED from direct current repository README inspection on 2026-09-09.

**Novelty consequence:** the following can no longer be treated as meaningful standalone novelty for Project 002: “upload material and generate a classroom,” “AI teacher plus AI classmates,” “multi-agent classroom,” “voice classroom,” “whiteboard,” “quiz generation,” “interactive simulation,” “project-based learning,” “local-model option,” “multi-provider support,” “responsive/mobile classroom,” or “exportable AI lessons.”

This is a major novelty threat, not a reason to hide or minimize the competitor.

## 2. SimClass relationship clarified
Direct inspection of the SimClass repository confirms that the NAACL 2025 research repository points to the broader MAIC platform for implementation. The peer-reviewed ACL Anthology record describes representative classroom roles, automatic class control, real-user participation, teacher-student and student-student interaction, and experiments in two real-world courses.

**Evidence state:** VERIFIED from ACL Anthology and direct repository inspection.

**Implication:** Project 002 must compare itself against the MAIC/SimClass lineage as a family of related research and implementations rather than treating SimClass as an isolated paper.

## 3. Other current open-source/agentic education evidence
Discovery also identified:
- AgentSchool: a multi-agent educational simulation platform modelling a teacher and multiple students, evolving memory/cognitive state, exercises, questionnaires, logs, evaluation, runtime inspection, pause/resume and rollback. This is relevant to simulated learner state and experimental classroom orchestration.
- EduAgent: a lightweight multi-agent teaching framework with plan/execute/reflect orchestration, specialized educational agents, memory, RAG, learning-path generation and assessment/progress functionality.
- Instructional Agents: an EACL 2026-associated multi-agent instructional-design system based on ADDIE for automated course generation/evaluation, including interactive/copilot workflow and multiple output formats.

These findings further weaken novelty claims based simply on agent specialization, orchestration, curriculum generation, adaptive roles, memory, RAG, or automated educational content production.

**Evidence state:** DISCOVERY/SUPPORTED from public project records; deeper code-level equivalence review remains pending for each project.

## 4. Governance, minors, privacy, and human oversight are product requirements
UNESCO's guidance on generative AI in education advocates a human-centred and age-appropriate approach, including data-privacy protection, age considerations for independent GenAI interaction, pedagogical/ethical validation, equity and inclusion. UNESCO's 2025 rights-of-learners work also emphasizes privacy, safety, governance, equity and the risk of widening inequality.

**Evidence state:** VERIFIED from official UNESCO materials.

### Design consequence
If Project 002 is intended for school-age learners, privacy/minor protection cannot be postponed until deployment. Before implementation approval, the project needs at minimum:
- a declared target age/user population;
- data-flow and retention model;
- role/permission model for learner, educator and administrator where applicable;
- explicit handling of uploaded educational material and learner conversation history;
- provider-data boundary and local/cloud processing policy;
- deletion/export controls;
- moderation/safety policy appropriate to age/context;
- human override/review path;
- accessibility requirements;
- clear statement of which educational decisions the AI is not authorized to make autonomously.

The exact legal obligations depend on jurisdiction and deployment context and therefore remain **UNKNOWN until target market/context is selected**. Do not prematurely label the product FERPA/COPPA/GDPR/NDPA compliant merely because design controls exist.

## 5. Updated product hypothesis
The original broad product hypothesis — “a virtual classroom with AI teachers/classmates, uploaded resources, speech and interactive learning” — is now too heavily occupied by prior art to serve as the core contribution.

A narrower research hypothesis survives:

> Can a source-provenance-preserving, pedagogically governed AI learning environment make multi-role interactions inspectable and evidence-bounded, deliberately preserve learner agency, and demonstrate measurable value over a strong single-agent tutor under equivalent content/model conditions?

This is **not yet a novelty claim**. It is a falsifiable research/product hypothesis.

## 6. Candidate differentiators after Pass 005
The following remain UNDER REVIEW:

### 6.1 Cross-role provenance contract
Every factual educational claim made by teacher, peer, challenger or evaluator role should be traceable to authoritative course/source evidence when the task is source-grounded. Roles should not silently inherit unsupported statements from other agents.

### 6.2 Pedagogy as inspectable policy, not hidden prompt text
Teacher/administrator should be able to inspect why the system selected a hint, challenge, remediation, peer discussion, retrieval source or progression decision. This could distinguish orchestration policy from persona theatre.

### 6.3 Anti-offloading modes
Assistance policy should support learner-first attempts, staged hints, justification requirements, source verification, delayed answers and independent post-assistance testing. The system should be evaluated for retained competence rather than only convenience.

### 6.4 Strong baseline comparison
Any research evaluation should compare the multi-role system against a competent source-grounded single-agent tutor using equivalent source material and, where practical, equivalent underlying model capability. A weak chatbot baseline would not establish useful multi-agent value.

### 6.5 Graceful low-resource mode
Investigate whether useful source-grounded learning can continue with local/cheap components or reduced functionality when premium generative services are unavailable. Existing local-model support in OpenMAIC means “works locally” alone is not novel; the possible differentiator would be trustworthy degradation with explicit capability/provenance states and modest resource targets.

### 6.6 Teacher-governed autonomy
Investigate explicit controls over what agents may explain, ask, assess, store, infer or escalate. Human-teacher augmentation may be more defensible than autonomous replacement.

## 7. Newly rejected standalone novelty claims
Project 002 must not use these as primary novelty claims without a much narrower demonstrated distinction:
- AI virtual classroom;
- AI teacher;
- AI classmates/peers;
- multi-agent classroom;
- uploaded-document lesson generation;
- RAG/course grounding by itself;
- quizzes/slides/whiteboard;
- TTS/ASR;
- simulations/games/PBL;
- adaptive or personalized teaching;
- learner-state simulation;
- curriculum generation;
- local LLM support;
- multi-provider LLM support;
- responsive/mobile access;
- open-source availability.

## 8. New kill / park criteria
Project 002 should be PARKED or materially reframed if research shows any of the following:
1. The surviving provenance/governance/anti-offloading combination is already substantially implemented and evaluated by current systems.
2. Multi-role interaction produces no meaningful learning, retention, transfer, agency or engagement benefit over a simpler strong tutor while adding significant cost/latency/error surface.
3. The only remaining differentiation is visual simulation/persona presentation rather than a defensible educational mechanism.
4. Privacy/safety requirements for the intended population make the proposed architecture impractical within available resources.
5. Required model/API/infrastructure costs make the intended accessible deployment unrealistic and no credible degraded mode exists.
6. Evaluation cannot be designed so that the claimed contribution is falsifiable.

## 9. Next evidence targets
Before a GO decision, continue with:
- detailed OpenMAIC architecture/security/data-flow inspection;
- AgentSchool and other current code-level comparison;
- patent search using appropriate patent databases/search systems rather than ordinary web snippets alone;
- accessibility requirements and WCAG-aligned interaction review;
- Nigeria/Africa-specific education, connectivity, device and data-protection context if that becomes a target deployment context;
- direct target-user/problem validation rather than assuming students/teachers want a simulated classroom;
- cost/latency benchmark design;
- a formal feature/prior-art matrix comparing P002, OpenMAIC/MAIC, SimClass, AgentSchool, OATutor, Khanmigo and a strong single-agent RAG tutor;
- direct tests of whether cross-role provenance and inspectable pedagogy are actually absent or materially weaker in prior systems.

## 10. Current decision
**MORE RESEARCH.**

Project 002 remains alive, but the broad original concept is no longer sufficient. The research process is doing its intended job: prior art is forcing the potential contribution toward a narrower, testable and more defensible problem.
