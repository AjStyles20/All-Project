# P005 results (2026-11-05)

The research verdict stands: **killed as research** (Pass 001–003: every element, including competing hypotheses and abstention, already exists in prior work). This is the engineering build Pass 003 called "high engineering value". Diagnosis rules were frozen in commit `87f788f` before the final run. Raw output: `results/final.json`.

## Benchmark
**Synthetic incidents** (`p005/benchmark.py`), never to be read as production ground truth. Each has five services with background traffic and noise, one injected fault cascading into symptom errors, and 60 seeds for each of four case types:

| Case type | Truth |
|---|---|
| clear | the injected cause |
| red herring | the injected cause; a second fault's signals appear only after the errors began |
| ambiguous | UNRESOLVED: two different causes both start before the symptoms |
| missing | UNRESOLVED: the failing service's own logs are absent |

## Results (240 incidents)

| Method | Correct when there is a single cause | Asserted a cause it could not back up | Correctly said "unresolved" | Abstained when it should have answered |
|---|---|---|---|---|
| B0 keyword counting | 67.5 % | 60.4 % | 11.7 % | 0 % |
| B1 anomaly + timing | 67.5 % | 40.0 % | 45.0 % | 7.5 % |
| **B4 evidence-bounded (this tool)** | **75.0 %** | **9.6 %** | **80.8 %** | 25.0 % |

Every hypothesis B4 showed carried its log lines with file and line number (100 %).

## Reading it honestly
- **The trade-off is real.** B4 asserts far fewer unsupported causes, but stays silent on a quarter of incidents that did have one clear cause. For an on-call engineer that may be the right trade; it is still a cost.
- **Synthetic and self-authored.** I wrote the fault library, the generator and the rules. The generator's cause messages match the rule patterns by construction, so real logs, with their endless phrasings, will do worse. Real incidents with known root causes (from LogHub or similar, Pass 001) were not used.
- **Two flaws were found on pilot data and fixed before freezing:** a single noisy minute was treated as the incident start; a message naming "payments-api" was treated as missing telemetry although the "payments" logs were present.
- **No language model.** Hypotheses come from a fixed library of eight fault types; anything outside it is invisible to the tool.
- **No metrics or traces,** only logs.
