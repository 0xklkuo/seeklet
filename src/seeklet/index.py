"""Index-building logic for Seeklet."""

from __future__ import annotations

import sqlite3
from collections import Counter
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

from seeklet.models import CrawledPage
from seeklet.normalize import tokenize_text
from seeklet.storage import clear_index, connect_database, initialize_database


def index_pages(db_path: Path, pages: Sequence[CrawledPage]) -> int:
    """Rebuild the local search index from crawled pages."""
    connection = connect_database(db_path)

    try:
        initialize_database(connection)

        with connection:
            clear_index(connection)
            term_ids: dict[str, int] = {}

            for page in pages:
                _index_page(connection, page, term_ids)

        return len(pages)
    finally:
        connection.close()


def _index_page(
    connection: sqlite3.Connection,
    page: CrawledPage,
    term_ids: dict[str, int],
) -> None:
    """Insert one crawled page and its postings."""
    combined_text = " ".join(part for part in (page.title, page.text) if part)
    tokens = tokenize_text(combined_text)
    term_frequencies = Counter(tokens)
    crawled_at = datetime.now(UTC).isoformat()

    cursor = connection.execute(
        """
        INSERT INTO documents (
            url,
            title,
            content,
            content_length,
            crawled_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            page.url,
            page.title,
            page.text,
            len(tokens),
            crawled_at,
        ),
    )
    if cursor.lastrowid is None:
        raise RuntimeError("Failed to insert document row.")

    document_id = int(cursor.lastrowid)

    for term, term_frequency in term_frequencies.items():
        term_id = _get_or_create_term_id(connection, term, term_ids)
        connection.execute(
            """
            INSERT INTO postings (
                term_id,
                document_id,
                term_frequency
            )
            VALUES (?, ?, ?)
            """,
            (term_id, document_id, term_frequency),
        )


def _get_or_create_term_id(
    connection: sqlite3.Connection,
    term: str,
    cache: dict[str, int],
) -> int:
    """Get or create the integer identifier for a term."""
    cached = cache.get(term)
    if cached is not None:
        return cached

    row = connection.execute(
        "SELECT id FROM terms WHERE term = ?",
        (term,),
    ).fetchone()
    if row is not None:
        term_id = int(row["id"])
        cache[term] = term_id
        return term_id

    cursor = connection.execute(
        "INSERT INTO terms (term) VALUES (?)",
        (term,),
    )
    if cursor.lastrowid is None:
        raise RuntimeError("Failed to insert term row.")

    term_id = int(cursor.lastrowid)
    cache[term] = term_id
    return term_id
