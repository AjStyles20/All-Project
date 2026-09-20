"""Prospective B2 second-wave manifest.

Created after Candidate D packetization and before any Candidate D B2 output.
It does not alter first-wave manifest P003-B2-MANIFEST-v1.
"""
from app.domain.b2_manifest import B2ExperimentManifest, plan_case_runs
from app.domain.candidate_d_packet import CANDIDATE_D_PACKET_V1

P003_B2_SECOND_WAVE_MANIFEST_V1 = B2ExperimentManifest(
    manifest_id="P003-B2-SECOND-WAVE-MANIFEST-v1",
    protocol_version="B2-v1",
    runs=plan_case_runs(CANDIDATE_D_PACKET_V1, "B2-D", 3),
)
