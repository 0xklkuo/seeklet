# Seeklet Architecture

## Purpose

Seeklet is a minimal educational search engine for learning the Python
ecosystem and the fundamentals of modern search systems.

## MVP Architecture

```text
seed URLs
  -> crawler
  -> HTML extraction
  -> normalization/tokenization
  -> SQLite storage
  -> inverted index
  -> BM25 ranking
  -> CLI results
```

## Design Priorities

1. Simplicity
2. Readability
3. Small dependency surface
4. Contributor friendliness
5. Real-world enough to teach core ideas

## Planned Modules

- `cli.py`:
  Parse commands and call application services.

- `config.py`:
  Store default paths and runtime settings.

- `crawl.py`:
  Crawl seed URLs within allowed scope.

- `extract.py`:
  Extract title, visible text, and links from HTML.

- `normalize.py`:
  Normalize URLs and tokenize text.

- `storage.py`:
  Manage SQLite persistence.

- `index.py`:
  Build and update the inverted index.

- `ranking.py`:
  Compute BM25 scores.

- `search.py`:
  Execute queries and return ranked results.

- `snippet.py`:
  Produce short result snippets.

## Initial Technical Choices

- Python 3.12
- SQLite for persistence
- `httpx` for HTTP fetching
- `beautifulsoup4` for HTML parsing
- `argparse` for CLI
- `pytest` for tests
- `ruff` for linting and formatting

## Deliberate MVP Limits

To keep the project educational and minimal, the MVP will not include:

- JavaScript execution
- asynchronous crawling
- advanced ranking signals
- vector databases
- browser UI
- distributed systems concerns
