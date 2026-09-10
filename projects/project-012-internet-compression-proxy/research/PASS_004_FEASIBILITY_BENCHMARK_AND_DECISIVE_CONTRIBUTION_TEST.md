# P004 — Pass 004: Feasibility Benchmark Design and Decisive Contribution Test

**Canonical project:** P004 — Internet Compression and Optimization Proxy System  
**Legacy directory:** project-012-internet-compression-proxy  
**Research stage:** Pass 004  
**Decision:** CONDITIONAL GO TO FORMAL SPECIFICATION  
**Implementation:** NOT AUTHORIZED BY THIS PASS

## 1. Purpose
This pass asks whether the narrowed P004 hypothesis can be tested as a defensible systems experiment rather than merely implemented as another compression proxy.

The surviving hypothesis is **Verifiable Net-Benefit Optimization Evaluation (VOC/B4)**: for each eligible object and network condition, a bounded optimizer should decide whether to pass through or transform, then verify the actual outcome against pass-through without hiding regressions behind compression ratio.

## 2. Prior-art pressure retained
Historical proxy benchmarking already established that proxy performance must be evaluated with multiple metrics rather than a single headline number, and that caching/proxy overhead can erase latency gains under some low-bandwidth conditions. Adaptive transcoding literature already predicts transformation delay, output size and bandwidth. Recent adaptive image-transmission research continues to optimize explicit latency/quality/throughput trade-offs under changing network conditions. Therefore P004 must not claim novelty for adaptive compression, multi-metric optimization, or network-aware codec selection alone.

## 3. Bounded deployment/trust model
The first experimental system MUST be one of:
1. an origin-controlled reverse proxy/gateway in front of a controlled test origin; or
2. an explicitly trusted local laboratory gateway operating only on controlled test content.

The first experiment MUST NOT require arbitrary public forward-proxy operation or silent TLS interception/MITM. HTTPS content transformation is allowed only where the test architecture legitimately terminates TLS or otherwise owns the plaintext trust boundary.

## 4. Experimental corpus
Use a reproducible corpus with separately reported classes rather than one aggregate score:
- already-compressed JPEG/WebP/AVIF images;
- oversized PNG/JPEG images with realistic photographic and graphical content;
- compressible text/JSON/CSS/JS where protocol semantics permit;
- incompressible/binary controls;
- small objects for which transformation overhead is likely to dominate;
- objects carrying transformation/cache restrictions such as `no-transform`, `private`, or `no-store`;
- authenticated/private-response fixtures;
- deliberately hostile fixtures for resource-limit/security tests.

The corpus must record source, license/provenance, original encoding, original byte size and a stable content hash.

## 5. Network profiles
Use controlled network emulation, not subjective browsing impressions. Initial profiles should span at least:
- unconstrained/local baseline;
- low bandwidth + low RTT;
- low bandwidth + moderate/high RTT;
- moderate bandwidth + high RTT;
- moderate packet loss/jitter where the emulator permits reliable control.

Exact rates/RTTs/loss values belong in formal specification and must be selected before benchmark execution. Every baseline and candidate policy must run under identical profiles.

## 6. Baselines
**B0 — Pass-through:** no content transformation.  
**B1 — Static modern-format optimization:** deterministic transformation where eligible, without network-aware policy.  
**B2 — Fixed aggressive data-saving profile:** prioritizes bytes saved subject to hard safety/semantic restrictions.  
**B3 — Simple network-aware adaptive policy:** chooses a predefined quality/codec rule from network condition and object type.  
**B4 — VOC-governed policy:** first checks trust/protocol/security/fidelity eligibility; predicts whether a candidate transformation is worthwhile; performs it only when eligible; records the outcome; and classifies the transformation as a success/regression after comparison with B0 under the same condition.

B4 must not receive privileged information unavailable to the other adaptive baseline except the explicit VOC governance/evaluation mechanism being tested.

## 7. Metrics
Do not collapse the experiment into one arbitrary weighted score.

Report at minimum:
- wire bytes delivered to client;
- object completion time;
- transformation/encoding CPU wall time;
- proxy-added latency;
- cache hit/miss state where caching is enabled;
- output byte size and ratio;
- client-visible errors;
- fidelity for lossy image transformations (at least PSNR and SSIM where technically valid, plus clearly defined perceptual/visual acceptance criteria if used);
- memory/resource-limit failures;
- policy/security violations;
- decision outcome: PASS_THROUGH, TRANSFORM_SUCCESS, TRANSFORM_REGRESSION, or ABSTAIN.

A transformation that saves bytes but increases completion time is not automatically a success. The result is objective-specific and both outcomes must remain visible.

## 8. Primary falsifiable questions
Q1. Does B4 reduce avoidable transformation regressions compared with B1-B3?  
Q2. Under constrained networks, can B4 retain most useful byte savings while avoiding transformations whose processing cost exceeds network benefit?  
Q3. Does B4 correctly abstain on protocol/security-ineligible content?  
Q4. Are B4 decisions reproducible from recorded inputs and policy state?  
Q5. Does B4 provide useful benefit on low-spec CPU hardware, or does policy/measurement overhead erase the gain?

## 9. Success/kill criteria
The formal specification must set numerical thresholds before implementation. This pass establishes qualitative kill conditions:

**KILL/REFRAME the research contribution if:**
- B4 behaves materially the same as a simple B3 threshold policy across the representative corpus;
- the added governance/measurement overhead materially worsens end-to-end performance without reducing regressions or unsafe transformations;
- most modern content is ineligible or already efficiently encoded, leaving too little transformable workload for meaningful evaluation;
- results depend on arbitrary objective weights rather than observable metric trade-offs;
- the test requires unsafe TLS interception or an open-proxy design to demonstrate value;
- low-spec hardware cannot execute the bounded transforms in useful time and there is no defensible server-side deployment alternative;
- apparent improvement comes from comparing B4 against deliberately weak/obsolete codecs rather than strong contemporary baselines.

**GO remains justified only if** B4 measurably reduces harmful/unjustified transformations while preserving useful savings under at least some clearly identified constrained-network regimes.

## 10. Hardware feasibility
The first prototype should deliberately avoid learned/neural compression. Contemporary learned compression research may require high-end GPU hardware and is a separate contribution space. P004 should use conventional codecs and lightweight policy logic so the benchmark can run on ordinary CPU hardware. If AVIF or other expensive encoders are included, encode time must be measured and the benchmark may use controlled server hardware in addition to AJ's low-spec development laptop; the hardware configuration must be reported, not hidden.

## 11. Security acceptance gate
Before any performance result can count, the implementation must pass bounded security tests including:
- honor `no-transform`;
- prevent unsafe caching of private/`no-store`/authenticated fixtures;
- cache-key/user isolation where relevant;
- deny open-proxy behavior;
- SSRF controls including redirects and private/link-local targets;
- decoded-image/dimension/resource limits;
- decompression-bomb/resource-exhaustion controls;
- transformation timeouts/concurrency limits;
- malformed media/parser failure handling;
- cache-poisoning resistance in the controlled design;
- sensitive header/query/log redaction;
- correct TLS certificate handling at the legitimate trust boundary.

A benchmark run with a failed security invariant cannot support a release-readiness claim.

## 12. Reproducibility
Each run should preserve:
- software version/commit;
- policy version;
- corpus manifest and hashes;
- codec/library versions;
- hardware/OS;
- network-emulation profile;
- warm/cold cache state;
- repetitions and raw measurements;
- failures/exclusions with reasons.

Do not discard failed transformations merely because they make B4 look worse.

## 13. Research contribution boundary
P004 should NOT claim:
- invention of compression proxies;
- invention of adaptive transcoding;
- invention of network-aware compression;
- invention of multi-objective optimization;
- invention of modern image formats;
- invention of proxy benchmarking.

The bounded research claim to test is instead:

> Within an explicitly trusted and protocol-compliant optimization gateway, a verifiable net-benefit policy can make transformation decisions auditable and can reduce objectively harmful or unjustified transformations relative to simpler static/aggressive/network-aware policies, while exposing when data saving trades off against latency, fidelity, compute cost, or security constraints.

This remains a hypothesis until benchmark evidence supports it.

## 14. Pass decision
**CONDITIONAL GO TO FORMAL SPECIFICATION.**

P004 is feasible as a bounded systems experiment. The remaining contribution is not a new compression technique; it is a measurable, policy-governed decision/evaluation layer over conventional transformations. Its value is falsifiable through B0-B4 comparison.

No implementation should begin until a formal specification fixes the trust boundary, corpus, network profiles, exact baseline algorithms, metric definitions, statistical/repetition plan, numerical success thresholds, security tests, and experiment provenance schema.

After formal specification, park P004 for portfolio comparison unless AJ explicitly selects it for implementation.