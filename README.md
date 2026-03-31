# Seeklet

Seeklet is a minimal, educational web search engine in Python.

Its purpose is to help developers learn how a small search engine works,
end to end, without unnecessary complexity.

## Goals

- Keep the codebase small and easy to read.
- Teach core search engine concepts through implementation.
- Follow modern Python best practices.
- Be easy to run, study, and contribute to.

## MVP Scope

Seeklet will:

- crawl one or more seed URLs
- stay within allowed domain scope
- respect `robots.txt`
- extract page titles, text, and links
- build a local SQLite-backed index
- search with BM25 ranking
- expose a simple CLI

## Non-Goals for the MVP

Seeklet will not initially include:

- JavaScript rendering
- distributed crawling
- semantic/vector search
- PageRank
- fuzzy search
- phrase/boolean search
- a REST API

## Current Status

The MVP is implemented.

At this stage, Seeklet can:

- crawl seed URLs
- stay within the original host scope
- respect `robots.txt`
- extract titles, visible text, and links
- build a local SQLite index
- search that index with BM25 ranking
- show index statistics
- reset local state

## Quickstart

### Requirements

- Python 3.12
- Linux or macOS

### Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Run

```bash
seeklet --help
```

Or:

```bash
python -m seeklet --help
```

### Run Checks

```bash
ruff check .
ruff format --check .
pytest
```

## Example Workflow

```bash
seeklet crawl https://example.com --max-pages 20 --max-depth 1
seeklet stats
seeklet search "example domain"
seeklet reset --yes
```

## Project Structure

```text
src/seeklet/
    __init__.py
    __main__.py
    cli.py
    config.py
    crawl.py
    extract.py
    index.py
    models.py
    normalize.py
    ranking.py
    search.py
    snippet.py
    storage.py

tests/
docs/
.github/workflows/
```

## Development Principles

- Prefer the standard library when it keeps the design clear.
- Add dependencies only when they clearly improve the project.
- Keep code explicit and readable over clever.
- Optimize only after measuring and only where it matters.

## License

MIT
