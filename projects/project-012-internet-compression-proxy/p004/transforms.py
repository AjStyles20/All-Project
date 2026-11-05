"""Conventional transformations and fidelity measures (specification §3).

Image decoding is bounded: 40 megapixels at most, decompression bombs refused, and any
decoder error means "do not transform" (S6, S7).
"""
import gzip
import io
import math
import time
import warnings

from PIL import Image, ImageChops, ImageStat

MAX_PIXELS = 40_000_000
Image.MAX_IMAGE_PIXELS = MAX_PIXELS

PSNR_FLOOR = 30.0
SSIM_FLOOR = 0.90


class NotTransformable(Exception):
    pass


def image_size(body: bytes):
    """(width, height) from the header only, or raise NotTransformable."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(body)) as img:
                w, h = img.size
    except Exception as exc:
        raise NotTransformable(f"unreadable image: {type(exc).__name__}") from exc
    if w * h > MAX_PIXELS:
        raise NotTransformable("image too large")
    return w, h


def _decode(body):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            img = Image.open(io.BytesIO(body))
            img.load()
            return img
    except Exception as exc:
        raise NotTransformable(f"cannot decode: {type(exc).__name__}") from exc


def to_webp(body: bytes, quality: int, max_width: int | None = None):
    """Returns (bytes, milliseconds)."""
    started = time.perf_counter()
    img = _decode(body)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
    if max_width and img.width > max_width:
        img = img.resize((max_width, round(img.height * max_width / img.width)), Image.LANCZOS)
    out = io.BytesIO()
    img.save(out, format="WEBP", quality=quality, method=4)
    return out.getvalue(), (time.perf_counter() - started) * 1000


def to_gzip(body: bytes, level: int):
    started = time.perf_counter()
    data = gzip.compress(body, compresslevel=level, mtime=0)
    return data, (time.perf_counter() - started) * 1000


def fidelity(original: bytes, transformed: bytes):
    """(PSNR in dB, SSIM on a 128-pixel greyscale thumbnail). The original is resized to the
    transformed size first, so downscaling itself is not counted as loss."""
    a = _decode(original).convert("RGB")
    b = _decode(transformed).convert("RGB")
    if a.size != b.size:
        a = a.resize(b.size, Image.LANCZOS)
    diff = ImageChops.difference(a, b)
    mse = sum(ImageStat.Stat(diff).sum2) / (a.width * a.height * 3)
    psnr = float("inf") if mse == 0 else 10 * math.log10(255 ** 2 / mse)
    return psnr, _ssim(a, b)


def _ssim(a, b, size=128, window=8):
    ga = a.convert("L").resize((size, size)).tobytes()
    gb = b.convert("L").resize((size, size)).tobytes()
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    scores = []
    for y in range(0, size, window):
        for x in range(0, size, window):
            pa = [ga[(y + j) * size + x + i] for j in range(window) for i in range(window)]
            pb = [gb[(y + j) * size + x + i] for j in range(window) for i in range(window)]
            n = len(pa)
            ma, mb = sum(pa) / n, sum(pb) / n
            va = sum((p - ma) ** 2 for p in pa) / n
            vb = sum((p - mb) ** 2 for p in pb) / n
            cov = sum((p - ma) * (q - mb) for p, q in zip(pa, pb)) / n
            scores.append(((2 * ma * mb + c1) * (2 * cov + c2)) / ((ma ** 2 + mb ** 2 + c1) * (va + vb + c2)))
    return sum(scores) / len(scores)


def faithful(psnr, ssim):
    return psnr >= PSNR_FLOOR and ssim >= SSIM_FLOOR
