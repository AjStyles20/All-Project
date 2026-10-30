from app.persistence.database import Database
from app.persistence.repositories import P001Repository
from app.research.pilot_cases import (
    PILOT_CORPUS_VERSION, case_pilot_001, case_pilot_003, load_bundle,
)


def test_case_pilot_001_loads_with_frozen_provenance(tmp_path):
    db = Database(tmp_path / "pilot.db")
    db.initialize()
    repo = P001Repository(db)
    bundle = case_pilot_001()
    load_bundle(repo, bundle)

    assert bundle.corpus_version == PILOT_CORPUS_VERSION
    evidence = repo.get_evidence_for_claim("CASE-PILOT-001", "CC3")
    assert [e.evidence_id for e in evidence] == ["P001-EV-A1", "P001-EV-X1"]
    assert {e.source_type for e in evidence} == {
        "constructed_pilot_artifact", "constructed_reference_execution"
    }
    assert all("student" not in e.source_type for e in evidence)


def test_case_pilot_003_remains_explicitly_constructed(tmp_path):
    db = Database(tmp_path / "pilot.db")
    db.initialize()
    repo = P001Repository(db)
    bundle = case_pilot_003()
    load_bundle(repo, bundle)

    evidence = repo.get_evidence_for_claim("CASE-PILOT-003", "CC3")
    assert len(evidence) == 1
    assert evidence[0].source_type == "constructed_independent_response"
    assert "assessor may disagree" in bundle.construction_expectation
