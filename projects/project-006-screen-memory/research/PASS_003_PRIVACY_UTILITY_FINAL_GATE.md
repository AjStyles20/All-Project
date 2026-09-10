# P009 — Pass 003: Privacy–Utility / Task-Resumption Final Gate

## Canonical identity
- Current ID: P009
- Previous ID: P006
- Project: Personal Screen Memory System
- Date: 10 September 2026

## Decision
**CONDITIONAL GO TO FORMAL SPECIFICATION — bounded evaluation contribution only.**

P009 does not survive as a novelty claim for screen capture, screenshot history, semantic retrieval, event-driven capture, privacy filters, task resumption, local-first storage, or activity reconstruction. It survives only as a narrowly scoped design-and-evaluation study of whether a selective desktop-memory capture policy can preserve task-resumption utility while reducing retained visual data, privacy exposure, storage growth, and processing overhead.

## Prior-art attack result
### Claims rejected
1. Generic personal screen memory / “remember everything I saw”.
2. Screenshot timeline and semantic search.
3. Event-driven capture — current Screenpipe documentation already describes OS-event-driven capture on app switches, clicks, typing pauses, scroll, clipboard, and periodic idle fallback.
4. Local-first/private screen memory.
5. Task resumption from captured screen history.
6. Privacy filtering/redaction/exclusion.
7. Privacy–utility trade-off as a general concept.
8. Data minimization for visual lifelogging as a general concept.
9. Activity recognition from reduced or transformed visual data.

### Closest technical threats
- Screenpipe implements event-driven screen capture and reports materially lower storage than continuous video while preserving searchable local screen history.
- Open Chronicle directly advertises “continue where I left off” task resumption from screen-memory history.
- CAPED (2026) evaluates task-driven selective visual exposure to reduce privacy leakage while preserving GUI-agent task utility.
- EdgeVLM privacy-filter work (2026) explicitly studies preserving activity-recognition utility while reducing visual privacy risk through local transformation.
- Visual-lifelogging research has long treated privacy as a first-class design problem.
- A 2026 position paper argues that life-logging privacy–utility trade-offs require pipeline-aware designs and standardized benchmarks, indicating the broad problem remains open but is not itself novel.
- ScreenTrack already demonstrated that screenshot histories can support retrieval and task-context recovery.

## Surviving gap
Targeted search did not identify a direct study evaluating this exact desktop-memory conjunction:

**selective capture policy + later human task-resumption utility + privacy exposure + storage/resource cost**, with dense capture and ordinary event-triggered capture as baselines.

This absence is not proof of first-of-kind. Therefore P009 must be defended as a bounded empirical design/evaluation contribution rather than an algorithmic invention.

## Frozen candidate hypothesis
### H5 — Task-Resumption-Constrained Selective Capture
A selective desktop-memory capture policy can reduce retained visual data, sensitive-screen exposure, storage growth, and processing overhead relative to dense fixed-interval capture while keeping human task-resumption performance within a predeclared acceptable degradation margin.

### Null hypothesis H0
Once task-resumption degradation, privacy misses, and ordinary event-triggered baselines are included, the proposed selective policy offers no material net benefit.

## Candidate research question
**Can a selective desktop-memory capture policy preserve task-resumption effectiveness within a predeclared tolerance of dense screenshot capture while materially reducing retained visual data, sensitive-screen exposure, storage growth, and processing overhead?**

## Candidate baselines
- B0 — dense fixed-interval capture.
- B1 — sparse fixed-interval capture.
- B2 — visual-change-triggered capture.
- B3 — ordinary activity/event-triggered capture.
- B4 — proposed utility/privacy-aware selective capture policy.

B4 must not receive privileged task labels or future knowledge unavailable to other policies.

## Required evaluation dimensions
### Human/task utility
- resumption lag / time to meaningful work restart;
- prior-goal recovery accuracy;
- relevant artifact/file/tab recovery;
- next-step recovery;
- post-resumption errors;
- subjective usefulness only as secondary evidence.

### Privacy
- sensitive frames retained;
- sensitive-frame retention rate;
- sensitive-content miss rate where a seeded benchmark permits ground truth;
- bystander/non-user information exposure where ethically appropriate.

### Resource cost
- screenshots retained per hour;
- MB per hour/day;
- CPU and RAM overhead;
- indexing delay;
- optional energy impact if measurable.

### Retrieval quality
- top-k recovery of required artifacts;
- time-to-find relevant context;
- context completeness.

## Critical experiment
Use controlled interruption/resumption tasks, preferably programming or document-work scenarios involving multiple applications such as an editor, browser, terminal, notes, and file manager. Participants work under one capture policy, are interrupted, and later resume using the memory system. The study compares B0–B4 under the same task structures.

A policy is not successful merely because it stores fewer screenshots. It must satisfy a predeclared task-utility constraint and improve at least one privacy/resource dimension materially without unacceptable regressions elsewhere.

## Falsification criteria
H5 fails if any of the following occur:
1. B4 materially worsens resumption performance beyond the predeclared tolerance.
2. B4 offers no meaningful privacy/storage/resource advantage over B3.
3. Privacy reduction is achieved mainly by missing task-critical evidence.
4. Sensitive-content filtering creates an unacceptable miss rate.
5. Results disappear across reasonable interruption lengths, task types, or capture-frequency settings.
6. Thresholds are tuned on the final evaluation set.
7. B4 relies on task labels or future information unavailable at capture time.

A negative result remains reportable and must not be reframed as success.

## Non-claims
P009 must not claim to invent:
- screen memory;
- lifelogging;
- screenshot search;
- semantic desktop history;
- event-driven capture;
- private/local-first recording;
- privacy filtering;
- task resumption support;
- adaptive sensing;
- privacy–utility trade-offs.

## Allowed contribution claim if supported
“In the defined desktop interruption benchmark, the evaluated selective capture policy reduced retained visual data and privacy/resource cost relative to specified baselines while preserving task-resumption performance within the predeclared tolerance.”

Do not generalize beyond the evaluated task classes, hardware, privacy labels, or participant sample.

## Feasibility
The prototype can remain lightweight: Windows activity/window hooks, compressed screenshots, SQLite, OCR/accessibility text when available, simple change/event features, and a local retrieval interface. No heavy GPU dependency is required for the core experiment.

## Final Pass 003 gate
**CONDITIONAL GO TO FORMAL SPECIFICATION.**

Reason: the obvious implementation space is crowded, but the exact bounded comparative evaluation of task-resumption utility against retained-data/privacy/resource cost remains defensible after targeted attack. Confidence is moderate, not high. Pass 004 should freeze the experimental protocol, capture-policy definitions, privacy-risk labeling scheme, metrics, thresholds/tolerances, participant/task design, reproducibility controls, and ethics/privacy boundaries before implementation.
