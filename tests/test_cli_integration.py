"""CLI integration tests."""

from pathlib import Path

from seeklet.cli import main
from seeklet.index import index_pages
from seeklet.models import CrawledPage


def test_search_command_prints_ranked_results(
    tmp_path: Path,
    capsys,
) -> None:
    """The search command should print indexed results."""
    db_path = tmp_path / "seeklet.sqlite3"

    pages = [
        CrawledPage(
            url="https://example.com/python",
            title="Python Guide",
            text="Python packaging and testing guide.",
            links=[],
            depth=0,
            status_code=200,
        )
    ]
    index_pages(db_path, pages)

    exit_code = main(
        ["search", "python packaging", "--db", str(db_path), "--top-k", "5"]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Python Guide" in captured.out
    assert "https://example.com/python" in captured.out


def test_stats_command_prints_index_counts(
    tmp_path: Path,
    capsys,
) -> None:
    """The stats command should print index statistics."""
    db_path = tmp_path / "seeklet.sqlite3"

    pages = [
        CrawledPage(
            url="https://example.com/page",
            title="Page",
            text="Example content for stats output.",
            links=[],
            depth=0,
            status_code=200,
        )
    ]
    index_pages(db_path, pages)

    exit_code = main(["stats", "--db", str(db_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Documents: 1" in captured.out
    assert "Terms:" in captured.out
    assert "Postings:" in captured.out


def test_reset_command_deletes_database(
    tmp_path: Path,
    capsys,
) -> None:
    """The reset command should remove the database file."""
    db_path = tmp_path / "seeklet.sqlite3"

    pages = [
        CrawledPage(
            url="https://example.com/page",
            title="Page",
            text="Example content.",
            links=[],
            depth=0,
            status_code=200,
        )
    ]
    index_pages(db_path, pages)

    exit_code = main(["reset", "--db", str(db_path), "--yes"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Deleted database" in captured.out
    assert not db_path.exists()


def test_crawl_command_rejects_invalid_limits(capsys) -> None:
    """The crawl command should reject invalid numeric options."""
    exit_code = main(["crawl", "https://example.com", "--max-pages", "0"])
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "--max-pages must be at least 1." in captured.out
