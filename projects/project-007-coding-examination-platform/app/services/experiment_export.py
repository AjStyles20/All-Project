"""Deterministic export of the bounded P001 comparative experiment record."""
from dataclasses import asdict
import json

from app.services.research_interface import ResearchInterface


class ExperimentExporter:
    def __init__(self, interface: ResearchInterface):
        self.interface=interface

    def as_dict(self, experiment_run_id: str) -> dict:
        view=self.interface.inspect_experiment(experiment_run_id)
        data=asdict(view)
        data["methods"]=[
            {
                **method,
                "state": method["state"].value,
                "evidence_ids": list(method["evidence_ids"]),
                "complexity": list(method["complexity"]),
            }
            for method in data["methods"]
        ]
        data["reference_state"]=(
            data["reference_state"].value if data["reference_state"] is not None else None
        )
        data["missing"]=list(data["missing"])
        return data

    def as_json(self, experiment_run_id: str) -> str:
        return json.dumps(
            self.as_dict(experiment_run_id),
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )
