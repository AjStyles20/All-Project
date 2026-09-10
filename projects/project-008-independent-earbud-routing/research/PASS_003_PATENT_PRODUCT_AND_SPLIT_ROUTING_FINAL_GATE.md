# P013 — Pass 003: Patent, Product, and Split-Routing Final Gate

## Canonical project
Current ID: P013
Previous ID: P008
Project: Independent Wireless Earbud Audio Routing

## Original bounded idea
Treat left and right members of a true-wireless earbud pair as either a conventional coordinated stereo device or, when explicitly requested, independently useful endpoints. Example target behavior: media in one ear and a call or other audio service in the other, plus per-ear mute/attention control and a later return to coupled stereo mode.

## Final novelty attack
Passes 001–002 established that LE Audio can physically carry independent left/right streams but ordinary Android applications do not control arbitrary third-party media and cellular telephony routing, while coordinated-set behavior intentionally preserves paired semantics.

Pass 003 searched patents, standards, products, and adjacent implementations for the remaining systems claim: independent source assignment to individual earbuds, possibly followed by recombination into normal stereo.

### Decisive patent collision
Bose patent family US11916988B2 / US20220103607 and continuation material explicitly describe independent wireless earbuds receiving different LE Audio broadcast sources. The disclosure states that the left bud may receive a first source while the right bud receives a second source, with mono downmix in each ear as needed. The patent also gives scenarios where a user listens to one program in one ear and a different source in the other, including a phone-call-related example. It further describes independent source selection for left and right earbuds through a mobile interface.

This is a direct collision with the product-level essence of the proposed split-ear routing concept.

### Broader prior art
- Bluetooth LE Audio Multi-Stream Audio already standardizes multiple independent synchronized streams between sources and sinks.
- LE Audio discovery/pairing guidance allows untethered left and right LE devices to be discovered separately while still coordinated as one product.
- Huawei-related patent material describes phones sending different audio data to left and right earbuds over separate ISO channels.
- Google patent US12615469B2 addresses switching between multiple earbud architectures/sources and cites the Bose multi-source patent and earlier Qualcomm simultaneous multi-source headset work.
- Samsung has an active patent family around Bluetooth audio multi-streaming.

### Commodity product state
Current Android/Pixel LE Audio sharing supports multiple Bluetooth LE Audio accessories, per-device volume, broadcast joining, and choosing which connected headphone handles calls. These features do not expose arbitrary Spotify-left / cellular-call-right routing to ordinary applications, but they confirm that multi-endpoint routing and call-device selection are now part of mainstream platform evolution.

## Hypothesis disposition
- H1 ordinary-app universal per-ear routing: REJECTED on feasibility and novelty grounds.
- H2 controlled asymmetric media/communication routing: technically plausible, but the essential multi-source/per-ear concept is directly covered by prior art.
- H3 dynamic coupled ↔ split transition: interesting implementation challenge, but narrowing novelty to transition policy/latency would be artificial given existing multi-source switching and coordination patents.
- H4 per-ear mute/attention control: useful feature, weak novelty.

## Final judgment
The exact consumer experience may not be commonly exposed in mainstream earbuds today, but lack of broad commercialization is not evidence of research novelty. The core idea—independent earbuds receiving different simultaneous audio sources, including phone-related audio—already exists explicitly in patent prior art, while LE Audio provides the underlying technical primitives and major platform vendors have active multi-stream and switching work.

Further narrowing to a custom transition controller, app policy layer, latency metric, or one particular media/call combination would risk manufactured novelty rather than identify a robust new contribution.

## Final decision
**KILL as a research-novelty/FYP candidate. PARK as an optional advanced engineering/embedded-systems project.**

A future engineering build could still be valuable as a controlled LE Audio prototype demonstrating split/coupled modes, per-ear mute, session continuity, and microphone selection, but it should be presented as implementation/integration work rather than as a novel research concept.

No formal research specification or implementation is authorized under the shortlist workflow.
