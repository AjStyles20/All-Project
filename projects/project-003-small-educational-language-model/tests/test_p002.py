import numpy as np
import pytest

from p002lm import corpus, model as M
from p002lm.tokenizer import BPE


# ---------- model maths ----------

def tiny(seed=1):
    params, cfg = M.init(vocab=11, d=8, layers=2, heads=2, ctx=6, seed=seed, dtype=np.float64)
    rng = np.random.default_rng(0)
    for k in params:      # move gains and biases off 1/0 so their gradients are exercised
        params[k] = params[k] + rng.normal(0, 0.1, params[k].shape)
    return params, cfg


def test_every_gradient_matches_finite_differences():
    params, cfg = tiny()
    rng = np.random.default_rng(3)
    idx, tgt = rng.integers(0, 11, (2, 5)), rng.integers(0, 11, (2, 5))
    grads = M.backward(params, cfg, M.forward(params, cfg, idx, tgt)[2])
    for name, p in params.items():
        for _ in range(4):
            i = tuple(rng.integers(0, s) for s in p.shape)
            old, h = p[i], 1e-6
            p[i] = old + h
            up = M.forward(params, cfg, idx, tgt)[1]
            p[i] = old - h
            down = M.forward(params, cfg, idx, tgt)[1]
            p[i] = old
            numeric = (up - down) / (2 * h)
            rel = abs(numeric - grads[name][i]) / max(1e-8, abs(numeric) + abs(grads[name][i]))
            assert rel < 1e-4, (name, i, numeric, grads[name][i])


def test_attention_is_causal():
    params, cfg = tiny()
    a = np.array([[1, 2, 3, 4, 5]])
    b = np.array([[1, 2, 3, 9, 9]])
    la = M.forward(params, cfg, a)[0]
    lb = M.forward(params, cfg, b)[0]
    assert np.allclose(la[0, :3], lb[0, :3])      # later tokens cannot change earlier predictions
    assert not np.allclose(la[0, 3:], lb[0, 3:])


def test_training_lowers_loss_on_a_pattern():
    params, cfg = M.init(vocab=5, d=16, layers=1, heads=2, ctx=8, seed=0)
    opt = M.AdamW(params, lr=1e-2)
    x = np.array([[0, 1, 2, 3, 4, 0, 1, 2]] * 4)
    y = np.array([[1, 2, 3, 4, 0, 1, 2, 3]] * 4)
    first = M.forward(params, cfg, x, y)[1]
    for _ in range(60):
        _, loss, cache = M.forward(params, cfg, x, y)
        opt.step(params, M.backward(params, cfg, cache))
    assert loss < first * 0.3


def test_float32_stays_float32():
    params, cfg = M.init(vocab=11, d=8, layers=1, heads=2, ctx=6)
    logits = M.forward(params, cfg, np.array([[1, 2, 3]]))[0]
    assert logits.dtype == np.float32


def test_checkpoints_hold_only_arrays(tmp_path):
    params, cfg = M.init(vocab=11, d=8, layers=1, heads=2, ctx=6)
    M.save(tmp_path / "m.npz", params, cfg)
    loaded, cfg2 = M.load(tmp_path / "m.npz")
    assert cfg2 == cfg and all(np.array_equal(loaded[k], params[k]) for k in params)
    np.savez(tmp_path / "evil.npz", x=np.array([object()], dtype=object))
    with pytest.raises(ValueError):
        M.load(tmp_path / "evil.npz")


# ---------- tokenizer ----------

def test_bpe_round_trip_and_compression():
    text = corpus.training_text("exposition", 0, 5000)
    tok = BPE.train(text, 150)
    ids = tok.encode(text)
    assert tok.decode(ids) == text
    assert len(ids) < len(text) / 2               # merges actually shorten the sequence


def test_bpe_save_load(tmp_path):
    tok = BPE.train("the cat sat on the mat. the cat ran.", 30)
    tok.save(tmp_path / "t.json")
    again = BPE.load(tmp_path / "t.json")
    assert again.encode("the cat ran.") == tok.encode("the cat ran.")


# ---------- corpus governance ----------

def test_evaluation_templates_never_appear_in_training():
    text = corpus.training_text("contrast", 1, 60_000)
    for good, bad in corpus.eval_items():
        assert good not in text and bad not in text
    assert "did you know" not in text and "a teacher would say" not in text


def test_conditions_have_equal_budgets_and_differ_only_in_contrast_units():
    a = corpus.training_text("exposition", 1, 20_000)
    b = corpus.training_text("contrast", 1, 20_000)
    assert len(a) == len(b) == 20_000
    assert "that is wrong" not in a and "that is wrong" in b
