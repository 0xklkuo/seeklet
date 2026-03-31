"""Snippet tests."""

from seeklet.snippet import build_snippet


def test_build_snippet_prefers_region_near_query_term() -> None:
    """Snippets should include the first matching query term."""
    text = (
        "alpha beta gamma delta epsilon zeta eta theta iota kappa "
        "python packaging makes distribution easier for projects"
    )

    snippet = build_snippet(text, ["python"], max_length=50)

    assert "python" in snippet.casefold()


def test_build_snippet_falls_back_to_prefix_when_no_match() -> None:
    """Snippets should fall back to the content prefix when needed."""
    text = "This is a simple document used for snippet generation tests."

    snippet = build_snippet(text, ["missing"], max_length=20)

    assert snippet.endswith("...")
