# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-01-14

### Added
- Initial release of StrepSuis-GenPhenNet
- Chi-square and Fisher exact tests with FDR correction for statistical rigor
- Information theory metrics (entropy, mutual information, Cramér's V) for association strength
- Mutually exclusive pattern detection for competitive relationships
- 3D network visualization with Plotly for interactive exploration
- Community detection algorithms (Louvain, label propagation) for module identification
- Bootstrap resampling for robust network inference (configurable iterations)
- Network-based integration of genome-phenome data
- Multi-omics data integration (AMR genes, virulence, MIC, MLST, serotypes)
- Statistical significance testing with FDR correction for multiple testing
- Interactive HTML reports with sortable tables and network visualizations
- Excel output with detailed statistical results and network metrics
- High-resolution PNG chart export (150+ DPI) for publications
- Complete test suite with pytest
- Docker container support with multi-stage build
- Google Colab notebook for non-programmers
- Comprehensive documentation (README, USER_GUIDE, CONTRIBUTING)
- CI/CD workflows (GitHub Actions)
- Pre-commit hooks for code quality (black, isort, ruff, mypy, bandit)
- Example datasets with documentation

### Features
- Network construction from binary genomic and phenotypic features
- Edge weight calculation using multiple statistical measures
- Community structure analysis for functional module detection
- Pathway enrichment and pattern discovery
- Interactive 3D network exploration with node/edge filtering
- Support for directed and undirected networks
- Statistical validation of network properties

### Technical Details
- Python 3.8+ support
- Reproducible analyses with fixed random seeds
- Bootstrap resampling for statistical robustness
- FDR correction for multiple testing
- Interactive 3D visualizations with Plotly
- Graph analysis with NetworkX
- Command-line interface (CLI) and Python API

## Project History

This tool was developed as part of the StrepSuis Suite for bacterial genomics research, 
with a focus on *Streptococcus suis* but applicable to any bacterial species.

[Unreleased]: https://github.com/MK-vet/strepsuis-genphennet/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/MK-vet/strepsuis-genphennet/releases/tag/v1.0.0
