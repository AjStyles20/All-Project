from dataclasses import dataclass
from app.domain.blinded_review import make_blind_id, blind_claims

@dataclass(frozen=True)
class C:
    claim_id: str
    text: str
    claim_type: str

def test_blind_id_is_deterministic_and_hides_original_id():
    a=make_blind_id("frozen-review-salt","B2-A-001-C01")
    b=make_blind_id("frozen-review-salt","B2-A-001-C01")
    assert a==b
    assert "B2-A-001" not in a

def test_blinded_claim_exposes_no_baseline_or_run_field():
    out=blind_claims((C("B2-A-001-C01","Nigeria faces upward cost pressure.","scenario"),),"salt-v1")[0]
    assert out.claim_text=="Nigeria faces upward cost pressure."
    assert not hasattr(out,"run_id")
    assert not hasattr(out,"baseline")

def test_blinding_rejects_empty_identity_inputs():
    import pytest
    with pytest.raises(ValueError):
        make_blind_id("","claim")
