import pytest
from app.domain.b2_manifest import B2ExperimentManifest, PlannedB2Run, plan_case_runs, validate_manifest
from app.fixtures.b2_experiment_manifest_v1 import B2_EXPERIMENT_MANIFEST_V1
from app.fixtures.candidate_a_packet import CANDIDATE_A_PACKET_V1
from app.fixtures.nc01_packet import NC01_PACKET_V1


def test_manifest_predeclares_three_runs_per_first_case():
    m=B2_EXPERIMENT_MANIFEST_V1
    assert [r.run_id for r in m.runs] == [
        "B2-A-001","B2-A-002","B2-A-003",
        "B2-NC01-001","B2-NC01-002","B2-NC01-003",
    ]
    validate_manifest(m)


def test_manifest_binds_runs_to_current_packet_hashes():
    m=B2_EXPERIMENT_MANIFEST_V1
    a=plan_case_runs(CANDIDATE_A_PACKET_V1,"B2-A",3)
    n=plan_case_runs(NC01_PACKET_V1,"B2-NC01",3)
    assert m.runs == a+n


def test_duplicate_run_ids_are_rejected():
    r=PlannedB2Run("X","P","H",1)
    with pytest.raises(ValueError):
        validate_manifest(B2ExperimentManifest("M","V",(r,r)))
