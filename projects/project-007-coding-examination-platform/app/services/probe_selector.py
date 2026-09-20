"""Bounded targeted verification selection for P001 B4 EGPCV.

The selector minimizes burden only after filtering to probes that are both
admissible for the evidence gap and potentially sufficient to resolve it.
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
class ProbeSelection:
    gap_type: str
    claim_id: str
    selected_probe: VerificationProbe | None
    decision: str
    rationale: str


class ProbeSelector:
    def select(
        self,
        *,
        gap_type: str,
        claim_id: str,
        probes: list[VerificationProbe],
    ) -> ProbeSelection:
        admissible = [
            probe
            for probe in probes
            if claim_id in probe.applicable_claims and gap_type in probe.gap_types
        ]

        adequate = [
            probe
            for probe in admissible
            if gap_type in probe.potentially_sufficient_gap_types
        ]

        if not adequate:
            return ProbeSelection(
                gap_type=gap_type,
                claim_id=claim_id,
                selected_probe=None,
                decision="HUMAN_REVIEW_REQUIRED",
                rationale=(
                    "No admissible candidate probe is currently classified as "
                    "potentially sufficient to resolve this evidence gap."
                ),
            )

        selected = min(adequate, key=lambda probe: (probe.burden_rank, probe.probe_id))
        return ProbeSelection(
            gap_type=gap_type,
            claim_id=claim_id,
            selected_probe=selected,
            decision="CONTINUE_VERIFICATION",
            rationale=(
                "Selected the lowest-burden probe among candidates that are "
                "admissible and potentially sufficient under the frozen "
                "development probe set."
            ),
        )
