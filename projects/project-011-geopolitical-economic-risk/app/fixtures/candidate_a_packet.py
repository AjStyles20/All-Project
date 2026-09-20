"""Candidate A frozen comparative evidence packet v1.

R2 retrospective reconstruction. Later outcome observations are intentionally
excluded from this baseline information packet.
"""
from app.domain.evidence_packet import ComparativeEvidencePacket, PacketEvidence, packet_hash

CANDIDATE_A_PACKET_V1 = ComparativeEvidencePacket(
    packet_id="P003-A-R2-PKT-v1",
    schema_version="1",
    case_id="P003-RU-WHEAT-A",
    replay_mode="R2",
    information_boundary="2022-02-24 reference boundary; retrospective archival reconstruction",
    target="Conditional upward pressure on Nigerian wheat-flour and bread/cereal costs",
    horizon="3-6 months after 2022-02-24",
    evidence=(
        PacketEvidence("A-E1","T1",1,"UN Secretary-General statement, 24-Feb-2022","2022-02-24","archival","Global/Nigeria target","EVENT-RU-UA","Russia-Ukraine event boundary."),
        PacketEvidence("A-E2","T1",1,"UN General Assembly resolution ES-11/1, 02-Mar-2022","2022-03-02","archival","Global/Nigeria target","EVENT-RU-UA","Authoritative corroboration after the reference boundary; retained as R2 provenance, not strict R1 input."),
        PacketEvidence("A-E3","T2",2,"UN Comtrade/WITS Nigeria 2021 wheat trade reconstruction","2021","current archival retrieval","Nigeria","HS100110/HS100190","Material Nigerian wheat exposure to Russia/Ukraine reconstructed from 2021 trade records; reporter/mirror asymmetry retained."),
        PacketEvidence("A-E4","T3",2,"USDA/FAS Nigeria Grain and Feed Annual 2022","2022","archival","Nigeria","WHEAT-FLOUR-BREAD","Documents wheat import dependence, milling, global wheat-price/FX pressure, miller price changes and supplier substitution."),
    ),
    counterevidence=(
        "Bread prices were already rising before 24-Feb-2022.",
        "Foreign-exchange scarcity was a material competing cost channel.",
        "Millers diversified/substituted suppliers after the shock.",
        "Freight, energy and logistics could amplify or confound transmission.",
        "Domestic wheat supply is relevant but not fully quantified in this packet.",
        "Inventories, contracts, hedges and policy mitigation remain partly unknown.",
    ),
    exclusions=(
        "No claim of exclusive causal attribution to the war.",
        "No numerical magnitude or probability forecast.",
        "No T5/T6 eligibility.",
        "Later NBS outcome observations are excluded from baseline input.",
        "Exact 24-Feb-2022 availability of the reconstructed Comtrade values is not established; packet is R2.",
    ),
)

CANDIDATE_A_PACKET_V1_HASH = packet_hash(CANDIDATE_A_PACKET_V1)
