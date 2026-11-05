# Balance notes (2026-11-05)

Tuned with a scripted bot that walks the quest route, attacks continuously and uses specials when ready. Results are the same across 10 seeds, because only enemy movement uses the random generator.

| Version | Bot result at the Lantern-Eater |
|---|---|
| Boss 520 HP, no area attack, mark ×2 | Wins in 6.6 s, party barely hurt (whole game 23 s) |
| Boss 1,500 HP, "Swallow the Light" area attack | Wins in 17 s, nobody down |
| Boss 3,200 HP, mark ×1.5 | Loses in 24 s |
| **Boss 2,200 HP, damage 20, area attack every 6 s for 30 (current)** | **Wins in about 26 s with two heroes down** |

Limits of this method:
- **The bot does not play like a person.** A bot that stepped back from the warning ring did *worse*, because only the controlled hero moves away while the AI companions stay in melee and take the hit. The companion AI does not dodge; that is a known weakness to fix.
- The results do not change smoothly with the numbers, so the bot is a sanity check (not trivial, not impossible), not a tuning tool.
- **No human playtest yet.** Difficulty for a real player is unknown.
