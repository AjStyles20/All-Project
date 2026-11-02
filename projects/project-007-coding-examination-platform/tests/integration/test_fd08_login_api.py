from app.services.login_guard import USER_FAILURE_LIMIT
from tests.integration.test_fd07_users_api import setup, sign_in


def bad_login(client, username="lecturer"):
    return client.post("/auth/login", json={"username": username, "password": "wrong-password"})


def test_repeated_failures_get_429_with_retry_after_even_for_the_right_password():
    client, _ = setup()
    for _ in range(USER_FAILURE_LIMIT):
        assert bad_login(client).status_code == 401
    locked = client.post("/auth/login", json={"username": "lecturer", "password": "LecturerPass123"})
    assert locked.status_code == 429 and int(locked.headers["retry-after"]) > 0
    assert "password" not in locked.json()["detail"].split("attempts")[0].lower()


def test_unknown_username_gets_identical_responses():
    client, _ = setup()
    real = bad_login(client, "lecturer")
    fake = bad_login(client, "no-such-person")
    assert (real.status_code, real.json()) == (fake.status_code, fake.json())
    for _ in range(USER_FAILURE_LIMIT - 1):
        real, fake = bad_login(client, "lecturer"), bad_login(client, "no-such-person")
    assert real.status_code == fake.status_code == 401
    assert bad_login(client, "lecturer").status_code == bad_login(client, "no-such-person").status_code == 429


def test_lock_does_not_end_an_existing_session_and_is_audited():
    client, repo = setup()
    lecturer = sign_in(client, "lecturer", "LecturerPass123")
    admin = sign_in(client, "root", "AdminPassword123")
    for _ in range(USER_FAILURE_LIMIT):
        bad_login(client)
    assert client.get("/examiner/ping", headers=lecturer).status_code == 200
    audit = client.get("/admin/audit", headers=admin).json()
    assert audit[0]["action"] == "LOGIN_LOCKED" and audit[0]["target_username"] == "lecturer"
    assert audit[0]["actor_user_id"] is None


def test_administrator_clears_a_lock_and_only_administrators_can():
    client, _ = setup()
    admin = sign_in(client, "root", "AdminPassword123")
    lecturer = sign_in(client, "lecturer", "LecturerPass123")
    for _ in range(USER_FAILURE_LIMIT):
        bad_login(client)
    assert client.post("/admin/users/lect-1/clear-login-lock", headers=lecturer).status_code == 403
    assert client.get("/admin/audit", headers=lecturer).status_code == 403
    assert client.post("/admin/users/lect-1/clear-login-lock", headers=admin).json() == {"cleared": 1}
    assert client.post("/auth/login", json={"username": "lecturer", "password": "LecturerPass123"}).status_code == 200


def test_forged_forwarded_header_does_not_dodge_the_limit():
    client, _ = setup()
    for n in range(USER_FAILURE_LIMIT):
        client.post("/auth/login", json={"username": "lecturer", "password": "wrong"},
                    headers={"X-Forwarded-For": f"10.9.9.{n}"})
    assert bad_login(client).status_code == 429


def test_oversized_login_input_is_rejected_before_hashing():
    client, _ = setup()
    assert client.post("/auth/login", json={"username": "lecturer", "password": "x" * 1025}).status_code == 422


def test_parallel_wrong_passwords_through_the_api_stop_at_the_limit():
    # Regression for the race found in browser testing (TE-018): real threads, real hashing.
    from concurrent.futures import ThreadPoolExecutor

    client, _ = setup()
    with ThreadPoolExecutor(max_workers=12) as pool:
        codes = list(pool.map(lambda _: bad_login(client).status_code, range(12)))
    assert codes.count(401) == USER_FAILURE_LIMIT and codes.count(429) == 12 - USER_FAILURE_LIMIT
    right = client.post("/auth/login", json={"username": "lecturer", "password": "LecturerPass123"})
    assert right.status_code == 429
