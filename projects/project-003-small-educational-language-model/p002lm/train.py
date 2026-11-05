"""Training and evaluation (Tier A: local proof system, Pass 001).

    python -m p002lm.train pilot      # one short run to check everything works
    python -m p002lm.train final      # both conditions x 3 seeds, plus a bigram baseline

Every run records its config, data hashes, losses and evaluation in results/.
"""
import hashlib
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

from p002lm import corpus, model as M
from p002lm.tokenizer import BPE

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
VOCAB = 320
TRAIN_CHARS = 60_000
MODEL = {"d": 64, "layers": 2, "heads": 4, "ctx": 32}
BATCH = 8


def tokenizer():
    # One tokenizer for every condition, trained on text both conditions share, so the
    # tokenizer is not the variable being tested.
    return BPE.train(corpus.training_text("exposition", 12345, 40_000), VOCAB)


def batches(ids, rng, ctx, batch):
    starts = rng.integers(0, len(ids) - ctx - 1, batch)
    x = np.stack([ids[s:s + ctx] for s in starts])
    y = np.stack([ids[s + 1:s + ctx + 1] for s in starts])
    return x, y


def val_loss(params, config, ids, ctx):
    losses = []
    for s in range(0, len(ids) - ctx - 1, ctx):
        x = np.array([ids[s:s + ctx]])
        y = np.array([ids[s + 1:s + ctx + 1]])
        losses.append(M.forward(params, config, x, y)[1])
    return float(np.mean(losses))


def pair_accuracy(score, tok, items):
    """Share of pairs where the correct sentence gets the higher log-probability."""
    return sum(score(tok.encode(good)) > score(tok.encode(bad)) for good, bad in items) / len(items)


def run(condition, seed, steps, tok, log_every=100):
    text = corpus.training_text(condition, seed, TRAIN_CHARS)
    ids = np.array(tok.encode(text))
    val_ids = np.array(tok.encode(corpus.validation_text()))
    params, config = M.init(len(tok.vocab), seed=seed, **MODEL)
    opt = M.AdamW(params)
    rng = np.random.default_rng(seed)
    curve, started = [], time.perf_counter()
    for step in range(1, steps + 1):
        lr = 3e-3 * min(1.0, step / 100) * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * step / steps)))
        x, y = batches(ids, rng, config["ctx"], BATCH)
        _, loss, cache = M.forward(params, config, x, y)
        grads = M.backward(params, config, cache)
        M.clip(grads, 1.0)
        opt.step(params, grads, lr)
        if step % log_every == 0 or step == steps:
            curve.append({"step": step, "train_loss": round(loss, 4)})
    seconds = time.perf_counter() - started
    score = lambda t: M.sequence_logprob(params, config, t)
    result = {
        "condition": condition, "seed": seed, "steps": steps, "params": M.count(params), "config": config,
        "train_tokens_seen": steps * BATCH * config["ctx"], "train_text_sha256": hashlib.sha256(text.encode()).hexdigest()[:16],
        "seconds": round(seconds, 1), "curve": curve,
        "val_loss": round(val_loss(params, config, val_ids, config["ctx"]), 4),
        "misconception_accuracy": round(pair_accuracy(score, tok, corpus.eval_items()), 3),
        "subject_recall_accuracy": round(pair_accuracy(score, tok, corpus.recall_items()), 3),
    }
    result["val_perplexity"] = round(math.exp(result["val_loss"]), 2)
    sample = M.generate(params, config, tok.encode("we know that the moon"), 20, seed=seed)
    result["sample"] = tok.decode(sample)
    return result, params, config


def bigram(condition, seed, tok):
    """Non-neural baseline (Pass 001 Q7): add-one smoothed bigram on the same tokens."""
    ids = tok.encode(corpus.training_text(condition, seed, TRAIN_CHARS))
    pairs, singles = Counter(zip(ids, ids[1:])), Counter(ids)
    v = len(tok.vocab)

    def score(t):
        return sum(math.log((pairs[(a, b)] + 1) / (singles[a] + v)) for a, b in zip(t, t[1:]))
    val = tok.encode(corpus.validation_text())
    nll = -score(val) / (len(val) - 1)
    return {"condition": condition, "seed": seed, "val_loss": round(nll, 4), "val_perplexity": round(math.exp(nll), 2),
            "misconception_accuracy": round(pair_accuracy(score, tok, corpus.eval_items()), 3),
            "subject_recall_accuracy": round(pair_accuracy(score, tok, corpus.recall_items()), 3)}


def main(argv):
    mode = argv[1] if len(argv) > 1 else "pilot"
    RESULTS.mkdir(exist_ok=True)
    tok = tokenizer()
    tok.save(RESULTS / "tokenizer.json")
    if mode == "pilot":
        result, params, config = run("exposition", 0, 200, tok, log_every=50)
        print(json.dumps(result, indent=1))
        (RESULTS / "pilot.json").write_text(json.dumps(result, indent=1), encoding="utf-8")
        return
    runs, baselines = [], []
    for condition in ("exposition", "contrast"):
        for seed in (1, 2, 3):
            result, params, config = run(condition, seed, 1200, tok)
            runs.append(result)
            baselines.append(bigram(condition, seed, tok))
            print(condition, seed, {k: result[k] for k in ("val_loss", "misconception_accuracy", "subject_recall_accuracy", "seconds")}, flush=True)
            if seed == 1:
                M.save(RESULTS / f"model_{condition}.npz", params, config)
    summary = {}
    for kind, rows in (("transformer", runs), ("bigram", baselines)):
        for condition in ("exposition", "contrast"):
            mine = [r for r in rows if r["condition"] == condition]
            summary[f"{kind}/{condition}"] = {k: round(float(np.mean([r[k] for r in mine])), 3)
                                             for k in ("val_loss", "misconception_accuracy", "subject_recall_accuracy")}
    out = {"runs": runs, "bigram": baselines, "summary": summary, "tokenizer_vocab": len(tok.vocab)}
    (RESULTS / "final.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main(sys.argv)
