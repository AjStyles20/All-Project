"""Minimal FastAPI surface for P001 research inspection.

The API is read-only at M7: it does not create evidence, change method outputs,
or perform consequential assessment decisions.
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.persistence.database import Database
from app.persistence.experiment_observation_repository import ExperimentObservationRepository
from app.persistence.experiment_run_repository import ExperimentRunRepository
from app.services.experiment_export import ExperimentExporter
from app.services.research_interface import ResearchInterface


def create_research_app(database_path: str) -> FastAPI:
    database = Database(database_path)
    database.initialize()
    interface = ResearchInterface(
        ExperimentRunRepository(database),
        ExperimentObservationRepository(database),
    )
    exporter = ExperimentExporter(interface)
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

    @app.get("/research/experiments/{experiment_run_id}/export")
    def export_experiment(experiment_run_id: str):
        try:
            return JSONResponse(content=exporter.as_dict(experiment_run_id))
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    return app
