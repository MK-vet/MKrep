# Phylogenetic Clustering Analysis Pipeline

Comprehensive phylogenetic clustering and binary trait analysis pipeline for microbial genomics data.

## Overview

This pipeline performs tree-aware phylogenetic clustering with comprehensive trait analysis including:
- Phylogenetic tree-based clustering with monophyly enforcement
- Evolutionary metrics (Faith's PD, beta diversity, evolution rates)
- Binary trait analysis (MIC, AMR genes, virulence factors)
- Statistical testing with FDR correction
- Association rule mining
- Multiple Correspondence Analysis (MCA)
- Comprehensive HTML and Excel reports

## Features

- **Tree-Aware Clustering**: Uses TreeCluster and Phydelity-inspired methods that respect tree structure
- **Automatic Cluster Selection**: Silhouette analysis determines optimal number of clusters
- **Monophyly Enforcement**: Ensures clusters are monophyletic
- **Comprehensive Logging**: Detailed execution logs with progress tracking
- **Memory Monitoring**: Tracks memory usage throughout analysis
- **Interactive Reports**: HTML reports with DataTables and Plotly visualizations
- **Excel Workbooks**: Multi-sheet Excel reports with all analysis results

## Requirements

### Input Data Files

The pipeline expects the following input files:

1. **Phylogenetic Tree** (Newick format)
   - Example: `Snp_tree.newick`
   - Contains phylogenetic relationships among strains

2. **MIC Data** (CSV format)
   - Example: `MIC.csv`
   - First column: `Strain_ID`
   - Subsequent columns: Binary (0/1) MIC resistance data

3. **AMR Genes** (CSV format)
   - Example: `AMR_genes.csv`
   - First column: `Strain_ID`
   - Subsequent columns: Binary (0/1) antimicrobial resistance gene presence

4. **Virulence Factors** (CSV format)
   - Example: `Virulence.csv`
   - First column: `Strain_ID`
   - Subsequent columns: Binary (0/1) virulence factor presence

### Python Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install numpy pandas scipy matplotlib seaborn plotly
pip install scikit-learn umap-learn biopython networkx
pip install statsmodels mlxtend prince jinja2 weasyprint
pip install openpyxl xlsxwriter kaleido pillow
pip install tqdm joblib numba psutil kmodes optuna
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MK-vet/MKrep.git
cd MKrep
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Execution

Run with default settings:

```bash
python run_phylogenetic_analysis.py
```

### Custom Configuration

Run with custom settings:

```bash
# Custom output folder
python run_phylogenetic_analysis.py --output my_results

# Custom tree file
python run_phylogenetic_analysis.py --tree my_tree.newick

# Custom bootstrap iterations
python run_phylogenetic_analysis.py --bootstrap 1000

# All custom settings
python run_phylogenetic_analysis.py \
    --tree my_tree.newick \
    --output my_results \
    --bootstrap 1000 \
    --fdr-alpha 0.01 \
    --max-clusters 15
```

### Command-Line Options

**Input Files:**
- `--tree FILE`: Phylogenetic tree file (default: Snp_tree.newick)
- `--mic FILE`: MIC data file (default: MIC.csv)
- `--amr FILE`: AMR genes file (default: AMR_genes.csv)
- `--virulence FILE`: Virulence genes file (default: Virulence.csv)

**Output Settings:**
- `--output FOLDER`: Output folder name (default: phylogenetic_clustering_results)
- `--base-dir DIR`: Base directory for input/output (default: .)

**UMAP Parameters:**
- `--umap-components N`: Number of UMAP components (default: 2)
- `--umap-neighbors N`: Number of UMAP neighbors (default: 15)
- `--umap-min-dist F`: UMAP minimum distance (default: 0.1)

**Clustering Parameters:**
- `--outlier-contamination F`: Outlier contamination threshold (default: 0.05)
- `--outlier-estimators N`: Number of outlier estimators (default: 200)
- `--min-clusters N`: Minimum number of clusters (default: 2)
- `--max-clusters N`: Maximum number of clusters (default: 10)

**Statistical Parameters:**
- `--bootstrap N`: Number of bootstrap iterations (default: 500)
- `--fdr-alpha F`: FDR alpha level (default: 0.05)

**Advanced Options:**
- `--parallel-tree`: Enable parallel processing for tree calculations
- `--parallel-jobs N`: Number of parallel jobs (default: 1)
- `--skip-html`: Skip HTML report generation
- `--skip-excel`: Skip Excel report generation

### Direct Script Execution

You can also run the analysis directly:

```bash
python Phylgenetic_clustering_2025_03_21.py
```

## Output Files

The pipeline generates multiple output files in the specified output folder:

### Main Outputs

1. **phylogenetic_analysis.log**
   - Comprehensive execution log with timestamps
   - Progress tracking and memory usage
   - Error messages and warnings

2. **phylogenetic_clusters.csv**
   - Cluster assignments for all strains
   - Columns: Strain_ID, Cluster

3. **phylogenetic_report.html**
   - Interactive HTML report with DataTables and Plotly
   - Phylogenetic tree visualization
   - UMAP embeddings
   - Statistical analysis results

4. **Phylogenetic_Clustering_Report_*.xlsx**
   - Multi-sheet Excel workbook
   - All analysis results in separate sheets
   - Metadata and methodology sheets
   - PNG charts directory

### Analysis Results (CSV files)

- `evolutionary_cluster_analysis.csv`: Phylogenetic diversity metrics
- `phylogenetic_beta_diversity.csv`: Between-cluster diversity
- `evolution_rates.csv`: Evolution rates per cluster
- `phylogenetic_signal.csv`: Phylogenetic signal statistics
- `cluster_distribution.csv`: Cluster size distribution
- `chi2_results_*.csv`: Chi-square test results
- `log_odds_*.csv`: Log-odds ratios for trait enrichment
- `feature_importance_*.csv`: Random Forest feature importance
- `association_rules_*.csv`: Frequent patterns and rules
- `mca_*.csv`: Multiple Correspondence Analysis results
- `shared_features_*.csv`: Shared and unique trait patterns
- `pairwise_tests_*.csv`: Pairwise FDR-corrected comparisons

### Visualizations (PNG files)

- `phylogenetic_tree_colored.png`: Tree with cluster colors
- `umap_clusters.png`: UMAP visualization
- `cluster_distribution.png`: Cluster size bar chart
- Various trait analysis plots

## Methodology

### Phylogenetic Clustering

1. **Distance Matrix Computation**: Pairwise patristic distances from phylogenetic tree
2. **UMAP Dimensionality Reduction**: Projects high-dimensional distances to 2D space
3. **Tree-Aware Clustering**: TreeCluster and custom methods that respect tree structure
4. **Cluster Optimization**: Silhouette analysis selects optimal number of clusters
5. **Monophyly Enforcement**: Ensures all clusters are monophyletic

### Evolutionary Metrics

- **Faith's Phylogenetic Diversity (PD)**: Quantifies evolutionary history
- **Pairwise Patristic Distances**: Measures evolutionary divergence
- **Beta Diversity**: Assesses cluster differentiation
- **Evolution Rates**: Cluster-specific evolutionary rates

### Statistical Analysis

- **Chi-square Tests**: Trait-cluster associations
- **FDR Correction**: Benjamini-Hochberg correction for multiple testing
- **Log-odds Ratios**: Effect size estimation with bootstrap confidence intervals
- **Random Forest**: Feature importance for discriminative traits
- **Pairwise Comparisons**: FDR-adjusted post-hoc tests

### Association Analysis

- **Apriori Algorithm**: Frequent pattern mining
- **Association Rules**: High support and confidence trait combinations
- **MCA**: Dimensionality reduction for categorical data

## Execution Summary

The pipeline provides comprehensive execution summaries including:

- Total execution time
- Step-by-step timing breakdown
- Memory usage monitoring
- File generation counts
- Output directory location
- Log file location

Example summary:

```
================================================================================
  EXECUTION SUMMARY
================================================================================

Total Execution Time: 125.45 seconds (2.09 minutes)

Step-by-Step Timing:
  Step 1: Phylogenetic Clustering: 45.23s (36.0%)
  Step 2: Evolutionary Analysis: 32.15s (25.6%)
  Step 3: Binary Trait Analysis: 38.92s (31.0%)
  Step 4: MCA Analysis: 9.15s (7.3%)

Output Files Generated:
  - CSV files: 28
  - PNG images: 15
  - HTML files: 2

Output folder: phylogenetic_clustering_results
Log file: phylogenetic_clustering_results/phylogenetic_analysis.log
Memory Usage: 1245.67 MB
```

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **File Not Found Errors**
   - Ensure all input files exist in the base directory
   - Check file names match exactly (case-sensitive)
   - Use `--base-dir` to specify a different directory

3. **Memory Errors**
   - Pipeline monitors memory usage
   - Reduce dataset size if needed
   - Close other applications

4. **Clustering Failures**
   - Pipeline falls back to ensemble clustering if tree-aware methods fail
   - Check log file for detailed error messages

5. **TreeCluster Not Found**
   - TreeCluster is optional but recommended
   - Pipeline will use alternative methods if not available

## Performance Notes

- **Small datasets** (~50 strains): 1-3 minutes
- **Medium datasets** (~200 strains): 5-15 minutes
- **Large datasets** (~1000+ strains): May take 30+ minutes

Bootstrap analyses are the most time-consuming steps. Reduce `--bootstrap` iterations for faster execution.

## Citation

If you use this pipeline in your research, please cite:

- MKrep repository: https://github.com/MK-vet/MKrep
- TreeCluster: Yu et al. (2021)
- UMAP: McInnes et al. (2018)
- Relevant statistical methods used

## Support

For issues or questions:
1. Check this README
2. Review the execution log file
3. Open an issue on GitHub: https://github.com/MK-vet/MKrep/issues

## Author

MK-vet (with tree-aware clustering improvements)

## License

See repository LICENSE file.

## Version History

- **v1.0** (2025-03-21): Initial implementation with comprehensive reporting
  - Tree-aware clustering with monophyly enforcement
  - Comprehensive logging and progress tracking
  - HTML and Excel report generation
  - Command-line interface
