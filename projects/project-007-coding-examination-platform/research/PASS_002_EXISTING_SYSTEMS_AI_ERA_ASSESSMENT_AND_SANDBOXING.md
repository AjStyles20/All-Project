# Coding Examination Platform — Pass 002: Existing Systems, AI-Era Assessment, and Sandboxing

> ID note: this directory retains the pre-renumbering ID `project-007-*`. As of 10 September 2026 this project is canonical **P001**. Historical paths are preserved to avoid breaking evidence links.

## Decision state
**MORE RESEARCH — STRONG FYP/PRODUCT CANDIDATE, DIFFERENTIATION NOT YET PROVEN.**

## Core question
How can a programming examination capture trustworthy evidence of actual programming competence in the AI era without reducing assessment to either paper coding, simplistic automated judging, or surveillance-driven accusation?

## Prior-art findings
### 1. Secure/sandboxed code execution is established infrastructure
Judge0 already provides scalable sandboxed execution across many languages and is explicitly usable for e-learning and assessment. Open edX CodeJail provides a separate mature example of executing untrusted learner code under OS-level restrictions. Therefore sandboxed execution, multi-language compilation, time/memory limits, and an in-browser coding environment are baseline engineering requirements rather than research novelty.

### 2. Automated grading is mature and becoming AI-assisted
A 2026 systematic review of 39 primary studies describes the field's movement from execution/test-based grading toward ML/LLM-assisted semantic assessment while highlighting reliability and pedagogical-validation gaps. Recent empirical comparisons also show that model/vendor choice can materially affect grades and that even leading LLM graders may align only moderately with human grading. P001 therefore must not delegate final high-stakes grades or misconduct decisions to an opaque model by default.

### 3. AI changes what a submitted program proves
A correct final program is no longer sufficient evidence that the student independently understands the code. Current AI-era assessment work increasingly separates tool-permitted production from independent verification. This supports studying process evidence, bounded oral/code-review checks, debugging tasks, or targeted follow-up rather than treating source-code output alone as competence.

### 4. Paper coding remains an active defensive response
Recent educators still investigate paper-based coding exams specifically because GenAI complicates unsupervised digital assessment. This validates AJ's lived problem but also shows the design tension: removing computers can reduce AI access, yet it also removes the authentic execution/debugging environment in which programming is normally performed.

## Strong novelty threats
- Online judges and IDE-based programming exams already exist.
- Browser lockdown/proctoring and focus/window monitoring already exist.
- Sandboxed execution is established.
- Automated test grading is established.
- LLM/rubric-based programming grading is established.
- GenAI-use detection research exists.
- Independent quizzes/code reviews/oral checks for verifying AI-assisted work exist.

No single item above can be claimed as P001's novelty.

## Candidate mechanisms after Pass 002
### C1 — Evidence-Based Examination Integrity Ledger
Record observable events with provenance, timestamp, policy relevance, limitations, and review state. Events are evidence, not automatic accusations. Example: `WINDOW_FOCUS_LOST` can be recorded without implying `CHEATING=true`.

### C2 — Process-Aware Competence Evidence
Preserve a bounded development trace: revisions, compile/run attempts, failing/passing tests, debugging progression, rubric checkpoints, and final solution. Research question: does this evidence improve assessment validity or reviewer confidence over final-code-only grading without becoming invasive surveillance?

### C3 — Policy-Explicit Exam Runtime
Each assessment declares permitted and prohibited resources: internet, documentation, local references, clipboard, AI, compiler feedback, debugger, tests, packages, collaboration, and accessibility accommodations. Evidence interpretation is relative to the declared policy rather than a universal cheating rule.

### C4 — Triangulated Competence Verification
Combine executable correctness + rubric evidence + bounded process evidence + independent verification when risk/uncertainty warrants it. Independent verification could be a short code explanation, modification, debugging task, or oral follow-up. This is a candidate architecture, not yet a novelty claim.

### C5 — Uncertainty-Aware Human Review
Automated systems may triage or summarize evidence but must expose uncertainty and evidence provenance. High-stakes misconduct and final grading decisions remain human-governed unless later evidence justifies stronger automation.

## Security baseline
Student code is hostile input. The execution service must be isolated from the application/database/network by default, enforce CPU/memory/process/time/file limits, use ephemeral workspaces, prevent privilege escalation, and produce auditable execution results. The application must also protect hidden tests, exam content, credentials, examiner data, and evidence logs. Client-side lockdown cannot be treated as a complete security boundary.

## Falsifiable research directions
1. Compare final-code-only grading against process-aware evidence for agreement with expert assessment.
2. Seed benign and suspicious events and measure false-positive/false-negative behavior of evidence triage.
3. Compare policy-explicit interpretation against universal event rules.
4. Test whether a short independent modification/debugging task better distinguishes superficial/AI-dependent completion from genuine understanding.
5. Measure security/resource isolation under adversarial student programs.

## Kill/reframe criteria
- If process traces add no useful assessment information beyond final code/tests and create disproportionate privacy burden, demote C2.
- If event evidence cannot be interpreted with acceptable false-positive control, avoid misconduct inference and retain logs only for operational/audit purposes.
- If independent verification adds excessive examination time for little validity gain, use it selectively rather than universally.
- If the contribution collapses to ordinary IDE + Judge0 + browser lockdown + auto-grading, P001 must be reframed because that combination is heavily established.

## Pass 002 conclusion
The project remains strong because the underlying assessment problem is real and measurable, but its contribution must sit above the execution layer. The most promising package is currently **policy-explicit examination + process-aware evidence + uncertainty-aware human review + selective independent competence verification**. Pass 003 should attack this package directly against named examination/proctoring platforms, process-mining/programming-trace literature, assessment-validity research, privacy/accessibility requirements, and AI-era competence-verification methods.
