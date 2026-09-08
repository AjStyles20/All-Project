# Architecture Proposal — Project 001

## Status
PROPOSED — not yet approved for implementation.

## Architecture Goal
Build a professional, explainable, low-complexity MVP for source-grounded technical/research review practice. The system should work on modest hardware, avoid unnecessary infrastructure, and preserve a clean upgrade path for speech, richer retrieval, and additional providers.

## Core Product Flow
1. User creates a project/workspace.
2. User uploads source artifacts such as PDF, DOCX, PPTX, Markdown, or text.
3. System extracts and chunks readable content while preserving file/page/section provenance where possible.
4. Retrieval layer indexes the chunks.
5. User configures a review session and selects reviewer roles/personas.
6. Question engine retrieves relevant evidence and generates a challenge question.
7. The question stores its evidence references and generation metadata.
8. User answers by text initially; speech can be added through a pluggable input layer.
9. Feedback engine evaluates the answer against retrieved evidence and explicit criteria.
10. Session history, questions, answers, evidence links, and feedback are stored for later review.

## Recommended MVP Stack

### Backend
**FastAPI + Python**

Reasons:
- user already works with Python/FastAPI;
- strong fit for document processing and AI integrations;
- explicit request/response models support explainability;
- lightweight enough for the user's current hardware;
- straightforward automated testing.

### Frontend
**Server-rendered HTML templates + lightweight JavaScript** for the first MVP.

Do not begin with a heavy SPA unless a concrete UX requirement demands it.

Reasons:
- lower memory/build-tool overhead;
- easier deployment and debugging;
- faster path to an end-to-end verified product;
- can later migrate or add richer components without changing the domain model.

### Database
**SQLite** for the MVP.

Reasons:
- zero service setup;
- sufficient for a single-user/local prototype and modest hosted deployment;
- easy to inspect and defend;
- can be migrated later if concurrency or scale requires it.

### Document Ingestion
Use format-specific parsers behind a common ingestion interface.

Initial formats:
- PDF
- DOCX
- PPTX
- TXT / Markdown

Each extracted chunk should preserve:
- document ID
- source filename
- page/slide/section when available
- chunk ID
- extraction status
- hash/version metadata where practical

### Retrieval
**Hybrid, inspectable retrieval** rather than a large opaque stack.

Recommended first implementation:
- lexical retrieval using SQLite FTS5;
- optional semantic embeddings stored with chunks;
- semantic similarity calculated in application code for project-sized corpora;
- weighted merge/rerank of lexical and semantic candidates.

Why not start with a dedicated vector database:
- additional dependency and operational complexity are not justified for a small MVP corpus;
- a simpler retrieval layer is easier to test, explain, and inspect;
- vector-store migration can remain an A2 scale decision later.

### LLM / Embedding Providers
Use provider interfaces/adapters rather than hard-coding one vendor into the domain layer.

Required interfaces:
- `QuestionGenerator`
- `AnswerEvaluator`
- `EmbeddingProvider`
- later `SpeechToTextProvider`
- later `TextToSpeechProvider`

Environment configuration should select the active provider.

No provider should be described as configured unless credentials and a live request have been verified.

## Reviewer/Persona Model
Reviewer roles are prompt/evaluation policies, not fictional humans.

Initial role candidates:
- Technical Reviewer
- Methodology Reviewer
- Evidence/Skeptical Reviewer
- Security & Privacy Reviewer
- Product/Usability Reviewer

Each role defines:
- purpose
- preferred question categories
- evidence types to prioritize
- challenge intensity
- prohibited unsupported judgments
- evaluation rubric

## Question Provenance Model
Every generated question should store:
- question ID
- session ID
- reviewer role
- generated question text
- retrieved chunk IDs
- source document references
- generation timestamp
- provider/model metadata when available
- grounding status

This enables verification of whether the question was actually supported by the source context.

## Feedback Model
Feedback should be separated into categories rather than collapsed into one arbitrary score:
- source/content correctness
- completeness
- evidence use
- reasoning/clarity
- uncertainty/unsupported statements
- delivery metrics, only when speech analysis exists

The system should avoid claiming objective overall presentation quality.

## Session Model
Core entities:
- ProjectWorkspace
- SourceDocument
- DocumentChunk
- ReviewerProfile
- PracticeSession
- Question
- Answer
- FeedbackItem
- RetrievalEvidence

## Security / Privacy Baseline
- uploaded files are private project data;
- do not expose raw file paths to clients;
- validate extension and content type;
- enforce file-size limits;
- store secrets only in environment configuration;
- sanitize rendered content;
- log provider/data-flow decisions;
- document whether uploaded text is sent to an external AI provider.

## Accessibility Baseline
- keyboard-operable interface;
- semantic form labels;
- non-color-only status indicators;
- text alternatives for audio/speech workflows;
- no mandatory VR/headset dependency;
- readable session transcript and evidence view.

## MVP Boundary
### Required
- workspace creation
- document upload/extraction
- provenance-aware chunking
- retrieval
- reviewer-role selection
- grounded question generation
- text answers
- evidence-aware feedback
- session history
- evidence/source inspection
- automated tests for ingestion, retrieval, question provenance, and core API/session flow

### Post-MVP / optional
- microphone/STT
- TTS/voice personas
- video/body-language analysis
- animated avatars
- VR scenes
- multi-user sessions
- cloud vector database
- complex analytics dashboard

## Architecture Risks
1. Generated questions may appear grounded even when retrieved evidence is weak.
2. Document extraction quality varies by format.
3. External LLM providers may introduce cost, latency, privacy, and availability risks.
4. Automated answer evaluation is partly judgment-based and needs careful wording/testing.
5. Persona prompts may differ stylistically without producing meaningful category differentiation.

## Proposed Verification Strategy
- fixture documents with known facts and deliberate contradictions;
- retrieval relevance tests;
- provenance correctness tests;
- unsupported-question detection set;
- reviewer-role category tests;
- API integration tests;
- manual evidence inspection on sample sessions;
- record provider/model/version for generated evaluation evidence.

## Architecture Decision Requested
Approve or modify the recommended MVP foundation:

**FastAPI + SQLite + server-rendered frontend + inspectable hybrid retrieval + provider-adapter AI layer.**

No implementation should begin until this core architecture is approved because it establishes the project's framework and persistence foundation.