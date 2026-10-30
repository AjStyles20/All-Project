import pytest
from dataclasses import replace
from app.domain.b2_run_record import B2RunRecord, AtomicClaim, b2_run_hash, validate_claims


def run():
    return B2RunRecord("B2-A-001","PKT-A","abc","provider","model","version","2026-09-20T00:00:00Z","sys","user","0","", "Nigeria may face higher wheat costs.")


def test_b2_run_hash_reproducible_and_response_sensitive():
    r=run()
    assert b2_run_hash(r)==b2_run_hash(r)
    assert b2_run_hash(r)!=b2_run_hash(replace(r,raw_response="changed"))


def test_atomic_claim_must_trace_to_same_run_and_preserved_span():
    r=run()
    validate_claims(r,(AtomicClaim("C1",r.run_id,"Nigeria may face higher wheat costs.","directional","Nigeria may face higher wheat costs."),))
    with pytest.raises(ValueError):
        validate_claims(r,(AtomicClaim("C2","other","x","directional",""),))
    with pytest.raises(ValueError):
        validate_claims(r,(AtomicClaim("C3",r.run_id,"invented","directional","not in response"),))


def test_duplicate_claim_ids_rejected():
    r=run(); c=AtomicClaim("C1",r.run_id,"x","other","")
    with pytest.raises(ValueError):
        validate_claims(r,(c,c))
