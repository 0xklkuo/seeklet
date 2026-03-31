"""Search execution for Seeklet."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from seeklet.models import SearchResult
from seeklet.normalize import tokenize_text
from seeklet.ranking import bm25_idf, bm25_term_score
from seeklet.snippet import build_snippet
from seeklet.storage import (
    connect_database,
    get_index_stats,
    initialize_database,
)


def search_index(
    db_path: Path,
    query: str,
    *,
    top_k: int,
) -> list[SearchResult]:
    """Search the local index and return ranked results."""
    if not db_path.exists():
        return []

    query_terms = sorted(set(tokenize_text(query)))
    if not query_terms:
        return []

    connection = connect_database(db_path)

    try:
        initialize_database(connection)
        stats = get_index_stats(connection)
        if stats.document_count == 0:
            return []

        term_rows = _fetch_term_rows(connection, query_terms)
        if not term_rows:
            return []

        scores: dict[int, float] = {}
        documents: dict[int, sqlite3.Row] = {}

        for row in term_rows:
            idf = bm25_idf(
                stats.document_count,
                int(row["document_frequency"]),
            )
            posting_rows = connection.execute(
                """
                SELECT
                    d.id AS document_id,
                    d.url,
                    d.title,
                    d.content,
                    d.content_length,
                    p.term_frequency
                FROM postings AS p
                JOIN documents AS d
                  ON d.id = p.document_id
                WHERE p.term_id = ?
                """,
                (row["id"],),
            ).fetchall()

            for posting in posting_rows:
                document_id = int(posting["document_id"])
                score = bm25_term_score(
                    term_frequency=int(posting["term_frequency"]),
                    document_length=int(posting["content_length"]),
                    average_document_length=(stats.average_document_length),
                    idf=idf,
                )
                scores[document_id] = scores.get(document_id, 0.0) + score
                documents[document_id] = posting

        results = [
            SearchResult(
                url=str(documents[document_id]["url"]),
                title=str(documents[document_id]["title"]),
                snippet=build_snippet(
                    str(documents[document_id]["content"]),
                    query_terms,
                ),
                score=score,
            )
            for document_id, score in scores.items()
        ]

        return sorted(
            results,
            key=lambda result: (-result.score, result.url),
        )[:top_k]
    finally:
        connection.close()


def _fetch_term_rows(
    connection: sqlite3.Connection,
    query_terms: list[str],
) -> list[sqlite3.Row]:
    """Fetch indexed term metadata for a query."""
    placeholders = ", ".join("?" for _ in query_terms)

    return connection.execute(
        f"""
        SELECT
            t.id,
            t.term,
            COUNT(p.document_id) AS document_frequency
        FROM terms AS t
        LEFT JOIN postings AS p
          ON p.term_id = t.id
        WHERE t.term IN ({placeholders})
        GROUP BY t.id, t.term
        """,
        query_terms,
    ).fetchall()
