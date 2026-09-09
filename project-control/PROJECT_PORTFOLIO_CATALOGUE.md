# AJ Project Portfolio — Project Catalogue

## Purpose
This is the canonical short-form registry of current AJ Project OS project ideas. It records what each project means before portfolio-wide research, prior-art analysis, feasibility review, and implementation. Titles are working titles and may change only through an explicit project decision.

## Portfolio rule
No project is to be called unique, first-of-its-kind, unprecedented, secure, production-ready, or otherwise stronger than the available evidence supports. Research must distinguish VERIFIED FACT, REASONED INFERENCE, UNVERIFIED HYPOTHESIS, and UNKNOWN. Absence from search results is not evidence of non-existence.

### Project 001 — Source-Grounded AI Presentation, Interview and Defense Simulator
An AI-assisted rehearsal environment in which users provide their own documents, reports, slides, research materials, or other sources and face configurable virtual reviewers. It generates evidence-grounded questions, accepts typed or spoken answers, conducts bounded follow-up questioning, and returns explainable qualitative feedback tied to authoritative source evidence. Potential contexts include academic defenses, presentations, interviews, oral examinations, and professional reviews.

**Status:** PAUSED — implemented prototype under verification. Do not restart from scratch.

**Pause point:** The prototype has implemented and live-tested major flows including document ingestion/provenance, lexical retrieval, provider-backed grounded questions and qualitative evaluation, bounded multi-turn questioning, microphone transcription, local browser reviewer speech, and reviewer playback controls. Latest user-reported Windows regression result before the pause: `146 passed, 2 warnings`, with zero test failures. Playback UI includes Play/Replay, Pause, Resume, Stop, and speed selection. A UX gap was identified at the pause: the workspace exposes Question History but no obvious Defense Session History for reopening complete multi-turn sessions; session-level previous/next navigation still requires proper implementation/verification. Semantic retrieval also remains a future verification/implementation area rather than something to assume complete.

### Project 002 — AI-Powered Virtual Classroom and Adaptive Learning Environment
A virtual learning environment in which users provide learning materials and interact with configurable AI teachers, tutors, or classroom personas. The concept may include lessons, questioning, explanations, discussion, different teaching styles, speech, classroom roles, and later richer visual interaction. Research must establish how this differs meaningfully from historical teaching machines, intelligent tutoring systems, conversational tutors, LMS/MOOC systems, RAG tutors, and current AI study products.

**Status:** RESEARCH REQUIRED BEFORE IMPLEMENTATION.

### Project 003 — Small Educational Language Model From First Principles
An educational project investigating how a small language model can be designed, trained, evaluated, and operated from the transformer/model foundations rather than merely wrapping a commercial LLM API. It should expose tokenization, embeddings, attention, transformer blocks, training, inference, evaluation, computational limits, and failure modes. It must not imply that an individual project can reproduce frontier-scale infrastructure without evidence and resources.

**Status:** FEASIBILITY AND RESEARCH REQUIRED.

### Project 004 — Gamified School Achievement, Rewards and Digital Economy System
A school-oriented platform that converts selected academic, extracurricular, behavioral, or institutional achievements into a governed points/reward economy. Students could earn, track, and potentially spend or exchange points under institutional rules. Research must address motivation, fairness, incentive design, abuse/fraud resistance, accessibility, governance, privacy, and whether a digital economy adds real educational value rather than superficial gamification.

**Status:** CONCEPT STAGE; PROBLEM AND INCENTIVE MODEL REQUIRE RESEARCH.

### Project 005 — Intelligent Online Chess Platform
An online chess environment combining normal chess play with selected communication and intelligent-support capabilities. Candidate directions include voice/video interaction, AI-assisted rule/arbitration support, session management, and clearly separated modes in which outside assistance is either prohibited or explicitly allowed. Existing chess platforms, engines, fair-play systems, communication features, and anti-cheating approaches must be reviewed before differentiation is claimed.

**Status:** RESEARCH AND DIFFERENTIATION REQUIRED.

### Project 006 — Privacy-Aware Searchable Digital Activity and Screen Memory System
A user-controlled system intended to help people recover information they previously saw or worked with on a computer. Candidate functions include selective screen/activity capture, chronological organization, OCR or other extraction, activity segmentation, semantic/lexical search, and questions such as “Where did I see this?” Privacy, consent, storage, encryption, retention, security, indexing cost, OS integration, and existing activity-recall systems are central to feasibility.

**Status:** RESEARCH REQUIRED; PRIVACY AND SECURITY ARE FIRST-CLASS CONSTRAINTS.

### Project 007 — Secure Coding Examination, Execution and Evidence-Based Integrity Platform
A purpose-built programming examination environment with an integrated editor/execution workflow and configurable examination controls. Candidate evidence may include execution history, focus/tab events, clipboard events, and other bounded integrity indicators. The system should not automatically label a student a cheater merely because an event occurs; it should preserve contextual evidence for authorized human review. Research must cover online judges, computer-based testing, plagiarism/integrity systems, lockdown/proctoring approaches, AI-era assessment, accessibility, privacy, security, and false-positive risk.

**Status:** STRONG CANDIDATE; PRIOR-ART, SECURITY, ASSESSMENT, AND ETHICS RESEARCH REQUIRED.

### Project 008 — Independent Wireless Earbud Audio Routing and Multi-Device Communication System
An investigation into whether left and right wireless earpieces can operate with greater independence than conventional paired playback, such as receiving different sources, devices, channels, or communication roles. Feasibility is likely constrained by Bluetooth generations/profiles, LE Audio, operating-system audio routing, firmware, chipset behavior, synchronization, latency, radio architecture, and hardware design. No implementation commitment should occur before these constraints are established.

**Status:** TECHNICAL FEASIBILITY MUST BE ESTABLISHED FIRST.

### Project 009 — Interactive AI Virtual Audience for Presentation and Public-Speaking Rehearsal
A simulated audience environment for practicing speeches, presentations, pitches, lectures, interviews, and other live communication. Configurable audience members could ask questions, challenge claims, represent different expertise levels or attitudes, and potentially provide feedback. It overlaps Project 001 substantially; research must determine whether it has an independently defensible problem/architecture, should become a broader layer around Project 001, or should ultimately merge with it.

**Status:** RESEARCH REQUIRED; RELATIONSHIP TO PROJECT 001 UNRESOLVED.

### Project 010 — Original Party-Based Fantasy Action RPG
An original game concept inspired at a high level by the appeal of ensemble fantasy adventures such as *The Legend of Vox Machina*: a party of distinctive characters, complementary abilities, fantasy combat, exploration, narrative progression, and team dynamics. The project must not copy protected characters, storylines, dialogue, artwork, locations, or other protected expressive elements. Research should verify related licensed games and adjacent fantasy party/action RPGs before making market or novelty claims, then identify an original gameplay and narrative identity.

**Status:** CONCEPT / RESEARCH STAGE. NO CLAIM THAT SUCH A GAME HAS NEVER EXISTED UNTIL VERIFIED.

## Portfolio-wide research protocol
Where applicable, each project proceeds through: discovery → genuine historical lineage → academic literature → current state of practice → commercial systems → open-source implementations → patents/standards/regulation where relevant → competing and failed approaches → prior-art matrix → gap analysis → novelty threats → problem definition → evidence-backed differentiation → feasibility → security/privacy/ethics → architecture candidates → rejected alternatives → go/park/kill recommendation → implementation.

Historical research goes back only as far as the real intellectual or technological lineage warrants; it is not artificially forced into a century-by-century narrative.
