# FD-06 — Operational → EGPCV Evidence Bridge Design

## Purpose
FD-06 copies consenting candidates' submitted answers from the operational MySQL platform into the EGPCV research store (SQLite), labelled with the Examination Capability Contract in force when each answer was saved. It implements:
- ECC v1.0 §6 (evidence labelling);
- DR-013 Q3: answers become `ARTIFACT` evidence and the contract `POLICY_CONTEXT` evidence; marks are not copied;
- DR-013 Q4: an explicit question → case link is required;
- AJ's research-data decisions, recorded as DR-015.

### Why consent comes first
`M8_PILOT_PROTOCOL.md` §8 requires consent, ethics, privacy and de-identification to be resolved before real-student data is collected. FD-06 is that collection step. **The software records the ethics approval reference; it cannot verify that the approval exists.** Obtaining real institutional approval is AJ's responsibility before any real student is bridged.

## Figure 3.7.5 — ERD increment (operational side)
**Figure 3.7.5 shows the bridge tables and how they connect to earlier increments.**

```text
examinations 1 ----< research_links >---- 1 questions
                       PK link_id; UNIQUE(examination_id, question_id)
                       template_case_id, claim_ids (JSON), ethics_reference
                       FK created_by_user_id (administrator)

examinations/users 1 ----< research_consent_events   (append-only; latest = current)
                              status OPTED_IN | WITHDRAWN, recorded_at

examinations/users 1 ---- 0..1 research_identities   (LOCKED: admin-only API)
                              research_code UNIQUE (random "R-…")

examination_sessions 1 ----< research_bridge_records >---- 1 research_links
                              PK(session_id, question_id)
                              outcome BRIDGED | NO_RESPONSE | NO_CONTRACT
                              research_case_id, response_revision, policy_version
```

*Figure 3.7.5: Operational-side ERD increment for the evidence bridge.*

The research store receives only:
- `programming_cases` `op-<research code>-<question id>`, copied from the template case;
- `case_claims`, copied from the template;
- two `evidence_items` per case;
- `claim_evidence_links` for the linked claims.

No user ID, name, mark or reason category is written there.

## Figure 3.5.8 — Bridge run sequence
**Figure 3.5.8 shows one run and where each gate is applied.**

```text
Admin -> API: POST /admin/research/examinations/{id}/bridge
API -> BridgeService: run(exam)
BridgeService: research store configured?          no -> 503, nothing copied
BridgeService: exam CLOSED or ARCHIVED?            no -> 409
for each SUBMITTED session:
    current consent == OPTED_IN?                   no -> skipped_no_consent
    for each research link (exam question):
        bridge record exists?                      yes -> already_recorded
        saved response?                            no -> record NO_RESPONSE
        contract in force at saved_at?             no -> record NO_CONTRACT (spec R5)
        research code (create once, random)
        SQLite, ONE transaction, INSERT OR IGNORE, deterministic ids:
            case op-<code>-<q> from template; template claims;
            ARTIFACT  = answer text, created_at = saved_at,
                        policy_version = ecc:<exam>@v<n>#<hash>,
                        assistance_context = assistance caps + construct + exceptions at saved_at
            POLICY_CONTEXT = bound contract (examiner id redacted) + full content hash
            links: each linked claim -> both evidence items
        MySQL: record BRIDGED (provenance)
```

*Figure 3.5.8: Sequence of an evidence-bridge run.*

## Key implementation choices
- **Two databases, no shared transaction.** Each case is written to SQLite in one transaction using `INSERT OR IGNORE` and deterministic IDs (`<case>:artifact:r<revision>`, `<case>:policy:v<version>`). The MySQL bridge record is written afterwards. If a run fails between the two, the next run rewrites identical rows and then records them. A test simulates exactly this failure.
- **Consent is checked at run time.** The latest consent event wins.
- **Withdrawal deletes bridged data** (DR-016 (1)):
  - the withdrawal is recorded first;
  - the candidate's evidence and claim links are then deleted;
  - each case row is deleted unless an analysis record references it, in which case a content-free shell is kept;
  - the candidate's bridge records and code link are forgotten, and `research_withdrawal_log` keeps only the code and counts;
  - if the store is unavailable, deletion is pending, and `POST /admin/research/examinations/{id}/purge-withdrawn` retries it;
  - re-consenting later bridges again under a new random code.
- **Store location** (DR-016 (2)): the bridge refuses a research store inside the application directory. The Workbench guide documents an outside folder with restricted NTFS permissions.
- **Privacy defect found by a test and fixed.** The first implementation copied the full contract document into `POLICY_CONTEXT`, which included `bound_by_user_id`, the examiner's identity. The contract is now copied with that field redacted. The redaction is declared, and the full content hash is kept, so the exact contract can still be verified against the operational database.
- **Assistance context** follows spec §6:
  - the `ai_assistance`, `documentation`, `internet` and `clipboard` capabilities;
  - the construct for each linked claim;
  - the candidate's exceptions approved at or before the save time (spec §5.4), without their reason category.

## API surface

| Method | Path | Role | Purpose |
|---|---|---|---|
| POST | `/admin/research/links` | Administrator | link an exam question to a template case and claims (ethics reference required; claims must be REQUIRED on the template) |
| GET | `/admin/research/examinations/{id}/links` | Administrator | list links |
| POST | `/admin/research/examinations/{id}/bridge` | Administrator | run the bridge; returns counts and case IDs |
| GET | `/admin/research/examinations/{id}/records` | Administrator | bridge provenance records |
| GET | `/admin/research/examinations/{id}/identities` | Administrator | the locked code → candidate link |
| POST | `/admin/research/examinations/{id}/purge-withdrawn` | Administrator | retry pending withdrawal deletions |
| GET | `/admin/research/examinations/{id}/withdrawals` | Administrator | anonymous deletion log |
| GET | `/candidate/examinations/{id}/research` | assigned candidate | whether a study is linked, ethics references, own consent, what is collected |
| PUT | `/candidate/examinations/{id}/research` | assigned candidate | opt in or withdraw |

Configuration: `P001_RESEARCH_DB_PATH` points to the research SQLite file. If it is unset, the bridge endpoints answer 503.

## Verification status
- Service tests (`tests/unit/test_research_bridge_service.py`) use the **real SQLite research store** on a temporary file. They dump the whole research store to show that no personal identifier is present.
- API tests: `tests/integration/test_fd06_research_api.py`.
- SQL-contract tests: `tests/unit/test_mysql_research_repository.py`.
- Live: `tests/integration/test_mysql_fd06_live.py` passed on 2026-10-29 (MySQL 8.4.9 disposable instance plus a temporary SQLite research store, TE-013).

FD-06 is **IMPLEMENTED / UNIT + API TESTED / LIVE VERIFIED** on that instance. This is software verification only; **no real student has been bridged**, and no research claim is affected.

## Decisions and remaining limits
- **Resolved:** DR-015 (consent, identifiers, link role, granularity); DR-016 (deletion on withdrawal, store location).
- **Still required before real use:** real institutional ethics approval. The software records the reference but cannot verify it.
- **Known limit:** text that analyses derived from evidence before a withdrawal is not rewritten; only the evidence itself is deleted.
