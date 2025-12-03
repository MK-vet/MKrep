# Testing Guide for StrepSuis Analyzer

This document describes how to run tests locally and in CI/CD for the StrepSuis Analyzer package.

## Overview

The test suite includes:
- **Unit tests**: Test individual functions and classes
- **Integration tests**: Test complete workflows with real data
- **Workflow tests**: End-to-end validation of analysis pipelines
- **Statistical validation tests**: Verify mathematical correctness
- **CLI tests**: Test command-line interface
- **Configuration tests**: Test configuration handling

## Test Data Strategy

### Example Data Location
Real example data is located in `data/` and `examples/` directories:
- `data/Virulence.csv` - Binary virulence factor profiles for *S. suis* strains

### Mini Datasets for CI
For fast CI execution, tests automatically create mini synthetic datasets:
- **Mini dataset**: 10-50 synthetic strains
- **Execution time**: <10 seconds for full test suite
- **Purpose**: Fast validation in GitHub Actions

### Full Datasets for Local Testing
Full example datasets are used for comprehensive validation:
- **Full dataset**: Real data with all strains
- **Execution time**: 30-60 seconds
- **Purpose**: Complete validation before releases
- **Marked as**: `@pytest.mark.slow` (skipped in CI)

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

### Statistical Validation Tests
Tests that verify mathematical correctness:

```bash
pytest tests/test_statistical_validation.py -v
```

## Running Specific Test Files

```bash
# Basic functionality tests
pytest tests/test_basic.py -v

# Analyzer core tests
pytest tests/test_analyzer.py -v

# CLI tests
pytest tests/test_cli.py -v

# Configuration tests
pytest tests/test_config.py -v

# Integration tests
pytest tests/test_integration.py -v

# End-to-end tests
pytest tests/test_end_to_end.py -v
```

## Coverage Targets

Current coverage targets:
- **Minimum**: 35% (enforced by CI)
- **Target**: 80% for core modules
- **Goal**: 95%+ for statistical functions

View coverage with:
```bash
pytest --cov=strepsuis_analyzer --cov-report=html
open htmlcov/index.html
```

## Test Fixtures

Common test fixtures are defined in `tests/conftest.py`:
- `tmp_path` - Temporary directory for test outputs
- `sample_data` - Sample binary trait data
- `sample_tree` - Sample phylogenetic tree (Newick format)

## Reproducibility

All tests use fixed random seeds (default: 42) to ensure:
- Deterministic results across runs
- Reproducible CI outcomes
- Consistent baseline comparisons

## Continuous Integration

GitHub Actions runs tests on:
- Python 3.8, 3.11, 3.12
- Ubuntu latest
- On pull requests and releases

Workflow file: `.github/workflows/test.yml`

## Local Development Tips

1. **Fast iteration**: Use `-m "not slow"` to skip slow tests
2. **Focus on changed code**: Run specific test files related to your changes
3. **Check coverage**: Use `--cov` to ensure new code is tested
4. **Fix failures immediately**: Don't let tests accumulate failures

## Debugging Failed Tests

### Verbose output
```bash
pytest -vv tests/test_analyzer.py::test_specific_function
```

### Show print statements
```bash
pytest -s tests/test_analyzer.py
```

### Stop on first failure
```bash
pytest -x
```

### Drop into debugger on failure
```bash
pytest --pdb
```

## Test Quality Standards

All tests should:
- ✅ Have clear, descriptive names
- ✅ Test one thing per test function
- ✅ Use appropriate fixtures and markers
- ✅ Clean up temporary files
- ✅ Be deterministic (same input → same output)
- ✅ Include assertions with meaningful error messages

## Adding New Tests

When adding new features:
1. Write tests first (TDD approach recommended)
2. Cover both success and failure cases
3. Add edge case tests
4. Use appropriate markers (`@pytest.mark.unit`, etc.)
5. Update this documentation if adding new test categories

## Common Issues

### Missing Dependencies
```bash
pip install -e .[dev]
```

### Permission Errors
Ensure test directories have write permissions

### Slow Tests
Mark slow tests with `@pytest.mark.slow` so they can be skipped in CI

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- GitHub Actions workflow: `.github/workflows/test.yml`
