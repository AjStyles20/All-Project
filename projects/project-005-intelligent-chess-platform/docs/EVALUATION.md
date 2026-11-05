# P010 arbiter evaluation (2026-11-05)

Methods, templates and the rule were committed in `5df38dd` before the final run. Raw output: `results/`.

## 1. Benchmark
`p010/benchmark.py` renders chat lines in seven real opening and middlegame positions. Each line is judged under all four match contracts, and the expected ruling comes from a policy table (`TRUTH`), not from any method.

| Class | Example | Strict | Social | Open | Training |
|---|---|---|---|---|---|
| C0 normal | "good luck have fun" | none | none | none | none |
| C1 banter | "lucky move" | none | none | none | none |
| C2 abuse | "you are an idiot" | warning | warning | warning | warning |
| C3 threat | "i know where you live" | escalate | escalate | escalate | escalate |
| C4 own position (player) | "my knight on c3 is stuck" | none | none | none | none |
| C5 suggestion to opponent (player) | "you should play knight f6" | possible violation | none | none | none |
| C6 spectator move hint, during play | "knight f6" | high-confidence | high-confidence | none | none |
| C8 analysis after the game | "knight f6 would have won" | none | none | none | none |
| C9 unclear | names a move that is not legal now | insufficient evidence | insufficient evidence | none | none |

C7 (collusion) is not modelled.

Pools: **dev** templates (used while building), **held-out** paraphrases (not used while building B4), and held-out with a **speech-noise** pass (digits as words, "night" for knight, dropped little words). B1 and B2 are trained on dev seeds 0–9.

## 2. Metrics
Macro F1 over rulings; **false-penalty rate** (any warning or violation when the expected ruling is none or insufficient evidence); **missed-severe rate** (expected high-confidence or escalate, predicted none); appropriate and incorrect abstention; policy consistency (the same line judged correctly under all four contracts); time per ruling.

## 3. Rule (predeclared)
On the dev set, B4's macro F1 beats the best other method by 0.05, its false-penalty rate is at most 0.05, and its missed-severe rate is at most 0.05; and on the noisy held-out set B4's macro F1 drops by at most 0.15.

## 4. Results (seeds 100–119)

| Method | Dev F1 | Dev false penalties | Held-out F1 | Held-out false penalties | Held-out missed severe | Held-out policy consistency |
|---|---|---|---|---|---|---|
| B0 keywords | 0.48 | 0.57 | 0.41 | 0.60 | 0.22 | 0.46 |
| B1 text classifier | 0.75 | 0.15 | 0.40 | 0.63 | 0.04 | 0.33 |
| B2 classifier + history | 0.74 | 0.14 | 0.37 | 0.56 | 0.03 | 0.32 |
| B3 keywords + board | 0.52 | 0.31 | 0.45 | 0.33 | 0.22 | 0.54 |
| B4 contextual | 1.00 | 0.00 | 0.93 | 0.00 | **0.22** | 0.92 |

Noisy held-out matched held-out for B4 (F1 0.93). **Rule: met.**

## 5. Reading it honestly
1. **The rule checked missed-severe cases only on the dev set.** On held-out paraphrases B4 misses 22 % of severe cases: every "I'm coming for you" (threat) and every "you are such a donkey" (abuse). Its abuse and threat word lists do not cover them. That is falsification condition 3 in miniature: part of the performance comes from keywords. Not fixed after the fact.
2. "psst O-O" was missed: castling mentions are not parsed.
3. B4 never wrongly penalised anyone on any set, and context worked: the same words got different rulings by speaker, phase and contract, and speech-recognition noise made no difference.
4. The text classifiers do well on familiar phrasing and collapse on paraphrases, with high false penalties. They also cannot know the contract.
5. I wrote both the templates and B4, so dev-set scores are expected to be high. Paraphrases help but are still mine. Real chat transcripts, labelled by people who have not seen B4, are needed.
6. No human-review procedure, no real speech-to-text, no appeals: Pass 003 requires these before deployment with people.
