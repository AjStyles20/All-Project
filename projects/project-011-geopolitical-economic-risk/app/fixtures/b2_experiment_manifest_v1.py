"""Frozen first B2 experiment manifest: Candidate A + NC-01."""
from app.domain.b2_manifest import B2ExperimentManifest, plan_case_runs
from app.fixtures.candidate_a_packet import CANDIDATE_A_PACKET_V1
from app.fixtures.nc01_packet import NC01_PACKET_V1

B2_EXPERIMENT_MANIFEST_V1 = B2ExperimentManifest(
    manifest_id="P003-B2-MANIFEST-v1",
    protocol_version="B2_PROMPT_AND_PACKET_SERIALIZATION_V1",
    runs=(
        *plan_case_runs(CANDIDATE_A_PACKET_V1, "B2-A", 3),
        *plan_case_runs(NC01_PACKET_V1, "B2-NC01", 3),
    ),
)
