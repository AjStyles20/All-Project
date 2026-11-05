"""The capture loop. Platform probes are injected so the logic is testable anywhere.

Each tick: skip if paused, locked or idle; skip (and count) excluded windows before any
image is taken; otherwise take the foreground window image, let policy B4 decide, and store
what it keeps. Only the current and previous images are ever held in memory.
"""
import threading
import time

from p009.exclusions import Exclusions
from p009.policies import Observation, make

IDLE_AFTER = 120.0


class Recorder:
    def __init__(self, store, probes, exclusions=None, policy="B4", ocr=None, clock=time.time):
        self.store = store
        self.probes = probes
        self.exclusions = exclusions or Exclusions()
        self.policy = make(policy)
        self.ocr = ocr
        self.clock = clock
        self.paused = False
        self.seq = 0
        self.previous = None   # (Observation, image) of the last tick
        self.lock = threading.Lock()
        self.status = "starting"

    def pause(self):
        with self.lock:
            self.paused = True
            # Pausing drops the buffered frame too, so nothing from before the pause is kept later.
            self.previous = None
            self.status = "paused"

    def resume(self):
        with self.lock:
            self.paused = False
            self.status = "recording"

    def tick(self):
        with self.lock:
            if self.paused:
                return []
            if self.probes.locked() or self.probes.seconds_since_input() > IDLE_AFTER:
                self.status = "idle"
                return self._flush()
            window = self.probes.foreground()
            if window is None:
                return []
            program, title, rect = window
            now = self.clock()
            self.seq += 1
            if self.exclusions.excluded(program, title):
                self.store.count_skip("excluded")
                obs = Observation(self.seq, now, "excluded", "", True, self.probes.seconds_since_input())
                return self._decide(obs, None)
            image = self.probes.capture(rect)
            if image is None:
                return []
            self.status = "recording"
            obs = Observation(self.seq, now, program, title, False, self.probes.seconds_since_input(),
                              self.probes.signature(image))
            return self._decide(obs, image)

    def _decide(self, obs, image):
        kept_ids = []
        for keep in self.policy.observe(obs):
            if keep.excluded:
                continue
            source = image if keep is obs else (self.previous[1] if self.previous and self.previous[0] is keep else None)
            if source is not None:
                kept_ids.append(self._save(keep, source, departure=keep is not obs))
        self.previous = (obs, image)
        return kept_ids

    def _flush(self):
        # Idle or locked: drop the buffered frame. Whatever was kept at the last trigger stays.
        self.previous = None
        return []

    def _save(self, obs, image, departure):
        text = ""
        if self.ocr is not None:
            try:
                text = self.ocr(image) or ""
            except Exception:
                text = ""
        return self.store.add(self.probes.encode(image), obs.app, obs.title, obs.t, text, departure)

    def run(self, stop: threading.Event, interval=1.0):
        self.store.enforce_limits()
        last_cleanup = time.monotonic()
        self.status = "recording"
        while not stop.is_set():
            self.tick()
            if time.monotonic() - last_cleanup > 3600:
                self.store.enforce_limits()
                last_cleanup = time.monotonic()
            stop.wait(interval)
