# StrepSuis_Suite User Guide

**Complete guide for using StrepSuis_Suite analysis tools for *Streptococcus suis* genomics**

## Table of Contents

1. [Getting Started](#getting-started)
2. [Analysis Tools Overview](#analysis-tools-overview)
3. [Using the Voilà Dashboard](#using-the-voilà-dashboard)
4. [Using Standalone Scripts](#using-standalone-scripts)
5. [Understanding Reports](#understanding-reports)
6. [Reproducibility](#reproducibility)
7. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Prerequisites

- **Python 3.8 or higher**
- **4GB RAM minimum** (8GB recommended)
- **Basic understanding of CSV files**
- **Binary data format knowledge** (0 = absence, 1 = presence)

### Installation

#### Option 1: Quick Install (Recommended for beginners)
```bash
# Clone repository
git clone https://github.com/MK-vet/MKrep.git
cd MKrep

# Install dependencies
pip install -r requirements.txt
```

#### Option 2: Voilà Dashboard Only
```bash
# Install only dashboard dependencies
cd MKrep/huggingface_demo
pip install -r requirements.txt

# Launch dashboard
voila MKrep_Dashboard.ipynb --port 8866
```

---

## Analysis Tools Overview

StrepSuis_Suite provides **5 fully functional analysis modules**, each designed for specific genomic analysis tasks in *Streptococcus suis*:

### 1. StrepSuis-AMRVirKM (`Cluster_MIC_AMR_Viruelnce.py`)
**Purpose:** K-Modes Clustering of Antimicrobial Resistance and Virulence Profiles

**Best for:**
- Identifying strain groups based on resistance and virulence patterns
- Analyzing MIC, AMR genes, and virulence factor profiles
- Finding natural groupings in binary genomic data

**Key Features:**
- Automatic optimal cluster number selection
- Silhouette score optimization
- Multiple Correspondence Analysis (MCA)
- Bootstrap confidence intervals
- Feature importance ranking

**Required Files:**
- `MIC.csv` - Minimum inhibitory concentrations
- `AMR_genes.csv` - Antimicrobial resistance genes
- `Virulence.csv` - Virulence factors

**Typical Runtime:** 5-10 minutes

---

### 2. StrepSuis-AMRPat (`MDR_2025_04_15.py`)
**Purpose:** Automated Detection of Antimicrobial Resistance Patterns

**Best for:**
- Identifying multidrug resistant strains
- Analyzing co-resistance patterns across antibiotic classes
- Finding resistance gene associations
- Understanding antimicrobial resistance networks

**Key Features:**
- Customizable MDR threshold (default: 3 classes)
- Bootstrap prevalence estimation
- Association rule mining
- Hybrid network visualization
- Community detection

**Required Files:**
- `resistance_data.csv` - Combined resistance data

**Typical Runtime:** 10-15 minutes

---

### 3. StrepSuis-GenPhenNet (`Network_Analysis_2025_06_26.py`)
**Purpose:** Network-Based Integration of Genome–Phenome Data

**Best for:**
- Finding genomic-phenotypic feature correlations
- Identifying mutually exclusive genetic patterns
- Network community detection in genome-phenome associations
- Understanding complex feature relationships

**Key Features:**
- Chi-square and Fisher exact tests
- Information theory metrics (entropy, Cramér's V)
- 3D network visualization
- Hub identification
- Community structure analysis

**Required Files:**
- `MGE.csv` - Mobile genetic elements
- `MIC.csv` - Minimum inhibitory concentrations
- `MLST.csv` - Multi-locus sequence typing
- `Plasmid.csv` - Plasmid profiles
- `Serotype.csv` - Serotype data
- `Virulence.csv` - Virulence factors
- `AMR_genes.csv` - Antimicrobial resistance genes

**Typical Runtime:** 3-5 minutes

---

### 4. StrepSuis-PhyloTrait (`Phylgenetic_clustering_2025_03_21.py`)
**Purpose:** Integrated Phylogenetic and Binary Trait Analysis

**Best for:**
- Analyzing phylogenetic relationships with trait context
- Tree-aware clustering with evolutionary metrics
- Evolutionary metric calculation
- Trait-phylogeny associations

**Key Features:**
- Multiple clustering algorithms
- Faith's Phylogenetic Diversity
- UMAP dimensionality reduction
- Bootstrap validation
- Trait profiling

**Required Files:**
- `tree.newick` or `tree.nwk` - Phylogenetic tree
- `MIC.csv` - Minimum inhibitory concentrations
- `AMR_genes.csv` - Antimicrobial resistance genes
- `Virulence.csv` - Virulence factors

**Optional Files:**
- `MLST.csv` - Multi-locus sequence typing
- `Serotype.csv` - Serotype data

**Typical Runtime:** 15-30 minutes

---

### 5. StrepSuis-GenPhen (`StrepSuisPhyloCluster_2025_08_11.py`)
**Purpose:** An Interactive Platform for Integrated Genomic–Phenotypic Analysis

**Best for:**
- Comprehensive *Streptococcus suis* strain characterization
- Integrative phylogenetic-trait analysis
- Complete genomic-phenotypic profiling

**Key Features:**
- Ensemble clustering with fallback
- Chi-square trait associations
- Log-odds effect sizes
- Random Forest importance
- MCA visualization

**Required Files:**
- `tree.newick` - Phylogenetic tree
- `MIC.csv` - Minimum inhibitory concentrations
- `AMR_genes.csv` - Antimicrobial resistance genes
- `Virulence.csv` - Virulence factors

**Typical Runtime:** 10-20 minutes

---

## Using the Voilà Dashboard

The Voilà dashboard provides a **user-friendly interface** for all analyses without requiring programming knowledge.

### Step 1: Launch Dashboard

```bash
cd huggingface_demo
voila MKrep_Dashboard.ipynb --port 8866
```

Open your browser to: http://localhost:8866

### Step 2: Select Analysis Type

1. Click the **"Analysis Type"** dropdown
2. Choose your desired analysis
3. Read the description and required files list

### Step 3: Upload Data Files

1. Click **"Upload Files"** button
2. Select all required CSV files
3. Wait for validation messages
4. Green checkmarks (✓) indicate successful upload
5. Red X marks (✗) indicate errors - fix data and re-upload

### Step 4: Configure Parameters

**Common Parameters:**
- **Bootstrap Iterations:** Number of resampling iterations (default: 500)
  - Higher = more robust but slower
  - Range: 100-2000
  
- **FDR Alpha:** False discovery rate threshold (default: 0.05)
  - Lower = more stringent
  - Range: 0.01-0.10
  
- **Random Seed:** For reproducibility (default: 42)
  - Use same seed for identical results

**Analysis-Specific Parameters:**
- **Max Clusters:** Maximum clusters to test (Cluster Analysis)
- **MDR Threshold:** Number of classes for MDR classification (MDR Analysis)

### Step 5: Run Analysis

1. Click **"▶ Run Analysis"** button
2. Watch progress in real-time
3. Analysis runs in background
4. Completion indicated by green success box

### Step 6: Download Results

1. Click **"📄 Download HTML Report"** for interactive report
2. Click **"📊 Download Excel Report"** for data analysis
3. PNG charts are included in the reports
4. Save files to your computer

---

## Using Standalone Scripts

For advanced users or automated workflows, use standalone Python scripts directly.

### Basic Usage

```bash
# Navigate to repository
cd MKrep

# Run analysis script
python Cluster_MIC_AMR_Viruelnce.py
```

### Script Execution

1. **Ensure data files are in current directory** or update paths in script
2. **Run script:** `python [script_name].py`
3. **Wait for completion:** Progress shown in terminal
4. **Find outputs:** Check `output/` or specified output folder

### Output Structure

```
output/
├── [analysis]_report.html           # Interactive HTML report
├── [analysis]_Report_YYYYMMDD.xlsx  # Excel workbook
└── png_charts/                      # PNG visualizations
    ├── chart1.png
    ├── chart2.png
    └── ...
```

### Customizing Analysis

Edit configuration section at top of script:

```python
# Configuration
output_folder = "my_analysis_results"
bootstrap_iterations = 1000
fdr_alpha = 0.01
random_seed = 42
```

---

## Understanding Reports

All StrepSuis_Suite modules generate **consistent, professional reports** with the same structure and appearance.

### HTML Reports

**Features:**
- Interactive DataTables (sort, filter, search)
- Export buttons (CSV, Excel, PDF, Print)
- Plotly interactive visualizations
- Bootstrap 5 responsive design
- Collapsible sections
- Single-file format (embeds CSS/JS)

**Sections:**
1. **Summary:** Overview of analysis results
2. **Methodology:** Detailed methods and assumptions
3. **Results:** Statistical tests and visualizations
4. **Interpretation:** Biological and clinical interpretation
5. **Metadata:** Analysis parameters and provenance

**Using HTML Reports:**
- Open in any modern web browser
- Export tables using buttons above each table
- Hover over plots for interactive features
- Print entire report or specific sections
- Share as single HTML file

### Excel Reports

**Features:**
- Multi-sheet workbooks (5-20 sheets)
- Metadata sheet (configuration, parameters)
- Methodology sheet (detailed methods)
- Data sheets (all analysis results)
- Chart_Index sheet (PNG file list)
- Auto-formatted tables
- Proper numeric precision (4 decimals)

**Sections:**
1. **Metadata:** Analysis information
2. **Methodology:** Statistical methods
3. **[Data Sheets]:** Results tables
4. **Chart_Index:** List of PNG files

**Using Excel Reports:**
- Open in Excel, LibreOffice, or Google Sheets
- Sort, filter, and analyze data
- Create custom visualizations
- Combine with other data sources
- Share specific sheets with collaborators

### Interpretation Boxes

Each report includes **interpretation sections** that explain:
- **What the results mean**
- **Key findings**
- **Statistical significance**
- **Biological relevance**
- **Clinical implications**
- **Recommendations for next steps**

**Example Interpretation:**
```
📊 Interpretation

Summary: The clustering analysis identified 4 distinct groups with 
average silhouette score of 0.62, indicating good cluster quality.

Key Findings:
• Cluster 1 shows highest resistance to β-lactams (p < 0.001)
• 23 features significantly associated with clusters (FDR < 0.05)
• Bootstrap validation confirms 95% confidence in assignments

Recommendations:
• Focus on β-lactam resistance genes for Cluster 1 characterization
• Validate findings with independent dataset
• Consider biological context when interpreting differences
```

---

## Reproducibility

**StrepSuis_Suite ensures complete reproducibility** of all analyses.

### Key Features

1. **Fixed Random Seeds**
   - All random processes controlled by seed parameter
   - Default seed: 42
   - Change seed for different random realizations

2. **Parameter Documentation**
   - All parameters saved in metadata
   - Configuration logged in reports
   - Timestamp and version tracking

3. **Deterministic Algorithms**
   - Most algorithms are deterministic
   - Random processes use fixed seeds
   - Same inputs → Same outputs

### Reproducing Results

To replicate an analysis:

1. **Use same input data**
   - Identical CSV file contents
   - Same file names and structure

2. **Use same parameters**
   - Check metadata sheet in Excel report
   - Or methodology section in HTML report
   - Apply same parameter values

3. **Use same random seed**
   - Found in metadata
   - Set in configuration or dashboard

4. **Use same software versions**
   - Check requirements.txt
   - Install exact package versions if needed

### Example

```python
# From metadata sheet
Random Seed: 42
Bootstrap Iterations: 500
FDR Alpha: 0.05
Max Clusters: 8

# Reproduce by using same values
np.random.seed(42)
bootstrap_iterations = 500
fdr_alpha = 0.05
max_clusters = 8
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. "Module not found" Error

**Problem:** Missing Python packages

**Solution:**
```bash
pip install -r requirements.txt
```

#### 2. "Data is not strictly 0/1 binary" Error

**Problem:** Data contains non-binary values

**Solution:**
- Check for missing values (NaN)
- Verify all values are 0 or 1
- Convert data: `df = df.fillna(0).astype(int)`

#### 3. "Missing Strain_ID column" Error

**Problem:** CSV file lacks required column

**Solution:**
- Ensure first column is named "Strain_ID"
- Column name is case-sensitive
- Use exact spelling: "Strain_ID"

#### 4. Memory Error

**Problem:** Insufficient RAM

**Solution:**
- Reduce bootstrap iterations (e.g., 100 instead of 500)
- Filter low-variance features
- Use smaller dataset for testing
- Close other applications

#### 5. "Cannot save PNG" Error

**Problem:** Missing kaleido package

**Solution:**
```bash
pip install kaleido
```

#### 6. Voilà Dashboard Not Loading

**Problem:** Port already in use or installation issue

**Solution:**
```bash
# Try different port
voila MKrep_Dashboard.ipynb --port 8867

# Or reinstall voila
pip uninstall voila
pip install voila>=0.4.0
```

#### 7. Analysis Takes Too Long

**Problem:** Large dataset or high parameter values

**Solution:**
- Start with small dataset for testing
- Reduce bootstrap iterations
- Use fewer features (pre-filter)
- Check CPU usage (should be high during analysis)

#### 8. Excel File Won't Open

**Problem:** Corrupted file or missing openpyxl

**Solution:**
```bash
pip install openpyxl>=3.0.0
```

### Getting Help

If you encounter issues:

1. **Check this guide** - Most common issues covered
2. **Read error messages** - Often contain solution hints
3. **Validate data** - Run `python validate.py`
4. **GitHub Issues** - Report bugs at https://github.com/MK-vet/MKrep/issues
5. **Documentation** - See README files in repository

---

## Best Practices

### Data Preparation

1. **Clean data before analysis**
   - Remove duplicate strains
   - Handle missing values consistently
   - Verify binary format (0/1)

2. **Use descriptive feature names**
   - Clear column headers
   - Avoid special characters
   - Keep names reasonably short

3. **Document data provenance**
   - Keep notes on data source
   - Record any transformations
   - Track versions

### Analysis Workflow

1. **Start with small dataset**
   - Test with subset of data
   - Verify outputs look correct
   - Then run full analysis

2. **Use default parameters first**
   - Defaults are well-tested
   - Adjust only if needed
   - Document any changes

3. **Review results critically**
   - Check for biological plausibility
   - Compare with literature
   - Validate with independent data

4. **Save everything**
   - Keep input data files
   - Save all reports
   - Document analysis decisions

### Reporting Results

1. **Cite StrepSuis_Suite properly**
   - Include version number
   - Reference GitHub repository
   - See README for citation format

2. **Report parameters used**
   - Include in methods section
   - State random seed value
   - Note any non-default settings

3. **Share reproducibility information**
   - Provide data if possible
   - Share parameter values
   - Include software versions

---

## Quick Reference

### File Formats

| File Type | Format | Required Column | Other Columns |
|-----------|--------|-----------------|---------------|
| CSV | Comma-separated | Strain_ID | Binary (0/1) features |
| Newick | Phylogenetic tree | N/A | Standard format |

### Parameter Defaults

| Parameter | Default | Range | Purpose |
|-----------|---------|-------|---------|
| Bootstrap Iterations | 500 | 100-2000 | Confidence intervals |
| FDR Alpha | 0.05 | 0.01-0.10 | Multiple testing |
| Random Seed | 42 | Any integer | Reproducibility |
| Max Clusters | 8 | 2-15 | Clustering limit |
| MDR Threshold | 3 | 2-5 | MDR definition |

### Output Files

| File | Purpose | Format |
|------|---------|--------|
| `*_report.html` | Interactive report | HTML |
| `*_Report_*.xlsx` | Data analysis | Excel |
| `png_charts/*.png` | Visualizations | PNG |
| `*.log` | Execution log | Text |

---

## Support and Contact

- **GitHub Issues:** https://github.com/MK-vet/MKrep/issues
- **Documentation:** https://github.com/MK-vet/MKrep
- **Email:** See repository for contact information

---

**Last Updated:** 2025-01-15  
**Version:** 1.0.0  
**License:** MIT
