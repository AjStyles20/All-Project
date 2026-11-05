"""Byte-pair encoding tokenizer, trained from scratch.

Starts from single characters and repeatedly merges the most frequent adjacent pair.
Merges never cross a space boundary, so tokens are whole words or word pieces.
Saved as JSON (no pickle).
"""
import json
from collections import Counter


class BPE:
    def __init__(self, vocab=None, merges=None):
        self.vocab = vocab or []           # id -> token string
        self.merges = merges or []         # ordered list of (a, b)
        self.index = {t: i for i, t in enumerate(self.vocab)}
        self.ranks = {tuple(p): r for r, p in enumerate(self.merges)}

    @classmethod
    def train(cls, text: str, vocab_size: int):
        chars = sorted(set(text))
        vocab = ["<unk>"] + chars
        words = Counter(_words(text))
        splits = {w: list(w) for w in words}
        merges = []
        while len(vocab) < vocab_size:
            pairs = Counter()
            for w, n in words.items():
                s = splits[w]
                for a, b in zip(s, s[1:]):
                    pairs[(a, b)] += n
            if not pairs:
                break
            (a, b), _ = max(pairs.items(), key=lambda kv: (kv[1], kv[0]))
            merges.append((a, b))
            vocab.append(a + b)
            for w in splits:
                splits[w] = _merge(splits[w], a, b)
        return cls(vocab, merges)

    def encode(self, text: str) -> list[int]:
        out = []
        for w in _words(text):
            parts = list(w)
            while len(parts) > 1:
                ranked = [(self.ranks.get((a, b), 1 << 30), i) for i, (a, b) in enumerate(zip(parts, parts[1:]))]
                rank, i = min(ranked)
                if rank == 1 << 30:
                    break
                parts = parts[:i] + [parts[i] + parts[i + 1]] + parts[i + 2:]
            out += [self.index.get(p, 0) for p in parts]
        return out

    def decode(self, ids) -> str:
        return "".join(self.vocab[i] if 0 < i < len(self.vocab) else "?" for i in ids)

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"vocab": self.vocab, "merges": self.merges}, f)

    @classmethod
    def load(cls, path):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return cls(data["vocab"], [tuple(m) for m in data["merges"]])


def _words(text):
    """Split into words that keep their leading space, so decoding is exact."""
    out, cur = [], ""
    for ch in text:
        if ch in " \n" and cur:
            out.append(cur)
            cur = ""
        cur += ch
    if cur:
        out.append(cur)
    return out


def _merge(parts, a, b):
    out, i = [], 0
    while i < len(parts):
        if i < len(parts) - 1 and parts[i] == a and parts[i + 1] == b:
            out.append(a + b)
            i += 2
        else:
            out.append(parts[i])
            i += 1
    return out
