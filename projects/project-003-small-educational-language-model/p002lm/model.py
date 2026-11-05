"""A decoder-only Transformer in NumPy, with every backward pass written by hand.

Pre-LayerNorm blocks: x + Attention(LN(x)), then x + MLP(LN(x)); learned positions; output
weights tied to the token embedding. tests/test_model.py checks every gradient against
finite differences, so the maths here is verified, not assumed.
"""
import numpy as np

# Python floats, not NumPy float64 scalars: those would silently promote float32 arrays to float64.
GELU_C = float(np.sqrt(2.0 / np.pi))


def init(vocab, d=64, layers=2, heads=4, ctx=64, seed=0, dtype=np.float32):
    rng = np.random.default_rng(seed)
    std = 0.02
    p = {"wte": rng.normal(0, std, (vocab, d)), "wpe": rng.normal(0, std, (ctx, d)),
         "lnf_g": np.ones(d), "lnf_b": np.zeros(d)}
    for i in range(layers):
        p.update({
            f"{i}.ln1_g": np.ones(d), f"{i}.ln1_b": np.zeros(d),
            f"{i}.wqkv": rng.normal(0, std, (d, 3 * d)), f"{i}.bqkv": np.zeros(3 * d),
            # Residual projections scaled down with depth (GPT-2 style), so early training is stable.
            f"{i}.wo": rng.normal(0, std / np.sqrt(2 * layers), (d, d)), f"{i}.bo": np.zeros(d),
            f"{i}.ln2_g": np.ones(d), f"{i}.ln2_b": np.zeros(d),
            f"{i}.w1": rng.normal(0, std, (d, 4 * d)), f"{i}.b1": np.zeros(4 * d),
            f"{i}.w2": rng.normal(0, std / np.sqrt(2 * layers), (4 * d, d)), f"{i}.b2": np.zeros(d),
        })
    config = {"vocab": vocab, "d": d, "layers": layers, "heads": heads, "ctx": ctx}
    return {k: v.astype(dtype) for k, v in p.items()}, config


def count(params):
    return int(sum(v.size for v in params.values()))


# ---------- building blocks: each returns (output, cache); *_back returns input grads ----------

def ln(x, g, b, eps=1e-5):
    mu = x.mean(-1, keepdims=True)
    var = x.var(-1, keepdims=True)
    rstd = 1.0 / np.sqrt(var + eps)
    xhat = (x - mu) * rstd
    return xhat * g + b, (xhat, rstd, g)


def ln_back(dy, cache):
    xhat, rstd, g = cache
    dg = (dy * xhat).reshape(-1, xhat.shape[-1]).sum(0)
    db = dy.reshape(-1, dy.shape[-1]).sum(0)
    dxhat = dy * g
    n = xhat.shape[-1]
    dx = rstd / n * (n * dxhat - dxhat.sum(-1, keepdims=True) - xhat * (dxhat * xhat).sum(-1, keepdims=True))
    return dx, dg, db


def gelu(x):
    t = np.tanh(GELU_C * (x + 0.044715 * x * x * x))
    return 0.5 * x * (1 + t), (x, t)


def gelu_back(dy, cache):
    x, t = cache
    return dy * (0.5 * (1 + t) + 0.5 * x * (1 - t * t) * GELU_C * (1 + 3 * 0.044715 * x * x))


def attention(x, w, b, heads):
    B, T, D = x.shape
    hd = D // heads
    qkv = x @ w + b
    q, k, v = np.split(qkv, 3, axis=-1)
    q, k, v = (a.reshape(B, T, heads, hd).transpose(0, 2, 1, 3) for a in (q, k, v))
    scale = 1.0 / float(np.sqrt(hd))
    s = q @ k.transpose(0, 1, 3, 2) * scale
    s = np.where(np.tril(np.ones((T, T), dtype=bool)), s, -1e9)
    s = s - s.max(-1, keepdims=True)
    p = np.exp(s)
    p /= p.sum(-1, keepdims=True)
    o = (p @ v).transpose(0, 2, 1, 3).reshape(B, T, D)
    return o, (x, q, k, v, p, scale, heads)


def attention_back(do, cache, w):
    x, q, k, v, p, scale, heads = cache
    B, T, D = x.shape
    hd = D // heads
    do = do.reshape(B, T, heads, hd).transpose(0, 2, 1, 3)
    dv = p.transpose(0, 1, 3, 2) @ do
    dp = do @ v.transpose(0, 1, 3, 2)
    ds = p * (dp - (dp * p).sum(-1, keepdims=True))      # softmax backward; masked entries have p = 0
    dq = ds @ k * scale
    dk = ds.transpose(0, 1, 3, 2) @ q * scale
    dqkv = np.concatenate([a.transpose(0, 2, 1, 3).reshape(B, T, D) for a in (dq, dk, dv)], axis=-1)
    dw = x.reshape(-1, D).T @ dqkv.reshape(-1, 3 * D)
    db = dqkv.reshape(-1, 3 * D).sum(0)
    return dqkv @ w.T, dw, db


# ---------- the model ----------

def forward(params, config, idx, targets=None):
    """idx: (B, T) token ids. Returns (logits, loss or None, cache)."""
    B, T = idx.shape
    x = params["wte"][idx] + params["wpe"][:T]
    caches = []
    for i in range(config["layers"]):
        h, c_ln1 = ln(x, params[f"{i}.ln1_g"], params[f"{i}.ln1_b"])
        a, c_att = attention(h, params[f"{i}.wqkv"], params[f"{i}.bqkv"], config["heads"])
        o = a @ params[f"{i}.wo"] + params[f"{i}.bo"]
        x = x + o
        h2, c_ln2 = ln(x, params[f"{i}.ln2_g"], params[f"{i}.ln2_b"])
        u = h2 @ params[f"{i}.w1"] + params[f"{i}.b1"]
        g, c_gelu = gelu(u)
        m = g @ params[f"{i}.w2"] + params[f"{i}.b2"]
        x = x + m
        caches.append((c_ln1, c_att, a, c_ln2, h2, c_gelu, g))
    xf, c_lnf = ln(x, params["lnf_g"], params["lnf_b"])
    logits = xf @ params["wte"].T
    loss, probs = None, None
    if targets is not None:
        z = logits - logits.max(-1, keepdims=True)
        probs = np.exp(z)
        probs /= probs.sum(-1, keepdims=True)
        picked = np.take_along_axis(probs, targets[..., None], -1)[..., 0]
        loss = float(-np.log(picked + 1e-12).mean())
    return logits, loss, (idx, caches, c_lnf, xf, probs, targets)


def backward(params, config, cache):
    idx, caches, c_lnf, xf, probs, targets = cache
    B, T = idx.shape
    D = config["d"]
    grads = {k: np.zeros_like(v) for k, v in params.items()}
    dlogits = probs.copy()
    np.put_along_axis(dlogits, targets[..., None], np.take_along_axis(dlogits, targets[..., None], -1) - 1, -1)
    dlogits /= B * T
    grads["wte"] += dlogits.reshape(-1, dlogits.shape[-1]).T @ xf.reshape(-1, D)
    dxf = dlogits @ params["wte"]
    dx, grads["lnf_g"], grads["lnf_b"] = ln_back(dxf, c_lnf)
    for i in reversed(range(config["layers"])):
        c_ln1, c_att, a, c_ln2, h2, c_gelu, g = caches[i]
        # MLP branch
        grads[f"{i}.w2"] = g.reshape(-1, 4 * D).T @ dx.reshape(-1, D)
        grads[f"{i}.b2"] = dx.reshape(-1, D).sum(0)
        dg = dx @ params[f"{i}.w2"].T
        du = gelu_back(dg, c_gelu)
        grads[f"{i}.w1"] = h2.reshape(-1, D).T @ du.reshape(-1, 4 * D)
        grads[f"{i}.b1"] = du.reshape(-1, 4 * D).sum(0)
        dh2 = du @ params[f"{i}.w1"].T
        dln2, grads[f"{i}.ln2_g"], grads[f"{i}.ln2_b"] = ln_back(dh2, c_ln2)
        dx = dx + dln2
        # attention branch
        grads[f"{i}.wo"] = a.reshape(-1, D).T @ dx.reshape(-1, D)
        grads[f"{i}.bo"] = dx.reshape(-1, D).sum(0)
        da = dx @ params[f"{i}.wo"].T
        dh, grads[f"{i}.wqkv"], grads[f"{i}.bqkv"] = attention_back(da, c_att, params[f"{i}.wqkv"])
        dln1, grads[f"{i}.ln1_g"], grads[f"{i}.ln1_b"] = ln_back(dh, c_ln1)
        dx = dx + dln1
    np.add.at(grads["wte"], idx, dx)
    grads["wpe"][:T] += dx.sum(0)
    return grads


class AdamW:
    def __init__(self, params, lr=3e-3, betas=(0.9, 0.95), weight_decay=0.01, eps=1e-8):
        self.lr, self.b1, self.b2, self.wd, self.eps = lr, *betas, weight_decay, eps
        self.m = {k: np.zeros_like(v) for k, v in params.items()}
        self.v = {k: np.zeros_like(v) for k, v in params.items()}
        self.t = 0

    def step(self, params, grads, lr=None):
        lr = self.lr if lr is None else lr
        self.t += 1
        for k in params:
            g = grads[k]
            self.m[k] = self.b1 * self.m[k] + (1 - self.b1) * g
            self.v[k] = self.b2 * self.v[k] + (1 - self.b2) * g * g
            mhat = self.m[k] / (1 - self.b1 ** self.t)
            vhat = self.v[k] / (1 - self.b2 ** self.t)
            # Decay matrices only, not gains, biases or embeddings' rows individually.
            decay = self.wd if params[k].ndim == 2 else 0.0
            params[k] -= lr * (mhat / (np.sqrt(vhat) + self.eps) + decay * params[k])


def clip(grads, max_norm=1.0):
    norm = float(np.sqrt(sum(float((g * g).sum()) for g in grads.values())))
    if norm > max_norm:
        for g in grads.values():
            g *= max_norm / norm
    return norm


def sequence_logprob(params, config, ids):
    """Sum of log P(token_t | tokens < t) over a sequence (for comparing two sentences)."""
    ids = ids[-config["ctx"]:]
    x = np.array([ids[:-1]])
    logits, _, _ = forward(params, config, x)
    z = logits[0] - logits[0].max(-1, keepdims=True)
    logp = z - np.log(np.exp(z).sum(-1, keepdims=True))
    return float(sum(logp[t, ids[t + 1]] for t in range(len(ids) - 1)))


def generate(params, config, ids, n, temperature=0.8, seed=0):
    rng = np.random.default_rng(seed)
    ids = list(ids)
    for _ in range(n):
        x = np.array([ids[-config["ctx"]:]])
        logits, _, _ = forward(params, config, x)
        z = logits[0, -1] / max(temperature, 1e-6)
        p = np.exp(z - z.max())
        p /= p.sum()
        ids.append(int(rng.choice(len(p), p=p)))
    return ids


def save(path, params, config):
    np.savez(path, **params, **{f"__config__{k}": np.array(v) for k, v in config.items()})


def load(path):
    # allow_pickle=False: a checkpoint can only contain plain arrays, never code (Pass 001 safety).
    data = np.load(path, allow_pickle=False)
    config = {k[len("__config__"):]: int(data[k]) for k in data.files if k.startswith("__config__")}
    params = {k: data[k] for k in data.files if not k.startswith("__config__")}
    return params, config
