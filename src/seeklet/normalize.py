"""URL and text normalization helpers."""

from __future__ import annotations

import posixpath
import re
from urllib.parse import SplitResult, urljoin, urlsplit, urlunsplit

SUPPORTED_SCHEMES = {"http", "https"}

_WHITESPACE_RE = re.compile(r"\s+")
_MULTI_SLASH_RE = re.compile(r"/{2,}")


def normalize_whitespace(text: str) -> str:
    """Collapse repeated whitespace into single spaces."""
    return _WHITESPACE_RE.sub(" ", text).strip()


def normalize_url(url: str, *, keep_query: bool = False) -> str | None:
    """Normalize an HTTP or HTTPS URL.

    The normalization rules are intentionally small and predictable:

    - keep only http/https
    - lowercase scheme and host
    - drop fragments
    - drop query strings by default
    - remove default ports
    - normalize repeated and relative path segments
    """
    stripped = url.strip()
    if not stripped:
        return None

    parsed = urlsplit(stripped)
    scheme = parsed.scheme.lower()
    if scheme not in SUPPORTED_SCHEMES:
        return None

    host = parsed.hostname
    if host is None:
        return None

    netloc = _build_netloc(scheme=scheme, host=host.lower(), port=parsed.port)
    path = _normalize_path(parsed.path)
    query = parsed.query if keep_query else ""

    normalized = SplitResult(
        scheme=scheme,
        netloc=netloc,
        path=path,
        query=query,
        fragment="",
    )
    return urlunsplit(normalized)


def resolve_url(
    base_url: str,
    href: str,
    *,
    keep_query: bool = False,
) -> str | None:
    """Resolve an extracted link against a base URL."""
    stripped = href.strip()
    if not stripped or stripped.startswith("#"):
        return None

    lowered = stripped.lower()
    if lowered.startswith(("mailto:", "javascript:", "tel:", "data:")):
        return None

    absolute = urljoin(base_url, stripped)
    return normalize_url(absolute, keep_query=keep_query)


def get_host(url: str) -> str:
    """Return the lowercase hostname for a URL."""
    host = urlsplit(url).hostname
    return host.lower() if host is not None else ""


def get_origin(url: str) -> str:
    """Return the origin portion of a URL."""
    parsed = urlsplit(url)
    scheme = parsed.scheme.lower()
    host = parsed.hostname
    if host is None:
        return ""

    netloc = _build_netloc(
        scheme=scheme,
        host=host.lower(),
        port=parsed.port,
    )
    return f"{scheme}://{netloc}"


def is_allowed_host(url: str, allowed_hosts: set[str]) -> bool:
    """Return whether the URL host is inside the allowed host set."""
    return get_host(url) in allowed_hosts


def _build_netloc(*, scheme: str, host: str, port: int | None) -> str:
    """Build a normalized network location."""
    if port is None:
        return host

    if scheme == "http" and port == 80:
        return host

    if scheme == "https" and port == 443:
        return host

    return f"{host}:{port}"


def _normalize_path(path: str) -> str:
    """Normalize a URL path."""
    if not path:
        return "/"

    collapsed = _MULTI_SLASH_RE.sub("/", path)
    if not collapsed.startswith("/"):
        collapsed = f"/{collapsed}"

    normalized = posixpath.normpath(collapsed)
    if normalized == ".":
        return "/"

    if not normalized.startswith("/"):
        normalized = f"/{normalized}"

    return normalized
