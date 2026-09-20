"""Bounded targeted verification selection for P001 B4 EGPCV.

The selector minimizes burden only after filtering to probes that are both
admissible for the evidence gap and potentially sufficient to resolve it.
Every candidate receives a machine-readable disposition so the bounded-minimum
decision can be audited rather than inferred after the fact.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class VerificationProbe:
    probe_id: str
    name: str
    prompt: str
    probe_type: str
    applicable_claims: frozenset[str]
    gap_types: frozenset[str]
    potentially_sufficient_gap_types: frozenset[str]
    burden_rank: int


@dataclass(frozen=True)
class ProbeCandidateDisposition:
    probe_id: str
    admissible: bool
    potentially_sufficient: bool
    burden_rank: int
    disposition: str
    rationale: str


@dataclass(frozen=True)
class ProbeSelection:
    gap_type: str
    claim_id: str
    selected_probe: VerificationProbe | None
    decision: str
    rationale: str
    candidate_dispositions: tuple[ProbeCandidateDisposition, ...] = ()


class ProbeSelector:
    def select(
        self, *, gap_type: str, claim_id: str, probes: list[VerificationProbe], used_probe_ids: frozenset[str] = frozenset(),
    ) -> ProbeSelection:
        assessed = []
        adequate = []
        for probe in probes:
            if probe.probe_id in used_probe_ids:
                assessed.append((probe, False, False, "REJECTED_ALREADY_USED"))
                continue
            admissible = claim_id in probe.applicable_claims and gap_type in probe.gap_types
            sufficient = admissible and gap_type in probe.potentially_sufficient_gap_types
            if sufficient:
                adequate.append(probe)
            assessed.append((probe, admissible, sufficient, None))

        selected = min(adequate, key=lambda p: (p.burden_rank, p.probe_id)) if adequate else None
        dispositions = []
        for probe, admissible, sufficient, forced_disposition in assessed:
            if forced_disposition == "REJECTED_ALREADY_USED":
                disposition, rationale = "REJECTED_ALREADY_USED", (
                    "Probe was already used in this verification run and is not reused."
                )
            elif not admissible:
                disposition, rationale = "REJECTED_NOT_ADMISSIBLE", (
                    "Probe is not admissible for this claim/gap combination."
                )
            elif not sufficient:
                disposition, rationale = "REJECTED_INSUFFICIENT", (
                    "Probe is admissible but is not classified as potentially sufficient "
                    "for this gap under the frozen development catalogue."
                )
            elif probe.probe_id == selected.probe_id:
                disposition, rationale = "SELECTED", (
                    "Probe is admissible, potentially sufficient, and has the lowest "
                    "burden among adequate candidates under the bounded candidate set."
                )
            else:
                disposition, rationale = "REJECTED_HIGHER_BURDEN", (
                    f"Probe is adequate but burden rank {probe.burden_rank} is higher "
                    f"than selected probe {selected.probe_id} rank {selected.burden_rank}."
                )
            dispositions.append(ProbeCandidateDisposition(
                probe_id=probe.probe_id, admissible=admissible,
                potentially_sufficient=sufficient, burden_rank=probe.burden_rank,
                disposition=disposition, rationale=rationale,
            ))

        if selected is None:
            return ProbeSelection(
                gap_type=gap_type, claim_id=claim_id, selected_probe=None,
                decision="HUMAN_REVIEW_REQUIRED",
                rationale="No admissible candidate probe is currently classified as potentially sufficient to resolve this evidence gap.",
                candidate_dispositions=tuple(dispositions),
            )
        return ProbeSelection(
            gap_type=gap_type, claim_id=claim_id, selected_probe=selected,
            decision="CONTINUE_VERIFICATION",
            rationale="Selected the lowest-burden probe among candidates that are admissible and potentially sufficient under the frozen development probe set.",
            candidate_dispositions=tuple(dispositions),
        )
