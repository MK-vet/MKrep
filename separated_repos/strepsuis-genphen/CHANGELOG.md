# Changelog

All notable changes to StrepSuis-GenPhen will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-11-20

### Added
- Initial release of StrepSuis-GenPhen
- Integrated genomic-phenotypic analysis framework
- Tree-aware clustering with ensemble fallback (KMeans/GMM/DBSCAN)
- Evolutionary metrics (phylogenetic diversity, beta diversity)
- Trait profiling with statistical significance testing
- Association rule mining with mlxtend
- Multiple Correspondence Analysis (MCA) with prince
- Interactive HTML reports with Bootstrap 5 and DataTables
- High-resolution chart export for publications
- Complete test suite with pytest
- Docker container support
- Google Colab notebook
- Comprehensive documentation
- CI/CD workflows (GitHub Actions)
- Pre-commit hooks for code quality
- Example datasets

### Changed
- Optimized GitHub Actions workflows to reduce runner minutes
- Docker builds now only run on releases and manual triggers
- Updated mypy configuration to Python 3.9

### Fixed
- Fixed 25 code quality issues identified by ruff linting
- Fixed undefined analyzer class names (Analyzer → GenPhenAnalyzer)
- Fixed all bare except clauses with specific exception handling
- Fixed type annotation issues for mypy compliance
- Added noqa directive for intentional E402 (Colab compatibility)
- Fixed example data inclusion in repository

### Features
- Automatic dependency installation for Colab compatibility
- Chi-square tests with FDR correction
- Log-odds ratio calculations
- Random Forest feature importance with bootstrap
- Phylogenetic signal detection
- Interactive visualizations with Plotly

### Technical Details
- Python 3.8+ support
- Reproducible analyses with fixed random seeds
- Optuna-based hyperparameter optimization
- Command-line interface (CLI) and Python API
- Docker containerization

## Project History

This tool was developed as part of the StrepSuis Suite for bacterial genomics research,
with a focus on *Streptococcus suis* but applicable to any bacterial species.

[Unreleased]: https://github.com/MK-vet/strepsuis-genphen/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/MK-vet/strepsuis-genphen/releases/tag/v1.0.0
