# MKrep

Comprehensive bioinformatics analysis pipeline for microbial genomics, focusing on antimicrobial resistance (AMR), virulence factors, and phylogenetic relationships.

## Overview

This repository contains Python scripts for analyzing bacterial genomic data with a focus on:
- Phylogenetic clustering and tree-based analysis
- Antimicrobial resistance patterns and multi-drug resistance (MDR)
- Network analysis of gene-phenotype associations
- Binary trait profiling for virulence and resistance genes
- Clustering analysis with multiple statistical methods

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

## NEW: Excel Report Generation ✨

All scripts now generate comprehensive Excel reports (.xlsx) in addition to HTML reports!

### Features:
- ✅ **Multi-sheet Excel workbooks** with organized data
- ✅ **High-quality PNG charts** saved separately
- ✅ **Detailed methodology** documentation in each report
- ✅ **Consistent structure** across all analysis types
- ✅ **Auto-formatted tables** with proper rounding and column widths

### Report Structure:
1. **Metadata Sheet**: Analysis configuration and parameters
2. **Methodology Sheet**: Detailed descriptions of all methods
3. **Data Sheets**: Analysis results (varies by script)
4. **Chart Index Sheet**: List of all generated PNG files

See [EXCEL_REPORTS_README.md](EXCEL_REPORTS_README.md) for detailed documentation.

## Requirements

### Core Dependencies:
```bash
pip install pandas numpy scipy matplotlib seaborn plotly
pip install scikit-learn biopython umap-learn networkx
pip install statsmodels mlxtend prince jinja2
pip install openpyxl kaleido pillow  # For Excel reports
```

### Script-Specific:
- `kmodes` - For K-Modes clustering
- `optuna` - For hyperparameter optimization
- `community` (python-louvain) - For network community detection
- `ydata-profiling` - For data profiling (optional)

## Usage

### Basic Execution:
```python
python <script_name>.py
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

If you use these scripts in your research, please cite:

```
[Your citation information here]
```

## License

[Your license information here]

## Contact

For questions or support:
- GitHub Issues: [github.com/MK-vet/MKrep/issues](https://github.com/MK-vet/MKrep/issues)
- Email: [Your contact email]

## Changelog

### 2025-01-07
- ✨ Added comprehensive Excel report generation to all scripts
- ✨ Implemented PNG chart export for all visualizations
- ✨ Created shared utility module (`excel_report_utils.py`)
- 📝 Added detailed documentation for Excel reports
- 🎨 Standardized report structure across all analysis types

### Previous versions
- Initial implementations of analysis scripts
- HTML report generation with interactive features