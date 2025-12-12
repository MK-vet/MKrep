# Quick Start Guide - Module Enhancement

This guide provides quick steps to enhance any StrepSuis module to reach 70%+ coverage.

## Prerequisites

- Python 3.8+
- pip with editable install support
- pytest and coverage tools

## Step-by-Step Process

### 1. Initial Setup (5 minutes)

```bash
cd separated_repos/{module-name}
pip install -e .[dev]
```

### 2. Baseline Analysis (10 minutes)

```bash
# Run tests and generate coverage report
pytest -v --cov --cov-report=html --cov-report=term

# Open coverage report
# Check htmlcov/index.html in browser
```

**Document baseline**:
- Overall coverage: \_\__%
- Passing tests: \_\_\_
- Failing tests: \_\_\_
- Main gaps: \_\_\_

### 3. Fix Data Dependencies (15-30 minutes)

**Problem**: Many tests fail due to missing data files

**Solution**:

```bash
# Create examples directory
mkdir -p data/examples/

# Copy synthetic data to examples
cp synthetic_data/synthetic_*.csv data/examples/

# Rename if needed
mv data/examples/synthetic_MIC.csv data/examples/MIC.csv
mv data/examples/synthetic_AMR_genes.csv data/examples/AMR_genes.csv

# Run tests again
pytest -v --cov --cov-report=term
```

**Expected impact**: +10-20% coverage, +10-30 passing tests

### 4. Add Config Tests (30 minutes)

Create `tests/test_config_extended.py`:

```python
"""Extended config tests for coverage."""

import pytest
import tempfile
from pathlib import Path
from strepsuis_{module}.config import Config

def test_config_fdr_alpha_lower_bound():
    """Test FDR alpha rejects values <= 0."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(ValueError):
            Config(data_dir=tmpdir, fdr_alpha=0.0)
        with pytest.raises(ValueError):
            Config(data_dir=tmpdir, fdr_alpha=-0.1)

def test_config_fdr_alpha_upper_bound():
    """Test FDR alpha rejects values >= 1."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(ValueError):
            Config(data_dir=tmpdir, fdr_alpha=1.0)
        with pytest.raises(ValueError):
            Config(data_dir=tmpdir, fdr_alpha=1.5)

def test_config_bootstrap_iterations_minimum():
    """Test bootstrap iterations minimum."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(ValueError):
            Config(data_dir=tmpdir, bootstrap_iterations=50)
        
        # Should work
        config = Config(data_dir=tmpdir, bootstrap_iterations=100)
        assert config.bootstrap_iterations == 100

def test_config_output_dir_created():
    """Test output directory is created."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "output"
        config = Config(data_dir=tmpdir, output_dir=str(output_dir))
        assert output_dir.exists()

def test_config_from_dict():
    """Test Config.from_dict method."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dict = {
            "data_dir": tmpdir,
            "bootstrap_iterations": 1000,
            "fdr_alpha": 0.01
        }
        config = Config.from_dict(config_dict)
        assert config.bootstrap_iterations == 1000
        assert config.fdr_alpha == 0.01
```

**Expected impact**: +5-10% config coverage

### 5. Add CLI Tests (30 minutes)

Create `tests/test_cli_extended.py`:

```python
"""Extended CLI tests for coverage."""

import subprocess
from pathlib import Path

def test_cli_help():
    """Test --help flag works."""
    result = subprocess.run(
        ['strepsuis-{module}', '--help'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'usage' in result.stdout.lower()

def test_cli_version():
    """Test --version flag works."""
    result = subprocess.run(
        ['strepsuis-{module}', '--version'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0

def test_cli_invalid_option():
    """Test invalid option shows error."""
    result = subprocess.run(
        ['strepsuis-{module}', '--invalid-option'],
        capture_output=True,
        text=True
    )
    assert result.returncode != 0
```

**Expected impact**: +5-15% CLI coverage

### 6. Verify Mathematical Validations (15 minutes)

Check that `tests/test_statistical_validation.py` exists and has tests for:

- [ ] Chi-square test (scipy comparison)
- [ ] Fisher exact test (scipy comparison)
- [ ] FDR correction (statsmodels comparison)
- [ ] Bootstrap CI (coverage verification)
- [ ] Edge cases (empty data, zero variance)
- [ ] Numerical stability
- [ ] Reproducibility

If missing, add validation tests:

```python
"""Statistical validation tests."""

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, fisher_exact
from statsmodels.stats.multitest import multipletests

def test_chi_square_matches_scipy():
    """Validate chi-square against scipy."""
    table = pd.DataFrame([[50, 30], [20, 40]])
    
    # Our implementation
    chi2_ours, p_ours, _ = our_chi_square_function(table)
    
    # Scipy reference
    chi2_ref, p_ref, _, _ = chi2_contingency(table)
    
    # Validate to 5 decimal places
    np.testing.assert_almost_equal(chi2_ours, chi2_ref, decimal=5)
    np.testing.assert_almost_equal(p_ours, p_ref, decimal=5)
```

### 7. Re-run Tests (5 minutes)

```bash
# Run all tests
pytest -v --cov --cov-report=html --cov-report=term

# Check specific coverage
pytest --cov=strepsuis_{module} --cov-report=term
```

### 8. Update Documentation (15 minutes)

**Update `TESTING.md`**:

```markdown
## Current Coverage

**Overall**: X%

### Component Breakdown

| Component | Coverage |
|-----------|----------|
| config.py | X% |
| cli.py | X% |
| analyzer.py | X% |
| {core}.py | X% |

**Tests**: X passing, Y failing, Z skipped
**Last Updated**: YYYY-MM-DD
```

**Update `README.md`** if needed:
- Verify installation instructions work
- Verify usage examples are accurate
- Update badges if applicable

### 9. Commit Changes

```bash
git add .
git commit -m "Enhanced {module}: Added tests, fixed data dependencies

- Added example data files from synthetic data
- Added extended config validation tests
- Added extended CLI tests
- Verified mathematical validations
- Updated documentation
- Coverage: X% → Y% (+Z%)"
```

## Expected Results

Following this guide should achieve:

- ✅ +20-30% overall coverage
- ✅ +15-40 passing tests
- ✅ Config coverage: 75-85%
- ✅ CLI coverage: 70-90%
- ✅ Mathematical validations verified
- ✅ Documentation updated

## Troubleshooting

### Tests still failing?

**Check data files**:
```bash
ls -la data/examples/
# Should show MIC.csv, AMR_genes.csv, etc.
```

**Check test logs**:
```bash
pytest -v -s tests/test_failing_test.py
# -s shows stdout/stderr
```

### Coverage not increasing?

**Identify untested code**:
```bash
pytest --cov --cov-report=html
# Open htmlcov/index.html
# Look for red/pink lines (untested)
```

**Focus on testable components**:
- Config validation
- CLI parsing
- Data loading
- Core algorithms (unit tests)

**Avoid low-value areas**:
- Visualization code (hard to test)
- Excel formatting (low priority)
- Legacy code (if any)

### Import errors?

**Reinstall in dev mode**:
```bash
pip install -e .[dev] --force-reinstall
```

## Quick Wins

**Fastest improvements**:

1. ✅ **Fix data files** → +10-20% coverage (15 min)
2. ✅ **Add config tests** → +5-10% coverage (30 min)
3. ✅ **Add CLI tests** → +5-15% coverage (30 min)
4. ✅ **Verify validations exist** → 0% coverage, high confidence (15 min)

**Total time**: 90-120 minutes  
**Total impact**: +20-45% coverage

## Success Criteria

✅ Overall coverage ≥ 70%  
✅ Config coverage ≥ 85%  
✅ CLI coverage ≥ 70%  
✅ Core algorithm coverage ≥ 70%  
✅ All mathematical validations passing  
✅ Documentation updated

---

**Based on**: strepsuis-mdr enhancement (38% → 67% coverage)  
**Time tested**: 2025-12-12  
**Success rate**: 76% of goal achieved
