"""HTML extraction helpers."""

from __future__ import annotations

from bs4 import BeautifulSoup

from seeklet.models import ExtractedContent
from seeklet.normalize import normalize_whitespace, resolve_url

UNWANTED_TAGS = (
    "script",
    "style",
    "noscript",
    "template",
    "svg",
    "canvas",
)


def extract_content(html: str, base_url: str) -> ExtractedContent:
    """Extract title, visible text, and normalized links from HTML."""
    soup = BeautifulSoup(html, "html.parser")

    for tag_name in UNWANTED_TAGS:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    title = ""
    if soup.title is not None:
        title = normalize_whitespace(soup.title.get_text(" ", strip=True))

    root = soup.body or soup
    text = normalize_whitespace(root.get_text(" ", strip=True))
    links = _extract_links(soup, base_url)

    return ExtractedContent(title=title, text=text, links=links)


def _extract_links(soup: BeautifulSoup, base_url: str) -> list[str]:
    """Extract normalized absolute links from a parsed document."""
    links: list[str] = []
    seen: set[str] = set()

    for anchor in soup.find_all("a", href=True):
        normalized = resolve_url(base_url, anchor["href"])
        if normalized is None or normalized in seen:
            continue

        seen.add(normalized)
        links.append(normalized)

    return links
