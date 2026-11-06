# P013 — technology selection

## Chosen: browser simulation (plain JavaScript + Web Audio)
- No earbud dev kit, LE Audio source board or firmware toolchain is available, and Pass 002 showed a stock-phone app cannot do the routing for other apps' audio.
- The routing rules are the part that carries over to any real version, so they are pure functions (`router.js`) with tests. The demo is a thin layer on top.
- Web Audio's `ChannelMergerNode` lets the page decide exactly what reaches each headphone channel, which is the closest a browser gets to "each bud".
- No dependencies, no build step, strict CSP, nothing recorded or sent.

## Rejected
| Option | Why not now |
|---|---|
| Android app with `AudioManager`/`AudioTrack` panning | Same result as the browser for its own audio; cannot reach other apps or calls (Pass 002). |
| Real LE Audio prototype (e.g. Nordic nRF5340 Audio DK pair + a source board) | Needs hardware purchase and firmware work; and the behaviour is patented (Bose US11916988B2), so legal review first. |
| Bluetooth Classic dual-A2DP tricks | Classic true-wireless designs relay or sniff one stream; not a sound basis (Pass 001). |

## What a hardware version would need
1. Two LE Audio earbud dev boards with firmware that accepts one CIS each, plus a source (dev board or a phone with system access).
2. The same routing rules as `router.js`, running on the source; per-bud volume and mute in the bud firmware.
3. Measured latency, sync between buds, loss and battery, to replace the rough model in `link.js`.
4. Legal review of the Bose, Huawei, Google and Samsung patent families before any product use.
