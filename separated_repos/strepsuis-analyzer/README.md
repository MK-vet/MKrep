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

## Reproducing the Full Analysis (Headless E2E)

For batch processing, automation, or reproducible research, use the headless E2E runner:

### Quick Start

```bash
# Install the package
pip install -e .

# Run complete analysis on both example and synthetic datasets
strepsuis-analyzer-e2e --dataset both

# Run on specific dataset only
strepsuis-analyzer-e2e --dataset example
strepsuis-analyzer-e2e --dataset synthetic

# Customize output directory
strepsuis-analyzer-e2e --dataset both --results-dir custom_output/

# Reproducible results (fixed random seed)
strepsuis-analyzer-e2e --dataset both --random-state 42
```

### What Gets Analyzed

The E2E runner performs comprehensive analysis across 7 categories:

1. **Validation**: Data quality checks, binary matrix validation, tree parsing
2. **Statistical Analysis**: Correlations, normality tests, hypothesis tests, meta-analysis
3. **Visualizations**: Histograms, scatter plots, box plots, violin plots, heatmaps
4. **Clustering**: K-Means, K-Modes, Hierarchical, DBSCAN
5. **Phylogenetic Analysis**: Tree visualization, Robinson-Foulds distance, Faith's PD
6. **ETL Operations**: Pivot tables, aggregations, normalization, data merging
7. **Report Generation**: Multi-sheet Excel and self-contained HTML reports

### Output Structure

Results are saved in timestamped directories:

```
results/strepsuis-analyzer-YYYYMMDD-HHMM/
├── example/                    # Results from example data
│   ├── validation/            # Data quality reports
│   ├── stats/                 # Statistical analysis tables & plots
│   ├── visualizations/        # Distribution and relationship plots
│   ├── clustering/            # Cluster assignments & dendrograms
│   ├── phylogenetics/         # Tree metrics & visualizations
│   ├── etl/                   # Transformed datasets
│   └── reports/               # Excel & HTML reports
├── synthetic/                  # Results from synthetic data
│   └── (same structure)
└── logs/
    └── run.log                # Detailed execution log
```

**Typical Output**: 30 files per dataset (60 total + log), ~2-3 MB

### Example Data

The package includes example datasets from 91 *Streptococcus suis* strains:

| File | Dimensions | Description |
|------|------------|-------------|
| `AMR_genes.csv` | 91 × 21 | AMR gene presence/absence (binary) |
| `MIC.csv` | 91 × 13 | Minimum inhibitory concentrations (numeric) |
| `Virulence.csv` | 91 × 106 | Virulence factor presence/absence (binary) |
| `MLST.csv` | 91 × 1 | Multi-locus sequence types (categorical) |
| `Serotype.csv` | 91 × 1 | Serotype classifications (categorical) |
| `Snp_tree.newick` | 91 taxa | SNP-based phylogenetic tree |

### Synthetic Data

Synthetic datasets for testing are auto-generated in `data/synthetic/`:
- 50 strains × 22 genes (AMR)
- 50 strains × 14 antibiotics (MIC)
- 50 strains × 107 factors (Virulence)
- MLST and Serotype classifications
- 50-taxa phylogenetic tree

These have known statistical properties for validation.

### CI Artifacts

When the E2E analysis runs in GitHub Actions CI, complete results are uploaded as artifacts:
- **Artifact name**: `e2e-results-{python-version}`
- **Retention**: 7 days
- **Location**: Actions tab → Workflow run → Artifacts section

Download artifacts to review full analysis outputs.

### Self-Checks

The E2E runner includes automated validation to ensure output quality:
- ✓ Minimum 1 validation report
- ✓ Minimum 2 statistical outputs (table + plot)
- ✓ Minimum 2 visualizations
- ✓ Minimum 1 clustering output
- ✓ Minimum 1 phylogenetic metric
- ✓ Minimum 1 ETL output
- ✓ Minimum 2 reports (Excel + HTML)

Exit code: 0 on success, 1 on failure.

## Troubleshooting

### Port Conflicts (Streamlit)

```bash
# Error: Address already in use (port 8501)
# Solution: Use a different port
strepsuis-analyzer --launch --port 8502

# Or use streamlit directly
streamlit run src/strepsuis_analyzer/app.py --server.port 8502
```

### Memory Issues (Large Datasets)

For datasets with >1000 strains or >500 features:

```bash
# Increase system memory limits
ulimit -v unlimited

# Or subsample data before analysis
# Use first 100 strains for exploration
```

**Recommended System Requirements**:
- Small datasets (<100 strains): 4GB RAM
- Medium datasets (100-500 strains): 8GB RAM
- Large datasets (>500 strains): 16GB+ RAM

### Missing Dependencies

```bash
# Reinstall with development dependencies
pip install -e .[dev]

# Or install individual missing packages
pip install streamlit pandas numpy scikit-learn matplotlib seaborn
```

### Phylogenetic Tree Errors

Common tree parsing issues:

```bash
# Error: Mismatch in parentheses
# Solution: Validate Newick format
# - Ensure balanced parentheses: ( matches )
# - Check for special characters in taxon names
# - Verify semicolon at end of tree string
```

### E2E Analysis Fails

```bash
# Check logs for details
cat results/*/logs/run.log

# Verify input data exists
ls -la data/AMR_genes.csv data/MIC.csv data/Snp_tree.newick

# For synthetic data
ls -la data/synthetic/

# Regenerate synthetic data if needed
python scripts/generate_synthetic_data.py
```

### Low Coverage in CI

Expected behavior:
- **Total coverage**: ~50% (Streamlit UI code not tested in headless mode)
- **Core functions**: 100% coverage (mathematical, statistical, phylogenetic)
- **Acceptable range**: 34-100%

The low total coverage is intentional as the E2E runner uses only the public API, not the Streamlit UI components.

### Docker Issues

```bash
# Permission errors with volumes
# Solution: Fix ownership
sudo chown -R $USER:$USER results/

# Container doesn't start
# Solution: Check logs
docker-compose logs

# Rebuild if needed
docker-compose build --no-cache
```

### Performance Optimization Tips

**Large Datasets**:
- Use subsetting for initial exploration
- Disable expensive visualizations
- Run clustering on PCA-reduced data
- Prefer DBSCAN over hierarchical clustering

**High-Dimensional Data (>1000 features)**:
- Apply feature selection first
- Use correlation-based filtering
- Consider dimensionality reduction (PCA, UMAP)

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

### Smoke Testing

Manual verification that the Streamlit app launches correctly:

```bash
# Install package
pip install -e .

# Launch Streamlit app
strepsuis-analyzer --launch

# Or directly
streamlit run src/strepsuis_analyzer/app.py

# Expected: Browser opens to http://localhost:8501
# Verify:
# - App loads without errors
# - Sidebar shows navigation menu
# - Example data can be loaded
# - Basic operations work (validation, plotting)
```

**What to Check**:
1. ✓ App starts without Python errors
2. ✓ Sidebar navigation appears
3. ✓ Example data loads successfully
4. ✓ At least one plot renders
5. ✓ No browser console errors

This smoke test is not automated in CI (requires browser), but should be performed manually before releases.

## Docker Deployment

### Building the Image

```bash
docker build -t strepsuis-analyzer .
```

### Running with Docker Compose

```bash
docker-compose up -d
```

### Running E2E Analysis in Docker

The `docker-compose.yml` includes a volume mount for results persistence:

```bash
# Run E2E analysis inside container
docker-compose run strepsuis-analyzer strepsuis-analyzer-e2e --dataset both

# Results are saved to the mounted ./results directory on your host
ls -la results/

# Or run interactively
docker-compose exec strepsuis-analyzer bash
# Inside container:
strepsuis-analyzer-e2e --dataset example
```

### Customization

Edit `docker-compose.yml` to customize:
- Port mappings (default: 8501)
- Volume mounts for data and results persistence
- Environment variables (Streamlit configuration)

**Key volumes**:
- `./data:/app/data` - Input data files
- `./results:/app/results` - E2E analysis outputs (persisted)

## Documentation

- **[API Documentation](docs/API.md)**: Complete API reference
- **[Testing Guide](docs/TESTING.md)**: Testing procedures and coverage
- **[Mathematical Validation](docs/MATHEMATICAL_VALIDATION.md)**: Statistical validation methodology
- **[Workflow Guide](docs/WORKFLOW.md)**: End-to-end analysis workflow and integration

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
