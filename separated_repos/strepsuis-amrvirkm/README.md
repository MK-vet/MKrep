# StrepSuis-AMRVirKM: K-Modes Clustering of Antimicrobial Resistance and Virulence Profiles

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/strepsuis-amrvirkm/blob/main/notebooks/AMRVirKM_Analysis.ipynb)

**Professional bioinformatics tool for comprehensive clustering analysis of antimicrobial resistance and virulence profiles in bacterial genomics.**

## Overview

StrepSuis-AMRVirKM is a production-ready Python package that performs advanced clustering analysis of antimicrobial resistance (AMR) and virulence factor profiles. Originally developed for *Streptococcus suis* genomics but applicable to any bacterial species.

### Key Features

- ✅ **K-Modes Clustering** with automatic silhouette optimization
- ✅ **Multiple Correspondence Analysis (MCA)** for dimensionality reduction
- ✅ **Feature Importance Ranking** using Random Forest and chi-square tests
- ✅ **Association Rule Discovery** with Apriori algorithm
- ✅ **Bootstrap Confidence Intervals** for robust statistical inference
- ✅ **Publication-Quality Reports** in HTML and Excel formats
- ✅ **High-Resolution Charts** (150+ DPI) ready for scientific publications
- ✅ **Full Reproducibility** with documented parameters and fixed random seeds

## Quick Start

### Installation

```bash
# Install from PyPI
pip install strepsuis-amrvirkm

# Or install from source
git clone https://github.com/MK-vet/strepsuis-amrvirkm.git
cd strepsuis-amrvirkm
pip install -e .
```

### Usage

#### Command Line Interface

```bash
# Run cluster analysis
strepsuis-amrvirkm --data-dir ./data --output ./results

# With custom parameters
strepsuis-amrvirkm \
  --data-dir ./data \
  --output ./results \
  --max-clusters 8 \
  --bootstrap 1000 \
  --fdr-alpha 0.05
```

#### Python API

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

#### Google Colab (No Installation!)

Click the badge above or use this link:
[Open in Google Colab](https://colab.research.google.com/github/MK-vet/strepsuis-amrvirkm/blob/main/notebooks/AMRVirKM_Analysis.ipynb)

- Upload your CSV files
- Run all cells
- Download results automatically

### Docker

```bash
# Pull and run
docker pull mkvet/strepsuis-amrvirkm:latest
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
    mkvet/strepsuis-amrvirkm:latest \
    --data-dir /data --output /output

# Or build locally
docker build -t strepsuis-amrvirkm .
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
    strepsuis-amrvirkm --data-dir /data --output /output
```

## Input Data Format

All input files should be CSV format with:
- **Strain_ID** column (required): Unique identifier for each strain
- **Binary features** (0 = absence, 1 = presence): Gene presence, resistance, virulence factors

Required files:
- `MIC.csv`: Minimum Inhibitory Concentration data
- `AMR_genes.csv`: Antimicrobial resistance genes
- `Virulence.csv`: Virulence factors

Optional files:
- `MLST.csv`: Multi-locus sequence typing
- `Serotype.csv`: Serological types
- `Plasmid.csv`: Plasmid presence/absence
- `MGE.csv`: Mobile genetic elements

Example:
```csv
Strain_ID,Gene1,Gene2,Antibiotic1,Virulence1
Strain001,1,0,1,0
Strain002,0,1,1,1
Strain003,1,1,0,1
```

## Output

Each analysis generates:

1. **HTML Report** (`Cluster_Analysis_report.html`)
   - Interactive tables with sorting, filtering, and export
   - Embedded high-quality visualizations
   - Statistical methodology and interpretation sections

2. **Excel Report** (`Cluster_Analysis_Report_<timestamp>.xlsx`)
   - Multiple sheets with organized results
   - Metadata and methodology documentation
   - Chart index for easy navigation

3. **PNG Charts** (`png_charts/` directory)
   - High-resolution visualizations (150+ DPI)
   - Publication-ready quality
   - Individual files for each chart

## Statistical Methods

- **K-Modes Clustering**: Categorical data clustering with Huang's algorithm
- **Silhouette Analysis**: Automatic optimal cluster number determination
- **Multiple Correspondence Analysis (MCA)**: Dimensionality reduction for categorical variables
- **Chi-square Tests**: Feature-cluster associations with FDR correction
- **Random Forest**: Feature importance ranking
- **Bootstrap Resampling**: Robust confidence interval estimation
- **Association Rule Mining**: Apriori algorithm for pattern discovery

## Documentation

See [USER_GUIDE.md](USER_GUIDE.md) for detailed installation instructions and usage examples.

- **[Examples](examples/)**: Sample datasets and analysis examples

## Requirements

- Python >= 3.8
- pandas >= 1.3.0
- numpy >= 1.21.0
- scikit-learn >= 1.0.0
- kmodes >= 0.12.0
- prince >= 0.7.0
- mlxtend >= 0.19.0
- plotly >= 5.0.0
- matplotlib >= 3.4.0

See [requirements.txt](requirements.txt) for complete dependency list.

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

MIT License - see [LICENSE](LICENSE) file for details

## Support

- **GitHub Issues**: [github.com/MK-vet/strepsuis-amrvirkm/issues](https://github.com/MK-vet/strepsuis-amrvirkm/issues)
- **Documentation**: [Full Documentation](https://mk-vet.github.io/strepsuis-amrvirkm/)
- **Email**: support@strepsuis-suite.org

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Acknowledgments

Part of the StrepSuis Suite - comprehensive bioinformatics tools for *Streptococcus suis* genomics research.

## Related Tools

- [StrepSuis-AMRPat](https://github.com/MK-vet/strepsuis-amrpat): MDR pattern detection
- [StrepSuis-GenPhenNet](https://github.com/MK-vet/strepsuis-genphennet): Network analysis
- [StrepSuis-PhyloTrait](https://github.com/MK-vet/strepsuis-phylotrait): Phylogenetic clustering
- [StrepSuis-GenPhen](https://github.com/MK-vet/strepsuis-genphen): Genomic-phenotypic analysis
