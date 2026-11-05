# P011 Defence Practice: first version results (2026-11-05)

Analysis rules, roles and evaluation were fixed in commit `4796c67` before the final run (seeds 100–139). Raw output: `results/final.json`.

## Method
Generated project reports (about 70 sentences each) with nine planted issues: unsupported claims, one contradiction between two reported figures, and admitted limitations. A session has 12 questions (four reviewers × 3).

| Method | What it asks |
|---|---|
| B0 | A fixed bank of 12 generic defence questions |
| B1 | Questions about 12 random sentences from the report |
| B4 | Questions planned from the analysis findings (this system) |

Two phrasing pools: **dev** (the phrasings I wrote the rules against) and **held-out** (different wording of the same issues, not used while writing the rules).

## Results

| Planted issues reached in 12 questions | Dev phrasing | Held-out phrasing |
|---|---|---|
| B0 generic bank | 0 % | 0 % |
| B1 random sentences | 20 % | 15 % |
| **B4 analysis** | **99 %** | **17 %** |

By kind on held-out phrasing, B4: contradictions 100 %, unsupported claims 0 %, limitations 0 %.

Also measured:
- Every grounded question's quoted sentence is in the passage it cites (100 %, both pools).
- No false alarms among B4's claim, limitation and contradiction findings.
- Roles ask different things: 97 % of a role's question categories are not used by the other roles in the same session.

## Reading it honestly
1. **The rules do not generalise.** On wording they were not written against, B4 is no better than random sentences (17 % against 15 %). Only the contradiction check, which compares figures rather than words, carries over. Keyword lists cannot recognise "No other tool does what our app does" as an unsupported claim or "we could only recruit 8 teachers" as a limitation. This is the main result of this version.
2. Contradictions within one paragraph are missed by design (the check compares different passages): 92.5 % on dev phrasing.
3. Feedback is surface-level: term overlap, figures not in the documents, absolute wording, missing hedges. It does not judge whether an answer is right. Its value is that each item names its criterion and whether it was checked against the documents.
4. The same agent wrote the rules, the generator and both phrasing pools.
5. No language model is connected. Recognising claims and limitations phrased in new ways is the obvious place a model would help, with every model output still tied to a quoted sentence.
