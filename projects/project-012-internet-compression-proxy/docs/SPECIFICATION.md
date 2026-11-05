# P004 formal specification (first implementation)

Required by Pass 004 §14 before implementation. Implementation authorised by AJ under DR-021. Values here are fixed before the benchmark is run; changing them later needs a new version of this document.

## 1. Trust boundary
- **Origin-controlled reverse gateway** (Pass 004 §3, option 1). The gateway is configured with exactly one upstream origin and only forwards paths on it.
- **Not an open proxy:** absolute-form request targets (`GET http://other/…`), `CONNECT`, and any path that is not a plain origin path are refused.
- **No TLS interception.** The gateway sees plaintext only because it is the origin's own front end. In the laboratory both run on 127.0.0.1.
- **No cache in this version.** This removes cache poisoning and private-response caching by construction; it is recorded as a limitation, not a feature.

## 2. Security invariants (must all pass before any result counts)
| # | Invariant | Test |
|---|---|---|
| S1 | `Cache-Control: no-transform` responses are passed through byte-for-byte | yes |
| S2 | Responses that are `private`/`no-store`, or answer a request with `Authorization`, are never stored; they may be transformed in flight unless S1 applies | yes |
| S3 | Absolute-form targets, `CONNECT`, `..`, `//`, and backslashes in paths are refused | yes |
| S4 | Upstream redirects are not followed; they are returned to the client unchanged | yes |
| S5 | Upstream bodies over 20 MB are refused (502) | yes |
| S6 | Images over 40 megapixels, or that Pillow flags as decompression bombs, are passed through untransformed | yes |
| S7 | Malformed images are passed through untransformed, never a 500 | yes |
| S8 | Each transformation has a 5 s time limit; at most 4 run at once | yes |
| S9 | Logs contain no query strings, cookies or authorisation headers | yes |
| S10 | Hop-by-hop headers are stripped in both directions | yes |

## 3. Transformations (conventional codecs only, Pass 004 §10)
- **Images:** JPEG or PNG to WebP (Pillow/libwebp), only if the request's `Accept` includes `image/webp`. Optional downscale to a maximum width.
- **Text:** gzip for `text/*`, `application/json`, `application/javascript` and `image/svg+xml`, only if `Accept-Encoding` includes gzip and the origin sent no `Content-Encoding`.
- **Fidelity:** PSNR on the full image and SSIM on a 128-pixel greyscale thumbnail (an approximation, stated as such). A lossy result is a fidelity failure below **PSNR 30 dB or SSIM 0.90**.

## 4. Network profiles (modelled, not emulated)
Network emulation (netem) is not available on the Windows development machine. Completion time is therefore **modelled**: measured gateway processing time + one round trip + wire bytes ÷ bandwidth. Transformation time is measured, not modelled.

| Profile | Bandwidth | RTT |
|---|---|---|
| N0 local | 1000 Mbit/s | 1 ms |
| N1 slow 2G-like | 0.25 Mbit/s | 300 ms |
| N2 3G-like | 1.5 Mbit/s | 100 ms |
| N3 high-RTT 4G | 10 Mbit/s | 200 ms |
| N4 broadband | 50 Mbit/s | 20 ms |

The gateway reads the client's network from Client Hints (`Downlink`, `RTT`, `Save-Data`), as a browser would send them.

## 5. Corpus (generated, reproducible)
`p004/corpus.py` generates all objects from a fixed seed. Nothing is downloaded, so there are no licence questions. `results/corpus_manifest.json` records each object's class, encoding, size and SHA-256.

| Class | Contents |
|---|---|
| K1 | already-compressed JPEG (quality 75) and WebP |
| K2 | oversized photographic-style PNG and high-quality JPEG |
| K3 | flat graphics PNG (logos, charts) |
| K4 | compressible text: JSON, CSS, JavaScript, HTML |
| K5 | incompressible binary |
| K6 | small objects (< 1 KB) |
| K7 | restricted: `no-transform`, `private`, `no-store` |
| K8 | hostile: oversized dimensions, malformed image |

## 6. Policies
| Policy | Rule |
|---|---|
| B0 | Pass-through |
| B1 static | Images to WebP quality 80; text gzip level 6 |
| B2 aggressive | Images to WebP quality 50 and downscale to 1280 px wide; text gzip level 9 |
| B3 network-aware | `Downlink` < 2 Mbit/s or `Save-Data`: WebP quality 60, else 80; gzip text over 1 KB |
| B4 VOC | (1) eligibility as in §2–§3, else ABSTAIN; (2) predict net benefit with a fixed cost model (encode ms per megapixel, gzip ms per MB, expected size ratios per class, all fitted on pilot objects only), and transform only if predicted completion time improves under the client's hints; (3) **verify**: if the result is larger than the original, or fails the fidelity floor, serve the original instead; (4) record the decision and its inputs |

All policies run behind the same gateway, so S1–S10 apply equally. B4 gets no information the other adaptive policy (B3) does not have, apart from its cost model and verification step.

## 7. Decision outcomes and metrics (per object, profile and policy)
- **PASS_THROUGH** (no transform attempted), **ABSTAIN** (ineligible under §2–§3), **TRANSFORM_SUCCESS** (served transformed, fewer bytes, completion time not worse than B0, fidelity floor met), **TRANSFORM_REGRESSION** (served transformed, and more bytes, or slower than B0 by more than 1 %, or below the fidelity floor).
- Reported: wire bytes, modelled completion time, measured transform time, PSNR/SSIM, outcome counts, security-invariant failures.

## 8. Repetitions and split
- Pilot: corpus seed 0, used only to fit B4's cost model.
- Final: corpus seeds 1–5, one run each; transform times are measured once per object and reused across profiles.

## 9. Success thresholds (fixed now)
| Question | Threshold |
|---|---|
| Q1 fewer regressions | B4 regressions ≤ 50 % of the fewest among B1–B3 |
| Q2 savings kept on slow links | On N1 and N2, B4's bytes saved ≥ 80 % of B3's |
| Q3 correct abstention | 100 % of K7/K8 objects ABSTAIN or pass through untouched, and every §2 invariant test passes |
| Q4 reproducible | Re-running B4's decision function on recorded inputs gives identical decisions |
| Kill check | If B4 and B3 make the same transform/no-transform decision on ≥ 90 % of eligible object-profile pairs, report "B4 behaves like B3" |

## 10. Not in scope
Real network emulation, caching, HTTP/2 and HTTP/3 specifics, AVIF, video, learned compression, forward-proxy use, and any third-party traffic.
