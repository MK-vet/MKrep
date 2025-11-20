# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-11-20

### Added
- Initial release of StrepSuis-AMRVirKM
- K-Modes clustering with automatic silhouette score optimization (2-15 clusters tested)
- Multiple Correspondence Analysis (MCA) for dimensionality reduction and visualization
- Feature importance ranking using Random Forest classifiers and chi-square tests
- Association Rule Discovery with Apriori algorithm (configurable support/confidence)
- Bootstrap confidence intervals for robust statistical inference (configurable iterations)
- Integrated antimicrobial resistance and virulence factor analysis
- Statistical significance testing with FDR correction for multiple testing
- Interactive HTML reports with sortable tables and visualizations
- Excel output with detailed statistical results and methodology
- High-resolution PNG chart export (150+ DPI) for publications
- Complete test suite with pytest
- Docker container support with multi-stage build
- Google Colab notebook for non-programmers
- Comprehensive documentation (README, USER_GUIDE, CONTRIBUTING)
- CI/CD workflows (GitHub Actions)
- Pre-commit hooks for code quality (black, isort, ruff, mypy, bandit)
- Example datasets with documentation

### Changed
- Optimized GitHub Actions workflows to reduce runner minutes
- Reduced Python version matrix from 5 to 3 versions (3.8, 3.11, 3.12)
- Docker builds now only run on releases and manual triggers
- Updated mypy configuration to Python 3.9 for better type checking

### Fixed
- Fixed 13 code quality issues identified by ruff linting
- Fixed all bare except clauses with specific exception handling
- Fixed unused variables and ambiguous naming
- Fixed module-level import organization
- Fixed type annotation issues for mypy compliance
- Fixed example data files inclusion in repository
- Updated .gitignore to properly track example CSV files
- Corrected README formatting issues
- Fixed test fixtures to properly use example data

### Features
- Automatic optimal cluster detection via silhouette analysis
- Binary trait clustering for multiple genomic features
- Strain profiling across data types (MIC, AMR genes, virulence, MLST, serotype)
- Statistical validation with permutation tests
- Interactive cluster visualizations with MCA 2D/3D projections
- Full CSV export capabilities for all results

### Technical Details
- Python 3.8+ support
- Reproducible analyses with fixed random seeds
- Bootstrap resampling for statistical robustness
- FDR correction for multiple testing
- Interactive visualizations with Plotly
- Command-line interface (CLI) and Python API

## Project History

This tool was developed as part of the StrepSuis Suite for bacterial genomics research, 
with a focus on *Streptococcus suis* but applicable to any bacterial species.

[Unreleased]: https://github.com/MK-vet/strepsuis-amrvirkm/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/MK-vet/strepsuis-amrvirkm/releases/tag/v1.0.0
