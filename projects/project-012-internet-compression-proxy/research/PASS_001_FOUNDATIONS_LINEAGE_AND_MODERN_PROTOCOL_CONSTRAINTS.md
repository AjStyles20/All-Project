# P004 (canonical; legacy directory P012) — Pass 001: Foundations, Historical Lineage and Modern Protocol Constraints

## Control
- Canonical portfolio ID: **P004**
- Previous ID / legacy directory: **P012** / `project-012-internet-compression-proxy`
- Class: GENERAL / PRODUCT SYSTEM
- Stage: FOUNDATIONS / PRIOR-ART / FEASIBILITY
- Implementation authorization: **NO**
- Decision: **MORE RESEARCH — LEGITIMATE PROBLEM, GENERIC PROXY NOVELTY FALSIFIED, TRUST-BOUNDARY REFRAME REQUIRED**

## 1. Working question
Can an application-level system materially reduce transferred data or improve perceived responsiveness for users on constrained links without making unsafe claims about encrypted traffic, violating web semantics, degrading content without consent, or merely rebuilding established CDN/browser/proxy techniques?

## 2. Problem legitimacy
Bandwidth cost, caps, slow links and unstable mobile connectivity are legitimate problems. Historical systems explicitly targeted these conditions, including Google's Flywheel data-compression proxy, carrier transparent proxies, transcoding proxies and caching proxies.

However, problem legitimacy does not establish novelty. The core idea of placing a proxy between client and origin to compress, cache or transcode web content is decades old.

## 3. Historical lineage / direct prior art
Prior art reviewed establishes:
- compression proxies for HTTP existed by the late 1990s;
- adaptive image transcoding proxies existed by 1998;
- proxy architectures combining transcoding and caching existed by the early 2000s;
- Google Flywheel operated a production mobile data-compression proxy and reported roughly 50% median reduction in proxied page size;
- Remote-Control Caching (RC2) used a proxy plus URL rewriting to reduce redundant mobile transfers and reported large warm-cache savings;
- carrier transparent proxies have performed caching, image compression, redirection and connection reuse, with benefits dependent on workload/network conditions.

Therefore none of the following are contribution claims:
1. proxy-based bandwidth reduction;
2. HTTP response compression;
3. image transcoding at a proxy;
4. caching at a proxy;
5. adaptive compression based on bandwidth;
6. connection reuse;
7. generic low-bandwidth web optimization;
8. combining caching + compression + transcoding.

## 4. Modern HTTP compression changes the baseline
Modern browsers/servers already negotiate representation compression through `Accept-Encoding` and `Content-Encoding`. Gzip and Brotli are established; Zstandard is now deployed by major infrastructure providers. Modern managed reverse proxies/CDNs can negotiate, recompress and serve Zstandard/Brotli/Gzip automatically.

This means a P004 prototype that merely receives HTML/CSS/JS and gzip-compresses it is not a meaningful modern contribution and may produce little or no saving when the origin/CDN already serves an efficient encoding.

Already-compressed media such as JPEG, modern image formats, audio, video and archives generally should not be blindly recompressed.

## 5. Shared/delta dictionaries raise the baseline further
Modern HTTP is adding shared dictionary compression, allowing a response to be encoded relative to content the browser already possesses. Current infrastructure support includes dictionary-compressed Brotli/Zstandard passthrough, subject to browser/origin support and origin scoping.

Therefore repeated-version transfer reduction cannot be treated as unexplored territory. P004 must benchmark against ordinary cache validation and modern dictionary/delta mechanisms where applicable.

## 6. HTTPS/TLS is the decisive trust boundary
A traditional intermediary cannot safely inspect and rewrite arbitrary HTTPS response bodies while preserving end-to-end TLS between browser and origin. With modern HTTPS prevalence, an ordinary network-path proxy often sees an encrypted tunnel rather than transformable application content.

Meaningful body optimization therefore requires an explicit trust/termination model such as:
- origin-controlled reverse proxy/CDN;
- client-controlled application/browser component paired with an optimization service;
- enterprise/user-installed TLS interception trust anchor (high security/privacy cost and unsuitable as a casual default);
- application/API integration where the service is authorized to transform content;
- metadata/transport optimization that does not require payload decryption.

P004 must never imply that it can transparently compress arbitrary encrypted Internet traffic without changing a trust boundary.

## 7. HTTP/2 and HTTP/3/QUIC constraint
Modern web traffic may use multiplexed HTTP/2 or HTTP/3 over QUIC. A legacy HTTP/1.1 forward-proxy design is therefore not representative of the contemporary web. HTTP/3/QUIC also complicates transparent network-path interception because application data is encrypted and carried over QUIC rather than a transformable plaintext HTTP stream.

A future prototype must state exactly which protocol boundary it supports and what happens to unsupported traffic. Silent downgrade claims are unacceptable.

## 8. Caching constraint
Caching can reduce transfer dramatically, but browser caches, CDNs, validators, managed caches and service workers already exist. HTTPS also prevents an unrelated in-path proxy from acting as a normal shared content cache for arbitrary encrypted origins.

Any caching contribution must therefore identify a measurable redundancy that existing cache semantics fail to exploit, while respecting `Cache-Control`, `Vary`, authorization, cookies, privacy and freshness.

The project must not intentionally violate `no-store`, private-content semantics or authenticated-resource isolation simply to improve a bandwidth metric.

## 9. Lossy transformation is a policy problem, not only a compression problem
Image/video transcoding can save bytes but changes fidelity and may damage text in images, accessibility, evidence, medical/technical diagrams, artwork, QR codes or user expectations. Historical carrier proxies have demonstrated that unilateral quality reduction can improve transfer time while hurting user satisfaction.

Therefore any lossy mode must be explicit, measurable and user/policy controlled. Candidate classes:
- lossless-safe;
- visually conservative;
- aggressive data-saving;
- no-transform / excluded.

The original content's directives and content type must constrain transformation.

## 10. Candidate reframing
The strongest surviving research direction after Pass 001 is not "a compression proxy." It is a **constraint-aware optimization policy system** that decides *whether an object should be transformed at all*, given protocol/trust boundary, existing encoding, cacheability, content type, estimated network condition, expected byte saving, transformation CPU/latency cost, quality budget, privacy sensitivity and user policy.

Candidate decision form:

`optimize(object, context) -> {PASS_THROUGH, REENCODE, TRANSCODE, CACHE/REVALIDATE, DELTA_IF_SUPPORTED, ABSTAIN}`

The research question becomes whether such a policy can produce net user benefit under constrained links relative to modern baselines, rather than whether compression itself works.

Novelty status: **UNKNOWN**. Adaptive transcoding and optimization policy have substantial prior art and must be attacked directly in Pass 002.

## 11. Required utility model
A future optimization must not optimize bytes alone. Candidate utility needs at least:
- bytes saved;
- added server/proxy CPU;
- transformation latency;
- time-to-first-byte / completion time;
- client decode cost where relevant;
- quality/fidelity loss;
- cache hit/revalidation effects;
- privacy/security cost;
- monetary data cost where measurable;
- failure/fallback behavior.

A transformation that saves 8 KB but adds 800 ms may be harmful. A transformation that saves 70% of a large image on a slow metered link may be useful if quality remains within the selected policy.

## 12. Security and privacy gate
Threats include:
- TLS interception/credential exposure;
- proxy becoming a high-value plaintext concentration point;
- cache leakage between users;
- incorrect caching of authenticated/private responses;
- content injection or transformation bugs;
- decompression bombs and oversized bodies;
- malicious media parser/transcoder inputs;
- request smuggling/desynchronization across protocol translations;
- SSRF/open-proxy abuse;
- DNS/rebinding abuse;
- certificate validation failure;
- logging sensitive URLs/headers/content;
- malicious origins manipulating content type/length;
- stale or poisoned cache objects;
- denial of service through expensive transforms.

Security architecture must be specified before implementation. An open forward proxy is explicitly out of scope for a first prototype.

## 13. Candidate prototype boundaries (not authorized yet)
Most defensible prototype families to research:

### A. Origin-controlled optimization gateway
A reverse proxy for sites/APIs the operator controls. Safest TLS semantics and easiest measurement, but overlaps heavily with CDNs and web servers.

### B. Client-consented low-bandwidth gateway
A dedicated client/browser/app explicitly routes supported content through an optimization service and knows the trust model. Potentially closer to historical Flywheel; requires strong privacy/security design.

### C. Offline/repeat-access optimization layer
Targets repeated transfer and version similarity using cache/delta techniques. Modern shared dictionaries are a major prior-art threat.

### D. Measurement/recommendation system rather than transparent proxy
Observes test workloads and recommends the optimal transformation policy without intercepting arbitrary private traffic. Lower deployment risk, but product value/novelty must be established.

## 14. Initial hypotheses to attack
- **H1 — Net-Benefit Transformation Gate:** predict when a transformation provides positive end-to-end utility rather than merely byte savings.
- **H2 — Constraint-Aware Data-Saving Profiles:** explicit user quality/data/latency policy combined with content risk and network state.
- **H3 — Transformation Provenance:** record original encoding/size, transformation, resulting size, latency, quality metric and reason so every claimed saving is auditable.
- **H4 — Safe Abstention:** pass through content when TLS/trust, cache semantics, content sensitivity, expected benefit or transformation safety does not justify modification.

These are hypotheses only. Adaptive transcoding, QoS policies and performance-aware proxies have old prior art, so novelty is not assumed.

## 15. Baselines required later
- B0 direct fetch/origin behavior;
- B1 normal browser HTTP compression/cache behavior;
- B2 modern reverse-proxy/CDN compression baseline where controllable;
- B3 fixed optimization policy (always transcode eligible content);
- B4 candidate adaptive/constraint-aware policy.

Metrics must include bytes and latency together; quality metrics are required for lossy transformations.

## 16. Kill/reframe criteria
Park or reframe if:
1. modern browser/CDN compression and caching eliminate meaningful savings for the supported workload;
2. remaining savings require unsafe or unacceptable TLS interception;
3. adaptive policy does not outperform a simple fixed policy on net utility;
4. transformation CPU/latency outweighs network savings under realistic constrained links;
5. quality degradation needed for useful savings is unacceptable;
6. protocol coverage is so narrow that the proposed product claim becomes misleading;
7. direct prior art already provides the same constraint-aware decision mechanism with comparable deployment goals;
8. privacy/security requirements make the architecture unsuitable for the intended users.

## 17. Pass 001 conclusion
**MORE RESEARCH — LEGITIMATE PROBLEM, GENERIC PROXY NOVELTY FALSIFIED, TRUST-BOUNDARY REFRAME REQUIRED.**

The historical problem remains real, especially on constrained or metered links, but compression/transcoding/caching proxies are mature prior art and modern HTTP/CDN capabilities raise the baseline substantially. HTTPS/TLS is the architectural dividing line: P004 can only transform content where the trust model explicitly permits access to plaintext. The strongest remaining research target is whether an auditable, constraint-aware optimization policy can create measurable net benefit over modern browser/CDN behavior without unsafe interception or misleading performance claims.

## 18. Next pass
**Pass 002 — Direct Prior-Art Attack on Adaptive Optimization Policy and Low-Bandwidth Gateways.**

Investigate:
- Opera Mini and historical/current data-saving browsers;
- Google Flywheel/Chrome Data Saver and why such products changed/disappeared;
- carrier optimization platforms;
- Squid/Varnish/nginx/CDN optimization;
- adaptive bitrate and image quality selection;
- WebP/AVIF negotiation and responsive images;
- Save-Data / Client Hints and content negotiation;
- shared dictionary compression;
- network-aware web adaptation;
- WAN optimization and enterprise products;
- VPN/TLS/QUIC constraints;
- open-source optimizing proxies;
- whether H1-H4 survive direct comparison.