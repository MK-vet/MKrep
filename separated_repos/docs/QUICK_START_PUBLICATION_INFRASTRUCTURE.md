# Quick Start Guide - Publication Standards Infrastructure

This guide helps you use the newly created publication standards infrastructure.

## What Was Added

### For Each Module (strepsuis-mdr, strepsuis-amrvirkm, strepsuis-genphennet, strepsuis-phylotrait):

1. **Synthetic Datasets** (`synthetic_data/`)
   - `clean_dataset.csv` - No noise, clear patterns
   - `noisy_dataset.csv` - 10% random bit flips
   - `adversarial_dataset.csv` - Extreme imbalance, perfect correlations
   - `metadata.json` - Ground truth metadata

2. **Colab Notebooks** (`notebooks/`)
   - `{module}_colab_demo.ipynb` - Google Colab demonstration
   - Installs from GitHub, shows basic usage

3. **Deployment Verification** (root level)
   - `deployment_verification.py` - Verify CLI, Docker, Colab
   - Generates logs for publication evidence

4. **Test Infrastructure** (`tests/`)
   - `tests/reports/` - Coverage and test reports
   - `tests/performance/` - Performance benchmarks

5. **Validation Results** (`validation_results/`)
   - Directory for mathematical validation outputs

6. **Updated Configuration**
   - `pytest.ini` - Coverage target raised to 70%

## How to Use

### 1. Run Tests with Coverage

```bash
cd separated_repos/strepsuis-mdr  # or any module
pip install -e .[dev]
pytest --cov --cov-report=html
```

Open `tests/reports/coverage.html/index.html` to view detailed coverage.

### 2. Run Mathematical Validation

```bash
cd separated_repos/strepsuis-mdr  # or any module
python validate_math.py
```

Check `validation_results/` for:
- `validation_results.json` - Detailed results
- `validation_summary.csv` - Summary metrics
- `*.png` - Validation plots

### 3. Verify Deployments

```bash
cd separated_repos/strepsuis-mdr  # or any module
python deployment_verification.py
```

Check:
- `deployment_verification.log` - JSON format
- `deployment_verification.txt` - Human-readable format

### 4. Test Colab Notebook

1. Open notebook in `notebooks/{module}_colab_demo.ipynb`
2. Upload to Google Colab
3. Run all cells
4. Verify package installs and works

### 5. Test Docker Deployment

```bash
cd separated_repos/strepsuis-mdr  # or any module
docker build -t strepsuis-mdr:latest .
docker run --rm strepsuis-mdr:latest --version
```

### 6. Run Performance Tests

```bash
cd separated_repos/strepsuis-mdr  # or any module
pytest -m performance --cov
```

## Directory Structure (Per Module)

```
strepsuis-{module}/
├── synthetic_data/              # NEW: Ground truth validation datasets
│   ├── clean_dataset.csv
│   ├── noisy_dataset.csv
│   ├── adversarial_dataset.csv
│   └── metadata.json
├── notebooks/                   # NEW: Colab demonstrations
│   └── strepsuis-{module}_colab_demo.ipynb
├── tests/
│   ├── reports/                # NEW: Test and coverage reports
│   └── performance/            # NEW: Performance benchmarks
├── validation_results/          # NEW: Validation outputs
├── deployment_verification.py   # NEW: Deployment verification script
├── validate_math.py            # EXISTING: Mathematical validation
├── pytest.ini                  # MODIFIED: Coverage target 70%
└── Dockerfile                  # EXISTING: Verified to install from GitHub
```

## Next Steps for Developers

### To Increase Coverage

1. Identify uncovered lines:
   ```bash
   pytest --cov --cov-report=html
   # Open htmlcov/index.html
   # Click on modules to see uncovered lines in red
   ```

2. Add tests for uncovered functions:
   - Mathematical functions → 100% coverage required
   - CLI functions → >85% coverage target
   - Utility functions → >60% coverage target

3. Run tests to verify:
   ```bash
   pytest --cov
   ```

### To Add Validation Tests

1. Open existing `test_statistical_validation.py`
2. Add new test comparing your function to scipy/statsmodels:
   ```python
   def test_my_function_matches_scipy():
       result_ours = our_function(data)
       result_scipy = scipy.function(data)
       np.testing.assert_almost_equal(result_ours, result_scipy, decimal=5)
   ```

3. Run validation tests:
   ```bash
   pytest tests/test_statistical_validation.py -v
   ```

### To Add Performance Tests

1. Create test in `tests/performance/test_performance_enhanced.py`:
   ```python
   @pytest.mark.performance
   def test_my_function_performance():
       start = time.time()
       result = my_function(large_dataset)
       elapsed = time.time() - start
       assert elapsed < 5.0, f"Took {elapsed:.2f}s, threshold is 5.0s"
   ```

2. Run performance tests:
   ```bash
   pytest -m performance
   ```

## Publication Checklist

Before submitting to Software X, verify:

- [ ] All modules have >70% test coverage
- [ ] All mathematical functions have 100% coverage
- [ ] All validation tests pass
- [ ] All deployment modes verified (CLI, Docker, Colab)
- [ ] All performance thresholds met
- [ ] Documentation includes deployment and validation sections
- [ ] All GitHub workflows pass
- [ ] CITATION.cff is up to date
- [ ] CHANGELOG.md includes latest version
- [ ] All code formatted (black, isort)
- [ ] All linting passes (ruff, mypy)
- [ ] Security scans pass (bandit)

## Automation Scripts

### Run All Quality Checks

```bash
#!/bin/bash
# run_all_qa.sh

cd separated_repos

for module in strepsuis-mdr strepsuis-amrvirkm strepsuis-genphennet strepsuis-phylotrait; do
    echo "Processing $module..."
    cd $module
    
    # Tests
    pytest --cov --cov-report=html -v
    
    # Validation
    python validate_math.py
    
    # Deployment
    python deployment_verification.py
    
    # Performance
    pytest -m performance
    
    cd ..
done
```

### Generate All Reports

```bash
#!/bin/bash
# generate_all_reports.sh

cd separated_repos

for module in strepsuis-mdr strepsuis-amrvirkm strepsuis-genphennet strepsuis-phylotrait; do
    echo "Generating reports for $module..."
    cd $module
    
    # Coverage report
    pytest --cov --cov-report=html --cov-report=xml
    
    # Validation report
    python validate_math.py
    
    cd ..
done
```

## Troubleshooting

### Tests Fail Due to Missing Dependencies

```bash
pip install -e .[dev]
```

### Coverage Too Low

1. Check `htmlcov/index.html` for uncovered lines
2. Add tests for critical paths first
3. Focus on mathematical functions (100% required)

### Validation Fails

1. Check `validation_results/validation_results.json`
2. Compare against ground truth in `synthetic_data/metadata.json`
3. Verify scipy/statsmodels versions match

### Docker Build Fails

1. Ensure you're connected to internet
2. Check GitHub repository is accessible
3. Verify package name in Dockerfile matches repository

### Colab Notebook Fails

1. Verify notebook is valid JSON
2. Check GitHub repository URL is correct
3. Test locally first

## Support

For questions or issues:
- Create an issue on GitHub
- Check existing documentation in `docs/`
- Review `TESTING.md` for detailed testing guide

---

**Version**: 1.0.0
**Last Updated**: 2025-12-11
**Status**: Infrastructure Ready ✅
