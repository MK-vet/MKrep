# MKrep - Complete Feature List

## Analysis Scripts (5 Total)

### 1. Cluster_MIC_AMR_Viruelnce.py
**Purpose**: Comprehensive clustering analysis for MIC, AMR, and virulence data

**Features**:
- K-Modes clustering with automatic cluster number selection
- Silhouette score optimization (2 to sqrt(N) clusters)
- Multiple Correspondence Analysis (MCA) for dimensionality reduction
- Chi-square and Fisher exact tests for associations
- Log-odds ratios with bootstrap confidence intervals (500+ resamples)
- Logistic regression for feature prediction
- Random Forest feature importance (100 bootstrap iterations)
- Association rule mining (Apriori algorithm)
- Data profiling with ydata-profiling

**Input Files**:
- MIC.csv, AMR_genes.csv, Virulence.csv, MLST.csv, Serotype.csv, Plasmid.csv, MGE.csv

**Output**:
- Interactive HTML report with DataTables
- Multi-sheet Excel workbook
- PNG charts (MCA scatter plots, correlation heatmaps)
- CSV files for all intermediate results

**Statistical Methods**:
- K-Modes clustering (Huang initialization)
- Chi-square tests with Yates correction
- Fisher exact test fallback for 2×2 tables
- Benjamini-Hochberg FDR correction (α=0.05)
- Bootstrap resampling (stratified)
- Logistic regression (L2 regularization)
- Random Forest (100 trees, bootstrap aggregation)
- MCA (2-10 components)
- Apriori (min support=0.1, min confidence=0.5)

---

### 2. MDR_2025_04_15.py
**Purpose**: Multi-drug resistance analysis with hybrid network approach

**Features**:
- MDR classification by antibiotic classes (threshold: 3+ classes)
- Bootstrap resampling for prevalence estimation (95% CI)
- Frequency analysis (all strains vs MDR strains)
- Pattern analysis (co-occurrence matrices)
- Association rule mining (phenotypes and genes separately)
- Hybrid co-resistance network (phenotype-gene interactions)
- Network community detection (Louvain algorithm)
- Interactive network visualization (3D Plotly)

**Input Files**:
- CSV files with binary resistance/gene data

**Output**:
- Interactive HTML report
- Multi-sheet Excel workbook
- PNG charts (hybrid network visualization)
- Network statistics (degree centrality, betweenness, communities)

**Statistical Methods**:
- Bootstrap resampling (1000 iterations)
- Chi-square tests for associations
- Fisher exact test for small samples
- Apriori for association rules
- Jaccard similarity for co-occurrence
- Louvain community detection
- Network centrality measures

---

### 3. Network_Analysis_2025_06_26.py
**Purpose**: Statistical network analysis for feature associations

**Features**:
- Chi-square and Fisher exact tests for all feature pairs
- Information theory metrics (Shannon entropy, Cramér's V)
- Mutually exclusive pattern detection (k=2 and k=3)
- Network construction with significance filtering
- Community detection and clustering
- Hub identification (degree centrality > mean + 1.5×SD)
- 3D network visualization with cluster labels
- Feature summary by category

**Input Files**:
- CSV files with binary feature data

**Output**:
- Interactive HTML report
- Multi-sheet Excel workbook
- PNG charts (3D network visualization)
- Detailed statistics for all feature pairs

**Statistical Methods**:
- Chi-square tests (α=0.05)
- Fisher exact test for 2×2 tables
- Benjamini-Hochberg FDR correction
- Shannon entropy (information content)
- Cramér's V (effect size, threshold=0.3)
- Network clustering (Louvain)
- Hub analysis (z-score based)

---

### 4. Phylgenetic_clustering_2025_03_21.py
**Purpose**: Complete phylogenetic clustering and binary trait analysis

**Features**:
- Phylogenetic tree parsing (Newick format)
- Tree-aware clustering (K-Means, DBSCAN, GMM)
- Outlier detection (Isolation Forest)
- Ensemble clustering (weighted voting)
- Hyperparameter optimization (Optuna, 50 trials)
- Faith's Phylogenetic Diversity (PD)
- Pairwise patristic distances
- Beta diversity metrics (phylogenetic)
- UMAP dimensionality reduction (2D projection)
- Binary trait analysis (Chi-square, log-odds, RF)
- Association rule mining
- Multiple Correspondence Analysis (MCA)

**Input Files**:
- Phylogenetic tree (Newick format)
- CSV files with binary trait data

**Output**:
- Interactive HTML report
- Multi-sheet Excel workbook
- PNG charts (phylogenetic tree, UMAP embedding)
- All CSV results included

**Statistical Methods**:
- Tree-based clustering (patristic distances)
- K-Means (optimized k)
- DBSCAN (optimized eps, min_samples)
- Gaussian Mixture Models (optimized components)
- Isolation Forest (contamination=0.1)
- Optuna hyperparameter search
- Faith's PD (phylogenetic diversity)
- UniFrac distances
- UMAP (n_neighbors=15, min_dist=0.1)
- Chi-square tests with FDR correction
- Bootstrap log-odds (200+ resamples)
- Random Forest (100 trees)
- MCA (2 components)
- Apriori (support=0.1, confidence=0.5)

---

### 5. StrepSuisPhyloCluster_2025_08_11.py
**Purpose**: Integrative phylogenetic clustering for Streptococcus suis

**Features**:
- Tree-aware clustering with ensemble fallback
- Trait profiling (chi-square, log-odds, RF importance)
- Association rules mining
- Multiple Correspondence Analysis (MCA)
- Bootstrap confidence intervals
- Bootstrap 5 UI with CSV export
- Comprehensive evolutionary metrics

**Input Files**:
- Snp_tree.newick (phylogenetic tree)
- CSV files with trait data

**Output**:
- Interactive HTML report (Bootstrap 5 theme)
- Multi-sheet Excel workbook
- PNG charts (phylogenetic tree with clusters)
- All analysis results in CSV format

**Statistical Methods**:
- Tree-based clustering
- Ensemble methods (majority voting)
- Chi-square tests with FDR correction
- Log-odds ratios with bootstrap CIs
- Random Forest feature importance
- MCA (2 components)
- Association rules (Apriori)

---

## Shared Features (All Scripts)

### Report Generation
✅ **HTML Reports**:
- Interactive DataTables (sorting, filtering, searching)
- Export buttons (CSV, Excel, PDF, Print)
- Responsive design (works on mobile)
- Plotly interactive visualizations
- Bootstrap styling (modern UI)
- Collapsible sections
- Pagination (10-100 rows per page)

✅ **Excel Reports**:
- Multi-sheet workbooks (5-20 sheets per report)
- Metadata sheet (configuration, parameters)
- Methodology sheet (detailed method descriptions)
- Data sheets (all analysis results)
- Chart Index sheet (list of PNG files)
- Auto-formatted tables (column widths, rounding)
- Proper numeric precision (4 decimal places)
- Descriptive sheet names (sanitized for Excel)

✅ **PNG Charts**:
- High-quality images (150 DPI for matplotlib, 1200×800 for plotly)
- Saved in png_charts/ subfolder
- Publication-ready quality
- All figures from HTML also as PNG

### Statistical Rigor
✅ **Multiple Testing Correction**:
- Benjamini-Hochberg FDR correction (α=0.05)
- Bonferroni correction (optional)
- Pairwise post-hoc tests with correction

✅ **Bootstrap Confidence Intervals**:
- 200-1000 resamples (configurable)
- Stratified sampling (preserves class balance)
- Percentile method (2.5% and 97.5%)
- Bias-corrected and accelerated (BCa) option

✅ **Effect Sizes**:
- Log-odds ratios (with pseudocount correction)
- Cramér's V (for categorical associations)
- Cohen's d (for continuous comparisons)
- Confidence intervals for all effect sizes

✅ **Model Validation**:
- Cross-validation (5-fold or 10-fold)
- Out-of-bag error (for Random Forest)
- Silhouette score (for clustering)
- Davies-Bouldin index (for clustering)
- Calinski-Harabasz score (for clustering)

### Binary Data Handling
✅ **Proper Treatment**:
- Validates data is strictly 0/1
- Uses both presence and absence in calculations
- Appropriate tests for categorical data
- No assumptions of normality
- Pseudocount correction to avoid infinities

✅ **Biological Interpretation**:
- 0 = absence is as informative as 1 = presence
- Pattern recognition (co-occurrence, mutual exclusivity)
- Cluster-specific enrichment/depletion
- Discriminative feature identification

---

## Deployment Options

### 1. Google Colab Notebooks (5 notebooks)
**Location**: `colab_notebooks/`

**Features**:
- No installation required
- One-click deployment
- File upload/download interface
- Free GPU access
- Automatic package installation
- Interactive parameter configuration
- Results packaging (ZIP download)

**Notebooks**:
1. Cluster_Analysis_Colab.ipynb
2. MDR_Analysis_Colab.ipynb
3. Network_Analysis_Colab.ipynb
4. Phylogenetic_Clustering_Colab.ipynb
5. StrepSuis_Analysis_Colab.ipynb

**Usage**: Click Colab badge → Upload data → Run all cells → Download results

---

### 2. Python Package with CLI
**Location**: `python_package/`

**Features**:
- Standard Python package structure
- Full command-line interface
- Python API for programmatic access
- Configuration file support (JSON/YAML)
- Entry points for all analyses
- pip installable

**Commands**:
```bash
mkrep-cluster      # K-Modes clustering
mkrep-mdr          # MDR analysis
mkrep-network      # Network analysis
mkrep-phylo        # Phylogenetic clustering
mkrep-strepsuis    # StrepSuis analysis
```

**Installation**:
```bash
cd python_package
pip install -e .
```

---

### 3. Hugging Face Demo with Voilà
**Location**: `huggingface_demo/`

**Features**:
- Interactive web dashboard
- Voilà-based interface
- ipywidgets for parameter control
- Drag-and-drop file upload
- Real-time analysis progress
- Results download
- Example datasets included

**Deployment**:
```bash
cd huggingface_demo
voila MKrep_Dashboard.ipynb --port 8866
```

Or deploy to Hugging Face Spaces

---

### 4. Standalone Scripts
**Location**: Root directory

**Features**:
- Direct Python execution
- Maximum flexibility
- Customizable parameters
- No package installation needed
- Suitable for HPC clusters

**Usage**:
```bash
python Cluster_MIC_AMR_Viruelnce.py
python MDR_2025_04_15.py
```

---

## Documentation

### Comprehensive Guides (6 documents)

1. **README.md** (Main documentation)
   - Quick start guide
   - Feature overview
   - Usage examples
   - Citation information

2. **INSTALLATION.md** (Installation guide)
   - Local installation (Windows, macOS, Linux)
   - Google Colab setup
   - Python package installation
   - Docker deployment
   - Troubleshooting guide

3. **BINARY_DATA_GUIDE.md** (Data format guide)
   - Binary data explanation
   - Statistical handling
   - Common pitfalls (and how to avoid them)
   - Data conversion examples
   - Validation checklist
   - Interpretation guide

4. **EXCEL_REPORTS_README.md** (Excel reports)
   - Report structure
   - Sheet descriptions
   - PNG chart handling
   - Troubleshooting

5. **EXCEL_REPORT_EXAMPLES.md** (Examples)
   - Real-world examples
   - Output samples
   - Interpretation tips

6. **FEATURES.md** (This document)
   - Complete feature list
   - Script comparisons
   - Deployment options
   - Statistical methods

### Additional Documentation

- `colab_notebooks/README.md` - Colab usage guide
- `python_package/README.md` - Package documentation
- `huggingface_demo/README.md` - Dashboard guide
- `validate.py` - Validation script with self-documentation

---

## Technical Specifications

### Data Requirements
- **Format**: CSV (comma-separated values)
- **Encoding**: UTF-8
- **Required column**: Strain_ID (first column)
- **Feature columns**: Binary (0 or 1) values only
- **Missing values**: Not allowed (encode as 0 or 1)
- **Minimum size**: 2 strains, 2 features
- **Recommended size**: 20+ strains, 10+ features

### Output Files
- **HTML**: Single-file reports with embedded CSS/JS
- **Excel**: Multi-sheet workbooks (.xlsx format)
- **PNG**: Lossless images (150-300 DPI)
- **CSV**: Intermediate results and data tables
- **Log**: analysis.log (debugging information)

### Performance
- **Small datasets** (< 100 strains): < 5 minutes
- **Medium datasets** (100-1000 strains): 5-30 minutes
- **Large datasets** (> 1000 strains): 30-120 minutes
- **Memory usage**: Typically < 4 GB RAM
- **CPU**: Multi-core support (automatic)
- **GPU**: Optional acceleration (Colab)

### Compatibility
- **Python**: 3.8, 3.9, 3.10, 3.11, 3.12
- **OS**: Windows, macOS, Linux
- **Browser**: Chrome, Firefox, Safari, Edge (for HTML reports)
- **Excel**: Microsoft Excel 2016+, LibreOffice Calc, Google Sheets

---

## Comparison Matrix

| Feature | Cluster | MDR | Network | Phylo | StrepSuis |
|---------|---------|-----|---------|-------|-----------|
| **Clustering** |||||
| K-Modes | ✓ | - | - | - | - |
| Tree-based | - | - | - | ✓ | ✓ |
| Ensemble | - | - | - | ✓ | ✓ |
| **Statistics** |||||
| Chi-square | ✓ | ✓ | ✓ | ✓ | ✓ |
| Fisher exact | ✓ | ✓ | ✓ | ✓ | ✓ |
| Log-odds | ✓ | ✓ | - | ✓ | ✓ |
| Bootstrap | ✓ | ✓ | - | ✓ | ✓ |
| **Methods** |||||
| MCA | ✓ | - | - | ✓ | ✓ |
| UMAP | - | - | - | ✓ | - |
| Random Forest | ✓ | - | - | ✓ | ✓ |
| Association rules | ✓ | ✓ | - | ✓ | ✓ |
| Network analysis | - | ✓ | ✓ | - | - |
| **Phylogenetics** |||||
| Tree parsing | - | - | - | ✓ | ✓ |
| Faith's PD | - | - | - | ✓ | - |
| Patristic distances | - | - | - | ✓ | ✓ |
| **Reports** |||||
| HTML | ✓ | ✓ | ✓ | ✓ | ✓ |
| Excel | ✓ | ✓ | ✓ | ✓ | ✓ |
| PNG charts | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Input** |||||
| CSV files | ✓ | ✓ | ✓ | ✓ | ✓ |
| Tree file | - | - | - | ✓ | ✓ |
| Binary data | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## Version Information

**Current Version**: 1.0.0  
**Release Date**: 2025-01-07  
**License**: MIT  
**Repository**: https://github.com/MK-vet/MKrep

---

## Citation

```bibtex
@software{mkrep2025,
  title = {MKrep: Comprehensive Bioinformatics Analysis Pipeline for Microbial Genomics},
  author = {MK-vet},
  year = {2025},
  url = {https://github.com/MK-vet/MKrep},
  version = {1.0.0},
  note = {Python scripts for phylogenetic clustering, AMR analysis, and network analysis}
}
```

---

**For support, issues, or contributions**: https://github.com/MK-vet/MKrep/issues
