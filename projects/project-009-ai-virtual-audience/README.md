# P012 (folder legacy P009) — Interactive AI Virtual Audience: *Rehearsal Room*

Practise a talk and the questions after it in front of a simulated panel that reacts. Panel members have moods (supportive, neutral, sceptical, impatient); they interrupt mid-talk, ask questions, and follow up when an answer is thin. Afterwards you get simple, explained measures of each answer, and a suggested next drill based on your recent runs.

Research verdict: **killed as research** (`research/PASS_003_…`: commercial tools already close the "spot a weakness, drill it" loop); built under DR-021 as the product Pass 003 listed. That verdict is unchanged.

**Practice only.** It does not assess, diagnose or treat anxiety or any other condition, and it says so on the page (Pass 001–003 boundary).

## Relation to P011
Following the project boundary ("do not split one product into two names"), Rehearsal Room does **not** repeat P011's document-grounded questioning. It adds what P011 lacks: a live panel with moods, **interruptions, rapid follow-ups and time pressure**, delivery measures and a practice journey. A combined product would use P011 for the questions and this for the room.

## What it measures (from the text of each answer)
- **Started after:** seconds from the question to your first keystroke or spoken word.
- **Took:** total time, and whether you went over the limit.
- **Filler words** per 100 words: um, uh, like, you know, basically, …
- **On the question:** overlap with the question's key words (with simple stemming) or the asker's focus.
- **Uses evidence:** numbers, tests, data or users mentioned.
- **States a limit:** acknowledges a limitation or uncertainty.
- **Interruption recovery:** did the talk after an interruption pick up the thread from before it?

These are surface measures of text, not judgements of quality. "Like" is counted as a filler even when it isn't one.

## Practice journey
Each run's measures are kept in this browser only, as the last 50 runs. The weakest area over your last five runs picks the next drill and pre-ticks its pressures: rapid questions, strict time, unexpected question, interruptions, a sceptical panel, or slow deliberate answers.

## Privacy
- **Typing never leaves the page.**
- **Reading questions aloud** uses the browser's own voices.
- **Answering by speech is optional.** In Chrome and Edge, speech-to-text sends audio to the browser maker's servers, and the page says so before you turn it on.
- There's no server, no account and no analytics.

## Run
```bash
cd app
python -m http.server 8020     # then open http://127.0.0.1:8020
node --test                    # 12 tests, no dependencies
```

## Limits
Fixed question banks for three scenarios; no avatars beyond simple drawn faces; no video or voice analysis (pace, volume, eye contact). Measures were not validated against human ratings, and nothing here shows that practice transfers to real talks.
