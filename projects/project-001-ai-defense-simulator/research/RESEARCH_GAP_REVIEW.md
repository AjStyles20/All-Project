# Research Gap Review — Project 001

## Reviewer Position
The initial concept is **not sufficiently differentiated** if framed as an AI presentation coach, virtual audience, interview simulator, or AI Q&A rehearsal tool. Existing products already provide many of those capabilities.

## Rejected / Unsafe Gap Claims
Do not use any of the following without much stronger evidence:
- "There is no AI presentation coach."
- "Existing systems do not generate questions."
- "No existing system allows users to upload slides."
- "No system provides virtual audiences."
- "This is the first AI defense simulator."
- "The system improves confidence."
- "The system objectively measures presentation quality."

## Stronger Gap Candidate
The reviewed public product documentation emphasizes presentation delivery, roleplay, speech analytics, virtual audiences, or generic AI questioning. A narrower opportunity is to focus on **evidence-aware review of the user's own technical/research artifacts**.

### Candidate gap statement
> While reviewed presentation-practice systems provide delivery coaching, roleplay, virtual audiences, and AI-generated questions, the current review did not establish that they provide a transparent workflow for source-grounded, role-specific technical review in which each challenge question and feedback item can be traced to uploaded project evidence, claims, requirements, limitations, or implementation artifacts.

This wording is deliberately limited to the systems reviewed and remains `UNDER REVIEW`.

## Proposed Core Contribution
Project 001 should investigate and implement a review simulator that can:
1. ingest user-provided project/research artifacts;
2. construct a grounded evidence base;
3. generate questions according to configurable reviewer roles;
4. cite or identify the source evidence that motivated each question;
5. challenge unsupported claims, contradictions, missing evidence, and limitations;
6. evaluate answers using explicit criteria while separating source-supported feedback from model judgment;
7. preserve session history for repeated practice and review.

## Why This Is More Defensible
This shifts the project away from subjective claims such as "AI measures confidence" and toward testable engineering questions such as:
- Did the question correspond to the retrieved source?
- Was the cited source actually relevant?
- Did the system identify a known limitation or unsupported claim?
- Did different reviewer roles produce measurably different question categories?
- Can a human reviewer verify the provenance of the feedback?

## Required Validation
Before claiming novelty or effectiveness, Project 001 should evaluate:
- retrieval precision/relevance;
- question grounding;
- unsupported-question rate;
- source attribution correctness;
- persona/role differentiation;
- coverage of important claims and requirements;
- user-perceived usefulness;
- answer-feedback consistency.

## Reviewer Decision
**Architecture may proceed**, provided the MVP is built around source grounding, traceability, reviewer-role differentiation, and explicit uncertainty. Generic delivery coaching should remain secondary.

Status: RESEARCH GAP PROVISIONALLY ACCEPTED / NOVELTY CLAIM STILL UNDER REVIEW.