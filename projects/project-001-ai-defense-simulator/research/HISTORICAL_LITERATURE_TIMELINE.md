# Project 001 Historical Literature Timeline

## Purpose
Trace the intellectual and technical lineage relevant to an AI-assisted presentation, viva, defense, and interview practice system from foundational intelligent tutoring and speech-interaction work through modern document-grounded LLM systems.

This file contains **screened** sources only. Search hits that have not been checked remain in the research search log and are not treated as evidence.

## 1990s — Speech-Aware Tutoring and Interactive Assistance

### Aist & Mostow (1997) — *When Speech Input is Not an Afterthought: A Reading Tutor that Listens*
- Strand: speech-based tutoring / interactive educational systems
- System/context: Project LISTEN Reading Tutor
- Contribution: demonstrated a computer tutor that listened to learners read aloud and provided assistance during spoken interaction.
- Relevance to P001: establishes that speech input, conversational timing, and adaptive assistance in educational software predate modern LLMs by decades.
- Limitation for P001: domain is oral reading, not presentation defense or open-ended viva questioning.
- Evidence status: SCREENED
- Source: https://publications.ri.cmu.edu/when-speech-input-is-not-an-afterthought-a-reading-tutor-that-listens

### Mostow & Aist (1999) — *Giving Help and Praise in a Reading Tutor with Imperfect Listening – Because Automated Speech Recognition Means Never Being Able to Say You're Certain*
- Strand: speech recognition uncertainty / tutor feedback
- Contribution: explicitly examined how imperfect speech recognition should influence the timing and confidence of automated help and praise.
- Relevance to P001: important design precedent for not treating speech-recognition output as infallible; future voice-enabled feedback should expose uncertainty where relevant.
- Limitation for P001: focused on reading assistance rather than assessment of technical explanations or presentations.
- Evidence status: SCREENED
- Source: https://publications.ri.cmu.edu/giving-help-and-praise-in-a-reading-tutor-with-imperfect-listening-because-automated-speech-recognition-means-never-being-able-to-say-youre-certain

## 2000s — Conversational Intelligent Tutoring

### Graesser, VanLehn, Rosé, Jordan, & Harter (2001) — *Intelligent Tutoring Systems with Conversational Dialogue*
- Strand: mixed-initiative conversational tutoring
- Contribution: described systems including AutoTutor that use multi-turn natural-language dialogue, questions, hints, feedback, and guided construction of answers.
- Relevance to P001: strongly overlaps with the proposed interaction pattern of examiner question → user answer → follow-up → feedback.
- Limitation for P001: systems were built around instructional domains and typed dialogue; not document-grounded project defenses or multimodal presentation evaluation.
- Evidence status: SCREENED
- DOI: 10.1609/aimag.v22i4.1591
- Source: https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/1591/0

### Mostow et al. (2003) — *Evaluation of an Automated Reading Tutor That Listens: Comparison to Human Tutoring and Classroom Instruction*
- Strand: evaluation of speech-enabled tutoring
- Context: year-long study with 131 second- and third-grade students in 12 classrooms.
- Contribution: provides an early example of evaluating an automated spoken tutor against human tutoring and normal classroom instruction.
- Relevance to P001: useful methodological precedent for separating system implementation from empirical evaluation and for comparing automated support against meaningful baselines.
- Limitation for P001: population, domain, and outcome measures differ substantially from presentation/viva practice.
- Evidence status: SCREENED
- DOI: 10.2190/06AX-QW99-EQ5G-RDCF
- Source: https://journals.sagepub.com/doi/10.2190/06AX-QW99-EQ5G-RDCF

## 2010s — Automatic Question Generation

### Heilman & Smith (2010) — *Good Question! Statistical Ranking for Question Generation*
- Strand: automatic question generation from text
- Contribution: generated literal reading-comprehension questions from informational text through transformation and statistical ranking.
- Relevance to P001: establishes a pre-LLM line of work for generating questions from supplied source material.
- Limitation for P001: largely factual/literal question generation; it does not by itself provide adversarial viva-style follow-up, persona control, or conversational defense simulation.
- Evidence status: SCREENED
- Source: https://www.cs.cmu.edu/~ark/mheilman/questions/

## 2020s — Automated Presentation Feedback and Immersive Practice

### Van Ginkel (2020) — *The impact of computer-mediated immediate feedback on developing oral presentation skills: An exploratory study in virtual reality*
- Strand: presentation coaching / immediate automated feedback / virtual reality
- Contribution: experimentally examined computer-mediated immediate feedback in a VR environment for presentation-skill development.
- Relevance to P001: directly supports the existence of automated presentation-practice systems and shows that feedback timing and presentation-performance outcomes are established research concerns.
- Limitation for P001: presentation-skill coaching is not equivalent to document-grounded defense questioning.
- Evidence status: SCREENED
- DOI: 10.1111/jcal.12424
- Source: https://onlinelibrary.wiley.com/doi/full/10.1111/jcal.12424

## 2024+ — Retrieval-Augmented Assessment and Grounded Educational Dialogue

### Han et al. (2024) — *Improving Assessment of Tutoring Practices using Retrieval-Augmented Generation*
- Strand: RAG / automated assessment / tutoring evaluation
- Contribution: compared multiple prompting strategies for automated assessment of tutoring practices and reported that RAG prompting improved correctness/hallucination behavior and cost within the studied setting.
- Relevance to P001: supports investigating RAG for feedback and evaluation where the system must ground judgments in explicit rubrics or reference material.
- Limitation for P001: evaluates tutor practices, not student presentations or defenses; results should not be generalized without testing.
- Evidence status: SCREENED
- Source: https://proceedings.mlr.press/v257/han24a.html

### Van Ginkel-related AI feedback work (2024–2025 research line)
- Strand: AI presentation feedback
- Current evidence: recent work explicitly compares AI-only presentation feedback with teacher-supported AI feedback.
- Relevance to P001: indicates that the key research question is no longer whether automated presentation feedback exists, but under what conditions it is useful, interpretable, and sufficient.
- Evidence status: DISCOVERY / NEEDS FULL SCREENING BEFORE CLAIM USE
- Source: https://research.ou.nl/en/publications/can-ai-feedback-stand-alone-for-fostering-students-presentation-p/

## 2026 — LLM-Mediated Oral/Performance Assessment

### Daylamani-Zad (2026) — AIvaluate performance-based assessment study
- Strand: LLM conversational assessment / oral presentation and viva experience
- Contribution: reports an LLM-augmented conversational agent evaluated in performance-based assessment settings including oral presentations and viva-voce style assessment, with 35 pre-university students.
- Relevance to P001: this is highly adjacent prior art and materially constrains any novelty claim around “AI viva simulator” or “AI presentation assessment.”
- Limitation for P001: a detailed feature/architecture comparison is still required before determining what is distinct.
- Evidence status: SCREENED AT ABSTRACT LEVEL; FULL PAPER REVIEW REQUIRED
- DOI: 10.1007/s11423-026-10634-x
- Source: https://link.springer.com/article/10.1007/s11423-026-10634-x

## Interim Interpretation
The literature already shows that the following components are **not novel by themselves**:
- intelligent tutoring;
- mixed-initiative conversational questioning;
- speech-enabled tutoring;
- automatic question generation from text;
- automated presentation feedback;
- RAG-based educational assessment;
- LLM-mediated oral/performance assessment.

Therefore Project 001 must not claim novelty from simply combining “AI + presentation + questions + feedback.” The defensible contribution, if one exists, will need to be narrower and supported by a detailed comparable-system analysis. Candidate differentiators to investigate include:
- user-document-grounded defense questioning across arbitrary project domains;
- explicit examiner-panel personas with traceable questioning behavior;
- multi-turn follow-up questions tied to gaps or contradictions in the user's prior answer;
- evidence-linked feedback that separates content accuracy, defense quality, and presentation delivery;
- transparent uncertainty/provenance rather than opaque AI scores;
- a workflow that supports both presentation rehearsal and adversarial viva/defense practice in one system.

These are **candidate differentiators only** and are not yet verified research gaps.

## Next Screening Tasks
1. Review AIvaluate in detail and identify architecture/features/evaluation dimensions.
2. Screen modern document-grounded tutoring and question-generation systems.
3. Build a comparable-system matrix for commercial and research systems.
4. Search older literature on oral examinations, computer-assisted speaking assessment, and presentation feedback.
5. Pass the screened evidence to the Research Gap Reviewer before any novelty statement is approved.
