"""Ranking tests."""

from seeklet.ranking import bm25_idf, bm25_term_score


def test_bm25_idf_is_higher_for_rarer_terms() -> None:
    """Rarer terms should have a higher IDF."""
    rare = bm25_idf(document_count=100, document_frequency=2)
    common = bm25_idf(document_count=100, document_frequency=50)

    assert rare > common > 0.0


def test_bm25_term_score_increases_with_term_frequency() -> None:
    """Higher term frequency should produce a higher score."""
    low = bm25_term_score(
        term_frequency=1,
        document_length=100,
        average_document_length=100.0,
        idf=1.0,
    )
    high = bm25_term_score(
        term_frequency=3,
        document_length=100,
        average_document_length=100.0,
        idf=1.0,
    )

    assert high > low > 0.0
