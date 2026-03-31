"""Data models used by Seeklet."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ExtractedContent:
    """Structured content extracted from a single HTML page."""

    title: str
    text: str
    links: list[str]


@dataclass(slots=True)
class CrawledPage:
    """A crawled and parsed HTML page."""

    url: str
    title: str
    text: str
    links: list[str]
    depth: int
    status_code: int


@dataclass(slots=True)
class SearchResult:
    """A ranked search result."""

    url: str
    title: str
    snippet: str
    score: float


@dataclass(slots=True)
class IndexStats:
    """Basic statistics about the local search index."""

    document_count: int
    term_count: int
    posting_count: int
    average_document_length: float
