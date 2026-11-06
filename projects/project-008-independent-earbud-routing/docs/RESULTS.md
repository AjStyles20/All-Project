# P013 Earbud Routing Lab — results

Date: 2026-11-06. Built under DR-021. Research verdict (KILL research, PARK engineering) unchanged.

## What was checked
**Routing rules (`sim/tests/router.test.js`, 12 tests, all pass):**
- coupled mode gives one source as L/R stereo; split mode gives a different mono source per ear;
- muting one ear in coupled mode turns the other ear into a mono downmix (and does not when downmix is off);
- a split-mode call goes to the chosen bud, uses only that bud's microphone, keeps media on the other bud, and blocks re-assigning the call ear or changing mode mid-call;
- a pause-media call uses both ears and pauses media; paused media does not advance;
- after either kind of call the earlier mode, sources and playback positions return;
- navigation prompts duck media on non-call ears, expire, and are held during a both-ears call;
- invalid ears, modes and non-media assignments are refused;
- the link model: retransmissions raise frame success as 1 − loss^(r+1); air time grows with streams and bitrate; the budget flag trips on a heavy setup; a split call adds a microphone uplink stream.

**Browser (built-in browser, static server on 127.0.0.1:8030):** started sound, switched to split, started a call on the right ear (left kept music, mic "right bud", three streams in the link panel: 58 % worst-case / 21 % typical air time at 5 % loss and 2 retransmissions), ended the call (split music/podcast restored), played a prompt (podcast ducked on the right), muted left. No console errors; no horizontal scroll at 375 px.

**Not checked:** I could not listen. Whether the generated sounds actually come out of the correct headphone side was not confirmed by ear; the gains that drive the left and right inputs of the channel merger come straight from the tested `mix()` output.

## Feasibility tiers (from Passes 001–003)
| Tier | Setting | Per-ear sources? |
|---|---|---|
| A | Ordinary app on a stock phone, commodity earbuds | **No** for other apps' audio or calls. The app can only play its own audio, as stereo. |
| B | Own app with its own sources, stereo output | **Partly**: this demo's approach. Two sources hard-panned to L/R works on any stereo earbuds, but calls and other apps stay outside its control. |
| C | Own LE Audio source + own earbud firmware (dev kits) | **Yes, technically**: two CIS streams, one per bud, as modelled here. Patent-encumbered. |
| D | Phone OS / chipset vendor | **Yes**: where Google, Samsung and others hold patents and work. |

## Radio model, in short
Per stream per 10 ms interval: payload bytes from bitrate, packet time on LE 2M PHY with ~112 bits overhead, plus inter-frame spaces and an acknowledgement, times (retransmissions + 1) for the worst case. Audio may use 60 % of air time. These are named parameters in `sim/src/link.js`; real figures depend on the controller, scheduling and interference.

## Honest caveats
- Same author built and checked everything; no independent review.
- No hardware, so nothing about latency, synchronisation between buds, battery or real loss is measured.
- Nothing here is new research; the behaviour is described in existing patents.
