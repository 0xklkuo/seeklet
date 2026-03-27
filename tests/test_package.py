"""Package-level tests."""

from seeklet import __version__


def test_version_is_defined() -> None:
    """The package should expose a version string."""
    assert __version__ == "0.1.0"
