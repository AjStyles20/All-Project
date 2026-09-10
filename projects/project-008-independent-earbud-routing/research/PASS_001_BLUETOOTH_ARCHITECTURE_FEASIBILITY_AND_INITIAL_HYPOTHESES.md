# P013 — Independent Wireless Earbud Audio Routing
## Pass 001 — Bluetooth Architecture, Feasibility and Initial Hypotheses

Date: 2026-09-10
Previous ID: P008
Status: FEASIBILITY REVIEW / MORE RESEARCH

## Original concept
AJ's original idea came from using JBL true-wireless earbuds and wanting the two physical earbuds to become independently useful endpoints when desired. Example target behaviour: left earbud plays Spotify while right earbud carries a phone call; alternatively both earbuds operate normally together. A secondary feature is independently muting either side without physically removing an earbud.

## Feasibility-first finding
The concept must be separated into two technically different requirements.

### R1 — Per-ear mute / silence
This is comparatively feasible at the audio-routing or firmware layer. A system can suppress one output channel or route mono/selected content to one side, depending on OS, device and firmware control. It does not by itself require two unrelated Bluetooth services to run independently.

### R2 — Concurrent heterogeneous per-ear services
Example: Spotify/media to left ear while an active phone call is heard/handled through right ear. This is substantially harder. Conventional Bluetooth Classic headset behaviour is profile/session oriented: media commonly uses A2DP while calls use HFP/HSP, and a TWS pair is normally exposed to the host as one coordinated audio device rather than two independently addressable application sinks. Multipoint generally permits connection to multiple source devices and switching/prioritisation; it does not imply simultaneous assignment of one source/service to each earbud.

## Bluetooth LE Audio changes the architecture
Bluetooth LE Audio, based on LE Isochronous Channels introduced with Bluetooth Core 5.2, explicitly supports Multi-Stream Audio: multiple independent synchronized streams between an audio source and one or more sinks. Bluetooth SIG documentation describes separate left/right streams to independent earbuds/hearing aids and smoother operation across multiple source devices. Coordinated Set Identification lets earbuds still be treated as a set.

This establishes that independent left/right transport is technically supported by the modern Bluetooth architecture. It does NOT by itself establish that Android/iOS exposes an application API allowing Spotify to be assigned to one earbud while telephony is assigned to the other. Transport capability, firmware capability, OS audio policy and application routing are separate layers.

## Initial feasibility matrix
| Requirement | Initial status |
|---|---|
| Mute left or right output independently | FEASIBLE in principle; implementation path depends on device/OS control |
| Use either single earbud alone | Common existing TWS behaviour; not novelty |
| Treat pair normally as stereo | Existing/default behaviour |
| Connect headset to two source devices | Existing multipoint behaviour |
| Switch between media and call sources | Existing multipoint/profile behaviour |
| Send independent synchronized L/R streams | Supported by LE Audio Multi-Stream |
| Spotify on one ear + same-phone call on other concurrently | TECHNICALLY PLAUSIBLE at transport level but OS/API/firmware feasibility UNVERIFIED; likely not possible as a normal third-party app on arbitrary existing earbuds |
| Different applications to each earbud concurrently | UNVERIFIED; requires host routing support plus independently controllable sinks/streams |
| Retrofit arbitrary JBL/AirPods-class earbuds purely through an app | STRONGLY THREATENED; firmware/profile/OS constraints may prevent it |

## Important distinction
The research problem cannot be framed as simply 'split stereo channels'. Left/right channel separation already exists and LE Audio Multi-Stream explicitly supports independent streams. AJ's intended feature is stronger: independent **service/application routing** to two members of a coordinated wearable set while preserving an optional coupled/stereo mode.

Conceptually:

Mode COUPLED:
Source/service -> coordinated L+R pair

Mode SPLIT:
Media/application A -> earbud L
Call/application B -> earbud R

The second mode requires policy and control above basic stereo channelization.

## Initial novelty threats
1. LE Audio Multi-Stream already standardizes independent synchronized streams to separate earbuds.
2. Multipoint already handles multiple source devices and media/call switching.
3. Hearing-aid architectures already use independently configurable left/right and bidirectional streams.
4. Per-side mute/balance/mono behaviour is not a strong novelty claim.
5. Proprietary TWS firmware may already expose portions of independent-bud control.

## Candidate hypotheses
### H1 — Per-ear application/service routing
A host-side routing policy can expose a coordinated earbud pair as independently targetable logical sinks for concurrent heterogeneous audio sessions while retaining an explicit coupled stereo mode.
Status: SURVIVES CONCEPTUALLY; feasibility on commodity mobile OSes is the critical threat.

### H2 — Service-aware asymmetric routing
Media and communication sessions can be assigned to different earbuds according to user policy without unacceptable call intelligibility, media continuity, latency or control conflicts.
Status: SURVIVES, but requires hardware/OS path that may not be available to an ordinary app.

### H3 — Dynamic coupled/split transition
A pair can transition between normal synchronized stereo and independent service routing with bounded interruption and deterministic restoration of session state.
Status: ENGINEERING/RESEARCH CANDIDATE; prior art attack required.

### H4 — Per-ear attention control
Independent mute/attenuation plus automatic restoration can reduce physical earbud removal for short environmental interactions.
Status: useful product feature; weak novelty.

## Critical next questions
1. What exactly do Android AudioPolicy, Telecom/CommunicationDevice APIs and Bluetooth stacks permit for simultaneous A2DP/LE Audio/telephony routing?
2. Can a normal Android application create two logical sinks for members of a coordinated LE Audio set, or is privileged/system-level access required?
3. Do current LE Audio earbuds expose each member independently to host routing, or only through a coordinated-set abstraction?
4. Can call downlink/uplink be bound to one member while media is bound to another?
5. What happens to microphones: which earbud supplies call uplink in split mode?
6. Are there direct patents/products/research systems for asymmetric service routing across left/right earbuds?
7. Is a prototype feasible with controllable LE Audio development hardware even if arbitrary commercial JBL earbuds cannot be retrofitted?

## Pass 001 decision
MORE RESEARCH / FEASIBILITY REVIEW.

The idea is not killed. Bluetooth LE Audio makes the underlying independent-stream topology substantially more plausible than Bluetooth Classic. However, the exact desired behaviour—concurrent per-ear application/service routing, especially Spotify on one side and a phone call on the other—must not be claimed feasible on ordinary consumer earbuds until OS audio policy, telephony routing, firmware control and LE Audio coordinated-set APIs are verified.

Next pass: Android/OS audio-routing constraints, LE Audio coordinated-set control, telephony/media concurrency, development-hardware feasibility, and direct product/patent prior art.