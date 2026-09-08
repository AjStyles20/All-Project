from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from typing import Protocol, Sequence


MAX_VECTOR_DIMENSION = 4096


class EmbeddingProvider(Protocol):
    provider_name: str
    model_name: str
    model_version: str | None

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Return one finite numeric vector per input text."""


@dataclass(frozen=True)
class EmbeddingIdentity:
    provider: str
    model: str
    version: str | None = None


def validate_vector(vector: Sequence[float], *, expected_dimension: int | None = None) -> list[float]:
    values = [float(value) for value in vector]
    if not values:
        raise ValueError("embedding vector cannot be empty")
    if len(values) > MAX_VECTOR_DIMENSION:
        raise ValueError("embedding vector exceeds maximum supported dimension")
    if expected_dimension is not None and len(values) != expected_dimension:
        raise ValueError("embedding vector dimension mismatch")
    if any(not isfinite(value) for value in values):
        raise ValueError("embedding vector contains non-finite values")
    return values


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    a = validate_vector(left)
    b = validate_vector(right, expected_dimension=len(a))
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sqrt(sum(x * x for x in a))
    norm_b = sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    score = dot / (norm_a * norm_b)
    return max(-1.0, min(1.0, score))


def provider_identity(provider: EmbeddingProvider) -> EmbeddingIdentity:
    return EmbeddingIdentity(
        provider=str(provider.provider_name).strip(),
        model=str(provider.model_name).strip(),
        version=(str(provider.model_version).strip() if provider.model_version else None),
    )


def embed_checked(provider: EmbeddingProvider, texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    vectors = provider.embed(texts)
    if len(vectors) != len(texts):
        raise ValueError("embedding provider returned an unexpected number of vectors")
    checked: list[list[float]] = []
    dimension: int | None = None
    for vector in vectors:
        values = validate_vector(vector, expected_dimension=dimension)
        if dimension is None:
            dimension = len(values)
        checked.append(values)
    return checked
