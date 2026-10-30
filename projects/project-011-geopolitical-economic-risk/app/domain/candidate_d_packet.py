"""Frozen Comparative Evidence Packet v1 for Candidate D."""
from .evidence_packet import ComparativeEvidencePacket, PacketEvidence

CANDIDATE_D_PACKET_V1 = ComparativeEvidencePacket(
    packet_id="P003-D-R2-PKT-v1", schema_version="1", case_id="P003-D", replay_mode="R2",
    information_boundary="Pre-outcome reconstruction anchored to pre-event institutional mechanism; exact trade-data publication vintage at 2022-02-24 unresolved.",
    target="Nigeria PMS subsidy / fiscal burden",
    horizon="Subsequent months; directional only.",
    evidence=(
        PacketEvidence("D-E1","T1",1,"Authoritative/institutional record of 2022 external energy-price shock","2022","historical","Global","energy/refined-fuel shock","Material external energy-price shock established."),
        PacketEvidence("D-E2","T2",2,"WITS / UN Comtrade Nigeria 2021 trade reconstruction","2021","current retrospective reconstruction","Nigeria","HS271000","Large pre-event non-crude petroleum-product import exposure; broad class is not identical to PMS."),
        PacketEvidence("D-E3","T3",2,"IMF Nigeria pre-event subsidy analysis","2021","pre-event institutional analysis","Nigeria","PMS subsidy","Imported PMS delivery cost above regulated pump price generated implicit subsidy borne through NNPC/Federation Account deductions."),
        PacketEvidence("D-E4","T3",2,"World Bank Nigeria pre-event fiscal analysis","2021","pre-event institutional analysis","Nigeria","PMS/fiscal channel","Subsidy burden and weak crude production documented as limiting fiscal benefit of higher oil prices."),
    ),
    counterevidence=(
        "Higher crude prices can increase gross Nigerian oil/export revenue.",
        "Weak crude production can reduce the offsetting revenue benefit.",
        "Foreign-exchange movements alter naira import costs.",
        "Import and consumption volumes can change.",
        "Regulated-price/subsidy policy can change.",
        "HS271000 is broader than PMS/gasoline.",
        "Subsidy accounting, NNPC deductions, smuggling/leakage and fiscal treatment complicate measured burden.",
    ),
    exclusions=(
        "No exclusive causal attribution to the Russia-Ukraine war.",
        "No numerical subsidy forecast.",
        "No probability forecast.",
        "No claim that all HS271000 imports are PMS.",
        "No T5/T6 eligibility.",
        "Post-boundary outcome observations are excluded from this packet.",
    ),
)
