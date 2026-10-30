"""Cohesive B4 EGPCV orchestration for the first research-critical CC3 slice."""
from dataclasses import dataclass
from datetime import datetime

from app.domain.enums import ClaimApplicability, EvidenceState
from app.domain.models import ClaimEvidenceLink, EvidenceStateRecord
from app.domain.verification_run import UsedProbe, VerificationRun, VerificationRunStatus
from app.services.audit_trail import AuditTrailRecorder
from app.services.cc3_response_evaluator import CC3ProbeResponse
from app.services.evidence_evaluator import EvidenceEvaluator
from app.services.gap_detector import GapDetector
from app.services.probe_catalog import cc3_development_probes
from app.services.probe_selector import ProbeSelection, ProbeSelector
from app.services.stop_rule import ClaimControlInput, StopRule
from app.services.verification_workflow import VerificationUpdate, VerificationWorkflow


@dataclass(frozen=True)
class B4StartResult:
    run_id: str
    state: EvidenceState
    selection: ProbeSelection | None
    control_decision: str


class B4Orchestrator:
    """Coordinates persistence, selection, verification and audit for CC3.

    This is deliberately bounded to the first development slice. It does not
    infer misconduct, authorship, marks, or overall programming competence.
    """

    def __init__(self, repository, run_repository, audit_repository, probe_audit_repository):
        self.repository = repository
        self.run_repository = run_repository
        self.audit = AuditTrailRecorder(audit_repository)
        self.probe_audit_repository = probe_audit_repository

    def start_cc3(
        self, *, run_id: str, case_id: str, started_at: datetime,
        method_version: str = "B4-v1.0-development",
        configuration_version: str = "PROBE-CATALOG-v1.0-development",
    ) -> B4StartResult:
        self.run_repository.create(VerificationRun(
            run_id=run_id, case_id=case_id, method_version=method_version,
            configuration_version=configuration_version,
            status=VerificationRunStatus.ACTIVE, started_at=started_at,
        ))
        case_claims = {c.claim_id: c for c in self.repository.get_case_claims(case_id)}
        cc3 = case_claims.get("CC3")
        if cc3 is None:
            raise ValueError("CC3 is not configured for this case.")

        evaluation = EvidenceEvaluator().evaluate(
            "CC3", self.repository.get_evidence_for_claim(case_id, "CC3")
        )
        state_record = EvidenceStateRecord(
            case_id=case_id, claim_id="CC3", state=evaluation.state,
            rationale=evaluation.rationale, recorded_at=started_at,
            source=method_version,
        )
        self.repository.append_evidence_state(state_record)
        self.audit.record_initial_state(
            event_id=f"{run_id}-STATE-01", case_id=case_id, claim_id="CC3",
            state=evaluation.state, rationale=evaluation.rationale, recorded_at=started_at,
        )

        if cc3.applicability is ClaimApplicability.NOT_APPLICABLE:
            decision = StopRule().decide([
                ClaimControlInput("CC3", cc3.applicability, evaluation.state, False)
            ])
            self._finish(run_id, decision.decision, decision.rationale, started_at)
            return B4StartResult(run_id, evaluation.state, None, decision.decision)

        gap = GapDetector().detect("CC3", cc3.applicability, evaluation.state)
        if gap is None:
            decision = StopRule().decide([
                ClaimControlInput("CC3", cc3.applicability, evaluation.state, False)
            ])
            if decision.decision != "CONTINUE_VERIFICATION":
                self._finish(run_id, decision.decision, decision.rationale, started_at)
            return B4StartResult(run_id, evaluation.state, None, decision.decision)

        self.audit.record_gap(
            event_id=f"{run_id}-GAP-01", case_id=case_id, gap=gap, recorded_at=started_at
        )
        used = self.run_repository.used_probe_ids(run_id)
        selection = ProbeSelector().select(
            gap_type=gap.gap_type, claim_id=gap.claim_id,
            probes=cc3_development_probes(), used_probe_ids=used,
        )
        selection_event_id = f"{run_id}-SELECT-01"
        self.audit.record_selection(
            event_id=selection_event_id, case_id=case_id,
            selection=selection, recorded_at=started_at,
        )
        self.probe_audit_repository.append_selection_candidates(
            event_id=selection_event_id, case_id=case_id, claim_id="CC3",
            gap_type=gap.gap_type, candidates=selection.candidate_dispositions,
        )
        if selection.selected_probe is None:
            self._finish(
                run_id, "HUMAN_REVIEW_REQUIRED", selection.rationale, started_at
            )
        return B4StartResult(run_id, evaluation.state, selection, selection.decision)

    def submit_cc3_response(
        self, *, run_id: str, response: CC3ProbeResponse,
        evidence_id: str, recorded_at: datetime,
    ) -> VerificationUpdate:
        run = self.run_repository.get(run_id)
        if run is None or run.status is not VerificationRunStatus.ACTIVE:
            raise ValueError("Verification run does not exist or is not ACTIVE.")

        history = self.repository.list_evidence_states(run.case_id, "CC3")
        if not history:
            raise ValueError("CC3 has no recorded state for this run.")
        previous_state = history[-1].state

        gap = GapDetector().detect("CC3", ClaimApplicability.REQUIRED, previous_state)
        if gap is None:
            raise ValueError("CC3 currently has no targetable EG-T3 evidence gap.")

        selection = ProbeSelector().select(
            gap_type=gap.gap_type, claim_id="CC3",
            probes=cc3_development_probes(),
            used_probe_ids=self.run_repository.used_probe_ids(run_id),
        )
        if selection.selected_probe is None:
            self._finish(run_id, "HUMAN_REVIEW_REQUIRED", selection.rationale, recorded_at)
            raise ValueError("No adequate unused probe remains.")

        probe = selection.selected_probe
        # The workflow guard ensures only a probe with a frozen response rubric executes.
        update = VerificationWorkflow().apply_cc3_response(
            case_id=run.case_id, selection=selection, response=response,
            evidence_id=evidence_id, recorded_at=recorded_at,
            source=run.method_version,
        )
        self.run_repository.record_used_probe(UsedProbe(
            run_id=run_id, probe_id=probe.probe_id, claim_id="CC3",
            gap_type=gap.gap_type, used_at=recorded_at,
        ))
        self.repository.add_evidence(update.evidence)
        self.repository.link_evidence(ClaimEvidenceLink(
            case_id=run.case_id, claim_id="CC3",
            evidence_id=update.evidence.evidence_id,
            rationale="Targeted independent verification evidence for EG-T3.",
        ))
        self.repository.append_evidence_state(update.state_record)

        has_unused = ProbeSelector().select(
            gap_type=gap.gap_type, claim_id="CC3",
            probes=cc3_development_probes(),
            used_probe_ids=self.run_repository.used_probe_ids(run_id),
        ).selected_probe is not None
        decision = StopRule().decide([
            ClaimControlInput(
                "CC3", ClaimApplicability.REQUIRED,
                update.state_record.state, has_unused,
            )
        ])
        self.audit.record_verification_update(
            result_event_id=f"{run_id}-RESULT-01",
            state_event_id=f"{run_id}-STATE-02",
            control_event_id=f"{run_id}-CONTROL-01",
            case_id=run.case_id, claim_id="CC3", gap_type=gap.gap_type,
            probe_id=probe.probe_id, from_state=previous_state,
            update=VerificationUpdate(update.evidence, update.state_record, decision.decision),
            recorded_at=recorded_at,
        )
        if decision.decision != "CONTINUE_VERIFICATION":
            self._finish(run_id, decision.decision, decision.rationale, recorded_at)
        return VerificationUpdate(update.evidence, update.state_record, decision.decision)

    def _finish(self, run_id: str, decision: str, rationale: str, at: datetime) -> None:
        status = (
            VerificationRunStatus.VERIFICATION_COMPLETE
            if decision == "VERIFICATION_COMPLETE"
            else VerificationRunStatus.HUMAN_REVIEW_REQUIRED
        )
        self.run_repository.finish(
            run_id=run_id, status=status, ended_at=at,
            final_decision=decision, final_rationale=rationale,
        )
