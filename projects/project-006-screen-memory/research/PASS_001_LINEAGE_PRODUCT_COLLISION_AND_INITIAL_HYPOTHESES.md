# P009 — Personal Screen Memory System — Pass 001

**Current canonical ID:** P009  
**Previous ID:** P006  
**Date:** 2026-09-10  
**Decision:** MORE RESEARCH

## Research question for this pass
Determine whether a personal system that captures what a user sees on a computer and later helps the user recover previously seen information or work context has defensible research space beyond established lifelogging, desktop search, screenshot-history, semantic retrieval, and current commercial/open-source screen-memory products.

## Historical lineage
The core idea is old. Microsoft Research's MyLifeBits, established in 2001, pursued a lifetime digital store inspired by Vannevar Bush's Memex and included broad capture, search, annotations, clustering, and later active-screen/interaction data. Stuff I've Seen and PHLAT explored personal desktop re-finding and associative retrieval. Lifelogging research has since developed multimodal capture, event segmentation, concept-based retrieval, and memory augmentation.

## Direct academic collisions
1. ScreenTrack (2020) periodically captures screenshots and lets users retrieve recently used documents/web pages from a visual history; studies found faster retrieval and support for task resumption.
2. Information-lifelogging work explicitly studies capturing and re-accessing what users see on computer screens for memory support.
3. Screenomics captures dense screenshot streams and applies OCR and other extraction methods to analyze digital life.
4. LifeSeeker and the broader Lifelog Search Challenge literature demonstrate semantic/concept-based retrieval over large personal visual lifelogs.
5. OmniQuery (CHI 2025) goes beyond single-memory retrieval and answers questions that require connecting multiple captured memories and contextual information.
6. IRCHIVER (2025) passively captures browser-visible information, stores full-resolution archives, extracts text, indexes it, and explicitly targets both information re-finding and mental-model restoration for past sensemaking tasks.

## Direct product/open-source collisions
### Microsoft Recall
Windows Recall periodically saves screen snapshots, indexes them locally, provides timeline and semantic search, allows app/site filtering and deletion, uses local processing, and protects content with Windows Hello/TPM/VBS-based mechanisms on supported Copilot+ PCs.

### Rewind / Limitless
Rewind previously captured screen/audio to create searchable personal memory. The Rewind app stopped screen/audio capture in December 2025 and is being sunset, but its existence remains prior art for the product concept.

### Screenpipe
Screenpipe currently describes itself as local private AI memory for screen/audio/work, with continuous capture, searchable memory, agent use, and local-first operation. Current project materials explicitly pursue durable personal memory.

### ActivityWatch
ActivityWatch is a mature privacy-first local activity tracker recording active applications/windows and browser activity, with extensible watchers and local ownership.

### Other current open-source projects
Projects such as Palimpsest and Mnemora combine screenshots, OCR, embeddings/vector search, semantic retrieval, structured context, thread/activity timelines, and local-first privacy.

## Claims killed in Pass 001
The following are not acceptable novelty claims:
- continuously/periodically capture screenshots;
- create a visual timeline of computer activity;
- OCR screenshots;
- search screenshots by text;
- semantic/vector search over screen history;
- retrieve something previously seen;
- local/private screen history;
- app/window/browser metadata capture;
- activity segmentation or timeline grouping;
- summarize screen history with an LLM;
- answer questions over captured personal history;
- combine screenshots with audio/documents/browser context;
- use captured history as context for AI agents;
- allow pause/delete/filter controls.

## Important current-system constraint
Microsoft Recall requires supported Copilot+ PC hardware. That creates a practical accessibility gap for older/low-end PCs, but 'works on weaker hardware' alone is an engineering constraint, not a research contribution.

## Stronger problem formulation
The user problem should not be framed as 'remember everything I saw.' A more defensible target is:

**recover the work state and reasoning context needed to resume an interrupted task, while capturing materially less personal data than indiscriminate continuous screenshot logging.**

This separates two dimensions:
1. memory/retrieval utility;
2. capture/privacy/storage cost.

## Candidate hypotheses
### H1 — Task-State Reconstruction from Sparse Evidence
Can a system reconstruct enough of a user's prior task state to resume work using sparse, event-triggered evidence rather than dense periodic screenshots?

Possible evidence:
- active app/window transitions;
- file/document identifiers;
- browser URL/title where permitted;
- selected screenshots at meaningful transitions;
- OCR snippets;
- user actions such as copy/save/open/compile;
- timestamps and task-session boundaries.

**Status:** SURVIVES PROVISIONALLY. Must attack against activity-based PIM, task resumption, event segmentation, and contextual desktop research.

### H2 — Utility-Constrained Selective Capture
Can capture be treated as an optimization problem: retain the minimum information necessary to satisfy later retrieval/task-resumption queries while reducing storage and sensitive-content exposure relative to fixed-interval capture?

This is not simply 'take fewer screenshots.' It requires a measurable utility/privacy/storage trade-off and a baseline comparison.

**Status:** SURVIVES PROVISIONALLY; strongest Pass 001 direction.

### H3 — Retrieval with Explicit Evidence Boundaries
Can the system distinguish what is directly recoverable from captured evidence from what is inferred, and avoid inventing unseen past actions or reasoning when reconstructing task context?

Potential output vocabulary:
- OBSERVED — directly recorded;
- DERIVED — mechanically extracted from observed data;
- INFERRED — plausible but not directly observed;
- UNKNOWN — evidence insufficient.

**Status:** SURVIVES PROVISIONALLY, but likely threatened by provenance-grounded RAG and evidence-aware personal memory systems.

### H4 — Privacy Risk Budget for Personal Screen Memory
Can the capture policy respond to estimated privacy sensitivity, retention cost, and future utility rather than treating every screen state equally?

**Status:** SURVIVES PROVISIONALLY, but privacy-aware sensing/selective capture is a mature research area and requires direct attack.

## Architecture direction if the candidate survives
User activity -> low-cost event stream -> selective capture trigger -> local extraction/index -> task/session graph -> retrieval/reconstruction -> evidence-labelled response.

Dense continuous capture is a baseline, not the assumed final architecture.

## Feasibility
A bounded prototype is feasible on modest hardware if it avoids large local vision-language models and continuous high-frequency capture. A practical implementation can use Python, SQLite, lightweight window/activity hooks, optional OCR, compressed screenshots, sparse embeddings or API-assisted embeddings, and a small local/web interface. Storage and CPU usage must be measured explicitly.

## Privacy/security constraints
Screen capture can expose passwords, messages, financial information, health information, third-party content, DRM material, and private browsing. The project must treat consent, exclusion rules, local storage, encryption, deletion, retention, sensitive-content filtering, and bystander/third-party privacy as first-class requirements rather than afterthoughts.

## Pass 001 verdict
**MORE RESEARCH.** Generic screen memory is decisively occupied. P009 only remains viable if it can demonstrate a bounded advantage in task-context recovery under a selective-capture/privacy/storage constraint, or another clearly falsifiable mechanism not already covered by lifelogging and current screen-memory systems.

## Next pass
P009 Pass 002 must directly attack H1-H4 against:
- task-resumption and interruption-recovery research;
- activity-based personal information management;
- event segmentation and sparse lifelogging;
- adaptive/selective screen capture;
- privacy-aware sensing and minimization;
- provenance/evidence-grounded personal-memory QA;
- IRCHIVER, OmniQuery, ScreenTrack, Microsoft Recall, Screenpipe, and related current systems.

If selective capture + task-state reconstruction is already established, narrow or kill rather than manufacturing novelty.