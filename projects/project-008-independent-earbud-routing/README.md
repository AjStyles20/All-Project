# P013 (folder legacy 008) — Independent Earbud Audio Routing: *Earbud Routing Lab*

Can the left and right earbuds play different things? This folder holds the research (three passes) and, under DR-021, a **simulation** of the routing rules a controlled LE Audio prototype would run. A browser demo plays the result through the left and right channels of ordinary headphones.

Research verdict: **KILL as research, PARK as advanced engineering** (`research/PASS_003_…`). That verdict is unchanged. The build is what Pass 003 suggested: "a controlled LE Audio prototype demonstrating split/coupled modes, per-ear mute, session continuity, and microphone selection". With no earbud hardware or firmware available, it is a simulation.

## ⚠ Read before using any of this commercially
- **Patent:** Bose US11916988B2 (and family) describes independent earbuds getting different LE Audio sources, with per-ear mono downmix and a phone-call example. Huawei, Google and Samsung patents cover nearby ground (Pass 003). **Shipping a product with this behaviour needs legal review.** This repository is a teaching and engineering demo.
- **Platform:** Ordinary Android or iOS apps cannot send *other apps'* audio (Spotify, phone calls) to one ear (Pass 002). A real version needs your own audio source, your own firmware, or system-level access.

## What it shows
| Feature | What happens |
|---|---|
| Coupled mode | One source in stereo, as normal earbuds play it. |
| Split mode | Each bud plays its own source, downmixed to mono. |
| Per-ear mute | Silences one bud. In coupled mode the other bud switches to a mono downmix, so nothing panned to the muted side is lost (can be turned off). |
| Calls | Either **pause media** (call on both ears, both mics) or **split** (call on one bud using only that bud's microphone, media continues on the other). |
| After a call | The earlier mode, sources and playback state come back; playback positions are kept. |
| Navigation prompts | Duck whatever plays on the ears not carrying a call; held while both ears are on a call. |
| Radio link panel | A rough air-time and frame-loss model for the streams the current routing needs, including the microphone uplink. |

## Layout
```
sim/
  src/router.js     routing rules (pure, tested)
  src/link.js       rough radio model (pure, tested)
  src/main.js       browser demo: Web Audio, generated sounds, controls
  index.html, style.css
  tests/router.test.js
docs/
  RESULTS.md                 what was checked and the feasibility tiers
  TECHNOLOGY_SELECTION.md    why a simulation, and what a hardware version would need
research/                    Passes 001–003 and the dossier
```

## Run
```bash
cd sim
node --test                              # 12 tests, no dependencies
python -m http.server 8030 --bind 127.0.0.1   # then open http://127.0.0.1:8030 with headphones on
```
Press **Start sound**. Every sound (music, a voice-like podcast, a call tone, a chime) is generated in the page; nothing is downloaded or recorded, and the microphone is never used.

## Limits
- A simulation: no Bluetooth, no earbuds, no firmware. Timing, latency, battery and real radio behaviour are not measured.
- The radio panel is a back-of-envelope model with named assumptions, not a measurement or a spec calculation.
- Generated sounds stand in for real music, speech and calls.
