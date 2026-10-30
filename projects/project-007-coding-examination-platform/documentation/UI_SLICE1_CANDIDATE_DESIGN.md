# Web UI Slice 1 — Candidate Examination Flow

## Purpose
This slice is the first browser interface for the P001 product layer. It covers the **candidate** side end to end:
- sign in;
- my examinations;
- examination rules (ECC);
- research participation (FD-06 consent);
- start or resume;
- answering with autosave;
- submission;
- released result.

Examiner and administrator screens are **not** built yet. A non-candidate who signs in is told so, rather than shown non-functional controls (PROJECT_RULES §4).

## Technology decision (DR-017)
Following `docs/TECHNOLOGY_PLATFORM_SELECTION.md` §5–6 (progressive frontend rule), the UI is **semantic HTML, one CSS file and plain JavaScript**, calling the existing JSON API. It is served by the same FastAPI app at `/ui`.

React or another single-page framework was **not** selected. The flow is form-driven, and the policy reserves frameworks for when complexity justifies them. Because the browser only displays state and sends requests, **no business rule lives in the UI**. Every rule (lifecycle, deadlines, revisions, consent) stays enforced server-side, as in FD-02 to FD-06.

Running it needs an ASGI server. The platform previously had none (its API had only ever run under test clients), so `uvicorn` was added and `app/main.py` exposes the app:

```powershell
# from projects/project-007-coding-examination-platform, with P001_DB_* set (database/mysql/README.md)
uvicorn app.main:app --host 127.0.0.1 --port 8001
# then open http://127.0.0.1:8001/
```

## Figure 4.1 — Candidate screen flow
**Figure 4.1 shows the screens and the API calls behind each.**

```text
[Sign in] --POST /auth/login--> [My examinations]  (GET /auth/me, GET /candidate/examinations)
                                     |
       +------------+----------------+-------------------+-------------------------+
       v            v                v                   v                         v
   [Rules]    [Research]      [Start / resume]       [My result]               [Sign out]
   GET …/      GET/PUT …/     POST …/session          GET …/session (read-only)  POST /auth/logout
   contract    research            |                  GET /sessions/{id}/result
                                   v
                          [Examination session]
                          GET /sessions/{id}
                          PUT …/responses/{q}  (autosave, base_revision)
                          POST …/submit        (after flushing saves)
```

*Figure 4.1: Candidate UI screen flow and supporting API calls.*

## Figure 4.2 — Answer save-state indicator (NFR-08)
**Figure 4.2 shows the save states each answer box can display. Every state is written in words, not shown by colour alone.**

```text
 (typing) ──> "Unsaved changes…" ──1.5 s or blur──> "Saving…"
                                                      │
          ┌──────────────── 200 ──────────────────────┤
          v                                           │ 409 newer save
  "Saved <time> (revision n)"                         ├──> "Not saved: a newer version was saved elsewhere.
                                                      │     Copy your text, then reload this page."   (no overwrite)
                                                      │ 409/422 other
                                                      ├──> "Not saved: <reason>"
                                                      │ network error
                                                      └──> "Not saved: connection problem. Retrying…" (every 5 s)
```

*Figure 4.2: Per-answer save states shown to the candidate.*

Submit flushes every pending save first. It refuses, with a message, while any answer is unsaved, so a candidate cannot lose their latest text by submitting. The page warns before closing with unsaved changes. The candidate's own deadline (`my_ends_at`, including FD-05 extra time) is shown and refreshed every 30 seconds.

## Security
- **Content Security Policy on `/ui`:** `default-src 'self'; script-src 'self'; style-src 'self'; … object-src 'none'; base-uri 'none'; frame-ancestors 'none'`. There is no inline script or style, so no `unsafe-inline` is needed.
- **Other headers:** `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, `Cache-Control: no-store`.
- **No HTML from data:** all API data, such as question prompts and answers, is written with `textContent` through one helper (`el()`). The script contains no `innerHTML`, `eval` or `document.write`. A test enforces this.
- **Token storage:** the bearer token is kept in `sessionStorage`, so it is cleared when the tab closes. A 401 response signs the user out.
- **Known limit:** a token in `sessionStorage` is readable by any script on the page. The strict CSP and the no-HTML rule are the mitigations. Moving to HttpOnly cookies would need CSRF protection and is left for a later slice.

## Accessibility (PROJECT_RULES §13; evidence in TE-015)
- Labelled inputs, with a **distinct name per answer box** ("Your answer to question n").
- Save status in an `aria-live` region linked through `aria-describedby`.
- A skip link.
- Focus moves to the new content after each view change.
- Visible focus rings on controls.
- States conveyed in words.
- Light and dark themes via `prefers-color-scheme`.
- No horizontal scrolling at 375 px width.

These were checked in a browser. **No screen-reader or user test has been done**, so no accessibility compliance claim is made.

## Verification
- **Automated** (`tests/integration/test_web_ui.py`):
  - the UI is served and `/` redirects to it;
  - the security headers are present, with no `unsafe-*`;
  - there is no inline code and no HTML sinks;
  - the read-only session lookup does not start a session;
  - API responses are unaffected.
- **Browser (TE-015):** the whole flow was driven in a real browser against the disposable MySQL 8.4.9 instance with seeded test data. Six defects were found and fixed during that run (TE-015).

## Not in this slice
- Examiner screens (exam/question/contract management, marking, release).
- Administrator research screens.
- An accessibility audit with assistive technology.
- HttpOnly-cookie sessions.
