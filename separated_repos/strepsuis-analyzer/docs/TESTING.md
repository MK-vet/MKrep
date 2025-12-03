# Testing Guide - StrepSuisAnalyzer

## Test Coverage

StrepSuisAnalyzer maintains comprehensive test coverage:

- **Overall Coverage**: >85%
- **Critical Components**: >95%
  - `data_validator.py`
  - `statistical_analysis.py`
  - `phylogenetic_utils.py`
- **Mathematical Validation**: 100%

## Test Structure

```
tests/
├── conftest.py                      # Pytest fixtures
├── test_data_validator.py           # Data validation tests
├── test_statistical_analysis.py     # Statistical function tests
├── test_phylogenetic_utils.py       # Phylogenetic analysis tests
├── test_visualization.py            # Visualization tests
├── test_mathematical_validation.py  # 100% mathematical property tests
├── test_synthetic_data.py           # Synthetic data validation
└── test_integration.py              # End-to-end integration tests
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_statistical_analysis.py

# Run specific test
pytest tests/test_statistical_analysis.py::TestStatisticalAnalyzer::test_compute_correlation_pearson
```

### Coverage Reports

```bash
# Run with coverage
pytest --cov=strepsuis_analyzer --cov-report=html

# View HTML coverage report
open htmlcov/index.html

# Run with coverage and terminal output
pytest --cov=strepsuis_analyzer --cov-report=term-missing
```

### Test Categories

```bash
# Run only mathematical validation tests
pytest -m mathematical

# Run only synthetic data tests
pytest -m synthetic

# Run only integration tests
pytest -m integration

# Run unit tests only
pytest -m unit

# Skip slow tests
pytest -m "not slow"
```

## Test Categories Explained

### Unit Tests (`@pytest.mark.unit`)
Test individual functions and methods in isolation.

```python
def test_compute_correlation_pearson(self, correlation_data_perfect):
    analyzer = StatisticalAnalyzer()
    corr, pval = analyzer.compute_correlation(
        correlation_data_perfect["x"],
        correlation_data_perfect["y"],
        method="pearson"
    )
    assert abs(corr - 1.0) < 0.001
```

### Mathematical Validation Tests (`@pytest.mark.mathematical`)
Test mathematical properties and invariants with 100% coverage.

**Tested Properties:**
- Entropy bounds: 0 ≤ H(X) ≤ log₂(n)
- Mutual information symmetry: MI(X,Y) = MI(Y,X)
- Cramér's V bounds: 0 ≤ V ≤ 1
- Correlation bounds: -1 ≤ r ≤ 1
- P-value bounds: 0 ≤ p ≤ 1
- Robinson-Foulds distance: RF ≥ 0

```python
@pytest.mark.mathematical
def test_entropy_bounds(self):
    analyzer = StatisticalAnalyzer(random_state=42)
    n = 8
    uniform = np.repeat(range(n), 100)
    entropy = analyzer.compute_entropy(uniform)
    
    assert entropy >= 0, "Entropy must be non-negative"
    assert entropy <= np.log2(n) + 0.01, f"Entropy must be <= log2({n})"
```

### Synthetic Data Tests (`@pytest.mark.synthetic`)
Tests with carefully constructed synthetic datasets with known ground truth.

```python
@pytest.mark.synthetic
def test_perfect_correlation_synthetic(self):
    analyzer = StatisticalAnalyzer(random_state=42)
    x = np.linspace(0, 100, 1000)
    y = 3 * x + 5
    
    corr, pval = analyzer.compute_correlation(x, y, method="pearson")
    
    assert abs(corr - 1.0) < 0.0001, "Perfect correlation should be exactly 1.0"
```

### Integration Tests (`@pytest.mark.integration`)
End-to-end workflow tests combining multiple components.

```python
@pytest.mark.integration
def test_complete_pipeline(self, sample_binary_data, sample_numeric_data):
    # Validate → ETL → Analyze → Report
    validator = DataValidator()
    etl = ETLOperations()
    analyzer = StatisticalAnalyzer()
    report = ReportGenerator()
    
    # ... complete workflow
```

## Coverage Requirements

### Minimum Coverage Thresholds

| Component | Minimum Coverage | Target Coverage |
|-----------|------------------|----------------|
| Overall | 80% | 90% |
| Critical Modules | 95% | 100% |
| Mathematical Functions | 100% | 100% |
| Data Validators | 95% | 100% |
| Statistical Analysis | 95% | 100% |
| Phylogenetic Utils | 95% | 100% |

### Critical Components

The following components must maintain >95% coverage:
- `data_validator.py`
- `statistical_analysis.py`
- `phylogenetic_utils.py`

## Continuous Integration

### GitHub Actions Workflow

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -e .[dev]
      - name: Run tests
        run: |
          pytest --cov=strepsuis_analyzer --cov-fail-under=80
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Writing New Tests

### Test Template

```python
"""Tests for new_module."""

import pytest
import numpy as np
from strepsuis_analyzer.new_module import NewClass


class TestNewClass:
    """Test suite for NewClass."""

    def test_init(self):
        """Test initialization."""
        obj = NewClass()
        assert isinstance(obj, NewClass)

    def test_method_with_valid_input(self, fixture_data):
        """Test method with valid input."""
        obj = NewClass()
        result = obj.method(fixture_data)
        
        assert result is not None
        assert isinstance(result, expected_type)

    def test_method_with_invalid_input(self):
        """Test method with invalid input."""
        obj = NewClass()
        
        with pytest.raises(ValueError):
            obj.method(invalid_data)

    @pytest.mark.mathematical
    def test_mathematical_property(self):
        """Test mathematical invariant."""
        obj = NewClass()
        result = obj.compute_metric(data)
        
        assert 0 <= result <= 1, "Metric must be in [0, 1]"
```

### Best Practices

1. **Use Descriptive Names**: Test names should clearly describe what is being tested
2. **One Assertion Per Concept**: Keep tests focused on single behaviors
3. **Use Fixtures**: Leverage pytest fixtures for reusable test data
4. **Test Edge Cases**: Include tests for boundary conditions
5. **Test Error Handling**: Verify exceptions are raised appropriately
6. **Document Expected Behavior**: Use docstrings to explain test purpose

## Debugging Failed Tests

```bash
# Run with detailed output
pytest -vv

# Show print statements
pytest -s

# Drop into debugger on failure
pytest --pdb

# Show local variables on failure
pytest -l

# Run last failed tests
pytest --lf

# Run failed tests first
pytest --ff
```

## Performance Testing

```bash
# Show slowest tests
pytest --durations=10

# Mark slow tests
@pytest.mark.slow
def test_expensive_operation():
    ...

# Skip slow tests in CI
pytest -m "not slow"
```

## Test Data

Test fixtures are defined in `conftest.py`:

```python
@pytest.fixture
def sample_binary_data():
    """Create sample binary data for testing."""
    np.random.seed(42)
    return pd.DataFrame(
        np.random.randint(0, 2, size=(50, 10)),
        columns=[f"gene_{i}" for i in range(10)]
    )
```

## Troubleshooting

### Common Issues

**Import errors:**
```bash
# Ensure package is installed in development mode
pip install -e .
```

**Missing dependencies:**
```bash
# Install development dependencies
pip install -e .[dev]
```

**Coverage not detected:**
```bash
# Ensure source directory is correct in pytest.ini
# Coverage should point to installed package name
```

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
