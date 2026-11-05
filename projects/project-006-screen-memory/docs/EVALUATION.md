# P009 offline evaluation (2026-11-05)

Policies and the rule below were committed in `fb03410` before the final run. Raw output is in `results/`.

## Method
`p009/simulate.py` generates 2-hour synthetic desktop sessions, one observation per second: task windows (editor, browser docs, terminal, document, notes), interruptions (chat, video) of 2–15 minutes, visits to sensitive windows the exclusion list catches (password manager, online banking), and visits to sensitive windows it **cannot** catch (a medical email, a messaging app). A window's appearance drifts while typing and jumps on scrolling.

| Measure | Meaning |
|---|---|
| frames/hour, MB/hour | Images kept, and their estimated size |
| sensitive frames | Images kept while a sensitive window was in front |
| sensitive visits exposed | Share of sensitive visits with at least one image kept |
| **resumption proxy** | Share of interruptions where a kept image shows the task window within 3 % of how it looked when the user left. **A stand-in, not task-resumption performance.** |
| window coverage | Share of non-excluded windows with at least one image |

Rule (predeclared): B4's proxy is within 0.05 of B0 and not more than 0.05 below B3, **and** B4 keeps at least 20 % fewer frames than B3 or at most half B3's sensitive frames.

## Final results (seeds 100–119)

| Policy | Frames/hour | MB/hour | Sensitive frames | Sensitive visits exposed | Resumption proxy |
|---|---|---|---|---|---|
| B0 dense (2 s) | 1800 | 162 | 199 | 0.95 | 0.99 |
| B1 sparse (30 s) | 120 | 11 | 13 | 0.91 | 0.74 |
| B2 visual change | 107 | 10 | 15 | 0.94 | 0.97 |
| B3 event-triggered | 415 | 37 | 51 | 0.95 | 1.00 |
| B4 selective | 145 | 13 | 12 | 0.46 | 1.00 |

Rule: **met on the proxy** (B4 keeps 65 % fewer frames and 78 % fewer sensitive frames than B3, with the same proxy).

## Reading it honestly
1. **B2 (visual change) keeps fewer images than B4** with a proxy only slightly lower (0.97). B4's clear advantage is privacy, and that comes mostly from the exclusion list, which any policy could use. B4 is not shown to be a better *selection* rule than B2.
2. **B4 still exposes 46 % of sensitive visits**: the ones the exclusion list cannot recognise (the medical email, the messaging app). Exclusion by name is not a privacy guarantee.
3. The proxy assumes "an image of the window as you left it" is what helps you resume. Only a study with people can test that.
4. The same agent wrote the generator and the policies; the synthetic sessions are simple (one task at a time, random drift).
5. Decision cost is tiny for all policies (B4 ≈ 56 µs per tick); real cost is dominated by capture and encoding, which was not measured on a live desktop.
