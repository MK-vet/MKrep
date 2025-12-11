# Developer Guide - StrepSuis Suite

This guide is for developers working on the StrepSuis Suite. For user documentation, see [README.md](README.md).

## Quick Start for Developers

```bash
# Clone the repository
git clone https://github.com/MK-vet/MKrep.git
cd MKrep

# Navigate to a specific module
cd separated_repos/strepsuis-mdr

# Install in development mode with dev dependencies
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install

# Run tests
pytest -m "not slow" -v

# Run all quality checks
pre-commit run --all-files
```

## Repository Structure

See [ARCHITECTURE.md](ARCHITECTURE.md) for a comprehensive overview of the repository structure and component relationships.

### Key Directories

- **`separated_repos/`** - Primary development area for publication-ready modules
- **`scripts/`** - Development and maintenance scripts
- **`src/`** - Legacy standalone scripts (maintained for compatibility)
- **`python_package/`** - Legacy CLI wrapper (maintained for compatibility)

## Working with Modules

Each module in `separated_repos/` is an independent package with its own:

- **Package structure**: `strepsuis_{module}/` with Python code
- **Test suite**: `tests/` with pytest
- **Configuration**: `pyproject.toml`, `pytest.ini`, `.pre-commit-config.yaml`
- **Documentation**: README.md, USER_GUIDE.md, TESTING.md, etc.
- **Deployment**: Dockerfile, docker-compose.yml, Colab notebook

### Module Development Workflow

1. **Navigate to module directory**:
   ```bash
   cd separated_repos/strepsuis-mdr
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install in development mode**:
   ```bash
   pip install -e .[dev]
   ```

4. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

5. **Make your changes**:
   - Edit code in `strepsuis_{module}/`
   - Add/update tests in `tests/`
   - Update documentation as needed

6. **Run tests**:
   ```bash
   # Fast tests only
   pytest -m "not slow" -v
   
   # All tests with coverage
   pytest --cov --cov-report=html -v
   
   # Specific test file
   pytest tests/test_config.py -v
   ```

7. **Run code quality checks**:
   ```bash
   # Run all pre-commit hooks
   pre-commit run --all-files
   
   # Individual tools
   black . --line-length=100
   isort . --profile=black --line-length=100
   ruff check . --fix
   mypy . --ignore-missing-imports
   bandit -r . -c pyproject.toml
   ```

8. **Build and test package**:
   ```bash
   # Build package
   python -m build
   
   # Test CLI
   strepsuis-mdr --help
   ```

9. **Update changelog**:
   ```bash
   # Edit CHANGELOG.md
   vim CHANGELOG.md
   ```

10. **Commit and push**:
    ```bash
    git add .
    git commit -m "feat: add new feature"
    git push
    ```

## Development Scripts

### Repository-Level Scripts (`scripts/`)

These scripts are for repository maintenance and are not part of user-facing tools:

- **`create_modules.py`** - Generate new module structures (template-based)
- **`generate_package_files.py`** - Batch generate package configuration files
- **`verify_all_modules.py`** - Verify all modules are functional
- **`verify_modules.py`** - Module verification utility
- **`validate_mdr_output.py`** - Validate MDR analysis outputs
- **`validate_phylogenetic_structure.py`** - Validate phylogenetic analysis structure
- **`run_all_analyses.py`** - Run all legacy analysis modules
- **`run_*.py`** - Individual legacy analysis runners

### Module-Level Tools (`separated_repos/tools/`)

These tools maintain consistency across modules:

- **`add_coverage_badges.py`** - Add coverage badges to READMEs
- **`generate_coverage_badge.py`** - Generate coverage badge images
- **`generate_coverage_reports.sh`** - Generate coverage reports for all modules
- **`create_notebooks.sh`** - Create Colab notebooks from templates
- **`replicate_standardization.py`** - Replicate standardization across modules
- **`replicate_tests.py`** - Replicate test structure across modules
- **`run_tests.sh`** - Run tests for all modules
- **`upgrade_to_publication_standards.py`** - Upgrade modules to publication standards

## Testing Guidelines

### Test Structure

Each module follows this test structure:

```
tests/
├── conftest.py              # Shared fixtures
├── test_config.py          # Configuration tests (100% coverage required)
├── test_cli.py             # CLI tests (85%+ coverage required)
├── test_analyzer.py        # Main analyzer tests (85%+ coverage)
├── test_*_core.py          # Algorithm tests (70%+ coverage)
└── test_statistical_validation.py  # Validation against scipy/statsmodels
```

### Test Markers

Use pytest markers to categorize tests:

```python
@pytest.mark.unit          # Unit tests (<1 second)
@pytest.mark.integration   # Integration tests (1-5 seconds)
@pytest.mark.slow          # Slow tests (>5 seconds)
@pytest.mark.stress        # Stress tests
@pytest.mark.performance   # Performance tests
```

Run specific test categories:

```bash
pytest -m unit -v           # Unit tests only
pytest -m integration -v    # Integration tests only
pytest -m slow -v           # Slow tests only
pytest -m "not slow" -v     # Skip slow tests (fastest)
```

### Statistical Validation

All statistical methods must be validated against reference implementations (scipy, statsmodels):

```python
def test_chi_square_matches_scipy():
    """Validate chi-square against scipy implementation."""
    result_ours = our_chi_square(data)
    result_scipy = scipy.stats.chi2_contingency(data)
    np.testing.assert_almost_equal(result_ours, result_scipy, decimal=5)
```

Standard tolerance: `decimal=5` or relative error `1e-10`.

### Coverage Requirements

- **config.py**: 100% (prevents invalid configurations)
- **cli.py**: 85%+ (ensures CLI usability)
- **analyzer.py**: 85%+ (ensures workflow correctness)
- ***_core.py**: 70%+ (ensures algorithm correctness)
- **Overall**: 70%+ across all modules

## Code Quality Standards

### Python Style

- **Formatting**: Black with line length 100
- **Import sorting**: isort with black profile
- **Linting**: Ruff
- **Type checking**: mypy with --ignore-missing-imports
- **Security**: Bandit

### Documentation

All functions must have:
- **Type hints** on parameters and return values
- **Docstrings** with Args, Returns, Raises, Examples sections (Google style)

```python
def analyze_data(
    data: pd.DataFrame,
    method: str = "chi-square",
    alpha: float = 0.05
) -> Dict[str, Any]:
    """
    Analyze data using specified statistical method.
    
    Args:
        data: Input dataframe with binary features
        method: Statistical method ("chi-square" or "fisher")
        alpha: Significance level for tests
        
    Returns:
        Dictionary containing:
            - test_statistics: Test statistic values
            - p_values: P-values for each test
            - significant: Boolean array of significant results
            
    Raises:
        ValueError: If method is not supported
        
    Examples:
        >>> result = analyze_data(df, method="chi-square")
        >>> print(result["p_values"])
        [0.001, 0.05, 0.23, ...]
    """
    pass
```

### Reproducibility

- Use **fixed random seeds**: `numpy.random.seed(42)` for all random operations
- Document all **default parameters** with rationale
- Ensure **deterministic behavior** for the same inputs

## CI/CD Workflows

GitHub Actions workflows automatically:

- **Test on Python 3.8-3.12** for all modules
- **Build Docker containers** for each module
- **Run linting and formatting checks**
- **Generate coverage reports**
- **Build documentation** (GitHub Pages)
- **Test deployment** scenarios

### Local CI Testing

Before pushing, verify your changes pass CI checks:

```bash
# Run tests with coverage
pytest --cov --cov-report=html -v

# Run all quality checks
pre-commit run --all-files

# Build Docker image (if changed)
docker build -t strepsuis-mdr .

# Test CLI installation
pip install -e .
strepsuis-mdr --help
```

## Adding a New Module

1. **Use existing module as template**:
   ```bash
   cd separated_repos
   cp -r strepsuis-mdr strepsuis-newmodule
   ```

2. **Update module configuration**:
   - Edit `pyproject.toml` (name, version, description, dependencies)
   - Update `setup.py` if present
   - Modify `__init__.py` exports
   - Update `config.py` with module-specific settings

3. **Implement core functionality**:
   - Create `strepsuis_newmodule/*_core.py` with algorithms
   - Implement `analyzer.py` for workflow orchestration
   - Create `cli.py` for command-line interface

4. **Add comprehensive tests**:
   - Unit tests for each function
   - Integration tests for workflows
   - Statistical validation tests
   - Aim for >70% coverage

5. **Create documentation**:
   - README.md with overview and quick start
   - USER_GUIDE.md with detailed usage
   - TESTING.md with testing instructions
   - ALGORITHMS.md with algorithm descriptions
   - BENCHMARKS.md with performance data

6. **Add deployment support**:
   - Dockerfile for containerization
   - docker-compose.yml for orchestration
   - Google Colab notebook for cloud execution

7. **Configure quality tools**:
   - `.pre-commit-config.yaml` for hooks
   - `pytest.ini` for test configuration
   - Add to repository CI workflows

8. **Update repository documentation**:
   - Add module to `separated_repos/README.md`
   - Update main `README.md`
   - Update `ARCHITECTURE.md`

## Maintaining Consistency

Use tools in `separated_repos/tools/` to maintain consistency:

```bash
# Standardize all modules
cd separated_repos/tools
python replicate_standardization.py

# Update coverage badges
python add_coverage_badges.py

# Generate coverage reports
./generate_coverage_reports.sh

# Run all tests
./run_tests.sh
```

## Common Development Tasks

### Update Dependencies

```bash
# Update dependencies for a module
cd separated_repos/strepsuis-mdr
pip install -U -e .[dev]

# Update requirements.txt
pip freeze > requirements.txt

# Update pyproject.toml manually
```

### Run Security Checks

```bash
# Bandit security scan
bandit -r . -c pyproject.toml

# Check for vulnerable dependencies
pip-audit
```

### Generate Documentation

```bash
# Build documentation locally (if using Sphinx)
cd docs
make html

# Or use mkdocs
mkdocs serve
```

### Profile Performance

```bash
# Profile with cProfile
python -m cProfile -o profile.stats script.py

# Visualize with snakeviz
snakeviz profile.stats

# Line profiling
kernprof -l -v script.py
```

## Best Practices

1. **Make minimal changes**: Focus on one feature or fix at a time
2. **Write tests first**: TDD approach for new features
3. **Document as you go**: Update docs with code changes
4. **Use type hints**: Help catch errors early
5. **Follow conventions**: Use existing code as reference
6. **Run tests locally**: Don't rely only on CI
7. **Keep dependencies minimal**: Only add what's necessary
8. **Validate statistically**: Compare against reference implementations
9. **Use fixed seeds**: Ensure reproducibility
10. **Ask for help**: Open an issue or discussion if stuck

## Troubleshooting

### Tests Failing

```bash
# Clear pytest cache
pytest --cache-clear

# Run in verbose mode
pytest -v -s

# Run specific test
pytest tests/test_config.py::test_specific_function -v
```

### Import Errors

```bash
# Reinstall in development mode
pip install -e .[dev]

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

### Pre-commit Hooks Failing

```bash
# Run individual hooks
pre-commit run black --all-files
pre-commit run mypy --all-files

# Update hooks
pre-commit autoupdate
```

### Coverage Too Low

```bash
# Generate detailed coverage report
pytest --cov --cov-report=html

# Open htmlcov/index.html to see uncovered lines
```

## Resources

- **Main Documentation**: [README.md](README.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Module Testing**: See TESTING.md in each module
- **Statistical Validation**: `separated_repos/MATHEMATICAL_VALIDATION.md`
- **Deployment Guide**: `separated_repos/DEPLOYMENT_GUIDE.md`
- **Workflow Usage**: `separated_repos/WORKFLOW_USAGE_GUIDE.md`

## Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and ideas
- **Module CONTRIBUTING.md**: For module-specific guidelines
- **Code Review**: Create a PR for feedback

---

**Happy coding!** Remember: all code in `separated_repos/` is production-grade and publication-ready. Maintain high standards.
