# MKrep Project Summary

## Project Overview

MKrep is a comprehensive bioinformatics analysis pipeline for microbial genomics, specializing in:
- Antimicrobial resistance (AMR) pattern analysis
- Virulence factor profiling
- Phylogenetic clustering and evolutionary analysis
- Network analysis of gene-phenotype associations
- Binary trait analysis (0 = absence, 1 = presence)

**Version**: 1.0.0  
**Release Date**: 2025-01-07  
**License**: MIT  
**Repository**: https://github.com/MK-vet/MKrep

---

## Project Structure

```
MKrep/
├── Analysis Scripts (5)
│   ├── Cluster_MIC_AMR_Viruelnce.py          # K-Modes clustering
│   ├── MDR_2025_04_15.py                     # MDR analysis
│   ├── Network_Analysis_2025_06_26.py        # Network analysis
│   ├── Phylgenetic_clustering_2025_03_21.py  # Phylogenetic clustering
│   └── StrepSuisPhyloCluster_2025_08_11.py   # S. suis analysis
│
├── Utilities
│   ├── excel_report_utils.py                 # Shared Excel report generator
│   └── validate.py                           # Validation script
│
├── Google Colab Notebooks (5)
│   ├── colab_notebooks/
│   │   ├── Cluster_Analysis_Colab.ipynb
│   │   ├── MDR_Analysis_Colab.ipynb
│   │   ├── Network_Analysis_Colab.ipynb
│   │   ├── Phylogenetic_Clustering_Colab.ipynb
│   │   ├── StrepSuis_Analysis_Colab.ipynb
│   │   └── README.md
│
├── Python Package
│   ├── python_package/
│   │   ├── mkrep/
│   │   │   ├── __init__.py
│   │   │   ├── cli.py                        # CLI interface
│   │   │   ├── analysis/                     # Analysis modules
│   │   │   └── utils/                        # Utility modules
│   │   ├── pyproject.toml                    # Package configuration
│   │   └── README.md
│
├── Hugging Face Demo
│   ├── huggingface_demo/
│   │   ├── example_data/                     # Example datasets
│   │   ├── requirements.txt                  # Voilà dependencies
│   │   └── README.md
│
├── Documentation (8 files)
│   ├── README.md                             # Main documentation
│   ├── INSTALLATION.md                       # Installation guide
│   ├── BINARY_DATA_GUIDE.md                  # Binary data handling
│   ├── FEATURES.md                           # Complete feature list
│   ├── EXCEL_REPORTS_README.md               # Excel report guide
│   ├── EXCEL_REPORT_EXAMPLES.md              # Report examples
│   ├── requirements.txt                      # Dependencies
│   └── PROJECT_SUMMARY.md                    # This file
│
└── Example Data (7 CSV files)
    ├── MIC.csv
    ├── AMR_genes.csv
    ├── Virulence.csv
    ├── MLST.csv
    ├── Serotype.csv
    ├── Plasmid.csv
    └── MGE.csv
```

---

## Key Features

### 1. Multiple Deployment Options

#### Option A: Google Colab (Recommended for Beginners)
- No installation required
- Cloud-based execution
- Free GPU access
- File upload/download interface
- One-click deployment

**Quick Start**:
1. Click: [Open in Colab](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Cluster_Analysis_Colab.ipynb)
2. Upload your CSV files
3. Run all cells
4. Download results (HTML, Excel, PNG)

#### Option B: Command-Line Interface
- Python package with full CLI
- Suitable for HPC clusters
- Batch processing
- Configuration file support

**Quick Start**:
```bash
pip install mkrep
mkrep-cluster --data-dir ./data --output ./results
```

#### Option C: Interactive Dashboard
- Web-based interface
- Voilà-powered dashboard
- Drag-and-drop file upload
- Real-time analysis
- Parameter widgets

**Quick Start**:
```bash
cd huggingface_demo
voila MKrep_Dashboard.ipynb
```

#### Option D: Standalone Scripts
- Direct Python execution
- Maximum customization
- No package installation
- Ideal for development

**Quick Start**:
```bash
python Cluster_MIC_AMR_Viruelnce.py
```

### 2. Comprehensive Reports

All analyses generate **three types of outputs**:

#### HTML Reports
- Interactive DataTables (sort, filter, search)
- Export buttons (CSV, Excel, PDF, Print)
- Plotly visualizations
- Bootstrap 5 styling
- Responsive design
- Single-file (embeds CSS/JS)

#### Excel Reports
- Multi-sheet workbooks (5-20 sheets)
- Metadata sheet (configuration)
- Methodology sheet (detailed methods)
- Data sheets (all results)
- Chart Index sheet (PNG files list)
- Auto-formatted tables
- Proper numeric precision

#### PNG Charts
- High-quality images (150-300 DPI)
- Publication-ready
- Saved in png_charts/ folder
- All visualizations from HTML

### 3. Binary Data Handling

**MKrep is specifically designed for binary data**:
- 0 = Absence of feature
- 1 = Presence of feature

**Both values are biologically significant!**

#### Proper Statistical Treatment
- ✓ K-Modes clustering (categorical data)
- ✓ Chi-square tests (contingency tables)
- ✓ Fisher exact test (small samples)
- ✓ Log-odds ratios (effect sizes)
- ✓ Bootstrap CIs (stratified resampling)
- ✓ Random Forest (binary classification)
- ✓ MCA (categorical dimensionality reduction)
- ✓ Association rules (binary patterns)

#### Data Validation
```python
def validate_binary_data(df):
    """Ensure data is strictly 0/1 binary."""
    if not ((df.values == 0) | (df.values == 1)).all():
        raise ValueError("Data is not strictly 0/1 binary.")
```

See [BINARY_DATA_GUIDE.md](BINARY_DATA_GUIDE.md) for comprehensive details.

### 4. Statistical Rigor

#### Multiple Testing Correction
- Benjamini-Hochberg FDR (α=0.05)
- Bonferroni (optional)
- Pairwise post-hoc with correction

#### Bootstrap Confidence Intervals
- 200-1000 resamples
- Stratified sampling
- Percentile method
- BCa option

#### Effect Sizes
- Log-odds ratios (with pseudocount)
- Cramér's V (categorical associations)
- Cohen's d (continuous comparisons)
- CIs for all effect sizes

#### Model Validation
- Cross-validation (5-fold, 10-fold)
- Out-of-bag error (RF)
- Silhouette score (clustering)
- Davies-Bouldin index
- Calinski-Harabasz score

---

## Analysis Scripts Comparison

| Feature | Cluster | MDR | Network | Phylo | StrepSuis |
|---------|:-------:|:---:|:-------:|:-----:|:---------:|
| **Primary Use** | General clustering | MDR patterns | Associations | Tree-based | S. suis specific |
| **Tree Required** | ✗ | ✗ | ✗ | ✓ | ✓ |
| **Clustering** | K-Modes | - | - | Multiple | Ensemble |
| **Bootstrap** | ✓ | ✓ | ✗ | ✓ | ✓ |
| **Network** | ✗ | ✓ | ✓ | ✗ | ✗ |
| **MCA** | ✓ | ✗ | ✗ | ✓ | ✓ |
| **UMAP** | ✗ | ✗ | ✗ | ✓ | ✗ |
| **Assoc. Rules** | ✓ | ✓ | ✗ | ✓ | ✓ |
| **Typical Runtime** | 5-10 min | 10-15 min | 3-5 min | 15-30 min | 10-20 min |

---

## Documentation

### Essential Guides
1. **README.md** - Start here! Quick start and overview
2. **INSTALLATION.md** - Complete installation instructions
3. **BINARY_DATA_GUIDE.md** - Binary data handling (crucial!)
4. **FEATURES.md** - Complete feature list

### Specialized Guides
5. **EXCEL_REPORTS_README.md** - Excel report structure
6. **EXCEL_REPORT_EXAMPLES.md** - Report examples
7. **colab_notebooks/README.md** - Colab usage
8. **python_package/README.md** - Package documentation
9. **huggingface_demo/README.md** - Dashboard guide

### Tools
10. **validate.py** - Validation script (checks dependencies, data, scripts)
11. **requirements.txt** - All dependencies

---

## Quick Start Examples

### Example 1: Basic Cluster Analysis (Colab)
```
1. Open: https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Cluster_Analysis_Colab.ipynb
2. Upload MIC.csv, AMR_genes.csv, Virulence.csv
3. Run all cells
4. Download results.zip
```

### Example 2: MDR Analysis (CLI)
```bash
# Install package
pip install mkrep

# Run analysis
mkrep-mdr \
  --data-dir ./data \
  --output ./results \
  --mdr-threshold 3 \
  --bootstrap 1000 \
  --confidence 0.6

# Results in ./results/
```

### Example 3: Network Analysis (Script)
```bash
# Clone repository
git clone https://github.com/MK-vet/MKrep.git
cd MKrep

# Install dependencies
pip install -r requirements.txt

# Run analysis
python Network_Analysis_2025_06_26.py

# Results in report.html and Excel report
```

### Example 4: Phylogenetic Analysis (Dashboard)
```bash
# Install Voilà
pip install voila

# Launch dashboard
cd huggingface_demo
voila MKrep_Dashboard.ipynb --port 8866

# Open browser to http://localhost:8866
```

---

## Data Requirements

### File Format
- **Type**: CSV (comma-separated values)
- **Encoding**: UTF-8
- **Required column**: Strain_ID (first column)
- **Feature columns**: Binary (0 or 1) only
- **No missing values**: Encode as 0 or 1

### Example
```csv
Strain_ID,Gene1,Gene2,Antibiotic1,Virulence1
Strain001,1,0,1,0
Strain002,0,1,1,1
Strain003,1,1,0,1
```

### Minimum Requirements
- At least 2 strains
- At least 2 features
- Features should have variability (not all 0 or all 1)

### Recommended Size
- 20+ strains (for robust statistics)
- 10+ features (for meaningful patterns)
- Balanced features (not all 0.9 or 0.1 frequency)

---

## Technical Specifications

### System Requirements
- **Python**: 3.8, 3.9, 3.10, 3.11, 3.12
- **RAM**: 4 GB minimum, 8 GB recommended
- **Storage**: 500 MB for software, 1-5 GB for outputs
- **CPU**: Multi-core recommended (automatic parallelization)

### Performance
- **Small** (< 100 strains): < 5 minutes
- **Medium** (100-1000 strains): 5-30 minutes
- **Large** (> 1000 strains): 30-120 minutes

### Compatibility
- **OS**: Windows, macOS, Linux
- **Browser**: Chrome, Firefox, Safari, Edge
- **Excel**: MS Excel 2016+, LibreOffice, Google Sheets

---

## Troubleshooting

### Common Issues

1. **"Module not found"**
   ```bash
   pip install -r requirements.txt
   ```

2. **"Data is not strictly 0/1 binary"**
   - Check for missing values: `df.isna().sum()`
   - Convert to binary: See BINARY_DATA_GUIDE.md

3. **"Memory error"**
   - Reduce bootstrap iterations
   - Filter features (remove low variance)
   - Use data chunking

4. **"Cannot save PNG"**
   ```bash
   pip install kaleido
   ```

5. **Colab session timeout**
   - Download results frequently
   - Mount Google Drive for persistence
   - Re-run cells if disconnected

For more help: See [INSTALLATION.md](INSTALLATION.md#troubleshooting)

---

## Validation

### Run Validation Script
```bash
python validate.py
```

This checks:
- ✓ All dependencies installed
- ✓ Data files exist and valid
- ✓ Binary format correct
- ✓ Analysis scripts available
- ✓ Utility modules working
- ✓ Directory structure complete

---

## Citation

If you use MKrep in your research, please cite:

```bibtex
@software{mkrep2025,
  title = {MKrep: Comprehensive Bioinformatics Analysis Pipeline for Microbial Genomics},
  author = {MK-vet},
  year = {2025},
  url = {https://github.com/MK-vet/MKrep},
  version = {1.0.0}
}
```

---

## Contributing

We welcome contributions! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests (if applicable)
5. Update documentation
6. Submit a pull request

See [GitHub repository](https://github.com/MK-vet/MKrep) for details.

---

## Support

- **Issues**: https://github.com/MK-vet/MKrep/issues
- **Documentation**: See README files in each directory
- **Validation**: Run `python validate.py`

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

## Acknowledgments

This tool was developed for the microbial genomics research community. We thank all contributors and users for their feedback and support.

---

## Version History

### Version 1.0.0 (2025-01-07)
- ✨ Initial release
- ✨ 5 analysis scripts with HTML and Excel reports
- ✨ Google Colab notebooks for all analyses
- ✨ Python package with CLI
- ✨ Hugging Face demo framework
- ✨ Comprehensive documentation (8 guides)
- ✨ Binary data validation and handling
- ✨ Validation script
- ✨ Example datasets

---

**Last Updated**: 2025-01-07  
**Status**: Production Ready  
**Maintainer**: MK-vet
