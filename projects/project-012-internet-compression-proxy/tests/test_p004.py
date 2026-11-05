import asyncio
import gzip
import logging

import pytest
from fastapi.testclient import TestClient

from p004 import gateway as gw
from p004.corpus import build
from p004.gateway import create_app
from p004.origin import OBJECTS, transport
from p004.policies import VOC, CostModel, Hints, Plan, facts_for, make
from p004.transforms import NotTransformable, image_size

BROWSER = {"accept": "image/webp,image/*", "accept-encoding": "gzip"}
SLOW = {**BROWSER, "downlink": "0.25", "rtt": "300"}


def client(policy="B4", model=None):
    return TestClient(create_app("http://origin.test", policy, model, transport()), base_url="http://127.0.0.1")


# ---------- security invariants S1-S10 ----------

@pytest.mark.parametrize("policy", ["B1", "B2", "B3", "B4"])
def test_s1_no_transform_is_byte_for_byte(policy):
    r = client(policy).get("/c/k7-no-transform.jpg", headers=SLOW)
    assert r.content == OBJECTS["k7-no-transform.jpg"].body and r.headers["content-type"] == "image/jpeg"


def test_s2_private_responses_are_served_fresh_every_time():
    c = client("B1")
    assert c.get("/account").status_code == 401
    r = c.get("/account", headers={**BROWSER, "authorization": "Bearer test"})
    assert r.status_code == 200 and b"balance" in r.content
    # No cache exists: an unauthenticated request after an authenticated one is still refused.
    assert c.get("/account").status_code == 401


@pytest.mark.parametrize("target", ["//evil.example/x", "/c/../../etc/passwd", "/c/%2e%2e/secret", "/c\\x"])
def test_s3_only_plain_origin_paths(target):
    assert client().get(target).status_code in (400, 404)


def test_s3_absolute_form_and_connect_are_refused():
    app = create_app("http://origin.test", "B4", transport=transport())
    results = []

    async def call(method, raw):
        scope = {"type": "http", "method": method, "path": "/", "raw_path": raw, "query_string": b"",
                 "headers": [(b"host", b"127.0.0.1")], "http_version": "1.1", "scheme": "http",
                 "server": ("127.0.0.1", 80), "client": ("127.0.0.1", 1), "root_path": ""}
        sent = []

        async def receive():
            return {"type": "http.request", "body": b"", "more_body": False}

        async def send(message):
            sent.append(message)
        await app(scope, receive, send)
        results.append(next(m["status"] for m in sent if m["type"] == "http.response.start"))

    asyncio.run(call("GET", b"http://169.254.169.254/latest"))
    asyncio.run(call("CONNECT", b"evil.example:443"))
    assert results == [400, 405]


def test_s4_redirects_are_returned_not_followed():
    r = client().get("/redirect", follow_redirects=False)
    assert r.status_code == 302 and r.headers["location"].startswith("http://169.254.169.254")


def test_s5_huge_upstream_body_is_refused():
    assert client().get("/big").status_code == 502


@pytest.mark.parametrize("name", ["k8-huge.png", "k8-broken.jpg"])
def test_s6_s7_hostile_images_pass_through_untouched(name):
    r = client("B2").get(f"/c/{name}", headers=SLOW)
    assert r.status_code == 200 and r.content == OBJECTS[name].body


def test_s8_transformations_time_out(monkeypatch):
    def slow(*args):
        import time
        time.sleep(0.5)
        raise AssertionError("should have timed out")
    monkeypatch.setattr(gw, "TRANSFORM_TIMEOUT", 0.05)
    monkeypatch.setattr(gw, "_apply", slow)
    r = client("B1").get("/c/k4-data.json", headers=BROWSER)
    assert r.status_code == 200 and r.content == OBJECTS["k4-data.json"].body
    assert "FALLBACK" in r.headers["x-optimization"]


def test_s9_logs_hold_no_query_or_credentials(caplog):
    with caplog.at_level(logging.INFO, logger="p004.gateway"):
        client().get("/c/k4-data.json?token=SECRET123", headers={**BROWSER, "authorization": "Bearer SECRET456",
                                                               "cookie": "sid=SECRET789"})
    text = caplog.text
    assert "/c/k4-data.json" in text and "SECRET" not in text


def test_s10_hop_by_hop_headers_are_not_forwarded():
    r = client().get("/echo-headers", headers={"connection": "keep-alive, x-secret", "proxy-authorization": "x",
                                               "te": "trailers", "x-normal": "yes"})
    body = r.text
    assert "x-normal: yes" in body and "proxy-authorization" not in body and "te: " not in body


# ---------- transformations through the gateway ----------

def test_text_is_gzipped_when_accepted_and_decodes_identically():
    r = client("B1").get("/c/k4-site.css", headers=BROWSER)
    assert r.headers["content-encoding"] == "gzip" and r.content == OBJECTS["k4-site.css"].body  # client decodes
    assert "Accept-Encoding" in r.headers["vary"]


def test_b4_skips_work_that_does_not_pay_on_a_fast_link():
    model = CostModel(webp_ms_per_mpx=1300, ratios={("image/png", "large", 80): 0.35})
    r = client("B4", model).get("/c/k2-photo-large.png", headers={**BROWSER, "downlink": "1000", "rtt": "1"})
    assert r.headers["content-type"] == "image/png" and "not worth it" in r.headers["x-optimization"]


def test_b4_transforms_when_the_link_is_slow():
    model = CostModel(webp_ms_per_mpx=1300, ratios={("image/png", "large", 60): 0.3})
    r = client("B4", model).get("/c/k2-photo-large.png", headers=SLOW)
    assert r.headers["content-type"] == "image/webp" and len(r.content) < len(OBJECTS["k2-photo-large.png"].body)


def test_b4_falls_back_when_the_result_is_not_smaller():
    model = CostModel(ratios={("image/png", "small", 60): 0.5})  # wrongly optimistic on purpose
    r = client("B4", model).get("/c/k6-icon.png", headers={**BROWSER, "save-data": "on"})
    assert r.content == OBJECTS["k6-icon.png"].body and "FALLBACK" in r.headers["x-optimization"]


def test_client_without_webp_gets_the_original():
    r = client("B2").get("/c/k2-photo-q95.jpg", headers={"accept": "image/jpeg"})
    assert r.headers["content-type"] == "image/jpeg"


def test_only_get_and_head():
    assert client().post("/c/k4-data.json").status_code == 405


def test_origin_must_be_a_bare_host():
    with pytest.raises(ValueError):
        create_app("http://origin.test/sub")


# ---------- policies and decisions ----------

def test_decisions_are_reproducible_from_recorded_inputs():
    model = CostModel(ratios={("image/jpeg", "large", 60): 0.5})
    objs = build(2)
    for o in objs:
        f = facts_for(o.content_type, o.body, o.headers)
        for h in (Hints(downlink_mbps=0.25), Hints(downlink_mbps=50)):
            assert make("B4", model)(f, h) == make("B4", model)(f, h)


def test_eligibility_is_shared_by_every_transforming_policy():
    o = OBJECTS["k7-no-transform.jpg"]
    f = facts_for(o.content_type, o.body, o.headers)
    assert {make(p)(f, Hints()).action for p in ("B1", "B2", "B3", "B4")} == {"abstain"}


def test_verify():
    assert VOC.verify(100, 120)[0] is False
    assert VOC.verify(100, 50, (25.0, 0.99))[0] is False
    assert VOC.verify(100, 50, (35.0, 0.97))[0] is True


def test_corpus_is_reproducible():
    assert [o.sha256 for o in build(3)] == [o.sha256 for o in build(3)]
    with pytest.raises(NotTransformable):
        image_size(OBJECTS["k8-huge.png"].body)


def test_gzip_output_is_valid():
    from p004.transforms import to_gzip
    data = b"hello " * 1000
    assert gzip.decompress(to_gzip(data, 6)[0]) == data


def test_plan_type():
    assert Plan("pass").action == "pass"


def test_lab_app_loads_the_fitted_cost_model(monkeypatch):
    # Regression: the lab gateway once ran B4 without its model, so it never transformed anything.
    monkeypatch.setenv("P004_ORIGIN", "http://origin.test")
    app = gw.lab_app()
    assert app is not None
    model = CostModel.load(gw.MODEL_PATH)
    assert model.ratios and model.webp_ms_per_mpx > 0
