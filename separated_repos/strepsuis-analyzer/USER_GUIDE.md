# User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Features](#features)
5. [Data Formats](#data-formats)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Usage](#advanced-usage)

## Introduction

StrepSuisAnalyzer is an interactive web application for comprehensive genomic and phenotypic analysis of *Streptococcus suis* and other bacterial species.

### Key Capabilities

- **Statistical Analysis**: Correlations, hypothesis tests, meta-analysis
- **Phylogenetic Analysis**: Tree visualization, Robinson-Foulds distance, Faith's PD
- **Machine Learning**: K-Means, K-Modes, hierarchical, DBSCAN clustering
- **Visualizations**: Interactive Plotly and publication-quality matplotlib plots
- **Report Generation**: Excel and HTML export

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 4GB RAM minimum (8GB recommended)

### Using pip

```bash
# Clone repository
git clone https://github.com/MK-vet/MKrep.git
cd MKrep/separated_repos/strepsuis-analyzer

# Install package
pip install -e .
```

### Using Docker

```bash
cd MKrep/separated_repos/strepsuis-analyzer
docker-compose up
```

Access at http://localhost:8501

## Getting Started

### Launch Application

```bash
# Using Streamlit directly
streamlit run app.py

# Or using Python module
python -m streamlit run src/strepsuis_analyzer/app.py
```

### First Analysis

1. **Upload Data**: Use the sidebar file uploader
2. **Select Analysis**: Choose from available analysis types
3. **Configure Parameters**: Adjust settings as needed
4. **Run Analysis**: Click the analysis button
5. **View Results**: Explore interactive visualizations
6. **Export**: Download reports in Excel or HTML format

## Features

### 1. Statistical Analysis

#### Correlation Analysis

Calculate Pearson, Spearman, or Kendall correlations:

1. Upload numeric data (MIC values, continuous variables)
2. Select correlation method
3. Set significance threshold
4. View correlation matrix heatmap
5. Export significant correlations

#### Hypothesis Testing

Perform statistical tests:

- **Chi-square test**: Categorical associations
- **Fisher's exact test**: Small sample sizes
- **T-test**: Compare means
- **Mann-Whitney U**: Non-parametric comparison

#### Meta-Analysis

Combine results from multiple studies:

1. Upload summary statistics
2. Select meta-analysis model (fixed/random effects)
3. Visualize forest plots
4. Export combined estimates

### 2. Phylogenetic Analysis

#### Tree Visualization

Interactive phylogenetic tree display:

1. Upload Newick format tree
2. Customize node labels and colors
3. Highlight clades of interest
4. Export publication-quality figures

#### Phylogenetic Metrics

Calculate:

- Robinson-Foulds distance
- Faith's Phylogenetic Diversity
- Tree balance metrics
- Branch length statistics

#### Trait Mapping

Map phenotypes to phylogeny:

1. Upload tree and trait data
2. Select traits to visualize
3. View ancestral state reconstruction
4. Export annotated trees

### 3. Machine Learning

#### Clustering

Available algorithms:

**K-Means Clustering**
- For numeric data
- Optimal k selection via elbow method
- Silhouette analysis

**K-Modes Clustering**
- For categorical/binary data
- Automatic parameter optimization
- Cluster characterization

**Hierarchical Clustering**
- Dendrogram visualization
- Multiple linkage methods
- Customizable distance metrics

**DBSCAN**
- Density-based clustering
- Noise detection
- Parameter tuning interface

### 4. Visualizations

#### Interactive Plots (Plotly)

- Scatter plots with hover information
- 3D visualizations
- Network graphs
- Heatmaps with dendrograms

#### Publication Figures (Matplotlib)

- High-resolution output
- Customizable styles
- Multiple export formats (PNG, PDF, SVG)
- Professional layout

### 5. ETL Operations

Transform and aggregate data:

- **Pivot Tables**: Reshape data
- **Aggregations**: Sum, mean, count, etc.
- **Window Functions**: Rolling statistics
- **Custom Formulas**: Create derived variables

### 6. Report Generation

Export analysis results:

**Excel Reports**
- Multiple sheets for different analyses
- Formatted tables
- Embedded charts

**HTML Reports**
- Interactive tables with DataTables
- Embedded visualizations
- Professional styling

## Data Formats

### Supported File Types

| Data Type | Format | Required Columns | Example |
|-----------|--------|-----------------|---------|
| AMR Genes | CSV | Strain_ID, gene columns | strain_001, aac(6')-Ie-aph(2'')-Ia |
| MIC Values | CSV | Strain_ID, antibiotic columns | strain_001, PEN, TET, ERY |
| Virulence | CSV | Strain_ID, factor columns | strain_001, sly, mrp, epf |
| MLST | CSV | Strain_ID, ST | strain_001, ST1 |
| Phylogeny | Newick | Tree structure | (strain_001:0.01,strain_002:0.02) |

### Data Requirements

**Binary Data** (AMR, Virulence)
- Values: 0 (absent) or 1 (present)
- First column: Strain_ID
- No missing values

**Numeric Data** (MIC)
- Numeric values only
- First column: Strain_ID
- Missing values: Use NA or leave blank

**Categorical Data** (MLST, Serotype)
- String values
- Consistent naming
- First column: Strain_ID

### Example Data

Example datasets are provided in `data/examples/`:

```bash
data/examples/
├── sample_amr.csv
├── sample_mic.csv
├── sample_virulence.csv
├── sample_mlst.csv
└── sample_tree.nwk
```

## Troubleshooting

### Common Issues

**Application won't start**
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -e . --force-reinstall
```

**Import errors**
```bash
# Install in development mode
pip install -e .
```

**Visualization issues**
- Clear browser cache
- Try different browser
- Check console for JavaScript errors

**Memory errors**
- Reduce dataset size
- Increase Docker memory allocation
- Use sampling for large datasets

### Performance Tips

1. **Use appropriate data types**: Integer for counts, float for measurements
2. **Filter data before analysis**: Remove irrelevant columns
3. **Use sampling**: For exploratory analysis on large datasets
4. **Close unused tabs**: Free up browser memory
5. **Restart application**: If experiencing slowdowns

## Advanced Usage

### Custom Analysis

Create custom analysis scripts:

```python
import streamlit as st
from src.strepsuis_analyzer import components

# Custom analysis implementation
st.title("Custom Analysis")
data = st.file_uploader("Upload data")
if data:
    result = components.custom_analysis(data)
    st.write(result)
```

### Batch Processing

Process multiple files:

```bash
# Create batch script
for file in data/*.csv; do
    python -m strepsuis_analyzer.batch --input "$file"
done
```

### Integration with Other Tools

Export data for external tools:

```python
# Export for R
import pandas as pd
data.to_csv("output_for_r.csv", index=False)

# Export for QIIME2
data.to_csv("output_for_qiime.txt", sep="\t")
```

## Best Practices

1. **Validate data**: Check data quality before analysis
2. **Document parameters**: Keep track of analysis settings
3. **Save intermediate results**: Export at each step
4. **Use version control**: Track analysis scripts
5. **Backup results**: Save reports and visualizations

## Getting Help

- **Documentation**: Check README.md and other docs
- **Issues**: Report bugs on GitHub
- **Questions**: Open a discussion on GitHub

## Citation

If you use StrepSuisAnalyzer in your research, please cite:

```bibtex
@software{strepsuis_analyzer,
  title = {StrepSuisAnalyzer: Interactive Analysis Platform},
  author = {MK-vet},
  year = {2025},
  url = {https://github.com/MK-vet/MKrep}
}
```

---

Last updated: 2025-01-15
