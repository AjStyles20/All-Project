"""Eligibility (shared by every policy) and policies B0–B4 (specification §6).

A policy returns a Plan from facts available at request time: the response headers, the
object's type, size and image dimensions, and the client's hints. B4 additionally has a
fixed cost model (fitted on pilot objects only) and a verification step.
"""
from dataclasses import dataclass

from p004.transforms import NotTransformable, faithful, image_size

TEXT_TYPES = ("text/", "application/json", "application/javascript", "image/svg+xml")
IMAGE_TYPES = ("image/jpeg", "image/png")


@dataclass(frozen=True)
class Hints:
    accept_webp: bool = True
    accept_gzip: bool = True
    downlink_mbps: float = 10.0
    rtt_ms: float = 50.0
    save_data: bool = False


@dataclass(frozen=True)
class Facts:
    content_type: str
    size: int
    headers: dict
    image_dims: tuple | None = None


@dataclass(frozen=True)
class Plan:
    action: str            # "pass", "abstain", "webp", "gzip"
    quality: int = 0
    max_width: int | None = None
    level: int = 0
    reason: str = ""


def facts_for(content_type: str, body: bytes, headers: dict) -> Facts:
    dims = None
    if content_type in IMAGE_TYPES:
        try:
            dims = image_size(body)
        except NotTransformable:
            dims = None
    return Facts(content_type, len(body), {k.lower(): v for k, v in headers.items()}, dims)


def eligibility(f: Facts, h: Hints) -> Plan | None:
    """Protocol and safety rules every policy obeys. None means 'eligible'."""
    cache_control = f.headers.get("cache-control", "").lower()
    if "no-transform" in cache_control:
        return Plan("abstain", reason="no-transform")
    if f.headers.get("content-encoding"):
        return Plan("abstain", reason="already encoded by the origin")
    if f.content_type in IMAGE_TYPES:
        if f.image_dims is None:
            return Plan("abstain", reason="image unreadable or too large")
        if not h.accept_webp:
            return Plan("pass", reason="client does not accept WebP")
        return None
    if f.content_type.startswith(TEXT_TYPES):
        return None if h.accept_gzip else Plan("pass", reason="client does not accept gzip")
    return Plan("pass", reason="no transformation for this type")


def _kind(f):
    return "image" if f.content_type in IMAGE_TYPES else "text"


def b0(f, h):
    return Plan("pass", reason="pass-through")


def b1(f, h):
    return eligibility(f, h) or (Plan("webp", quality=80) if _kind(f) == "image" else Plan("gzip", level=6))


def b2(f, h):
    return eligibility(f, h) or (Plan("webp", quality=50, max_width=1280) if _kind(f) == "image" else Plan("gzip", level=9))


def _b3_quality(h):
    return 60 if h.downlink_mbps < 2 or h.save_data else 80


def b3(f, h):
    gate = eligibility(f, h)
    if gate:
        return gate
    if _kind(f) == "image":
        return Plan("webp", quality=_b3_quality(h))
    return Plan("gzip", level=6) if f.size > 1024 else Plan("pass", reason="small text")


@dataclass
class CostModel:
    """Fitted on pilot objects only (benchmark.fit). Values are per content type and size."""
    webp_ms_per_mpx: float = 900.0
    gzip_ms_per_mb: float = 60.0
    webp_overhead_ms: float = 5.0
    gzip_overhead_ms: float = 1.0
    ratios: dict = None       # (content_type, bucket, quality or level) -> expected output/input ratio

    @staticmethod
    def bucket(size):
        return "small" if size < 4096 else "large"

    def ratio(self, f, key):
        return (self.ratios or {}).get((f.content_type, self.bucket(f.size), key), 1.0)


class VOC:
    """B4: eligibility, predicted net benefit, verification, recorded decision."""

    def __init__(self, model: CostModel):
        self.model = model

    def __call__(self, f, h):
        gate = eligibility(f, h)
        if gate:
            return gate
        if _kind(f) == "image":
            q = _b3_quality(h)
            mpx = f.image_dims[0] * f.image_dims[1] / 1e6
            cost_ms = self.model.webp_overhead_ms + self.model.webp_ms_per_mpx * mpx
            out = f.size * self.model.ratio(f, q)
            candidate = Plan("webp", quality=q)
        else:
            cost_ms = self.model.gzip_overhead_ms + self.model.gzip_ms_per_mb * f.size / 1e6
            out = f.size * self.model.ratio(f, 6)
            candidate = Plan("gzip", level=6)
        saved_ms = (f.size - out) * 8 / (h.downlink_mbps * 1000)   # bits / (bits per ms)
        if h.save_data and out < 0.95 * f.size:
            return Plan(candidate.action, candidate.quality, None, candidate.level,
                        f"save-data: predicted {out / f.size:.0%} of original size")
        if saved_ms > cost_ms:
            return Plan(candidate.action, candidate.quality, None, candidate.level,
                        f"predicted {saved_ms:.0f} ms saved for {cost_ms:.0f} ms of work")
        return Plan("pass", reason=f"not worth it: predicted {saved_ms:.0f} ms saved for {cost_ms:.0f} ms of work")

    @staticmethod
    def verify(original_size, transformed_size, fidelity_scores=None):
        """Serve the transformed bytes only if they are smaller and faithful enough."""
        if transformed_size >= original_size:
            return False, "result was not smaller"
        if fidelity_scores is not None and not faithful(*fidelity_scores):
            return False, "result below the fidelity floor"
        return True, "verified"


POLICIES = ("B0", "B1", "B2", "B3", "B4")


def make(name, model=None):
    return {"B0": b0, "B1": b1, "B2": b2, "B3": b3}.get(name) or VOC(model or CostModel())
