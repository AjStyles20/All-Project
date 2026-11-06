# P008 (folder legacy P013) — StartupMatch: Founder–Investor Matching Platform

A two-sided web app. Founders find investors whose stated focus and recent deals fit their startup; investors see startups that fit their thesis; intros are requested, accepted and then continued by message.

Research verdict: **killed as research** (`research/PASS_003_…`); built under DR-021 as the product Pass 003 described. That verdict is unchanged. There is no research claim, so there is no accuracy benchmark: the matching rules are tested for their behaviour.

## What it does (Pass 003 product scope)
- **Transparent matching:** sector, stage, region and cheque size each get their own verdict and a plain-language reason. **Unknown data is left out, not counted as a miss**, and lowers the confidence label instead.
- **Says vs does:** an investor's stated thesis is compared with their deals from the last three years (with at least four deals), and disagreements are shown to founders and to the investor.
- **Evidence provenance:** every recorded deal carries its source and the date it was last checked. Unverified or stale data and old profiles are flagged.
- **Workflow:** intro requests (at most 10 a day and one open per investor), then accept, in talks, pass or decline. Messages open only after acceptance.
- **Contact privacy:** contact details are revealed only after the investor accepts.
- **Disclaimer on every match list:** scores describe fit with a stated and recent focus; *they do not predict investment quality or the chance of funding.*

## Security
- **Passwords:** scrypt with per-user salts, and hashing even for unknown e-mails so timing doesn't reveal who has an account. Five failed sign-ins per e-mail per 15 minutes, then a pause.
- **Sessions:** random tokens stored as hashes, in an HttpOnly, SameSite=Strict cookie.
- **Requests:** every state-changing request must carry a custom header (CSRF), and every route checks role and ownership.
- **Page:** strict CSP, with all text written as text.
- **Not done:** profiles are **not identity-verified**, and the page says so.

## Run
```bash
pip install -r requirements.txt
python -m pytest -q
python -m p008 seed        # fictional demo accounts; prints a one-time demo password
python -m p008             # http://127.0.0.1:8019
```

## Limits
Not identity-verified; no e-mail notifications; no admin or moderation tools; single SQLite file; deal records are self-reported unless someone checks them. Fit scoring is a simple average of known criteria, deliberately easy to explain rather than tuned on any data.
