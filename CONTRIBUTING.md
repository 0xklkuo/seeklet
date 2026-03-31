# Contributing to Seeklet

Thanks for your interest in contributing.

## Development Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run Checks

```bash
ruff check .
ruff format --check .
pytest
```

## Project Principles

- Keep implementations small and explicit.
- Prefer readability over cleverness.
- Avoid adding dependencies unless they clearly help.
- Keep the code educational and easy to follow.
- Preserve the CLI-first, SQLite-backed MVP direction.

## Pull Request Checklist

Before opening a PR:

- ensure tests pass
- ensure Ruff passes
- update docs if behavior changed
- keep changes focused and small
- add or adjust tests for new behavior

## Code Style

Seeklet follows:

- PEP 8
- Ruff for linting and formatting
- simple module boundaries
- clear docstrings where they improve understanding
