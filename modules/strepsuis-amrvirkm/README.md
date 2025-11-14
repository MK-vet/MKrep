# StrepSuis-AMRVirKM: K-Modes Clustering of Antimicrobial Resistance and Virulence Profiles

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/strepsuis-amrvirkm/blob/main/notebooks/cluster_analysis.ipynb)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://hub.docker.com)

## Overview

StrepSuis-AMRVirKM is a comprehensive bioinformatics tool for clustering analysis of antimicrobial resistance (AMR) and virulence profiles in bacterial genomics. It uses K-Modes clustering optimized for categorical binary data (0/1), combined with Multiple Correspondence Analysis (MCA) and association rule mining.

### Key Features

- **K-Modes Clustering**: Optimized for categorical binary data (presence/absence)
- **Automatic Cluster Selection**: Silhouette score optimization (2-10 clusters)
- **Multiple Correspondence Analysis (MCA)**: Dimensionality reduction for visualization
- **Feature Importance Ranking**: Identify key discriminating features
- **Association Rule Mining**: Discover co-occurrence patterns (Apriori algorithm)
- **Bootstrap Confidence Intervals**: Robust statistical inference (200-1000 resamples)
- **Professional Reports**: Interactive HTML and Excel formats
- **Publication-Ready Charts**: High-resolution PNG exports (150+ DPI)

### Statistical Methods

- Chi-square and Fisher exact tests with FDR correction
- Log-odds ratios with confidence intervals
- Random Forest feature importance
- Stratified bootstrap resampling
- Silhouette, Calinski-Harabasz, and Davies-Bouldin clustering metrics

## Quick Start

### Option 1: Google Colab (No Installation Required) ⭐ Recommended for Beginners

Click the badge below to run the analysis in Google Colab:

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/strepsuis-amrvirkm/blob/main/notebooks/cluster_analysis.ipynb)

**Steps:**
1. Click the Colab badge
2. Upload your CSV files (MIC.csv, AMR_genes.csv, Virulence.csv)
3. Run all cells (Runtime → Run all)
4. Download results (HTML report, Excel file, PNG charts)

**No coding knowledge required!** The notebook guides you through each step.

### Option 2: Python Package Installation

```bash
# Install from PyPI (when published)
pip install strepsuis-amrvirkm

# Or install from GitHub
pip install git+https://github.com/MK-vet/strepsuis-amrvirkm.git

# Run analysis
strepsuis-amrvirkm --data-dir ./data --output ./results
```

### Option 3: Docker Container

```bash
# Pull and run with Docker
docker pull mkvet/strepsuis-amrvirkm:latest

# Run analysis
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
    mkvet/strepsuis-amrvirkm:latest \
    --data-dir /data --output /output
```

Or use Docker Compose:

```bash
# Clone repository
git clone https://github.com/MK-vet/strepsuis-amrvirkm.git
cd strepsuis-amrvirkm

# Run with Docker Compose
docker-compose up
```

### Option 4: Local Installation

```bash
# Clone repository
git clone https://github.com/MK-vet/strepsuis-amrvirkm.git
cd strepsuis-amrvirkm

# Install dependencies
pip install -r requirements.txt

# Run analysis
python -m strepsuis_amrvirkm.cli --data-dir ./examples/data --output ./results
```

## Usage

### Command Line Interface

```bash
# Basic usage
strepsuis-amrvirkm --data-dir ./data --output ./results

# Advanced options
strepsuis-amrvirkm \
    --data-dir ./data \
    --output ./results \
    --max-clusters 10 \
    --bootstrap 500 \
    --min-support 0.3 \
    --min-confidence 0.6
```

### Python API

```python
from strepsuis_amrvirkm import ClusterAnalyzer

# Initialize analyzer
analyzer = ClusterAnalyzer(
    data_dir="./data",
    output_dir="./results",
    max_clusters=8,
    bootstrap_iterations=500
)

# Run analysis
results = analyzer.run()

# Generate reports
analyzer.generate_html_report(results)
analyzer.generate_excel_report(results)
```

## Input Data Format

The tool expects CSV files with binary data (0 = absence, 1 = presence):

### Required Files

1. **MIC.csv**: Minimum Inhibitory Concentration data (resistance phenotypes)
2. **AMR_genes.csv**: Antimicrobial resistance genes
3. **Virulence.csv**: Virulence factors

### Format Requirements

- **First column**: `Strain_ID` (unique identifier)
- **Other columns**: Binary values (0 or 1)
- **Encoding**: UTF-8
- **Separator**: Comma (,)

### Example

```csv
Strain_ID,Gene1,Gene2,Antibiotic1,Virulence1
Strain001,1,0,1,0
Strain002,0,1,1,1
Strain003,1,1,0,1
```

**Important**: 
- **0 = Absence** (no gene, susceptible, negative)
- **1 = Presence** (gene present, resistant, positive)
- Both values are biologically significant
- Do not use missing values (NaN)

See [examples/data/](examples/data/) for sample datasets.

## Output Files

```
results/
├── Cluster_Analysis_Report_YYYYMMDD_HHMMSS.html  # Interactive HTML report
├── Cluster_Analysis_Report_YYYYMMDD_HHMMSS.xlsx  # Excel workbook
└── png_charts/                                    # High-quality PNG charts
    ├── kmodes_clusters_mca.png
    ├── silhouette_scores.png
    ├── feature_importance.png
    ├── association_rules.png
    └── cluster_composition.png
```

### Report Contents

**HTML Report:**
- Interactive DataTables (sortable, searchable, exportable)
- Plotly visualizations (zoomable, hover details)
- Statistical summaries with interpretation
- Bootstrap 5 styling
- Complete methodology

**Excel Report:**
- Metadata sheet (configuration, run info)
- Methodology sheet (detailed methods)
- Cluster assignments
- Feature importance rankings
- Association rules
- Statistical tests results
- Chart index

## Installation Requirements

### System Requirements

- Python 3.8 or higher
- 4 GB RAM minimum (8 GB recommended)
- 500 MB disk space

### Python Dependencies

Core packages (automatically installed):
- pandas, numpy, scipy
- scikit-learn, matplotlib, seaborn, plotly
- kmodes, prince, mlxtend
- openpyxl, jinja2, kaleido

See [requirements.txt](requirements.txt) for complete list.

### Platform Support

- **Operating Systems**: Windows, macOS, Linux
- **Python Versions**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Browsers** (for HTML reports): Chrome, Firefox, Safari, Edge

## Configuration

### Configuration File (Optional)

Create a `config.yaml` file:

```yaml
data_dir: "./data"
output_dir: "./results"
max_clusters: 10
bootstrap_iterations: 500
min_support: 0.3
min_confidence: 0.6
random_seed: 42
```

Run with config:
```bash
strepsuis-amrvirkm --config config.yaml
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--data-dir` | str | required | Directory containing CSV files |
| `--output` | str | `./results` | Output directory |
| `--max-clusters` | int | 8 | Maximum number of clusters to test |
| `--bootstrap` | int | 200 | Bootstrap iterations |
| `--min-support` | float | 0.3 | Minimum support for association rules |
| `--min-confidence` | float | 0.5 | Minimum confidence for association rules |
| `--seed` | int | 42 | Random seed for reproducibility |

## Documentation

- **[USAGE.md](docs/USAGE.md)**: Detailed usage guide
- **[API.md](docs/API.md)**: Python API reference
- **[EXAMPLES.md](docs/EXAMPLES.md)**: Example analyses and outputs
- **[notebooks/README.md](notebooks/README.md)**: Google Colab guide

## Examples

See [examples/](examples/) directory for:
- Sample datasets
- Example configurations
- Expected outputs
- Tutorial notebooks

## Citation

If you use StrepSuis-AMRVirKM in your research, please cite:

```bibtex
@software{strepsuis_amrvirkm2025,
  title = {StrepSuis-AMRVirKM: K-Modes Clustering of Antimicrobial Resistance and Virulence Profiles},
  author = {MK-vet},
  year = {2025},
  url = {https://github.com/MK-vet/strepsuis-amrvirkm},
  version = {1.0.0}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

- **Issues**: [GitHub Issues](https://github.com/MK-vet/strepsuis-amrvirkm/issues)
- **Discussions**: [GitHub Discussions](https://github.com/MK-vet/strepsuis-amrvirkm/discussions)
- **Documentation**: [docs/](docs/)

## Acknowledgments

This tool was developed for the microbial genomics research community. We thank all contributors and users for their feedback and support.

## Related Projects

- **StrepSuis-AMRPat**: MDR pattern detection
- **StrepSuis-GenPhenNet**: Network analysis
- **StrepSuis-PhyloTrait**: Phylogenetic clustering
- **StrepSuis-GenPhen**: Integrated genomic-phenotypic analysis

---

**Last Updated**: 2025-01-14  
**Status**: Production Ready  
**Maintainer**: MK-vet
