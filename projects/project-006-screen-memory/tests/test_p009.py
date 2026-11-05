import time

import pytest
from fastapi.testclient import TestClient

from p009.api import create_app
from p009.exclusions import Exclusions
from p009.policies import Observation, make
from p009.recorder import IDLE_AFTER, Recorder
from p009.simulate import evaluate, generate, proxy_rule
from p009.store import DAY, Store


class FakeProtector:
    """Reversible stand-in for DPAPI that makes it obvious if plaintext reaches disk."""
    def protect(self, data):
        return b"SEALED" + bytes(b ^ 0x5A for b in data)

    def unprotect(self, data):
        assert data.startswith(b"SEALED")
        return bytes(b ^ 0x5A for b in data[6:])


class FakeProbes:
    def __init__(self):
        self.window = ("code.exe", "main.py - VS Code", (0, 0, 800, 600))
        self.image = 0
        self.idle = 0.0
        self.is_locked = False
        self.captures = 0

    def foreground(self):
        return self.window

    def seconds_since_input(self):
        return self.idle

    def locked(self):
        return self.is_locked

    def capture(self, rect):
        self.captures += 1
        return self.image

    def signature(self, image):
        return tuple([image % 256] * 256)

    def encode(self, image):
        return f"image-{image}".encode()


def store(tmp_path, **kw):
    return Store(tmp_path / "data", FakeProtector(), **kw)


def obs(seq, window=("a.exe", "A"), sig=0, idle=0.0, excluded=False):
    return Observation(seq, float(seq), window[0], window[1], excluded, idle, tuple([sig] * 256), 1000)


# ---------- exclusions ----------

@pytest.mark.parametrize("program,title,expected", [
    ("KeePassXC.exe", "Database", True),
    ("chrome.exe", "Online Banking - Chrome", True),
    ("msedge.exe", "New InPrivate tab - Microsoft Edge", True),
    ("chrome.exe", "Login | Example", True),
    ("chrome.exe", "My blogging tips - Chrome", False),
    ("code.exe", "bankruptcy_notes.md", False),
    ("code.exe", "main.py", False),
])
def test_exclusions(program, title, expected):
    assert Exclusions().excluded(program, title) is expected


def test_user_added_exclusions():
    assert Exclusions(extra_title_words=["salary"]).excluded("excel.exe", "Salary review.xlsx")


# ---------- policies ----------

def test_dense_and_sparse_intervals():
    b0, b1 = make("B0"), make("B1")
    kept0 = sum(len(b0.observe(obs(i))) for i in range(60))
    kept1 = sum(len(b1.observe(obs(i))) for i in range(60))
    assert kept0 == 30 and kept1 == 2


def test_b4_never_keeps_excluded_windows_and_keeps_the_last_view_on_leaving():
    b4 = make("B4")
    assert b4.observe(obs(1, sig=10)) == [obs(1, sig=10)]
    for i in range(2, 20):
        b4.observe(obs(i, sig=10 + i * 5))          # typing changes the window
    kept = b4.observe(obs(20, window=("keepass.exe", "x"), excluded=True))
    assert [k.seq for k in kept] == [19]            # the "where was I" frame, not the password manager
    assert b4.observe(obs(21, window=("keepass.exe", "x"), excluded=True)) == []


def test_b4_skips_near_duplicates():
    b4 = make("B4")
    b4.observe(obs(1, sig=10))
    b4.observe(obs(2, window=("b.exe", "B"), sig=50))
    assert b4.observe(obs(3, sig=10)) == []         # back to A, looks the same as last time


def test_policies_see_no_future():
    # Same prefix, different futures: identical decisions on the prefix.
    a = [obs(i, sig=i) for i in range(30)]
    b = a[:15] + [obs(i, window=("z.exe", "Z"), sig=200) for i in range(15, 30)]
    for name in ("B0", "B1", "B2", "B3", "B4"):
        pa, pb = make(name), make(name)
        assert [pa.observe(o) for o in a[:15]] == [pb.observe(o) for o in b[:15]]


# ---------- store ----------

def test_images_are_encrypted_on_disk(tmp_path):
    s = store(tmp_path)
    frame_id = s.add(b"secret pixels", "code.exe", "t", time.time())
    raw = (s.images / f"{frame_id}.bin").read_bytes()
    assert b"secret pixels" not in raw and s.image(frame_id) == b"secret pixels"


def test_retention_and_storage_cap(tmp_path):
    s = store(tmp_path, retention_days=7, max_bytes=50)
    now = time.time()
    s.add(b"x" * 10, "a", "old", now - 8 * DAY)
    for i in range(5):
        s.add(b"y" * 10, "a", f"new{i}", now - i)
    removed = s.enforce_limits(now)
    titles = {r["title"] for r in s.search()}
    assert "old" not in titles and removed >= 1
    assert s.stats()["bytes"] <= 50


def test_delete_recent_and_all(tmp_path):
    s = store(tmp_path)
    now = time.time()
    s.add(b"1", "a", "earlier", now - 3600)
    s.add(b"2", "a", "just now", now - 60)
    assert s.delete_since(15 * 60, now) == 1
    assert [r["title"] for r in s.search()] == ["earlier"]
    s.add(b"3", "a", "x", now)
    assert s.delete_all() == 2 and s.search() == [] and not list(s.images.glob("*"))


def test_image_ids_cannot_escape_the_folder(tmp_path):
    s = store(tmp_path)
    assert s.image("../../secret") is None and s.delete("../x") == 0


def test_search_treats_wildcards_literally(tmp_path):
    s = store(tmp_path)
    s.add(b"1", "a", "100% done", time.time())
    s.add(b"2", "a", "other", time.time())
    assert [r["title"] for r in s.search("%")] == ["100% done"]


# ---------- recorder ----------

def recorder(tmp_path):
    probes = FakeProbes()
    return Recorder(store(tmp_path), probes, clock=lambda: 1000.0), probes


def test_excluded_window_is_never_captured_or_named(tmp_path):
    rec, probes = recorder(tmp_path)
    probes.window = ("bitwarden.exe", "Vault", (0, 0, 800, 600))
    rec.tick()
    assert probes.captures == 0 and rec.store.search() == []
    assert rec.store.stats()["skipped"] == {"excluded": 1}


def test_paused_locked_and_idle_take_nothing(tmp_path):
    rec, probes = recorder(tmp_path)
    rec.pause()
    rec.tick()
    rec.resume()
    probes.is_locked = True
    rec.tick()
    probes.is_locked, probes.idle = False, IDLE_AFTER + 1
    rec.tick()
    assert probes.captures == 0


def test_nothing_buffered_before_a_pause_is_kept_after_it(tmp_path):
    rec, probes = recorder(tmp_path)
    rec.tick()                      # first frame kept
    probes.image = 99
    rec.tick()                      # changed, buffered as "previous"
    rec.pause()
    rec.resume()
    probes.window = ("chrome.exe", "Docs", (0, 0, 800, 600))
    rec.tick()                      # leaving the window would normally keep the buffered frame
    titles = [r["title"] for r in rec.store.search()]
    assert titles.count("main.py - VS Code") == 1


def test_recorder_keeps_frames(tmp_path):
    rec, probes = recorder(tmp_path)
    rec.tick()
    assert len(rec.store.search()) == 1


# ---------- dashboard ----------

def client(tmp_path, rec=None):
    return TestClient(create_app(store(tmp_path), "t0ken", rec), base_url="http://127.0.0.1")


def test_api_requires_the_token(tmp_path):
    c = client(tmp_path)
    assert c.get("/api/status").status_code == 401
    assert c.get("/api/status", headers={"X-Token": "wrong"}).status_code == 401
    assert c.get("/api/status", headers={"X-Token": "t0ken"}).status_code == 200


def test_foreign_host_is_refused_even_with_the_token(tmp_path):
    c = TestClient(create_app(store(tmp_path), "t0ken"), base_url="http://evil.example")
    assert c.get("/api/status", headers={"X-Token": "t0ken"}).status_code == 403
    assert c.get("/").status_code == 403


def test_dashboard_controls(tmp_path):
    rec, probes = recorder(tmp_path)
    c = TestClient(create_app(rec.store, "t0ken", rec), base_url="http://127.0.0.1")
    h = {"X-Token": "t0ken"}
    rec.tick()
    frame = c.get("/api/frames", headers=h).json()[0]
    assert c.get(f"/api/frames/{frame['frame_id']}/image", headers=h).content == b"image-0"
    assert c.post("/api/pause", headers=h).json()["recorder"] == "paused"
    assert c.post("/api/delete-all", headers=h, json={"confirm": "yes"}).status_code == 400
    assert c.post("/api/delete-all", headers=h, json={"confirm": "DELETE"}).json() == {"deleted": 1}
    response = c.get("/", headers=h)
    assert "img-src 'self' blob:" in response.headers["content-security-policy"]
    assert response.headers["cache-control"] == "no-store"


# ---------- simulation ----------

def test_simulation_is_reproducible_and_scored():
    a, b = generate(3), generate(3)
    assert a.observations == b.observations
    result = evaluate(a, "B4")
    assert 0 <= result["resumption_proxy"] <= 1 and result["frames_per_hour"] > 0


def test_listed_sensitive_windows_never_reach_b4():
    session = generate(5)
    listed = {o.seq for o in session.observations if o.excluded}
    policy = make("B4")
    kept = [k for o in session.observations for k in policy.observe(o)]
    assert not any(k.seq in listed for k in kept)


def test_proxy_rule_needs_utility_and_a_saving():
    base = {"resumption_proxy": 1.0, "frames_per_hour": 100, "sensitive_frames": 10}
    worse = {"resumption_proxy": 0.8, "frames_per_hour": 10, "sensitive_frames": 0}
    assert proxy_rule({"B0": base, "B3": base, "B4": worse})["overall"] == "NOT MET"
