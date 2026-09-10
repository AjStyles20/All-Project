# P013 — Pass 002: Android Audio Policy, LE Audio Coordinated Sets, and Call/Media Feasibility

## Decision
MORE RESEARCH / FEASIBILITY REVIEW. Commodity Android application implementation is strongly constrained; a system-level or controlled-hardware prototype remains plausible.

## Core question
Can a normal mobile application route independent services to individual members of a true-wireless earbud pair, e.g. media to the left earbud and call audio to the right, then restore coupled stereo without reconnecting?

## Verified findings
1. Android public APIs permit an application to select a preferred output device for an AudioTrack it owns. This does not grant arbitrary control over another app's playback such as Spotify.
2. Android's `setCommunicationDevice()` allows a voice/video application to choose a communication output from the platform's available communication devices, while the matching input source is selected automatically. This is communication-device selection, not explicit left/right-earbud routing.
3. Android supports combined routing to multiple devices through Audio Policy Manager, but strategy-level preferred-device APIs are system/privileged capabilities. They are not an ordinary third-party app mechanism for taking over global media/telephony routing.
4. Android telephony/capture rules privilege the active call. Ordinary apps cannot freely capture call uplink/downlink; privileged permissions are required for call audio capture.
5. Bluetooth LE Audio can send independent synchronized left/right streams, but coordinated-set mechanisms are specifically designed so left/right devices can be treated as one set and transition together.
6. Bluetooth's own LE Audio architecture explicitly describes coordinated transitions as preventing one source from taking only the right earbud while another source takes the left. This directly conflicts with P013's desired commodity-headset behaviour unless the stack or endpoint firmware is intentionally designed otherwise.

## Implications for the original idea
### Spotify left + phone call right
A normal app cannot simply reroute Spotify because Spotify owns its AudioTrack and Android does not expose a general third-party API to bind another application's media track to an arbitrary sink. The phone-call path is also controlled by telephony/communication audio policy. Even if the physical LE Audio pair receives independent left/right streams internally, the OS may expose it as one coordinated logical output rather than two separately selectable sinks.

### Per-ear mute
This remains much easier than split-service routing. It could be implemented through endpoint firmware, channel attenuation, accessibility/control APIs where exposed, or a controlled prototype. It is useful but not a strong novelty claim.

## Architecture viability by implementation level
### A. Ordinary Android app + arbitrary commercial earbuds
Status: STRONGLY THREATENED.
Reason: insufficient authority over other apps' media, telephony routing and left/right coordinated-set membership.

### B. Android system / custom ROM / privileged service
Status: PLAUSIBLE.
Reason: system audio-policy APIs can control strategies and multiple preferred devices. This could permit an experimental routing policy if the Bluetooth stack exposes the members suitably.

### C. Controlled LE Audio hardware / custom firmware
Status: PLAUSIBLE TO STRONG.
Reason: left/right endpoints and stream assignments can be designed explicitly. This is the cleanest environment for testing split/coupled policies, but it becomes an embedded/networking systems project rather than a consumer app.

## Hypothesis migration
- H1 per-ear application/service routing: survives only for controlled/system-level environments; commodity-app claim is heavily weakened.
- H2 asymmetric media/communication routing: survives as a systems feasibility question, not yet as product novelty.
- H3 dynamic coupled/split transitions: survives as an experimental systems mechanism.
- H4 per-ear mute: useful engineering feature; weak research novelty.

## Candidate next research question
Can a controllable LE Audio source/endpoint architecture support dynamic transitions between coordinated stereo and independently assigned service streams with acceptable latency, continuity, synchronization and microphone behaviour?

## Required next pass
Directly attack patents, commercial products, research prototypes and LE Audio multi-service use cases that may already implement or claim asymmetric member-level routing. If direct prior art substantially occupies split/coupled service routing, kill the research-novelty path. If not, freeze a systems experiment around controlled hardware or privileged Android rather than promising arbitrary consumer-earbud support.
