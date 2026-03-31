"""Ranking helpers for Seeklet."""

from __future__ import annotations

import math


def bm25_idf(document_count: int, document_frequency: int) -> float:
    """Compute BM25 inverse document frequency."""
    if document_count <= 0 or document_frequency <= 0:
        return 0.0

    return math.log(
        1.0
        + (document_count - document_frequency + 0.5)
        / (document_frequency + 0.5)
    )


def bm25_term_score(
    *,
    term_frequency: int,
    document_length: int,
    average_document_length: float,
    idf: float,
    k1: float = 1.2,
    b: float = 0.75,
) -> float:
    """Compute the BM25 contribution of a term for one document."""
    if term_frequency <= 0 or idf <= 0.0:
        return 0.0

    if average_document_length <= 0.0:
        return 0.0

    length_ratio = document_length / average_document_length
    denominator = term_frequency + k1 * (1.0 - b + b * length_ratio)

    return idf * (term_frequency * (k1 + 1.0) / denominator)
