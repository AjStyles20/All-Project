# Data card: P002 science-facts corpus

Follows the data-governance requirements of Pass 001 and Pass 002.

| Field | Value |
|---|---|
| Source | 40 facts and 40 matching misconceptions written by hand for this project (`p002lm/corpus.py`) |
| Licence | CC0; no external text was copied |
| Teacher model | None. No larger model generated or filtered any data, so the trained model's knowledge comes only from these sentences. |
| Accuracy | Simplified school-level statements, not an authoritative reference (e.g. water boils at 100 °C only at sea level). |
| Personal data | None |
| Conditions | `exposition`: each fact in five training templates. `contrast`: the same, plus "some people think X. that is wrong. Y." units (40 % of lines). Both use the same character budget (60,000). |
| Evaluation | Two templates ("did you know …?", "a teacher would say …") never appear in training (tested). Misconception items: correct vs misconception sentence in those templates. Recall items: correct subject vs a wrong subject. |
| Validation | 6,000 characters of exposition text from a separate seed. |
| Known contamination | The contrast condition sees every misconception sentence in training (inside "that is wrong" units), so contrast results measure discrimination of misconceptions it has been told about, not transfer to new ones. |
| Hashes | Each run records a SHA-256 prefix of its training text in `results/final.json`. |
