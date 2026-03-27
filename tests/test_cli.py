"""CLI tests."""

from pathlib import Path

from seeklet.cli import build_parser, main
from seeklet.config import DEFAULT_DB_PATH


def test_main_without_arguments_returns_error_code() -> None:
    """Running without a subcommand should return a non-zero exit code."""
    assert main([]) == 1


def test_crawl_command_parses_seed_urls_and_defaults() -> None:
    """The crawl command should parse arguments correctly."""
    parser = build_parser()
    args = parser.parse_args(["crawl", "https://example.com"])

    assert args.command == "crawl"
    assert args.seed_urls == ["https://example.com"]
    assert args.db == DEFAULT_DB_PATH
    assert args.max_pages > 0
    assert args.max_depth >= 0


def test_search_command_parses_query_and_db() -> None:
    """The search command should parse arguments correctly."""
    parser = build_parser()
    args = parser.parse_args(
        ["search", "python", "--db", str(Path("/tmp/test.sqlite3"))]
    )

    assert args.command == "search"
    assert args.query == "python"
    assert args.db == Path("/tmp/test.sqlite3")
