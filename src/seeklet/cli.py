"""Command-line interface for Seeklet."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from seeklet.config import (
    DEFAULT_DB_PATH,
    DEFAULT_DELAY_SECONDS,
    DEFAULT_MAX_DEPTH,
    DEFAULT_MAX_PAGES,
    DEFAULT_TOP_K,
)


def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="seeklet",
        description="A minimal educational web search engine.",
    )

    subparsers = parser.add_subparsers(dest="command")

    crawl_parser = subparsers.add_parser(
        "crawl",
        help="Crawl and index one or more seed URLs.",
    )
    crawl_parser.add_argument(
        "seed_urls",
        nargs="+",
        help="One or more seed URLs to crawl.",
    )
    crawl_parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help="Path to the SQLite database.",
    )
    crawl_parser.add_argument(
        "--max-pages",
        type=int,
        default=DEFAULT_MAX_PAGES,
        help="Maximum number of pages to crawl.",
    )
    crawl_parser.add_argument(
        "--max-depth",
        type=int,
        default=DEFAULT_MAX_DEPTH,
        help="Maximum crawl depth from the seed URL.",
    )
    crawl_parser.add_argument(
        "--delay-seconds",
        type=float,
        default=DEFAULT_DELAY_SECONDS,
        help="Delay between requests in seconds.",
    )
    crawl_parser.set_defaults(func=handle_crawl)

    search_parser = subparsers.add_parser(
        "search",
        help="Search the local index.",
    )
    search_parser.add_argument(
        "query",
        help="Search query text.",
    )
    search_parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help="Path to the SQLite database.",
    )
    search_parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_TOP_K,
        help="Maximum number of results to return.",
    )
    search_parser.set_defaults(func=handle_search)

    stats_parser = subparsers.add_parser(
        "stats",
        help="Show local index statistics.",
    )
    stats_parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help="Path to the SQLite database.",
    )
    stats_parser.set_defaults(func=handle_stats)

    reset_parser = subparsers.add_parser(
        "reset",
        help="Delete local index data.",
    )
    reset_parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help="Path to the SQLite database.",
    )
    reset_parser.add_argument(
        "--yes",
        action="store_true",
        help="Confirm deletion without prompting.",
    )
    reset_parser.set_defaults(func=handle_reset)

    return parser


def handle_crawl(args: argparse.Namespace) -> int:
    """Handle the crawl command."""
    print("Crawl is not implemented yet.")
    print(f"Seed URLs: {args.seed_urls}")
    print(f"Database: {args.db}")
    return 0


def handle_search(args: argparse.Namespace) -> int:
    """Handle the search command."""
    print("Search is not implemented yet.")
    print(f"Query: {args.query}")
    print(f"Database: {args.db}")
    return 0


def handle_stats(args: argparse.Namespace) -> int:
    """Handle the stats command."""
    print("Stats is not implemented yet.")
    print(f"Database: {args.db}")
    return 0


def handle_reset(args: argparse.Namespace) -> int:
    """Handle the reset command."""
    print("Reset is not implemented yet.")
    print(f"Database: {args.db}")
    print(f"Confirmed: {args.yes}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return 1

    return args.func(args)
