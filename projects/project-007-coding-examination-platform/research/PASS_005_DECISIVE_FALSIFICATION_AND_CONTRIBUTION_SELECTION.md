# P001 (canonical; legacy directory P007) — Pass 005: Decisive Falsification and Contribution Selection

## Control
- Canonical portfolio ID: **P001**
- Legacy repository directory: `project-007-coding-examination-platform`
- Research stage: DECISIVE FALSIFICATION / CONTRIBUTION REDUCTION
- Implementation authorization: **NO**
- Decision after this pass: **GO TO FORMAL SPECIFICATION — PROVISIONAL RESEARCH GATE PASS**

## 1. Purpose
Pass 005 attempts to destroy the three surviving hypotheses from Pass 004 against evidence-centered assessment, AI-era ICT assessment frameworks, process evidence, adaptive viva/verification, policy declarations, and resource-constrained computing education.

The project is not allowed to claim novelty from secure code execution, browser IDEs, lockdown, automated tests, process logging, permitted-help statements, AI disclosure, viva verification, human review, or evidence-centered assessment individually.

## 2. Strong prior-art attacks
### Evidence-centered assessment
Evidence-Centered Design (ECD) already formalizes assessment as claims about competence supported by observable evidence elicited through tasks. It has been applied to computer-science and interactive/digital assessment. Therefore `assessment as an evidentiary argument` is established and cannot be P001's novelty.

### AI-era ICT assessment design
2026 ICT assessment research already connects competencies, assessment strategies, and methods under GenAI conditions. Therefore `redesign coding assessment for AI` is not sufficient.

### Nigerian/resource-constrained AI verification
The 2026 Scaffolded AI-Verification Framework (SAVF) is a direct threat: it arises from Nigerian computing departments and includes permitted-help statements with disclosure, process-evidence bundles emphasizing explanation/testing, and course-anchored prompts under low-data constraints. Therefore permitted-help policy + process evidence + low-resource deployment cannot be claimed as new.

### Adaptive viva / independent verification
Integrevise and other current work pair submitted artifacts with short/adaptive viva verification. Programming-specific work also proposes code explanations/vivas. Therefore `use a viva to verify AI-assisted work` is established/crowded.

### Programming-process evidence
Prior work records keystrokes, source snapshots, compilation and debugging behavior. Competence-oriented programming assessment maps tests/tasks to competence models. Therefore a process trace or competence mapping alone is established.

## 3. Hypothesis-by-hypothesis decision

### H1 — Policy-Bound Evidence Interpretation
**Original idea:** observations are interpreted relative to the exact examination capability policy and authorized exceptions in force at the time.

**Prior art found:**
- configurable/permitted-help assessment rules;
- AI-use declarations and disclosure;
- lockdown/proctoring policy settings;
- human review of automated alerts;
- SAVF permitted-help statements;
- institutional assessment governance.

**What remains potentially distinctive:** a machine-enforced runtime linkage where each relevant evidence object is evaluated against a versioned policy state and applicable accommodation/exception, so the same event can be compliant, ambiguous, or policy-violating depending on context.

Example:
`PASTE_EVENT + policy clipboard=INTERNAL_ONLY + source=exam-editor -> PERMITTED`
versus
`PASTE_EVENT + policy clipboard=DENY + external-source evidence -> POLICY_EXCEPTION/REVIEW`

The runtime must preserve the policy version used for interpretation and must not retroactively reinterpret old evidence under a later policy without an explicit migration/review event.

**Verdict:** **PARTIAL / SUPPORTING MECHANISM.** Useful, but too close to policy/configuration/governance work to carry the research contribution alone.

### H2 — Structured Competence Evidence
**Original idea:** typed process, execution, rubric, integrity, and verification evidence form an explainable competence case rather than a flat score.

**Prior art found:**
- ECD claim/evidence/task models;
- programming process traces;
- competence models tied to programming tests;
- learning analytics from logs;
- evidence bundles in SAVF;
- automated/human scoring pipelines.

**What remains potentially distinctive:** a programming-exam runtime that maintains explicit provenance from observed coding events and test/rubric outcomes to *bounded competence claims*, while preserving contradictory, missing, policy-contaminated, or assistance-dependent evidence rather than collapsing everything into one grade/integrity score.

However, graph representation itself is not a novelty claim; ECD and provenance systems make that too broad.

**Verdict:** **PARTIAL / FOUNDATIONAL ARCHITECTURE.** Essential to the system but not selected as standalone novelty.

### H3 — Evidence-Targeted Independent Verification
**Original idea:** independent verification is selectively generated/selected to close a specific competence-evidence gap exposed by the student's artifact/process/policy context.

**Prior art found:**
- oral/viva verification of submitted work;
- adaptive viva platforms;
- AI-permitted assessments followed by independent checks;
- code explanation and modification tasks;
- process-evidence-based assessment.

**What remains potentially distinctive:** verification is not merely mandatory or generically adaptive. It is triggered by an explicit unresolved competence claim and is constrained to request the *minimum additional independent evidence* needed to resolve that claim. The verification result feeds back into the same evidence model, with `SUPPORTED`, `PARTIAL`, `UNRESOLVED`, or `CONTRADICTED` competence states. Integrity suspicion is not required to trigger verification.

Example:
- Artifact passes all tests.
- Process shows substantial permitted AI assistance.
- Evidence supports `can integrate API` but not `can explain asynchronous error handling independently`.
- System selects a bounded modification/debug/explanation task specifically targeting asynchronous error handling.
- Result updates that competence claim; it does not decide whether the learner cheated.

**Verdict:** **STRONGEST SURVIVING RESEARCH CANDIDATE, BUT NOVELTY REMAINS BOUNDED/PROVISIONAL.** Adaptive viva and evidence-centered assessment are prior art, so the defensible contribution is the operational coupling of evidence gaps to minimal independent verification inside a programming-exam evidence model.

## 4. Primary contribution selection
Select one primary research contribution for specification:

> **Evidence-Gap-Driven Programming Competence Verification (EGPCV): a policy-aware programming assessment mechanism that constructs bounded competence claims from process/execution/rubric evidence, identifies unresolved or assistance-dependent competence gaps, and selects the minimum targeted independent verification needed to strengthen, contradict, or leave those claims unresolved—without treating automated integrity observations as misconduct verdicts.**

This is a **working contribution statement**, not a claim that no prior system has ever implemented it.

Supporting mechanisms:
1. versioned Examination Capability Contract;
2. typed/provenance-bearing Competence Evidence Model;
3. uncertainty-aware integrity observations and human disposition;
4. targeted independent verification tasks;
5. lab-first/resource-conscious deployment mode.

## 5. Core invariants
1. **Observed event != misconduct verdict.**
2. **Working code != complete evidence of programming competence.**
3. **Permitted assistance != misconduct.**
4. **Assisted success != independent competence unless the assessment construct explicitly permits assistance as part of the competence.**
5. **A competence claim must identify the evidence that supports it and material evidence gaps/contradictions.**
6. **Verification is for acquiring missing competence evidence, not manufacturing suspicion.**
7. **Verification scope must be bounded to the unresolved claim where feasible.**
8. **Consequential integrity findings remain human-authorized.**
9. **Exam policy and accommodations are versioned/server-authoritative.**
10. **Sensitive surveillance is minimized; lab-controlled operation must remain viable without mandatory webcam capture.**

## 6. Kill criteria for EGPCV
P001's research contribution should be demoted/reframed if specification or prototype evidence shows any of the following:
- a directly comparable published/programming-assessment system already performs policy-aware competence-claim construction plus evidence-gap-targeted minimal independent verification in substantially the same way;
- targeted verification does not improve agreement with expert judgments of independent competence over ordinary final-code/tests plus generic viva;
- the mechanism produces excessive verification burden such that most students require broad re-examination;
- evidence gaps cannot be operationalized reproducibly between reviewers;
- targeted tasks are too easy to game or too difficult to generate/validate safely;
- policy/process telemetry adds little useful information beyond simpler assessment evidence;
- false competence conclusions or fairness/accessibility problems remain unacceptable after bounded redesign.

## 7. Required baselines
- **B0:** final submission + ordinary tests/rubric.
- **B1:** compile-and-run exam + ordinary process/event logging.
- **B2:** B1 + generic fixed viva/code explanation.
- **B3:** evidence-centered competence model without targeted verification.
- **B4:** EGPCV: evidence model + gap-driven targeted verification.

The project only earns its added complexity if B4 materially improves competence inference, reviewer efficiency, or evidence quality over B2/B3.

## 8. Evaluation targets for specification
Primary:
- agreement with expert human competence judgments;
- precision/recall or calibrated agreement for selected bounded competence claims;
- reduction in unresolved competence claims after verification;
- verification minutes/questions per resolved gap;
- rate of unnecessary verification;
- inter-rater agreement on evidence-gap identification;
- false integrity escalation rate;
- accessibility/accommodation failures.

Secondary:
- execution latency;
- evidence completeness/provenance integrity;
- student usability/perceived fairness;
- examiner review time;
- bandwidth/resource requirements;
- robustness when AI is allowed versus denied.

No threshold should be invented before benchmark design and pilot data justify it.

## 9. Threat model carried into specification
- malicious/untrusted student code;
- client telemetry spoofing or missing events;
- hidden-test leakage;
- policy tampering/version mismatch;
- unauthorized role access;
- AI-generated verification questions with invalid/ambiguous expected answers;
- prompt injection if AI is used in question generation/review;
- evidence deletion/tampering;
- overcollection of sensitive telemetry;
- denial of service/resource exhaustion;
- collusion/external assistance outside observable runtime;
- accessibility tools incorrectly interpreted as prohibited behavior.

## 10. Scope for first research prototype
The prototype should be intentionally smaller than a full proctoring product:
- one/two programming languages;
- browser editor + sandbox adapter or controlled execution service;
- server-authoritative exam policy;
- code snapshots and compile/run/test events;
- explicit competence/rubric claims;
- evidence-gap engine using deterministic rules first;
- a small validated library of verification task types: explain, predict, modify, debug;
- human examiner review;
- no mandatory webcam;
- no automatic cheating verdict;
- AI optional behind an adapter and never required for deterministic policy/evidence logic.

## 11. Formal-specification questions
Before implementation:
1. Define the competence ontology at a tractable granularity.
2. Define evidence types and admissibility/weight rules without pretending statistical certainty.
3. Define how permitted AI/tool assistance changes which competence claims can be inferred.
4. Define gap-detection rules and when `UNKNOWN` is preferable to inference.
5. Define minimal-verification selection and stopping conditions.
6. Define deterministic verification templates before LLM generation.
7. Define examiner override, rationale, audit and appeal workflow.
8. Define lab-mode threat model and execution isolation.
9. Define accessibility/accommodation representation so exceptions are not exposed unnecessarily.
10. Define benchmark tasks and expert ground-truth procedure.

## 12. Decision
**GO TO FORMAL SPECIFICATION — PROVISIONAL RESEARCH GATE PASS.**

P001 has enough evidence to stop broad ideation. The project should no longer search for a collection of novel features. Its research prototype should test one bounded systems/assessment contribution: **Evidence-Gap-Driven Programming Competence Verification (EGPCV)**.

This GO does not authorize implementation. The next P001 step, when resumed, is a formal specification pass covering requirements, data model, state machines, policy schema, competence/evidence ontology, threat model, baselines, benchmark design, evaluation protocol, acceptance/kill criteria, and file structure.

Portfolio action: park P001 at this research gate and move to the next general/FYP priority project, **P003 — Geopolitical Risk → Economic Impact System**, while P002 remains AJ's personal LLM track and can continue independently.