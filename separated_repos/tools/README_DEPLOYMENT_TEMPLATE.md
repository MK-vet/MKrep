# Deployment and Validation Template

This template should be added to each module's README.md to document deployment options and quality assurance.

---

## Deployment Options

### Local Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/MK-vet/{MODULE_NAME}.git
```

Verify installation:

```bash
{CLI_COMMAND} --version
{CLI_COMMAND} --help
```

### Docker Deployment

Build and run with Docker:

```bash
# Build the image
docker build -t {MODULE_NAME}:latest .

# Run with mounted volumes
docker run --rm \
    -v $(pwd)/data:/data \
    -v $(pwd)/output:/output \
    {MODULE_NAME}:latest analyze /data/input.csv --output /output
```

The Dockerfile installs the package directly from GitHub, ensuring consistency with the repository.

### Google Colab

Try the module in Google Colab without any local installation:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](notebooks/{MODULE_NAME}_colab_demo.ipynb)

The Colab notebook:
1. Installs the package from GitHub
2. Verifies the installation
3. Demonstrates basic usage
4. Provides sample analysis workflow

## Quality Assurance & Validation

### Test Coverage

This module maintains high test coverage standards:

- **Overall Coverage**: >70% (target for Software X publication)
- **Mathematical Functions**: 100% coverage required
- **Test Categories**:
  - Unit tests (<1 second each)
  - Integration tests (1-5 seconds)
  - Statistical validation tests (against scipy/statsmodels)
  - Performance tests (with strict thresholds)
  - Edge case tests (empty data, single samples, extreme values)

Run tests locally:

```bash
# Clone repository
git clone https://github.com/MK-vet/{MODULE_NAME}.git
cd {MODULE_NAME}

# Install with development dependencies
pip install -e .[dev]

# Run all tests
pytest --cov --cov-report=html

# Run fast tests only (skip slow tests)
pytest -m "not slow" --cov

# View coverage report
open htmlcov/index.html
```

### Mathematical Validation

All statistical methods are validated against gold-standard implementations:

**Validation Strategy**:
1. **Synthetic Ground Truth**: Tested on Clean, Noisy, and Adversarial datasets
2. **Reference Comparison**: All methods validated against scipy/statsmodels
3. **Numerical Stability**: Tests for extreme values, edge cases, and numerical precision
4. **Reproducibility**: Fixed random seeds ensure deterministic results

**Validated Methods**:
- Chi-square tests (validated against `scipy.stats.chi2_contingency`)
- Fisher's exact test (validated against `scipy.stats.fisher_exact`)
- FDR correction (validated against `statsmodels.stats.multitest`)
- Bootstrap confidence intervals (coverage verification)
- [Add module-specific methods]

Run validation:

```bash
python validate_math.py
```

This generates:
- `validation_results/validation_results.json` - Detailed test results
- `validation_results/validation_summary.csv` - Summary metrics
- `validation_results/*.png` - Validation plots

### Synthetic Test Datasets

Three synthetic datasets are included for validation:

1. **Clean Dataset** (`synthetic_data/clean_dataset.csv`)
   - No noise, clear statistical patterns
   - n=200 samples, 20 features
   - Ideal for verifying algorithm correctness

2. **Noisy Dataset** (`synthetic_data/noisy_dataset.csv`)
   - 10% random bit flips
   - Tests robustness to measurement error
   - Verifies statistical methods handle noise appropriately

3. **Adversarial Dataset** (`synthetic_data/adversarial_dataset.csv`)
   - Extreme class imbalance (5% prevalence)
   - Perfect feature correlations
   - Tests edge case handling

Each dataset includes `metadata.json` with ground truth values for validation.

### Performance Benchmarking

Performance is continuously monitored with strict thresholds:

**Benchmarks**:
- Small datasets (1k records): < 1 second
- Medium datasets (10k records): < 5 seconds
- Large datasets (100k records): < 30 seconds
- Complexity: O(n) or better
- Memory usage: < 500MB for 50k records

Run performance tests:

```bash
pytest -m performance --cov
```

### Deployment Verification

Verify all deployment methods work correctly:

```bash
python deployment_verification.py
```

This script:
1. Checks CLI is available and working
2. Verifies Docker can build the image
3. Confirms Colab notebook exists and is valid JSON
4. Generates `deployment_verification.log` and `deployment_verification.txt`

### Continuous Integration

All quality checks run automatically:
- ✓ Tests on Python 3.8, 3.9, 3.10, 3.11, 3.12
- ✓ Code formatting (black, isort)
- ✓ Linting (ruff, mypy)
- ✓ Security scanning (bandit)
- ✓ Coverage reporting
- ✓ Performance regression detection

## Publication Standards

This module adheres to Software X publication standards:

- ✅ Comprehensive testing (>70% coverage)
- ✅ Mathematical validation against reference implementations
- ✅ Multiple deployment options (CLI, Docker, Colab)
- ✅ Performance benchmarking with defined thresholds
- ✅ Publication-ready documentation
- ✅ Reproducible results with fixed random seeds
- ✅ Open source (MIT License)
- ✅ Citation metadata (CITATION.cff)

## Documentation

- **USER_GUIDE.md**: Comprehensive usage documentation
- **ALGORITHMS.md**: Detailed algorithm descriptions
- **TESTING.md**: Testing methodology and guidelines
- **BENCHMARKS.md**: Performance benchmarks and optimization notes
- **CONTRIBUTING.md**: Contribution guidelines
- **CHANGELOG.md**: Version history and changes

## Support

- **Issues**: [GitHub Issues](https://github.com/MK-vet/MKrep/issues)
- **Discussions**: [GitHub Discussions](https://github.com/MK-vet/MKrep/discussions)
- **Documentation**: [Online Docs](https://mk-vet.github.io/MKrep/)

---

**Note**: Replace `{MODULE_NAME}` with the actual module name (e.g., `strepsuis-mdr`) and `{CLI_COMMAND}` with the CLI command name when adding to README.md.
