# Project 001 — Windows Local Runbook

## Scope
This runbook is for the local single-user prototype. The supported launcher binds only to the loopback interface; it is not a public/LAN deployment guide.

## 1. Prepare Python environment
From PowerShell in `projects/project-001-ai-defense-simulator`:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, you can call the virtual-environment Python directly instead of changing execution policy:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 2. Keep external providers disabled for the first local run
The default is already disabled. You may make it explicit for the current PowerShell session:

```powershell
$env:P001_OPENAI_ENABLED = "0"
```

Do not paste API keys into source files, HTML, JavaScript, Git commits, screenshots, or browser forms.

## 3. Run the self-check

```powershell
python self_check.py
```

Expected result ends with `SELF-CHECK PASS`. The check validates local bind configuration, writable data location, SQLite initialization and provider configuration structure. It does not make an external AI request.

## 4. Start the local application

```powershell
python run_local.py
```

The supported launcher defaults to:

`http://127.0.0.1:8000`

It refuses non-loopback bind addresses. Do not replace it with `0.0.0.0` for normal local use.

## 5. First browser verification
Open `http://127.0.0.1:8000` and verify:
- home page renders;
- workspace can be created;
- a TXT/Markdown/PDF/DOCX/PPTX source can be uploaded;
- lexical search returns provenance;
- provider-dependent controls truthfully show unavailable while providers are disabled.

Speech input/output cannot be considered device-verified until the configured provider path and browser microphone/audio path are exercised intentionally.

## 6. Optional provider configuration
Only after the local provider-disabled path works, set an API key in the **server process environment** and enable the provider intentionally:

```powershell
$env:P001_OPENAI_API_KEY = "<set-this-locally; never commit it>"
$env:P001_OPENAI_ENABLED = "1"
python self_check.py
python run_local.py
```

The self-check reports only that a key is present; it never prints the value and it does not make a provider request.

## 7. Backup local data
Stop active write-heavy work if practical, then run:

```powershell
python backup_database.py
```

The tool uses SQLite's backup API and runs an integrity check on the created backup. Backups are placed under the untracked `backups/` directory.

## Claim boundary
A successful local run verifies the exercised machine/browser path only. It does not establish public-deployment security, multi-user isolation, educational effectiveness, universal prompt-injection resistance, or production readiness.
