# Changelog

All notable changes to StrepSuis-AMRPat will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-01-14

### Added
- Initial release of StrepSuis-AMRPat
- Bootstrap resampling for robust prevalence estimation (configurable iterations)
- Co-occurrence analysis for phenotypes and resistance genes
- Association rule mining for antimicrobial resistance patterns
- Hybrid co-resistance network construction and visualization
- Louvain community detection for resistance gene clustering
- Publication-quality network visualizations with high-resolution PNG output
- Complete test suite with pytest
- Docker container support with multi-stage build
- Google Colab notebook for non-programmers
- Comprehensive documentation (README, USER_GUIDE, CONTRIBUTING)
- Pre-commit hooks for code quality (black, isort, ruff, mypy, bandit)
- CI/CD workflows (GitHub Actions)
- Example datasets with documentation
- Publication-ready HTML and Excel reports
- High-resolution PNG charts (150+ DPI)

### Features
- Automated detection of multidrug resistance (MDR) patterns
- Statistical significance testing with FDR correction for multiple testing
- Bootstrap confidence intervals for robust statistical inference
- Chi-square tests for gene-phenotype associations
- Fisher's exact test for rare events
- Interactive HTML reports with sortable tables
- Excel workbooks with multiple sheets (summary, detailed results, methodology)
- CSV export capabilities for downstream analysis

### Technical Details
- Python 3.8+ support
- Reproducible analyses with fixed random seeds
- Bootstrap resampling for statistical robustness
- FDR correction for multiple testing
- Interactive visualizations with Plotly
- Command-line interface (CLI) for batch processing
- Python API for programmatic access
- Docker containerization for consistent environments

## Project History

This tool was developed as part of the StrepSuis Suite for bacterial genomics research, 
with a focus on *Streptococcus suis* but applicable to any bacterial species.

[Unreleased]: https://github.com/MK-vet/strepsuis-amrpat/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/MK-vet/strepsuis-amrpat/releases/tag/v1.0.0
