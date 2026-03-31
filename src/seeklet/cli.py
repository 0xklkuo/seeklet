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
    ensure_data_dir,
)
from seeklet.crawl import Crawler
from seeklet.index import index_pages
from seeklet.search import search_index
from seeklet.storage import delete_database, read_index_stats


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
    ensure_data_dir(args.db)

    crawler = Crawler()

    try:
        pages = crawler.crawl(
            args.seed_urls,
            max_pages=args.max_pages,
            max_depth=args.max_depth,
            delay_seconds=args.delay_seconds,
        )
    except ValueError as error:
        print(f"Error: {error}")
        return 2
    finally:
        crawler.close()

    indexed_count = index_pages(args.db, pages)

    print(f"Rebuilt index with {indexed_count} page(s).")
    print(f"Database: {args.db}")

    for page in pages:
        title = page.title or "(untitled)"
        print(f"[depth={page.depth}] {title}")
        print(f"  {page.url}")

    return 0


def handle_search(args: argparse.Namespace) -> int:
    """Handle the search command."""
    results = search_index(
        args.db,
        args.query,
        top_k=args.top_k,
    )

    if not results:
        print("No results.")
        return 0

    for index, result in enumerate(results, start=1):
        title = result.title or "(untitled)"
        print(f"{index}. {title}")
        print(f"   URL: {result.url}")
        print(f"   Score: {result.score:.4f}")
        if result.snippet:
            print(f"   Snippet: {result.snippet}")
        print()

    return 0


def handle_stats(args: argparse.Namespace) -> int:
    """Handle the stats command."""
    stats = read_index_stats(args.db)

    print(f"Database: {args.db}")
    print(f"Documents: {stats.document_count}")
    print(f"Terms: {stats.term_count}")
    print(f"Postings: {stats.posting_count}")
    print(f"Average document length: {stats.average_document_length:.2f}")

    return 0


def handle_reset(args: argparse.Namespace) -> int:
    """Handle the reset command."""
    if not args.yes:
        response = input(f"Delete local index at {args.db}? [y/N]: ").strip()
        if response.casefold() not in {"y", "yes"}:
            print("Aborted.")
            return 1

    deleted = delete_database(args.db)
    if deleted:
        print(f"Deleted database: {args.db}")
    else:
        print(f"Nothing to delete: {args.db}")

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return 1

    return args.func(args)
