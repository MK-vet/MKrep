# Changelog

All notable changes to StrepSuis Analyzer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2025.8.11] - 2025-08-11

### Added
- Initial release of StrepSuis Analyzer
- Core clustering and trait association analysis
- HTML and Excel report generation
- MCA (Multiple Correspondence Analysis) dimensionality reduction
- Phylogenetic tree integration support
- Bootstrap 5 web interface for HTML reports
- Command-line interface for easy data analysis
- Docker support for containerized deployment
- Comprehensive test suite
- CI/CD workflows for automated testing
- User guide and documentation
- Example datasets and notebooks

### Features
- **Hierarchical Clustering**: Jaccard distance with Ward linkage
- **Statistical Tests**: Chi-square test, Cramér's V, FDR correction
- **Dimensionality Reduction**: MCA for binary data visualization
- **Interactive Reports**: HTML reports with Plotly visualizations
- **Excel Export**: Multi-sheet workbooks with detailed results
- **Phylogenetic Integration**: Optional tree-based distance calculations
- **Reproducibility**: Fixed random seeds for deterministic results

### Documentation
- README with comprehensive usage examples
- TESTING.md with detailed testing instructions
- USER_GUIDE.md with step-by-step tutorials
- CONTRIBUTING.md for contributors
- SECURITY.md for security policies
- CITATION.cff for proper citation

### Infrastructure
- GitHub Actions CI/CD workflows
- Docker and docker-compose support
- Pre-commit hooks for code quality
- Pytest configuration with coverage reporting

### Dependencies
- Python 3.8+ support
- Core scientific stack: numpy, pandas, scipy, scikit-learn
- Visualization: matplotlib, seaborn, plotly
- Clustering: kmodes, prince (for MCA)
- Phylogenetics: biopython
- Reporting: openpyxl, jinja2

## [Unreleased]

### Planned
- Bootstrap confidence intervals for associations
- Additional clustering algorithms (K-modes, DBSCAN)
- Network analysis integration
- Command-line progress bars
- More example datasets
- Jupyter notebook tutorials
- API documentation with Sphinx

---

## Release Notes Format

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security fixes or improvements
