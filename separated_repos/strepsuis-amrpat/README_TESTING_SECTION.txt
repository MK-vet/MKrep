
## Testing

This package includes a comprehensive test suite covering unit tests, integration tests, and full workflow validation.

### Quick Start

```bash
# Install development dependencies
pip install -e .[dev]

# Run all tests
pytest

# Run with coverage
pytest --cov --cov-report=html
```

### Test Categories

- **Unit tests**: Fast tests of individual components
- **Integration tests**: Tests using real example data
- **Workflow tests**: End-to-end pipeline validation

### Running Specific Tests

```bash
# Fast tests only (for development)
pytest -m "not slow"

# Integration tests only
pytest -m integration

# Specific test file
pytest tests/test_workflow.py -v
```

For detailed testing instructions, see [TESTING.md](TESTING.md).

### Coverage

Current test coverage: See badge above or run `pytest --cov --cov-report=html`.

Target coverage: 60% minimum, 80%+ recommended for production.

