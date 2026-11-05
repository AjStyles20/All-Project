# P014 technology selection (PROJECT_RULES §21)

| Item | Choice | Why |
|---|---|---|
| Platform | Browser game | No install; runs on the 4 GB development laptop. A game engine (Godot, Unity) would add a heavy toolchain for a one-region prototype. |
| Language | Plain JavaScript modules | No build step; anyone can open and read the code. |
| Rendering | HTML canvas, shapes drawn in code | No art assets, so nothing to license, and the look stays original. |
| Game rules | `engine.js`, pure and deterministic with a seeded random generator | Rules can be tested in Node without a browser, and runs can be reproduced. |
| Tests | Node's built-in test runner (`node --test`) | No dependencies. |
| Saving | `localStorage`, wrapped so the game still works where storage is blocked | Single player, local. |
| Accessibility | Full keyboard play; story, goal and party status as text beside the canvas (polite live region); enemy types differ by shape, not only colour; water and lantern animations stop when the system asks for reduced motion; pause at any time | Game state must not be available only as pictures. |
| Security | Content Security Policy allowing only same-origin scripts and styles; all text written with `textContent` | Nothing is loaded from elsewhere. |
