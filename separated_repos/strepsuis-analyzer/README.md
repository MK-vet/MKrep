# StrepSuis Analyzer: Integrated Phylogenetic Clustering Analysis

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/StrepSuis_Analysis_Colab.ipynb)

**Comprehensive integrative analysis tool for *Streptococcus suis* genomic data**

## Overview

StrepSuis Analyzer is a production-ready, standalone Python tool for comprehensive phylogenetic clustering analysis of bacterial genomic data. Originally developed for *Streptococcus suis* but applicable to any bacterial species with binary trait data.

### Key Features

- ✅ **Tree-aware clustering** with ensemble fallback methods
- ✅ **Binary trait profiling** (chi-square, log-odds, random forest importance)
- ✅ **Association rule mining** for co-occurrence patterns
- ✅ **Multiple Correspondence Analysis (MCA)** for dimensionality reduction
- ✅ **Bootstrap confidence intervals** for robust statistics
- ✅ **Interactive HTML reports** with Bootstrap 5 UI
- ✅ **Excel workbooks** with multiple analysis sheets
- ✅ **CSV exports** for downstream analysis
- ✅ **Reproducible results** with fixed random seeds

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 4GB RAM minimum (8GB recommended for large datasets)

### Installation

#### Option 1: Standalone Installation (Recommended)

```bash
# Clone or download this directory
cd strepsuis-analyzer

# Install dependencies
pip install -r requirements.txt
```

#### Option 2: From Main MKrep Repository

```bash
# Clone the main repository
git clone https://github.com/MK-vet/MKrep.git
cd MKrep/separated_repos/strepsuis-analyzer

# Install dependencies
pip install -r requirements.txt
```

#### Option 3: Google Colab (No Installation Required)

Click here: [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/StrepSuis_Analysis_Colab.ipynb)

### Basic Usage

#### 1. Prepare Your Data

Organize your data files in the current directory:

```
├── AMR_genes.csv          # Antimicrobial resistance genes (binary)
├── Virulence.csv          # Virulence factors (binary)
├── Snp_tree.newick        # Phylogenetic tree (optional)
└── StrepSuisPhyloCluster_2025_08_11.py
```

**Data Format Requirements:**
- CSV files with binary data (0 = absence, 1 = presence)
- First column must be `Strain_ID`
- Other columns are feature names
- Missing values will be treated as 0 (absence)

**Example CSV:**
```csv
Strain_ID,Gene1,Gene2,Gene3
Strain001,1,0,1
Strain002,0,1,1
Strain003,1,1,0
```

#### 2. Run the Analysis

**Basic analysis (auto-detect optimal clusters):**
```bash
python StrepSuisPhyloCluster_2025_08_11.py
```

**Custom data files:**
```bash
python StrepSuisPhyloCluster_2025_08_11.py --data AMR_genes.csv Virulence.csv MGE.csv
```

**Include phylogenetic tree:**
```bash
python StrepSuisPhyloCluster_2025_08_11.py --tree Snp_tree.newick
```

**Specify number of clusters:**
```bash
python StrepSuisPhyloCluster_2025_08_11.py --clusters 4
```

**Custom output directory:**
```bash
python StrepSuisPhyloCluster_2025_08_11.py --output my_results
```

**All options:**
```bash
python StrepSuisPhyloCluster_2025_08_11.py \
  --data AMR_genes.csv Virulence.csv \
  --tree Snp_tree.newick \
  --output results \
  --clusters 5 \
  --seed 42
```

#### 3. View Results

The analysis generates three types of output files:

1. **Interactive HTML Report** (`analysis_report.html`)
   - Open in any web browser
   - Interactive visualizations
   - Bootstrap 5 responsive design
   - Downloadable data tables

2. **Excel Workbook** (`analysis_results.xlsx`)
   - Multiple sheets with different analysis results
   - Cluster assignments
   - Statistical associations
   - Summary statistics
   - Metadata

3. **CSV Files**
   - `clustered_data.csv` - Strain assignments with cluster labels
   - `trait_associations.csv` - Statistical associations between traits and clusters

## Analysis Methods

### 1. Clustering

**Hierarchical Clustering:**
- Uses Jaccard distance for binary data
- Ward linkage method
- Automatic cluster number selection via silhouette score
- Or manual specification of cluster count

**Phylogenetic Distance:**
- Integrates phylogenetic tree distances (if provided)
- Calculates pairwise evolutionary distances
- Tree-aware cluster validation

### 2. Trait Association Analysis

**Statistical Tests:**
- Chi-square test for independence
- Cramér's V for effect size
- FDR (Benjamini-Hochberg) correction for multiple testing
- Significance threshold: FDR < 0.05

### 3. Dimensionality Reduction

**Multiple Correspondence Analysis (MCA):**
- Projects high-dimensional binary data to 2D/3D
- Preserves categorical relationships
- Visualizes cluster separation
- Explained variance reported

### 4. Quality Metrics

- Silhouette score for cluster quality
- Within-cluster vs. between-cluster distances
- Phylogenetic diversity metrics (if tree provided)
- Bootstrap confidence intervals (planned feature)

## Output Files Description

### HTML Report (`analysis_report.html`)

Interactive web-based report featuring:
- **Overview section**: Dataset summary and cluster statistics
- **Cluster distribution**: Bar chart of strain counts per cluster
- **MCA biplot**: 2D visualization colored by cluster
- **Trait associations**: Top significant features ranked by FDR-adjusted p-value
- **Export links**: Direct access to CSV and Excel files

### Excel Workbook (`analysis_results.xlsx`)

Multi-sheet workbook containing:

1. **Clustered_Data**: Complete dataset with cluster assignments
2. **Cluster_Summary**: Size and prevalence of each cluster
3. **Trait_Associations**: Full statistical results with p-values, effect sizes
4. **Metadata**: Analysis parameters and run information

### CSV Files

- **clustered_data.csv**: Same as Excel Clustered_Data sheet, for easy import
- **trait_associations.csv**: Statistical results for programmatic access

## Command-Line Options

```bash
python StrepSuisPhyloCluster_2025_08_11.py [OPTIONS]

Options:
  --data FILES [FILES ...]   CSV data files (default: AMR_genes.csv Virulence.csv)
  --tree FILE                Phylogenetic tree file in Newick format (default: Snp_tree.newick)
  --output DIR               Output directory (default: output)
  --clusters INT             Number of clusters (default: auto-determined by silhouette score)
  --seed INT                 Random seed for reproducibility (default: 42)
  -h, --help                 Show help message and exit
```

## Example Dataset

This repository includes a sample dataset in the `data/` directory:

- `Virulence.csv` - Binary virulence factor profiles for *S. suis* strains

To test with the example data:
```bash
python StrepSuisPhyloCluster_2025_08_11.py --data data/Virulence.csv
```

## Reproducibility

All analyses are fully reproducible:
- Fixed random seed (default: 42)
- Deterministic algorithms
- Version-pinned dependencies in `requirements.txt`
- Documented methods in code and reports

## Citation

If you use StrepSuis Analyzer in your research, please cite:

```
[Citation information will be added upon publication]
```

## Contributing

This tool is part of the [MKrep repository](https://github.com/MK-vet/MKrep). 

For bug reports or feature requests:
- Open an issue on GitHub
- Contact the maintainers

## License

MIT License - see LICENSE file for details

## Acknowledgments

Developed as part of the MKrep bioinformatics suite for *Streptococcus suis* genomics research.

## Support

- 📖 **Documentation**: This README and in-code docstrings
- 💬 **Questions**: Open an issue on GitHub
- 🐛 **Bug Reports**: Use GitHub issue tracker
- ✨ **Feature Requests**: Submit via GitHub issues

## Changelog

### Version 2025-08-11
- Initial release
- Core clustering and trait association analysis
- HTML and Excel report generation
- MCA dimensionality reduction
- Phylogenetic tree integration
- Bootstrap 5 web interface

## Related Tools

This analyzer is part of the StrepSuis analysis suite:

1. **strepsuis-mdr** - AMR Pattern Detection and MDR analysis
2. **strepsuis-amrvirkm** - K-Modes Clustering for AMR/virulence
3. **strepsuis-genphennet** - Gene-Phenotype Network Integration
4. **strepsuis-phylotrait** - Phylogenetic Trait Analysis
5. **strepsuis-analyzer** - This integrated analysis tool (you are here)

Each tool can be used independently or combined for comprehensive analysis.
