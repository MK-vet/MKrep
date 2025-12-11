# StrepSuis Suite Architecture

## Overview

This repository contains the **StrepSuis Suite** - a collection of professional bioinformatics tools for *Streptococcus suis* genomics analysis. The repository is structured to support multiple deployment strategies while maintaining publication-ready quality for each independent module.

## Repository Purpose

The primary goal of this repository is to host **5 independent, publication-ready bioinformatics modules**, each designed for separate publication in scientific journals (e.g., SoftwareX). Each module follows professional software engineering practices with comprehensive testing, documentation, and multiple deployment options.

## Directory Structure

```
MKrep/
├── separated_repos/          🎯 PRIMARY: Production-ready modules for publication
│   ├── strepsuis-mdr/       → AMR Pattern Detection (Publication 1)
│   ├── strepsuis-amrvirkm/  → K-Modes Clustering (Publication 2)
│   ├── strepsuis-genphennet/→ Network Integration (Publication 3)
│   ├── strepsuis-phylotrait/→ Phylogenetic Traits (Publication 4)
│   ├── strepsuis-analyzer/  → Interactive Analysis (Publication 5)
│   ├── docs/                → Development documentation
│   └── tools/               → Development automation scripts
│
├── src/                      📜 LEGACY: Original standalone scripts
│   ├── cluster_mic_amr_virulence.py
│   ├── mdr_analysis.py
│   ├── network_analysis.py
│   ├── phylogenetic_clustering.py
│   └── strep_suis_phylo_cluster.py
│
├── python_package/           🔧 LEGACY: CLI wrapper (backward compatibility)
│   └── mkrep/               → Wraps src/ scripts with CLI interface
│
├── scripts/                  🛠️ DEVELOPMENT: Helper and build scripts
│   ├── create_modules.py
│   ├── verify_all_modules.py
│   └── run_*.py
│
├── colab_notebooks/          ☁️ DEPLOYMENT: Google Colab notebooks
├── huggingface_demo/         🌐 DEPLOYMENT: Hugging Face Spaces
├── docs/                     📚 DOCUMENTATION: GitHub Pages site
├── data/                     📊 DATA: Example datasets
├── tests/                    ✅ TESTING: Repository-level tests
└── binder/                   🔬 DEPLOYMENT: MyBinder support
```

## Component Relationships

### Primary Components (separated_repos/)

Each module in `separated_repos/` is a **complete, standalone bioinformatics package**:

- **Independent publication target**: Each module will be published separately in scientific journals
- **Complete package structure**: Every module includes:
  - Python package with CLI (`pyproject.toml`, `setup.py`)
  - Docker container (`Dockerfile`, `docker-compose.yml`)
  - Google Colab notebook (`.ipynb`)
  - Comprehensive documentation (README, USER_GUIDE, TESTING, etc.)
  - Test suite with pytest
  - CI/CD workflows (GitHub Actions)
  - Pre-commit hooks for code quality

- **Modules**:
  1. **strepsuis-mdr** - Multidrug resistance pattern detection with bootstrap methods
  2. **strepsuis-amrvirkm** - K-Modes clustering for AMR/virulence profiling
  3. **strepsuis-genphennet** - Network-based genome-phenome integration
  4. **strepsuis-phylotrait** - Phylogenetic diversity and binary trait analysis
  5. **strepsuis-analyzer** - Interactive Streamlit web application

### Legacy Components

#### src/ Directory
Original standalone Python scripts that were refactored into the modular structure in `separated_repos/`. These are kept for:
- **Backward compatibility**: Existing users and workflows may depend on these
- **Reference implementation**: Original code that was validated and published
- **Simple usage**: Direct script execution without package installation

**Status**: Maintained but not actively developed. New features go into `separated_repos/`.

#### python_package/ Directory
A CLI wrapper around the `src/` scripts, providing a unified command-line interface:
- Commands: `mkrep-cluster`, `mkrep-mdr`, `mkrep-network`, `mkrep-phylo`, `mkrep-strepsuis`
- Purpose: Convenience wrapper for the legacy scripts

**Status**: Maintained for backward compatibility. Users are encouraged to use individual modules from `separated_repos/` for publication-quality work.

### Development Tools

#### scripts/ Directory
Helper scripts used during development and repository maintenance:
- Module generation and verification scripts
- Legacy analysis runners
- Template files
- Validation scripts

**Status**: Development utilities, not part of user-facing tools.

#### separated_repos/tools/
Automation tools specific to the modular packages:
- Coverage report generation
- Test replication across modules
- Standardization scripts
- Badge generation

**Status**: Development utilities for maintaining consistency across modules.

#### separated_repos/docs/
Development and implementation documentation:
- Implementation notes
- Upgrade summaries
- Coverage results
- Agent configuration

**Status**: Historical and development documentation, not user-facing.

### Deployment Options

#### colab_notebooks/
Google Colab notebooks providing cloud-based execution:
- Interactive notebook interface (no installation required)
- Advanced analysis notebooks with full code
- Support for both free and Pro Colab tiers

**Purpose**: Accessibility for users without local Python environments.

#### huggingface_demo/
Voilà dashboard for deployment on Hugging Face Spaces:
- Interactive web interface
- No coding required
- Cloud deployment option

**Purpose**: Public demonstration and easy access for non-technical users.

#### binder/
Configuration for MyBinder deployment:
- Alternative cloud execution platform
- Compatible with Jupyter notebooks

**Purpose**: Additional cloud deployment option.

## Usage Recommendations

### For Researchers and Publications

**Recommended**: Use modules from `separated_repos/`
- Each module is publication-ready with peer-review quality
- Complete documentation and validation
- Professional package structure
- Active development and support

```bash
# Install a specific module
pip install git+https://github.com/MK-vet/MKrep.git#subdirectory=separated_repos/strepsuis-mdr

# Or use Docker
docker build -t strepsuis-mdr separated_repos/strepsuis-mdr/
```

### For Legacy Workflows

**Backward Compatibility**: Use `src/` scripts or `python_package/`
- Maintains compatibility with existing workflows
- Simpler for quick analyses
- Less overhead than full package installation

```bash
# Legacy scripts
python src/mdr_analysis.py

# Or via package
pip install -e python_package/
mkrep-mdr --help
```

### For Non-Technical Users

**Recommended**: Use cloud deployment options
- Google Colab notebooks (no installation)
- Hugging Face Spaces (web interface)
- MyBinder (Jupyter notebooks)

## Migration Path

Users currently using `src/` scripts or `python_package/` are encouraged to migrate to `separated_repos/` modules:

1. **Identify your current workflow**: Which script or command are you using?
2. **Find the equivalent module**:
   - `src/mdr_analysis.py` → `separated_repos/strepsuis-mdr/`
   - `src/cluster_mic_amr_virulence.py` → `separated_repos/strepsuis-amrvirkm/`
   - `src/network_analysis.py` → `separated_repos/strepsuis-genphennet/`
   - `src/phylogenetic_clustering.py` → `separated_repos/strepsuis-phylotrait/`
   - `src/strep_suis_phylo_cluster.py` → `separated_repos/strepsuis-phylotrait/`
3. **Install the module**: Follow the README in each module directory
4. **Update your workflow**: Use the new CLI commands or Python API

## Development Workflow

### Adding a New Feature

1. **Identify the target module** in `separated_repos/`
2. **Navigate to the module directory**
3. **Follow the module's CONTRIBUTING.md** guidelines
4. **Run tests**: `pytest -v`
5. **Run pre-commit hooks**: `pre-commit run --all-files`
6. **Update documentation** as needed

### Creating a New Module

1. **Use the template** from existing modules
2. **Follow the standardized structure**:
   - `pyproject.toml` for package configuration
   - `tests/` for comprehensive test coverage
   - Complete documentation suite
   - Docker support
   - Google Colab notebook
3. **Ensure publication quality**:
   - Type hints on all functions
   - Comprehensive docstrings
   - Statistical validation tests
   - Coverage > 70%

## Quality Standards

All modules in `separated_repos/` must meet these standards:

- **Documentation**: README, USER_GUIDE, TESTING, CONTRIBUTING, CHANGELOG
- **Testing**: pytest with >70% coverage, statistical validation
- **Code Quality**: Black formatting, type hints, docstrings
- **Security**: Bandit scanning, dependency checks
- **Reproducibility**: Fixed random seeds, documented parameters
- **Multi-platform**: Python 3.8-3.12 compatibility

## Version Control Strategy

- **Main branch**: Stable, production-ready code
- **Develop branch**: Integration branch for new features
- **Feature branches**: Individual feature development
- **Module branches**: Can develop modules independently

## Continuous Integration

GitHub Actions workflows test:
- All modules in `separated_repos/` (Python 3.8-3.12)
- Legacy scripts in `src/`
- Package installation and CLI
- Docker builds
- Documentation generation

## Future Plans

1. **Separate GitHub repositories**: Each module in `separated_repos/` may be split into its own repository for independent development and publication
2. **PyPI publication**: Publish each module to PyPI for easier installation
3. **Conda packages**: Add conda-forge packages
4. **Enhanced CI/CD**: Per-module release automation
5. **Deprecation of legacy code**: Gradual phase-out of `src/` and `python_package/` as modules mature

## Contact and Support

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Contributions**: See CONTRIBUTING.md in each module
- **Publications**: Each module has a CITATION.cff file

---

**Note**: This architecture supports both backward compatibility and future growth while maintaining publication-ready quality for scientific research.
