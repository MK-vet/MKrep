# Cluster Analysis Pipeline - Comprehensive Guide

## Overview
The Cluster_MIC_AMR_Viruelnce.py script performs comprehensive clustering analysis on bacterial strain data, integrating Minimum Inhibitory Concentration (MIC), Antimicrobial Resistance (AMR) genes, and Virulence factors.

## Features

### Analysis Components
1. **K-Modes Clustering**
   - Automatic optimal cluster determination using silhouette score
   - Sqrt(N) heuristic for maximum cluster count
   - Huang initialization for stable results

2. **Statistical Tests**
   - Chi-square tests with FDR correction (Benjamini-Hochberg)
   - Fisher's exact test for small samples
   - Pairwise post-hoc tests with multiple testing correction
   - Log-odds ratio analysis with bootstrap confidence intervals

3. **Feature Analysis**
   - Logistic regression with L1 penalty for feature selection
   - Random Forest feature importance
   - Shared and unique feature identification
   - Association rule mining (support=0.3, confidence=0.7)

4. **Dimensionality Reduction**
   - Multiple Correspondence Analysis (MCA)
   - 2D scatter plots for cluster visualization
   - Phi correlation heatmaps

5. **Validation Metrics**
   - Calinski-Harabasz score
   - Davies-Bouldin score
   - Silhouette score

## Requirements

### Input Data Files
The script expects three CSV files with binary (0/1) data:
- `MIC.csv` - Minimum Inhibitory Concentration data
- `AMR_genes.csv` - Antimicrobial Resistance genes
- `Virulence.csv` - Virulence factors

Each file must have:
- First column: `Strain_ID`
- Subsequent columns: Binary features (0 = absence, 1 = presence)

### Python Dependencies
```bash
pip install kmodes prince ydata-profiling joblib numba tqdm psutil statsmodels jinja2 plotly openpyxl kaleido pillow
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Execution
```bash
python Cluster_MIC_AMR_Viruelnce.py
```

The script will:
1. Load and validate input data
2. Perform clustering on each category (MIC, AMR, Virulence)
3. Generate statistical analyses
4. Create comprehensive reports

### Output Structure

#### Output Directory: `clustering_analysis_results6/`

##### CSV Files (57 files total)
For each category (MIC, AMR, Virulence):
- `{category}_cluster_statistics.csv` - Cluster sizes and proportions with bootstrap CIs
- `{category}_characteristic_patterns.csv` - Defining features per cluster
- `{category}_chi2_global.csv` - Global chi-square test results
- `{category}_chi2_per_cluster.csv` - Per-cluster chi-square tests
- `{category}_log_odds_global.csv` - Global log-odds ratios
- `{category}_log_odds_per_cluster.csv` - Per-cluster log-odds with bootstrap CIs
- `{category}_shared_features.csv` - Features present in multiple clusters
- `{category}_unique_features.csv` - Cluster-specific features
- `{category}_logistic_regression_coefficients.csv` - L1 regression results
- `{category}_association_rules.csv` - Association rules found
- `{category}_cluster_correlation.csv` - Phi correlations
- `{category}_cluster_importance.csv` - Random Forest feature importance
- `{category}_validation_scores.csv` - Clustering validation metrics
- `{category}_fdr_post_hoc_results.csv` - Pairwise post-hoc tests
- `{category}_MCA_results.csv` - MCA coordinates
- `MCA_{category}_summary.csv` - MCA eigenvalues and variance explained

Integrated results:
- `integrated_clustering_results.csv` - Cluster assignments for all strains
- `combined_cluster_statistics_with_ci.csv` - Joint cluster combinations

##### HTML Report
- `comprehensive_cluster_analysis_report.html`
  - Interactive tables with sorting, filtering, and export
  - MCA scatter plots
  - Correlation heatmaps
  - Complete methodology section
  - All analysis results in one file

##### Excel Report
- `Cluster_Analysis_Report_YYYYMMDD_HHMMSS.xlsx`
  - Metadata sheet with analysis information
  - Methodology sheet with detailed descriptions
  - 56+ data sheets with all results
  - Integrated cluster assignments
  - Chart index (if PNG charts are generated)

## Methodology

### Clustering Algorithm
- **K-Modes** clustering for categorical data
- Cluster count: 2 to sqrt(N) tested
- Selection: Maximum silhouette score
- 1-based cluster labels

### Statistical Corrections
- **FDR correction**: Benjamini-Hochberg at α=0.05
- **Pseudo-counts**: 0.5 added to avoid zero/infinite ratios
- **Bootstrap CIs**: 200-500 resamples with stratified sampling

### Association Rules
- **Minimum support**: 0.3 (30% of cluster)
- **Minimum confidence**: 0.7 (70% confidence)
- Pairwise rules only (not exhaustive itemset mining)

## Interpreting Results

### Cluster Statistics
- **Count**: Number of strains in cluster
- **Percentage**: Proportion of total strains
- **CI_low/CI_high**: Bootstrap confidence intervals (95%)

### Characteristic Patterns
Format: `Feature (count/total, percentage%, CI:low-high%)`
- Shows defining features for each cluster
- Only features with >50% prevalence shown

### Log-Odds Ratios
- **Positive values**: Feature enriched in cluster
- **Negative values**: Feature depleted in cluster
- **CI crossing zero**: Not significantly different

### Chi-Square Tests
- **FDR_Rejected = True**: Significant after correction
- **P_Value**: Unadjusted p-value
- **Adjusted_P**: FDR-corrected p-value

### MCA Plots
- **2D scatter**: Clusters should form distinct groups
- **Components**: Axes show main sources of variation
- **Eigenvalues**: Variance explained by each component

## Troubleshooting

### Common Issues

1. **File not found errors**
   - Ensure MIC.csv, AMR_genes.csv, and Virulence.csv exist in current directory
   - Check file names match exactly (case-sensitive)

2. **Memory errors**
   - Script monitors memory usage
   - Reduce dataset size if needed
   - Close other applications

3. **Convergence warnings**
   - K-Modes may warn about convergence
   - Script includes retry logic (3 attempts)
   - Results are still valid

4. **Missing dependencies**
   - Install all required packages
   - Use `pip install -r requirements.txt`

### Performance Notes
- Small dataset (~100 strains): 1-3 minutes
- Medium dataset (~1000 strains): 10-30 minutes
- Large dataset (~10000 strains): May take hours

The bootstrap analyses (CIs for log-odds, logistic regression) are the most time-consuming steps.

## Output Validation

After running, verify:
1. ✅ Output folder created: `clustering_analysis_results6/`
2. ✅ 57 CSV files generated
3. ✅ HTML report generated (~45MB)
4. ✅ Excel report generated with 56+ sheets
5. ✅ Console shows completion message

## Citation

If you use this analysis pipeline, please cite the MKrep repository and relevant methods:
- K-Modes clustering: Huang (1998)
- MCA: Multiple Correspondence Analysis
- FDR correction: Benjamini & Hochberg (1995)

## Support

For issues or questions:
1. Check this README
2. Review the HTML report methodology section
3. Open an issue on the GitHub repository

## Version History

- **v1.0**: Initial implementation with comprehensive reporting
- Colab-compatible code removed for standalone execution
- Fixed Virulence.csv file reference
