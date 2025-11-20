# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Optimized GitHub Actions workflows to reduce runner minutes
- Reduced Python version matrix from 5 to 3 versions (3.8, 3.11, 3.12)
- Docker builds now only run on releases and manual triggers

### Fixed
- Fixed example data files inclusion in repository
- Updated .gitignore to properly track example CSV files
- Corrected README formatting issues

## [1.0.0] - 2025-01-14

### Added
- Initial release of StrepSuis-GenPhen
- Tree-aware phylogenetic clustering with ensemble fallback for non-tree data
- Comprehensive trait profiling with multiple statistical methods (chi-square, log-odds, RF importance)
- Association rules mining with Apriori algorithm for pattern discovery
- Multiple Correspondence Analysis (MCA) for dimensionality reduction
- Interactive Bootstrap 5 UI with modern responsive design
- Full CSV export capabilities for all analysis results
- Bootstrap resampling for robust statistical inference (configurable iterations)
- Statistical significance testing with FDR correction for multiple testing
- Interactive HTML reports with sortable DataTables and Plotly visualizations
- Excel output with detailed statistical results and methodology sheets
- High-resolution PNG chart export (150+ DPI) for publications
- Complete test suite with pytest
- Docker container support with multi-stage build
- Google Colab notebook for non-programmers
- Comprehensive documentation (README, USER_GUIDE, CONTRIBUTING)
- CI/CD workflows (GitHub Actions)
- Pre-commit hooks for code quality (black, isort, ruff, mypy, bandit)
- Example datasets with documentation

### Features
- Phylogenetic tree integration for evolutionary-aware clustering
- Automatic fallback to standard clustering when tree unavailable
- Multi-method trait importance scoring (Random Forest, chi-square, log-odds ratio)
- Genotype-phenotype association analysis with statistical validation
- Pattern discovery across AMR genes, virulence factors, and phenotypes
- Interactive web-based UI with data filtering and export
- Support for MLST and serotype metadata integration

### Technical Details
- Python 3.8+ support
- Reproducible analyses with fixed random seeds
- Bootstrap resampling for statistical robustness
- FDR correction for multiple testing
- Interactive visualizations with Plotly and Bootstrap 5
- Command-line interface (CLI) and Python API
- Flexible data input (phylogenetic tree optional)

## Project History

This tool was developed as part of the StrepSuis Suite for bacterial genomics research, 
with a focus on *Streptococcus suis* but applicable to any bacterial species.

[Unreleased]: https://github.com/MK-vet/strepsuis-genphen/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/MK-vet/strepsuis-genphen/releases/tag/v1.0.0
