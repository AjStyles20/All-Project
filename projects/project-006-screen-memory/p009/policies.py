"""Capture policies B0–B4 (docs/PRIVACY_SECURITY_MODEL.md §5).

A policy sees one Observation per tick, in order, and returns the observations to keep.
It never sees task labels or future observations (Pass 003 falsification criterion 7).
B4 may return the *previous* observation: the last frame of a window the user just left.
"""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Observation:
    seq: int
    t: float                 # seconds
    app: str
    title: str
    excluded: bool
    seconds_since_input: float
    signature: tuple = ()    # 16x16 grayscale thumbnail, 0-255; empty when no image was taken
    size_bytes: int = 0      # size the stored image would have

    @property
    def window(self):
        return (self.app, self.title)


def change(a: tuple, b: tuple) -> float:
    """Mean absolute difference of two signatures, 0..1."""
    if not a or not b or len(a) != len(b):
        return 1.0
    return sum(abs(x - y) for x, y in zip(a, b)) / (255 * len(a))


class Interval:
    def __init__(self, seconds, name):
        self.seconds, self.name, self.last = seconds, name, None

    def observe(self, obs):
        if self.last is None or obs.t - self.last >= self.seconds:
            self.last = obs.t
            return [obs]
        return []


class VisualChange:
    name = "B2"

    def __init__(self, threshold=0.08):
        self.threshold, self.last = threshold, None

    def observe(self, obs):
        if self.last is None or change(obs.signature, self.last.signature) > self.threshold:
            self.last = obs
            return [obs]
        return []


class EventTriggered:
    name = "B3"
    TYPING_PAUSE = 2.0
    FALLBACK = 60.0

    def __init__(self):
        self.prev = None
        self.last_kept_t = None

    def _triggered(self, obs):
        prev = self.prev
        if prev is None or obs.window != prev.window:
            return True
        # Input stopped about TYPING_PAUSE seconds ago: the user just finished something.
        if prev.seconds_since_input < self.TYPING_PAUSE <= obs.seconds_since_input:
            return True
        return self.last_kept_t is None or obs.t - self.last_kept_t >= self.FALLBACK

    def observe(self, obs):
        keep = [obs] if self._triggered(obs) else []
        if keep:
            self.last_kept_t = obs.t
        self.prev = obs
        return keep


@dataclass
class Selective(EventTriggered):
    """B4: event-triggered, minus near-duplicates of the same window, never excluded windows,
    plus the last frame of a window when the user leaves it."""
    duplicate_threshold: float = 0.03
    name: str = "B4"
    prev: Observation | None = None
    last_kept_t: float | None = None
    last_kept_by_window: dict = field(default_factory=dict)

    def observe(self, obs):
        kept = []
        prev = self.prev
        if prev is not None and prev.window != obs.window and not prev.excluded:
            last = self.last_kept_by_window.get(prev.window)
            if last is None or (last.seq != prev.seq and change(prev.signature, last.signature) > self.duplicate_threshold):
                kept.append(prev)
        if not obs.excluded and self._triggered(obs):
            last = self.last_kept_by_window.get(obs.window)
            if last is None or change(obs.signature, last.signature) > self.duplicate_threshold:
                kept.append(obs)
            # A trigger resets the fallback clock even when the image was a duplicate.
            self.last_kept_t = obs.t
        for k in kept:
            self.last_kept_by_window[k.window] = k
        self.prev = obs
        return kept


def make(name: str):
    return {
        "B0": lambda: Interval(2.0, "B0"),
        "B1": lambda: Interval(30.0, "B1"),
        "B2": VisualChange,
        "B3": EventTriggered,
        "B4": Selective,
    }[name]()


POLICIES = ("B0", "B1", "B2", "B3", "B4")
