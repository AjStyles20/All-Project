import ast
import inspect

import pytest

from p007 import audit, benchmark
from p007.audit import ENGINES, State, b4_contextual
from p007.benchmark import SCENARIOS, Config, generate
from p007.domain import Dataset
from p007.evaluation import score, success_rule


def kinds(report, state=State.GOVERNANCE_SIGNAL):
    return {f.kind for f in report.findings if f.state is state}


@pytest.mark.parametrize("scenario,expected", [
    ("S0", set()), ("S1", {"OPPORTUNITY_GAP"}), ("S2", {"ISSUER_DISPARITY"}), ("S3", set()),
    ("S4", {"PROXY_GAMING"}), ("S7", {"ECONOMY_IMBALANCE"}), ("S8", {"ISSUER_DISPARITY", "PROXY_GAMING"}),
])
def test_contextual_audit_on_each_scenario(scenario, expected):
    dataset, _ = generate(scenario, 7)
    assert kinds(b4_contextual(dataset)) == expected


def test_category_concentration_is_raised_with_its_access_gap():
    found = kinds(b4_contextual(generate("S5", 7)[0]))
    assert "CATEGORY_CONCENTRATION" in found and found <= {"CATEGORY_CONCENTRATION", "OPPORTUNITY_GAP"}


def test_missing_context_gives_insufficient_context_not_an_accusation():
    report = b4_contextual(generate("S6", 7)[0])
    assert report.state is State.INSUFFICIENT_CONTEXT and not kinds(report)
    finding = report.findings[0]
    assert finding.missing_context and finding.non_claims


def test_legitimate_high_issuance_is_not_flagged_by_b4_but_is_by_a_static_threshold():
    dataset, _ = generate("S3", 7)
    assert b4_contextual(dataset).state is State.NO_MATERIAL_SIGNAL
    assert "ISSUER_OUTLIER" in kinds(audit.b1_static(dataset))


def test_every_signal_carries_review_evidence_and_non_claims():
    for scenario in SCENARIOS:
        for f in b4_contextual(generate(scenario, 3)[0]).findings:
            assert f.observations and f.comparison and f.non_claims


def test_no_binary_fair_unfair_output():
    assert {s.value for s in State} == {"NO MATERIAL SIGNAL", "GOVERNANCE SIGNAL", "INSUFFICIENT CONTEXT"}


def test_engines_cannot_see_ground_truth():
    # Pass 004 §12: B4 must not receive the labels. The generator returns them separately,
    # and the audit module does not import the benchmark.
    def imported(module):
        tree = ast.parse(inspect.getsource(module))
        return {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)} | \
               {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}

    assert "p007.benchmark" not in imported(audit) and "p007.audit" not in imported(benchmark)
    assert set(Dataset.__dataclass_fields__) == {"policies", "students", "issuers", "transactions", "catalogue"}


def test_generation_is_reproducible():
    assert generate("S4", 11)[0] == generate("S4", 11)[0]
    assert generate("S4", 11)[0] != generate("S4", 12)[0]


def test_engines_run_on_small_and_empty_inputs():
    tiny, _ = generate("S0", 1, Config(students_per_group=3))
    for engine in ENGINES.values():
        engine(tiny)


def test_scoring_counts_unsupported_claims_and_insufficiency():
    from p007.audit import AuditReport, Finding
    from p007.benchmark import Truth
    signal = Finding("GROUP_DISPARITY", State.GOVERNANCE_SIGNAL, "x", ("o",))
    unsure = Finding("GROUP_DISPARITY", State.INSUFFICIENT_CONTEXT, "x", ("o",))
    cases = [
        (Truth("S6", expect_insufficient=True), AuditReport("X", [signal])),   # accusation where unsure
        (Truth("S6", expect_insufficient=True), AuditReport("X", [unsure])),   # correct
        (Truth("S0"), AuditReport("X", [signal])),                             # false positive
        (Truth("S1", frozenset({"OPPORTUNITY_GAP"})), AuditReport("X", [signal])),  # surfaced
    ]
    m = score(cases)
    assert m["M1_recall"] == 1.0 and m["M2_false_positive_rate"] == 1.0
    assert m["M3_unsupported_claims"] == 2 and m["M4_appropriate_insufficiency"] == 0.5


def test_success_rule_needs_improvement_on_the_combined_objective():
    same = {"M1_recall": 0.5, "M2_false_positive_rate": 0.2, "M3_unsupported_claim_rate": 0.3,
            "M4_appropriate_insufficiency": 0.0}
    recall_bought_with_accusations = {"M1_recall": 0.9, "M2_false_positive_rate": 0.6,
                                      "M3_unsupported_claim_rate": 0.7, "M4_appropriate_insufficiency": 0.0}
    assert success_rule({"B1": same, "B3": same, "B4": recall_bought_with_accusations})["overall"] == "NOT SUPPORTED"
