# API Documentation - StrepSuisAnalyzer

## Module: `strepsuis_analyzer.data_validator`

### Class: `DataValidator`

Validates input data for analysis.

#### Methods

##### `validate_dataframe(df, name, min_rows, min_cols, required_columns, allow_missing)`
Validate a pandas DataFrame.

**Parameters:**
- `df` (pd.DataFrame): DataFrame to validate
- `name` (str): Name for error messages
- `min_rows` (int, optional): Minimum required rows
- `min_cols` (int, optional): Minimum required columns
- `required_columns` (list, optional): List of required column names
- `allow_missing` (bool): Whether to allow missing values (default: True)

**Returns:** `(bool, list, list)` - Tuple of (is_valid, errors, warnings)

##### `validate_binary_matrix(df, name)`
Validate that DataFrame contains only binary (0/1) values.

**Returns:** `(bool, list, list)` - Tuple of (is_valid, errors, warnings)

##### `validate_numeric_matrix(df, name, min_value, max_value)`
Validate that DataFrame contains numeric values within range.

**Returns:** `(bool, list, list)` - Tuple of (is_valid, errors, warnings)

---

## Module: `strepsuis_analyzer.statistical_analysis`

### Class: `StatisticalAnalyzer`

Performs statistical analysis on genomic and phenotypic data.

#### Methods

##### `compute_correlation(x, y, method='pearson')`
Compute correlation coefficient between two variables.

**Parameters:**
- `x`: First variable
- `y`: Second variable
- `method` (str): 'pearson', 'spearman', or 'kendall'

**Returns:** `(float, float)` - Tuple of (correlation, p_value)

##### `compute_phi_coefficient(x, y)`
Compute phi coefficient for two binary variables.

**Returns:** `float` - Phi coefficient value

##### `compute_cramers_v(x, y)`
Compute Cramér's V for categorical variables.

**Returns:** `float` - Cramér's V value (0 to 1)

##### `perform_ttest(group1, group2, paired=False)`
Perform t-test.

**Returns:** `(float, float)` - Tuple of (statistic, p_value)

##### `perform_anova(*groups)`
Perform one-way ANOVA.

**Returns:** `(float, float)` - Tuple of (F_statistic, p_value)

##### `apply_multiple_testing_correction(pvalues, method='fdr_bh', alpha=0.05)`
Apply multiple testing correction.

**Parameters:**
- `pvalues` (list): List of p-values
- `method` (str): 'bonferroni', 'fdr_bh', or 'fdr_by'
- `alpha` (float): Significance level

**Returns:** `(ndarray, ndarray)` - Tuple of (rejected, corrected_pvalues)

##### `meta_analysis_fixed_effects(effect_sizes, variances)`
Perform fixed-effects meta-analysis.

**Returns:** `(float, float, float)` - Tuple of (pooled_effect, pooled_variance, pooled_se)

##### `meta_analysis_random_effects(effect_sizes, variances)`
Perform random-effects meta-analysis using DerSimonian-Laird method.

**Returns:** `(float, float, float, float)` - Tuple of (pooled_effect, pooled_variance, pooled_se, tau_squared)

---

## Module: `strepsuis_analyzer.phylogenetic_utils`

### Class: `PhylogeneticAnalyzer`

Analyzes phylogenetic trees and computes tree-based metrics.

#### Methods

##### `load_tree_from_newick(newick_string)`
Load a phylogenetic tree from Newick format.

**Returns:** `bool` - True if successful

##### `get_leaf_names()`
Get names of all leaf nodes.

**Returns:** `list` - List of leaf names

##### `compute_robinson_foulds_distance(tree1_newick, tree2_newick, normalize=False)`
Compute Robinson-Foulds distance between two trees.

**Returns:** `float` - Robinson-Foulds distance

##### `get_bipartitions(newick_string)`
Get bipartitions (splits) from a tree.

**Returns:** `set` - Set of bipartitions as frozensets

##### `compute_faith_pd(newick_string, taxa_subset=None)`
Compute Faith's Phylogenetic Diversity.

**Returns:** `float` - Faith's PD value

---

## Module: `strepsuis_analyzer.visualization`

### Class: `Visualizer`

Creates visualizations for genomic and phenotypic data analysis.

#### Methods

##### `create_histogram(data, bins=30, title, xlabel, ylabel, color)`
Create a histogram.

**Returns:** `plt.Figure` - Matplotlib figure

##### `create_scatter_plot(x, y, title, xlabel, ylabel, color, show_regression=False)`
Create a scatter plot.

**Returns:** `plt.Figure` - Matplotlib figure

##### `create_heatmap(data, title, cmap='viridis', annot=False, fmt='.2f')`
Create a heatmap.

**Returns:** `plt.Figure` - Matplotlib figure

##### `create_plotly_scatter(x, y, title, xlabel, ylabel, hover_text=None)`
Create an interactive scatter plot using Plotly.

**Returns:** `go.Figure` - Plotly figure

---

## Module: `strepsuis_analyzer.report_generator`

### Class: `ReportGenerator`

Generates reports from analysis results.

#### Methods

##### `add_dataframe(name, df, description='')`
Add a DataFrame to the report.

##### `add_statistics(name, stats_dict, description='')`
Add statistics to the report.

##### `export_to_excel(filepath, include_metadata=True, style_headers=True)`
Export report to Excel file.

##### `export_to_html(filepath, include_css=True)`
Export report to HTML file.

**Returns:** `str` - HTML content as string

---

## Module: `strepsuis_analyzer.etl_operations`

### Class: `ETLOperations`

Performs ETL operations on data.

#### Methods

##### `pivot_table(df, index, columns, values, aggfunc='mean', fill_value=None)`
Create a pivot table.

**Returns:** `pd.DataFrame` - Pivot table

##### `aggregate_data(df, group_by, agg_dict)`
Aggregate data by groups.

**Returns:** `pd.DataFrame` - Aggregated DataFrame

##### `normalize_columns(df, columns, method='zscore')`
Normalize specified columns.

**Parameters:**
- `method` (str): 'zscore', 'minmax', or 'robust'

**Returns:** `pd.DataFrame` - DataFrame with normalized columns

##### `merge_dataframes(left, right, how='inner', on=None, left_on=None, right_on=None)`
Merge two DataFrames.

**Returns:** `pd.DataFrame` - Merged DataFrame

---

## Example Usage

```python
from strepsuis_analyzer import (
    DataValidator,
    StatisticalAnalyzer,
    PhylogeneticAnalyzer,
    Visualizer,
    ReportGenerator,
)
import pandas as pd

# Load data
df = pd.read_csv('data/AMR_genes.csv', index_col=0)

# Validate
validator = DataValidator()
is_valid, errors, warnings = validator.validate_binary_matrix(df)

# Statistical analysis
analyzer = StatisticalAnalyzer(random_state=42)
corr, pval = analyzer.compute_correlation(df['SAT-4'], df['ermB'])
print(f"Correlation: {corr:.3f}, p-value: {pval:.3e}")

# Visualization
viz = Visualizer()
fig = viz.create_heatmap(df.corr(), title="AMR Gene Correlations")
viz.save_figure(fig, 'correlation_heatmap.png')

# Generate report
report = ReportGenerator()
report.add_dataframe('AMR Data', df)
report.add_statistics('Summary', {'n_strains': len(df), 'n_genes': len(df.columns)})
report.export_to_excel('analysis_report.xlsx')
```
