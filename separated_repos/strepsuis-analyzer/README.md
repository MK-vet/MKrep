# StrepSuisAnalyzer: Interactive Analysis Platform for *Streptococcus suis* Genomics

> **Current Location**: This module is part of the [MKrep repository](https://github.com/MK-vet/MKrep) under `separated_repos/strepsuis-analyzer/`. Designed to become a standalone repository in the future.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen)]()

**Interactive Streamlit-based application for comprehensive genomic and phenotypic analysis of *Streptococcus suis* data**

## Overview

StrepSuisAnalyzer is a production-ready interactive web application for advanced bioinformatics analysis. Originally developed for *Streptococcus suis* genomics but applicable to any bacterial species.

### Key Features

- ✅ **Interactive Web Interface**: Streamlit-based UI for easy data exploration
- ✅ **Comprehensive Statistical Analysis**: Correlations, hypothesis tests, meta-analysis
- ✅ **Advanced Visualizations**: Interactive plots with Plotly and publication-quality matplotlib figures
- ✅ **Phylogenetic Analysis**: Tree visualization, Robinson-Foulds distance, bipartition analysis
- ✅ **Machine Learning**: K-Means, K-Modes, Hierarchical, DBSCAN clustering
- ✅ **ETL Operations**: Pivot tables, aggregations, window functions, custom formulas
- ✅ **Report Generation**: Export to Excel and HTML formats

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- 4GB RAM minimum (8GB recommended for large datasets)

### Installation

#### Option 1: From Current Location (MKrep Repository)
```bash
# Clone the main repository
git clone https://github.com/MK-vet/MKrep.git
cd MKrep/separated_repos/strepsuis-analyzer
pip install -e .
```

#### Option 2: Using Docker
```bash
cd MKrep/separated_repos/strepsuis-analyzer
docker-compose up
```

Access the application at http://localhost:8501

### Usage

#### Launch Web Interface
```bash
# Using CLI
strepsuis-analyzer --launch

# Or directly with Python
python -m streamlit run src/strepsuis_analyzer/app.py
```

#### Using Docker
```bash
docker-compose up
# Access at http://localhost:8501
```

## Supported Data Types

StrepSuisAnalyzer supports the following data types:

| Data Type | Format | Description | Example Dimensions |
|-----------|--------|-------------|-------------------|
| **AMR Genes** | CSV (binary) | Antimicrobial resistance gene presence/absence | 91 strains × 21 genes |
| **MIC Values** | CSV (numeric) | Minimum inhibitory concentrations | 91 strains × 13 antibiotics |
| **Virulence Factors** | CSV (binary) | Virulence gene presence/absence | 91 strains × 106 factors |
| **MLST Data** | CSV (categorical) | Multi-locus sequence typing | 91 strains × ST types |
| **Serotypes** | CSV (categorical) | Serotype classifications | 91 strains |
| **Plasmid Data** | CSV | Plasmid information | Variable entries |
| **MGE Data** | CSV | Mobile genetic elements | Variable entries |
| **Phylogenetic Trees** | Newick | Phylogenetic relationships | 91 taxa |

## Features

### 1. Data Loading and Validation
- Upload custom CSV files or use example datasets
- Comprehensive data validation (shape, type, missing values)
- Binary matrix validation for genomic data
- Newick tree format validation

### 2. Statistical Analysis
- **Correlation Analysis**: Pearson, Spearman, Kendall, Phi coefficient, Cramér's V
- **Normality Testing**: Shapiro-Wilk test with Q-Q plots
- **Hypothesis Tests**: t-test, Mann-Whitney U, ANOVA, Kruskal-Wallis
- **Multiple Testing Correction**: Bonferroni, FDR (Benjamini-Hochberg)
- **Meta-Analysis**: Fixed-effects and random-effects models, Cochran's Q test
- **Information Theory**: Entropy, mutual information

### 3. Visualizations
- **Exploratory**: Histograms, scatter plots, box plots, violin plots
- **Statistical**: Q-Q plots, correlation heatmaps
- **Interactive**: Plotly-based interactive visualizations
- **Publication-Ready**: High-resolution matplotlib exports (SVG, PDF, PNG)

### 4. Clustering Analysis
- **K-Means**: Numeric data clustering with elbow plots
- **K-Modes**: Categorical data clustering (optimal for genomic binary data)
- **Hierarchical**: Dendrogram-based hierarchical clustering
- **DBSCAN**: Density-based clustering for complex patterns

### 5. Phylogenetic Analysis
- **Tree Visualization**: Interactive and static tree plots
- **Robinson-Foulds Distance**: Tree comparison metric
- **Bipartition Analysis**: Compare tree topologies
- **Faith's Phylogenetic Diversity**: Biodiversity metrics
- **Cophenetic Correlation**: Tree quality assessment

### 6. ETL Operations
- **Pivot Tables**: Flexible data reshaping
- **Aggregations**: Group-by operations with multiple functions
- **Window Functions**: Rolling statistics
- **Custom Formulas**: Apply custom calculations
- **Data Normalization**: Z-score, min-max, robust scaling
- **Merging**: Join datasets on common keys

### 7. Report Generation
- **Excel Export**: Multi-sheet workbooks with styled headers
- **HTML Reports**: Self-contained HTML with CSS styling
- **Metadata Tracking**: Automatic timestamp and version tracking

## Example Data

The package includes example datasets from 91 *Streptococcus suis* strains:

```python
from pathlib import Path
import pandas as pd

# Load example AMR data
amr_data = pd.read_csv('data/AMR_genes.csv', index_col=0)
print(f"AMR genes: {amr_data.shape}")  # (91, 21)

# Load example MIC data
mic_data = pd.read_csv('data/MIC.csv', index_col=0)
print(f"MIC values: {mic_data.shape}")  # (91, 13)

# Load phylogenetic tree
with open('data/Snp_tree.newick') as f:
    tree = f.read()
```

## API Usage

```python
from strepsuis_analyzer import (
    DataValidator,
    StatisticalAnalyzer,
    PhylogeneticAnalyzer,
    Visualizer,
    ReportGenerator
)

# Validate data
validator = DataValidator()
is_valid, errors, warnings = validator.validate_dataframe(df)

# Statistical analysis
analyzer = StatisticalAnalyzer(random_state=42)
corr, pval = analyzer.compute_correlation(x, y, method='pearson')

# Phylogenetic analysis
phylo = PhylogeneticAnalyzer()
phylo.load_tree_from_newick(tree_string)
rf_distance = phylo.compute_robinson_foulds_distance(tree1, tree2)

# Visualization
viz = Visualizer()
fig = viz.create_scatter_plot(x, y, show_regression=True)

# Generate reports
report = ReportGenerator()
report.add_dataframe('Results', results_df)
report.export_to_excel('report.xlsx')
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e .[dev]

# Run all tests
pytest -v

# Run with coverage
pytest --cov=strepsuis_analyzer --cov-report=html

# Run specific test categories
pytest -m mathematical  # Mathematical validation tests
pytest -m synthetic     # Synthetic data tests
pytest -m integration   # Integration tests
```

### Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint
ruff src/ tests/

# Type checking
mypy src/
```

## Testing

The package includes comprehensive test coverage (>85%):

- **Unit Tests**: Individual function testing (>400 tests)
- **Mathematical Validation**: 100% coverage of mathematical properties
- **Synthetic Data Tests**: Known ground-truth validation
- **Integration Tests**: End-to-end workflow testing

### Mathematical Properties Tested

✅ Entropy bounds: 0 ≤ H(X) ≤ log₂(n)  
✅ Mutual information symmetry: MI(X,Y) = MI(Y,X)  
✅ Cramér's V bounds: 0 ≤ V ≤ 1  
✅ Correlation bounds: -1 ≤ r ≤ 1  
✅ P-value bounds: 0 ≤ p ≤ 1  
✅ Robinson-Foulds distance: RF ≥ 0  
✅ Meta-analysis variance positivity

## Docker Deployment

### Building the Image

```bash
docker build -t strepsuis-analyzer .
```

### Running with Docker Compose

```bash
docker-compose up -d
```

### Customization

Edit `docker-compose.yml` to customize:
- Port mappings
- Volume mounts for data persistence
- Environment variables

## Documentation

- **[API Documentation](docs/API.md)**: Complete API reference
- **[Testing Guide](docs/TESTING.md)**: Testing procedures and coverage
- **[Mathematical Validation](docs/MATHEMATICAL_VALIDATION.md)**: Statistical validation methodology

## Citation

If you use StrepSuisAnalyzer in your research, please cite:

```bibtex
@software{strepsuis_analyzer,
  title = {StrepSuisAnalyzer: Interactive Analysis Platform for Streptococcus suis Genomics},
  author = {MK-vet},
  year = {2024},
  url = {https://github.com/MK-vet/strepsuis-analyzer},
  version = {1.0.0}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## Support

- **Issues**: [GitHub Issues](https://github.com/MK-vet/strepsuis-analyzer/issues)
- **Email**: support@strepsuis-suite.org

## Acknowledgments

Part of the StrepSuis Suite for comprehensive *Streptococcus suis* analysis:
- [strepsuis-mdr](../strepsuis-mdr/): MDR pattern detection
- [strepsuis-amrvirkm](../strepsuis-amrvirkm/): K-modes clustering
- [strepsuis-genphennet](../strepsuis-genphennet/): Network-based analysis
- [strepsuis-phylotrait](../strepsuis-phylotrait/): Phylogenetic trait analysis

---

**Version:** 1.0.0  
**Python:** 3.8+  
**License:** MIT  
**Status:** Production/Stable
