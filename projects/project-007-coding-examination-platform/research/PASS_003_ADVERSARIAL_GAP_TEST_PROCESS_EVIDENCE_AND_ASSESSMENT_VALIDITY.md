# P001 (canonical; legacy directory P007) — Pass 003: Adversarial Gap Test — Process Evidence, Assessment Validity, Privacy and Existing Platforms

## Control
- Canonical portfolio ID: **P001**
- Legacy repository directory: `project-007-coding-examination-platform`
- Research stage: GAP REVIEW / ADVERSARIAL PRIOR-ART TEST
- Implementation authorization: **NO**
- Decision after this pass: **MORE RESEARCH — STRONG CANDIDATE, CONTRIBUTION MUST BE NARROWED**

## 1. Question attacked
Can P001 contribute something defensible beyond an existing secure browser-based coding exam with sandboxed execution, automated tests, lockdown/proctoring, event logs, plagiarism/authorship signals and human review?

## 2. Evidence from current products and practice
Current products already cover much of the obvious feature set. CodeGrade advertises browser coding exams with session lockdown, IP restrictions, passwords and proctoring integrations. Viovn Lab0 advertises a secure browser, sandboxed IDE, hidden tests, similarity analysis, incident logs and faculty review. TestDome and other assessment platforms advertise screen/webcam proctoring and Safe Exam Browser lockdown. Therefore the following are **not contribution claims** by themselves:
- browser IDE;
- compile/run during an exam;
- hidden test cases;
- lockdown browser;
- tab/focus monitoring;
- clipboard monitoring;
- screen/webcam proctoring;
- automated grading;
- similarity/plagiarism checks;
- event/audit logs;
- a human review queue.

## 3. Process evidence is also prior art
Programming-process research already records and analyzes more than final submissions. InsProg (2024) captures keystrokes and source snapshots to visualize editing/debugging pathways. Gubanyi & Soh (ICER 2025) collect programming-process data during assignments and secure compile-and-run exams and derive behavior metrics from keystrokes and compilations. Therefore `record code evolution` or `record compile/run events` is not a defensible novelty statement.

This is a major narrowing result.

## 4. Authorship and AI-detection cannot be treated as proof
Recent educational authorship work reports that process features can add signal beyond final code but explicitly frames such models as instructor-mediated decision support rather than independent proof. Broader authorship research also shows coding style evolves over time. Machine-generated-code detection is an active research area, but a detector score is not ground truth.

**Required invariant:** no stylometry, AI-detection, similarity, focus, clipboard, keystroke or proctoring signal may independently produce a misconduct verdict.

## 5. Assessment validity is stronger than surveillance novelty
A more defensible problem is whether the examination captures evidence of programming competence. Prior work comparing pseudocode with compile-and-run prompts found students preferred and performed better in a compile-and-run environment, supporting more authentic assessment. ICER 2025 further reports meaningful differences between assignment and exam programming behavior and recommends process-data tracking.

Therefore P001 should not optimize primarily for `maximum surveillance`. It should optimize for **valid, policy-bounded evidence of competence**, with integrity evidence supporting—not replacing—the assessment judgment.

## 6. Privacy and accessibility are architectural constraints
Lockdown/proctoring technologies can restrict tabs, applications, copying and other device functions, but institutions explicitly warn that accessibility, accommodations, privacy and student experience must be considered. Some assistive technologies can conflict with lockdown approaches. Recording webcams/screens also increases data sensitivity and retention obligations.

P001 therefore needs a graduated integrity model rather than one mandatory surveillance mode.

Candidate modes:
1. **Lab-controlled mode** — institution-controlled machines/network; minimal personal-device surveillance.
2. **Restricted-browser mode** — bounded browser/session controls; no webcam unless separately justified.
3. **Remote-proctored mode** — additional evidence sources only where policy, consent/legal basis, accessibility and necessity justify them.
4. **Open-tool / AI-declared mode** — selected external tools or AI explicitly allowed; competence verified through process evidence and/or independent checkpoint.

## 7. Candidate contribution reduction

### C1 — Policy-Explicit Examination Capability Contract
An exam declares machine-readable capabilities rather than assuming one universal lockdown policy.

Examples:
- compiler: ALLOW
- debugger: ALLOW
- visible tests: ALLOW
- terminal: LIMITED
- documentation: ALLOWLIST
- internet: DENY
- clipboard: INTERNAL_ONLY
- AI: DENY | DECLARE | ALLOW_BOUNDED
- external IDE: DENY
- assistive technology exception: EXPLICIT

Why it matters: observed behavior can only be interpreted against the policy actually in force. A paste is not inherently misconduct if paste is permitted; AI use is not misconduct in an AI-allowed assessment.

Novelty status: **UNKNOWN / PARTIAL**. Configurable exam settings are common; the research candidate is the explicit policy→evidence→interpretation linkage, not configuration alone.

### C2 — Competence Evidence Graph / Trace
Represent assessment evidence as typed, provenance-bearing objects rather than a single score or integrity index.

Candidate nodes:
- question/task;
- code snapshot;
- compile event;
- run/test event;
- error state;
- revision;
- rubric criterion;
- final result;
- tool-use event;
- integrity observation;
- student explanation/oral checkpoint;
- reviewer finding.

Candidate edges:
- REVISES;
- CAUSED_BY;
- ADDRESSES_ERROR;
- SATISFIES_TEST;
- SUPPORTS_CRITERION;
- OBSERVED_UNDER_POLICY;
- REQUIRES_REVIEW;
- CONTRADICTS;
- VERIFIED_BY.

Important: the graph is not automatically a guilt graph. It is an evidence structure for competence and integrity review.

Novelty status: **UNKNOWN**. Process traces are prior art; graph-structured policy-aware competence evidence requires deeper search.

### C3 — Uncertainty-Aware Integrity Review
Every integrity observation has:
- event type;
- timestamp;
- collection mechanism;
- active policy;
- evidence payload/reference;
- confidence/limitations where applicable;
- alternative benign explanations;
- accommodation context where authorized;
- reviewer state;
- final human disposition.

Invariant:
> An observed event is evidence, not a misconduct verdict.

Novelty status: **PRODUCT-STRONG; STANDALONE NOVELTY WEAK/UNKNOWN** because current platforms already advertise evidence logs and human review. The defensible contribution would require calibrated uncertainty/interpretation rules and evaluation of false accusations.

### C4 — Independent Competence Verification
When assessment conditions permit strong assistance (including AI), the platform can require a bounded independent verification step: explain code, modify code, debug a seeded fault, predict behavior, or implement a related micro-task without the previously allowed assistance.

Invariant:
> Assisted artifact quality alone must not automatically establish independent programming competence.

Novelty status: **PROMISING BUT CROWDED BY AI-era assessment research**. Needs direct prior-art comparison.

## 8. What was falsified in this pass
- `Secure coding exam platform` — already exists.
- `Browser IDE + lockdown` — already exists.
- `Process-aware assessment` — established research area.
- `Keystroke/snapshot/compile history` — established.
- `Integrity event log + human review` — already appears in products.
- `AI/code authorship detector` — active prior art and unsuitable as proof.
- `Automated tests prove competence` — too strong; tests can be incomplete and process/assessment validity matters.

## 9. Stronger combined hypothesis
The surviving direction is not one feature. It is a policy/evidence architecture:

> **A programming examination system in which allowed capabilities are explicitly declared, programming-process and integrity observations are preserved as typed evidence under that policy, automated signals cannot independently produce misconduct findings, and assisted performance can be followed by targeted independent verification of competence.**

This is a **research hypothesis**, not a novelty claim.

## 10. Evaluation design emerging
Compare at least:
- B0: paper/pseudocode assessment where practical/ethical;
- B1: ordinary compile-and-run exam + final tests;
- B2: compile-and-run + conventional lockdown/event flags;
- B3: P001 policy-aware evidence model;
- B4: P001 + independent verification for assisted/flagged cases.

Metrics:
- correctness/functional score;
- rubric agreement with expert human assessors;
- ability to identify genuine debugging/programming competence;
- false-positive integrity review rate;
- reviewer agreement;
- review time;
- student usability;
- accessibility failures/accommodation conflicts;
- system overhead/latency;
- evidence completeness;
- ability to distinguish policy-permitted from policy-prohibited behavior;
- independent verification success after assisted work.

## 11. Security requirements already implied
- Untrusted student code executes in a sandbox with CPU, memory, process, filesystem, network and time limits.
- Exam policy is server-authoritative and versioned.
- Client events are not trusted merely because the client reports them.
- Evidence records require tamper-evident integrity and server timestamps where possible.
- Secrets/test cases must not leak into the candidate runtime.
- Authorization separates candidate, invigilator, examiner, reviewer and administrator actions.
- Evidence collection must be minimized to what the selected exam mode requires.
- Retention/deletion rules must exist for sensitive evidence.
- AI/ML outputs are advisory unless a later specification explicitly establishes a bounded deterministic use.

## 12. Next decisive research questions
1. Has a published system already formalized an exam capability policy and interpreted evidence relative to that policy?
2. Has a programming-assessment system represented competence/integrity as an evidence graph or comparable provenance model?
3. What evidence exists on false positives and fairness of automated proctoring/integrity flags?
4. Which process signals correlate with programming competence versus merely correlating with student identity/style?
5. What independent verification formats best distinguish AI-assisted artifact production from retained programming competence?
6. Can the model work in an on-campus lab with little/no webcam surveillance?
7. What threat model is realistic for browser-only versus managed-lab deployments?

## 13. Decision
**MORE RESEARCH — STRONG FYP/PRODUCT CANDIDATE.**

P001 remains high priority, but Pass 003 removes several easy novelty stories. The strongest remaining candidate is the **integration of explicit capability policy, typed process/competence evidence, uncertainty-aware human integrity review, and selective independent verification**. Pass 004 should conduct a mechanism-by-mechanism prior-art matrix against this exact combination and attempt to reduce it further before specification or implementation.
