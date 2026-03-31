# Seeklet

[![CI](https://github.com/0xklkuo/seeklet/actions/workflows/ci.yml/badge.svg)](https://github.com/0xklkuo/seeklet/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)]()

Seeklet is a minimal, educational web search engine written in Python.

It is designed as a self-educational playground for developers who want to
learn the fundamentals of:

- web crawling
- HTML extraction
- text normalization and tokenization
- inverted indexing
- BM25 ranking
- SQLite-backed search systems
- open-source Python project structure and workflows

Seeklet intentionally favors **clarity, simplicity, and contributor
friendliness** over advanced features or production-scale complexity.

---

## Why Seeklet?

Modern search systems can become complex quickly. Seeklet exists to show the
core ideas with a small, readable codebase.

The project aims to be:

- **minimal**: only the essential moving parts
- **practical**: built around real website crawling and search
- **educational**: architecture and logic are easy to inspect
- **open-source friendly**: straightforward setup, tooling, and testing

---

## Features

Current MVP features:

- seeded website crawling from one or more URLs
- same-host crawl scoping
- `robots.txt` support
- HTML title, text, and link extraction
- normalized URL handling
- SQLite-backed local persistence
- inverted index storage
- BM25 ranking
- result snippets
- CLI commands for:
  - `crawl`
  - `search`
  - `stats`
  - `reset`
- automated tests with `pytest`
- linting and formatting with `ruff`
- GitHub Actions CI

---

## Non-goals for the MVP

Seeklet is intentionally not trying to be a full production search engine.

Not included in the MVP:

- JavaScript rendering
- distributed crawling
- asynchronous crawling
- PageRank or link-analysis ranking
- phrase search
- boolean search
- fuzzy search
- semantic/vector search
- REST API
- full browser UI

These can be added later as follow-up learning milestones.

---

## Architecture at a glance

```text
seed URLs
  -> crawl allowed pages
  -> fetch HTML
  -> extract title, text, and links
  -> normalize URLs and tokenize text
  -> rebuild SQLite index
  -> execute BM25 search
  -> print ranked CLI results
```

Core modules:

- `crawl.py` — seeded crawling and `robots.txt` handling
- `extract.py` — HTML parsing and content extraction
- `normalize.py` — URL normalization and tokenization
- `storage.py` — SQLite schema and storage helpers
- `index.py` — index rebuilding
- `ranking.py` — BM25 scoring helpers
- `search.py` — query execution
- `snippet.py` — result snippet generation
- `cli.py` — command-line interface

For more detail, see [`docs/architecture.md`](docs/architecture.md).

---

## Project status

Seeklet is currently at the **MVP stage**.

It is ready to:

- crawl a small website
- extract and index its pages locally
- perform BM25-based keyword search from the CLI

It is not yet optimized for large-scale crawling or advanced retrieval
features.

---

## Requirements

- Python **3.12**
- Linux or macOS
- internet access for crawling live websites

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/0xklkuo/seeklet.git
cd YOUR-REPO
```

### 2. Create a virtual environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Install the project

```bash
pip install -e ".[dev]"
```

---

## Quickstart

### Crawl a site

```bash
seeklet crawl https://example.com --max-pages 20 --max-depth 1
```

### Show index statistics

```bash
seeklet stats
```

### Search the local index

```bash
seeklet search "example domain"
```

### Reset local state

```bash
seeklet reset --yes
```

---

## CLI usage

### `seeklet crawl`

Crawl and index one or more seed URLs.

```bash
seeklet crawl SEED_URL [SEED_URL ...] [--db PATH] [--max-pages N] [--max-depth N] [--delay-seconds N]
```

Example:

```bash
seeklet crawl https://example.com --max-pages 50 --max-depth 2
```

Options:

- `--db` — path to the SQLite database
- `--max-pages` — maximum number of pages to crawl
- `--max-depth` — maximum crawl depth from seed URLs
- `--delay-seconds` — delay between requests

### `seeklet search`

Search the local index.

```bash
seeklet search "query text" [--db PATH] [--top-k N]
```

Example:

```bash
seeklet search "python packaging"
```

Options:

- `--db` — path to the SQLite database
- `--top-k` — maximum number of results to return

### `seeklet stats`

Show index statistics.

```bash
seeklet stats [--db PATH]
```

### `seeklet reset`

Delete local index data.

```bash
seeklet reset [--db PATH] [--yes]
```

---

## Example workflow

```bash
seeklet crawl https://example.com --max-pages 20 --max-depth 1
seeklet stats
seeklet search "example domain"
seeklet reset --yes
```

Example output shape for search:

```text
1. Example Domain
   URL: https://example.com/
   Score: 1.2345
   Snippet: This domain is for use in illustrative examples...
```

Exact results depend on the crawled site and its content.

---

## SQLite storage model

Seeklet stores its local index in SQLite.

Main tables:

- `documents`
  - one row per crawled page
- `terms`
  - one row per normalized term
- `postings`
  - term-to-document mapping with term frequency

This keeps the storage layer:

- simple
- inspectable
- easy to learn from
- easy to run locally without extra services

---

## Ranking model

Seeklet currently uses **BM25** for ranking.

At query time:

1. query text is normalized and tokenized
2. matching terms are looked up in the index
3. postings are loaded from SQLite
4. BM25 scores are computed in Python
5. top results are sorted and printed

This keeps the ranking logic explicit and educational.

---

## Design principles

Seeklet follows a few simple rules:

- prefer the standard library when it keeps the code clear
- add dependencies only when they clearly help
- keep modules small and focused
- favor readability over cleverness
- avoid premature optimization
- keep the contributor experience simple

---

## Limitations

Current limitations are intentional:

- crawl scope is limited to the original host(s)
- JavaScript-rendered pages are not indexed
- the crawler is synchronous
- each crawl rebuilds the full index
- tokenization is intentionally basic
- ranking uses only term-based BM25, not link signals or semantics

These are acceptable tradeoffs for the educational MVP.

---

## Development

### Run all checks

```bash
ruff check .
ruff format --check .
pytest
```

### Run the CLI directly

```bash
python -m seeklet --help
```

### Local editable install

```bash
pip install -e ".[dev]"
```

---

## Project structure

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

---

## Contributing

Contributions are welcome, especially if they preserve the project's goals:

- simplicity
- readability
- educational value
- minimalism

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

Good first areas for contribution:

- better tokenization
- sitemap support
- benchmark scripts
- phrase search
- optional subdomain crawl mode
- improved documentation and examples

---

## Roadmap

Possible next steps after the MVP:

- incremental recrawling
- phrase search
- boolean search
- optional subdomain crawling
- sitemap discovery
- better language handling
- benchmark scripts
- simple web UI
- link-analysis ranking experiments

These are future learning extensions, not required for the current MVP.

---

## Open-source notes

Seeklet is intentionally structured to be approachable for contributors.

The repo includes:

- tests
- linting/formatting
- CI
- architecture documentation
- contributor guidance

The goal is to make it easy for developers of different experience levels to:

- run the project
- inspect the code
- understand the design
- contribute improvements

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

Seeklet is inspired by the idea that the best way to understand search systems
is to build one from first principles, with modern tooling but without
unnecessary complexity.
