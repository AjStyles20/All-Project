# P002 (folder legacy P003) — Educational Language Model From First Principles

A tiny language model built end to end by hand: a hand-written corpus, a byte-pair tokenizer, a decoder-only Transformer in NumPy whose backward pass is written out and checked against finite differences, AdamW training, and evaluation on wordings never seen in training. Built under DR-021; the portfolio status ("build regardless of novelty, outside FYP competition") is unchanged.

Research context: `research/PASS_001_…` and `research/PASS_002_…`. This is **Tier A** (local proof system) from Pass 001.

## Status (2026-11-05)
- Pipeline verified: gradients match finite differences; 9 tests.
- The model learns its 40-fact corpus (validation perplexity 1.66) and beats a bigram baseline on recall.
- **Finding:** naive misconception-contrast pretraining made the model *prefer* misconceptions (37.5 % vs 90 %). See `docs/RESULTS.md`.

## Run
```bash
python -m venv venv
venv\Scripts\activate            # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
python -m p002lm.train pilot     # about 1-2 minutes
python -m p002lm.train final     # 6 runs, about 25 minutes on a low-end laptop
python -m p002lm sample "a teacher would say the heart"
python -m p002lm compare "did you know a whale is a mammal?" "did you know a whale is a fish?" --condition contrast
python -m p002lm tokens "the moon reflects light"
python -m p002lm attention "we know that ice floats on water"
```

## Layout
| Path | Contents |
|---|---|
| `p002lm/model.py` | Transformer forward and hand-written backward, AdamW, sampling, safe checkpoints |
| `p002lm/tokenizer.py` | Byte-pair encoding |
| `p002lm/corpus.py` | Hand-written facts and misconceptions, training and held-out templates |
| `p002lm/train.py` | Training runs, bigram baseline, evaluation |
| `p002lm/__main__.py` | Inspection lab: tokens, sampling, sentence comparison, attention |
| `docs/` | Data card, technology selection, results |
