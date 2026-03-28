"""Crawler tests."""

from __future__ import annotations

import httpx

from seeklet.crawl import Crawler


def test_crawler_respects_host_scope_and_robots() -> None:
    """The crawler should stay on host and skip disallowed paths."""
    transport = httpx.MockTransport(_host_scope_handler)
    client = httpx.Client(transport=transport, follow_redirects=True)

    crawler = Crawler(client=client)

    try:
        pages = crawler.crawl(
            ["https://example.com/"],
            max_pages=10,
            max_depth=2,
            delay_seconds=0.0,
        )
    finally:
        crawler.close()
        client.close()

    urls = [page.url for page in pages]

    assert "https://example.com/" in urls
    assert "https://example.com/about" in urls
    assert "https://example.com/private" not in urls
    assert all("external.example" not in url for url in urls)


def test_crawler_respects_max_depth() -> None:
    """The crawler should not fetch pages deeper than max_depth."""
    transport = httpx.MockTransport(_depth_handler)
    client = httpx.Client(transport=transport, follow_redirects=True)

    crawler = Crawler(client=client)

    try:
        pages = crawler.crawl(
            ["https://example.com/"],
            max_pages=10,
            max_depth=1,
            delay_seconds=0.0,
        )
    finally:
        crawler.close()
        client.close()

    urls = [page.url for page in pages]

    assert "https://example.com/" in urls
    assert "https://example.com/level-1" in urls
    assert "https://example.com/level-2" not in urls


def _host_scope_handler(request: httpx.Request) -> httpx.Response:
    """Serve a small test site with robots rules."""
    if request.url.path == "/robots.txt":
        text = "User-agent: *\nDisallow: /private\n"
        return _response(request, 200, text, "text/plain")

    if request.url.path == "/":
        text = """
        <html>
          <head><title>Home</title></head>
          <body>
            <a href="/about">About</a>
            <a href="/private">Private</a>
            <a href="https://external.example/">External</a>
          </body>
        </html>
        """
        return _response(request, 200, text, "text/html")

    if request.url.path == "/about":
        text = """
        <html>
          <head><title>About</title></head>
          <body>
            <p>About page.</p>
          </body>
        </html>
        """
        return _response(request, 200, text, "text/html")

    if request.url.path == "/private":
        text = """
        <html>
          <head><title>Private</title></head>
          <body>
            <p>Should not be crawled.</p>
          </body>
        </html>
        """
        return _response(request, 200, text, "text/html")

    return _response(request, 404, "not found", "text/plain")


def _depth_handler(request: httpx.Request) -> httpx.Response:
    """Serve a small test site with multiple levels."""
    if request.url.path == "/robots.txt":
        text = "User-agent: *\nDisallow:\n"
        return _response(request, 200, text, "text/plain")

    if request.url.path == "/":
        text = """
        <html>
          <head><title>Root</title></head>
          <body>
            <a href="/level-1">Level 1</a>
          </body>
        </html>
        """
        return _response(request, 200, text, "text/html")

    if request.url.path == "/level-1":
        text = """
        <html>
          <head><title>Level 1</title></head>
          <body>
            <a href="/level-2">Level 2</a>
          </body>
        </html>
        """
        return _response(request, 200, text, "text/html")

    if request.url.path == "/level-2":
        text = """
        <html>
          <head><title>Level 2</title></head>
          <body>
            <p>Deep page.</p>
          </body>
        </html>
        """
        return _response(request, 200, text, "text/html")

    return _response(request, 404, "not found", "text/plain")


def _response(
    request: httpx.Request,
    status_code: int,
    text: str,
    content_type: str,
) -> httpx.Response:
    """Build a response for a mocked request."""
    return httpx.Response(
        status_code=status_code,
        headers={"content-type": content_type},
        text=text,
        request=request,
    )
