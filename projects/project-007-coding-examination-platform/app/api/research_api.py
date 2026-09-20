"""Minimal FastAPI surface for P001 research inspection.

The API is read-only at M7: it does not create evidence, change method outputs,
or perform consequential assessment decisions.
"""
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse

from app.persistence.database import Database
from app.persistence.audit_repository import AuditRepository
from app.persistence.experiment_observation_repository import ExperimentObservationRepository
from app.persistence.experiment_run_repository import ExperimentRunRepository
from app.domain.enums import EvidenceState
from app.services.experiment_export import ExperimentExporter
from app.services.experiment_record import IndependentReferenceJudgment
from app.services.research_interface import ResearchInterface


class ReferenceJudgmentInput(BaseModel):
    assessor_id: str = Field(min_length=1)
    state: EvidenceState
    rationale: str = Field(min_length=1)
    rubric_version: str = Field(min_length=1)


def create_research_app(database_path: str) -> FastAPI:
    database = Database(database_path)
    database.initialize()
    interface = ResearchInterface(
        ExperimentRunRepository(database),
        ExperimentObservationRepository(database),
    )
    exporter = ExperimentExporter(interface)
    audits = AuditRepository(database)
    app = FastAPI(title="P001 EGPCV Research API", version="0.1.0")

    @app.get("/health")
    def health():
        return {"status": "ok", "scope": "research-interface"}

    @app.get("/research/experiments/{experiment_run_id}")
    def inspect_experiment(experiment_run_id: str):
        try:
            return exporter.as_dict(experiment_run_id)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.post("/research/experiments/{experiment_run_id}/reference", status_code=201)
    def record_reference(experiment_run_id: str, payload: ReferenceJudgmentInput):
        run = interface.runs.get(experiment_run_id)
        if run is None:
            raise HTTPException(status_code=404, detail="Unknown experiment run.")
        reference = IndependentReferenceJudgment(
            assessor_id=payload.assessor_id,
            claim_id=run.claim_id,
            state=payload.state,
            rationale=payload.rationale,
            rubric_version=payload.rubric_version,
        )
        try:
            interface.observations.add_reference(
                experiment_run_id, reference, datetime.now(timezone.utc)
            )
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        except Exception as exc:
            # The persistence layer enforces one immutable reference per run.
            if "UNIQUE constraint failed" in str(exc):
                raise HTTPException(
                    status_code=409,
                    detail="Independent reference already exists for this experiment.",
                ) from exc
            raise
        return {
            "experiment_run_id": experiment_run_id,
            "claim_id": run.claim_id,
            "assessor_id": payload.assessor_id,
            "state": payload.state.value,
            "rubric_version": payload.rubric_version,
        }

    @app.get("/research/experiments/{experiment_run_id}/audit")
    def experiment_audit(experiment_run_id: str):
        try:
            view = interface.inspect_experiment(experiment_run_id)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        events = audits.list_for_case(view.case_id)
        return {
            "experiment_run_id": experiment_run_id,
            "case_id": view.case_id,
            "events": [
                {
                    "event_id": event.event_id,
                    "event_type": event.event_type.value,
                    "recorded_at": event.recorded_at.isoformat(),
                    "actor_type": event.actor_type,
                    "rationale": event.rationale,
                    "claim_id": event.claim_id,
                    "gap_type": event.gap_type,
                    "probe_id": event.probe_id,
                    "evidence_id": event.evidence_id,
                    "from_state": event.from_state,
                    "to_state": event.to_state,
                    "decision": event.decision,
                    "method_version": event.method_version,
                }
                for event in events
                if event.claim_id in (None, view.claim_id)
            ],
        }

    @app.get("/research/experiments/{experiment_run_id}/export")
    def export_experiment(experiment_run_id: str):
        try:
            return JSONResponse(content=exporter.as_dict(experiment_run_id))
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    return app
