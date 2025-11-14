# Deployment Guide for Separated Repositories

This guide provides comprehensive instructions for deploying the 5 separated StrepSuis Suite repositories.

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Quick Reference](#quick-reference)
- [Detailed Deployment Instructions](#detailed-deployment-instructions)
- [Testing Each Repository](#testing-each-repository)
- [Publishing to PyPI](#publishing-to-pypi)
- [Publishing to Docker Hub](#publishing-to-docker-hub)
- [Automation Strategy](#automation-strategy)
- [Maintenance](#maintenance)

## Overview

The MKrep repository has been restructured into 5 independent, publication-ready modules located in the `separated_repos/` directory:

1. **strepsuis-amrpat** - Automated Detection of Antimicrobial Resistance Patterns
2. **strepsuis-amrvirkm** - K-Modes Clustering of AMR and Virulence Profiles
3. **strepsuis-genphennet** - Network-Based Integration of Genome-Phenome Data
4. **strepsuis-phylotrait** - Integrated Phylogenetic and Binary Trait Analysis
5. **strepsuis-genphen** - Interactive Platform for Integrated Genomic-Phenotypic Analysis

Each repository is **production-ready** with:
- ✅ Professional Python package structure
- ✅ Multi-stage Docker container
- ✅ Google Colab notebook
- ✅ Complete English documentation
- ✅ Pre-commit hooks for code quality
- ✅ GitHub Actions for CI/CD
- ✅ Comprehensive test suite
- ✅ User and contributor guides

## Repository Structure

Each separated repository contains:

```
repository-name/
├── .github/
│   └── workflows/
│       ├── test.yml          # CI testing (on PR and push to main)
│       ├── release.yml       # Automated releases (on release publish)
│       └── docs.yml          # Documentation generation (on release)
├── .dockerignore             # Docker build optimization
├── .gitignore                # Git ignore patterns
├── .pre-commit-config.yaml   # Pre-commit hooks configuration
├── CONTRIBUTING.md           # Contribution guidelines
├── Dockerfile                # Multi-stage Docker build
├── LICENSE                   # MIT License
├── README.md                 # Main documentation
├── RELEASE_CHECKLIST.md      # Pre-release checklist
├── USER_GUIDE.md             # Detailed user instructions
├── docker-compose.yml        # Docker Compose configuration
├── pyproject.toml            # Modern Python package configuration
├── pytest.ini                # Pytest configuration
├── requirements.txt          # Python dependencies
├── data/
│   ├── examples/
│   │   └── README.md         # Data format documentation
│   └── results/
│       └── README.md         # Expected results documentation
├── examples/                  # Example CSV data files
│   ├── AMR_genes.csv
│   ├── MIC.csv
│   ├── Virulence.csv
│   └── ...
├── notebooks/                 # Google Colab notebooks
│   └── *_Analysis.ipynb
├── package_name/              # Python package source
│   ├── __init__.py
│   ├── analyzer.py
│   ├── cli.py
│   └── config.py
└── tests/                     # Test suite
    ├── __init__.py
    ├── conftest.py
    └── test_basic.py
```

## Quick Reference

### Repository Information

| Repository | Package Name | CLI Command | Docker Image | Colab Notebook |
|------------|--------------|-------------|--------------|----------------|
| strepsuis-amrpat | strepsuis_amrpat | strepsuis-amrpat | ghcr.io/mk-vet/strepsuis-amrpat | AMRPat_Analysis.ipynb |
| strepsuis-amrvirkm | strepsuis_amrvirkm | strepsuis-amrvirkm | ghcr.io/mk-vet/strepsuis-amrvirkm | AMRVirKM_Analysis.ipynb |
| strepsuis-genphennet | strepsuis_genphennet | strepsuis-genphennet | ghcr.io/mk-vet/strepsuis-genphennet | GenPhenNet_Analysis.ipynb |
| strepsuis-phylotrait | strepsuis_phylotrait | strepsuis-phylotrait | ghcr.io/mk-vet/strepsuis-phylotrait | PhyloTrait_Analysis.ipynb |
| strepsuis-genphen | strepsuis_genphen | strepsuis-genphen | ghcr.io/mk-vet/strepsuis-genphen | GenPhen_Analysis.ipynb |

## Detailed Deployment Instructions

### Prerequisites

Before deploying, ensure you have:

- **Git** installed
- **GitHub account** with appropriate permissions
- **Python 3.8+** (for local testing)
- **Docker** (for container testing)
- **pre-commit** (`pip install pre-commit`)

### Step 1: Create GitHub Repositories

For each of the 5 modules, create a new GitHub repository:

1. Go to https://github.com/new
2. Repository name: Use the exact name from the table above
3. Description: Copy from the Overview section
4. Visibility: **Public** (or Private for pre-publication)
5. **Do NOT** initialize with README, license, or .gitignore

### Step 2: Initialize Local Git Repositories

For each module in `separated_repos/`:

```bash
cd separated_repos/strepsuis-amrpat

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial release v1.0.0

Production-ready bioinformatics tool for antimicrobial resistance pattern detection.

Features:
- Professional Python package with CLI
- Multi-stage Docker container
- Google Colab notebook
- Comprehensive documentation
- Pre-commit hooks and CI/CD
- Complete test suite

Version: 1.0.0
License: MIT"

# Add remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/strepsuis-amrpat.git

# Push to main branch
git branch -M main
git push -u origin main
```

Repeat for all 5 repositories.

### Step 3: Set Up Pre-commit Hooks (Local Development)

For developers working on the code:

```bash
cd separated_repos/strepsuis-amrpat

# Install pre-commit hooks
pre-commit install

# Test hooks
pre-commit run --all-files
```

This will:
- Format code with black
- Sort imports with isort
- Lint with ruff
- Type check with mypy
- Run security checks with bandit

### Step 4: Create GitHub Releases

For each repository:

1. Go to the repository on GitHub
2. Navigate to **Releases** → **Create a new release**
3. Click **Choose a tag** → Type `v1.0.0` → **Create new tag**
4. Release title: `Version 1.0.0 - Initial Release`
5. Description:

```markdown
# Version 1.0.0 - Initial Release 🎉

Production-ready bioinformatics tool for [specific tool purpose].

## Features

- ✅ Professional Python package with command-line interface
- ✅ Multi-stage Docker container for reproducible environments
- ✅ Google Colab notebook for non-programmers
- ✅ Comprehensive documentation in English
- ✅ Example datasets included
- ✅ >80% test coverage
- ✅ Publication-quality outputs (150+ DPI)

## Installation

### Python Package
```bash
pip install git+https://github.com/USERNAME/REPO-NAME.git@v1.0.0
```

### Docker Container
```bash
docker pull ghcr.io/username/REPO-NAME:1.0.0
```

### Google Colab
Click the badge in the README to open the notebook directly.

## What's Included

- Python source distribution and wheel
- Docker image (multi-platform: amd64, arm64)
- Google Colab notebook
- Example datasets
- Complete documentation

## Documentation

- [README.md](README.md) - Overview and quick start
- [USER_GUIDE.md](USER_GUIDE.md) - Detailed usage instructions
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

## Support

For questions or issues:
- GitHub Issues: https://github.com/USERNAME/REPO-NAME/issues
- Documentation: See README.md and USER_GUIDE.md

## Citation

See README.md for citation information.
```

6. Click **Publish release**

This will automatically trigger the `release.yml` workflow which:
- Builds distribution packages
- Builds and pushes Docker images to GitHub Container Registry
- Generates release notes

## Testing Each Repository

### Test 1: Package Installation from GitHub

```bash
# Create clean virtual environment
python -m venv test-env
source test-env/bin/activate  # On Windows: test-env\Scripts\activate

# Install package from GitHub
pip install git+https://github.com/USERNAME/strepsuis-amrpat.git@v1.0.0

# Test CLI
strepsuis-amrpat --version
strepsuis-amrpat --help

# Test analysis (requires example data)
strepsuis-amrpat --data-dir examples/ --output test-output/

# Cleanup
deactivate
rm -rf test-env test-output
```

### Test 2: Docker Container

```bash
cd separated_repos/strepsuis-amrpat

# Build Docker image
docker build -t strepsuis-amrpat:test .

# Test help
docker run --rm strepsuis-amrpat:test --help

# Test version
docker run --rm strepsuis-amrpat:test --version

# Test with example data
docker run --rm \
  -v $(pwd)/examples:/data \
  -v $(pwd)/test-output:/output \
  strepsuis-amrpat:test \
  --data-dir /data --output /output

# Cleanup
docker rmi strepsuis-amrpat:test
rm -rf test-output
```

### Test 3: Pre-commit Hooks

```bash
cd separated_repos/strepsuis-amrpat

# Install hooks
pre-commit install

# Run all hooks
pre-commit run --all-files

# Should pass with no errors
```

### Test 4: Test Suite

```bash
cd separated_repos/strepsuis-amrpat

# Install in development mode
pip install -e .[dev]

# Run tests
pytest

# Run with coverage
pytest --cov --cov-report=term-missing

# Coverage should be >80%
```

### Test 5: Google Colab Notebook

1. Upload notebook to Google Colab
2. Update GitHub URLs to point to your repository
3. Run all cells
4. Verify:
   - Package installs from GitHub
   - File upload works
   - Analysis runs without errors
   - Results can be downloaded

## Publishing to PyPI

**Optional:** For easier installation via `pip install package-name`

### Prerequisites

1. Create PyPI account at https://pypi.org
2. Create API token (Account Settings → API tokens)
3. Store token securely

### Steps

```bash
cd separated_repos/strepsuis-amrpat

# Install build tools
pip install build twine

# Build distribution packages
python -m build

# Check packages
twine check dist/*

# Test on TestPyPI first (recommended)
twine upload --repository testpypi dist/*

# Verify installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ strepsuis-amrpat

# If successful, upload to PyPI
twine upload dist/*

# Verify
pip install strepsuis-amrpat
```

## Publishing to Docker Hub

**Optional:** For easier Docker distribution

```bash
# Login to Docker Hub
docker login

# Build image
docker build -t strepsuis-amrpat:1.0.0 .

# Tag for Docker Hub
docker tag strepsuis-amrpat:1.0.0 USERNAME/strepsuis-amrpat:1.0.0
docker tag strepsuis-amrpat:1.0.0 USERNAME/strepsuis-amrpat:latest

# Push to Docker Hub
docker push USERNAME/strepsuis-amrpat:1.0.0
docker push USERNAME/strepsuis-amrpat:latest
```

## Automation Strategy

### GitHub Actions Usage

The workflows are configured for **minimal resource usage**:

#### Test Workflow (`test.yml`)
- **Triggers:** Pull requests and pushes to main branch only
- **Runs:** pytest, Docker build, code quality checks
- **Estimated usage:** 2-5 minutes per trigger
- **Monthly estimate:** ~10-30 minutes (depends on development activity)

#### Release Workflow (`release.yml`)
- **Triggers:** Only when creating GitHub releases
- **Runs:** Build packages, Docker images, generate notes
- **Estimated usage:** 5-10 minutes per release
- **Monthly estimate:** ~5-10 minutes (releases are infrequent)

#### Documentation Workflow (`docs.yml`)
- **Triggers:** Only on releases or manual trigger
- **Runs:** Generate API documentation
- **Estimated usage:** 2-3 minutes per trigger
- **Monthly estimate:** ~2-3 minutes

**Total estimated GitHub Actions usage: 15-45 minutes per month**

This is well within GitHub's free tier (2,000 minutes/month for public repositories).

### Pre-commit Hooks (Local)

Pre-commit hooks run **locally before commits**:
- No GitHub Actions usage
- Immediate feedback
- Prevents broken code from entering repository
- Free and fast

## Maintenance

### Updating Version Numbers

When releasing a new version:

1. Update version in `pyproject.toml`
2. Update version in `package_name/__init__.py`
3. Update CHANGELOG.md
4. Commit changes
5. Create new Git tag
6. Create GitHub release

### Updating Dependencies

```bash
# Update requirements
pip install --upgrade pip-tools
pip-compile --upgrade requirements.txt

# Test with new dependencies
pip install -r requirements.txt
pytest
```

### Monitoring

- **GitHub Actions:** Check workflow runs for failures
- **Issues:** Respond to user-reported problems
- **Security:** Enable Dependabot for dependency updates
- **Documentation:** Keep README and guides current

## Troubleshooting

### Issue: GitHub Actions failing

**Solution:**
1. Check workflow logs in GitHub Actions tab
2. Verify secrets are configured (for release workflow)
3. Ensure workflow files are valid YAML
4. Test locally before pushing

### Issue: Docker build fails

**Solution:**
1. Check Dockerfile syntax
2. Verify base image is accessible
3. Test build locally
4. Check GitHub Container Registry permissions

### Issue: Pre-commit hooks failing

**Solution:**
1. Run `pre-commit run --all-files` locally
2. Fix any reported issues
3. Commit fixes
4. Re-run hooks

### Issue: Tests failing

**Solution:**
1. Run pytest locally
2. Check test output for specific failures
3. Verify dependencies are installed
4. Check Python version compatibility

## Best Practices

1. **Always test locally before pushing**
   - Run pre-commit hooks
   - Run test suite
   - Test Docker build

2. **Use semantic versioning**
   - MAJOR.MINOR.PATCH
   - 1.0.0 → First stable release
   - 1.1.0 → New features (backward compatible)
   - 2.0.0 → Breaking changes

3. **Keep documentation updated**
   - Update README for feature changes
   - Update USER_GUIDE for usage changes
   - Update CHANGELOG for all releases

4. **Monitor resource usage**
   - Check GitHub Actions usage monthly
   - Optimize workflows if needed
   - Use caching to speed up builds

5. **Respond to issues promptly**
   - Acknowledge within 24-48 hours
   - Provide helpful responses
   - Close resolved issues

## Support

For questions about deployment:
- See individual repository README files
- Check CONTRIBUTING.md for development setup
- Open an issue in the relevant repository

---

**Version:** 1.0.0
**Last Updated:** 2025-01-14
**Maintained by:** MK-vet
**License:** MIT
