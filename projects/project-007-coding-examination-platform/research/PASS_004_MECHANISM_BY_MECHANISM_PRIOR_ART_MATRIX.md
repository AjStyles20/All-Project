# P001 (canonical; legacy directory P007) — Pass 004: Mechanism-by-Mechanism Prior-Art Matrix

## Control
- Canonical portfolio ID: **P001 — Intelligent Coding Examination Platform**
- Legacy repository directory: `project-007-coding-examination-platform`
- Research stage: ADVERSARIAL GAP REVIEW / CANDIDATE REDUCTION
- Implementation authorization: **NO**
- Decision after this pass: **MORE RESEARCH — CONDITIONAL GO CANDIDATE**

## 1. Purpose
Pass 003 reduced the project to four candidate mechanisms. Pass 004 attacks those mechanisms individually and as a combined architecture. Absence from reviewed documentation is recorded as UNKNOWN, never as proof that a feature does not exist.

Candidate mechanisms:
- C1 Policy-Explicit Examination Capability Contract
- C2 Competence Evidence Graph / Trace
- C3 Uncertainty-Aware Integrity Review
- C4 Independent Competence Verification

## 2. New evidence pressure
### 2.1 Policy-relative assessment is established in principle
Current assessment practice already distinguishes permitted and prohibited resources. AI policies may vary by assessment; current course and qualification guidance explicitly defines when AI is prohibited, permitted, must be declared, or must be independently verified. Therefore `the exam says what tools are allowed` is not novel.

Surviving C1 question: can the policy be machine-readable, versioned, server-authoritative, and directly bind runtime capability enforcement and later interpretation of evidence?

### 2.2 Process evidence is established
InsProg (2024) captures keystrokes and code snapshots. Gubanyi & Soh (ICER 2025) collect keystroke/compilation process data in assignments and secure compile-and-run exams and relate behavior to performance. Therefore process capture and visualization are prior art.

Surviving C2 question: does a typed evidence model explicitly connect task, code revisions, execution results, rubric criteria, active capability policy, integrity observations, independent checkpoints, reviewer findings and provenance without collapsing them into a score?

### 2.3 Human review of automated flags is established
Current proctoring/certification practice already uses automated alerts as supporting evidence with human review. Recent Nigerian CIPM online-proctoring guidance is especially direct: automated proctoring flags are alerts; evidence includes video/audio/screenshots/system logs/incident reports/candidate response; a designated panel reviews cases and the candidate may respond. Microsoft/Pearson guidance similarly says AI monitoring generates alerts while authorized personnel make final security decisions.

Therefore `AI flag + human review` is not novel.

Surviving C3 question: can observations carry explicit uncertainty, collection limitations, alternative benign explanations, accommodation context and policy-relative meaning, with no automated signal independently escalating into a misconduct verdict?

### 2.4 Independent verification after AI assistance is established
Current AI-era assessment research and policy already use or propose independent verification. Chung (2026) permits GenAI for programming assignments but verifies individual mastery using immediate AI-free assignment-driven quizzes. AP Computer Science Principles permits AI as a supplementary development/debugging resource while requiring students to understand and later explain their code. ICER 2026 work in resource-constrained environments explicitly studies scaffolded AI-verification patterns. Therefore `allow AI then independently test understanding` is not novel.

Surviving C4 question: can independent verification be selectively generated from the candidate's own evidence trace and targeted at uncertainty in competence rather than imposed as a generic second exam?

## 3. Mechanism matrix
Legend: YES = directly evidenced in reviewed source; PARTIAL = nearby mechanism but not full candidate; UNKNOWN = not established from reviewed evidence; NO is used only where a source explicitly rules a mechanism out.

| Prior art / practice family | C1 explicit policy | C1 policy→runtime/evidence binding | C2 process trace | C2 typed competence provenance | C3 human review | C3 explicit uncertainty/benign alternatives | C4 independent verification | C4 trace-targeted verification |
|---|---|---|---|---|---|---|---|---|
| Secure coding-exam platforms | YES/PARTIAL | PARTIAL | PARTIAL | UNKNOWN | YES/PARTIAL | UNKNOWN | UNKNOWN | UNKNOWN |
| InsProg (2024) | UNKNOWN | UNKNOWN | YES | PARTIAL | teacher interpretation | UNKNOWN | UNKNOWN | UNKNOWN |
| Gubanyi & Soh ICER (2025) | secure exam context | UNKNOWN | YES | PARTIAL | research interpretation | UNKNOWN | UNKNOWN | UNKNOWN |
| Certification/proctoring practice | YES | PARTIAL | event/session evidence | PARTIAL | YES | PARTIAL | retest can occur | UNKNOWN |
| CIPM Nigeria online-proctoring guidance (2026) | YES | PARTIAL | evidence bundle | PARTIAL | YES | PARTIAL/YES | fair-hearing response, not competence test | UNKNOWN |
| Microsoft/Pearson online exam practice | YES | PARTIAL | monitoring evidence | PARTIAL | YES | PARTIAL | UNKNOWN | UNKNOWN |
| Chung AI-open programming assessment (2026) | YES | assessment-level policy | assignment artifact, not full process graph | UNKNOWN | educator assessment | UNKNOWN | YES | PARTIAL — quiz tied to assignment |
| AP CSP AI policy | YES | policy-governed | artifact/checkpoint evidence | PARTIAL | YES | UNKNOWN | YES — explanation/exam | PARTIAL |
| General high-stakes AI-marking guidance | YES | PARTIAL | assessment evidence | PARTIAL | YES | fairness/transparency required | UNKNOWN | UNKNOWN |

The matrix does **not** establish that no existing system combines all columns. It establishes that each individual ingredient is crowded while several integration semantics remain unresolved.

## 4. Candidate verdicts
### C1 — Policy-Explicit Examination Capability Contract
**Standalone novelty: WEAK.**
Policies and configurable permissions are established.

**Surviving engineering/research value: STRONG/PARTIAL.**
The candidate becomes a versioned executable contract that:
1. declares capabilities;
2. configures runtime enforcement;
3. labels every evidence event with the active policy version;
4. prevents later reviewers from interpreting an event outside the policy under which it occurred;
5. represents approved accessibility/accommodation exceptions without converting them into suspicious behavior.

Invariant:
> No event is classified as a policy violation without resolving it against the exact policy version and authorized exception state active when the event occurred.

### C2 — Competence Evidence Graph / Trace
**Standalone process-tracking novelty: DEAD.**
Process traces, snapshots, compilations and debugging analysis already exist.

**Surviving candidate: PARTIAL / UNKNOWN.**
The stronger mechanism is a provenance-bearing competence case rather than a surveillance timeline. It separates:
- task requirement;
- observable programming actions;
- executable evidence;
- rubric evidence;
- integrity observations;
- assistance/tool context;
- independent verification;
- human findings.

The key claim is not that a graph is novel. The research question is whether this structured evidence improves validity, review consistency and explainability compared with final-output grading or flat proctoring flags.

### C3 — Uncertainty-Aware Integrity Review
**Standalone human-review novelty: DEAD.**
Human review of automated alerts already exists.

**Surviving candidate: PRODUCT-STRONG / RESEARCH PARTIAL.**
The useful mechanism is calibrated evidence semantics:
- OBSERVATION != VIOLATION;
- VIOLATION != MISCONDUCT;
- anomaly confidence != guilt probability;
- alternative benign explanations are first-class;
- accommodation/policy context is first-class;
- candidate response can become part of the case record;
- consequential disposition remains human-authorized.

This is consistent with current assessment practice emphasizing evidence, fairness, transparency and human accountability.

### C4 — Independent Competence Verification
**Standalone novelty: DEAD/WEAK.**
AI-assisted work followed by AI-free or explanation-based verification already exists.

**Surviving candidate: STRONG PRODUCT/EXPERIMENTAL MECHANISM.**
The narrowed idea is **evidence-targeted verification**. The system selects a small verification task based on uncertainty in the candidate's own trace. Examples:
- code works but candidate never demonstrated understanding of a key branch → predict/modify that branch;
- heavy permitted AI assistance produced a solution → explain or repair a related fragment without AI;
- suspicious paste occurred but was policy-permitted → test the relevant concept rather than accuse;
- tests pass but debugging trace shows unresolved conceptual confusion → seeded bug or transfer micro-task.

Invariant:
> Verification is used to acquire missing competence evidence, not to manufacture a misconduct finding.

Novelty remains UNKNOWN/PARTIAL and requires direct search against adaptive oral exams, viva generation, mastery verification and evidence-centered assessment.

## 5. Strongest surviving architecture
The project should no longer present C1–C4 as four novel inventions. A defensible architecture is:

### Policy-Bound Programming Competence Evidence System
1. **Policy layer** — machine-readable, versioned capability contract.
2. **Execution layer** — sandboxed code execution under bounded resources.
3. **Evidence layer** — typed, provenance-bearing competence/integrity evidence.
4. **Interpretation layer** — policy-relative rules; automated observations cannot become misconduct verdicts.
5. **Verification layer** — acquire missing evidence through targeted independent micro-assessment where justified.
6. **Human decision layer** — authorized examiners/reviewers decide marks and integrity findings according to institutional policy.

Core chain:
`ASSESSMENT POLICY → RUNTIME CONDITIONS → OBSERVATIONS → COMPETENCE EVIDENCE → UNCERTAINTY/GAPS → TARGETED VERIFICATION → HUMAN FINDING`

This is stronger than `LOCKDOWN → FLAGS → CHEATING SCORE`.

## 6. Nigeria/resource-constrained relevance
P001 should retain a lab-first deployment mode. This is not merely a cost concession. In institutions where programming exams are currently paper-based or computer resources are constrained, a managed-lab architecture can provide authentic compile-and-run assessment without imposing webcam-heavy remote proctoring.

Current 2026 Nigerian assessment policy also emphasizes exam integrity and evidence-based handling of malpractice. Recent ICER 2026 work specifically studies AI-verification assessment patterns in resource-constrained Nigerian computing departments, making it important that P001 not claim `resource-constrained AI verification` itself as novel.

Potential contextual contribution instead:
- low-bandwidth/on-premise operation;
- local sandbox workers;
- server-authoritative policy/evidence records;
- graceful network interruption handling;
- minimal surveillance in managed labs;
- exportable evidence case for human review.

These are implementation/evaluation dimensions, not novelty claims yet.

## 7. What Pass 004 falsifies
Do not claim novelty for:
- configurable exam permissions;
- AI allowed/prohibited policies;
- compile-and-run exams;
- process traces;
- keystroke/code-snapshot collection;
- automated proctoring alerts;
- human review of flags;
- AI-assisted assignment followed by AI-free quiz/viva;
- evidence logs;
- use of a graph data structure by itself.

## 8. Research hypotheses surviving
### H1 — Policy-bound evidence interpretation
A versioned executable capability policy can reduce false or inconsistent integrity interpretations by ensuring observations are evaluated against the actual allowed-tool/accommodation state.

### H2 — Structured competence evidence
A typed competence evidence model can improve reviewer agreement/explainability and assessment validity compared with final-output-only grading or flat integrity event logs.

### H3 — Evidence-targeted independent verification
A small verification task selected from missing/uncertain competence evidence can recover confidence in individual programming competence more efficiently than universal second-stage verification.

H1–H3 are hypotheses, not novelty claims.

## 9. Required baselines
- B0 paper/pseudocode exam where ethically/practically available;
- B1 ordinary compile-and-run + final tests;
- B2 compile-and-run + conventional policy/lockdown + flat flags;
- B3 P001 policy-bound structured evidence without targeted verification;
- B4 P001 + evidence-targeted verification.

## 10. Evaluation targets
Measure:
- programming-task correctness;
- agreement with expert competence judgments;
- reviewer agreement;
- false-positive policy-violation interpretation;
- false misconduct escalation rate;
- time per review;
- number/duration of verification tasks;
- verification information gain / resolved uncertainty;
- student usability;
- accommodation/accessibility conflicts;
- bandwidth/compute overhead;
- evidence completeness and tamper detection;
- performance during network interruption/recovery;
- differences between assisted and independently verified competence.

No numeric threshold is approved yet; Pass 005 should derive defensible acceptance criteria from pilot design and evidence.

## 11. Security/privacy implications
- Student code is hostile input and must be sandboxed with CPU/memory/process/filesystem/network/time limits.
- Policy is server-authoritative and cryptographically/tamper-evidently versioned where justified.
- Client telemetry is untrusted evidence; server corroboration is preferred.
- Hidden tests/secrets never enter candidate-accessible contexts.
- Roles separate candidate, invigilator, examiner, integrity reviewer and administrator.
- Evidence collection follows data minimization; webcam/audio are not default requirements for managed-lab mode.
- Retention/deletion/access logging must be specified before collecting sensitive evidence.
- AI-generated grading, authorship, anomaly or verification suggestions are advisory unless independently validated for a tightly bounded deterministic use.
- Appeals/candidate-response workflow should be representable rather than assuming automated findings are final.

## 12. Decision
**MORE RESEARCH — CONDITIONAL GO CANDIDATE.**

P001 remains a strong FYP/product candidate, but Pass 004 substantially narrows the contribution. The best current package is not a new IDE, proctor or auto-grader. It is a **policy-bound programming competence evidence architecture**, with three experimental mechanisms:
1. policy-bound evidence interpretation;
2. structured competence evidence;
3. evidence-targeted independent verification.

The next pass should be decisive rather than broad: directly attack H1–H3 against evidence-centered assessment, adaptive/oral/viva verification, assessment validity, policy-as-code/access-control systems, provenance/audit systems and existing coding-assessment products. It should then select at most one primary research contribution plus supporting mechanisms, define kill criteria, and decide whether to proceed to formal specification or move to the next portfolio project.