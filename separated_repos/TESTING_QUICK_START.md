# Testing Quick Start

Quick reference for running tests in the StrepSuis Suite.

## Quick Commands

```bash
# Navigate to module
cd separated_repos/strepsuis-mdr

# Install dev dependencies
pip install -e .[dev]

# Run fast tests
pytest -m "not slow" -v

# Run all tests
pytest -v

# With coverage
pytest --cov --cov-report=html
```

## Test Types

| Command | Purpose | Time |
|---------|---------|------|
| `pytest -m "not slow"` | CI/development | ~5s |
| `pytest` | Full suite | ~30s |
| `pytest tests/test_end_to_end.py` | E2E only | ~10s |
| `pytest --cov` | With coverage | ~30s |

## Coverage Report

```bash
pytest --cov --cov-report=html
# Open htmlcov/index.html
```

## Before Committing

```bash
pre-commit run --all-files
pytest -m "not slow" -v
```

## Debugging

```bash
pytest -vv --tb=long  # Verbose
pytest -x             # Stop on first failure
pytest --pdb          # Debugger
pytest -s             # Show prints
```

## Module Commands

```bash
# strepsuis-mdr
cd separated_repos/strepsuis-mdr && pytest -v

# strepsuis-amrvirkm
cd separated_repos/strepsuis-amrvirkm && pytest -v

# strepsuis-genphennet
cd separated_repos/strepsuis-genphennet && pytest -v

# strepsuis-phylotrait
cd separated_repos/strepsuis-phylotrait && pytest -v
```

## All Modules

```bash
cd separated_repos
./run_all_tests.sh
```

---

For comprehensive documentation, see [TESTING.md](TESTING.md).
