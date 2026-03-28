"""Web crawling utilities for Seeklet."""

from __future__ import annotations

import time
from collections import deque
from collections.abc import Sequence
from urllib.robotparser import RobotFileParser

import httpx

from seeklet.config import DEFAULT_TIMEOUT_SECONDS, DEFAULT_USER_AGENT
from seeklet.extract import extract_content
from seeklet.models import CrawledPage
from seeklet.normalize import (
    get_host,
    get_origin,
    is_allowed_host,
    normalize_url,
)


class Crawler:
    """A minimal synchronous seeded crawler."""

    def __init__(
        self,
        *,
        client: httpx.Client | None = None,
        user_agent: str = DEFAULT_USER_AGENT,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        """Initialize the crawler."""
        self._user_agent = user_agent
        self._robots_cache: dict[str, RobotFileParser] = {}
        self._owns_client = client is None

        self._client = client or httpx.Client(
            follow_redirects=True,
            headers={"User-Agent": user_agent},
            timeout=timeout,
        )

    def close(self) -> None:
        """Close the owned HTTP client."""
        if self._owns_client:
            self._client.close()

    def crawl(
        self,
        seed_urls: Sequence[str],
        *,
        max_pages: int,
        max_depth: int,
        delay_seconds: float = 0.0,
    ) -> list[CrawledPage]:
        """Crawl pages within the allowed host scope."""
        normalized_seed_urls = _normalize_seed_urls(seed_urls)
        if not normalized_seed_urls:
            message = "At least one valid HTTP or HTTPS seed URL is required."
            raise ValueError(message)

        allowed_hosts = {get_host(url) for url in normalized_seed_urls}
        queue = deque((url, 0) for url in normalized_seed_urls)
        queued = set(normalized_seed_urls)
        seen: set[str] = set()
        pages: list[CrawledPage] = []

        while queue and len(pages) < max_pages:
            url, depth = queue.popleft()
            if url in seen:
                continue

            seen.add(url)

            if not is_allowed_host(url, allowed_hosts):
                continue

            if not self.is_allowed_by_robots(url):
                continue

            page = self._fetch_page(
                url, depth=depth, allowed_hosts=allowed_hosts
            )
            if page is None:
                continue

            if page.url != url and page.url in seen:
                continue

            seen.add(page.url)
            pages.append(page)

            if depth >= max_depth:
                continue

            for link in page.links:
                if link in seen or link in queued:
                    continue

                if not is_allowed_host(link, allowed_hosts):
                    continue

                queue.append((link, depth + 1))
                queued.add(link)

            if delay_seconds > 0:
                time.sleep(delay_seconds)

        return pages

    def is_allowed_by_robots(self, url: str) -> bool:
        """Return whether the URL is allowed by robots.txt."""
        parser = self._get_robots_parser(url)
        return parser.can_fetch(self._user_agent, url)

    def _get_robots_parser(self, url: str) -> RobotFileParser:
        """Get or load the cached robots parser for the URL origin."""
        origin = get_origin(url)
        parser = self._robots_cache.get(origin)
        if parser is not None:
            return parser

        robots_url = f"{origin}/robots.txt"
        parser = RobotFileParser()

        try:
            response = self._client.get(robots_url)
        except httpx.HTTPError:
            parser.parse([])
        else:
            if response.status_code == 200:
                parser.set_url(robots_url)
                parser.parse(response.text.splitlines())
            else:
                parser.parse([])

        self._robots_cache[origin] = parser
        return parser

    def _fetch_page(
        self,
        url: str,
        *,
        depth: int,
        allowed_hosts: set[str],
    ) -> CrawledPage | None:
        """Fetch, validate, and extract a single page."""
        try:
            response = self._client.get(url)
        except httpx.HTTPError:
            return None

        if response.status_code >= 400:
            return None

        if not _is_html_content_type(response.headers.get("content-type", "")):
            return None

        final_url = normalize_url(str(response.url))
        if final_url is None:
            return None

        if not is_allowed_host(final_url, allowed_hosts):
            return None

        extracted = extract_content(response.text, final_url)
        return CrawledPage(
            url=final_url,
            title=extracted.title,
            text=extracted.text,
            links=extracted.links,
            depth=depth,
            status_code=response.status_code,
        )


def _normalize_seed_urls(seed_urls: Sequence[str]) -> list[str]:
    """Normalize, validate, and deduplicate seed URLs."""
    normalized_seed_urls: list[str] = []
    seen: set[str] = set()

    for raw_url in seed_urls:
        normalized = normalize_url(raw_url)
        if normalized is None or normalized in seen:
            continue

        seen.add(normalized)
        normalized_seed_urls.append(normalized)

    return normalized_seed_urls


def _is_html_content_type(content_type: str) -> bool:
    """Return whether the content type represents HTML."""
    lowered = content_type.lower()
    return "text/html" in lowered or "application/xhtml+xml" in lowered
