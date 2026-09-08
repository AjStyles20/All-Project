# Documentation Guidelines

## Purpose
These guidelines define the default documentation standard for all projects managed under AJ Project OS.

The default is **professional, product-neutral, and institution-neutral**. A project should read like a credible technical/research project that could be used for a portfolio, client, research prototype, startup, internal engineering effort, or later academic submission.

Academic or institution-specific formatting is an optional export/adaptation layer applied only after AJ explicitly chooses a project for that purpose.

## 1. Default Documentation Identity
Do not include any of the following unless AJ explicitly approves an academic adaptation:
- school or university name
- faculty or department name
- supervisor name
- head of department or dean name
- registration/student number
- institutional declaration/certification/approval pages
- wording such as “submitted in partial fulfilment…”
- institution-specific cover colours, hard-copy counts, signatures, or submission rituals

Do not infer or auto-fill any of these from prior chats, uploaded guidelines, old projects, or connected documents.

## 2. Professional Core Documentation
Every project should maintain only the documentation that materially helps another competent person understand, evaluate, reproduce, maintain, or defend the work.

Recommended core set:
- Executive / Project Summary
- Problem and Context
- Goals and Approved Scope
- Requirements
- Research / Prior Art / Related Systems, where relevant
- Architecture and Design
- Data and Model Design, where relevant
- Implementation Notes
- Testing and Verification
- Risks, Security, Privacy, Accessibility, and Ethics, where relevant
- Limitations
- User / Operator Guide, where relevant
- Decision Log
- Work Log and Handoffs
- References and Source Provenance
- Future Work / Roadmap

Do not force a five-chapter dissertation structure onto projects that do not need one.

## 3. Writing Standard
Documentation must be:
- precise, professional, and technically literate
- consistent in terminology
- grounded in verified project state
- explicit about assumptions, simulation, limitations, and unverified claims
- free of fabricated results, citations, users, data, integrations, or experiments
- written for a reader who was not present in the project chats

Prefer concrete statements over promotional language. Avoid unsupported adjectives such as “accurate”, “intelligent”, “robust”, “secure”, “real-time”, “production-ready”, or “state-of-the-art” unless evidence supports them.

## 4. Evidence and Claim Discipline
Every material claim should map to one or more of:
- source / citation
- requirement
- architecture decision
- code or implementation artifact
- test evidence
- experiment result with provenance
- user-verified behavior

Unsupported claims must remain `UNDER REVIEW`, `PARTIAL`, or `UNSUPPORTED` rather than being written as conclusions.

## 5. Implementation / Documentation Synchronization
Documentation must follow the current implementation, not the original plan.

When architecture, data flow, framework, database, model, feature behavior, or testing status changes, the affected documentation must be updated or explicitly marked stale.

Planned, proposed, simulated, parked, or partially implemented functionality must never be presented as complete.

## 6. Research and References
Research notes must preserve source provenance. Do not fabricate or normalize incomplete references into fictional completeness.

For general Project OS work, use a consistent citation format appropriate to the document type. For research-heavy work, preserve author, title, year, venue/publisher, DOI/URL, access information when relevant, and evidence notes.

APA 7 may be applied later when an academic export requires it; it is not mandatory for every Project OS document.

## 7. Tables, Figures, and Diagrams
Tables and figures should be used when they communicate structure or evidence better than prose.

- Give every important table/figure a clear title or caption.
- Discuss important tables/figures in the surrounding text.
- Cite the source if a visual is not original.
- Prefer readable, simple diagrams over decorative complexity.
- Keep architecture, data-flow, ERD, sequence, use-case, activity, and other diagrams synchronized with implementation.

## 8. Testing Documentation
Where software is implemented, maintain evidence for:
- unit testing
- integration testing
- system/end-to-end testing where relevant
- regression testing after important fixes
- failure reports and corrections
- test traceability to requirements

An implementation section should include meaningful problems encountered, diagnosed causes, corrections, and verification rather than pretending development was error-free.

## 9. Abstract / Executive Summary
For professional documentation, use an Executive Summary unless a formal abstract is appropriate.

If an academic-style abstract is later requested, keep it concise and evidence-based, summarizing what was done, how it was done, major findings/results, and conclusions. Do not write results before they exist.

## 10. Academic Adaptation Layer
When AJ explicitly designates a project for academic submission, create a separate adaptation plan rather than contaminating the professional source documents.

Possible adaptations may include:
- institution-specific title and preliminary pages
- dissertation chapter structure
- required fonts, margins, spacing, pagination, and heading rules
- minimum literature-review length
- formal lists of tables, figures, and abbreviations
- APA 7 reference formatting
- appendices and code excerpts
- submission-specific packaging

The professional project documentation remains the canonical technical source. Academic documents are derived from it.

## 11. Privacy / Identity Rule
Institutional identity and personal academic details are opt-in fields. Never introduce a school, supervisor, lecturer, staff member, student identifier, or institutional branding unless AJ explicitly requests it for the selected project.

## 12. Quality Gate
Before a document is considered ready, verify:
- terminology matches `PROJECT_STATE.md`
- implementation descriptions match code and architecture
- test claims match `TEST_EVIDENCE.md`
- research claims match `RESEARCH_CLAIMS.md`
- limitations are not hidden
- no institution-specific identity has been inserted by default
- no unsupported claim has been upgraded through wording
- references are real and traceable
