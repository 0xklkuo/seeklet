"""Snippet generation helpers."""

from __future__ import annotations

from seeklet.normalize import normalize_whitespace


def build_snippet(
    text: str,
    query_terms: list[str],
    *,
    max_length: int = 160,
) -> str:
    """Build a short snippet around the first matched query term."""
    normalized = normalize_whitespace(text)
    if not normalized:
        return ""

    if len(normalized) <= max_length:
        return normalized

    lowered = normalized.casefold()
    first_match = -1

    for term in query_terms:
        position = lowered.find(term.casefold())
        if position == -1:
            continue

        if first_match == -1 or position < first_match:
            first_match = position

    if first_match == -1:
        excerpt = normalized[:max_length].rstrip()
        return f"{excerpt}..."

    start = max(0, first_match - max_length // 3)
    end = min(len(normalized), start + max_length)

    if end - start < max_length and start > 0:
        start = max(0, end - max_length)

    excerpt = normalized[start:end].strip()

    if start > 0:
        excerpt = f"...{excerpt}"

    if end < len(normalized):
        excerpt = f"{excerpt}..."

    return excerpt
