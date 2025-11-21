# Separated Repositories Summary

> **Note:** This repository is being renamed from `MKrep` to `StrepSuis_Suite`. 
> All documentation reflects the new name. GitHub URLs will be updated after repository rename.

This document provides a high-level overview of the separated repository structure created for the StrepSuis Suite bioinformatics tools.

## Overview

The MKrep repository has been structured to support **5 independent, publication-ready bioinformatics tools**, each in its own subdirectory within `separated_repos/`. Each tool is designed to be deployed as a separate GitHub repository.

## Repository List

### 1. strepsuis-amrpat
**Location:** `separated_repos/strepsuis-amrpat/`
**Full Name:** StrepSuis-AMRPat
**Purpose:** Automated Detection of Antimicrobial Resistance Patterns
**Key Features:**
- Bootstrap resampling for robust prevalence estimation
- Co-occurrence analysis for phenotypes and resistance genes
- Association rule mining for resistance patterns
- Hybrid co-resistance network construction and visualization

### 2. strepsuis-amrvirkm
**Location:** `separated_repos/strepsuis-amrvirkm/`
**Full Name:** StrepSuis-AMRVirKM
**Purpose:** K-Modes Clustering of Antimicrobial Resistance and Virulence Profiles
**Key Features:**
- K-Modes clustering with automatic silhouette optimization
- Multiple Correspondence Analysis (MCA)
- Feature importance ranking
- Bootstrap confidence intervals

### 3. strepsuis-genphennet
**Location:** `separated_repos/strepsuis-genphennet/`
**Full Name:** StrepSuis-GenPhenNet
**Purpose:** Network-Based Integration of Genome-Phenome Data
**Key Features:**
- Chi-square and Fisher exact tests with FDR correction
- Information theory metrics (entropy, mutual information)
- Mutually exclusive pattern detection
- 3D network visualization with community detection

### 4. strepsuis-phylotrait
**Location:** `separated_repos/strepsuis-phylotrait/`
**Full Name:** StrepSuis-PhyloTrait
**Purpose:** Integrated Phylogenetic and Binary Trait Analysis
**Key Features:**
- Tree-aware clustering with evolutionary metrics
- Faith's Phylogenetic Diversity calculations
- Binary trait analysis for AMR and virulence factors
- Interactive HTML reports with DataTables and Plotly

### 5. strepsuis-genphen
**Location:** `separated_repos/strepsuis-genphen/`
**Full Name:** StrepSuis-GenPhen
**Purpose:** Interactive Platform for Integrated Genomic-Phenotypic Analysis
**Key Features:**
- Tree-aware phylogenetic clustering with ensemble fallback
- Comprehensive trait profiling (chi-square, log-odds, RF importance)
- Association rules mining and Multiple Correspondence Analysis
- Interactive Bootstrap 5 UI with full CSV export capabilities

## What's Included in Each Repository

Each separated repository is **production-ready** with:

### Core Components
- ✅ **Python Package** - Professional package structure with `pyproject.toml`
- ✅ **Docker Container** - Multi-stage build with dynamic GitHub installation
- ✅ **Google Colab Notebook** - User-friendly notebook for non-programmers
- ✅ **Example Data** - Representative CSV datasets for testing

### Documentation
- ✅ **README.md** - Main documentation with installation and usage
- ✅ **USER_GUIDE.md** - Detailed step-by-step instructions
- ✅ **CONTRIBUTING.md** - Guidelines for contributors
- ✅ **CHANGELOG.md** - Version history and release notes
- ✅ **RELEASE_CHECKLIST.md** - Pre-release verification checklist
- ✅ **LICENSE** - MIT License
- ✅ **Data Documentation** - Format specifications in examples/ directories

### Quality Assurance
- ✅ **Pre-commit Hooks** - Automated code formatting and linting (.pre-commit-config.yaml)
- ✅ **Test Suite** - pytest-based tests with >80% coverage target
- ✅ **GitHub Actions** - CI/CD workflows (test.yml, release.yml, docs.yml)
- ✅ **Type Checking** - mypy configuration for type safety
- ✅ **Security Scanning** - bandit for security checks

### Configuration Files
- ✅ `.pre-commit-config.yaml` - Pre-commit hooks setup
- ✅ `.dockerignore` - Docker build optimization
- ✅ `.gitignore` - Git ignore patterns
- ✅ `pytest.ini` - Test configuration
- ✅ `pyproject.toml` - Package configuration with dev dependencies
- ✅ `requirements.txt` - Core dependencies
- ✅ `docker-compose.yml` - Docker Compose configuration

### Optional Components (may vary by tool)

The following files may be present in some repositories depending on tool-specific requirements:
- `.env.example` - Environment variables template (currently not needed - tools use CLI arguments)
- Additional tool-specific documentation (see individual repository README)

## Key Features

### 1. No Code Duplication
- Docker containers install packages from GitHub dynamically
- Colab notebooks install packages from GitHub dynamically
- Single source of truth for each tool's code

### 2. Smart Automation
**Local (Free):**
- Pre-commit hooks run before commits
- Immediate feedback on code quality
- Prevents broken code from entering repository

**Cloud (Minimal):**
- GitHub Actions only on PR and releases
- Estimated usage: 15-45 minutes/month
- Well within free tier limits

### 3. Three Distribution Methods

**Method 1: Python Package**
```bash
pip install git+https://github.com/MK-vet/REPO-NAME.git
```

**Method 2: Docker Container**
```bash
docker pull ghcr.io/mk-vet/REPO-NAME:latest
```

**Method 3: Google Colab**
- Click badge in README
- No installation required

### 4. Production Ready
- Version 1.0.0 throughout
- MIT License
- Complete English documentation
- Publication-quality outputs
- Reproducible analyses

## Directory Structure Example

```
strepsuis-amrpat/
├── .github/workflows/       # CI/CD workflows
├── .dockerignore           # Docker optimization
├── .gitignore              # Git ignore rules
├── .pre-commit-config.yaml # Code quality hooks
├── CONTRIBUTING.md         # Contribution guide
├── Dockerfile              # Multi-stage build
├── LICENSE                 # MIT License
├── README.md               # Main documentation
├── RELEASE_CHECKLIST.md    # Release verification
├── USER_GUIDE.md           # User instructions
├── docker-compose.yml      # Docker Compose
├── pyproject.toml          # Package config
├── pytest.ini              # Test config
├── requirements.txt        # Dependencies
├── data/
│   ├── examples/           # Example data + docs
│   └── results/            # Expected results + docs
├── examples/               # CSV data files
├── notebooks/              # Colab notebooks
├── strepsuis_amrpat/       # Python package
│   ├── __init__.py
│   ├── analyzer.py
│   ├── cli.py
│   └── config.py
└── tests/                  # Test suite
```

## Next Steps

### For Deployment

See `separated_repos/DEPLOYMENT_GUIDE.md` for comprehensive deployment instructions including:
- Creating GitHub repositories
- Testing each component
- Publishing to PyPI (optional)
- Publishing to Docker Hub (optional)
- Automation strategy
- Maintenance procedures

### For Development

Each repository includes:
1. **Setup pre-commit hooks:**
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

## Version Information

- **Version:** 1.0.0
- **Status:** Production Ready
- **License:** MIT
- **Language:** Python 3.8+
- **Documentation:** English

## Automation Summary

### Local Automation (Free)
- **Pre-commit hooks** run before every commit
- **Tools:** black, isort, ruff, mypy, bandit
- **Cost:** $0
- **Speed:** Immediate

### Cloud Automation (Minimal)
- **GitHub Actions** run on PR and releases only
- **Workflows:** test.yml, release.yml, docs.yml
- **Estimated usage:** 15-45 minutes/month
- **Cost:** Free (within GitHub's 2,000 min/month limit)

### Manual Steps (One-time)
- Publishing to PyPI (optional)
- Publishing to Docker Hub (optional)
- Creating GitHub releases


## Testing Infrastructure

All repositories now include **comprehensive test coverage** designed for both scientific validity and minimal CI consumption.

### Test Coverage Summary

| Module | Tests | Coverage | Fast Tests | Full Suite |
|--------|-------|----------|------------|------------|
| strepsuis-amrpat | 82 | 57-80% | ~4s | ~10-30s |
| strepsuis-amrvirkm | 82 | 57-80% | ~4s | ~10-30s |
| strepsuis-genphen | 82 | 57-80% | ~4s | ~10-30s |
| strepsuis-genphennet | 82 | 57-80% | ~4s | ~10-30s |
| strepsuis-phylotrait | 82 | 57-80% | ~4s | ~10-30s |

### Test Categories

Each repository includes:
- **Unit Tests**: Fast tests of individual components
- **Integration Tests**: Tests using real example data
- **Workflow Tests**: End-to-end pipeline validation
- **CLI Tests**: Command-line interface validation
- **Data Validation Tests**: Input data format checking

### Quick Testing Commands

```bash
# Fast tests (for development)
pytest -m "not slow" -v

# Full test suite
pytest -v

# With coverage report
pytest --cov --cov-report=html
open htmlcov/index.html
```

### CI/CD Optimization

- Tests run on: Pull requests, manual triggers, releases only
- Fast tests only in CI (slow tests run locally)
- Estimated CI time: 4-6 minutes per module
- Well within GitHub's free tier

### Documentation

- [📊 Test Coverage Summary](TEST_COVERAGE_SUMMARY.md) - Comprehensive testing overview
- [⚡ Local Testing Guide](LOCAL_TESTING_GUIDE.md) - Quick reference
- [📝 Testing README](README_TESTING.md) - Complete testing documentation
- Module-specific: Each repository has a `TESTING.md` file

### Generate All Coverage Reports

```bash
cd separated_repos
./generate_coverage_reports.sh
```


## Quality Standards

All repositories meet:
- ✅ **Code Quality:** Black, isort, ruff, mypy, bandit
- ✅ **Testing:** >80% coverage target
- ✅ **Documentation:** Complete English docs
- ✅ **Reproducibility:** Fixed seeds, documented parameters
- ✅ **Publication Ready:** High-resolution outputs (150+ DPI)
- ✅ **User Friendly:** Three distribution methods
- ✅ **Maintainable:** Clear structure, comprehensive tests

## Resources

- **Main Repository:** https://github.com/MK-vet/MKrep
- **Deployment Guide:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Original Documentation:** ../README.md
- **Module Separation Guide:** ../REPOSITORY_SEPARATION_GUIDE.md

## Support

For questions or issues:
- Main repository issues: https://github.com/MK-vet/MKrep/issues
- Individual tool issues: Create issue in specific repository
- Documentation: See README and USER_GUIDE in each repository

---

**Created:** 2025-01-14
**Version:** 1.0.0
**Status:** Production Ready
**License:** MIT
