# StrepSuis Suite - Publication-Ready Bioinformatics Modules

This directory contains **five independent, publication-ready bioinformatics modules** for antimicrobial resistance and genomic analysis of *Streptococcus suis* and other bacterial species. Each module is designed for standalone publication in international peer-reviewed journals.

## Overview

The StrepSuis Suite consists of five specialized tools, each in its own subdirectory. Each module is production-ready with comprehensive documentation, testing, and deployment infrastructure suitable for publication in software journals such as SoftwareX.

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

## Documentation

Comprehensive documentation is organized in the `docs/` directory:

### Technical Documentation
- **[TESTING.md](docs/TESTING.md)** - Testing guide and coverage information
- **[TESTING_QUICK_START.md](docs/TESTING_QUICK_START.md)** - Quick reference for testing
- **[DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)** - Deployment strategies and instructions
- **[WORKFLOW_USAGE_GUIDE.md](docs/WORKFLOW_USAGE_GUIDE.md)** - GitHub Actions workflow documentation

### Scientific Documentation
- **[MATHEMATICAL_VALIDATION.md](docs/MATHEMATICAL_VALIDATION.md)** - Statistical method validation
- **[SYNTHETIC_DATA_VALIDATION.md](docs/SYNTHETIC_DATA_VALIDATION.md)** - Synthetic data testing methodology
- **[ANALYSIS_EXAMPLES.md](docs/ANALYSIS_EXAMPLES.md)** - Example analyses and use cases
- **[END_TO_END_TESTS.md](docs/END_TO_END_TESTS.md)** - End-to-end testing documentation
- **[COVERAGE_RESULTS.md](docs/COVERAGE_RESULTS.md)** - Test coverage reports

### Example Data
- **[docs/examples/synthetic_data/](docs/examples/synthetic_data/)** - Synthetic datasets for validation

## Module Structure

Each module follows a consistent, publication-ready structure:

### Core Components
- **Python Package** - Professional package structure with `pyproject.toml`
- **Docker Container** - Multi-stage build for reproducible deployment
- **Example Data** - Representative datasets for testing and demonstration
- **Test Suite** - Comprehensive pytest-based tests (70-85% coverage)

### Required Documentation (All Modules)
- **README.md** - Main documentation with installation and quick start
- **USER_GUIDE.md** - Detailed usage instructions and examples
- **CONTRIBUTING.md** - Contribution guidelines and code standards
- **CHANGELOG.md** - Version history and release notes
- **TESTING.md** - Testing documentation and coverage reports
- **CITATION.cff** - Citation metadata for research software
- **SECURITY.md** - Security policy and vulnerability reporting
- **LICENSE** - MIT License

### Module-Specific Documentation (CLI Modules)
- **ALGORITHMS.md** - Algorithm descriptions and complexity analysis
- **BENCHMARKS.md** - Performance benchmarks and scalability tests

### Quality Assurance Infrastructure
- **Pre-commit Hooks** - Automated code formatting (black, isort, ruff, mypy, bandit)
- **Type Hints** - Full type annotation with mypy validation
- **CI/CD Workflows** - GitHub Actions for testing and deployment
- **Security Scanning** - Automated vulnerability detection

### Configuration Files
- `.pre-commit-config.yaml` - Code quality automation
- `.dockerignore` - Docker build optimization
- `.gitignore` - Version control exclusions
- `pytest.ini` - Test configuration and markers
- `pyproject.toml` - Package metadata and dependencies
- `requirements.txt` - Production dependencies
- `docker-compose.yml` - Container orchestration

## Publication Readiness

All modules are designed for publication in peer-reviewed software journals such as:

- **SoftwareX** - Each module will be submitted as a separate publication
- **Journal of Open Source Software (JOSS)**
- **Bioinformatics**
- **BMC Bioinformatics**

### Publication Standards Met

✅ **Comprehensive Documentation** - README, user guides, algorithm descriptions  
✅ **Citation Metadata** - CITATION.cff files with DOI-ready format  
✅ **Testing Infrastructure** - 70-85% test coverage with multiple test types  
✅ **Reproducibility** - Docker containers, fixed random seeds, example data  
✅ **Code Quality** - Type hints, linting, formatting, security scanning  
✅ **Open Source** - MIT License, contribution guidelines  
✅ **Scientific Validation** - Mathematical correctness verified against reference implementations

## Installation and Usage

Each module can be installed independently:

### Installation from GitHub

```bash
# Install a specific module
pip install git+https://github.com/MK-vet/MKrep.git#subdirectory=separated_repos/strepsuis-mdr

# Or clone and install locally
git clone https://github.com/MK-vet/MKrep.git
cd MKrep/separated_repos/strepsuis-mdr
pip install -e .
```

### Docker Deployment

```bash
# Navigate to module directory
cd separated_repos/strepsuis-mdr

# Build and run with docker-compose
docker-compose up

# Or build manually
docker build -t strepsuis-mdr .
docker run -it strepsuis-mdr
```

### Usage Examples

**CLI-based modules** (mdr, amrvirkm, genphennet, phylotrait):
```bash
# Install module
pip install -e .

# Run analysis
strepsuis-mdr analyze --input data/example.csv --output results/
```

**Interactive module** (analyzer):
```bash
# Install module
pip install -e .

# Launch web interface
streamlit run app.py
```

For detailed usage instructions, refer to each module's USER_GUIDE.md.

## Development and Testing

### Running Tests

```bash
# Navigate to a module
cd strepsuis-mdr

# Install development dependencies
pip install -e .[dev]

# Run tests
pytest -v

# Run with coverage
pytest --cov --cov-report=html -v

# Run fast tests only (exclude slow tests)
pytest -m "not slow" -v
```

See [docs/TESTING.md](docs/TESTING.md) for comprehensive testing documentation.

### Code Quality

All modules use pre-commit hooks for automated code quality:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

Tools used:
- **black** - Code formatting (line length 100)
- **isort** - Import sorting (black profile)
- **ruff** - Fast linting
- **mypy** - Type checking
- **bandit** - Security analysis

## Directory Structure

```
separated_repos/
├── README.md                           # This file - suite overview
├── docs/                               # Centralized documentation
│   ├── TESTING.md                     # Testing guide
│   ├── TESTING_QUICK_START.md         # Quick testing reference
│   ├── DEPLOYMENT_GUIDE.md            # Deployment instructions
│   ├── WORKFLOW_USAGE_GUIDE.md        # GitHub Actions guide
│   ├── MATHEMATICAL_VALIDATION.md     # Statistical validation
│   ├── SYNTHETIC_DATA_VALIDATION.md   # Synthetic data methodology
│   ├── ANALYSIS_EXAMPLES.md           # Example analyses
│   ├── END_TO_END_TESTS.md           # E2E testing documentation
│   ├── COVERAGE_RESULTS.md           # Coverage reports
│   ├── examples/                      # Example datasets
│   │   └── synthetic_data/           # Synthetic test data
│   └── archive/                       # Historical implementation docs
├── strepsuis-mdr/                     # AMR Pattern Detection module
│   ├── strepsuis_mdr/                # Python package
│   ├── tests/                        # Test suite
│   ├── examples/                     # Example data
│   ├── README.md                     # Module documentation
│   ├── USER_GUIDE.md                 # Usage instructions
│   ├── ALGORITHMS.md                 # Algorithm descriptions
│   ├── BENCHMARKS.md                 # Performance benchmarks
│   ├── TESTING.md                    # Module testing guide
│   ├── CONTRIBUTING.md               # Contribution guidelines
│   ├── CHANGELOG.md                  # Version history
│   ├── CITATION.cff                  # Citation metadata
│   ├── SECURITY.md                   # Security policy
│   ├── pyproject.toml                # Package configuration
│   └── Dockerfile                    # Container definition
├── strepsuis-amrvirkm/                # K-Modes Clustering module
│   └── [same structure as strepsuis-mdr]
├── strepsuis-genphennet/              # Network Integration module
│   └── [same structure as strepsuis-mdr]
├── strepsuis-phylotrait/              # Phylogenetic Traits module
│   └── [same structure as strepsuis-mdr]
└── strepsuis-analyzer/                # Interactive Analysis module
    ├── src/strepsuis_analyzer/       # Python package (Streamlit app)
    ├── tests/                        # Test suite
    ├── data/                         # Example data
    ├── README.md                     # Module documentation
    ├── USER_GUIDE.md                 # Usage instructions
    ├── TESTING.md                    # Module testing guide
    ├── CONTRIBUTING.md               # Contribution guidelines
    ├── CHANGELOG.md                  # Version history
    ├── CITATION.cff                  # Citation metadata
    ├── SECURITY.md                   # Security policy
    ├── pyproject.toml                # Package configuration
    └── Dockerfile                    # Container definition
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

See [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) for comprehensive deployment instructions:
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

For comprehensive testing documentation, see [docs/TESTING.md](docs/TESTING.md).


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

- **Deployment Guide:** [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)
- **Testing Guide:** [docs/TESTING.md](docs/TESTING.md)
- **Analysis Examples:** [docs/ANALYSIS_EXAMPLES.md](docs/ANALYSIS_EXAMPLES.md)
- **Mathematical Validation:** [docs/MATHEMATICAL_VALIDATION.md](docs/MATHEMATICAL_VALIDATION.md)
- **Synthetic Data Validation:** [docs/SYNTHETIC_DATA_VALIDATION.md](docs/SYNTHETIC_DATA_VALIDATION.md)
- **Documentation Index:** [docs/archive/INDEX.md](docs/archive/INDEX.md)

## Publication-Readiness Checklist (per module)

| Module | CLI & Docs | Docker | Colab Notebook | Tests & Coverage | Reports & Results | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| strepsuis-mdr | [README](strepsuis-mdr/README.md) · [CLI](strepsuis-mdr/strepsuis_mdr/cli.py) | [Dockerfile](strepsuis-mdr/Dockerfile) | [Notebook](strepsuis-mdr/notebooks/MDR_Analysis.ipynb) | [TESTING.md](strepsuis-mdr/TESTING.md) · [test_reports/](strepsuis-mdr/test_reports/README.md) | [examples/](strepsuis-mdr/examples/) · [analysis_results/](strepsuis-mdr/analysis_results/) | CLI module (pip/CLI entrypoint) |
| strepsuis-amrvirkm | [README](strepsuis-amrvirkm/README.md) · [CLI](strepsuis-amrvirkm/strepsuis_amrvirkm/cli.py) | [Dockerfile](strepsuis-amrvirkm/Dockerfile) | [Notebook](strepsuis-amrvirkm/notebooks/AMRVirKM_Analysis.ipynb) | [TESTING.md](strepsuis-amrvirkm/TESTING.md) · [test_reports/](strepsuis-amrvirkm/test_reports/README.md) | [examples/](strepsuis-amrvirkm/examples/) · [analysis_results/](strepsuis-amrvirkm/analysis_results/) | CLI module (pip/CLI entrypoint) |
| strepsuis-genphennet | [README](strepsuis-genphennet/README.md) · [CLI](strepsuis-genphennet/strepsuis_genphennet/cli.py) | [Dockerfile](strepsuis-genphennet/Dockerfile) | [Notebook](strepsuis-genphennet/notebooks/GenPhenNet_Analysis.ipynb) | [TESTING.md](strepsuis-genphennet/TESTING.md) · [test_reports/](strepsuis-genphennet/test_reports/README.md) | [examples/](strepsuis-genphennet/examples/) · [analysis_results/](strepsuis-genphennet/analysis_results/) | CLI module (pip/CLI entrypoint) |
| strepsuis-phylotrait | [README](strepsuis-phylotrait/README.md) · [CLI](strepsuis-phylotrait/strepsuis_phylotrait/cli.py) | [Dockerfile](strepsuis-phylotrait/Dockerfile) | [Notebook](strepsuis-phylotrait/notebooks/PhyloTrait_Analysis.ipynb) | [TESTING.md](strepsuis-phylotrait/TESTING.md) · [test_reports/](strepsuis-phylotrait/test_reports/README.md) | [examples/](strepsuis-phylotrait/examples/) · [analysis_results/](strepsuis-phylotrait/analysis_results/) | CLI module (pip/CLI entrypoint) |
| strepsuis-analyzer | [README](strepsuis-analyzer/README.md) · [App](strepsuis-analyzer/app.py) | [Dockerfile](strepsuis-analyzer/Dockerfile) | N/A (Streamlit app) | [TESTING_COVERAGE.md](strepsuis-analyzer/TESTING_COVERAGE.md) · [tests/](strepsuis-analyzer/tests/) | [data/](strepsuis-analyzer/data/) · [results/](strepsuis-analyzer/results/) | Streamlit app (launch via `streamlit run app.py`) |

## Support

For questions or issues:
- Main repository issues: https://github.com/MK-vet/MKrep/issues
- Individual tool issues: Create issue in specific repository
- Documentation: See README and USER_GUIDE in each repository

---

**Version:** 1.0.0  
**License:** MIT  
**Python:** 3.8+
