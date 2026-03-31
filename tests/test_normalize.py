"""Normalization tests."""

from seeklet.normalize import normalize_url, resolve_url, tokenize_text


def test_normalize_url_removes_fragment_and_query_by_default() -> None:
    """URL normalization should drop fragments and query strings."""
    url = "HTTPS://Example.com:443/docs/page/?q=test#section"

    assert normalize_url(url) == "https://example.com/docs/page"


def test_normalize_url_keeps_query_when_requested() -> None:
    """URL normalization should optionally preserve query strings."""
    url = "https://example.com/search?q=python#top"

    assert normalize_url(url, keep_query=True) == (
        "https://example.com/search?q=python"
    )


def test_resolve_url_skips_non_http_links() -> None:
    """Non-web links should be ignored."""
    base_url = "https://example.com/docs"

    assert resolve_url(base_url, "mailto:test@example.com") is None
    assert resolve_url(base_url, "javascript:void(0)") is None
    assert resolve_url(base_url, "#local-anchor") is None


def test_resolve_url_resolves_relative_links() -> None:
    """Relative links should resolve against the base URL."""
    base_url = "https://example.com/docs/index.html"
    href = "../guide/getting-started.html#intro"

    assert resolve_url(base_url, href) == (
        "https://example.com/guide/getting-started.html"
    )


def test_tokenize_text_normalizes_case_and_whitespace() -> None:
    """Tokenization should return lowercase search terms."""
    text = " Python,\nPACKAGING\t101! "

    assert tokenize_text(text) == ["python", "packaging", "101"]
