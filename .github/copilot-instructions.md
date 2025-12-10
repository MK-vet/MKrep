# GitHub Copilot Instructions for StrepSuis Suite

## Repository Overview

This is the **StrepSuis Suite** - a collection of 5 bioinformatics Python modules for antimicrobial resistance (AMR) analysis in *Streptococcus suis*. Each module is publication-ready and will be published independently in SoftwareX journal.

### Repository Structure
```
MKrep/
├── .github/                      # GitHub workflows and Copilot instructions
├── separated_repos/              # 5 independent modules (production code)
│   ├── strepsuis-mdr/           # AMR Pattern Detection
│   ├── strepsuis-amrvirkm/      # K-Modes Clustering
│   ├── strepsuis-genphennet/    # Network Integration
│   ├── strepsuis-phylotrait/    # Phylogenetic Traits
│   └── strepsuis-analyzer/      # Interactive Streamlit Analysis
├── src/                          # Legacy analysis scripts
├── data/                         # Demo datasets
├── docs/                         # GitHub Pages documentation
├── colab_notebooks/              # Google Colab notebooks
├── tests/                        # Repository-level tests
└── requirements.txt              # Main dependencies
```

## Modules Overview
| Module | Purpose | CLI Command | Package Name |
|--------|---------|-------------|--------------|
| strepsuis-mdr | AMR Pattern Detection | `strepsuis-mdr` | strepsuis_mdr |
| strepsuis-amrvirkm | K-Modes Clustering | `strepsuis-amrvirkm` | strepsuis_amrvirkm |
| strepsuis-genphennet | Network Integration | `strepsuis-genphennet` | strepsuis_genphennet |
| strepsuis-phylotrait | Phylogenetic Traits | `strepsuis-phylotrait` | strepsuis_phylotrait |
| strepsuis-analyzer | Interactive Analysis | `streamlit run app.py` | strepsuis_analyzer |

## Build, Test, and Lint Commands

### Repository-Level Commands
```bash
# Install main dependencies
pip install -r requirements.txt

# Run legacy scripts (for backward compatibility)
python src/cluster_mic_amr_virulence.py
python src/mdr_analysis.py
python src/network_analysis.py
python src/phylogenetic_clustering.py
```

### Module-Level Commands
```bash
# Navigate to a module
cd separated_repos/strepsuis-mdr  # or any other module

# Install module in development mode
pip install -e .[dev]

# Run tests (fast tests only, skip slow ones)
pytest -m "not slow" -v

# Run all tests with coverage
pytest --cov --cov-report=html -v

# Run specific test categories
pytest -m unit -v           # Unit tests only
pytest -m integration -v    # Integration tests only
pytest -m slow -v           # Slow tests only

# Run linting and formatting (pre-commit)
pre-commit run --all-files

# Individual linting tools
black . --line-length=100
isort . --profile=black --line-length=100
ruff check . --fix
mypy . --ignore-missing-imports
bandit -r . -c pyproject.toml

# Build package
python -m build

# Install CLI locally for testing
pip install -e .
strepsuis-mdr --help  # Test CLI works
```

## Code Quality Standards

### 1. Python Code Requirements
- **Python Version**: 3.8+ compatible (test with 3.8, 3.9, 3.10, 3.11, 3.12)
- **Type Hints**: Required on all function signatures
- **Docstrings**: Required on all functions with Args, Returns, Raises sections
- **Formatting**: black (line length 100), isort (black profile)
- **Linting**: ruff, mypy --ignore-missing-imports
- **Security**: bandit for security checks

### 2. Testing Standards
- **Framework**: pytest with pytest-cov
- **Coverage**: >70% overall, 100% for critical paths (config, CLI, core algorithms)
- **Test Markers**: 
  - `@pytest.mark.unit` - Unit tests (<1 second)
  - `@pytest.mark.integration` - Integration tests (1-5 seconds)
  - `@pytest.mark.slow` - Slow tests (>5 seconds)
  - `@pytest.mark.stress` - Stress tests
  - `@pytest.mark.performance` - Performance tests
- **Fixtures**: Use tests/conftest.py for shared fixtures
- **Reproducibility**: Use `numpy.random.seed(42)` for all random operations

### 3. Statistical Validation
All statistical methods MUST be validated against gold-standard reference implementations:
- **Chi-square**: Validate against `scipy.stats.chi2_contingency` (5 decimal places)
- **Fisher exact**: Validate against `scipy.stats.fisher_exact` (5 decimal places)
- **FDR correction**: Validate against `statsmodels.stats.multitest.multipletests` (tolerance 1e-10)
- **Bootstrap CIs**: Verify coverage contains true parameter 95% of time
- **Test Location**: `tests/test_statistical_validation.py`
- **Standard Tolerance**: Use `decimal=5` for `np.testing.assert_almost_equal` or `1e-10` for relative error

### 4. Documentation Requirements
- **Language**: English only, publication-ready
- **License**: MIT
- **Required Files per Module**:
  - README.md - Quick start and overview
  - USER_GUIDE.md - Comprehensive usage guide
  - TESTING.md - Testing documentation
  - CONTRIBUTING.md - Contribution guidelines
  - CHANGELOG.md - Version history
  - CITATION.cff - Citation metadata
  - SECURITY.md - Security policy
  - ALGORITHMS.md - Algorithm descriptions
  - BENCHMARKS.md - Performance benchmarks

### 5. Deployment Architecture
- **CLI**: Click-based with subcommands (all modules except strepsuis-analyzer)
- **Streamlit**: Web app for strepsuis-analyzer only
- **Docker**: Install from GitHub: `pip install git+https://github.com/MK-vet/REPO.git`
- **Google Colab**: Install from GitHub: `!pip install git+https://github.com/MK-vet/REPO.git`
- **PyPI**: Not published yet (planned for future)

## Module Architecture Pattern

Each module follows a consistent architecture:

```
strepsuis-{module}/
├── strepsuis_{module}/          # Python package
│   ├── __init__.py             # Package exports
│   ├── config.py               # Configuration dataclasses with validation
│   ├── cli.py                  # Click-based CLI interface
│   ├── analyzer.py             # Main orchestration class
│   ├── *_core.py               # Core statistical algorithms
│   └── excel_report_utils.py   # Report generation utilities
├── tests/
│   ├── conftest.py             # Pytest fixtures
│   ├── test_config.py          # Configuration tests (100% coverage required)
│   ├── test_cli.py             # CLI tests (85%+ coverage required)
│   ├── test_analyzer.py        # Analyzer tests (85%+ coverage required)
│   ├── test_*_core.py          # Core algorithm tests (70%+ coverage required)
│   └── test_statistical_validation.py  # Validation against scipy/statsmodels
├── pyproject.toml              # Package metadata and dependencies
├── pytest.ini                  # Pytest configuration
├── .pre-commit-config.yaml     # Pre-commit hooks
├── README.md                   # Module documentation
├── Dockerfile                  # Docker deployment
└── CHANGELOG.md                # Version history
```

### Key Files and Their Purpose

| File | Coverage Target | Purpose |
|------|----------------|---------|
| config.py | 100% | Configuration validation, prevents invalid inputs |
| cli.py | 85%+ | User-facing CLI, ensures usability |
| analyzer.py | 85%+ | Main orchestration, coordinates workflow |
| *_core.py | 70%+ | Statistical algorithms, mathematical correctness |
| excel_report_utils.py | 60%+ | Report generation, formatting |

## Important Documentation Files

Always consult these files before making changes:

### Mathematical and Statistical Documentation
- `separated_repos/MATHEMATICAL_VALIDATION.md` - Statistical validation methodology
- `separated_repos/SYNTHETIC_DATA_VALIDATION.md` - Synthetic data testing approach
- `separated_repos/COVERAGE_RESULTS.md` - Current test coverage status

### Testing and Development
- `separated_repos/TESTING.md` - Comprehensive testing guide
- `separated_repos/TESTING_QUICK_START.md` - Quick testing reference
- `separated_repos/END_TO_END_TESTS.md` - End-to-end testing documentation

### Deployment and Configuration
- `separated_repos/DEPLOYMENT_GUIDE.md` - Deployment strategies
- `separated_repos/AGENT_SERVER_CONFIG.md` - Agent configuration
- `separated_repos/COMPREHENSIVE_FIX_PROMPT.md` - Common fixes and solutions

### Workflows and CI/CD
- `separated_repos/WORKFLOW_USAGE_GUIDE.md` - GitHub Actions workflows
- `.github/workflows/ci.yml` - Main CI pipeline
- `.github/workflows/deployment.yml` - Deployment tests

## Common Development Workflows

### Adding a New Feature
1. Read relevant documentation (MATHEMATICAL_VALIDATION.md if statistical)
2. Navigate to the appropriate module: `cd separated_repos/strepsuis-{module}`
3. Create feature branch: `git checkout -b feature/description`
4. Add code with type hints and docstrings
5. Add corresponding tests (unit + integration)
6. Run tests: `pytest -m "not slow" -v`
7. Run pre-commit: `pre-commit run --all-files`
8. Verify coverage: `pytest --cov --cov-report=html`
9. Update CHANGELOG.md
10. Submit PR

### Fixing a Bug
1. Navigate to module: `cd separated_repos/strepsuis-{module}`
2. Add failing test that reproduces bug
3. Fix the bug
4. Verify test passes: `pytest -v`
5. Run full test suite: `pytest --cov -v`
6. Update CHANGELOG.md

### Adding a Statistical Method
1. Consult MATHEMATICAL_VALIDATION.md
2. Implement method in `*_core.py` with type hints and docstrings
3. Add validation test in `test_statistical_validation.py` comparing to scipy/statsmodels
4. Add unit tests with known-answer data
5. Add integration test with realistic data
6. Document algorithm in ALGORITHMS.md
7. Verify coverage: `pytest --cov`

## Module-Specific Details

### strepsuis-mdr (AMR Pattern Detection)
- **Core Algorithms**: Bootstrap prevalence, co-occurrence, association rules
- **Key Files**: `mdr_core.py`, `bootstrap_utils.py`
- **Statistics**: Bootstrap CI, binomial tests, association mining
- **CLI Subcommands**: analyze, prevalence, co-occurrence, rules

### strepsuis-amrvirkm (K-Modes Clustering)
- **Core Algorithms**: K-modes clustering, MCA, silhouette optimization
- **Key Files**: `clustering_core.py`, `mca_utils.py`
- **Statistics**: Silhouette score, cluster validation, MCA
- **CLI Subcommands**: cluster, optimize, visualize

### strepsuis-genphennet (Network Integration)
- **Core Algorithms**: Chi-square/Fisher tests, FDR, information theory, network analysis
- **Key Files**: `network_core.py`, `association_utils.py`
- **Statistics**: Chi-square, Fisher exact, FDR (Benjamini-Hochberg), mutual information
- **CLI Subcommands**: analyze, network, associations

### strepsuis-phylotrait (Phylogenetic Traits)
- **Core Algorithms**: Faith's PD, tree-aware clustering, binary trait analysis
- **Key Files**: `phylo_core.py`, `tree_utils.py`
- **Statistics**: Faith's phylogenetic diversity, trait mapping
- **CLI Subcommands**: analyze, diversity, traits

### strepsuis-analyzer (Interactive Analysis)
- **Framework**: Streamlit web application
- **Run Command**: `streamlit run app.py` (NOT CLI-based)
- **Key Files**: `app.py`, `components/*.py`
- **Features**: File upload, interactive widgets, visualization panels

## Development Guidelines

### When Writing Code
1. **Always include docstrings** with Args, Returns, Raises sections (Google style)
2. **Always include type hints** on function signatures
3. **Always add corresponding test cases** (unit + integration)
4. **Use `numpy.random.seed(42)`** for reproducibility in all random operations
5. **Validate mathematical outputs** against reference implementations (scipy/statsmodels)
6. **Follow naming conventions**:
   - Functions: `snake_case`
   - Classes: `PascalCase`
   - Constants: `UPPER_SNAKE_CASE`
   - Private members: `_leading_underscore`
7. **Keep functions focused**: One function should do one thing well
8. **Avoid magic numbers**: Use named constants or configuration

### When Modifying Code
1. **Do NOT break downstream dependencies**: CLIs, Dockerfiles, Colab notebooks
2. **Consult MATHEMATICAL_VALIDATION.md** before modifying numerical logic
3. **Consider all code in `strepsuis-*/` as production-grade** - no experimental changes
4. **Run tests before and after changes** to detect regressions
5. **Update documentation** if APIs change
6. **Update CHANGELOG.md** with notable changes
7. **Maintain backward compatibility** when possible

### Common Pitfalls and How to Avoid Them

#### 1. Breaking CLI Changes
❌ **Don't**: Change CLI argument names or remove options
✅ **Do**: Add new options as optional, deprecate old ones gracefully
```python
# Bad
@click.option("--new-name")  # Breaking change!

# Good
@click.option("--new-name")
@click.option("--old-name", hidden=True)  # Keep for compatibility
```

#### 2. Statistical Correctness
❌ **Don't**: Implement statistical methods from scratch without validation
✅ **Do**: Validate against scipy/statsmodels with automated tests
```python
# Good - with explicit tolerance
def test_chi_square_matches_scipy():
    result_ours = our_chi_square(data)
    result_scipy = scipy.stats.chi2_contingency(data)
    # Validate to 5 decimal places as per project standard
    np.testing.assert_almost_equal(result_ours, result_scipy, decimal=5)
```

#### 3. Test Isolation
❌ **Don't**: Share mutable state between tests
✅ **Do**: Use pytest fixtures and reset state
```python
# Good
@pytest.fixture
def sample_data():
    return pd.DataFrame({"A": [1, 2], "B": [3, 4]})
```

#### 4. Missing Type Hints
❌ **Don't**: Leave functions without type hints
✅ **Do**: Always specify parameter and return types
```python
# Good
def calculate_prevalence(data: pd.DataFrame, threshold: float = 0.5) -> Dict[str, float]:
    """Calculate prevalence rates."""
    pass
```

#### 5. Incomplete Docstrings
❌ **Don't**: Write minimal docstrings
✅ **Do**: Include Args, Returns, Raises, Examples
```python
def analyze_data(data: pd.DataFrame, method: str = "chi-square") -> Dict[str, Any]:
    """
    Analyze data using specified statistical method.
    
    Args:
        data: Input dataframe with binary features
        method: Statistical method ("chi-square" or "fisher")
        
    Returns:
        Dictionary with test statistics and p-values
        
    Raises:
        ValueError: If method is not supported
        
    Examples:
        >>> result = analyze_data(df, method="chi-square")
        >>> print(result["p_value"])
    """
    pass
```

## File Naming Conventions

### Source Code
- **Tests**: `tests/test_*.py`
- **Fixtures**: `tests/conftest.py`
- **Core algorithms**: `*_core.py`
- **Utilities**: `*_utils.py`
- **Configuration**: `config.py`
- **CLI interface**: `cli.py`
- **Main orchestration**: `analyzer.py`

### Documentation
- **User guide**: `USER_GUIDE.md`
- **Testing guide**: `TESTING.md`
- **Contributing**: `CONTRIBUTING.md`
- **Changelog**: `CHANGELOG.md`
- **Algorithms**: `ALGORITHMS.md`
- **Benchmarks**: `BENCHMARKS.md`

### Configuration
- **Package metadata**: `pyproject.toml`
- **Pytest config**: `pytest.ini`
- **Pre-commit hooks**: `.pre-commit-config.yaml`
- **Docker**: `Dockerfile`
- **Docker Compose**: `docker-compose.yml`

## GitHub Actions Workflows

### Available Workflows
- **ci.yml**: Main CI pipeline (test on Python 3.8-3.12)
- **deployment.yml**: Deployment and installation tests
- **strepsuis-analyzer-tests.yml**: Streamlit app tests
- **strepsuis-analyzer-e2e.yml**: End-to-end tests for analyzer
- **version-info.yml**: Version information
- **pages.yml**: GitHub Pages deployment
- **generate_reports.yml**: Generate coverage and analysis reports
- **quickstart-demo.yml**: Quick start demo validation

### Workflow Triggers
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Manual dispatch (`workflow_dispatch`)

## Dependencies and Package Management

### Core Dependencies
- **pandas** ≥1.3.0 - Data manipulation
- **numpy** ≥1.21.0 - Numerical computing
- **scipy** ≥1.7.0 - Scientific computing
- **matplotlib** ≥3.4.0 - Visualization
- **seaborn** ≥0.11.0 - Statistical visualization
- **scikit-learn** ≥1.0.0 - Machine learning
- **biopython** ≥1.79 - Bioinformatics tools
- **networkx** ≥2.6.0 - Network analysis
- **click** ≥8.0.0 - CLI framework (except strepsuis-analyzer)
- **streamlit** - Web framework (strepsuis-analyzer only)

### Development Dependencies
- **pytest** ≥7.0.0 - Testing framework
- **pytest-cov** - Coverage reporting
- **black** - Code formatting
- **isort** - Import sorting
- **ruff** - Fast linting
- **mypy** - Type checking
- **bandit** - Security analysis
- **pre-commit** - Git hooks

## Security Considerations

1. **Never commit secrets** to the repository
2. **Use bandit** for security scanning: `bandit -r . -c pyproject.toml`
3. **Validate all user inputs** in CLI and web interfaces
4. **Sanitize file paths** to prevent directory traversal
5. **Use parameterized queries** if database access is added
6. **Keep dependencies updated** but test thoroughly
7. **Follow SECURITY.md** for reporting vulnerabilities

## Performance Guidelines

1. **Use vectorized operations** (numpy/pandas) instead of loops
2. **Profile before optimizing**: `python -m cProfile script.py`
3. **Cache expensive computations** when appropriate
4. **Use generators** for large datasets
5. **Parallel processing** for independent computations (use `joblib` or `multiprocessing`)
6. **Monitor memory usage** for large genomic datasets

## Troubleshooting Common Issues

### Tests Failing
```bash
# Clear pytest cache
pytest --cache-clear

# Run in verbose mode to see details
pytest -v -s

# Run specific test
pytest tests/test_config.py::test_specific_function -v
```

### Coverage Too Low
```bash
# Generate detailed coverage report
pytest --cov --cov-report=html
# Open htmlcov/index.html to see uncovered lines
```

### Pre-commit Failing
```bash
# Run individual hooks
pre-commit run black --all-files
pre-commit run mypy --all-files

# Update pre-commit hooks
pre-commit autoupdate
```

### Import Errors
```bash
# Reinstall in development mode
pip install -e .[dev]

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

## Global Standards and Best Practices

1. ✅ **Always consult MATHEMATICAL_VALIDATION.md** before modifying numerical logic
2. ✅ **Always run tests** before committing: `pytest -m "not slow" -v`
3. ✅ **Always run pre-commit** before committing: `pre-commit run --all-files`
4. ✅ **Never break downstream dependencies**: CLIs, Dockerfiles, Colab notebooks
5. ✅ **Consider all code in `strepsuis-*/` packages as production-grade**
6. ✅ **Focus on increasing test coverage** and mathematical correctness
7. ✅ **Write publication-ready code** - clear, documented, validated
8. ✅ **Maintain Python 3.8+ compatibility** - test across versions
9. ✅ **Use fixed random seeds** for reproducibility: `numpy.random.seed(42)`
10. ✅ **Follow the DRY principle** - Don't Repeat Yourself

## Quick Reference

### Essential Commands Cheat Sheet
```bash
# Setup
cd separated_repos/strepsuis-{module}
pip install -e .[dev]
pre-commit install

# Development
pytest -m "not slow" -v              # Fast tests
pytest --cov --cov-report=html -v    # Coverage
pre-commit run --all-files           # Lint & format
black . --line-length=100            # Format code
mypy . --ignore-missing-imports      # Type check

# CLI Testing
strepsuis-{module} --help            # Check CLI works
strepsuis-{module} --version         # Check version

# Build
python -m build                      # Build package
docker build -t strepsuis-{module} . # Build Docker image
```

---

**Version**: 3.0.0  
**Last Updated**: 2025-12-10  
**Maintained by**: MK-vet Team  
**For questions**: See CONTRIBUTING.md or open an issue
