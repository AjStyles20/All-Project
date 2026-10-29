# FD-05 — Examination Capability Contract Management Design

## Purpose
FD-05 implements management of the Examination Capability Contract (ECC), as specified in the **approved ECC v1.0** (`specification/EXAMINATION_CAPABILITY_CONTRACT_SPECIFICATION.md`, DR-013). It covers spec §9 "FD-05":
- storage;
- draft editing;
- binding on schedule, with a content hash;
- amendments;
- per-candidate exceptions;
- examiner API;
- candidate read-only view;
- DECLARED, NOT ENFORCED labelling.

This document describes the implementation and does not change the approved specification.

## Figure 3.7.4 — ERD increment
**Figure 3.7.4 shows the contract tables added by FD-05.**

```text
examinations 1 ----< capability_contracts
                       PK/FK examination_id
                       PK    version
                       status DRAFT | BOUND | SUPERSEDED
                       document (canonical JSON, spec §8)
                       content_hash (sha256:<64 hex>)
                       bound_at
                            |1
                            |
                            '----< contract_exceptions >---- 1 users (candidate)
                                     PK exception_id
                                     FK (examination_id, contract_version)
                                     capability_overrides (JSON)
                                     extra_time_minutes (0..1440)
                                     reason_category (category only, NFR-10)
                                     FK approved_by_user_id, approved_at
```

*Figure 3.7.4: ERD increment for capability contracts and authorized exceptions.*

As Figure 3.7.4 shows, every contract version is a separate row keyed by (`examination_id`, `version`). Bound and superseded rows are never rewritten. Each exception references the exact contract version it amends.

## Figure 3.5.7 — Contract version lifecycle
**Figure 3.5.7 shows how contract versions move between states and which examination transitions drive them.**

```text
 exam DRAFT:  save_draft ──> v1 DRAFT  (editable; same version)
                               │
 exam DRAFT → SCHEDULED:       │  bind in the same transaction
                               v
                             v1 BOUND ──────────────────────────────┐
                               │                                     │
 exam SCHEDULED/ACTIVE: amend  │ (reason required)                   │ exam SCHEDULED → DRAFT,
                               v                                     │ then save_draft (reason required)
                 v1 SUPERSEDED + v2 BOUND (bound immediately)        v
                                                             v2 DRAFT (v1 stays BOUND)
                                                                     │ next DRAFT → SCHEDULED
                                                                     v
                                                     v1 SUPERSEDED + v2 BOUND
```

*Figure 3.5.7: Version lifecycle of an Examination Capability Contract.*

As Figure 3.5.7 shows, no transition rewrites an existing bound version. Every change after binding creates a new version with a recorded reason, as spec §5.3 requires.

## Key implementation choices
- **Binding transaction.** `MySQLExaminationRepository.update_status` binds within the DRAFT → SCHEDULED compare-and-set transaction:
  1. lock the DRAFT row (`FOR UPDATE`);
  2. supersede any BOUND version;
  3. bind the draft with `bound_at = UTC_TIMESTAMP(6)`;
  4. require exactly one BOUND version.

  If no contract exists it raises `ContractRequiredError`, which rolls back the status change too. The service pre-checks first so the user gets a clear message (409).
- **Content hash** (spec §8): SHA-256 over the canonical JSON (sorted keys, no whitespace) of every field except `status`, `bound_at` and the hash itself. The binder is inside the hash. Because only the owning examiner can schedule or amend (FD-02 ownership), the binder is known when the draft is saved, so the hash is fixed before binding. The stored JSON document is the hashed document, so the hash can be recomputed and checked at any time. The live test does exactly this after a MySQL round trip.
- **Capability validation:** all nine keys are required. Values come from the fixed sets. `LIMITED`, `ALLOWLIST` and `ALLOW_BOUNDED` require detail, and other values reject detail. Exception overrides are validated by the same per-key function.
- **Version in force at an event:** `in_force_at(exam, t)` returns the version bound most recently at or before `t`. FD-06 will use it to label evidence (spec §6).
- **Return to DRAFT:** the bound version stays in force. A new draft version needs a reason and replaces the old one only at the next schedule.

## API surface

| Method | Path | Role | Purpose |
|---|---|---|---|
| GET | `/examiner/examinations/{id}/contract` | owner | all versions |
| PUT | `/examiner/examinations/{id}/contract` | owner | save the draft (exam DRAFT) |
| POST | `/examiner/examinations/{id}/contract/amendments` | owner | new bound version (exam SCHEDULED/ACTIVE, reason required) |
| POST | `/examiner/examinations/{id}/contract/exceptions` | owner | per-candidate exception (assigned candidate) |
| GET | `/examiner/examinations/{id}/contract/exceptions` | owner | list exceptions |
| GET | `/candidate/examinations/{id}/contract` | assigned candidate | bound contract plus own exceptions |

Every contract body carries `"enforcement": "DECLARED_NOT_ENFORCED"`. Bound versions also carry their `policy_version` label (`ecc:<exam>@v<n>#<hash prefix>`).

## Known limitation (truthful labelling)
- **Extra time is recorded but not applied** to FD-03 session deadlines. Exception bodies say so explicitly (`extra_time_applied_to_deadline: false`). Applying it is an open point for AJ.
- No capability is enforced at runtime; the whole contract is declarative (spec §3, R7).

## Verification status
- Domain and service: `tests/unit/test_capability_contract.py`.
- API: `tests/integration/test_fd05_contract_api.py`.
- SQL contract: `tests/unit/test_mysql_contract_repository.py`, covering binding statements, rollback trigger, DRAFT guards, supersede guard and document round trip.
- Live: `tests/integration/test_mysql_fd05_live.py` passed on 2026-10-29 against MySQL 8.4.9 on a disposable instance (TE-011). The FD-02 to FD-04 live tests now store a contract before scheduling.

FD-05 is **IMPLEMENTED / UNIT + API TESTED / LIVE VERIFIED** on that instance.

## Open point for AJ
1. Apply exception extra time to the candidate's FD-03 deadline (`ends_at` + minutes), or keep recording it only until the UI work?
