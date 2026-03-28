"""Project configuration defaults."""

from pathlib import Path

APP_NAME = "seeklet"

DEFAULT_DATA_DIR = Path(".seeklet")
DEFAULT_DB_PATH = DEFAULT_DATA_DIR / "seeklet.sqlite3"

DEFAULT_MAX_PAGES = 200
DEFAULT_MAX_DEPTH = 2
DEFAULT_DELAY_SECONDS = 0.5
DEFAULT_TOP_K = 10

DEFAULT_USER_AGENT = "seeklet/0.1"
DEFAULT_TIMEOUT_SECONDS = 10.0


def ensure_data_dir(path: Path) -> None:
    """Create the parent directory for the given database path."""
    path.parent.mkdir(parents=True, exist_ok=True)
