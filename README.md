# StrepSuis_Suite

Comprehensive bioinformatics analysis suite for *Streptococcus suis* genomics, focusing on antimicrobial resistance (AMR), virulence factors, and phylogenetic relationships.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Interactive_Analysis_Colab.ipynb)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/MK-vet/MKrep/main?filepath=colab_notebooks%2FInteractive_Analysis_Colab.ipynb)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://hub.docker.com)
[![DOI](https://img.shields.io/badge/DOI-pending-lightgrey.svg)]()

[![CI - All Tools](https://github.com/MK-vet/MKrep/actions/workflows/ci.yml/badge.svg)](https://github.com/MK-vet/MKrep/actions/workflows/ci.yml)
[![Deployment Tests](https://github.com/MK-vet/MKrep/actions/workflows/deployment.yml/badge.svg)](https://github.com/MK-vet/MKrep/actions/workflows/deployment.yml)
[![Version Info](https://github.com/MK-vet/MKrep/actions/workflows/version-info.yml/badge.svg)](https://github.com/MK-vet/MKrep/actions/workflows/version-info.yml)

---

## 🌐 Interactive Tool Portal

**NEW!** Access all analysis tools through our interactive documentation portal:

### 👉 **[https://mk-vet.github.io/MKrep/](https://mk-vet.github.io/MKrep/)** 👈

The portal provides:
- 📊 **Dedicated pages for each analysis tool** with detailed documentation
- 🚀 **One-click access** to run tools in Google Colab
- 📁 **Demo datasets** ready to download and test
- 📈 **Example results** from completed analyses
- 🎯 **Quick navigation** designed for researchers reading scientific articles

**Perfect for external users who want to:**
- Quickly understand what each tool does
- Run analyses without installation
- See example outputs before using their own data
- Access all resources in one place

---

## Overview

This repository contains **production-ready** Python scripts for analyzing bacterial genomic data with a focus on:
- Phylogenetic clustering and tree-based analysis
- Antimicrobial resistance patterns and multi-drug resistance (MDR)
- Network analysis of gene-phenotype associations
- Binary trait profiling for virulence and resistance genes
- Clustering analysis with multiple statistical methods

### 🔬 Production-Ready for Scientific Publications

All tools in this repository are **fully functional and production-ready**, not demos:

- ✅ **Publication-quality outputs**: High-resolution charts (150+ DPI) and professional reports
- ✅ **Reproducible research**: Fixed random seeds, documented parameters, complete methodology
- ✅ **Peer-review ready**: Comprehensive documentation and validation
- ✅ **Multi-platform support**: Works on Linux, macOS, Windows (Python 3.8-3.12)
- ✅ **Independent tools**: Each tool can be used standalone while maintaining consistent appearance
- ✅ **User-accessible**: Multiple deployment options for different skill levels
- ✅ **Computational flexibility**: Support for local execution and cloud computing (Google Colab/Colab Pro)

**For researchers:** All tools generate standardized reports suitable for scientific publications. Methods are fully documented and results are reproducible.

## 🚀 Quick Start

### Option 1: Google Colab (No Installation Required)

#### A. Interactive Interface (No Coding!)
**NEW!** User-friendly interface with buttons and widgets:
- [**Interactive Analysis**](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Interactive_Analysis_Colab.ipynb) - Perfect for non-programmers!
  - Upload files with drag-and-drop
  - Select analysis type from dropdown
  - Configure parameters with sliders
  - Click one button to run
  - Download results automatically

#### B. Advanced Notebooks (For Researchers)
Detailed notebooks with full code and explanations:
- [Cluster Analysis](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Cluster_Analysis_Colab.ipynb)
- [MDR Analysis](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/MDR_Analysis_Colab.ipynb)
- [Network Analysis](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Network_Analysis_Colab.ipynb)
- [Phylogenetic Clustering](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Phylogenetic_Clustering_Colab.ipynb)
- [Streptococcus suis Analysis](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/StrepSuis_Analysis_Colab.ipynb)

**For computationally intensive analyses:** Google Colab Pro is recommended for large datasets, providing:
- High-RAM runtime (up to 52GB)
- Priority GPU access (T4, P100, V100)
- Extended session times
- Background execution

All notebooks work with both free and Pro versions of Google Colab.

### Option 2: Local Installation
```bash
git clone https://github.com/MK-vet/MKrep.git
cd MKrep
pip install -r requirements.txt
python src/cluster_mic_amr_virulence.py
```

### Option 3: Docker Container (Universal Deployment)
**NEW!** Run MKrep in any environment with Docker:
```bash
# Build the image
docker build -t mkrep:latest .

# Run cluster analysis
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
    mkrep:latest mkrep-cluster --data-dir /data --output /output
```

Or use Docker Compose:
```bash
docker-compose up mkrep-cluster
```

See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for complete guide including:
- Running in Google Colab with Docker
- All analysis types
- Advanced configurations

### Option 4: Python Package (CLI)
```bash
pip install mkrep  # When published
mkrep-cluster --data-dir ./data --output ./results
```

### Option 5: Standalone Scripts (Traditional)
```bash
git clone https://github.com/MK-vet/MKrep.git
cd MKrep
pip install -r requirements.txt
python src/cluster_mic_amr_virulence.py
```

## Analysis Modules

### 1. StrepSuis-AMRPat: Automated Detection of Antimicrobial Resistance Patterns
**Script:** `src/mdr_analysis.py`

Advanced multidrug resistance pattern detection:
- Bootstrap resampling for robust prevalence estimation
- Co-occurrence analysis for phenotypes and resistance genes
- Association rule mining for resistance patterns
- Hybrid co-resistance network construction and visualization

### 2. StrepSuis-AMRVirKM: K-Modes Clustering of Antimicrobial Resistance and Virulence Profiles
**Script:** `src/cluster_mic_amr_virulence.py`

Comprehensive clustering analysis for resistance and virulence:
- K-Modes clustering with automatic silhouette optimization
- Multiple Correspondence Analysis (MCA) for dimensionality reduction
- Feature importance ranking and association rule discovery
- Bootstrap confidence intervals for robust statistical inference

### 3. StrepSuis-PhyloTrait: Integrated Phylogenetic and Binary Trait Analysis
**Script:** `src/phylogenetic_clustering.py`

Complete phylogenetic and binary trait analysis:
- Tree-aware clustering with evolutionary metrics
- Faith's Phylogenetic Diversity and pairwise distance calculations
- Binary trait analysis for AMR and virulence factors
- Interactive HTML reports with DataTables and Plotly visualizations

### 4. StrepSuis-GenPhenNet: Network-Based Integration of Genome–Phenome Data
**Script:** `src/network_analysis.py`

Statistical network analysis for genomic-phenotypic associations:
- Chi-square and Fisher exact tests with FDR correction
- Information theory metrics (entropy, mutual information, Cramér's V)
- Mutually exclusive pattern detection algorithms
- 3D network visualization with community detection

### 5. StrepSuis-Analyzer: General-Purpose Data Analysis Tool
**Script:** `StrepSuisPhyloCluster_2025_08_11.py` | **Module:** `separated_repos/strepsuis-analyzer/`

**A flexible tool for analyzing YOUR genomic data** - unlike the four specialized modules above:
- **User-focused design**: Upload and analyze your own binary trait datasets
- **General-purpose**: Not limited to specific workflows - exploratory data analysis
- **Easy to use**: Google Colab with drag-and-drop upload or simple command-line
- **Flexible analysis**: Automatic pattern discovery in your custom datasets
- **Comprehensive outputs**: Interactive HTML reports and Excel workbooks
- **No programming required**: Designed for researchers without coding expertise

> 💡 **Use this tool when**: You have your own genomic data (AMR, virulence, etc.) and want to explore patterns, clusters, and associations without predefined analysis workflows.

## ✨ NEW: Multiple Usage Options

### 📊 Comprehensive Reports (Standardized)
All scripts generate **professional, consistent reports** with:
- ✅ **Interactive HTML**: Bootstrap 5 styling, DataTables with export, interpretation sections
- ✅ **Excel Workbooks**: Multi-sheet with metadata, methodology, and chart index
- ✅ **High-quality PNG charts**: 150 DPI minimum, publication-ready
- ✅ **Consistent styling**: Unified appearance and structure across all tools
- ✅ **Interpretation included**: Every report explains what results mean
- ✅ **Full reproducibility**: Fixed seeds, documented parameters, complete provenance

### 🎯 Multiple Deployment Options

1. **📓 Google Colab Notebooks**: Run in the cloud without installation
   - See [colab_notebooks/](colab_notebooks/) directory
   - One-click deployment with file upload/download
   - Free GPU access for faster processing

2. **📦 Python Package with CLI**: Install as a package
   - See [python_package/](python_package/) directory
   - Full command-line interface for all analyses
   - Python API for programmatic access

3. **💻 Standalone Scripts**: Traditional execution
   - Direct Python script execution
   - Maximum flexibility and customization

### 🧪 Module Verification and Testing

**Comprehensive test suite with 180+ tests** ensures all modules work correctly:

#### Test Coverage
- **Mathematical validation tests** (24 tests): Entropy bounds, mutual information symmetry, phi coefficient and Cramér's V properties
- **CLI integration tests** (20 tests): Syntax validation, argument parsing, configuration loading
- **Docker smoke tests** (24 tests): Dockerfile and docker-compose.yml structure verification
- **Module-specific tests**: Statistical routines, clustering, network analysis, phylogenetic metrics

```bash
# Run all tests
python -m pytest

# Verify all modules are functional
python verify_all_modules.py

# Run all analyses with unified interface
python run_all_analyses.py --all

# Run specific analysis module
python run_all_analyses.py --module cluster
python run_all_analyses.py --module mdr
python run_all_analyses.py --module network
python run_all_analyses.py --module phylo
python run_all_analyses.py --module strepsuis

# List all available modules
python run_all_analyses.py --list
```

Features:
- Automated dependency checking
- Data file validation
- Syntax verification for all scripts
- Mathematical validation of statistical routines
- Comprehensive result generation
- JSON report of verification status

See [APPLICATION_VARIANTS_GUIDE.md](APPLICATION_VARIANTS_GUIDE.md) for complete details on all modules.

### 🔧 GitHub Actions - Run Tools from GitHub

All tools can be tested and run directly from GitHub using automated workflows:

- **CI - All Tools**: Continuous integration testing for all deployment options
  - Tests Python scripts, CLI package, and notebooks
  - Runs on Python 3.8-3.12 across multiple operating systems
  - Automatically validates all tools on every push
  
- **Deployment Tests**: Comprehensive deployment verification
  - Verifies standalone script execution
  - Tests CLI package installation and commands
  - Checks Colab notebook compatibility
  
- **Version Info**: Collects and displays version information
  - Python environment details
  - All package versions
  - Available commands and scripts
  
- **Quick Start Demo**: Interactive demonstration (manual trigger)
  - Choose specific tools to demonstrate
  - See examples of all deployment options
  - Can be triggered from GitHub Actions tab

To view workflow status and trigger demos:
1. Go to the [Actions tab](https://github.com/MK-vet/MKrep/actions)
2. Select a workflow to view results
3. For Quick Start Demo, click "Run workflow" to see tools in action

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
- `jupyter` - For notebook execution
- GPU support - For accelerated processing (Google Colab)

## Documentation

**Core Guides:**
- **[README.md](README.md)** - Start here! Overview and quick start
- **[QUICK_START.md](QUICK_START.md)** - Get started in 5 minutes
- **[USER_GUIDE.md](USER_GUIDE.md)** - Complete user guide with step-by-step instructions
- **[INTERPRETATION_GUIDE.md](INTERPRETATION_GUIDE.md)** - How to interpret analysis results
- **[INSTALLATION.md](INSTALLATION.md)** - Detailed installation instructions

**Deployment Guides:**
- **[DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)** - Docker deployment guide
- **[GITHUB_ACTIONS.md](GITHUB_ACTIONS.md)** - CI/CD and GitHub Actions usage

**Reference:**
- **[BINARY_DATA_GUIDE.md](BINARY_DATA_GUIDE.md)** - Binary data handling (crucial for data format)
- **[FEATURES.md](FEATURES.md)** - Complete feature list
- **[EXAMPLE_RESULTS.md](EXAMPLE_RESULTS.md)** - Example outputs and verification status

**Specialized Guides:**
- **[colab_notebooks/README.md](colab_notebooks/README.md)** - Google Colab usage
- **[python_package/README.md](python_package/README.md)** - Package documentation

*Note: Historical implementation summaries are archived in `docs/archive/`*

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
python src/cluster_mic_amr_virulence.py
python src/mdr_analysis.py
python src/network_analysis.py
python src/phylogenetic_clustering.py
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

## Features by Module

| Feature | AMRPat | AMRVirKM | PhyloTrait | GenPhenNet |
|---------|--------|----------|------------|------------|
| Phylogenetic clustering | - | - | ✓ | - |
| Network analysis | ✓ | - | - | ✓ |
| K-Modes clustering | - | ✓ | - | - |
| Chi-square tests | ✓ | ✓ | ✓ | ✓ |
| Bootstrap CIs | ✓ | ✓ | ✓ | - |
| Association rules | ✓ | ✓ | ✓ | - |
| MCA | - | ✓ | ✓ | - |
| Excel reports | ✓ | ✓ | ✓ | ✓ |
| PNG charts | ✓ | ✓ | ✓ | ✓ |

## Statistical Methods

- **Chi-square and Fisher exact tests** with FDR correction
- **Bootstrap resampling** for confidence intervals
- **Multiple Correspondence Analysis (MCA)** for dimensionality reduction
- **Random Forest** for feature importance
- **Association rule mining** (Apriori algorithm)
- **Network community detection** (Louvain algorithm)
- **Phylogenetic diversity metrics** (Faith's PD, UniFrac)
- **Clustering metrics** (Silhouette, Calinski-Harabasz, Davies-Bouldin)
- **Information theory metrics** (entropy, mutual information, Cramér's V)

### Mathematical Validation

All statistical routines are validated through automated tests that verify:
- **Entropy bounds**: Non-negativity and upper bounds (H ≤ log₂(n))
- **Mutual information symmetry**: MI(X,Y) = MI(Y,X)
- **Cramér's V properties**: Range [0,1] and perfect association detection
- **Phi coefficient**: Consistency with chi-square statistics
- **Bootstrap stability**: Confidence interval convergence

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

If you use StrepSuis_Suite in your research, please cite:

```bibtex
@software{strepsuis_suite2025,
  title = {StrepSuis\_Suite: Comprehensive Bioinformatics Analysis Suite for Streptococcus suis Genomics},
  author = {MK-vet},
  year = {2025},
  url = {https://github.com/MK-vet/MKrep},
  version = {2.0.0}
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

### 2025-01-16 - Version 1.2.0 🎉 **NEW FEATURES**
- ✨ **Interactive Colab Notebook** - No coding required!
  - Widget-based interface with buttons, dropdowns, and sliders
  - Upload files, select analysis, configure parameters, click run
  - Automatic result packaging and download
  - Perfect for non-programmers and quick analysis
- 🐳 **Docker Deployment** - Run anywhere with containers
  - Complete Dockerfile for containerized deployment
  - Docker Compose for easy multi-analysis workflows
  - Works in Google Colab, local machines, cloud platforms
  - Reproducible environments for research
- 📚 **Enhanced Documentation**
  - Complete Docker deployment guide (DOCKER_DEPLOYMENT.md)
  - Interactive notebook guide (INTERACTIVE_NOTEBOOK_GUIDE.md)
  - Consolidated quick start guide (QUICK_START.md)
  - Validation script to verify deployment readiness
- 🔄 **Google Colab Updates**
  - All existing notebooks verified and validated
  - Better file handling and output management
  - Improved instructions for beginners

### 2025-01-15 - Version 1.1.0 🎉
- ✨ **Standardized report templates** across all analysis tools
- ✨ **Comprehensive interpretation sections** in all reports
- ✨ **Complete user guide** (USER_GUIDE.md) with step-by-step instructions
- ✨ **Results interpretation guide** (INTERPRETATION_GUIDE.md) for understanding outputs
- ✨ **Standardization guide** (STANDARDIZATION_GUIDE.md) for developers
- ✨ **Script template** (analysis_script_template.py) for consistent development
- 📝 **All documentation in English** with clear explanations
- 🎨 **Unified Bootstrap 5 styling** with consistent color scheme
- 🔁 **Full reproducibility** with documented parameters and fixed seeds
- ✅ **One HTML + One Excel per tool** - consolidated report generation

### 2025-01-07 - Version 1.0.0 🎉
- ✨ **Added Google Colab notebooks** for cloud-based analysis
- ✨ **Created Python package** with full CLI support
- ✨ **Comprehensive installation guide** (INSTALLATION.md)
- ✨ **Multiple deployment options** (Colab, CLI, Scripts)
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