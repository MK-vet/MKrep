# MKrep - Microbial Genomics Analysis Package

A comprehensive Python package for bioinformatics analysis of microbial genomics data.

## Features

- **Clustering Analysis**: K-Modes clustering for MIC, AMR, and virulence data
- **MDR Analysis**: Multi-drug resistance pattern detection and hybrid network analysis
- **Network Analysis**: Feature association networks with community detection
- **Phylogenetic Clustering**: Tree-based clustering with evolutionary metrics
- **Streptococcus suis Analysis**: Specialized analysis for S. suis strains

## Installation

### From PyPI (when published)
```bash
pip install mkrep
```

### From Source
```bash
git clone https://github.com/MK-vet/MKrep.git
cd MKrep/python_package
pip install -e .
```

### With Development Dependencies
```bash
pip install -e ".[dev]"
```

## Quick Start

### Command Line Interface

```bash
# Cluster analysis
mkrep-cluster --data-dir ./data --output ./results

# MDR analysis
mkrep-mdr --data-dir ./data --output ./results

# Network analysis
mkrep-network --data-dir ./data --output ./results

# Phylogenetic clustering
mkrep-phylo --tree tree.newick --data-dir ./data --output ./results

# StrepSuis analysis
mkrep-strepsuis --tree tree.newick --data-dir ./data --output ./results
```

### Python API

```python
from mkrep.analysis import ClusterAnalyzer, MDRAnalyzer, NetworkAnalyzer

# Cluster analysis
analyzer = ClusterAnalyzer(data_dir="./data", output_dir="./results")
results = analyzer.run()

# Generate reports
analyzer.generate_html_report(results)
analyzer.generate_excel_report(results)
```

## Data Format

All input files should be CSV format with:
- **Strain_ID** column (required): Unique identifier for each strain
- **Binary features** (0 = absence, 1 = presence): Gene presence, resistance, virulence factors

Example:
```csv
Strain_ID,Gene1,Gene2,Antibiotic1,Virulence1
Strain001,1,0,1,0
Strain002,0,1,1,1
Strain003,1,1,0,1
```

## Output

Each analysis generates:
1. **HTML Report** - Interactive tables with DataTables (sorting, filtering, export)
2. **Excel Report** - Multi-sheet workbook with methodology and detailed results
3. **PNG Charts** - High-quality visualizations for publications
4. **CSV Files** - Intermediate results and data tables

## Command Line Options

### Common Options (all commands)

```
--data-dir PATH          Directory containing input CSV files
--output PATH           Output directory for results (default: ./output)
--config FILE           Configuration file (JSON/YAML)
--verbose               Enable verbose logging
--help                  Show help message
```

### Cluster Analysis Options

```
mkrep-cluster [OPTIONS]

Options:
  --max-clusters INT      Maximum number of clusters to test (default: auto)
  --bootstrap INT         Number of bootstrap iterations (default: 500)
  --fdr-alpha FLOAT       FDR correction alpha level (default: 0.05)
  --mca-components INT    Number of MCA components (default: 2)
```

### MDR Analysis Options

```
mkrep-mdr [OPTIONS]

Options:
  --mdr-threshold INT     Minimum classes for MDR classification (default: 3)
  --bootstrap INT         Number of bootstrap iterations (default: 500)
  --confidence FLOAT      Association rules confidence threshold (default: 0.5)
  --support FLOAT         Association rules support threshold (default: 0.1)
```

### Network Analysis Options

```
mkrep-network [OPTIONS]

Options:
  --chi2-threshold FLOAT  Chi-square p-value threshold (default: 0.05)
  --cramers-threshold FLOAT  Cramér's V threshold (default: 0.3)
  --min-degree INT        Minimum node degree for hubs (default: auto)
```

### Phylogenetic Analysis Options

```
mkrep-phylo [OPTIONS]

Options:
  --tree FILE             Phylogenetic tree file (Newick format) [required]
  --clustering METHOD     Clustering method (kmeans/dbscan/gmm) (default: auto)
  --n-clusters INT        Number of clusters (default: auto)
  --umap-components INT   UMAP dimensions (default: 2)
  --bootstrap INT         Number of bootstrap iterations (default: 500)
```

## Configuration File

Create a JSON or YAML configuration file for reproducible analyses:

```json
{
  "data_dir": "./data",
  "output_dir": "./results",
  "clustering": {
    "max_clusters": 10,
    "bootstrap_iterations": 500
  },
  "statistics": {
    "fdr_alpha": 0.05,
    "chi2_threshold": 0.05
  },
  "reporting": {
    "generate_html": true,
    "generate_excel": true,
    "save_png_charts": true
  }
}
```

Use with: `mkrep-cluster --config config.json`

## Examples

### Example 1: Basic Cluster Analysis
```bash
mkrep-cluster \
  --data-dir ./example_data \
  --output ./cluster_results \
  --max-clusters 8 \
  --bootstrap 1000
```

### Example 2: MDR Analysis with Custom Thresholds
```bash
mkrep-mdr \
  --data-dir ./example_data \
  --output ./mdr_results \
  --mdr-threshold 3 \
  --confidence 0.6 \
  --support 0.15
```

### Example 3: Phylogenetic Clustering
```bash
mkrep-phylo \
  --tree tree.newick \
  --data-dir ./example_data \
  --output ./phylo_results \
  --clustering kmeans \
  --n-clusters 5
```

## Requirements

- Python >= 3.8
- See `pyproject.toml` for complete dependency list

## Documentation

Full documentation is available at:
- [Main Repository README](https://github.com/MK-vet/MKrep#readme)
- [Excel Reports Guide](https://github.com/MK-vet/MKrep/blob/main/EXCEL_REPORTS_README.md)
- [Google Colab Notebooks](https://github.com/MK-vet/MKrep/tree/main/colab_notebooks)

## Citation

If you use MKrep in your research, please cite:

```
MK-vet/MKrep: Comprehensive bioinformatics analysis pipeline for microbial genomics
https://github.com/MK-vet/MKrep
```

## License

MIT License - see LICENSE file for details

## Support

- GitHub Issues: https://github.com/MK-vet/MKrep/issues
- Documentation: https://github.com/MK-vet/MKrep#readme

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Changelog

### Version 1.0.0 (2025-01-07)
- Initial package release
- CLI interface for all analysis types
- HTML and Excel report generation
- PNG chart export
- Comprehensive documentation
