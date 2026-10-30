from app.security.passwords import hash_password, verify_password

def test_password_hash_is_salted_and_verifiable():
    first = hash_password("correct horse battery staple", iterations=1_000)
    second = hash_password("correct horse battery staple", iterations=1_000)
    assert first != second
    assert "correct horse battery staple" not in first
    assert verify_password("correct horse battery staple", first)
    assert not verify_password("wrong", first)

def test_malformed_hash_is_rejected():
    assert not verify_password("anything", "not-a-valid-hash")
