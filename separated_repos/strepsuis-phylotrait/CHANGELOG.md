# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-01-14

### Added
- Initial release of StrepSuis-PhyloTrait
- Tree-aware clustering with evolutionary distance metrics
- Faith's Phylogenetic Diversity (PD) calculations for biodiversity assessment
- Pairwise phylogenetic distance matrices from Newick trees
- Binary trait analysis for AMR genes and virulence factors
- UMAP dimensionality reduction for phylogenetic visualization
- Bootstrap resampling for robust statistical inference (configurable iterations)
- Phylogenetic diversity analysis with tree-based metrics
- Trait evolution analysis on phylogenetic trees
- Tree-based statistical testing (phylogenetic signal, trait clustering)
- Statistical significance testing with FDR correction for multiple testing
- Interactive HTML reports with phylogenetic trees and DataTables
- Plotly visualizations for tree exploration and trait mapping
- Excel output with detailed statistical results and phylogenetic metrics
- High-resolution PNG chart export (150+ DPI) for publications
- Complete test suite with pytest
- Docker container support with multi-stage build
- Google Colab notebook for non-programmers
- Comprehensive documentation (README, USER_GUIDE, CONTRIBUTING)
- CI/CD workflows (GitHub Actions)
- Pre-commit hooks for code quality (black, isort, ruff, mypy, bandit)
- Example datasets with phylogenetic trees

### Features
- Phylogenetic tree parsing from Newick format
- Evolutionary-aware trait clustering
- Phylogenetic signal detection (Moran's I, phylogenetic autocorrelation)
- Ancestral state reconstruction for binary traits
- Tree visualization with trait mapping
- Support for ultrametric and non-ultrametric trees
- Integration with standard genomic data (AMR, virulence, MIC)

### Technical Details
- Python 3.8+ support
- Reproducible analyses with fixed random seeds
- Bootstrap resampling for statistical robustness
- FDR correction for multiple testing
- Interactive visualizations with Plotly
- Phylogenetic analysis with Bio.Phylo and ETE Toolkit
- Command-line interface (CLI) and Python API
- Newick tree format support

## Project History

This tool was developed as part of the StrepSuis Suite for bacterial genomics research, 
with a focus on *Streptococcus suis* but applicable to any bacterial species.

[Unreleased]: https://github.com/MK-vet/strepsuis-phylotrait/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/MK-vet/strepsuis-phylotrait/releases/tag/v1.0.0
