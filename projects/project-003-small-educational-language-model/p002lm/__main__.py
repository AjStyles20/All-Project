"""Small command-line lab for inspecting the trained model.

    python -m p002lm tokens "the moon reflects light"
    python -m p002lm sample "we know that the heart" [--condition contrast]
    python -m p002lm compare "the moon reflects light from the sun." "the moon makes its own light."
    python -m p002lm attention "the heart pumps blood"
"""
import argparse
import sys
from pathlib import Path

import numpy as np

from p002lm import model as M
from p002lm.tokenizer import BPE

RESULTS = Path(__file__).resolve().parent.parent / "results"


def load(condition):
    tok = BPE.load(RESULTS / "tokenizer.json")
    path = RESULTS / f"model_{condition}.npz"
    if not path.exists():
        sys.exit(f"No trained model at {path}. Run: python -m p002lm.train final")
    params, config = M.load(path)
    return tok, params, config


def main(argv=None):
    parser = argparse.ArgumentParser(prog="p002lm")
    parser.add_argument("command", choices=["tokens", "sample", "compare", "attention"])
    parser.add_argument("text", nargs="+")
    parser.add_argument("--condition", default="exposition", choices=["exposition", "contrast"])
    parser.add_argument("--tokens", type=int, default=30)
    args = parser.parse_args(argv)
    text = " ".join(args.text).lower()

    if args.command == "tokens":
        tok = BPE.load(RESULTS / "tokenizer.json")
        ids = tok.encode(text)
        print(f"{len(ids)} tokens for {len(text)} characters:")
        print(" | ".join(repr(tok.vocab[i]) for i in ids))
        return 0

    tok, params, config = load(args.condition)
    if args.command == "sample":
        print(tok.decode(M.generate(params, config, tok.encode(text), args.tokens)))
    elif args.command == "compare":
        for sentence in args.text:
            print(f"{M.sequence_logprob(params, config, tok.encode(sentence.lower())):8.2f}  {sentence}")
        print("(higher = the model finds the sentence more likely)")
    else:
        ids = tok.encode(text)[-config["ctx"]:]
        _, _, cache = M.forward(params, config, np.array([ids]))
        p = cache[1][-1][1][4][0]          # last layer, attention probabilities, batch 0: (heads, T, T)
        names = [tok.vocab[i] for i in ids]
        print(f"Last layer, averaged over heads: what each token attends to most")
        avg = p.mean(0)
        for t, name in enumerate(names):
            best = int(avg[t].argmax())
            print(f"  {name!r:>14} -> {names[best]!r} ({avg[t, best]:.2f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
