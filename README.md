# MKrep

Comprehensive bioinformatics analysis pipeline for microbial genomics, focusing on antimicrobial resistance (AMR), virulence factors, and phylogenetic relationships.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Cluster_Analysis_Colab.ipynb)

## Overview

This repository contains Python scripts for analyzing bacterial genomic data with a focus on:
- Phylogenetic clustering and tree-based analysis
- Antimicrobial resistance patterns and multi-drug resistance (MDR)
- Network analysis of gene-phenotype associations
- Binary trait profiling for virulence and resistance genes
- Clustering analysis with multiple statistical methods

## 🚀 Quick Start

### Option 1: Google Colab (No Installation Required)
Click to open interactive notebooks:
- [Cluster Analysis](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Cluster_Analysis_Colab.ipynb)
- [MDR Analysis](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/MDR_Analysis_Colab.ipynb)
- [Network Analysis](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Network_Analysis_Colab.ipynb)

### Option 2: Local Installation
```bash
git clone https://github.com/MK-vet/MKrep.git
cd MKrep
pip install -r requirements.txt
python Cluster_MIC_AMR_Viruelnce.py
```

### Option 3: Python Package (CLI)
```bash
pip install mkrep  # When published
mkrep-cluster --data-dir ./data --output ./results
```

### Option 4: Interactive Dashboard
Visit our [Hugging Face Demo](https://huggingface.co/spaces/MK-vet/mkrep-demo) (when deployed)

## Analysis Scripts

### 1. `Phylgenetic_clustering_2025_03_21.py`
Complete phylogenetic clustering and binary trait analysis with:
- Tree-aware clustering methods
- Evolutionary metrics (Faith's PD, pairwise distances)
- Binary trait analysis (AMR, virulence)
- Interactive HTML reports with DataTables and Plotly

### 2. `StrepSuisPhyloCluster_2025_08_11.py`
Integrative phylogenetic clustering tool for *Streptococcus suis* with:
- Tree-aware clustering with ensemble fallback
- Trait profiling (chi-square, log-odds, RF importance)
- Association rules and MCA
- Bootstrap 5 UI with CSV export

### 3. `Network_Analysis_2025_06_26.py`
Statistical network analysis for feature associations:
- Chi-square and Fisher exact tests
- Information theory metrics (entropy, Cramér's V)
- Mutually exclusive pattern detection
- 3D network visualization with community detection

### 4. `MDR_2025_04_15.py`
Enhanced MDR analysis with hybrid network approach:
- Bootstrap resampling for prevalence estimation
- Co-occurrence analysis (phenotypes and genes)
- Association rule mining
- Hybrid co-resistance network construction

### 5. `Cluster_MIC_AMR_Viruelnce.py`
Comprehensive clustering analysis for MIC, AMR, and virulence data:
- K-Modes clustering with silhouette optimization
- Multiple Correspondence Analysis (MCA)
- Feature importance and association rules
- Bootstrap confidence intervals

## ✨ NEW: Multiple Usage Options

### 📊 Comprehensive Reports
All scripts generate **both HTML and Excel reports** with:
- ✅ **Interactive HTML**: DataTables with sorting, filtering, and export
- ✅ **Excel Workbooks**: Multi-sheet reports with methodology documentation
- ✅ **High-quality PNG charts**: Saved separately for publications
- ✅ **Consistent styling**: Uniform appearance across all outputs

### 🎯 Multiple Deployment Options

1. **📓 Google Colab Notebooks**: Run in the cloud without installation
   - See [colab_notebooks/](colab_notebooks/) directory
   - One-click deployment with file upload/download
   - Free GPU access for faster processing

2. **📦 Python Package with CLI**: Install as a package
   - See [python_package/](python_package/) directory
   - Full command-line interface for all analyses
   - Python API for programmatic access

3. **🎨 Hugging Face Dashboard**: Interactive web interface
   - See [huggingface_demo/](huggingface_demo/) directory
   - Voilà-based dashboard with widgets
   - Drag-and-drop file upload

4. **💻 Standalone Scripts**: Traditional execution
   - Direct Python script execution
   - Maximum flexibility and customization

See [INSTALLATION.md](INSTALLATION.md) for complete setup instructions.

## Requirements

### Quick Install:
```bash
pip install -r requirements.txt
```

### Core Dependencies:
- Python >= 3.8
- pandas, numpy, scipy
- scikit-learn, matplotlib, plotly
- biopython, networkx
- See [requirements.txt](requirements.txt) for complete list

### Optional:
- `voila` - For interactive dashboards
- `jupyter` - For notebook execution
- GPU support - For accelerated processing (Google Colab)

## Installation

See [INSTALLATION.md](INSTALLATION.md) for detailed installation instructions for:
- Local installation (Windows, macOS, Linux)
- Google Colab setup
- Python package installation
- Docker deployment
- Troubleshooting guide

## Usage

### Option 1: Google Colab (Recommended for Beginners)
1. Click on a Colab notebook link above
2. Upload your CSV files when prompted
3. Run all cells
4. Download results (HTML, Excel, PNG charts)

[See Colab README](colab_notebooks/README.md) for details.

### Option 2: Command Line Interface
```bash
# Cluster analysis
mkrep-cluster --data-dir ./data --output ./results --bootstrap 500

# MDR analysis
mkrep-mdr --data-dir ./data --output ./results --mdr-threshold 3

# Network analysis
mkrep-network --data-dir ./data --output ./results

# Phylogenetic clustering
mkrep-phylo --tree tree.newick --data-dir ./data --output ./results

# StrepSuis analysis
mkrep-strepsuis --tree tree.newick --data-dir ./data --output ./results
```

[See Package README](python_package/README.md) for full CLI documentation.

### Option 3: Python API
```python
from mkrep.analysis import ClusterAnalyzer

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

### Option 4: Standalone Scripts
```bash
# Direct execution
python Cluster_MIC_AMR_Viruelnce.py
python MDR_2025_04_15.py
python Network_Analysis_2025_06_26.py
python Phylgenetic_clustering_2025_03_21.py
python StrepSuisPhyloCluster_2025_08_11.py
```

Each script will:
1. Load required data files (CSV format)
2. Perform analysis
3. Generate HTML report (interactive)
4. Generate Excel report (structured data)
5. Save PNG charts in `png_charts/` subfolder

### Input Data Format:

All scripts expect CSV files with a `Strain_ID` column:
- `MIC.csv`: Minimum Inhibitory Concentration data
- `AMR_genes.csv`: Antimicrobial resistance genes
- `Virulence.csv` / `Virulence3.csv`: Virulence factors
- `MLST.csv`: Multi-locus sequence typing
- `Serotype.csv`: Serological types
- `Plasmid.csv`: Plasmid presence/absence
- `MGE.csv`: Mobile genetic elements
- `tree.newick` / `tree.nwk`: Phylogenetic tree (for phylogenetic scripts)

**Important: Binary Data Format**
- **0 = Absence** of feature (gene, resistance, virulence factor)
- **1 = Presence** of feature
- Both absence and presence are biologically significant
- Do not use missing values (NaN) - encode as 0 or 1

Example:
```csv
Strain_ID,Gene1,Gene2,Antibiotic1,Virulence1
Strain001,1,0,1,0
Strain002,0,1,1,1
Strain003,1,1,0,1
```

### Output Files:

```
output/
├── <analysis>_Report_<timestamp>.xlsx    # Excel report
├── <analysis>_report.html                # HTML report
└── png_charts/                           # PNG visualizations
    ├── network_3d_visualization.png
    ├── phylogenetic_tree.png
    └── ...
```

## Features by Script

| Feature | Phylo_2025 | StrepSuis | Network | MDR | Cluster |
|---------|-----------|-----------|---------|-----|---------|
| Phylogenetic clustering | ✓ | ✓ | - | - | - |
| Network analysis | - | - | ✓ | ✓ | - |
| K-Modes clustering | - | - | - | - | ✓ |
| Chi-square tests | ✓ | ✓ | ✓ | ✓ | ✓ |
| Bootstrap CIs | ✓ | ✓ | - | ✓ | ✓ |
| Association rules | ✓ | ✓ | - | ✓ | ✓ |
| MCA | ✓ | ✓ | - | - | ✓ |
| Excel reports | ✓ | ✓ | ✓ | ✓ | ✓ |
| PNG charts | ✓ | ✓ | ✓ | ✓ | ✓ |

## Statistical Methods

- **Chi-square and Fisher exact tests** with FDR correction
- **Bootstrap resampling** for confidence intervals
- **Multiple Correspondence Analysis (MCA)** for dimensionality reduction
- **Random Forest** for feature importance
- **Association rule mining** (Apriori algorithm)
- **Network community detection** (Louvain algorithm)
- **Phylogenetic diversity metrics** (Faith's PD, UniFrac)
- **Clustering metrics** (Silhouette, Calinski-Harabasz, Davies-Bouldin)

## Configuration

Each script accepts configuration parameters. Example:

```python
config = Config(
    base_dir=".",
    output_folder="results",
    tree_file="tree.newick",
    umap_components=2,
    bootstrap_iterations=500,
    fdr_alpha=0.05
)
```

## Citation

If you use MKrep in your research, please cite:

```bibtex
@software{mkrep2025,
  title = {MKrep: Comprehensive Bioinformatics Analysis Pipeline for Microbial Genomics},
  author = {MK-vet},
  year = {2025},
  url = {https://github.com/MK-vet/MKrep},
  version = {1.0.0}
}
```

## License

MIT License - see [LICENSE](LICENSE) file for details

## Contact

For questions or support:
- **GitHub Issues**: [github.com/MK-vet/MKrep/issues](https://github.com/MK-vet/MKrep/issues)
- **Documentation**: See README files in each directory
- **Installation Help**: See [INSTALLATION.md](INSTALLATION.md)
- **Colab Issues**: See [colab_notebooks/README.md](colab_notebooks/README.md)

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Acknowledgments

This tool was developed for the microbial genomics research community. We thank all contributors and users for their feedback and support.

## Changelog

### 2025-01-07 - Version 1.0.0 🎉
- ✨ **Added Google Colab notebooks** for cloud-based analysis
- ✨ **Created Python package** with full CLI support
- ✨ **Developed Hugging Face demo** with Voilà dashboard
- ✨ **Comprehensive installation guide** (INSTALLATION.md)
- ✨ **Multiple deployment options** (Colab, CLI, Dashboard, Scripts)
- 📝 **Enhanced documentation** with usage examples
- 📝 **Binary data handling** explicitly documented (0=absence, 1=presence)
- ✨ Added comprehensive Excel report generation to all scripts
- ✨ Implemented PNG chart export for all visualizations
- ✨ Created shared utility module (`excel_report_utils.py`)
- 📝 Added detailed documentation for Excel reports
- 🎨 Standardized report structure across all analysis types

### Previous versions
- Initial implementations of analysis scripts
- HTML report generation with interactive features