# Testing Infrastructure - StrepSuis Suite

## Overview

All modules in the StrepSuis Suite now include comprehensive test coverage with optimized execution strategies for both local development and CI/CD.

## Quick Links

### Documentation
- 📊 [Test Coverage Summary](separated_repos/TEST_COVERAGE_SUMMARY.md) - Comprehensive overview of testing enhancements
- ⚡ [Local Testing Guide](separated_repos/LOCAL_TESTING_GUIDE.md) - Quick reference for running tests
- 📝 Module-specific guides: Each module has a detailed `TESTING.md` file

### Scripts
- 🔧 [Coverage Report Generator](separated_repos/generate_coverage_reports.sh) - Generate coverage for all modules

## Test Coverage by Module

| Module | Tests | Coverage | Documentation |
|--------|-------|----------|---------------|
| strepsuis-amrpat | ✅ 82 tests | 57%+ | [TESTING.md](separated_repos/strepsuis-amrpat/TESTING.md) |
| strepsuis-amrvirkm | ✅ 82 tests | 57%+ | [TESTING.md](separated_repos/strepsuis-amrvirkm/TESTING.md) |
| strepsuis-genphen | ✅ 82 tests | 57%+ | [TESTING.md](separated_repos/strepsuis-genphen/TESTING.md) |
| strepsuis-genphennet | ✅ 82 tests | 57%+ | [TESTING.md](separated_repos/strepsuis-genphennet/TESTING.md) |
| strepsuis-phylotrait | ✅ 82 tests | 57%+ | [TESTING.md](separated_repos/strepsuis-phylotrait/TESTING.md) |

*Coverage shown is for fast tests only. Full suite coverage is higher.*

## Quick Start

### Run Tests for All Modules

```bash
cd separated_repos
./generate_coverage_reports.sh
```

### Run Tests for a Specific Module

```bash
cd separated_repos/strepsuis-amrpat
pip install -e .[dev]
pytest -v
```

### Fast Development Iteration

```bash
# Exclude slow tests for rapid feedback
pytest -m "not slow" -v
```

### Generate Coverage Report

```bash
pytest --cov --cov-report=html
open htmlcov/index.html
```

## Test Categories

Each module includes:

- **Unit Tests**: Fast tests of individual components
- **Integration Tests**: Tests using real example data
- **Workflow Tests**: End-to-end pipeline validation
- **CLI Tests**: Command-line interface validation
- **Data Validation Tests**: Input data format checking

## CI/CD Optimization

### GitHub Actions Strategy

Tests are optimized to minimize CI minutes:
- ✅ Run on pull requests, manual triggers, and releases only
- ✅ Exclude slow tests in CI (run locally)
- ✅ Parallel execution across Python 3.8, 3.11, 3.12
- ✅ Coverage reports uploaded to Codecov
- ✅ Docker builds only on releases

**Estimated CI time per module**: 4-6 minutes

### Local Testing First

Comprehensive pre-commit hooks catch issues before CI:
- Code formatting (black)
- Import sorting (isort)
- Linting (ruff)
- Type checking (mypy)
- Security checks (bandit)

## Coverage Goals

| Component | Target | Status |
|-----------|--------|--------|
| Config modules | 90-100% | ✅ Achieved |
| CLI interfaces | 85-100% | ✅ Achieved |
| Analyzers (init) | 80-100% | ✅ Achieved |
| Test code | 80-100% | ✅ Achieved |
| Core analysis | 60%+ | 🔄 In progress |
| Overall package | 60% min | ✅ Achieved |

## Scientific Validity

All tests use real example data:
- MIC.csv: Minimum inhibitory concentration data
- AMR_genes.csv: Antimicrobial resistance gene profiles
- Virulence.csv: Virulence factor data
- Snp_tree.newick: Phylogenetic trees

Tests validate:
- ✅ Data loading and validation
- ✅ Configuration and parameter handling
- ✅ Analysis pipeline initialization
- ✅ Output generation and formatting
- ✅ Error handling and edge cases
- ✅ Multi-file integration
- ✅ Reproducibility

## For Researchers

### Quick Validation After Installation

```bash
# Install a module
cd separated_repos/strepsuis-amrpat
pip install -e .[dev]

# Verify installation
pytest -v
```

### Running Your Own Data

While tests use example data, the same validation framework ensures your analysis will work correctly:

```bash
# Run analysis with your data
strepsuis-amrpat --data-dir /path/to/your/data --output /path/to/output

# Validate results
ls -lh /path/to/output
```

## For Developers

### Before Committing

```bash
# 1. Run pre-commit hooks
pre-commit run --all-files

# 2. Run fast tests
pytest -m "not slow" -v

# 3. Check coverage
pytest --cov --cov-report=term

# 4. Optional: Run full suite
pytest -v
```

### Adding New Features

When adding new features:
1. Write tests in `tests/test_workflow.py` or relevant test file
2. Run tests to ensure they pass
3. Check coverage is maintained or improved
4. Update documentation as needed

## Resources

### Documentation Files
- [TEST_COVERAGE_SUMMARY.md](separated_repos/TEST_COVERAGE_SUMMARY.md) - Detailed enhancement summary
- [LOCAL_TESTING_GUIDE.md](separated_repos/LOCAL_TESTING_GUIDE.md) - Quick reference guide
- Individual module TESTING.md files - Comprehensive testing guides

### External Resources
- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [Coverage.py documentation](https://coverage.readthedocs.io/)
- [Codecov](https://codecov.io/)

## Benefits

This comprehensive testing infrastructure provides:

✅ **Publication-ready quality**: High test coverage ensures reliability
✅ **Efficient development**: Fast test execution for rapid iteration
✅ **Cost-effective CI/CD**: Minimal GitHub Actions minutes consumption
✅ **Scientific validity**: Real-world workflow validation
✅ **Reproducibility**: Documented testing procedures
✅ **Researcher confidence**: Comprehensive validation of analysis pipelines

## Support

For testing-related questions:
1. Check module-specific TESTING.md
2. Review this guide and TEST_COVERAGE_SUMMARY.md
3. Check CI logs in GitHub Actions
4. Open an issue on GitHub

---

**Last Updated**: 2024
**Test Framework**: pytest 9.0.1+
**Coverage Tool**: pytest-cov 7.0.0+
**CI/CD**: GitHub Actions
