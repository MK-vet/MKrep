# Complete Analysis Workflow Guide
## Running MKrep as a Complete Bioinformatics Suite

This guide demonstrates how to run all MKrep analysis modules as a coordinated, complete bioinformatics analysis pipeline. Each module is a standalone, production-ready application that generates complete results.

---

## Quick Start - Complete Analysis

### Step 1: Verify System is Ready
```bash
# Check all modules are functional
python verify_all_modules.py
```

Expected output:
```
✅ ALL MODULES VERIFIED SUCCESSFULLY!
- 5 modules verified
- All dependencies installed
- All data files present
```

### Step 2: Run Complete Analysis Suite
```bash
# Run all analyses sequentially
python run_all_analyses.py --all
```

This will execute:
1. Cluster Analysis (5-10 minutes)
2. MDR Analysis (5-10 minutes)
3. Network Analysis (3-5 minutes)
4. Phylogenetic Clustering (7-12 minutes)
5. StrepSuis Analysis (7-12 minutes)

**Total time:** ~30-50 minutes

### Step 3: Review Results
Each module generates its own output folder:
- `clustering_analysis_results/`
- `mdr_analysis_results/`
- `network_analysis_results/`
- `phylo_clustering_results/`
- `strepsuis_analysis_results/`

---

## Module Execution Order

### Recommended Order for Comprehensive Analysis:

#### 1. Start with Basic Characterization
```bash
# Cluster Analysis - Understand basic groupings
python run_all_analyses.py --module cluster
```
**Output:** Strain clusters, trait profiles, feature importance

#### 2. Analyze Resistance Patterns
```bash
# MDR Analysis - Multi-drug resistance patterns
python run_all_analyses.py --module mdr
```
**Output:** MDR classification, co-resistance networks, gene-phenotype associations

#### 3. Explore Feature Networks
```bash
# Network Analysis - Gene-phenotype associations
python run_all_analyses.py --module network
```
**Output:** Association networks, community detection, hub identification

#### 4. Add Phylogenetic Context
```bash
# Phylogenetic Clustering - Evolutionary relationships
python run_all_analyses.py --module phylo
```
**Output:** Tree-aware clusters, phylogenetic diversity, trait evolution

#### 5. Species-Specific Deep Dive (if applicable)
```bash
# StrepSuis Analysis - Specialized for S. suis
python run_all_analyses.py --module strepsuis
```
**Output:** Serotype analysis, MLST integration, mobile elements

---

## Alternative Workflows

### Workflow A: Resistance-Focused Analysis
For studies focused on antimicrobial resistance:

```bash
# 1. MDR patterns
python run_all_analyses.py --module mdr

# 2. Gene-phenotype networks
python run_all_analyses.py --module network

# 3. Phylogenetic context
python run_all_analyses.py --module phylo
```

### Workflow B: Epidemiological Analysis
For population structure and epidemiology:

```bash
# 1. Population clusters
python run_all_analyses.py --module cluster

# 2. Phylogenetic structure
python run_all_analyses.py --module phylo

# 3. Species-specific analysis
python run_all_analyses.py --module strepsuis
```

### Workflow C: Quick Exploration
For rapid initial assessment:

```bash
# 1. Basic clustering
python run_all_analyses.py --module cluster

# 2. Network overview
python run_all_analyses.py --module network
```

---

## Integration of Results

### Cross-Module Analysis Strategy

Results from different modules complement each other:

#### 1. Cluster Analysis Results → MDR Analysis
- Use identified clusters to stratify MDR analysis
- Compare resistance patterns across clusters
- Identify cluster-specific MDR phenotypes

#### 2. MDR Analysis → Network Analysis
- Focus network analysis on MDR-associated genes
- Validate co-resistance patterns
- Explore mechanistic associations

#### 3. Network Analysis → Phylogenetic Analysis
- Test if network communities align with phylogeny
- Identify phylogenetic signal in associations
- Map network hubs onto tree

#### 4. Phylogenetic Analysis → StrepSuis Analysis
- Integrate serotype with phylogenetic clusters
- Map MLST to evolutionary relationships
- Analyze mobile elements in phylogenetic context

### Example Integration Workflow:

```bash
# Step 1: Generate all results
python run_all_analyses.py --all

# Step 2: Manual integration (cross-reference outputs)
# - Compare cluster assignments across methods
# - Overlay MDR classification on phylogenetic tree
# - Validate network communities with clusters
# - Integrate serotype/MLST data

# Step 3: Synthesis
# - Create integrated visualizations
# - Write comparative analysis
# - Draw comprehensive conclusions
```

---

## Batch Processing Multiple Datasets

### Processing Multiple Studies:

Create a script to process multiple datasets:

```bash
#!/bin/bash
# process_multiple_datasets.sh

DATASETS=("dataset1" "dataset2" "dataset3")

for dataset in "${DATASETS[@]}"; do
    echo "Processing $dataset..."
    
    # Set up dataset-specific directory
    cd "$dataset"
    
    # Run all analyses
    python ../run_all_analyses.py --all
    
    # Move to next dataset
    cd ..
done

echo "All datasets processed!"
```

---

## Parallel Execution

For multiple independent datasets:

```bash
# Run different modules in parallel (different terminals)
# Terminal 1:
python run_all_analyses.py --module cluster

# Terminal 2:
python run_all_analyses.py --module mdr

# Terminal 3:
python run_all_analyses.py --module network
```

**Note:** Ensure sufficient RAM for parallel execution (8-16 GB recommended)

---

## Output Organization

### Recommended Directory Structure:

```
project_directory/
├── data/
│   ├── MIC.csv
│   ├── AMR_genes.csv
│   ├── Virulence.csv
│   ├── MLST.csv
│   ├── Serotype.csv
│   ├── Plasmid.csv
│   ├── MGE.csv
│   └── Snp_tree.newick
│
├── results/
│   ├── clustering_analysis_results/
│   │   ├── cluster_analysis_report.html
│   │   ├── Cluster_Analysis_Report_[timestamp].xlsx
│   │   └── png_charts/
│   │
│   ├── mdr_analysis_results/
│   │   ├── mdr_analysis_report.html
│   │   ├── MDR_Analysis_Report_[timestamp].xlsx
│   │   └── png_charts/
│   │
│   ├── network_analysis_results/
│   │   ├── network_analysis_report.html
│   │   ├── Network_Analysis_Report_[timestamp].xlsx
│   │   └── png_charts/
│   │
│   ├── phylo_clustering_results/
│   │   ├── phylo_analysis_report.html
│   │   ├── Phylogenetic_Analysis_Report_[timestamp].xlsx
│   │   └── png_charts/
│   │
│   └── strepsuis_analysis_results/
│       ├── strepsuis_analysis_report.html
│       ├── StrepSuis_Analysis_Report_[timestamp].xlsx
│       └── png_charts/
│
├── logs/
│   ├── analysis_run_results.json
│   ├── module_verification_report.json
│   └── ANALYSIS_SUMMARY.md
│
└── scripts/
    ├── verify_all_modules.py
    └── run_all_analyses.py
```

---

## Quality Control Checklist

Before considering analysis complete:

### ✅ Pre-Analysis Checks:
- [ ] All required data files present
- [ ] Data files in correct format (binary: 0/1)
- [ ] No missing Strain_ID columns
- [ ] Tree file valid (for phylogenetic modules)
- [ ] All dependencies installed

### ✅ During Analysis:
- [ ] Monitor for error messages
- [ ] Check progress output
- [ ] Verify sufficient disk space
- [ ] Monitor memory usage

### ✅ Post-Analysis Validation:
- [ ] All HTML reports generated
- [ ] All Excel files created
- [ ] PNG charts folder populated
- [ ] No error logs in output
- [ ] Results make biological sense

### ✅ Results Review:
- [ ] Sample sizes reasonable
- [ ] Statistical significance assessed
- [ ] Confidence intervals checked
- [ ] Visualizations clear and informative
- [ ] Interpretation sections reviewed

---

## Troubleshooting

### Issue: Module fails to run
**Solutions:**
1. Run `python verify_all_modules.py` to diagnose
2. Check data files are present and correctly formatted
3. Verify dependencies: `pip install -r requirements.txt`
4. Check available memory (minimum 4 GB recommended)

### Issue: Analysis runs but produces no output
**Solutions:**
1. Check console for error messages
2. Verify write permissions in output directory
3. Ensure sufficient disk space (minimum 1 GB free)
4. Review log files in output directories

### Issue: Different results on repeated runs
**Solutions:**
1. Verify random seed is set (default: 42)
2. Check if data files have changed
3. Ensure same Python version used
4. Verify package versions match

### Issue: Memory error during analysis
**Solutions:**
1. Close other applications
2. Reduce dataset size (subset samples)
3. Run modules individually rather than all at once
4. Use machine with more RAM (16 GB recommended for large datasets)

---

## Performance Optimization

### For Large Datasets (>500 strains):

#### 1. Increase Timeouts:
```bash
python run_all_analyses.py --all --timeout 3600  # 1 hour per module
```

#### 2. Reduce Bootstrap Iterations:
Edit configuration in scripts:
```python
bootstrap_iterations = 100  # Reduce from default 500
```

#### 3. Use Sampling:
For initial exploration, use a representative subset:
```python
# Randomly sample 200 strains
sampled_data = data.sample(n=200, random_state=42)
```

### For Small Datasets (<20 strains):

#### 1. Use Fisher's Exact Test:
Appropriate for small samples (automatically used when expected counts < 5)

#### 2. Interpret with Caution:
- Wider confidence intervals expected
- Lower statistical power
- Focus on effect sizes rather than p-values

#### 3. Reduce Cluster Numbers:
```python
max_clusters = 3  # Instead of default 8
```

---

## Publication-Ready Outputs

All modules generate publication-ready materials:

### For Methods Section:
- Detailed methodology in HTML reports
- Statistical methods documented
- Software versions logged
- Parameters recorded

### For Results Section:
- Publication-quality figures (PNG, 150+ DPI)
- Statistical results tables (Excel)
- Interactive visualizations (HTML)
- Comprehensive datasets

### For Supplementary Materials:
- Complete Excel workbooks
- All statistical test results
- Raw data tables
- Interactive HTML reports

---

## Citation and References

### Citing MKrep:
```bibtex
@software{mkrep2025,
  title = {MKrep: Comprehensive Bioinformatics Analysis Pipeline for Microbial Genomics},
  author = {MK-vet},
  year = {2025},
  url = {https://github.com/MK-vet/MKrep},
  version = {1.2.0}
}
```

### Statistical Methods to Cite:
- **K-Modes:** Huang, Z. (1998). Extensions to the k-means algorithm
- **MCA:** Greenacre, M. (2007). Correspondence Analysis in Practice
- **Louvain:** Blondel, V. D., et al. (2008). Fast unfolding of communities
- **Apriori:** Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules
- **UniFrac:** Lozupone, C., & Knight, R. (2005). UniFrac distance metric
- **Faith's PD:** Faith, D. P. (1992). Conservation evaluation and phylogenetic diversity

---

## Advanced Usage

### Custom Analysis Pipeline:

Create a custom Python script to chain analyses:

```python
#!/usr/bin/env python3
"""Custom analysis pipeline"""

import subprocess
import sys

def run_module(module_name):
    """Run a single analysis module"""
    result = subprocess.run(
        [sys.executable, 'run_all_analyses.py', '--module', module_name],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

# Custom workflow
modules = ['cluster', 'mdr', 'network']

for module in modules:
    print(f"Running {module}...")
    if not run_module(module):
        print(f"Error in {module}, stopping pipeline")
        sys.exit(1)

print("Custom pipeline complete!")
```

### Automated Reporting:

Generate summary across all modules:

```python
import pandas as pd
import glob

# Collect key results from all modules
summary = {}

for excel_file in glob.glob('*/*.xlsx'):
    module = excel_file.split('/')[0]
    # Extract key metrics
    # ... processing code ...
    summary[module] = metrics

# Create integrated report
summary_df = pd.DataFrame(summary)
summary_df.to_excel('integrated_summary.xlsx')
```

---

## Best Practices

### 1. Always Start with Verification
```bash
python verify_all_modules.py
```

### 2. Use Version Control
```bash
git init
git add data/ results/
git commit -m "Analysis results for study X"
```

### 3. Document Parameters
Keep a record of analysis parameters and date:
```bash
echo "Analysis run: $(date)" > analysis_log.txt
python run_all_analyses.py --all 2>&1 | tee -a analysis_log.txt
```

### 4. Backup Results
```bash
# Create timestamped backup
tar -czf results_$(date +%Y%m%d).tar.gz *_results/
```

### 5. Validate Results
- Check for biological plausibility
- Compare with literature
- Discuss with domain experts
- Perform sensitivity analyses

---

## Support and Resources

### Getting Help:
1. **Documentation:** See all guides in repository
2. **Issues:** GitHub Issues page
3. **Email:** Contact repository maintainers

### Additional Resources:
- [USER_GUIDE.md](USER_GUIDE.md) - Detailed user guide
- [INTERPRETATION_GUIDE.md](INTERPRETATION_GUIDE.md) - Results interpretation
- [APPLICATION_VARIANTS_GUIDE.md](APPLICATION_VARIANTS_GUIDE.md) - Module details
- [EXAMPLE_RESULTS.md](EXAMPLE_RESULTS.md) - Expected outputs

---

## Version History

**Version 1.2.0** (Current)
- Module verification script
- Unified analysis runner
- Comprehensive documentation
- Production-ready status

**Version 1.1.0**
- Standardized reports
- Excel export for all modules
- Interpretation guides

**Version 1.0.0**
- Initial public release
- Five analysis modules
- Complete functionality

---

**Last Updated:** 2025-10-17  
**Status:** Production Ready  
**Maintained By:** MK-vet  
**License:** MIT
