"""Indexing and search tests."""

from pathlib import Path

from seeklet.index import index_pages
from seeklet.models import CrawledPage
from seeklet.search import search_index
from seeklet.storage import read_index_stats


def test_index_pages_and_search_rank_results(tmp_path: Path) -> None:
    """Indexing should persist searchable ranked documents."""
    db_path = tmp_path / "seeklet.sqlite3"

    pages = [
        CrawledPage(
            url="https://example.com/python-packaging",
            title="Python Packaging",
            text="Python packaging with pyproject and wheel builds.",
            links=[],
            depth=0,
            status_code=200,
        ),
        CrawledPage(
            url="https://example.com/rust-cargo",
            title="Rust Cargo",
            text="Cargo handles Rust package builds and dependencies.",
            links=[],
            depth=1,
            status_code=200,
        ),
        CrawledPage(
            url="https://example.com/python-testing",
            title="Python Testing",
            text="Pytest helps test Python applications effectively.",
            links=[],
            depth=1,
            status_code=200,
        ),
    ]

    indexed_count = index_pages(db_path, pages)
    results = search_index(db_path, "python packaging", top_k=3)

    assert indexed_count == 3
    assert len(results) >= 2
    assert results[0].url == "https://example.com/python-packaging"
    assert "python" in results[0].snippet.casefold()


def test_read_index_stats_returns_expected_counts(tmp_path: Path) -> None:
    """Index stats should reflect the current database contents."""
    db_path = tmp_path / "seeklet.sqlite3"

    pages = [
        CrawledPage(
            url="https://example.com/a",
            title="Alpha",
            text="Python alpha beta",
            links=[],
            depth=0,
            status_code=200,
        ),
        CrawledPage(
            url="https://example.com/b",
            title="Beta",
            text="Python gamma delta",
            links=[],
            depth=1,
            status_code=200,
        ),
    ]

    index_pages(db_path, pages)
    stats = read_index_stats(db_path)

    assert stats.document_count == 2
    assert stats.term_count > 0
    assert stats.posting_count > 0
    assert stats.average_document_length > 0.0
