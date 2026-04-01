# Contributing to Seeklet

Thanks for your interest in contributing to Seeklet.

Seeklet is a minimal educational web search engine written in Python. The goal
of the project is not only to work, but to remain:

- small
- readable
- easy to learn from
- easy to run locally
- easy to contribute to

Please keep those goals in mind when proposing changes.

---

## Table of Contents

- [Project principles](#project-principles)
- [Development setup](#development-setup)
- [Run local checks](#run-local-checks)
- [Project workflow](#project-workflow)
- [Coding guidelines](#coding-guidelines)
- [Testing guidelines](#testing-guidelines)
- [Documentation guidelines](#documentation-guidelines)
- [Submitting changes](#submitting-changes)
- [Pull request checklist](#pull-request-checklist)
- [Good first contributions](#good-first-contributions)
- [Questions and discussions](#questions-and-discussions)

---

## Project Principles

Seeklet prioritizes:

1. **Simplicity**
   - prefer straightforward solutions over clever ones

2. **Readability**
   - code should be easy for learners to follow

3. **Minimalism**
   - avoid unnecessary dependencies and abstractions

4. **Educational value**
   - implementation details should remain visible and understandable

5. **Incremental improvement**
   - small focused changes are preferred over large rewrites

When in doubt, choose the option that makes the codebase easier to understand.

---

## Development Setup

### Requirements

- Python **3.12**
- Linux or macOS
- `git`

### Clone the Repository

```bash
git clone https://github.com/YOUR-USER/YOUR-REPO.git
cd YOUR-REPO
```

### Create and Activate a Virtual Environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### Install the Project in Editable Mode

```bash
pip install -e ".[dev]"
```

This installs both the runtime dependencies and the development tools used by
CI.

---

## Run Local Checks

Before opening a pull request, run the same checks used in CI:

```bash
ruff check .
ruff format --check .
python -m pytest -vv
```

These are the canonical local verification commands for the project.

If `ruff format --check .` fails, you can apply formatting with:

```bash
ruff format .
```

If `ruff check .` reports fixable issues, you can try:

```bash
ruff check . --fix
```

Then rerun the full check set.

---

## Project Workflow

### 1. Create a Branch

Create a focused branch for your change:

```bash
git checkout -b feat/short-description
```

Examples:

- `feat/phrase-search`
- `fix/url-normalization`
- `docs/readme-improvements`

### 2. Make Small, Focused Changes

Please avoid mixing unrelated changes in one pull request.

Good:
- one bug fix
- one small feature
- one documentation improvement
- one refactor with tests

Less ideal:
- formatting changes + crawler refactor + README rewrite in one PR

### 3. Run the Checks Locally

```bash
ruff check .
ruff format --check .
python -m pytest -vv
```

### 4. Commit Clearly

Seeklet uses conventional-style commit messages where practical.

Examples:

- `feat: add sitemap discovery`
- `fix: handle empty query terms`
- `docs: clarify crawl scope behavior`
- `test: add snippet edge case coverage`
- `ci: simplify github actions workflow`

### 5. Open a Pull Request

Describe:
- what changed
- why it changed
- how you tested it
- any tradeoffs or limitations

---

## Coding Guidelines

### General Style

- follow **PEP 8**
- keep functions and modules focused
- prefer explicit code over clever shortcuts
- use descriptive names
- avoid premature abstraction
- avoid unnecessary dependencies

### Keep the Code Educational

Seeklet is intentionally designed for learning.

Please prefer code that is:
- easy to inspect
- easy to reason about
- easy to debug

Even if a more advanced pattern is possible, it may not be the right fit if it
hurts clarity.

### Type Hints

Use type hints where they improve clarity.

Examples:
- function parameters
- return values
- small internal data structures

Avoid overcomplicating the code just to satisfy typing.

### Error Handling

Prefer:
- clear validation
- predictable return values
- explicit failures when invariants break

If something should never happen, raising a clear exception is usually better
than silently hiding the problem.

### Dependencies

Add a new dependency only if it clearly improves the project without
undermining its simplicity.

Before adding one, ask:
- can this be handled well with the standard library?
- does this dependency make the project easier to understand?
- is it worth the extra maintenance cost?

---

## Testing Guidelines

### Write Tests for Behavior Changes

If you change behavior, add or update tests.

Typical test areas include:
- URL normalization
- crawling scope rules
- HTML extraction
- indexing
- ranking
- snippets
- CLI behavior

### Prefer Deterministic Tests

Tests should be:
- fast
- deterministic
- isolated

Prefer mocked or local test data over live network dependencies.

### Keep Tests Readable

Tests are part of the learning value of the project. They should help explain
what the code is expected to do.

Use:
- descriptive test names
- small fixtures
- focused assertions

### Run the Full Suite

Always run:

```bash
python -m pytest -vv
```

before submitting a PR.

---

## Documentation Guidelines

Documentation changes are welcome and important.

Please update docs when you change:
- CLI behavior
- setup steps
- architecture
- constraints
- contributor workflows

Relevant files may include:
- `README.md`
- `CONTRIBUTING.md`
- `docs/architecture.md`

Good documentation should be:
- concise
- accurate
- practical
- synced with actual behavior

---

## Submitting Changes

### Before Opening a PR

Please make sure your branch is up to date and all local checks pass.

### Pull Request Content

A good pull request should include:

- a clear summary
- the motivation for the change
- notes about implementation choices
- tests for behavior changes
- doc updates when needed

### Review Expectations

Maintainers will generally review for:

- correctness
- clarity
- scope control
- test coverage
- alignment with project principles

Changes may be asked to be simplified if they introduce unnecessary
complexity.

---

## Pull Request Checklist

Before submitting, confirm:

- [ ] the change is focused and limited in scope
- [ ] the code remains simple and readable
- [ ] `ruff check .` passes
- [ ] `ruff format --check .` passes
- [ ] `python -m pytest -vv` passes
- [ ] tests were added or updated when behavior changed
- [ ] documentation was updated if needed

---

## Good First Contributions

These are especially welcome:

- improving documentation clarity
- expanding tests for edge cases
- improving error messages
- small crawler correctness fixes
- tokenization improvements that preserve simplicity
- benchmark scripts for educational comparison
- small CLI usability improvements
- architecture and code comments that improve understanding

Good first issue labels are a great place to start if they are available in the
repo.

---

## Questions and Discussions

If you are unsure whether a change fits the project, start with:

- a GitHub issue
- a discussion thread
- a draft pull request

That is especially helpful for:
- larger features
- architectural changes
- new dependencies
- changes that may affect the project's educational focus

Early discussion helps keep the project coherent and minimal.

---

## Final Note

Seeklet is intentionally small.

A contribution is successful not only when it adds functionality, but when it
does so while preserving:

- clarity
- simplicity
- maintainability
- educational value

Thanks again for contributing.
