import pytest
from dataclasses import replace
from app.domain.b2_execution_gate import prepare_run
from app.fixtures.b2_experiment_manifest_v1 import B2_EXPERIMENT_MANIFEST_V1
from app.fixtures.candidate_a_packet import CANDIDATE_A_PACKET_V1
from app.fixtures.nc01_packet import NC01_PACKET_V1


def test_all_six_predeclared_runs_prepare_against_frozen_packets():
    packets={"P003-A-R2-PKT-v1":CANDIDATE_A_PACKET_V1,"P003-NC01-R2-PKT-v1":NC01_PACKET_V1}
    for planned in B2_EXPERIMENT_MANIFEST_V1.runs:
        p=prepare_run(B2_EXPERIMENT_MANIFEST_V1,planned.run_id,packets[planned.packet_id])
        assert p.packet_hash == planned.packet_hash
        assert p.system_prompt and p.user_prompt


def test_unplanned_run_is_rejected():
    with pytest.raises(ValueError):
        prepare_run(B2_EXPERIMENT_MANIFEST_V1,"B2-A-999",CANDIDATE_A_PACKET_V1)


def test_packet_mutation_after_manifest_is_rejected():
    changed=replace(CANDIDATE_A_PACKET_V1,target=CANDIDATE_A_PACKET_V1.target+" changed")
    with pytest.raises(ValueError):
        prepare_run(B2_EXPERIMENT_MANIFEST_V1,"B2-A-001",changed)
