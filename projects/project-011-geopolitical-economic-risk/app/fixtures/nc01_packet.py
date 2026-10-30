"""NC-01 frozen comparative evidence packet v1.

R2 retrospective reconstruction for the narrow direct Russian urea-dependence
negative-control question. Broader fertilizer effects are explicitly excluded.
"""
from app.domain.evidence_packet import ComparativeEvidencePacket, PacketEvidence, packet_hash

NC01_PACKET_V1 = ComparativeEvidencePacket(
    packet_id="P003-NC01-R2-PKT-v1",
    schema_version="1",
    case_id="P003-NC01-RU-UREA",
    replay_mode="R2",
    information_boundary="2022-02-24 reference boundary; retrospective 2021 trade reconstruction",
    target="Material Nigeria-specific warning based on direct Russian urea import dependence (HS310210)",
    horizon="Immediate-to-near-term warning after 2022-02-24 event boundary",
    evidence=(
        PacketEvidence("NC01-E1","T1",1,"UN Secretary-General statement, 24-Feb-2022","2022-02-24","archival","Global/Nigeria target","EVENT-RU-UA","Authoritative event boundary."),
        PacketEvidence("NC01-E2","T2",2,"WITS/UN Comtrade Nigeria reporter, 2021 HS310210 imports","2021","current archival retrieval","Nigeria","HS310210","Nigeria reporter record shows USD161.82k total urea imports, principally Netherlands, with small India/Turkey values."),
        PacketEvidence("NC01-E3","T2",2,"WITS/UN Comtrade Russia reporter, 2021 HS310210 exports to Nigeria","2021","current archival retrieval","Russia→Nigeria","HS310210","Mirror record shows Russia→Nigeria urea exports of USD8.85k / 27,785kg: non-zero but negligible for the frozen direct-dependence target."),
        PacketEvidence("NC01-E4","T2",2,"WITS/UN Comtrade Nigeria reporter, 2021 HS310210 exports to world","2021","current archival retrieval","Nigeria→World","HS310210","Nigeria exported about USD906.350m / 1.331bn kg of urea in 2021."),
    ),
    counterevidence=(
        "Nigeria reporter and partner mirror urea-import records disagree substantially.",
        "Partner mirror data indicate large non-Russian urea flows to Nigeria, so reporter absence cannot prove total import absence.",
        "Indirect/re-export Russian-origin supply has not been fully excluded.",
        "Global urea-price, natural-gas/feedstock and other-fertilizer channels remain possible.",
    ),
    exclusions=(
        "This packet does not test whether Nigeria was unaffected by the broader fertilizer shock.",
        "It does not treat Russian exposure in potassium sulphate or other fertilizers as urea exposure.",
        "It does not rule out global-price or indirect-trade transmission.",
        "Later Nigerian fertilizer outcomes are excluded from baseline input.",
        "Exact availability/vintage of the reconstructed trade records at 2022-02-24 is not established; packet is R2.",
    ),
)

NC01_PACKET_V1_HASH = packet_hash(NC01_PACKET_V1)
