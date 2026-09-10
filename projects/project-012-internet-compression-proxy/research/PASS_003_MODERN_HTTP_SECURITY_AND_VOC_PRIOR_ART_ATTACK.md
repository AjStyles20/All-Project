# P004 — Pass 003: Modern HTTP Semantics, Security Constraints and Direct Prior-Art Attack on VOC

**Canonical project ID:** P004  
**Legacy directory ID:** P012  
**Project:** Internet Compression and Optimization Proxy System  
**Research state:** MORE RESEARCH — VOC survives only as an evaluation/governance mechanism, not yet as a novelty claim

## Research question
Can the proposed Verifiable Optimization Contract (VOC)—permission + expected benefit + measured outcome + safe abstention—survive modern HTTP semantics, current CDN/image optimization practice, and proxy/cache security constraints?

## Evidence reviewed

### HTTP transformation semantics
RFC 9111 defines `Cache-Control: no-transform` for requests and responses. A response carrying `no-transform` means an intermediary MUST NOT transform the content. `no-store` also prohibits a cache from storing the request/response for reuse. Therefore a conforming optimizer needs an explicit semantic-eligibility gate before any byte-saving decision.

Historical HTTP intermediary semantics also explicitly recognize payload transformation and require transformed responses to be represented honestly. This reinforces that transformation is governed by protocol semantics rather than being an unrestricted optimization action.

### Current CDN/image optimization practice
Current Cloudflare Images can resize, compress, transcode and cache images, automatically choose formats, adapt image dimensions, and use slow-connection quality settings driven by client/network hints. Transformation flows provide condition/action rules. Workers provide programmatic control and can negotiate size, format and quality according to device/network conditions.

Google Cloud CDN also provides edge image optimization with explicit transformations, output caching, resizing, cropping and format conversion.

These systems directly attack any claim that P004 is novel because it conditionally transforms media, automatically selects formats, uses network/device conditions, caches transformed variants, or records/controls transformation parameters.

### Outcome/cost awareness
Current infrastructure documentation explicitly recognizes transformation compute cost and latency. For example, AVIF encoding can be substantially slower than other formats, and uncached image decode/re-encode adds avoidable latency. This supports the engineering need for cost-aware decisions, but it also means “consider processing cost before optimizing” cannot safely be presented as novel.

### Security constraints
A transformation/caching intermediary increases attack surface. Relevant threats include cache poisoning, cross-user leakage caused by incorrect cache keys or private-response handling, malicious or oversized media inputs, decompression/resource-exhaustion attacks, SSRF when fetching remote transformation sources, open-proxy abuse, request-routing/parser inconsistencies, unsafe logging, and certificate/TLS mistakes.

Current CDN systems constrain source origins and provide access-control mechanisms around remote image fetching, demonstrating that source-fetch authorization is already a practical security requirement.

## Direct attack on VOC components

| VOC component | Prior-art pressure | Pass 003 status |
|---|---|---|
| Respect transformation permission | HTTP `no-transform` already standardizes a hard constraint | NOT NOVEL |
| Respect storage/cache permission | HTTP cache directives already govern this | NOT NOVEL |
| Condition transformations on content/device/network | Mature research + current CDN products | NOT NOVEL |
| Choose modern output format automatically | Current image/CDN services | NOT NOVEL |
| Cache transformed variants | Standard CDN/image-optimization practice | NOT NOVEL |
| Consider processing latency/cost | Historical adaptive-transcoding research and modern service guidance | NOT NOVEL |
| Measure bytes saved | Basic optimization telemetry | NOT NOVEL |
| Abstain when transformation is forbidden | Required protocol behavior in some cases | NOT NOVEL |
| Security-gate remote fetching/caching | Established secure intermediary practice | NOT NOVEL |
| Combine protocol permission, predicted utility, measured outcome and explicit failure accounting into a reproducible evaluation contract | No decisive evidence yet that this exact research/evaluation formulation is a distinct contribution | UNKNOWN / SURVIVES ONLY FOR FURTHER TEST |

## What Pass 003 kills
P004 must not claim novelty for:
1. protocol-aware content transformation;
2. honoring `no-transform`;
3. adaptive image quality;
4. network-aware media optimization;
5. automatic AVIF/WebP/format negotiation;
6. CDN-style transformed-object caching;
7. conditional transformation rules;
8. measuring byte savings;
9. avoiding transformations that cost too much latency;
10. security restrictions around remote image origins.

## VOC reframe
VOC should no longer be treated as a candidate new optimization algorithm. Its defensible role is an **evaluation and governance contract** for a bounded low-bandwidth optimizer.

For each candidate transformation T on response R under user/network context C:

1. **Trust eligibility** — does the system legitimately have plaintext/content authority?
2. **Protocol eligibility** — do HTTP semantics permit transformation and any proposed caching?
3. **Security eligibility** — can the object be processed/fetched/cached within defined limits without violating isolation or origin policy?
4. **Fidelity eligibility** — does the requested profile permit the expected quality change?
5. **Predicted utility** — is the expected saving large enough relative to transform cost and latency?
6. **Measured result** — what actually happened to bytes, latency, processing time and quality?
7. **Decision audit** — was the prediction correct, and would pass-through have been better?

### Core invariant
**An optimization counts as successful only if it was permissible and its measured net outcome beats the defined pass-through baseline under the chosen user objective.**

This is deliberately stronger than “bytes became smaller,” but it is not yet claimed as novel.

## Candidate measurable objective
For controlled experiments, define a profile-specific utility rather than one universal score. Candidate dimensions:
- transferred bytes;
- time-to-first-byte / completion time where applicable;
- transformation CPU time;
- cache hit/miss behavior;
- fidelity metric for lossy media plus bounded human inspection where appropriate;
- protocol violations = hard failure;
- security-policy violations = hard failure.

A weighted scalar score may be useful experimentally, but weights must not be invented as universal truth. Report the component metrics separately.

## Architecture consequence
The first defensible prototype should **not** be an arbitrary Internet forward proxy or TLS MITM.

Preferred experimental boundary:
- an origin-controlled or explicitly trusted test gateway;
- HTTP semantics visible legitimately;
- bounded content types, initially images and already-compressible text where appropriate;
- no transformation of `no-transform` responses;
- no shared caching of private/authenticated responses unless a deliberately proven cache policy allows it;
- remote-fetch allowlists / SSRF controls;
- strict input-size, decoded-size, dimension, processing-time and concurrency limits;
- transformation provenance and benchmark logs;
- pass-through as the safe default.

This allows the research hypothesis to be tested without pretending that arbitrary HTTPS payloads can be safely optimized.

## Security test requirements for eventual specification
Before any release claim, tests must include at minimum:
- `no-transform` enforcement;
- `no-store`/private-cache handling;
- cache-key isolation and cross-user leakage tests;
- malicious/invalid image handling;
- compressed/decompressed size limits;
- SSRF attempts against loopback/private/link-local/cloud-metadata targets;
- redirect-based SSRF bypass attempts;
- oversized dimensions / image-bomb resource exhaustion;
- transformation timeout/concurrency limits;
- cache poisoning attempts;
- header/parser edge cases;
- sensitive-header/log redaction;
- fail-closed behavior when policy cannot be evaluated.

## Remaining research hypothesis
### H5 — Verifiable Net-Benefit Optimization Evaluation
A bounded optimizer may be useful as a research system if it can show, per object and per network/profile condition, whether an allowed transformation actually improved the chosen objective relative to pass-through, while exposing regressions and abstentions rather than hiding them behind aggregate compression ratios.

**Novelty:** UNKNOWN.  
**Engineering value:** plausible.  
**Research value:** requires empirical falsification against standard/static optimization policies.

## Required baselines
- **B0:** pass-through / origin representation.
- **B1:** static modern-format policy (for example fixed WebP/AVIF policy where supported).
- **B2:** fixed low-quality/data-saving profile.
- **B3:** simple network-aware adaptive rule.
- **B4:** VOC-governed net-benefit policy.

If B4 does not materially reduce regressions or improve the defined objective over simpler B1–B3 policies, the remaining contribution should be rejected or reframed as an educational systems implementation.

## Kill criteria
P004 should be PARKED/KILLED as a research contribution if:
1. direct prior art is found implementing essentially the same permission + predicted-benefit + measured-baseline + regression-accounting contract;
2. B4 cannot beat simpler static/adaptive baselines in controlled experiments;
3. the only meaningful gains require TLS interception or unsafe trust assumptions;
4. transformations save bytes but routinely worsen end-to-end latency/quality under realistic constrained-network traces;
5. security isolation requirements make the proposed deployment model impractical for the intended scope;
6. the remaining work is primarily reimplementation of CDN/image-optimization features.

## Pass 003 decision
**MORE RESEARCH — VOC survives only as a bounded, falsifiable evaluation hypothesis.**

The generic proxy idea and nearly all feature-level novelty claims are now dead. The next pass should be decisive rather than another terminology-narrowing exercise.

## Next pass
**Pass 004 — Feasibility Benchmark Design and Decisive Contribution Test**

Required work:
1. choose a bounded deployment/trust model;
2. define reproducible network profiles (bandwidth, RTT, loss where practical);
3. choose representative object corpus and content classes;
4. define B0–B4 exactly;
5. define byte, latency, compute, cache and fidelity metrics;
6. define hard protocol/security failure conditions;
7. determine whether experiments can be run on AJ-accessible hardware;
8. set numerical/decision thresholds before implementation;
9. issue GO / PARK / KILL for formal specification.

No implementation is authorized by this pass.
