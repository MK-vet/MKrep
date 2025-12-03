# StrepSuis Suite - Separated Repositories

This document provides an overview of the StrepSuis Suite bioinformatics tools, which consist of four independent, publication-ready modules for antimicrobial resistance and genomic analysis.

## Overview

The StrepSuis Suite contains **four production-ready bioinformatics tools**, each in its own subdirectory within `separated_repos/`. Each tool is designed for independent deployment as a GitHub repository.

## Module Overview

| Module | Purpose | Key Capabilities |
|--------|---------|------------------|
| [strepsuis-mdr](strepsuis-mdr/) | AMR Pattern Detection | Bootstrap prevalence estimation, co-occurrence analysis, association rules, network visualization |
| [strepsuis-amrvirkm](strepsuis-amrvirkm/) | K-Modes Clustering | Silhouette-optimized clustering, MCA, feature importance, bootstrap CIs |
| [strepsuis-genphennet](strepsuis-genphennet/) | Network Integration | Chi-square/Fisher tests, FDR correction, information theory, 3D visualization |
| [strepsuis-phylotrait](strepsuis-phylotrait/) | Phylogenetic Traits | Tree-aware clustering, Faith's PD, binary trait analysis, interactive reports |
| [strepsuis-analyzer](strepsuis-analyzer/) | Interactive Analysis | Streamlit web app, statistical tests, phylogenetics, clustering, report generation |

### strepsuis-mdr
**StrepSuis-AMRPat** provides automated detection of antimicrobial resistance patterns through:
- Bootstrap resampling for robust prevalence estimation
- Co-occurrence analysis for phenotypes and resistance genes
- Association rule mining for resistance patterns
- Hybrid co-resistance network construction and visualization

### strepsuis-amrvirkm
**StrepSuis-AMRVirKM** performs K-Modes clustering of antimicrobial resistance and virulence profiles:
- K-Modes clustering with automatic silhouette optimization
- Multiple Correspondence Analysis (MCA)
- Feature importance ranking
- Bootstrap confidence intervals

### strepsuis-genphennet
**StrepSuis-GenPhenNet** enables network-based integration of genome-phenome data:
- Chi-square and Fisher exact tests with FDR correction
- Information theory metrics (entropy, mutual information)
- Mutually exclusive pattern detection
- 3D network visualization with community detection

### strepsuis-phylotrait
**StrepSuis-PhyloTrait** provides integrated phylogenetic and binary trait analysis:
- Tree-aware clustering with evolutionary metrics
- Faith's Phylogenetic Diversity calculations
- Binary trait analysis for AMR and virulence factors
- Interactive HTML reports with DataTables and Plotly

### strepsuis-analyzer
**StrepSuis-Analyzer** provides an interactive Streamlit-based analysis platform:
- Interactive web interface for comprehensive data exploration
- Statistical analysis (correlations, hypothesis tests, meta-analysis)
- Advanced visualizations (interactive Plotly, publication-quality matplotlib)
- Phylogenetic analysis (Robinson-Foulds, bipartitions, Faith's PD)
- Machine learning (K-Means, K-Modes, Hierarchical, DBSCAN)
- ETL operations and report generation (Excel, HTML)

## Repository Contents

Each module is **production-ready** with the following components:

### Core Components
- **Python Package** - Professional package structure with `pyproject.toml`
- **Docker Container** - Multi-stage build with dynamic GitHub installation
- **Google Colab Notebook** - User-friendly notebook for non-programmers
- **Example Data** - Representative CSV datasets for testing

### Documentation
- **README.md** - Main documentation with installation and usage
- **USER_GUIDE.md** - Detailed step-by-step instructions
- **CONTRIBUTING.md** - Guidelines for contributors
- **CHANGELOG.md** - Version history and release notes
- **TESTING.md** - Comprehensive testing documentation
- **LICENSE** - MIT License

### Quality Assurance
- **Pre-commit Hooks** - Automated code formatting and linting
- **Test Suite** - pytest-based tests with comprehensive coverage
- **GitHub Actions** - CI/CD workflows (test.yml, release.yml, docs.yml)
- **Type Checking** - mypy configuration for type safety
- **Security Scanning** - bandit for security checks

### Configuration Files
- `.pre-commit-config.yaml` - Pre-commit hooks setup
- `.dockerignore` - Docker build optimization
- `.gitignore` - Git ignore patterns
- `pytest.ini` - Test configuration
- `pyproject.toml` - Package configuration with dev dependencies
- `requirements.txt` - Core dependencies
- `docker-compose.yml` - Docker Compose configuration

## Installation and Distribution

Each module supports three distribution methods:

### Python Package
```bash
pip install git+https://github.com/MK-vet/REPO-NAME.git
```

### Docker Container
```bash
docker pull ghcr.io/mk-vet/REPO-NAME:latest
```

### Google Colab
Click the Colab badge in each module's README to run without installation.

## Architecture

### Code Organization
- Docker containers install packages from GitHub dynamically
- Colab notebooks install packages from GitHub dynamically
- Single source of truth for each tool's code

### Automation Strategy

**Local Automation:**
- Pre-commit hooks execute before every commit
- Tools: black, isort, ruff, mypy, bandit
- Provides immediate feedback on code quality

**Cloud Automation:**
- GitHub Actions trigger on pull requests and releases
- Estimated usage: 15-45 minutes/month
- Workflows: test.yml, release.yml, docs.yml

## Directory Structure

```
strepsuis-mdr/
├── .github/workflows/       # CI/CD workflows
├── .pre-commit-config.yaml  # Code quality hooks
├── Dockerfile               # Multi-stage build
├── LICENSE                  # MIT License
├── README.md                # Main documentation
├── USER_GUIDE.md            # User instructions
├── TESTING.md               # Test documentation
├── pyproject.toml           # Package config
├── requirements.txt         # Dependencies
├── examples/                # CSV data files
├── notebooks/               # Colab notebooks
├── strepsuis_mdr/        # Python package
│   ├── __init__.py
│   ├── analyzer.py
│   ├── cli.py
│   └── config.py
└── tests/                   # Test suite
```

## Development

### Setup

1. **Install pre-commit hooks:**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

2. **Install in development mode:**
   ```bash
   pip install -e .[dev]
   ```

3. **Run tests:**
   ```bash
   pytest --cov
   ```

4. **Build Docker image:**
   ```bash
   docker build -t tool-name:dev .
   ```

### Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for comprehensive deployment instructions:
- Creating GitHub repositories
- Testing each component
- Publishing to PyPI (optional)
- Publishing to Docker Hub (optional)


## Testing Infrastructure

The suite implements comprehensive test coverage with 3-level validation across all modules.

### Test Coverage

| Module | Tests | Coverage | Critical Paths |
|--------|-------|----------|----------------|
| strepsuis-mdr | 110+ | 62% | 85-100% |
| strepsuis-amrvirkm | 100+ | 50% | 85-100% |
| strepsuis-genphennet | 100+ | 50% | 85-100% |
| strepsuis-phylotrait | 90+ | 50% | 85-100% |

### Testing Strategy

The testing framework includes:
- **Unit Tests** - Configuration validation, analyzer initialization
- **Integration Tests** - Multi-component workflows, data loading
- **End-to-End Tests** - Complete analysis pipelines with real data

End-to-end tests validate:
- Complete pipeline execution (Input → Processing → Output)
- Data preprocessing (CSV loading, merging, validation)
- Output generation (HTML, Excel, PNG charts)
- Reproducibility (consistent results with identical inputs)
- Error handling (missing files, invalid data, edge cases)

### Test Data

**Mini Datasets (CI):**
- 10 strains from real example data
- Execution time: <5 seconds per module
- Purpose: Fast feedback in CI pipelines

**Full Datasets (Local):**
- 92 strains (complete example data)
- Execution time: 30-60 seconds per module
- Purpose: Comprehensive validation before releases

### Running Tests

```bash
# Fast tests (for CI/development)
pytest -m "not slow" -v

# Full test suite (for local validation)
pytest -v

# End-to-end tests only
pytest tests/test_end_to_end.py -v

# With coverage report
pytest --cov --cov-report=html
```

### CI/CD Optimization

- Tests trigger on pull requests, manual dispatch, and releases
- Fast tests execute in CI; slow tests run locally
- Estimated CI time: 3-5 minutes per module
- Monthly usage: approximately 30-50 minutes total

For comprehensive testing documentation, see [TESTING.md](TESTING.md).


## Quality Standards

All modules meet the following standards:
- **Code Quality:** Black, isort, ruff, mypy, bandit
- **Testing:** Comprehensive test coverage with 3-level validation
- **Documentation:** Complete English documentation
- **Reproducibility:** Fixed seeds, documented parameters
- **Publication Ready:** High-resolution outputs (150+ DPI)
- **User Friendly:** Three distribution methods
- **Maintainable:** Clear structure, comprehensive tests

## Resources

- **Deployment Guide:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Testing Guide:** [TESTING.md](TESTING.md)
- **Analysis Examples:** [ANALYSIS_EXAMPLES.md](ANALYSIS_EXAMPLES.md)
- **Mathematical Validation:** [MATHEMATICAL_VALIDATION.md](MATHEMATICAL_VALIDATION.md)
- **Synthetic Data Validation:** [SYNTHETIC_DATA_VALIDATION.md](SYNTHETIC_DATA_VALIDATION.md)
- **Documentation Index:** [INDEX.md](INDEX.md)

## Support

For questions or issues:
- Main repository issues: https://github.com/MK-vet/MKrep/issues
- Individual tool issues: Create issue in specific repository
- Documentation: See README and USER_GUIDE in each repository

---

**Version:** 1.0.0  
**License:** MIT  
**Python:** 3.8+
