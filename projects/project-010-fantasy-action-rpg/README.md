# P014 (folder legacy P010) — Lanterns of Brinewold

An original top-down, party-based fantasy action RPG that runs in the browser. You control one of four heroes and switch between them at any time; the others fight alongside you. Built under DR-021 as a **creative project**: Pass 001 removed it from the research shortlist, and that verdict is unchanged.

Inspiration and IP boundary: `research/PASS_001_IP_GENRE_COLLISION_AND_CREATIVE_TRACK_GATE.md`. What is original: `docs/IP_NOTES.md`.

## The game
The Murk, a light-eating fog, has drowned the waymarker lanterns of Brinewold. Four friends set out to light them again:
- **Brannoch Vey**: a retired dock fighter with a ship's anchor (melee tank).
- **Oswin Tallow**: a nervous lamplighter with firebombs. Only he can relight the lanterns.
- **Ilse Marrow**: a hedge-healer who bargains with marsh spirits.
- **Kettle**: a clockwork heron that marks enemies' weak points.

The quest: find the ferrywoman, cross the river, relight three lanterns (each draws an ambush), open the drowned chapel, and defeat the Lantern-Eater, which telegraphs its area attack with a warning ring. Party banter reacts to what happens. Downed heroes can be helped up by a friend standing beside them.

## Play
Serve the `game` folder with any static server and open it in a browser. Browsers block ES modules from `file://`, so opening the file directly won't work.
```bash
cd game
python -m http.server 8000      # then open http://127.0.0.1:8000
```
Controls:
- Move: WASD or the arrow keys.
- Attack: Space or J (hold).
- Special ability: K or Shift.
- Talk or use: E.
- Switch hero: 1–4 or Tab.
- Pause, save and load: P or Esc.

The game autosaves at each story step.

## Develop
```bash
cd game
node --test          # 12 tests, no dependencies
```
| Path | Contents |
|---|---|
| `game/src/data.js` | World, party, enemies, quest and banter |
| `game/src/engine.js` | Game rules: pure, deterministic, seeded; tested in Node |
| `game/src/render.js` | Canvas drawing (shapes, not images) |
| `game/src/main.js` | Keyboard, loop, party panel, story log, save and load |
| `docs/` | IP notes, balance notes, technology selection |

## Status (2026-11-05)
- **Playable:** one region, one quest chain, four heroes, three enemy types and a boss. Tested by unit tests, a scripted playthrough, and a browser check (title, combat, the ferry quest, crossing, pause, save).
- **Not yet done:** no human playtest (`docs/BALANCE.md`); companions don't dodge; no sound; keyboard only (no touch or gamepad).
