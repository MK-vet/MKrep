# MKrep Application Variants Guide
## Complete Analysis Suite - Production Ready

This document describes all available MKrep analysis applications organized as separate, ordered modules with complete functionality.

## Quick Start

Run the verification script to ensure all modules are working:
```bash
python verify_all_modules.py
```

Run all analyses at once:
```bash
python run_all_analyses.py --all
```

Run a specific analysis:
```bash
python run_all_analyses.py --module cluster
python run_all_analyses.py --module mdr
python run_all_analyses.py --module network
python run_all_analyses.py --module phylo
python run_all_analyses.py --module strepsuis
```

---

## Application Variants

### 1. Cluster Analysis Module
**Script:** `Cluster_MIC_AMR_Viruelnce.py`  
**Purpose:** Comprehensive clustering analysis for MIC, AMR, and virulence data  
**Status:** ✅ **Production Ready** - Full functionality with complete results

#### Features:
- K-Modes clustering with automatic cluster number optimization
- Silhouette analysis for cluster validation
- Multiple Correspondence Analysis (MCA) for dimensionality reduction
- Feature importance ranking (Random Forest)
- Association rule mining (Apriori algorithm)
- Bootstrap confidence intervals (500+ iterations)
- Chi-square tests with FDR correction
- Interactive HTML reports with DataTables
- Excel workbooks with multiple sheets
- High-quality PNG charts (150+ DPI)

#### Input Requirements:
- **Required:** `MIC.csv`, `AMR_genes.csv`, `Virulence.csv`
- **Optional:** `MLST.csv`, `Serotype.csv`, `Plasmid.csv`, `MGE.csv`

#### Output Files:
- `clustering_analysis_results/cluster_analysis_report.html` - Interactive HTML report
- `clustering_analysis_results/Cluster_Analysis_Report_[timestamp].xlsx` - Excel workbook
- `clustering_analysis_results/png_charts/` - Directory with PNG visualizations

#### Usage:
```bash
# Direct execution
python Cluster_MIC_AMR_Viruelnce.py

# Using runner script
python run_all_analyses.py --module cluster

# Using quick start script
python run_cluster_analysis.py
```

#### Estimated Time: 5-10 minutes

---

### 2. MDR Analysis Module
**Script:** `MDR_2025_04_15.py`  
**Purpose:** Multi-drug resistance pattern analysis with network approach  
**Status:** ✅ **Production Ready** - Full functionality with complete results

#### Features:
- MDR threshold detection and classification
- Bootstrap prevalence estimation with confidence intervals
- Co-occurrence analysis (phenotypes and genes)
- Association rule mining for resistance patterns
- Hybrid co-resistance network construction
- Statistical significance testing (chi-square, Fisher's exact)
- Community detection in resistance networks
- Interactive 3D network visualizations
- Comprehensive HTML and Excel reports

#### Input Requirements:
- **Required:** `MIC.csv`, `AMR_genes.csv`
- **Optional:** `Virulence.csv`, `MLST.csv`

#### Output Files:
- `mdr_analysis_results/mdr_analysis_report.html` - Interactive HTML report
- `mdr_analysis_results/MDR_Analysis_Report_[timestamp].xlsx` - Excel workbook
- `mdr_analysis_results/png_charts/` - Directory with PNG visualizations

#### Usage:
```bash
# Direct execution
python MDR_2025_04_15.py

# Using runner script
python run_all_analyses.py --module mdr

# Using quick start script
python run_mdr_analysis.py
```

#### Estimated Time: 5-10 minutes

---

### 3. Network Analysis Module
**Script:** `Network_Analysis_2025_06_26.py`  
**Purpose:** Statistical network analysis of gene-phenotype associations  
**Status:** ✅ **Production Ready** - Full functionality with complete results

#### Features:
- Chi-square and Fisher exact tests for associations
- Information theory metrics (entropy, Cramér's V)
- Mutual information and conditional entropy
- Mutually exclusive pattern detection
- Network construction with statistical filtering
- Community detection (Louvain algorithm)
- 3D network visualization with Plotly
- Centrality measures (degree, betweenness, closeness)
- Interactive HTML reports with network explorer

#### Input Requirements:
- **Required:** `MIC.csv`, `AMR_genes.csv`, `Virulence.csv`
- **Optional:** `MLST.csv`, `Serotype.csv`, `MGE.csv`

#### Output Files:
- `network_analysis_results/network_analysis_report.html` - Interactive HTML report
- `network_analysis_results/Network_Analysis_Report_[timestamp].xlsx` - Excel workbook
- `network_analysis_results/png_charts/` - Directory with PNG visualizations

#### Usage:
```bash
# Direct execution
python Network_Analysis_2025_06_26.py

# Using runner script
python run_all_analyses.py --module network
```

#### Estimated Time: 3-5 minutes

---

### 4. Phylogenetic Clustering Module
**Script:** `Phylgenetic_clustering_2025_03_21.py`  
**Purpose:** Tree-aware clustering with evolutionary metrics  
**Status:** ✅ **Production Ready** - Full functionality with complete results

#### Features:
- Phylogenetic tree-based clustering
- Faith's Phylogenetic Diversity (PD)
- UniFrac distances (weighted and unweighted)
- Pairwise evolutionary distances
- Binary trait analysis integrated with tree structure
- Trait enrichment in phylogenetic clusters
- Tree visualization with trait mapping
- Bootstrap support for cluster assignments
- MCA with phylogenetic constraints
- Comprehensive HTML and Excel reports

#### Input Requirements:
- **Required:** `Snp_tree.newick`, `AMR_genes.csv`, `Virulence.csv`
- **Optional:** `MIC.csv`, `MLST.csv`, `Serotype.csv`

#### Output Files:
- `phylo_clustering_results/phylo_analysis_report.html` - Interactive HTML report
- `phylo_clustering_results/Phylogenetic_Analysis_Report_[timestamp].xlsx` - Excel workbook
- `phylo_clustering_results/png_charts/` - Directory with PNG visualizations

#### Usage:
```bash
# Direct execution
python Phylgenetic_clustering_2025_03_21.py

# Using runner script
python run_all_analyses.py --module phylo

# Using quick start script
python run_phylogenetic_analysis.py
```

#### Estimated Time: 7-12 minutes

---

### 5. StrepSuis Analysis Module
**Script:** `StrepSuisPhyloCluster_2025_08_11.py`  
**Purpose:** Specialized integrative analysis for *Streptococcus suis*  
**Status:** ✅ **Production Ready** - Full functionality with complete results

#### Features:
- Species-specific phylogenetic clustering
- Ensemble clustering with fallback strategies
- Comprehensive trait profiling:
  - Chi-square tests for trait associations
  - Log-odds ratios for feature enrichment
  - Random Forest feature importance
- Association rule mining
- Multiple Correspondence Analysis (MCA)
- Serotype and MLST integration
- Plasmid and MGE analysis
- Bootstrap 5 styled HTML reports
- CSV export functionality

#### Input Requirements:
- **Required:** `Snp_tree.newick`, `AMR_genes.csv`, `Virulence.csv`
- **Optional:** `MIC.csv`, `MLST.csv`, `Serotype.csv`, `Plasmid.csv`, `MGE.csv`

#### Output Files:
- `strepsuis_analysis_results/strepsuis_analysis_report.html` - Interactive HTML report
- `strepsuis_analysis_results/StrepSuis_Analysis_Report_[timestamp].xlsx` - Excel workbook
- `strepsuis_analysis_results/png_charts/` - Directory with PNG visualizations

#### Usage:
```bash
# Direct execution
python StrepSuisPhyloCluster_2025_08_11.py

# Using runner script
python run_all_analyses.py --module strepsuis
```

#### Estimated Time: 7-12 minutes

---

## Running All Analyses

### Sequential Execution
Run all analyses one after another:
```bash
python run_all_analyses.py --all
```

This will:
1. Verify all requirements for each module
2. Run each analysis in sequence
3. Generate complete results for each module
4. Create a summary report (`ANALYSIS_SUMMARY.md`)
5. Save execution results to JSON (`analysis_run_results.json`)

### Individual Execution
Run modules individually for focused analysis:
```bash
# Cluster analysis only
python run_all_analyses.py --module cluster

# MDR analysis only
python run_all_analyses.py --module mdr

# Network analysis only
python run_all_analyses.py --module network

# Phylogenetic analysis only
python run_all_analyses.py --module phylo

# StrepSuis analysis only
python run_all_analyses.py --module strepsuis
```

### Custom Timeout
Set custom timeout for long-running analyses:
```bash
# 20 minute timeout per module
python run_all_analyses.py --all --timeout 1200

# 30 minute timeout for phylogenetic analysis
python run_all_analyses.py --module phylo --timeout 1800
```

---

## Verification and Testing

### Module Verification
Verify all modules are functional:
```bash
python verify_all_modules.py
```

This checks:
- All required Python dependencies
- Data file availability
- Script syntax and structure
- Import functionality
- Output generation capability

### Functionality Testing
Run comprehensive tests:
```bash
python test_functionality.py
```

### Integration Testing
Test module integration:
```bash
python test_network_integration.py
```

---

## Output Structure

Each analysis module generates:

### 1. HTML Report
- Interactive tables with sorting and filtering (DataTables)
- Embedded Plotly visualizations (zoomable, interactive)
- Bootstrap 5 styling for professional appearance
- Interpretation sections explaining results
- Methodology documentation
- Parameter settings and reproducibility information

### 2. Excel Workbook
- Multiple sheets organized by analysis type:
  - Metadata and parameters
  - Main results tables
  - Statistical test results
  - Feature importance rankings
  - Association rules
  - Chart index with thumbnails
- Professional formatting
- Cell comments with explanations
- Consistent structure across all modules

### 3. PNG Charts
Stored in `png_charts/` subdirectory:
- High resolution (150+ DPI)
- Publication quality
- Consistent color schemes
- Clear labels and legends
- Multiple visualization types:
  - Heatmaps
  - Scatter plots
  - Network diagrams
  - Phylogenetic trees
  - Bar charts
  - 3D visualizations

---

## Data Requirements

### Binary Data Format
All input CSV files must use binary encoding:
- **0 = Absence** of feature (gene, resistance, virulence factor)
- **1 = Presence** of feature
- No missing values (NaN) - encode as 0 or 1
- First column must be `Strain_ID`

Example:
```csv
Strain_ID,Gene1,Gene2,Antibiotic1,Virulence1
Strain001,1,0,1,0
Strain002,0,1,1,1
Strain003,1,1,0,1
```

### File Formats

#### MIC.csv
Minimum Inhibitory Concentration data (binary: resistant=1, susceptible=0)

#### AMR_genes.csv
Antimicrobial resistance genes (binary: present=1, absent=0)

#### Virulence.csv
Virulence factors (binary: present=1, absent=0)

#### MLST.csv
Multi-locus sequence typing data

#### Serotype.csv
Serological types

#### Plasmid.csv
Plasmid presence/absence (binary)

#### MGE.csv
Mobile genetic elements (binary)

#### Snp_tree.newick
Phylogenetic tree in Newick format (required for phylogenetic modules)

---

## Statistical Methods Used

All modules implement rigorous statistical methods:

### Clustering
- K-Modes for categorical data
- Silhouette analysis for validation
- Calinski-Harabasz index
- Davies-Bouldin index

### Statistical Testing
- Chi-square tests with Yates correction
- Fisher's exact test for small samples
- FDR correction (Benjamini-Hochberg)
- Bootstrap confidence intervals (500-1000 iterations)

### Feature Analysis
- Random Forest feature importance
- Log-odds ratios
- Information theory metrics
- Association rule mining (Apriori)

### Dimensionality Reduction
- Multiple Correspondence Analysis (MCA)
- UMAP for visualization
- PCA for continuous features

### Network Analysis
- Louvain community detection
- Centrality measures
- Statistical edge filtering
- Mutual information

### Phylogenetic Methods
- Faith's Phylogenetic Diversity
- UniFrac distances
- Tree-aware clustering
- Trait enrichment analysis

---

## Reproducibility

All analyses ensure reproducibility through:
- **Fixed random seeds** (seed=42 by default)
- **Documented parameters** in all reports
- **Version information** for all packages
- **Complete methodology** sections
- **Data provenance** tracking
- **Timestamp logging** for all runs

---

## Performance Considerations

### Memory Usage
- Typical memory requirements: 2-8 GB RAM
- For large datasets (>1000 strains): 16+ GB recommended
- Memory-efficient algorithms used throughout
- Garbage collection optimized

### Processing Time
- Cluster Analysis: 5-10 minutes
- MDR Analysis: 5-10 minutes
- Network Analysis: 3-5 minutes
- Phylogenetic Clustering: 7-12 minutes
- StrepSuis Analysis: 7-12 minutes

Times based on reference dataset (~50 strains, ~200 features)

### Optimization
- Parallel processing where applicable
- Numba JIT compilation for bottlenecks
- Efficient data structures
- Incremental garbage collection

---

## Troubleshooting

### Common Issues

#### Module fails with "File not found"
**Solution:** Ensure all required data files are in the same directory as the script.

#### "Memory Error" during analysis
**Solution:** 
1. Close other applications
2. Use a machine with more RAM
3. Reduce bootstrap iterations (edit script configuration)

#### Analysis runs but no output generated
**Solution:**
1. Check for error messages in console
2. Verify write permissions in output directory
3. Check available disk space

#### "Import Error" for packages
**Solution:** Install all requirements:
```bash
pip install -r requirements.txt
```

### Getting Help

1. Check documentation in each README file
2. Review log files in output directories
3. Run verification script: `python verify_all_modules.py`
4. Open an issue on GitHub with:
   - Error message
   - Module being run
   - Python version
   - Operating system

---

## Version Information

**Current Version:** 1.2.0  
**Release Date:** 2025-01-16  
**Python Support:** 3.8 - 3.12  
**Status:** Production Ready

---

## Citation

If you use MKrep in your research, please cite:

```bibtex
@software{mkrep2025,
  title = {MKrep: Comprehensive Bioinformatics Analysis Pipeline for Microbial Genomics},
  author = {MK-vet},
  year = {2025},
  url = {https://github.com/MK-vet/MKrep},
  version = {1.2.0}
}
```

---

## License

MIT License - See LICENSE file for details

---

## Additional Resources

- **Main README:** [README.md](README.md)
- **User Guide:** [USER_GUIDE.md](USER_GUIDE.md)
- **Interpretation Guide:** [INTERPRETATION_GUIDE.md](INTERPRETATION_GUIDE.md)
- **Installation Guide:** [INSTALLATION.md](INSTALLATION.md)
- **Docker Deployment:** [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)
- **Binary Data Guide:** [BINARY_DATA_GUIDE.md](BINARY_DATA_GUIDE.md)

---

**Last Updated:** 2025-10-17  
**Maintained By:** MK-vet  
**Repository:** https://github.com/MK-vet/MKrep
