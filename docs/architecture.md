# Seeklet Architecture

## Purpose

Seeklet is a minimal educational search engine for learning the Python
ecosystem and the fundamentals of modern search systems.

## End-to-End Flow

```text
seed URLs
  -> crawl allowed pages
  -> fetch HTML
  -> extract title, text, and links
  -> normalize and tokenize text
  -> rebuild SQLite index
  -> execute ranked BM25 search
  -> print CLI results
```

## Design Priorities

1. Simplicity
2. Readability
3. Small dependency surface
4. Contributor friendliness
5. Real-world enough to teach core ideas

## Current Modules

- `cli.py`
  - parses commands
  - validates inputs
  - orchestrates crawl, search, stats, and reset

- `crawl.py`
  - performs synchronous seeded crawling
  - enforces host scope
  - respects `robots.txt`

- `extract.py`
  - parses HTML
  - extracts title, visible text, and links

- `normalize.py`
  - normalizes URLs
  - normalizes whitespace
  - tokenizes searchable text

- `storage.py`
  - creates the SQLite schema
  - reads stats
  - deletes local state

- `index.py`
  - rebuilds the local inverted index from crawled pages

- `ranking.py`
  - implements BM25 scoring helpers

- `search.py`
  - retrieves postings
  - computes document scores
  - returns ranked search results

- `snippet.py`
  - generates short text excerpts for results

- `models.py`
  - defines small data objects shared between modules

## SQLite Schema

### `documents`
Stores one row per crawled page.

Fields:
- `id`
- `url`
- `title`
- `content`
- `content_length`
- `crawled_at`

### `terms`
Stores one row per normalized term.

Fields:
- `id`
- `term`

### `postings`
Stores the inverted index.

Fields:
- `term_id`
- `document_id`
- `term_frequency`

## Search Model

Seeklet currently uses BM25.

For each query:

1. tokenize and normalize query text
2. find indexed terms
3. fetch matching postings
4. compute BM25 contributions in Python
5. sort by descending score
6. return top-k results

This keeps the ranking logic easy to inspect and learn from.

## Deliberate MVP Limits

To keep the project educational and minimal, the MVP does not include:

- JavaScript execution
- asynchronous crawling
- distributed indexing
- PageRank
- fuzzy matching
- phrase or boolean search
- vector search
- a web API
- a browser UI

## Tradeoffs

### Why SQLite?
- built into Python
- easy to inspect locally
- enough for a small educational search engine
- low setup cost for contributors

### Why a Synchronous Crawler?
- easier to understand
- easier to test
- enough for the current scale target

### Why Rebuild the Index on Each Crawl?
- simpler correctness model
- easier for learners to follow
- avoids premature complexity around partial updates

## Future Extension Points

Natural next improvements after the MVP:

- incremental recrawling
- better tokenization and language support
- phrase and boolean queries
- link-analysis signals
- sitemap support
- benchmark scripts
- optional minimal web UI
