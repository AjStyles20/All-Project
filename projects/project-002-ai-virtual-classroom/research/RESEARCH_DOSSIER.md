# Project 002 Research Dossier — AI-Powered Virtual Classroom and Adaptive Learning Environment

## Research status
DISCOVERY / EVIDENCE BUILD — expanded third pass. No novelty conclusion and no implementation approval.

## 1. Working concept under investigation
A virtual learning environment in which a learner can provide course/learning materials and interact with configurable AI teacher/tutor/classroom roles. Candidate capabilities include structured lessons, explanations, questioning, discussion, multiple pedagogical/persona roles, speech, resource-grounded answers, adaptive support, and later richer classroom/audience simulation.

This description is a hypothesis about a useful product, not evidence that the combination is novel or educationally effective.

## 2. Historical and technical lineage
### 2.1 Mechanical and programmed instruction
- Technology-mediated instruction predates electronic computers. Discovery evidence includes twentieth-century teaching-machine work and historical scholarship tracing patented educational devices into the nineteenth century.
- The relevant historical contribution is not merely the physical machine: programmed instruction formalized sequenced learner interaction, feedback, pacing, and instructional logic. Project 002 must therefore treat “adaptive sequence” and “automated feedback” as historically deep ideas rather than generative-AI inventions.

**Claim state:** SUPPORTED; nineteenth-century primary patent/device review remains incomplete.

### 2.2 PLATO and generalized computer-assisted instruction
- University of Illinois and ERIC historical records establish PLATO as a major early computer-based learning environment originating around 1959–1960. PLATO developed from a small classroom system into a geographically distributed educational network and supported courseware across numerous disciplines.
- PLATO is particularly relevant because it weakens any simplistic claim that a networked “virtual classroom” is new. Historical PLATO systems combined computer-delivered instruction with communication/community capabilities; later PLATO environments included chat and bulletin-board functions.
- A 1977 University of Illinois final report documents a large geographically dispersed PLATO IV network, educational programs, teacher/author training, curriculum planning, materials development, field testing, and evaluation planning.
- Historical assessments are not uniformly celebratory. A later review of PLATO and TICCIT describes both as foundational to later computer-based teaching while also stating that neither large demonstration project proved successful. This is important counterevidence against technological determinism.

**Claim state:** VERIFIED for PLATO's existence, broad chronology and educational-network role; detailed outcome claims require source-specific treatment.

### 2.3 Intelligent tutoring and cognitive tutors
- Intelligent tutoring predates LLMs by decades. The field moved beyond fixed computer-assisted instruction toward systems representing domain knowledge, learner state and instructional strategy.
- Anderson, Corbett, Koedinger and Pelletier's *Cognitive Tutors: Lessons Learned* reviews roughly a decade of tutor development based on ACT cognitive models, including tutors for LISP, geometry and algebra. This establishes model-based adaptive tutoring as mature prior art by the 1990s.
- Therefore, learner modeling, skill tracking, adaptive problem selection and individualized hints cannot by themselves constitute Project 002 novelty.

**Claim state:** VERIFIED at publication-summary level; foundational ITS architecture and SCHOLAR/Carbonell primary-source extraction remains pending.

### 2.4 Conversational tutoring
- By 2001, Graesser et al. described intelligent tutoring systems using mixed-initiative conversational dialogue. AutoTutor supported typed natural-language interaction and guided learners through multi-turn construction of answers rather than functioning as simple information delivery.
- AutoTutor literature includes feedback, prompts, hints, misconception correction, learner questions and answer summarization.

**Claim state:** VERIFIED. Conversational tutoring and talking/animated tutor concepts are established prior art.

### 2.5 Pedagogical agents, teachable agents and collaborative learning
- Pedagogical-agent research predates contemporary generative AI by decades. Systematic reviews show agents serving tutor, peer, coach, facilitator and other roles; visible anthropomorphism or learner preference does not reliably imply stronger learning outcomes.
- Teachable-agent research is particularly relevant because it reverses the normal tutor relationship: the learner teaches or guides an artificial agent, using learning-by-teaching, explanation and reflection as the pedagogical mechanism. Therefore, “AI classmates” or “AI peers” cannot be treated as a new idea merely because they are not the teacher.
- A 2022 two-phase systematic review of pedagogical-agent communication found agents can support intrapersonal processes such as self-regulation, self-efficacy, motivation and metacognition and can scaffold group learning, while also concluding that then-current pedagogical agents could not replicate instructional communication.
- A 2026 systematic review of AI agents in computer-supported collaborative learning synthesized 46 empirical studies from 2014–2025. It reports AI agents performing cognitive scaffolding, social facilitation and instructional orchestration, often in small-group problem-solving contexts. Cognitive outcomes were generally positive in the reviewed corpus, while behavioral, social and emotional outcomes were more context-dependent.

**Novelty implication:** peer-like agents, group facilitation, collaborative AI agents, social roles and instructional orchestration are all prior art. The relevant question is not whether Project 002 can simulate classmates, but whether a particular multi-role design creates measurable value beyond simpler alternatives.

**Claim state:** VERIFIED at systematic-review level; direct head-to-head multi-agent versus single-agent evidence remains insufficient.

### 2.6 Contemporary RAG / generative-AI tutoring
- Contemporary research includes RAG-based tutors grounded in instructor/course materials. Recent educational RAG work still reports or reviews problems such as incorrect answers, hallucination, stale knowledge and limited multimodality.
- Lightweight/resource-constrained RAG tutoring is already an explicit research direction. Project 002 therefore cannot claim novelty merely from combining user/course materials, retrieval grounding, AI tutoring and low-resource operation.

**Claim state:** VERIFIED at source-summary level; deeper comparative extraction continues.

### 2.7 LLM multi-agent classroom simulation
- SimClass (NAACL 2025) describes an LLM-powered multi-agent classroom simulation with representative classroom roles, automatic classroom control, real-user participation and teacher-student/student-student interaction.
- This directly threatens novelty claims based only on “AI teacher + AI students,” “multiple classroom personas,” or “simulated classroom interaction.”

**Claim state:** VERIFIED from published record; full-paper feature/evaluation matrix remains pending.

## 3. Evidence on educational effectiveness — do not flatten into one claim
### 3.1 Established ITS evidence
- Ma et al. (2014) meta-analyzed 107 effect sizes involving 14,321 participants. ITS use was associated with greater achievement than teacher-led large-group instruction, non-ITS computer instruction, and textbooks/workbooks in that analysis, while differences versus individualized human tutoring and small-group instruction were not significant.
- A 2025 systematic review of AI-driven ITS in K–12 analyzed 28 studies involving 4,597 students. It reports generally positive effects, but those effects were reduced when ITS were compared with non-intelligent tutoring systems; the review calls for longer interventions, larger/diverse samples and more attention to ethics.
- These results strengthen the case for tutoring as a useful design space while simultaneously weakening any claim that “intelligence” or generative AI automatically creates large learning gains.

### 3.2 Generative-AI tutor evidence
- A 2025 randomized controlled trial in an undergraduate physics course (N=194) reported greater learning in less time and higher engagement/motivation for a research-informed AI tutor compared with an in-class active-learning condition using the same material.
- A 2024 study of mathematics help (N=274) found ChatGPT-generated help could produce learning gains comparable to human tutor-authored help in the tested design.
- A 2026 systematic review/meta-analysis of generative AI in STEM included 85 eligible studies and 49 studies/59 effect sizes in the meta-analysis. It reports a positive overall effect on cognitive outcomes but extremely high heterogeneity (I²=96.32%), a prediction interval spanning negative to positive effects, and possible publication bias. This is strong evidence against presenting GenAI learning effects as uniform.

**Claim state:** VERIFIED for the cited reviews/studies; external validity to Project 002 NOT ESTABLISHED.

### 3.3 Multi-agent / collaborative-agent evidence
- The 2026 CSCL systematic review provides evidence that AI agents can support cognitive scaffolding, social facilitation and orchestration in collaborative learning. However, this does not establish that a simulated classroom containing multiple AI peers is superior to a single well-designed tutor.
- The evidence currently located is heterogeneous in agent roles, platforms, subjects, populations and outcomes. A direct, generalizable “multi-agent > single-agent” educational effect has NOT been established in this dossier.

**Claim state:** COLLABORATIVE-AGENT VALUE SUPPORTED IN SOME CONTEXTS; SUPERIORITY OVER SINGLE AGENT UNKNOWN.

## 4. Cognitive offloading, dependency and learner agency
This is now a core design/evaluation issue, not a side-risk.

- A 2026 scoping review of 123 studies on generative AI, cognitive offloading and learner agency in higher education describes a dual pattern: scaffolded/augmentation-oriented use can support self-regulation, self-efficacy, feedback literacy and reflective engagement, while replacement-oriented use is associated with overreliance, cognitive offloading, dependence, uncritical uptake and weakened judgment. The review explicitly treats this as a synthesis of heterogeneous evidence, not a causal effect estimate.
- A 2026 systematic review of GenAI and cognitive load found effects were conditional on scaffolding, dosage, prior knowledge and task design. It warns that lower cognitive load is not automatically beneficial: a system can reduce unproductive load, but it can also displace productive thinking.
- A 2026 systematic review/meta-analysis in STEM similarly reports high heterogeneity and possible publication bias, reinforcing the need for task-level and design-level evaluation rather than broad “AI improves learning” claims.
- Recent systematic reviews of higher-order cognition also identify overreliance, reduced analytical autonomy and cognitive offloading as recurring risks, particularly under weak pedagogical framing.

**Design implication:** Project 002 should not optimize for “make every task easier.” A defensible design would distinguish *scaffolding* from *substitution*. Candidate controls include staged hints, learner-first attempts, explanation/justification requirements, retrieval/source inspection, reflection prompts, uncertainty checks, delayed assistance, and teacher-configurable autonomy levels. These are design hypotheses until experimentally evaluated.

**Evaluation implication:** If Project 002 proceeds, success metrics should include retention, transfer, independent post-assistance performance, calibration/verification behavior and learner agency—not only immediate task completion, satisfaction or perceived helpfulness.

## 5. Commercial/current-practice novelty threats
### 5.1 Khanmigo / Khan Academy
- Current Khan Academy materials describe Khanmigo as an AI tutor and teaching assistant. Learner-facing behavior is framed around guiding students rather than simply giving direct answers.
- Teacher capabilities include lesson planning, classroom activities, student-work summaries, learning objectives, rubrics, exit tickets, differentiation and student grouping.
- Student access is governed more tightly than ordinary consumer chatbot access; current Khan Academy materials describe parent/school/district controls for minors and moderation/safety mechanisms.
- In 2026, Google and Khan Academy publicly described classroom AI tooling using Gemini, including adaptive visual aids and teacher-controlled assignment/practice tooling.

**Novelty implication:** “AI tutor,” “teacher assistant,” “Socratic guidance,” “teacher planning tools,” “student progress summaries,” “content-library grounding,” and “AI in real classrooms” are not defensible novelty claims by themselves.

**Claim state:** VERIFIED from current official product/help materials; feature landscape remains non-exhaustive.

## 6. Open-source implementation evidence
### 6.1 OATutor
- CAHLR's OATutor is a public open-source adaptive tutoring system. Direct repository inspection shows Bayesian Knowledge Tracing for mastery estimation, adaptive item selection, modular hints/scaffolding, multiple content sources, data logging, optional LMS integration, optional text-to-speech and accessibility work.
- The repository cites a CHI 2023 paper and a later journal study involving LLM-generated help. It can operate largely as a frontend application with optional Firebase/middleware components.
- Direct repository metadata/README inspection confirms it is a substantive implementation rather than a paper-only concept.

**Novelty implication:** Open-source adaptive tutoring, skill mastery estimation, scaffolding/hints, content-source modularity, LMS integration, accessibility work and optional speech already exist in concrete prior art.

### 6.2 Broader GitHub discovery
- GitHub discovery surfaces multiple repositories explicitly describing LLM tutoring, RAG tutoring and intelligent tutoring. Discovery results alone are not proof of quality or equivalence; candidate repositories require direct inspection before entering the verified evidence matrix.

## 7. Updated prior-art / novelty-threat register
| Threat | What it already establishes | What remains open |
|---|---|---|
| Teaching machines / programmed instruction | Automated sequencing, pacing and feedback have deep roots. | Which principles transfer effectively to generative systems. |
| PLATO / CAI | Networked computer-based learning, courseware and educational communication predate the web/LLMs. | Which modern constraints/problems remain unsolved. |
| Cognitive Tutors / ITS | Learner modeling, domain models, adaptive tutoring and skill-sensitive support are established. | Whether generative orchestration adds measurable value. |
| AutoTutor | Multi-turn natural-language tutoring, hints and feedback predate LLMs. | Reliability/provenance and broader orchestration remain possible research areas. |
| Pedagogical/teachable agents | Artificial tutor/peer/learner roles and learning-by-teaching are established. | Which roles measurably help which learners/tasks. |
| Collaborative-learning agents | AI-supported cognitive/social/orchestration roles in group learning are established. | Direct multi-agent vs single-agent value remains insufficiently established. |
| Educational RAG | Course/source-grounded AI tutoring already exists. | Stronger provenance/source-bound uncertainty may remain open. |
| SimClass | Multi-agent LLM classroom simulation with user participation exists. | Exact overlap/gaps after full-paper extraction. |
| Khanmigo | Current AI tutor + teacher assistant with classroom workflows and safety controls exists. | Different deployment contexts, provenance, multi-role simulation, offline/local control, research transparency. |
| OATutor | Open-source adaptive tutor with BKT, scaffolding, content sources, accessibility and LMS integration exists. | Multi-role generative classroom and source-provenance questions require proof of value. |
| Cognitive-offloading literature | GenAI can support or erode learner agency depending on design/use. | Which safeguards reliably preserve long-term independent competence. |

## 8. Candidate gaps — UNDER REVIEW, not novelty claims
1. **Evidence/provenance across roles:** Can every teacher/peer/tutor claim be traced to authoritative user/course material, with source-bound uncertainty visible to the learner?
2. **Pedagogically constrained multi-role orchestration:** Can AI roles have explicit instructional functions and state transitions rather than merely different personalities/prompts?
3. **Inspectable pedagogy:** Can teachers/users see and configure why a role asks, hints, challenges, remediates or advances rather than having pedagogy hidden inside prompts?
4. **Multi-agent value test:** Does simulated peer/classroom interaction produce measurable benefit over a single high-quality tutor, or is it mostly interface theater and additional cost/latency/hallucination surface?
5. **Anti-offloading pedagogy:** Can assistance be deliberately designed to preserve learner reasoning, verification and independent performance rather than maximize answer convenience?
6. **Low-resource trustworthy degradation:** Can the platform retain useful source-grounded learning on modest hardware/connectivity while clearly marking unavailable generative functions?
7. **Human-teacher augmentation boundary:** Which functions should remain teacher-controlled or human-reviewed instead of being delegated to agents?
8. **Longitudinal learning and dependency:** Does repeated use improve retention/transfer, or encourage overreliance/cognitive offloading?
9. **Accessibility by design:** Can multimodal interaction remain optional and equivalent, rather than making voice/avatars/VR prerequisites?
10. **Evaluation transparency:** Can the project expose what was measured, what evidence supports feedback/adaptation, and what remains uncertain?

None of these is yet an established novelty gap.

## 9. Claims registry
| ID | Claim | State | Evidence boundary |
|---|---|---|---|
| P002-C001 | Technology-mediated teaching predates electronic computers. | SUPPORTED | Historical review/collections; primary patent expansion pending. |
| P002-C002 | PLATO provided generalized/networked computer-assisted learning beginning around 1960. | VERIFIED | Illinois/ERIC historical records. |
| P002-C003 | Model-based adaptive/cognitive tutoring was mature prior art by the 1990s. | VERIFIED | Cognitive Tutor literature. |
| P002-C004 | Conversational ITS existed before modern LLMs. | VERIFIED | AutoTutor/ITS literature. |
| P002-C005 | Pedagogical and teachable agents have established educational lineages. | VERIFIED | Systematic/review literature. |
| P002-C006 | ITS can improve learning in some contexts. | VERIFIED | Meta-analytic/systematic evidence, with comparator/heterogeneity caveats. |
| P002-C007 | A research-informed generative AI tutor outperformed one active-learning condition in a 2025 RCT. | VERIFIED | Specific N=194 undergraduate physics study only. |
| P002-C008 | Course/source-grounded RAG tutoring is existing prior art. | VERIFIED | Contemporary educational RAG literature. |
| P002-C009 | Multi-agent LLM classroom simulation exists. | VERIFIED | SimClass NAACL 2025. |
| P002-C010 | Current Khanmigo overlaps several tutor/teacher-assistant functions. | VERIFIED | Official current product/help material. |
| P002-C011 | A substantial open-source adaptive tutoring implementation exists in OATutor. | VERIFIED | Direct GitHub repository inspection. |
| P002-C012 | AI agents have been used for collaborative-learning scaffolding/social facilitation/orchestration. | VERIFIED | 2026 CSCL systematic review of 46 empirical studies. |
| P002-C013 | Project 002 is unique. | UNSUPPORTED | Must not be claimed. |
| P002-C014 | Project 002 will improve learning. | UNSUPPORTED | Requires Project 002-specific evaluation. |
| P002-C015 | Multiple AI classroom roles improve learning over a single tutor. | UNKNOWN | Direct comparative evidence not established. |
| P002-C016 | Lower cognitive load caused by AI necessarily means better learning. | CONTRADICTED | Reviews distinguish useful load reduction from cognitive substitution/offloading. |
| P002-C017 | GenAI effects on learning are uniformly positive. | CONTRADICTED | High heterogeneity, context dependence and possible publication bias in recent reviews/meta-analysis. |

## 10. Contradictions and caution
- Positive ITS and GenAI findings coexist with heterogeneous effects, comparator dependence, implementation dependence and population/context limits.
- K–12 ITS evidence can look positive while advantages shrink against non-intelligent tutoring comparators; “AI” itself is not the causal contribution.
- A classroom-like interface, avatars, speech or social presence are not evidence of better pedagogy.
- Multiple agents can increase interaction richness while simultaneously increasing latency, cost, inconsistency, privacy surface and hallucination pathways.
- Lower cognitive load can represent good scaffolding or harmful substitution of productive thought; the direction cannot be inferred from a single load score.
- Grounding/RAG can reduce some knowledge errors but does not make generated claims automatically correct.
- Commercial product claims are evidence of product capabilities/positioning, not independent proof of learning effectiveness.
- GitHub popularity/activity is evidence that an implementation is real and maintained, not that its pedagogical claims are true.

## 11. Search / inspection log — pass 3
### Scholarly/counterevidence discovery
- `AI peer learning teachable agents multi-agent tutoring classroom systematic review pedagogical agents social learning`
- `LLM multi-agent education classroom tutoring single agent multi agent learning outcomes 2025 2026`
- `generative AI education cognitive offloading dependency learning retention transfer systematic review 2025 2026`
- `AI tutoring privacy minors accessibility education AI guidance 2025 2026`

### Independent academic database/plugin cross-check
- Consensus: systematic-review search for AI pedagogical agents, collaborative learning and multi-agent tutoring, 2018–2026.
- Consensus record fetched for Ba, Shi, Wu & Lu (2026), *Artificial intelligence agents in computer-supported collaborative learning: A systematic literature review*.
- Consensus record fetched for Létourneau et al. (2025), *A systematic review of AI-driven intelligent tutoring systems (ITS) in K-12 education*.
- Web discovery independently surfaced the Ba et al. review, providing cross-tool corroboration of the same publication.

### GitHub prior-art inspection
- Direct inspection retained for `CAHLR/OATutor` README and repository metadata.
- Broader repository discovery remains screening-only until individual repositories are inspected.

## 12. Sources screened / retained so far
Historical/foundational:
1. Smithsonian teaching-machine historical collection.
2. Benjamin (1988), *A History of Teaching Machines* — primary-source expansion pending.
3. University of Illinois / ERIC PLATO historical records and PLATO IV report.
4. Anderson, Corbett, Koedinger & Pelletier, *Cognitive Tutors: Lessons Learned*.
5. Graesser et al. (2001), *Intelligent Tutoring Systems with Conversational Dialogue*.
6. AutoTutor natural-language dialogue literature.
7. Pedagogical-agent historical/systematic reviews.
8. Teachable-agent literature and reviews.

Effectiveness/contemporary:
9. Ma et al. (2014), ITS learning-outcomes meta-analysis.
10. Létourneau et al. (2025), K–12 AI-driven ITS systematic review — 28 studies, N=4,597.
11. 2025 Scientific Reports RCT of research-informed generative AI tutor in undergraduate physics, N=194.
12. Pardos & Bhandari (2024), ChatGPT-generated versus human-authored mathematics help, N=274.
13. Ba, Shi, Wu & Lu (2026), AI agents in computer-supported collaborative learning — systematic review of 46 empirical studies from 2014–2025.
14. 2026 GenAI-in-STEM systematic review/meta-analysis — 85 eligible studies, 49 studies/59 effect sizes meta-analyzed; high heterogeneity and possible publication bias.
15. 2026 scoping review of GenAI, cognitive offloading and learner agency — 123 included studies.
16. 2026 systematic review of GenAI and cognitive load — 39 empirical studies; conditional effects and explicit offloading distinction.
17. Contemporary educational RAG studies/surveys.
18. Hevia, Arredondo & Kumar (2025), lightweight/customizable/accessible AI tutor work.
19. Zhang et al. (2025), SimClass, NAACL 2025.

Current systems/open source:
20. Khan Academy official Khanmigo materials.
21. Google/Khan Academy 2026 classroom AI announcement/material.
22. CAHLR/OATutor repository and README.

## 13. Evaluation consequences if Project 002 survives research
A credible experiment should avoid evaluating only “Did users like it?” or “Did they finish the task?” Candidate comparison arms:
- conventional/self-study material;
- single-agent grounded tutor;
- multi-role grounded classroom;
- optionally multi-role classroom with explicit anti-offloading scaffolds.

Candidate outcomes:
- immediate learning gain;
- delayed retention;
- transfer to novel problems;
- independent post-assistance performance;
- source/evidence verification behavior;
- calibration of trust in AI answers;
- learner agency/self-regulation;
- cognitive load separated into meaningful components where feasible;
- time-on-task;
- interaction cost/latency;
- hallucination/unsupported-claim rate;
- accessibility/usability;
- teacher/user control and inspectability.

This evaluation design is itself provisional and must be matched to the eventual target population and domain.

## 14. Coverage audit after pass 3
Still missing or insufficient:
- nineteenth-century primary patents/devices and broader international historical lineage;
- foundational SCHOLAR/Carbonell primary-source extraction;
- full SimClass paper feature/evaluation extraction;
- direct head-to-head evidence comparing multi-agent/classroom simulation with a single tutor;
- deeper teachable-agent primary studies beyond reviews;
- current commercial competitor matrix beyond Khanmigo;
- direct inspection of additional open-source tutoring/RAG systems;
- patents overlapping multi-agent tutoring/classroom simulation;
- standards/interoperability including LTI and education-data standards where relevant;
- jurisdiction-specific privacy/child-safety/education regulation once deployment population is defined;
- accessibility requirements beyond isolated product claims;
- security threat model for user-uploaded course materials, prompt injection, cross-class/workspace leakage and agent/tool authorization;
- costs/model-provider dependencies and offline/local feasibility;
- longitudinal evidence on dependency, retention and transfer;
- precise user/problem validation;
- empirical evidence that “classroom simulation” is preferable to a simpler tutor for a concrete user need.

## 15. Current decision
**MORE RESEARCH.**

The third pass further weakens feature-level novelty but strengthens the research problem. The most defensible direction currently visible is not “build an AI classroom because AI classmates are novel.” It is to test whether a transparent, source-grounded, pedagogically constrained multi-role environment can add measurable learning value while preserving learner agency better than simpler AI-tutor designs. That proposition remains an UNVERIFIED HYPOTHESIS and must survive competitor, patent, security/privacy, feasibility and direct comparative-evidence review before implementation approval.
