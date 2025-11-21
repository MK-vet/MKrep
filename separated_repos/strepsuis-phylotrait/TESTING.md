# Testing Guide for strepsuis-phylotrait

This document describes how to run tests locally and in CI/CD for the strepsuis-phylotrait package.

## Overview

The test suite includes:
- **Unit tests**: Test individual functions and classes
- **Integration tests**: Test complete workflows with real data
- **Workflow tests**: End-to-end validation of analysis pipelines

## Quick Start

### Install Development Dependencies

```bash
pip install -e .[dev]
```

### Run All Tests

```bash
pytest
```

### Run with Coverage Report

```bash
pytest --cov --cov-report=term --cov-report=html
```

Then open `htmlcov/index.html` in your browser to view the detailed coverage report.

## Test Categories

### Unit Tests
Fast tests that validate individual components:

```bash
pytest -m unit -v
```

### Integration Tests
Tests that use real example data:

```bash
pytest -m integration -v
```

### Workflow Tests
Complete end-to-end pipeline tests (may be slower):

```bash
pytest tests/test_workflow.py -v
```

### Exclude Slow Tests
For rapid iteration during development:

```bash
pytest -m "not slow" -v
```

## Running Specific Test Files

```bash
# Test basic functionality
pytest tests/test_basic.py -v

# Test configuration
pytest tests/test_config.py -v

# Test CLI interface
pytest tests/test_cli.py -v

# Test analyzer functionality
pytest tests/test_analyzer.py -v

# Test data validation
pytest tests/test_data_validation.py -v

# Test complete workflows
pytest tests/test_workflow.py -v
```

## Coverage Requirements

- **Target Coverage**: 60% minimum for CI/CD
- **Recommended Coverage**: 80%+ for production code

### Generate Coverage Report

```bash
# Terminal report
pytest --cov --cov-report=term-missing

# HTML report
pytest --cov --cov-report=html
open htmlcov/index.html

# XML report (for CI tools)
pytest --cov --cov-report=xml
```

### Coverage by Module

Check coverage for specific modules:

```bash
pytest --cov=strepsuis_phylotrait --cov-report=term-missing
```

## Local Development Workflow

### 1. Quick Check (Fast Tests Only)
```bash
pytest -m "not slow" --cov-fail-under=0
```

### 2. Full Test Suite
```bash
pytest --cov
```

### 3. Pre-Commit Validation
```bash
pre-commit run --all-files
pytest -v
```

## CI/CD Testing

Tests run automatically on:
- Pull requests to main branch
- Manual workflow dispatch
- Release creation

### GitHub Actions Workflow

The CI runs:
1. Code quality checks (black, isort, ruff, mypy)
2. Full test suite with coverage
3. Coverage upload to Codecov

### Optimizing CI Minutes

To minimize GitHub Actions usage:
- Fast tests run on every PR
- Slow/integration tests can be marked with `@pytest.mark.slow`
- Docker builds only on releases or manual dispatch
- Coverage reports only uploaded once per test run

## Test Data

Example data is located in `data/examples/`:
- `MIC.csv`: Minimum Inhibitory Concentration data
- `AMR_genes.csv`: Antimicrobial resistance gene profiles
- Additional CSV files for comprehensive testing

### Using Custom Test Data

```python
import pytest
from pathlib import Path

@pytest.fixture
def custom_data(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    # Add your test data here
    return data_dir
```

## Debugging Failed Tests

### Verbose Output
```bash
pytest -vv -s
```

### Show Print Statements
```bash
pytest -s
```

### Run Specific Test
```bash
pytest tests/test_workflow.py::test_data_loading_workflow -v
```

### Drop into Debugger on Failure
```bash
pytest --pdb
```

### Show Full Traceback
```bash
pytest --tb=long
```

## Writing New Tests

### Test File Naming
- Test files: `test_*.py`
- Test functions: `test_*`
- Test classes: `Test*`

### Example Test

```python
import pytest
from strepsuis_phylotrait.analyzer import PhyloTraitAnalyzer
from strepsuis_phylotrait.config import Config

@pytest.mark.integration
def test_my_workflow(tmp_path):
    """Test description."""
    # Setup
    config = Config(
        data_dir="data/examples",
        output_dir=str(tmp_path / "output")
    )
    
    # Execute
    analyzer = PhyloTraitAnalyzer(config=config)
    
    # Assert
    assert analyzer.config is not None
```

### Test Markers

Use markers to categorize tests:

```python
@pytest.mark.unit  # Fast unit test
@pytest.mark.integration  # Integration test with real data
@pytest.mark.slow  # Long-running test
@pytest.mark.local  # Local development only
```

## Performance Considerations

### Test Speed Optimization

1. **Use minimal test data**: Reduce dataset size for faster tests
2. **Reduce bootstrap iterations**: Use 100 instead of 500+ for tests
3. **Mock external dependencies**: Avoid network calls or heavy computations
4. **Parallel testing**: Use pytest-xdist for faster execution

```bash
# Run tests in parallel
pip install pytest-xdist
pytest -n auto
```

## Continuous Integration

### Pre-commit Hooks

Install and run pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

This runs:
- black (formatting)
- isort (import sorting)
- ruff (linting)
- mypy (type checking)
- bandit (security checks)

### Local CI Simulation

Simulate the full CI pipeline locally:

```bash
# Code quality
black --check --line-length=100 .
isort --check --profile=black --line-length=100 .
ruff check .
mypy --ignore-missing-imports --no-strict-optional .

# Tests
pytest --cov --cov-report=xml --cov-report=term
```

## Troubleshooting

### Common Issues

**Issue**: Tests fail with "FileNotFoundError"
- **Solution**: Ensure example data exists in `data/examples/`

**Issue**: Coverage too low
- **Solution**: Add workflow tests or integration tests that exercise real code paths

**Issue**: Tests timeout
- **Solution**: Mark slow tests with `@pytest.mark.slow` and reduce test data size

**Issue**: Import errors
- **Solution**: Install package in editable mode: `pip install -e .[dev]`

## Coverage Goals

### Priority Areas for Testing

1. **High Priority** (>90% coverage):
   - Core analysis functions
   - Data validation
   - Configuration handling
   - Error handling

2. **Medium Priority** (>70% coverage):
   - Utility functions
   - Reporting functions
   - CLI interface

3. **Lower Priority** (>50% coverage):
   - Visualization code
   - Interactive components

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [Coverage.py documentation](https://coverage.readthedocs.io/)
- [Codecov](https://codecov.io/)

## Getting Help

If you encounter issues with testing:
1. Check this guide
2. Review existing tests in `tests/`
3. Check CI logs in GitHub Actions
4. Open an issue on GitHub

## Contributing

When contributing:
1. Write tests for new features
2. Maintain or improve coverage
3. Run full test suite before submitting PR
4. Update documentation if adding new test categories
