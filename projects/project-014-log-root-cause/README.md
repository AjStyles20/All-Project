# P005 (folder legacy P014) — Automated Log Analysis and Root-Cause Assistance Tool

A local command-line tool that reads your log files, finds when an incident began, and lists **competing explanations**. Each one comes with the exact log lines for and against it, and the tool says which check would best tell them apart. It answers **UNRESOLVED** or **INSUFFICIENT EVIDENCE** when the logs can't decide, and **never declares a cause verified on its own**: only a check result you record can do that.

Research verdict: **killed as research** after three passes (`research/`); built under DR-021 for its engineering value. That verdict is unchanged.

## Claim states (Pass 001)
- **OBSERVED:** present in the logs.
- **CORRELATED:** present around the incident.
- **SUPPORTED:** appears before the errors began, repeatedly. Not proof.
- **CONTRADICTED:** evidence against it, such as first appearing well after the errors began.
- **VERIFIED:** only by a check you record.
- **UNRESOLVED / INSUFFICIENT EVIDENCE:** the tool abstains.

## Use
```bash
pip install -r requirements.txt            # only pytest; the tool itself uses the standard library
python -m p005 demo ambiguous --out incident.log         # or use your own logs
python -m p005 analyse incident.log --report report.html --session incident.p005.json
python -m p005 record incident.p005.json --hypothesis deploy --result refutes \
    --check "config diff against the last healthy release is empty" --by "AJ"
python -m p005 analyse incident.log --report report.html --session incident.p005.json   # report now shows it
python -m pytest -q
python -m p005.benchmark final
```
Log formats: `TIMESTAMP LEVEL [service] message`, `TIMESTAMP LEVEL service: message`, or JSON lines with `ts`, `level`, `service` and `msg`.

## Safety
- Logs are untrusted: text is only matched and displayed (HTML-escaped), never executed or obeyed.
- Passwords, tokens, bearer and JWT values, AWS keys, e-mail addresses and long digit runs are redacted before anything is stored or shown.
- Files over 50 MB and lines over 4,000 characters are refused or truncated.
- The tool has no remediation actions at all.

## Results
On 240 synthetic incidents, it asserted unsupported causes in 9.6 % of cases, against 40–60 % for simpler methods. It was right 75 % of the time when there was one cause, but stayed silent on 25 % of those. Details and caveats: `docs/RESULTS.md`.
