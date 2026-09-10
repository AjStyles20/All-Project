# P007 Research Pass 001 — Problem Lineage and Prior-Art Screen

## Status
DISCOVERY / PROBLEM VALIDATION / PRIOR-ART SCREEN.

## Origin condition
The project originates from a concrete observed problem: programming knowledge is sometimes assessed through handwritten code on paper even though programming practice normally involves editing, compiling/interpreting, executing, testing, debugging, and revising code in a computing environment.

This origin is valuable because it gives P007 a problem-first motivation rather than a feature-first motivation. It does not, by itself, establish novelty.

## Initial problem statement
Design and evaluate a programming examination environment that better represents authentic coding activity while preserving examination integrity, explainable evidence, security, and fairness.

The project must answer two competing requirements:
1. students should be able to demonstrate real programming competence using an actual editor/execution environment;
2. the environment must preserve a defensible examination boundary without converting ordinary user behavior into automatic accusations of cheating.

## Early historical and technical lineage
### Automated programming assessment is old prior art
Automated grading and online-judge systems have existed for decades. A 2003 Computers & Education paper described an Online Judge used in a compulsory first-year programming course with more than 700 students. Therefore electronic code submission, automated testing, and immediate feedback are not novel contributions.

### Paper-versus-computer programming exams are already studied
A 2018 Journal of Computers in Education study directly compared novice programmers taking the same assessment by pen-and-paper versus computer. The paper explicitly notes that pen-and-paper coding is an artificial assessment situation and investigates whether assessment mode affects performance. Its small experiment (20 students) found no statistically significant difference in total score, although the computer group had a higher mean. Therefore P007 must not claim that research has already proven computerized exams universally outperform paper exams.

### Modern secure programming-exam platforms already exist
A 2026 paper describes E-Proctor, a web-based programming examination platform with an integrated development environment, live testing, window monitoring, browser locking, examination management, and automated grading. This is a direct prior-art threat to any claim framed as "a secure web platform where students write and run code during exams."

### Online judges themselves can produce false confidence
An empirical study of 939 coding problems and 541,552 accepted solutions found that many online-judge problem test suites admitted false-positive solutions. This means "all tests passed" is not necessarily equivalent to semantic correctness. P007 evaluation must therefore consider test adequacy and possibly multiple evidence types rather than treating automated execution verdicts as infallible.

## AI-era assessment pressure
Generative AI changes the problem substantially. A 2024 programming-education study found large score increases when students could use an AI programming assistant, but also observed many students accepting incorrect AI-generated answers. This demonstrates that AI access can alter both performance and the interpretation of what an exam score means.

A 2026 ACM report based on more than 750 higher-education computing educators across 49 countries reports a broad shift toward assessment forms such as oral exams, code reviews, debugging exercises, and project-based assessment in response to generative AI. This is important prior art at the assessment-design level: P007 should not assume that stronger surveillance alone is the right answer.

## What is already crowded / not novel
The following cannot currently be treated as standalone novelty:
- browser-based code editor;
- code execution during an exam;
- automated test-case grading;
- browser locking;
- focus/window monitoring;
- plagiarism checking;
- webcam/proctoring;
- exam timers;
- code autosave;
- teacher dashboards;
- real-time submission;
- "AI detection" as a binary cheating detector;
- generic secure online exams.

## Stronger surviving research questions
### Q1 — Evidence-based integrity instead of accusation-based monitoring
Can examination integrity be represented as a bounded, auditable set of events and artifacts that assist authorized human review without automatically classifying a student as dishonest?

Candidate evidence objects:
- code snapshots and revisions;
- compile/run/test events;
- submission timeline;
- focus/tab visibility changes where technically and legally justified;
- clipboard events where explicitly authorized;
- external-resource access only where the platform can reliably observe it;
- optional oral/code-review follow-up evidence;
- examiner annotations;
- final human decision separated from raw telemetry.

Core invariant:
> An integrity event is evidence for review, not a cheating verdict by itself.

### Q2 — Process-aware programming assessment
Can the system evaluate aspects of the programming process, not only the final code artifact?

Potential signals:
- progression from syntax errors to working code;
- debugging attempts;
- test usage;
- revision structure;
- explanation/code-review performance;
- consistency between submitted code and later oral explanation;
- task-specific rubric evidence.

The goal would not be to infer hidden cognition from keystrokes. The goal is to preserve observable process evidence that can support assessment and review.

### Q3 — Assessment modes for the AI era
Can one platform support clearly separated examination policies such as:
- NO-AI coding exam;
- restricted-reference exam;
- open-resource exam;
- AI-permitted exam where AI use itself becomes part of what is assessed;
- coding plus oral defense/code review;
- debugging-oriented examination.

The policy must be explicit and enforceable where technically feasible. The platform must not claim to detect all external AI use when it cannot.

### Q4 — Trustworthy execution and grading
How can untrusted student code be executed with strong resource isolation while preserving reproducible evidence and test validity?

This includes:
- sandbox/container isolation;
- CPU/memory/time limits;
- filesystem/network restrictions;
- deterministic test environments where possible;
- secure secret test handling;
- output limits;
- language/runtime version pinning;
- reproducible grading;
- test-suite adequacy review.

## Candidate contribution directions
### C1 — Evidence-Based Examination Integrity Ledger
A structured event/evidence model that preserves what happened, source/time/context, confidence/limitations, and human-review status without converting telemetry directly into misconduct labels.

Novelty status: UNKNOWN. Similar proctoring/event logging exists; exact gap requires direct comparison.

### C2 — Process-Aware Coding Assessment Record
A versioned attempt record combining code evolution, executions, tests, rubric evidence, and optional oral/code-review verification.

Novelty status: PARTIAL / UNKNOWN. Programming-process analytics and learning analytics are established fields.

### C3 — Policy-Explicit AI-Era Programming Exam Runtime
An exam definition specifies what assistance is allowed, what is prohibited, what tools are available, what evidence is collected, and what verification step is required.

Novelty status: UNKNOWN. Strong product value even if research novelty is limited.

### C4 — Evidence Triangulation for Programming Competence
Instead of relying on one signal such as final code or anti-cheating telemetry, combine:
1. executable correctness;
2. code-quality/rubric evidence;
3. process evidence;
4. optional oral/debugging verification.

Research question: does this reduce false confidence and improve assessment validity compared with final-code-only grading?

Novelty status: UNKNOWN.

## Security and privacy are release gates
P007 handles two high-risk categories simultaneously: untrusted code execution and student assessment/integrity data.

Minimum security questions include:
- How is untrusted code sandboxed?
- Can student code access network, host filesystem, process table, secrets, or other submissions?
- Are resource limits enforced server-side?
- Can hidden test cases be extracted?
- Can users tamper with client telemetry?
- Is server-side authorization enforced independently of the browser?
- Are exam definitions immutable/audited once an attempt begins?
- Is evidence tamper-evident without overstating it as tamper-proof?
- Are logs retained only as long as justified?
- Can a student inspect/export appropriate records?
- Are examiner/admin roles least-privileged?
- Are integrity flags explainable and appealable?

No security claim is valid until concrete threat-model tests pass.

## Accessibility and fairness
Lockdown/proctoring controls can disadvantage legitimate users through assistive technologies, unstable internet, device limitations, OS differences, accidental focus changes, or accessibility accommodations.

Therefore:
- accessibility accommodations must be first-class exam-policy parameters;
- telemetry rules must distinguish permitted accommodations from prohibited assistance;
- network/device failures need explicit recovery policy;
- suspicious-event thresholds cannot be treated as ground-truth misconduct;
- human review and appeal remain required for consequential integrity decisions.

## Initial baseline family
Future evaluation should compare against at least:
B0. pen-and-paper programming assessment;
B1. simple browser editor + final code submission;
B2. conventional online judge with automated tests;
B3. monitored/locked programming exam platform;
B4. P007 evidence-based/process-aware assessment configuration.

Not every study must include all baselines, but the project must avoid comparing itself only to the weakest possible alternative.

## Initial kill/reframe criteria
Reframe or park the research contribution if:
- direct prior art already implements the same evidence model and evaluation;
- integrity telemetry cannot be made sufficiently reliable to be useful without unacceptable false positives;
- secure code execution is infeasible within available deployment constraints;
- process evidence does not improve assessment validity over simpler methods;
- usability/accessibility burden overwhelms educational benefit;
- the strongest implementation becomes merely an ordinary online judge plus proctoring.

## Current assessment
Problem reality: STRONG.
Engineering feasibility: LIKELY, but sandboxing/deployment must be proven.
Academic relevance: STRONG.
Novelty: UNKNOWN.
FYP suitability: HIGH, pending prior-art and evaluation design.
Product potential: HIGH for schools/universities/training organizations if governance and security are handled correctly.

## Decision
MORE RESEARCH.

The original problem survives strongly, but the obvious implementation (IDE + online judge + monitoring) is already prior art. The next research pass should attack C1-C4 and inspect current open-source/commercial systems, academic programming-assessment research, sandboxing architectures, anti-cheating/proctoring limitations, AI-era assessment policies, and evidence/appeal governance.
