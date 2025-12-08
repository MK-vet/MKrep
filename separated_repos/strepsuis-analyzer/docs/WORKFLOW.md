# StrepSuis Analyzer End-to-End Workflow Guide

This document describes the complete end-to-end workflow for the StrepSuis Analyzer, including headless analysis execution, data processing pipelines, and output interpretation.

## Table of Contents
1. [Overview](#overview)
2. [Data Preparation](#data-preparation)
3. [Analysis Pipeline](#analysis-pipeline)
4. [Output Interpretation](#output-interpretation)
5. [Integration with Other Tools](#integration-with-other-tools)
6. [Troubleshooting](#troubleshooting)

## Overview

The StrepSuis Analyzer provides two modes of operation:
- **Interactive Mode**: Streamlit web interface for exploratory analysis
- **Headless Mode**: Command-line E2E analysis for batch processing and CI/CD

### Workflow Diagram

```
Input Data → Validation → Analysis → Outputs
                ↓           ↓
            Logs/QC    Reports/Viz
```

## Data Preparation

### Supported Data Types

| Type | Format | Description | Example Dimensions |
|------|--------|-------------|-------------------|
| AMR Genes | CSV (binary) | Gene presence/absence | 91 × 21 |
| MIC Values | CSV (numeric) | Minimum inhibitory concentrations | 91 × 13 |
| Virulence | CSV (binary) | Virulence factor presence/absence | 91 × 106 |
| MLST | CSV (categorical) | Multi-locus sequence types | 91 × 1 |
| Serotypes | CSV (categorical) | Serotype classifications | 91 × 1 |
| Phylogenetic Tree | Newick | Phylogenetic relationships | 91 taxa |

### Data Requirements

**CSV Files:**
- First column: Strain IDs (unique identifiers)
- Remaining columns: Features/variables
- No missing values in critical columns
- Binary data: 0/1 values only
- Numeric data: Real numbers
- Categorical data: String labels

**Newick Files:**
- Valid Newick format
- Taxa names matching strain IDs in CSV files
- Well-formed tree structure (balanced parentheses)

### Example Data Location

Example datasets are included in `data/`:
```bash
data/
├── AMR_genes.csv      # 91 strains × 21 genes
├── MIC.csv            # 91 strains × 13 antibiotics
├── Virulence.csv      # 91 strains × 106 factors
├── MLST.csv           # 91 strains with ST types
├── Serotype.csv       # 91 strains with serotypes
└── Snp_tree.newick    # Phylogenetic tree (91 taxa)
```

### Synthetic Data

Synthetic datasets for testing are generated in `data/synthetic/` using:
```bash
python scripts/generate_synthetic_data.py
```

## Analysis Pipeline

### 1. Interactive Analysis (Streamlit)

Launch the web interface:
```bash
# Using CLI
strepsuis-analyzer --launch

# Or directly
streamlit run src/strepsuis_analyzer/app.py

# Custom port
strepsuis-analyzer --launch --port 8502
```

Access at: http://localhost:8501

**Workflow:**
1. Upload data files or select example datasets
2. Validate data quality
3. Perform statistical analyses
4. Generate visualizations
5. Run clustering algorithms
6. Analyze phylogenetic relationships
7. Export reports

### 2. Headless E2E Analysis

For batch processing, automation, or CI/CD:

```bash
# Run on both example and synthetic datasets
strepsuis-analyzer-e2e --dataset both

# Run on specific dataset
strepsuis-analyzer-e2e --dataset example
strepsuis-analyzer-e2e --dataset synthetic

# Custom output directory
strepsuis-analyzer-e2e --dataset both --results-dir custom_output/

# Reproducible results
strepsuis-analyzer-e2e --dataset both --random-state 42
```

**E2E Pipeline Steps:**

1. **Data Loading**
   - Load CSV files (AMR, MIC, Virulence, MLST, Serotype)
   - Load phylogenetic tree (Newick)
   - Validate file formats and structure

2. **Validation**
   - Check DataFrame shape and types
   - Validate binary matrices (0/1 values)
   - Parse and validate Newick tree
   - Export validation report and summary

3. **Statistical Analysis**
   - Compute correlations (Pearson, Spearman, Kendall, Phi, Cramér's V)
   - Test normality (Shapiro-Wilk, Q-Q plots)
   - Hypothesis testing (t-test, Mann-Whitney U, ANOVA, Kruskal-Wallis)
   - Multiple testing correction (Bonferroni, Benjamini-Hochberg FDR)
   - Meta-analysis (fixed/random effects, heterogeneity testing)

4. **Visualizations**
   - Distribution plots (histograms, box plots, violin plots)
   - Relationship plots (scatter plots with regression)
   - Correlation heatmaps
   - Q-Q plots for normality assessment

5. **Clustering**
   - K-Means clustering (numeric data) with elbow plot
   - K-Modes clustering (binary/categorical data)
   - Hierarchical clustering with dendrogram
   - DBSCAN density-based clustering

6. **Phylogenetic Analysis**
   - Tree visualization
   - Robinson-Foulds distance (tree comparison)
   - Faith's Phylogenetic Diversity
   - Cophenetic correlation (tree quality)
   - Bipartition analysis

7. **ETL Operations**
   - Pivot table generation
   - Data aggregation (group-by operations)
   - Normalization (z-score, min-max scaling)
   - Dataset merging and joining

8. **Report Generation**
   - Multi-sheet Excel workbook
   - Self-contained HTML report
   - Metadata tracking (timestamp, version)

### 3. Programmatic Access (Python API)

```python
from strepsuis_analyzer import (
    DataValidator,
    StatisticalAnalyzer,
    PhylogeneticAnalyzer,
    Visualizer,
    ReportGenerator
)
import pandas as pd

# Load data
amr_data = pd.read_csv('data/AMR_genes.csv', index_col=0)
mic_data = pd.read_csv('data/MIC.csv', index_col=0)

# Validate
validator = DataValidator()
is_valid, errors, warnings = validator.validate_dataframe(amr_data)

# Statistical analysis
analyzer = StatisticalAnalyzer(random_state=42)
corr_matrix, p_values = analyzer.compute_correlation_matrix(
    mic_data, method='spearman'
)

# Clustering
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(amr_data)

# Visualization
viz = Visualizer()
fig = viz.create_heatmap(
    corr_matrix,
    title='MIC Correlations',
    cmap='coolwarm'
)
viz.save_figure(fig, 'correlation_heatmap.png')

# Report
report = ReportGenerator()
report.add_dataframe('AMR Data', amr_data)
report.add_dataframe('Correlation Matrix', corr_matrix)
report.export_to_excel('analysis_report.xlsx')
report.export_to_html('analysis_report.html')
```

## Output Interpretation

### Directory Structure

```
results/strepsuis-analyzer-YYYYMMDD-HHMM/
├── example/           # Results from example data
├── synthetic/         # Results from synthetic data
└── logs/             # Execution logs
```

Each dataset directory contains:
- `validation/` - Data quality checks
- `stats/` - Statistical analysis results
- `visualizations/` - Plots and figures
- `clustering/` - Cluster assignments and plots
- `phylogenetics/` - Tree analyses
- `etl/` - Transformed data
- `reports/` - Final reports (Excel, HTML)

### Key Outputs

**Validation Report** (`validation/validation_report.csv`):
- Dataset shape, data types
- Missing value counts
- Binary matrix validation
- Tree structure validation

**Correlation Matrix** (`stats/correlation_matrix.csv`):
- Pairwise correlations between variables
- Different methods: Pearson, Spearman, Kendall

**Hypothesis Tests** (`stats/hypothesis_tests.csv`):
- Test statistics and p-values
- Effect sizes
- Confidence intervals

**Cluster Labels** (`clustering/*_labels.csv`):
- Cluster assignments for each strain
- Cluster statistics

**Phylogenetic Metrics** (`phylogenetics/*.csv`):
- Tree distances and diversity metrics
- Quality assessments

**Final Reports** (`reports/`):
- `final_report.xlsx`: Multi-sheet workbook with all tables
- `final_report.html`: Interactive HTML report with visualizations

## Integration with Other Tools

### Docker Deployment

```bash
# Build image
docker-compose build

# Run interactive app
docker-compose up

# Access at http://localhost:8501
```

**Docker E2E Analysis:**
```bash
# Run E2E inside container
docker-compose run strepsuis-analyzer \
    strepsuis-analyzer-e2e --dataset both

# Results are persisted in mounted ./results volume
```

### CI/CD Integration

The E2E analysis integrates with GitHub Actions:

```yaml
- name: Run E2E Analysis
  run: |
    cd separated_repos/strepsuis-analyzer
    strepsuis-analyzer-e2e --dataset both --random-state 42

- name: Upload Results
  uses: actions/upload-artifact@v4
  with:
    name: e2e-results
    path: separated_repos/strepsuis-analyzer/results/
```

Artifacts are available in the Actions tab for 7 days.

### Batch Processing

Process multiple datasets:
```bash
#!/bin/bash
for dataset in dataset1 dataset2 dataset3; do
    # Copy dataset files to data/
    cp ${dataset}/*.csv data/
    
    # Run analysis
    strepsuis-analyzer-e2e --dataset example \
        --results-dir results/${dataset}
    
    # Move results
    mkdir -p archive/${dataset}
    mv results/strepsuis-analyzer-* archive/${dataset}/
done
```

## Troubleshooting

### Common Issues

**1. Port Already in Use (Streamlit)**
```bash
# Error: Address already in use
# Solution: Use custom port
strepsuis-analyzer --launch --port 8502
```

**2. Memory Issues (Large Datasets)**
```bash
# For datasets with >1000 strains or >500 features
# Increase Python memory limit
ulimit -v unlimited
export PYTHONHASHSEED=0
```

**3. Missing Dependencies**
```bash
# Reinstall with dev dependencies
pip install -e .[dev]
```

**4. Phylogenetic Tree Parse Errors**
- Ensure Newick file has balanced parentheses
- Check for special characters in taxon names
- Verify taxon names match CSV strain IDs

**5. E2E Self-Checks Fail**
- Check that all input files exist
- Verify file formats (CSV headers, data types)
- Review logs in `results/*/logs/run.log`

**6. Coverage Below Threshold in CI**
- Expected coverage: ~50% (Streamlit UI code not tested)
- Core mathematical functions: 100% coverage
- Acceptable range: 34-100%

### Performance Optimization

**For Large Datasets (>500 strains):**
- Use subsetting for exploratory analysis
- Disable expensive visualizations
- Run clustering on PCA-reduced data
- Use DBSCAN instead of hierarchical clustering

**For High-Dimensional Data (>1000 features):**
- Apply feature selection first
- Use correlation-based filtering
- Consider dimensionality reduction (PCA, UMAP)

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/MK-vet/MKrep/issues)
- **Documentation**: See `README.md`, `docs/API.md`, `docs/TESTING.md`
- **Examples**: Check `scripts/README.md` for code examples

## Best Practices

1. **Always validate data** before analysis
2. **Use consistent strain IDs** across all files
3. **Set random seeds** for reproducibility
4. **Check self-checks** in E2E logs
5. **Review validation reports** for data quality issues
6. **Apply multiple testing correction** for hypothesis tests
7. **Document workflow** for reproducible research

## Version History

- **v1.0.0**: Initial release with E2E analysis support
  - Headless CLI runner
  - Comprehensive analysis pipeline
  - CI/CD integration
  - Docker deployment
