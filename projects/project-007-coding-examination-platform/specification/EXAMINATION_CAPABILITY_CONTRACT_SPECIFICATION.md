# P001 Examination Capability Contract (ECC) — Specification v1.0

**Status:** **APPROVED v1.0.** AJ approved it on 2026-10-29 (DR-013, A3), answering open questions Q1–Q5 (§10). This is the frozen ECC schema named in the development-corpus versioning list. Nothing in it is implemented yet; implementation is planned as FD-05/FD-06. Changing it requires a new versioned decision.
**History:** v0.1 drafted 2026-10-29 (PR #22) → v1.0 approved the same day with no change to the drafted content. The JSON shape in §8 is labelled schema v1.0 from approval onwards.
**Requirement:** RTM FR-15 (ECC Management). It also bounds FR-16 (process capture), FR-17 (integrity observations), FR-18 (authorized exceptions) and FR-19 (evidence provenance).
**Drafted:** 2026-10-29 by Claude Code (Engineering), at AJ's request.

## 1. Why the ECC exists
§12 of `FORMAL_RESEARCH_EXPERIMENT_SPECIFICATION.md` states that an observation is interpreted under the ECC before any integrity meaning is assigned. Without an ECC, the platform cannot tell whether a paste, a documentation lookup or an AI interaction was permitted. Operational submissions (FD-03) therefore cannot yet become EGPCV evidence (deferred in FD-04).

The ECC is the examination's **declared, versioned statement of which capabilities a candidate may use**. Evidence is then labelled with the exact contract version under which it arose.

## 2. Sources this specification formalises
No new research claim is introduced here. The ECC operationalises existing project material:

| Source | What it contributes |
|---|---|
| `research/PASS_003_…` §7, candidate C1 | Machine-readable capability list (compiler, debugger, visible tests, terminal, documentation, internet, clipboard, AI, external IDE, assistive-technology exception) and the four integrity modes |
| `research/PASS_004_…` §4, C1 verdict | Standalone novelty WEAK. Value lies in the versioned contract that declares capabilities, labels every evidence event with the active version, prevents out-of-policy interpretation and represents accommodations. Also supplies the core invariant (§7, R1) |
| `research/PASS_005_…` §4–5 | ECC as EGPCV supporting mechanism #1; invariants 1, 3, 4, 8, 9, 10 |
| `FORMAL_RESEARCH_EXPERIMENT_SPECIFICATION.md` §12–13 | Interpretation order; no invented evidence |
| `DEVELOPMENT_CORPUS_SPECIFICATION.md` (Versioning) | The ECC schema is one of the artifacts that must be frozen and versioned |
| `app/domain/models.py` `EvidenceItem` | `policy_version` and `assistance_context` fields already exist; `EvidenceType.POLICY_CONTEXT` already exists |

**Novelty position (inherited, unchanged):** configurable exam permissions are established prior art. The ECC is **not** claimed as a contribution in itself. It is infrastructure that makes the EGPCV interpretation chain explicit and auditable.

## 3. Scope
**The ECC is:**
- a declaration of permitted capabilities, an integrity mode and an assistance construct per examination;
- versioned, and immutable once bound;
- extended per candidate by authorized exceptions;
- the reference against which observations are labelled.

**The ECC is not:**
- a runtime enforcement mechanism. Enforcement (lockdown, sandboxing, process capture) is separate future work (FR-16, secure execution).
- a misconduct detector or a source of verdicts;
- a competence judgment.

Until enforcement exists, every contract must be reported as **DECLARED, NOT ENFORCED** wherever it is shown, as required by the truth rules in PROJECT_RULES §4–5.

## 4. Concepts

### 4.1 Contract
A contract belongs to one examination. It has an identifier, a monotonically increasing version, a content hash and a status of `DRAFT`, `BOUND` or `SUPERSEDED`.

### 4.2 Capabilities
Each capability key takes exactly one value from its permitted set.

| Key | Permitted values | Meaning of the values |
|---|---|---|
| `compiler` | `ALLOW`, `DENY` | compile/run own code |
| `debugger` | `ALLOW`, `DENY` | step/inspect tools |
| `visible_tests` | `ALLOW`, `DENY` | candidate sees provided tests |
| `terminal` | `ALLOW`, `LIMITED`, `DENY` | `LIMITED` requires a declared command allowlist |
| `documentation` | `ALLOW`, `ALLOWLIST`, `DENY` | `ALLOWLIST` requires named sources |
| `internet` | `ALLOW`, `ALLOWLIST`, `DENY` | as above |
| `clipboard` | `ALLOW`, `INTERNAL_ONLY`, `DENY` | `INTERNAL_ONLY` allows copying within the exam workspace only |
| `ai_assistance` | `DENY`, `DECLARE`, `ALLOW_BOUNDED`, `ALLOW` | `DECLARE` means permitted but the candidate must declare use; `ALLOW_BOUNDED` requires stated limits |
| `external_ide` | `ALLOW`, `DENY` | tools outside the platform |

The key set comes from PASS_003 C1. The "assistive technology exception" listed there is modelled as an authorized exception (§4.5), not as a capability, so that it can never be read as a candidate choice. Adding or removing keys after approval requires a new schema version.

### 4.3 Integrity mode
Exactly one of the following (PASS_003 §6):
- `LAB_CONTROLLED` (the default; PASS_005 invariant 10 keeps lab operation viable without webcam capture);
- `RESTRICTED_BROWSER`;
- `REMOTE_PROCTORED`, which requires a recorded justification (policy, legal basis/consent, accessibility review);
- `OPEN_TOOL_DECLARED`.

The mode describes the collection conditions under which observations arise. It changes what observations exist, not what they mean.

### 4.4 Assistance construct
For each competence claim assessed, the contract states whether the claim is **independent** or **assistance-inclusive**. This implements PASS_005 invariant 4: assisted success counts as independent competence only if the construct explicitly includes assistance. The default is `INDEPENDENT`.

### 4.5 Authorized exceptions
A per-candidate amendment to the contract, such as extra time, an assistive tool, or a permitted capability that is otherwise denied. Each exception records:
- candidate;
- capability or time change;
- reason **category** (for example `ACCESSIBILITY` or `TECHNICAL`). Detailed reasons are deliberately not stored, under the NFR-10 privacy requirement;
- approver;
- approval time;
- the contract version it amends.

Exceptions are versioned with the contract and are never inferred from behaviour.

## 5. Lifecycle and versioning
1. **Drafting.** The contract is editable only while the examination is DRAFT, and only by the owning examiner. This mirrors FD-02 DRAFT-only editing.
2. **Binding.** The DRAFT → SCHEDULED transition binds the current draft. It becomes immutable, receives a content hash, and the transition is refused if no contract exists. This mirrors DR-011 (1), "no scheduling without content".
3. **Amendment after binding** creates a new version with a recorded reason. The old version becomes `SUPERSEDED`. **Amendments are never retroactive.** Every observation keeps the version active when it occurred.
4. **Exceptions** may be added after binding. Each one is time-stamped, and only applies to events after its approval time.
5. **Experiments.** For research runs, the contract version and hash form part of the frozen experiment configuration. The same contract applies to every B0–B4 method on a given case (cross-method rule, `BASELINE_METHOD_CONTRACTS.md`).

## 6. Evidence labelling (the bridge to EGPCV)
When operational artifacts are registered as EGPCV evidence (the deferred "evidence bridge", a later increment):
- `EvidenceItem.policy_version` = `ecc:<examination_id>@v<version>#<hash prefix>`, the contract **in force when the artifact was produced**;
- `EvidenceItem.assistance_context` = a canonical summary of the assistance-relevant capabilities (`ai_assistance`, `documentation`, `internet`, `clipboard`), the assistance construct and the active exception state;
- the bound contract itself is registered once per case as `EvidenceType.POLICY_CONTEXT` evidence, so reviewers and assessors see the policy alongside the artifact.

**Mapping (Q3, approved):**
- a submitted FD-03 response becomes `ARTIFACT` evidence;
- process/event capture becomes `PROCESS` evidence (FR-16, not yet built);
- FD-04 examiner marks are **not** mapped automatically, because they are operational judgments, not evidence states.

## 7. Interpretation rules (normative once approved)
- **R1 (core invariant, PASS_004):** no event is classified as a policy deviation without resolving it against the exact contract version and the authorized-exception state active when the event occurred.
- **R2:** use of a permitted capability is never a deviation and never misconduct (PASS_005 invariant 3).
- **R3:** assisted success supports an `INDEPENDENT` competence claim only through additional independent evidence. Gap-driven verification (B4) is how such evidence is acquired (invariants 4, 6).
- **R4:** the ECC can only produce **observation labels**, never verdicts:
  - `WITHIN_CONTRACT`;
  - `OUTSIDE_CONTRACT`, which is routed to human review (FR-17);
  - `UNDETERMINABLE`, used when capture is missing or ambiguous.

  Consequential integrity findings remain human-authorized (invariant 8).
- **R5:** if the contract is missing or unbound, observations are labelled `UNDETERMINABLE`. The system never assumes DENY or ALLOW (§13 of the formal spec: missing data is not invented).
- **R6:** behaviour covered by an authorized accessibility exception is labelled `WITHIN_CONTRACT` and is never surfaced as suspicious (PASS_004 C1 point 5).
- **R7:** while a contract is DECLARED, NOT ENFORCED, an absence of observed deviations must not be reported as evidence of compliance.

## 8. Schema v1.0
```json
{
  "contract_id": "ecc-<examination_id>",
  "examination_id": "<id>",
  "version": 1,
  "status": "BOUND",
  "content_hash": "sha256:<hex>",
  "enforcement": "DECLARED_NOT_ENFORCED",
  "integrity_mode": "LAB_CONTROLLED",
  "capabilities": {
    "compiler": "ALLOW", "debugger": "ALLOW", "visible_tests": "ALLOW",
    "terminal": {"value": "LIMITED", "allowlist": ["python", "pytest"]},
    "documentation": {"value": "ALLOWLIST", "sources": ["python-stdlib-docs"]},
    "internet": "DENY", "clipboard": "INTERNAL_ONLY",
    "ai_assistance": "DENY", "external_ide": "DENY"
  },
  "assistance_construct": {"default": "INDEPENDENT", "per_claim": {}},
  "remote_proctoring_justification": null,
  "bound_at": "<UTC>", "bound_by_user_id": "<examiner>",
  "supersedes_version": null, "amendment_reason": null
}
```
The content hash covers every field except `status`, `bound_at` and `content_hash` itself, with keys in canonical (sorted) order.

## 9. Implementation increments
- **FD-05, ECC management:**
  - storage (migration 005);
  - DRAFT editing;
  - binding on schedule, with a hash;
  - amendments and per-candidate exceptions;
  - examiner API;
  - a candidate-visible read-only view, so candidates know what is permitted;
  - DECLARED, NOT ENFORCED labelling.
- **FD-06, evidence bridge:** register submitted responses and the bound contract as EGPCV evidence for a configured case and claims, with full provenance (§6). Per Q4, the link is an **explicit research step**: a researcher links an examination question to a `ProgrammingCase` and its claims. Nothing becomes EGPCV evidence by default.
- **Later:** process capture (FR-16), integrity observations (FR-17), runtime enforcement and secure execution.

## 10. Resolved decisions (AJ, 2026-10-29, DR-013)
1. **Q1 Capability set:** accepted exactly as §4.2 (the PASS_003 list). Adding keys later, for example runtime limits once secure execution exists, needs a new schema version.
2. **Q2 Binding point:** bind on DRAFT → SCHEDULED, so candidates see final rules before the exam opens.
3. **Q3 Evidence mapping:** submitted responses become `ARTIFACT` evidence and the bound contract becomes `POLICY_CONTEXT` evidence. Examiner marks are **not** mapped.
4. **Q4 Case mapping:** linking an examination question to a `ProgrammingCase` and its claims is a separate, explicit research step. There is no automatic mapping.
5. **Q5 Default integrity mode:** `LAB_CONTROLLED`.

## 11. Non-claims
This specification does not:
- establish novelty;
- validate any interpretation rule empirically;
- implement enforcement;
- make any integrity or competence claim.

Approval froze it as the ECC schema v1.0 named in the development-corpus versioning list. That does not make it a validated instrument.
