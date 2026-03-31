"""SQLite storage helpers for Seeklet."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from seeklet.models import IndexStats

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    content_length INTEGER NOT NULL,
    crawled_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS terms (
    id INTEGER PRIMARY KEY,
    term TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS postings (
    term_id INTEGER NOT NULL,
    document_id INTEGER NOT NULL,
    term_frequency INTEGER NOT NULL,
    PRIMARY KEY (term_id, document_id),
    FOREIGN KEY (term_id) REFERENCES terms(id) ON DELETE CASCADE,
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_postings_document_id
ON postings(document_id);
"""


def connect_database(db_path: Path) -> sqlite3.Connection:
    """Open a SQLite connection for the given database path."""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(connection: sqlite3.Connection) -> None:
    """Create the database schema if it does not exist."""
    connection.executescript(SCHEMA_SQL)


def clear_index(connection: sqlite3.Connection) -> None:
    """Remove all indexed data from the database."""
    connection.execute("DELETE FROM postings")
    connection.execute("DELETE FROM terms")
    connection.execute("DELETE FROM documents")


def get_index_stats(connection: sqlite3.Connection) -> IndexStats:
    """Read index statistics from an open database connection."""
    document_count = _scalar_int(
        connection,
        "SELECT COUNT(*) FROM documents",
    )
    term_count = _scalar_int(
        connection,
        "SELECT COUNT(*) FROM terms",
    )
    posting_count = _scalar_int(
        connection,
        "SELECT COUNT(*) FROM postings",
    )

    average_document_length = float(
        connection.execute(
            """
            SELECT COALESCE(AVG(content_length), 0.0)
            FROM documents
            """
        ).fetchone()[0]
    )

    return IndexStats(
        document_count=document_count,
        term_count=term_count,
        posting_count=posting_count,
        average_document_length=average_document_length,
    )


def read_index_stats(db_path: Path) -> IndexStats:
    """Read index statistics from a database path."""
    if not db_path.exists():
        return IndexStats(
            document_count=0,
            term_count=0,
            posting_count=0,
            average_document_length=0.0,
        )

    connection = connect_database(db_path)
    try:
        initialize_database(connection)
        return get_index_stats(connection)
    finally:
        connection.close()


def delete_database(db_path: Path) -> bool:
    """Delete the SQLite database file if it exists."""
    if not db_path.exists():
        return False

    db_path.unlink()
    return True


def _scalar_int(connection: sqlite3.Connection, sql: str) -> int:
    """Execute a scalar integer query."""
    return int(connection.execute(sql).fetchone()[0])
