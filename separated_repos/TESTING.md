# Testing Guide

This document provides comprehensive testing documentation for the StrepSuis Suite bioinformatics tools.

## Overview

The StrepSuis Suite implements a 3-level testing strategy across all five modules, with 400+ tests ensuring scientific validity and software reliability.

## Test Architecture

### Testing Levels

| Level | Description | Coverage Focus | Execution Time |
|-------|-------------|----------------|----------------|
| Unit | Individual component validation | Config, utilities | <1 second |
| Integration | Multi-component workflows | Data loading, pipelines | 1-5 seconds |
| End-to-End | Complete analysis pipelines | Full workflow validation | 2-30 seconds |

### Coverage Summary

| Module | Total Tests | Coverage | Critical Paths |
|--------|-------------|----------|----------------|
| strepsuis-amrpat | 110+ | 62% | 85-100% |
| strepsuis-amrvirkm | 100+ | 50% | 85-100% |
| strepsuis-genphen | 100+ | 50% | 85-100% |
| strepsuis-genphennet | 100+ | 50% | 85-100% |
| strepsuis-phylotrait | 90+ | 50% | 85-100% |

**Critical Paths** include configuration validation (100%), CLI interfaces (85-89%), and analyzer orchestration (85-86%).

## Running Tests

### Quick Start

```bash
# Navigate to a module
cd separated_repos/strepsuis-amrpat

# Install development dependencies
pip install -e .[dev]

# Run all tests
pytest -v

# Run with coverage
pytest --cov --cov-report=html
```

### Test Commands

```bash
# Fast tests (excludes slow tests, suitable for CI)
pytest -m "not slow" -v

# Full test suite (includes all tests)
pytest -v

# End-to-end tests only
pytest tests/test_end_to_end.py -v

# Unit tests only
pytest -m unit -v

# Integration tests only
pytest -m integration -v

# Specific test file
pytest tests/test_config.py -v

# Single test function
pytest tests/test_workflow.py::test_data_loading_workflow -v
```

### Coverage Reports

```bash
# Terminal coverage report
pytest --cov --cov-report=term

# HTML coverage report
pytest --cov --cov-report=html
# Open htmlcov/index.html in browser

# XML coverage report (for CI integration)
pytest --cov --cov-report=xml
```

## Test Data

### Mini Datasets (CI)

Mini datasets contain 10 strains from real example data and are designed for fast CI execution:

- **Location:** Generated in test fixtures from `examples/` data
- **Execution Time:** <5 seconds per module
- **Purpose:** Fast feedback, all code paths exercised
- **Usage:** Default for `pytest -m "not slow"`

### Full Datasets (Local)

Full datasets contain 92 strains representing complete example data for comprehensive validation:

- **Location:** `examples/` directory in each module
- **Execution Time:** 30-60 seconds per module
- **Purpose:** Publication-ready output validation
- **Usage:** Included with `pytest -v` (full suite)

### Data Files

Each module's `examples/` directory contains:

| File | Description | Records |
|------|-------------|---------|
| MIC.csv | Minimum inhibitory concentration data | 92 strains |
| AMR_genes.csv | Antimicrobial resistance gene profiles | 92 strains |
| Virulence.csv | Virulence factor data | 92 strains |
| MLST.csv | Sequence types | 92 strains |
| Serotype.csv | Serological classification | 92 strains |
| Plasmid.csv | Plasmid replicons | 92 strains |
| MGE.csv | Mobile genetic elements | 92 strains |
| Snp_tree.newick | Phylogenetic tree (phylo modules) | 92 taxa |

## Test Categories

### Unit Tests

Unit tests validate individual components in isolation:

```python
def test_config_defaults():
    """Validate default configuration values."""
    config = Config()
    assert config.bootstrap_iterations > 0
    assert 0 < config.fdr_alpha < 1
    assert config.random_seed is not None
```

**Files:** `test_config.py`, `test_utilities.py`, `test_basic.py`

### Integration Tests

Integration tests validate component interactions:

```python
@pytest.mark.integration
def test_data_loading_workflow(mini_dataset):
    """Validate data loading across multiple files."""
    analyzer = get_analyzer(config)
    data = analyzer.load_data()
    assert "MIC" in data
    assert "AMR_genes" in data
```

**Files:** `test_integration.py`, `test_workflow.py`

### End-to-End Tests

End-to-end tests validate complete analysis pipelines:

```python
def test_complete_pipeline(mini_dataset):
    """Validate full analysis from input to output."""
    analyzer = get_analyzer(config)
    results = analyzer.run()
    
    assert results["status"] == "success"
    assert len(results["html_reports"]) > 0
    assert len(results["excel_reports"]) > 0
```

**Files:** `test_end_to_end.py`

### CLI Tests

CLI tests validate command-line interfaces:

```python
def test_cli_help():
    """Validate CLI help output."""
    result = subprocess.run(
        ["strepsuis-amrpat", "--help"],
        capture_output=True
    )
    assert result.returncode == 0
    assert b"Usage:" in result.stdout
```

**Files:** `test_cli.py`

## CI/CD Integration

### GitHub Actions

Tests execute automatically on:
- Pull requests to main branch
- Manual workflow dispatch
- Release creation

Workflow configuration excludes slow tests in CI:

```yaml
- name: Run tests
  run: pytest -m "not slow" --cov --cov-report=xml
```

### Optimization

- **Python Versions:** 3.8, 3.11, 3.12
- **Pip Caching:** Enabled for faster builds
- **Docker Builds:** Only on releases
- **Estimated CI Time:** 3-5 minutes per module
- **Monthly Usage:** 30-50 minutes total

## Local Development Workflow

### Before Committing

```bash
# 1. Run pre-commit hooks
pre-commit run --all-files

# 2. Run fast tests
pytest -m "not slow" -v

# 3. Check coverage
pytest --cov --cov-report=term

# 4. Run full suite (optional)
pytest -v
```

### Debugging Failed Tests

```bash
# Verbose output with full traceback
pytest -vv --tb=long

# Stop at first failure
pytest -x

# Drop into debugger on failure
pytest --pdb

# Show print statements
pytest -s
```

## Writing Tests

### Test Structure

Follow this pattern for new tests:

```python
import pytest
from module_name.config import Config
from module_name.analyzer import get_analyzer


@pytest.fixture
def config(tmp_path):
    """Provide test configuration."""
    return Config(
        data_dir="examples/",
        output_dir=str(tmp_path),
        random_seed=42
    )


def test_feature_name(config):
    """Description of what is being tested."""
    # Arrange
    analyzer = get_analyzer(config)
    
    # Act
    result = analyzer.some_method()
    
    # Assert
    assert result is not None
    assert result["key"] == expected_value
```

### Test Markers

Use pytest markers to categorize tests:

```python
@pytest.mark.unit
def test_config_validation():
    """Fast unit test."""
    pass

@pytest.mark.integration
def test_data_loading():
    """Integration test using example data."""
    pass

@pytest.mark.slow
def test_full_analysis():
    """Slow test using complete dataset."""
    pass
```

### Fixtures

Common fixtures are defined in `conftest.py`:

```python
@pytest.fixture
def mini_dataset(tmp_path):
    """Create mini dataset for fast testing."""
    # Copy first 10 rows of example data
    pass

@pytest.fixture
def full_dataset(tmp_path):
    """Use complete example dataset."""
    # Copy full example data
    pass
```

## Troubleshooting

### Common Issues

**Tests fail with FileNotFoundError:**
```bash
# Verify example data exists
ls examples/*.csv
```

**Coverage lower than expected:**
```bash
# Generate HTML report and examine uncovered lines
pytest --cov --cov-report=html
# Open htmlcov/index.html
```

**Tests timeout:**
```bash
# Increase timeout or mark as slow
pytest --timeout=60
# Or mark the test: @pytest.mark.slow
```

**Import errors:**
```bash
# Reinstall in development mode
pip install -e .[dev]
```

### Performance Optimization

```bash
# Parallel execution (requires pytest-xdist)
pip install pytest-xdist
pytest -n auto

# Run only failed tests from last run
pytest --lf

# Run failed tests first, then rest
pytest --ff
```

## Coverage Analysis

### Component Coverage

| Component | Target | Typical |
|-----------|--------|---------|
| Config modules | 95%+ | 100% |
| CLI interfaces | 85%+ | 85-89% |
| Analyzer orchestration | 85%+ | 85-86% |
| Utility functions | 80%+ | 80-100% |
| Core analysis | 40%+ | 10-60% |

### Coverage Rationale

Core analysis modules show lower coverage due to:
- Complex statistical algorithms requiring extensive mocking
- Interactive components difficult to test in isolation
- Visualization code with external dependencies

These algorithms are validated through end-to-end tests using real data.

## Module-Specific Notes

### strepsuis-amrpat
- Tests MDR classification, co-occurrence analysis, network construction
- Validates bootstrap resampling and association rules

### strepsuis-amrvirkm
- Tests K-modes clustering, silhouette optimization
- Validates MCA dimensionality reduction

### strepsuis-genphen
- Requires tree file (Snp_tree.newick) for phylogenetic tests
- Tests tree-aware clustering and trait profiling

### strepsuis-genphennet
- Tests network construction and community detection
- Validates information theory metrics

### strepsuis-phylotrait
- Requires tree file for all tests
- Tests phylogenetic diversity calculations

## Automation Scripts

Scripts in `separated_repos/` for test automation:

```bash
# Generate coverage reports for all modules
python generate_coverage_badge.py

# Generate all coverage reports
./generate_coverage_reports.sh

# Run all module tests
./run_all_tests.sh
```

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- Module-specific `TESTING.md` files in each repository

---

**Total Tests:** 400+  
**Coverage Target:** 50-62% total, 85-100% critical paths  
**Test Execution:** <5 minutes for CI suite
