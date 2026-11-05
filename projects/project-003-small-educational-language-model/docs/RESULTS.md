# P002 Tier A results (2026-11-05)

Configuration fixed in commit `3c79bf6` before the final run. Raw output: `results/final.json` (each run's settings, training-text hash, loss curve, scores and a sample). Model files are not committed; `python -m p002lm.train final` recreates them in about 25 minutes on the development laptop.

## Setup
- Model: from-scratch decoder-only Transformer in NumPy, about 122,600 parameters (2 layers, 4 heads, width 64, context 32), trained for 1,200 steps of 8 × 32 tokens (307,200 tokens seen).
- Tokenizer: BPE with 320 tokens.
- Two conditions on the same 60,000-character budget. Three seeds each.
- Bigram baseline on the same tokens.
- Machine: Pentium N3710-class laptop, about 4 minutes per run.

## Results (mean of 3 seeds)

| | Validation loss | Misconception test | Subject recall |
|---|---|---|---|
| Transformer, exposition | **0.51** (perplexity 1.66) | **90.0 %** | **99.2 %** |
| Transformer, misconception-contrast | 0.60 | **37.5 %** | 97.5 % |
| Bigram, exposition | 2.34 | 86.3 % | 70.8 % |
| Bigram, misconception-contrast | 2.71 | 73.3 % | 61.7 % |

- **Misconception test:** the model gives the correct sentence a higher probability than the matching misconception, in two wordings never seen in training.
- **Subject recall:** the right subject beats a wrong one for the same fact.

## What it shows
1. **The pipeline works from first principles.**
   - The hand-written gradients match finite differences.
   - The model learns the corpus: it reaches validation perplexity 1.66, and its samples reproduce facts fluently.
   - It generalises to evaluation wordings it never saw, and it clearly beats the bigram baseline on recall (99 % against 71 %).
2. **Naive misconception-contrast pretraining backfired (Pass 002, H2).**
   - Adding "some people think X. that is wrong. Y." units made the model rate misconceptions as *more* likely than facts (37.5 % correct, against 90 % with exposition only), consistently across all three seeds.
   - For example, the contrast model prefers "a whale is a fish" to "a whale is a mammal".
   - A next-token model learns which strings occur, not which ones the text labels as wrong.
   - This is a negative result for the simplest form of H2. It does not test the stronger version from Pass 002 (diagnosis plus near-transfer problems), or any objective other than plain next-token prediction.

## Limits
- **Tiny and closed.** 40 facts, one domain, 120k parameters. It memorises a world, it does not learn science. Coherent tiny models are established prior art (TinyStories); nothing here is a novelty claim.
- **Likelihood is not understanding.** The misconception test asks which sentence is more probable, not whether the model can explain anything.
- **Contrast contamination by design.** The contrast condition saw every misconception string in training (`DATA_CARD.md`), so the result is about exposure, not transfer to new misconceptions.
- **Same author.** I wrote the corpus, templates and evaluation.
- **Tier B (GPU, larger models) was not attempted.**
