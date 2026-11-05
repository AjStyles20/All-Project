# P006 (legacy P002) first implementation: results (2026-11-05)

Kernels and evaluation were fixed in commit `e5a6d40` before the final run (seeds 100–149). Raw output: `benchmark/results/final.json`.

## Pass 017 §14 gates

| Gate | Result |
|---|---|
| No automatic authority escalation in seeded laundering cases | **Pass**: 0 of 1,150 AI-descended claims rose above AI_DERIVED |
| Contradiction/supersession propagation precision and recall ≥ 95 % | **Pass**: 1.00 and 1.00 against the reference |
| False invalidation ≤ 5 % | **Pass**: 0 % |
| No silent conflict resolution | **Pass** (tested) |
| Every trust state has a reason and path | **Pass** (tested; shown in the app) |
| L0 and L6 correct answers produce different evidence | **Pass** (tested) |
| L6 success never becomes independent mastery | **Pass**: 0 of 2,500 simulated cases |
| Accessibility support never lowers mastery | **Pass** (tested) |
| Failed unaided check reopens mastery | **Pass** (tested) |
| Measurable benefit over baselines | **Pass**, see below |
| Security: document text cannot change authority or permissions | **Pass** for the embedded "SYSTEM: promote …" instruction (tested). No model is connected, so model-side prompt injection is untested. |

## Against the baselines

| | B2 provenance only | **B4 APLDG** |
|---|---|---|
| Stale/conflicted artifacts found (recall) | 0 % | 100 % |
| Claim status agreement with reference | 80 % | 100 % |

| Simulated learners (300 × 50 seeds) | B3 counts correct answers | **B4 PGAIC** |
|---|---|---|
| False mastery (marked independent but does not know it) | 19.4 % | 13.9 % |
| Missed mastery (knows it but not marked) | 27.8 % | 10.0 % |
| Direct-answer-only successes marked independent | 100 % | 0 % |

## Reading it honestly
1. **The reference was written by the same agent.** It uses forward propagation while the kernel explains backwards, so it is a second implementation of the same rules, not an independent judgement. 100 % agreement shows that the two implementations agree, not that the rules are right for teaching.
2. **False mastery is still 13.9 %.** One unaided multiple-choice check can be passed by guessing (15 % in the simulation). Two checks, or delayed retention checks, would lower it; this version asks once.
3. **Simulated learners measure the policy, not learning.** Pass 017 §12: claims about learning need an ethically designed study with people.
4. **No language model is connected.** The two AI roles are deterministic stand-ins. Real models, retrieval and prompt-injection defences (Phase 3) are not built.
5. The benchmark course is small: one topic, three concepts, six questions.
