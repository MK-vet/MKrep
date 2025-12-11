# Testing Guide

## Overview

StrepSuisAnalyzer uses pytest for testing with comprehensive coverage of all modules and components.

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── test_app.py             # Main application tests
├── test_components.py      # Component-level tests
├── test_integration.py     # Integration tests
└── test_e2e.py            # End-to-end tests
```

## Running Tests

### Quick Start

```bash
# Install development dependencies
pip install -e .[dev]

# Run all tests
pytest -v

# Run with coverage
pytest --cov=src --cov-report=html -v

# Run fast tests (exclude slow tests)
pytest -m "not slow" -v
```

### Test Categories

Tests are organized by markers:

```bash
# Unit tests only
pytest -m unit -v

# Integration tests only
pytest -m integration -v

# End-to-end tests only
pytest -m e2e -v

# Slow tests
pytest -m slow -v
```

### Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html

# View report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Test Requirements

### Coverage Targets

- **Overall**: 85%+
- **Critical paths**: 95%+
- **UI components**: 80%+

### Test Types

1. **Unit Tests**: Test individual functions and classes
2. **Integration Tests**: Test component interactions
3. **End-to-End Tests**: Test complete workflows

## Writing Tests

### Test Structure

```python
import pytest
from src.strepsuis_analyzer import component

@pytest.fixture
def sample_data():
    """Create sample test data."""
    return pd.DataFrame(...)

def test_component_function(sample_data):
    """Test component function with sample data."""
    result = component.process(sample_data)
    assert result is not None
    assert len(result) > 0
```

### Best Practices

1. **Use Fixtures**: Share common test data
2. **Test Edge Cases**: Empty data, invalid inputs, boundary conditions
3. **Use Descriptive Names**: `test_function_with_valid_input_returns_expected_result`
4. **Mock External Dependencies**: Use `unittest.mock` or `pytest-mock`
5. **Parametrize Tests**: Use `@pytest.mark.parametrize` for multiple inputs

### Example Test

```python
import pytest
import pandas as pd
from src.strepsuis_analyzer.components import statistics

@pytest.mark.unit
def test_calculate_correlation_with_valid_data():
    """Test correlation calculation with valid numeric data."""
    data = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [2, 4, 6, 8, 10]
    })
    result = statistics.calculate_correlation(data)
    assert result['correlation'] == pytest.approx(1.0)

@pytest.mark.integration
def test_full_analysis_pipeline():
    """Test complete analysis pipeline."""
    # Test implementation
    pass
```

## Continuous Integration

Tests are automatically run on:

- Every push to main/develop branches
- All pull requests
- Scheduled nightly builds

## Debugging Tests

```bash
# Verbose output with full traceback
pytest -vv --tb=long

# Stop on first failure
pytest -x

# Drop into debugger on failure
pytest --pdb

# Show print statements
pytest -s
```

## Performance Testing

```bash
# Run performance benchmarks
pytest tests/test_performance.py -v

# Profile test execution
pytest --profile
```

## Test Data

Test data is located in:

```
tests/
├── fixtures/
│   ├── sample_amr.csv
│   ├── sample_mic.csv
│   └── sample_tree.nwk
└── conftest.py
```

## Common Issues

### Import Errors

```bash
# Ensure package is installed in development mode
pip install -e .
```

### Streamlit Tests

Streamlit components require special handling:

```python
from streamlit.testing.v1 import AppTest

def test_streamlit_app():
    at = AppTest.from_file("app.py")
    at.run()
    assert not at.exception
```

## Coverage Goals

| Component | Current | Target |
|-----------|---------|--------|
| Core logic | 85% | 90% |
| Components | 80% | 85% |
| UI elements | 75% | 80% |
| Utilities | 90% | 95% |

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Streamlit testing](https://docs.streamlit.io/library/advanced-features/app-testing)

---

For questions or issues with testing, please open an issue on GitHub.
