# P009 — Personal Screen Memory System
## Pass 002 — Selective Capture, Task Resumption, Privacy Minimization and Prior-Art Attack

Date: 10 September 2026
Canonical ID: P009
Previous ID: P006

## Decision
MORE RESEARCH — generic task-context recovery and privacy-aware lifelogging are established; the strongest surviving hypothesis is a bounded optimization/evaluation problem: preserve task-resumption utility while reducing capture volume and privacy exposure.

## Direct prior-art collisions

### 1. Task resumption and context restoration are established
Research on interrupted work already studies how people reconstruct task state, which cues improve resumption, and how captured desktop context can support return to work. Prior work includes automated resumption cues for programmers, desktop screenshot thumbnails for restoring mental context, and task-context tracking systems that log windows, applications, documents, interaction history and related interface state.

Therefore the following are not approved novelty claims:
- restoring interrupted task context;
- using screenshots as resumption cues;
- logging windows/applications/documents for later resumption;
- showing recent artifacts to help a user continue work;
- building a task snapshot or task capsule.

### 2. Privacy-preserving lifelogging is established
Visual lifelogging research has long treated privacy as a first-class problem. Privacy-by-design, selective exclusion, visual degradation/redaction, local processing and privacy-aware capture policies are established directions.

Therefore the following are not approved novelty claims:
- adding privacy settings to a screen-memory tool;
- blurring/redacting sensitive content;
- excluding apps/sites;
- local-only storage;
- reducing capture merely to improve privacy.

### 3. Event-triggered and activity-aware capture are not novel by themselves
Existing screenomics and activity-trace systems use screen/activity events as anchors, and event-triggered screenshots are an established engineering mechanism.

Therefore 'capture on app change/click/navigation instead of every N seconds' is not sufficient novelty.

## Surviving research object
The surviving object is not a capture mechanism itself. It is the measurable trade-off among:

1. task-resumption/retrieval utility;
2. amount of screen content captured;
3. privacy exposure;
4. storage/compute overhead.

The project should test whether a selective policy can preserve useful task-state reconstruction while materially reducing retained screen data and sensitive exposure compared with dense capture.

## Hypothesis migration

### H1 — Task-state reconstruction from sparse evidence
Status: DEMOTED TO SUPPORTING CAPABILITY.
Task-state reconstruction is established. It is still required for evaluation but cannot carry novelty alone.

### H2 — Utility-constrained selective capture
Status: SURVIVES, NARROWED.

Revised hypothesis:
> A selective capture policy using lightweight task/activity signals may preserve task-resumption utility within a predefined tolerance of dense screenshot capture while reducing retained visual data, storage growth and sensitive-screen exposure.

Novelty is not claimed for event-triggered capture itself. The defensible contribution, if it survives further review, would be the bounded formulation, policy design and comparative evaluation of the utility/privacy/storage trade-off.

### H3 — OBSERVED / DERIVED / INFERRED / UNKNOWN boundaries
Status: DEMOTED TO GOVERNANCE/DESIGN REQUIREMENT.
Evidence-status separation remains desirable but overlaps strongly with provenance and grounded-memory research.

### H4 — Privacy-risk-aware capture policy
Status: SURVIVES ONLY AS PART OF H2.
Privacy-aware lifelogging is mature. H4 alone is not sufficiently distinctive.

## Proposed evaluation frame

### Baselines
- B0 — dense fixed-interval screenshots;
- B1 — sparse fixed-interval screenshots;
- B2 — visual-change-triggered capture;
- B3 — activity/event-triggered capture;
- B4 — proposed utility/privacy-aware selective policy.

### Task scenarios
- S0 — normal document editing with short interruption;
- S1 — programming/debugging across IDE, terminal and browser;
- S2 — research task spanning browser tabs and notes;
- S3 — interruption immediately after a meaningful state change;
- S4 — long low-information period where dense capture adds little utility;
- S5 — sensitive screen occurs during otherwise relevant task;
- S6 — rapid app switching / noisy activity;
- S7 — incomplete capture around a task boundary;
- S8 — multi-session return after a longer delay.

### Candidate metrics
Task-resumption utility:
- resumption time;
- correct identification of prior task goal/state;
- artifact recovery success;
- next-step recovery accuracy;
- user-rated reconstruction usefulness.

Capture cost:
- screenshots retained per hour;
- bytes retained per hour;
- CPU/memory overhead;
- indexing latency.

Privacy exposure:
- sensitive frames retained;
- sensitive-frame retention rate;
- sensitive visual area retained where measurable;
- false-safe / missed-sensitive rate if automatic risk detection is used.

### Key comparative criterion
B4 must not be judged successful merely because it captures less. It must preserve task-recovery utility within a predefined tolerance while reducing capture/storage/privacy cost.

Example success condition:
- task-recovery performance no worse than an agreed margin relative to B0;
- materially lower retained visual volume;
- materially lower sensitive-frame exposure;
- acceptable system overhead.

## Important counterexample
If dense capture achieves 94% task recovery and selective capture achieves 62%, the privacy/storage savings do not rescue the hypothesis. Conversely, if selective capture closely matches dense recovery while retaining far less visual data and fewer sensitive frames, that is evidence for the bounded hypothesis.

## Feasibility
The prototype remains feasible with lightweight desktop event monitoring, compressed screenshots, SQLite, simple image-difference or event heuristics, and an optional small OCR/embedding stage. No large local model is required.

## Remaining novelty threat
The surviving formulation still risks being only a combination of established selective sensing, privacy minimization and task-resumption support. Pass 003 must directly attack the exact joint objective against adaptive sensing, privacy-utility optimization, selective lifelogging, context-aware capture and minimization-aware personal memory systems.

## Gate
MORE RESEARCH.
Do not claim novelty yet. Do not begin full implementation. Next: Pass 003 — final attack on privacy–utility optimized selective capture and task-recovery evaluation.
