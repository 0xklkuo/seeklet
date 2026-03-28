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
