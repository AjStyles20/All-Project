# P004 (legacy folder P012) — Internet Compression and Optimization Proxy System

An optimising gateway placed in front of **its own origin**. It converts images to WebP and gzips text only when that is allowed and worthwhile for the client's network. Policy B4 also checks every result before serving it, and records why it decided what it did (header `X-Optimization`).

**Read first:** `docs/SPECIFICATION.md`. It was written and committed before any code, as Pass 004 requires. It fixes the trust boundary, the security invariants S1–S10, the network profiles, the policies and the success thresholds.

## Status (2026-11-05)
- **First version, built under DR-021.** Gateway, test origin, generated corpus, policies B0–B4, benchmark.
- **Not an open proxy and no TLS interception:** one fixed upstream; it only sees plaintext because it is that origin's front end.
- **No cache** in this version.
- **Results:** all predeclared thresholds met (B4: 3 regressions against at least 147 for the others), with important caveats (modelled network, verification cost not counted). See `docs/RESULTS.md`.

## Run
```bash
python -m venv venv
venv\Scripts\activate            # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
uvicorn p004.origin:app --port 8014                          # test origin
uvicorn p004.gateway:lab_app --factory --port 8013           # gateway (P004_POLICY=B0..B4)
curl -H "Accept-Encoding: gzip" -H "Downlink: 1.5" -D - http://127.0.0.1:8013/c/k4-data.json -o NUL
python -m p004.benchmark pilot && python -m p004.benchmark final
```

## Layout
| Path | Contents |
|---|---|
| `p004/gateway.py` | Reverse gateway with S1–S10 |
| `p004/policies.py` | Shared eligibility; B0 pass-through, B1 static, B2 aggressive, B3 network-aware, B4 VOC with cost model and verification |
| `p004/transforms.py` | WebP, gzip, PSNR, SSIM (thumbnail approximation), decode limits |
| `p004/corpus.py`, `p004/origin.py` | Generated corpus and test origin with security fixtures |
| `p004/benchmark.py` | Cost-model fit (pilot) and final comparison under modelled networks |
