# P004 — Internet Compression & Optimization Proxy System
## Pass 002 — Direct Prior-Art Attack on Adaptive Optimization Policy and Low-Bandwidth Gateways

**Canonical ID:** P004  
**Legacy directory:** project-012-internet-compression-proxy  
**Research state:** MORE RESEARCH — MAJOR NARROWING REQUIRED  
**Implementation:** NOT AUTHORIZED

## Research question
Do existing browsers, compression proxies, carrier middleboxes, standards and academic systems already implement the Pass-001 candidates: net-benefit transformation gating, constraint-aware saving profiles, transformation provenance and safe abstention?

## Evidence reviewed

### Opera Mini
Opera Mini remains direct product prior art. Opera documents selectable data-saving modes. Extreme mode can reduce pages/images/text to roughly 10% of original size, while its cloud compression requires access to plaintext content and therefore does not preserve strict client-to-origin end-to-end encryption in that mode. Opera also distinguishes less-aggressive and extreme modes for different network/user priorities.

Implication: user-selectable quality/data-saving profiles, server-side transformation and aggressive low-bandwidth optimization are not novel.

### Chrome Data Saver / Lite mode
Chrome Data Saver/Lite mode used Google servers to compress pages and reported data-use reductions up to 60%. It also used network information/prediction to decide when to provide Lite pages; Chrome stated that if it predicted more than about five seconds before first text/image, it could load a Lite version. Google sunset Lite mode in Chrome M100 in 2022.

Implication: adaptive decision-making based on expected network/page-load conditions is established product prior art. The discontinuation is not evidence that the underlying problem disappeared; it is evidence that product economics, browser evolution and changing mobile-data conditions matter.

### Save-Data and Client Hints
The Save-Data request header represents explicit user preference for reduced data usage. It permits origins to return smaller images/video, altered markup/style, reduce polling/updates and otherwise adapt content. HTTP Client Hints formalizes server-selected response adaptation based on client-provided preferences/capabilities with privacy considerations.

Implication: explicit user preference + context-aware response adaptation is standardized prior art. H2 cannot be claimed as novel in generic form.

### Academic adaptive transcoding
Han et al. (1998), *Dynamic adaptation in an image transcoding proxy for mobile Web browsing*, explicitly describes deciding whether and how much to transcode based on predicted transcoding delay, predicted output size and estimated network bandwidth, with fixed-quality and fixed-delay adaptation policies.

Implication: the central Pass-001 H1 concept — deciding whether transformation is worth its processing/network tradeoff — has direct historical prior art going back decades. H1 is killed as a generic novelty claim.

### Cellular transparent proxies
Xu et al. (2015) found cellular carrier proxies performing combinations of caching, traffic redirection, image compression and connection reuse. Crucially, they found these proxies did not necessarily improve performance; noticeable benefits depended on conditions such as sufficiently large flows and paths with high latency/loss. They also observed quality degradation from unilateral image compression.

Implication: "bytes saved" and "performance improved" are empirically distinct. Conditional benefit and user-quality cost are established findings. P004 must measure both.

## Hypothesis attack

### H1 — Net-Benefit Transformation Gate
**Status: KILLED AS STANDALONE NOVELTY.**
Adaptive transcoding literature already predicts network bandwidth, output size and processing delay to decide whether/how much to transcode. Chrome Lite mode also used expected page-load performance to select alternate delivery.

Retain only as required engineering behavior.

### H2 — Constraint-Aware Data-Saving Profiles
**Status: KILLED AS STANDALONE NOVELTY.**
Opera Mini has user-selectable saving modes; Save-Data represents explicit user preference; Client Hints support context-aware adaptation.

Retain only as product/UX mechanism.

### H3 — Transformation Provenance
**Status: PARTIAL SURVIVOR, NOVELTY UNKNOWN.**
Recording original/transformed byte size and latency is ordinary observability. A stronger version may survive if provenance becomes an auditable per-object decision record: what transformation was considered, why it was permitted/refused, predicted benefit, actual benefit, quality/fidelity effect, trust boundary and rollback/revalidation outcome. This requires direct prior-art attack in optimization observability/CDN/WAN systems before any novelty claim.

### H4 — Safe Abstention
**Status: PARTIAL SURVIVOR, NOT NOVEL GENERICALLY.**
Adaptive systems already choose not to transcode under unfavorable conditions. However, P004 may distinguish *technical/economic abstention* from *trust-boundary abstention*: no transformation when the system lacks legitimate plaintext access, content is sensitive/authenticated, cache semantics prohibit reuse, transformation safety is uncertain, or expected utility is non-positive.

This is currently a safety architecture candidate, not a research contribution.

## Major conclusion
The original P004 contribution space is much more crowded than Pass 001 alone suggested. Adaptive compression, quality profiles, network-aware transformation and conditional optimization are established.

A defensible P004 cannot be "an intelligent compression proxy" or "a proxy that decides how much to compress." Those ideas have direct prior art.

## Strongest surviving research direction
### Verifiable Optimization Contract (VOC) — provisional name
Instead of inventing another compression algorithm or adaptive proxy, investigate a policy/evidence layer that decides whether an optimization is *permissible and demonstrably beneficial* under modern encrypted-web constraints.

For each object/request, a bounded contract could require:
1. **Trust eligibility** — is the system legitimately allowed to inspect/transform this payload?
2. **Semantic eligibility** — do cache-control, content type, authentication, integrity/signature and application semantics permit transformation/reuse?
3. **Benefit eligibility** — predicted transfer saving and latency benefit exceed transformation/compute overhead.
4. **Fidelity eligibility** — expected quality loss is inside the selected user/application budget.
5. **Security eligibility** — parser/transcoder/resource limits and content safety requirements are satisfied.
6. **Observed outcome** — actual bytes, latency, CPU and quality proxy are measured after transformation.
7. **Counterfactual comparison** — preserve enough information to compare transformed delivery against pass-through baseline.
8. **Decision state** — PASS THROUGH / REENCODE / TRANSCODE / CACHE-REVALIDATE / DELTA / ABSTAIN.

The core invariant becomes:

> An optimization is not successful merely because it reduces bytes; it must satisfy the applicable trust, semantic, fidelity and security constraints and show positive measured net benefit against a pass-through baseline.

This is a candidate contribution only. Similar ideas may exist in CDNs, WAN optimization controllers, adaptive media systems, service meshes or policy-driven proxies.

## HTTPS/TLS boundary
P004 should not normalize TLS interception as its primary architecture. A first defensible prototype should prefer an origin-controlled/reverse-proxy test environment or another explicit endpoint trust arrangement. Arbitrary third-party HTTPS interception creates certificate, privacy, credential, compliance and plaintext-concentration risks that would overwhelm the intended research contribution.

## Evaluation implications
Future experiments must compare at least:
- B0: pass-through/no optimization;
- B1: fixed compression/transcoding policy;
- B2: network-aware adaptive policy;
- B3: candidate VOC policy/evidence gate.

Measure bytes transferred, wall-clock completion/load time, transformation CPU time, cache behavior, fidelity/quality proxy where relevant, incorrect transformations, abstention rate and security/policy violations.

Important adversarial cases:
- already-compressed payload where recompression wastes CPU;
- tiny payload where overhead exceeds saving;
- large image on constrained link where transcoding helps;
- fast link where transformation increases latency;
- authenticated/private response that must not enter shared cache;
- `no-store`/non-transformable semantics;
- malformed or decompression-bomb-like content;
- signed/integrity-sensitive object;
- unsupported encrypted flow where plaintext is unavailable;
- user requests high fidelity despite expensive network.

## Killed claims after Pass 002
Do not use as novelty claims:
- bandwidth-saving proxy;
- compression proxy;
- image transcoding proxy;
- cache + transcode proxy;
- adaptive compression based on bandwidth;
- deciding whether/how much to transcode based on latency/size/network;
- user-selectable data-saving modes;
- network-aware Lite/low-bandwidth pages;
- Save-Data-aware optimization;
- generic "AI chooses the best compression level".

## Security gate
The next pass must include explicit investigation of HTTP `Cache-Control: no-transform`, authenticated/private caching, Content-Digest/integrity semantics, CSP/SRI interactions where relevant, decompression bombs, image parser/transcoder vulnerabilities, cache poisoning/key confusion, SSRF/open-proxy abuse, request smuggling, privacy leakage and TLS trust boundaries.

## Pass-002 verdict
**MORE RESEARCH — MAJOR NARROWING REQUIRED.**

P004 remains technically worthwhile, but its generic optimization ideas are prior art. The only plausible research direction now is a modern, verifiable optimization decision contract under encryption, semantics, fidelity, security and measured-benefit constraints. Novelty is UNKNOWN.

## Next pass
**Pass 003 — Modern HTTP Semantics, Security Constraints and Direct Prior-Art Attack on Verifiable Optimization Contracts.**

The next pass must attempt to falsify VOC by examining:
- `Cache-Control: no-transform` and cache semantics;
- CDN/WAN optimization decision logs and policy engines;
- content adaptation standards;
- integrity/signature implications;
- modern reverse proxies and image optimization services;
- explicit transformation observability/provenance;
- security failures introduced by content-transforming intermediaries;
- whether existing systems already implement permission + expected-benefit + measured-outcome gating.
