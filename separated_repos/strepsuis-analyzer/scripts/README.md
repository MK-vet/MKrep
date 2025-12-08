# End-to-End Analysis Runner for strepsuis-analyzer

This directory contains comprehensive end-to-end (E2E) testing and demonstration scripts for the strepsuis-analyzer application.

## Contents

- **`generate_synthetic_data.py`**: Generates synthetic datasets matching the schema of example data
- **`e2e_run.py`**: Comprehensive E2E analysis runner demonstrating full application capabilities

## Synthetic Data Generation

### Usage

```bash
python scripts/generate_synthetic_data.py
```

This generates the following files in `data/synthetic/`:
- `AMR_genes.csv` - Binary matrix (50 strains × 21 AMR genes)
- `MIC.csv` - Numeric matrix (50 strains × 13 antibiotics)
- `Virulence.csv` - Binary matrix (50 strains × 106 virulence factors)
- `MLST.csv` - Categorical data (50 strains with ST types)
- `Serotype.csv` - Categorical data (50 strains with serotypes)
- `Snp_tree.newick` - Phylogenetic tree (50 taxa)

All data is generated deterministically with `random_state=42` for reproducibility.

## E2E Analysis Runner

### Overview

The E2E runner performs a comprehensive analysis workflow using the public API of strepsuis-analyzer, demonstrating:

1. **Data Validation**: Validates datasets, checks binary matrices, parses phylogenetic trees
2. **Statistical Analysis**: Correlations, normality tests, hypothesis tests, multiple testing corrections, meta-analysis
3. **Visualizations**: Histograms, scatter plots, box plots, violin plots, correlation heatmaps
4. **Clustering**: K-Means, K-Modes, hierarchical clustering, DBSCAN
5. **Phylogenetic Analysis**: Tree visualization, Robinson-Foulds distance, Faith's PD, cophenetic correlation
6. **ETL Operations**: Pivot tables, aggregations, normalization (z-score, min-max), data transformations
7. **Report Generation**: Excel (multi-sheet) and HTML reports with metadata

### Usage

#### Command Line (via installed package)

```bash
# Analyze both example and synthetic datasets
strepsuis-analyzer-e2e --dataset both --random-state 42

# Analyze only synthetic data
strepsuis-analyzer-e2e --dataset synthetic

# Analyze only example data
strepsuis-analyzer-e2e --dataset example

# Custom results directory
strepsuis-analyzer-e2e --dataset both --results-dir /path/to/results

# Don't fail if example data is missing
strepsuis-analyzer-e2e --dataset example --no-fail-on-missing
```

#### Direct Script Execution

```bash
# From repository root
python scripts/e2e_run.py --dataset both --random-state 42
```

### Output Structure

The E2E runner creates timestamped results directories:

```
results/strepsuis-analyzer-YYYYMMDD-HHMM/
├── example/                          # Example dataset results
│   ├── validation/
│   │   ├── validation_report.csv
│   │   └── summary.log
│   ├── stats/
│   │   ├── correlation_matrix.csv
│   │   ├── correlation_heatmap.png
│   │   ├── correlations_with_pvalues.csv
│   │   ├── normality_results.csv
│   │   ├── qq_plots.png
│   │   ├── hypothesis_tests.csv
│   │   ├── corrected_pvalues.csv
│   │   └── meta_analysis_results.csv
│   ├── visualizations/
│   │   ├── histogram_example.png
│   │   ├── scatter_plot_example.png
│   │   ├── boxplot_example.png
│   │   └── violin_plot_example.png
│   ├── clustering/
│   │   ├── kmeans_labels.csv
│   │   ├── kmeans_elbow_plot.png
│   │   ├── kmodes_labels.csv
│   │   ├── hierarchical_labels.csv
│   │   ├── hierarchical_dendrogram.png
│   │   └── dbscan_labels.csv
│   ├── phylogenetics/
│   │   ├── tree_plot.png
│   │   ├── rf_distances.csv
│   │   ├── phylo_diversity.csv
│   │   └── cophenetic_correlation.csv
│   ├── etl/
│   │   ├── aggregated_by_st.csv
│   │   ├── normalized_zscore.csv
│   │   ├── normalized_minmax.csv
│   │   └── transformed_data.csv
│   └── reports/
│       ├── final_report.xlsx
│       └── final_report.html
├── synthetic/                        # Synthetic dataset results (same structure)
│   └── ...
└── logs/
    └── run.log                       # Comprehensive execution log
```

### Operations Performed

#### 1. Validation (validation/)
- DataFrame validation (shape, required columns, missing values)
- Binary matrix validation (AMR genes, virulence factors)
- Phylogenetic tree parsing validation

**Outputs:**
- `validation_report.csv`: Detailed validation results for each dataset
- `summary.log`: Human-readable validation summary

#### 2. Statistical Analysis (stats/)

**Correlations:**
- Pearson, Spearman, Kendall correlations with p-values
- Phi coefficient for binary variables
- Cramér's V for categorical variables

**Normality Tests:**
- Shapiro-Wilk test for each numeric variable
- Q-Q plots for visual assessment

**Hypothesis Tests:**
- T-tests and Mann-Whitney U tests comparing groups
- ANOVA and Kruskal-Wallis for multi-group comparisons

**Multiple Testing Corrections:**
- Bonferroni correction
- Benjamini-Hochberg FDR correction

**Meta-Analysis:**
- Fixed-effects and random-effects models
- Cochran's Q test for heterogeneity

**Outputs:**
- `correlation_matrix.csv`: Correlation coefficients
- `correlation_heatmap.png`: Visual correlation matrix
- `correlations_with_pvalues.csv`: Detailed correlation results
- `normality_results.csv`: Normality test results
- `qq_plots.png`: Q-Q plots for normality assessment
- `hypothesis_tests.csv`: Statistical test results
- `corrected_pvalues.csv`: Multiple testing corrected p-values
- `meta_analysis_results.csv`: Meta-analysis results

#### 3. Visualizations (visualizations/)
- Histograms for distribution analysis
- Scatter plots with optional regression lines
- Box plots for group comparisons
- Violin plots showing distribution densities

**Outputs:**
- `histogram_example.png`
- `scatter_plot_example.png`
- `boxplot_example.png`
- `violin_plot_example.png`

#### 4. Clustering Analysis (clustering/)

**K-Means:**
- Elbow plot for optimal k selection
- Cluster assignments for numeric data

**K-Modes:**
- Clustering for binary/categorical data
- Optimal for AMR gene profiles

**Hierarchical Clustering:**
- Ward linkage dendrogram
- Cluster assignments at specified cutoff

**DBSCAN:**
- Density-based clustering
- Automatic outlier detection

**Outputs:**
- `kmeans_elbow_plot.png`: Elbow curve for K-Means
- `kmeans_labels.csv`: K-Means cluster assignments
- `kmodes_labels.csv`: K-Modes cluster assignments
- `hierarchical_dendrogram.png`: Dendrogram visualization
- `hierarchical_labels.csv`: Hierarchical cluster assignments
- `dbscan_labels.csv`: DBSCAN cluster assignments

#### 5. Phylogenetic Analysis (phylogenetics/)

**Tree Visualization:**
- Phylogenetic tree plots

**Distance Metrics:**
- Robinson-Foulds distance for tree comparison
- Pairwise phylogenetic distances

**Diversity Metrics:**
- Faith's Phylogenetic Diversity (PD)
- Cophenetic correlation

**Outputs:**
- `tree_plot.png`: Phylogenetic tree visualization
- `rf_distances.csv`: Robinson-Foulds distances
- `phylo_diversity.csv`: Faith's PD values
- `cophenetic_correlation.csv`: Tree-distance correlation

#### 6. ETL Operations (etl/)

**Transformations:**
- Pivot tables for data reshaping
- Group-by aggregations
- Z-score normalization
- Min-max normalization
- Data merging and joining

**Outputs:**
- `aggregated_by_st.csv`: Aggregated statistics by ST type
- `normalized_zscore.csv`: Z-score normalized data
- `normalized_minmax.csv`: Min-max normalized data
- `transformed_data.csv`: Merged and transformed datasets

#### 7. Report Generation (reports/)

**Excel Reports:**
- Multi-sheet workbooks
- Metadata sheet with analysis details
- Formatted tables with styled headers

**HTML Reports:**
- Self-contained HTML documents
- Interactive tables
- Analysis metadata

**Outputs:**
- `final_report.xlsx`: Multi-sheet Excel report
- `final_report.html`: Interactive HTML report

### Self-Checks

The E2E runner includes automated self-checks that verify:

1. **Minimum Output Requirements:**
   - ≥1 validation report
   - ≥2 statistical outputs (tables + figures)
   - ≥2 visualizations
   - ≥1 clustering output
   - ≥1 phylogenetic metric
   - ≥1 ETL output
   - 2 reports (Excel + HTML)

2. **Directory Structure:**
   - All required subdirectories exist
   - No empty category directories

3. **File Generation:**
   - Expected output files are created
   - Files contain valid data

The script exits with code 0 if all checks pass, code 1 otherwise.

### Determinism and Reproducibility

All random operations use a fixed seed (`random_state=42` by default):
- Synthetic data generation
- K-Means clustering
- K-Modes clustering
- DBSCAN clustering
- Statistical resampling operations

Running the same analysis twice with the same parameters produces identical results.

### Logging

Comprehensive logging includes:
- Timestamp for each operation
- Dataset shapes and summaries
- Operation progress indicators
- Error messages with context
- Final statistics (duration, outputs generated)

All logs are saved to `logs/run.log` with both file and console output.

### Error Handling

The runner is designed to be robust:
- Individual analysis failures don't stop the entire run
- Errors are logged with descriptive messages
- Missing optional dependencies are handled gracefully
- Final summary reports all errors encountered

### Example Run

```bash
$ strepsuis-analyzer-e2e --dataset both --random-state 42

================================================================================
Starting E2E Analysis Run
Results directory: ./results/strepsuis-analyzer-20231208-1430
Dataset type: both
Random state: 42
================================================================================

================================================================================
Analyzing EXAMPLE dataset
================================================================================

Loading example dataset...
  Loaded AMR_genes.csv: (91, 22)
  Loaded MIC.csv: (91, 14)
  Loaded Virulence.csv: (91, 107)
  Loaded MLST.csv: (91, 2)
  Loaded Serotype.csv: (91, 2)
  Loaded Snp_tree.newick
Running data validation...
  Saved validation report
Running statistical analysis...
  Computing correlations...
  Running normality tests...
  Running hypothesis tests...
  Applying multiple testing corrections...
  Running meta-analysis example...
Running visualizations...
  Generated 4 visualization plots
Running clustering analysis...
  Completed clustering analyses
Running phylogenetic analysis...
  Completed phylogenetic analyses
Running ETL operations...
  Completed ETL operations
Generating reports...
  Generated Excel and HTML reports

[... synthetic dataset analysis ...]

================================================================================
ANALYSIS COMPLETE
================================================================================
Duration: 8.43 seconds
Datasets analyzed: example, synthetic
Total outputs generated: 60
Results directory: ./results/strepsuis-analyzer-20231208-1430

================================================================================
PERFORMING SELF-CHECKS
================================================================================

Checking example dataset outputs...
  ✓ validation: 2 outputs (>=1 required)
  ✓ stats: 8 outputs (>=2 required)
  ✓ visualizations: 4 outputs (>=2 required)
  ✓ clustering: 6 outputs (>=1 required)
  ✓ phylogenetics: 4 outputs (>=1 required)
  ✓ etl: 4 outputs (>=1 required)
  ✓ reports: 2 outputs (>=2 required)

Checking synthetic dataset outputs...
  ✓ validation: 2 outputs (>=1 required)
  ✓ stats: 8 outputs (>=2 required)
  ✓ visualizations: 4 outputs (>=2 required)
  ✓ clustering: 6 outputs (>=1 required)
  ✓ phylogenetics: 4 outputs (>=1 required)
  ✓ etl: 4 outputs (>=1 required)
  ✓ reports: 2 outputs (>=2 required)

================================================================================
✓ ALL SELF-CHECKS PASSED
================================================================================
```

## Integration with CI/CD

The E2E runner can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: E2E Tests
on: [push, pull_request]
jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -e .
      - run: python scripts/generate_synthetic_data.py
      - run: strepsuis-analyzer-e2e --dataset synthetic --random-state 42
```

## API Usage Examples

The E2E runner demonstrates proper usage of all public API components:

```python
from strepsuis_analyzer import (
    DataValidator,
    StatisticalAnalyzer,
    PhylogeneticAnalyzer,
    Visualizer,
    ReportGenerator,
)
from strepsuis_analyzer.etl_operations import ETLOperations

# Initialize components
validator = DataValidator()
stats = StatisticalAnalyzer(random_state=42)
phylo = PhylogeneticAnalyzer()
viz = Visualizer()
etl = ETLOperations()
report = ReportGenerator()

# Validate data
is_valid, errors, warnings = validator.validate_dataframe(df, min_rows=10)

# Compute correlations
corr, pval = stats.compute_correlation(x, y, method='pearson')

# Create visualizations
fig = viz.create_histogram(data, bins=30)
fig.savefig('histogram.png')

# Cluster data
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(X)

# Phylogenetic analysis
phylo.load_tree_from_newick(tree_string)
pd_value = phylo.compute_faith_pd(tree_string, taxa_subset)

# ETL operations
normalized = etl.normalize_columns(df, columns=['col1', 'col2'], method='zscore')

# Generate reports
report.add_dataframe('results', df, 'Analysis results')
report.export_to_excel('report.xlsx')
report.export_to_html('report.html')
```

## Troubleshooting

### Missing Dependencies

If you encounter import errors:
```bash
pip install -e .
```

### BioPython/DendroPy Issues

Some phylogenetic features require BioPython and DendroPy:
```bash
pip install biopython dendropy
```

### Memory Issues

For very large datasets, you may need to:
- Reduce the number of strains/features
- Run analyses on subsets
- Increase available memory

### File Permission Errors

Ensure you have write permissions for the results directory:
```bash
chmod -R u+w results/
```

## Contributing

When adding new features to strepsuis-analyzer:

1. Update `e2e_run.py` to demonstrate the new functionality
2. Add appropriate self-checks
3. Update this README with usage examples
4. Ensure deterministic behavior (use `random_state` parameters)

## License

Same license as strepsuis-analyzer (MIT License).

## Contact

For issues or questions:
- GitHub Issues: https://github.com/MK-vet/strepsuis-analyzer/issues
- Email: support@strepsuis-suite.org
