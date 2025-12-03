# User Guide for StrepSuis Analyzer

General-purpose genomic data analysis tool for clustering and trait association analysis

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
  - [Method 1: Python Package](#method-1-python-package)
  - [Method 2: Docker Container](#method-2-docker-container)
  - [Method 3: Google Colab](#method-3-google-colab)
- [Quick Start](#quick-start)
- [Detailed Usage](#detailed-usage)
- [Input Data Format](#input-data-format)
- [Output Files](#output-files)
- [Examples](#examples)
- [Advanced Options](#advanced-options)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

## Introduction

StrepSuis Analyzer is a flexible, user-friendly tool for analyzing genomic data without requiring programming expertise. It performs clustering, statistical association analysis, and generates interactive visualizations.

### Who Should Use This Tool?

- **Researchers** who want to analyze their own genomic data
- **Microbiologists** studying bacterial traits and patterns
- **Students** learning data analysis for genomics
- **Anyone** with binary trait data (AMR, virulence, etc.)

### What You Need

- Binary trait data in CSV format (0/1 values)
- Optional: Phylogenetic tree in Newick format
- Python 3.8+ OR Docker OR Google account (for Colab)

### Key Features

✨ **Bring Your Own Data** - Analyze any binary trait dataset  
📊 **Automatic Clustering** - Hierarchical clustering with optimal cluster selection  
📈 **Statistical Analysis** - Chi-square tests with FDR correction  
🎨 **Interactive Reports** - HTML reports with Plotly visualizations  
📑 **Excel Export** - Multi-sheet workbooks for easy sharing  
🌳 **Phylogenetic Integration** - Optional tree-based analysis  
🔄 **Reproducible** - Fixed random seeds for deterministic results  

## Installation

Choose ONE of the three installation methods below.

### Method 1: Python Package

**Best for:** Users comfortable with Python and command-line tools

**Requirements:**
- Python 3.8 or higher
- pip package manager
- 4GB RAM minimum

**Steps:**

1. Clone the repository:
   ```bash
   git clone https://github.com/MK-vet/MKrep.git
   cd MKrep/separated_repos/strepsuis-analyzer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Verify installation:
   ```bash
   python StrepSuisPhyloCluster_2025_08_11.py --help
   ```

### Method 2: Docker Container

**Best for:** Users who want a consistent environment across systems

**Requirements:**
- Docker installed on your system
- Basic knowledge of Docker commands

**Steps:**

1. Clone the repository:
   ```bash
   git clone https://github.com/MK-vet/MKrep.git
   cd MKrep/separated_repos/strepsuis-analyzer
   ```

2. Build the Docker image:
   ```bash
   docker build -t strepsuis-analyzer:latest .
   ```

3. Test the container:
   ```bash
   docker run --rm strepsuis-analyzer:latest --help
   ```

4. Run with your data:
   ```bash
   docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
       strepsuis-analyzer:latest --data /data/Virulence.csv --output /output
   ```

### Method 3: Google Colab

**Best for:** Users who want to run analysis without installing anything

**Requirements:**
- Google account
- Web browser
- Internet connection

**Steps:**

1. Open the Colab notebook: [Link to be added]

2. Follow the instructions in the notebook:
   - Run the first cell to install the package
   - Upload your data files when prompted
   - Configure parameters
   - Run the analysis
   - Download results

## Quick Start

### Basic Analysis

```bash
# Navigate to strepsuis-analyzer directory
cd MKrep/separated_repos/strepsuis-analyzer

# Run with example data
python StrepSuisPhyloCluster_2025_08_11.py --data data/Virulence.csv

# Run with your own data
python StrepSuisPhyloCluster_2025_08_11.py --data your_data.csv
```

### With Multiple Data Files

```bash
# Merge multiple CSV files
python StrepSuisPhyloCluster_2025_08_11.py \
  --data your_amr.csv your_virulence.csv
```

### With Phylogenetic Tree

```bash
# Include phylogenetic analysis
python StrepSuisPhyloCluster_2025_08_11.py \
  --data your_data.csv \
  --tree your_tree.newick
```

### Specify Number of Clusters

```bash
# Set specific number of clusters
python StrepSuisPhyloCluster_2025_08_11.py \
  --data your_data.csv \
  --clusters 4
```

## Detailed Usage

### Command-Line Options

```
python StrepSuisPhyloCluster_2025_08_11.py [OPTIONS]

Options:
  --data FILES [FILES ...]   CSV data files (required)
  --tree FILE                Phylogenetic tree file in Newick format (optional)
  --output DIR               Output directory (default: output)
  --clusters INT             Number of clusters (default: auto-determined)
  --seed INT                 Random seed for reproducibility (default: 42)
  -h, --help                 Show help message and exit
```

### Parameter Details

**--data**
- One or more CSV files with binary trait data
- Files will be merged on 'Strain_ID' column
- Example: `--data amr.csv virulence.csv`

**--tree** (optional)
- Phylogenetic tree in Newick format
- Enables phylogenetic distance calculations
- Example: `--tree phylogeny.newick`

**--output**
- Directory for output files
- Created automatically if doesn't exist
- Example: `--output results_2025`

**--clusters** (optional)
- Number of clusters to create
- If not specified, determined by silhouette score
- Range: 2 to n_strains/2
- Example: `--clusters 5`

**--seed**
- Random seed for reproducibility
- Ensures same results with same input
- Example: `--seed 123`

## Input Data Format

### CSV Data Files

Your data files must follow this format:

```csv
Strain_ID,Gene1,Gene2,Gene3,Gene4
Strain001,1,0,1,1
Strain002,0,1,1,0
Strain003,1,1,0,1
```

**Requirements:**
- **First column**: Must be named 'Strain_ID' (or similar identifier)
- **Other columns**: Your features (genes, traits, etc.)
- **Values**: Binary (0 = absence, 1 = presence)
- **Missing values**: Treated as 0 (absence)
- **Format**: CSV with comma separator

### Multiple Files

When providing multiple CSV files:
- All files must have the same 'Strain_ID' column
- Files are merged on 'Strain_ID'
- Only strains present in ALL files are included
- Feature columns are combined

Example:
```bash
# amr.csv: Strain_ID, Gene1, Gene2
# vir.csv: Strain_ID, Gene3, Gene4
# Result: Strain_ID, Gene1, Gene2, Gene3, Gene4
```

### Phylogenetic Tree (Optional)

If providing a tree file:
- Format: Newick (.newick, .nwk, .tree)
- Tip labels must match Strain_IDs in data
- Can be rooted or unrooted
- Branch lengths optional but recommended

Example Newick:
```
((Strain001:0.1,Strain002:0.15):0.2,(Strain003:0.12,Strain004:0.18):0.25);
```

## Output Files

The analysis generates three types of output:

### 1. Interactive HTML Report
**File**: `analysis_report.html`

- Open in any web browser
- Interactive Plotly visualizations
- Responsive Bootstrap 5 design
- Contains:
  - Dataset overview
  - Cluster distribution plot
  - MCA biplot (2D visualization)
  - Top significant trait associations
  - Links to download CSV/Excel files

### 2. Excel Workbook
**File**: `analysis_results.xlsx`

Multiple sheets:
- **Clustered_Data**: Complete dataset with cluster assignments
- **Cluster_Summary**: Size and statistics for each cluster
- **Trait_Associations**: Statistical results (p-values, effect sizes)
- **Metadata**: Analysis parameters and run information

### 3. CSV Files

**clustered_data.csv**
- Dataset with cluster assignments
- Same as Clustered_Data Excel sheet
- Easy import to other tools

**trait_associations.csv**
- Statistical association results
- Includes p-values and FDR-adjusted p-values
- Sorted by significance

## Examples

### Example 1: Basic Analysis

```bash
# Use included example data
python StrepSuisPhyloCluster_2025_08_11.py --data data/Virulence.csv
```

**What it does:**
- Loads virulence factor data
- Automatically determines optimal number of clusters
- Performs statistical tests
- Generates reports in `output/` directory

### Example 2: Custom Cluster Number

```bash
# Specify 3 clusters
python StrepSuisPhyloCluster_2025_08_11.py \
  --data data/Virulence.csv \
  --clusters 3 \
  --output results_k3
```

**What it does:**
- Creates exactly 3 clusters
- Saves results in `results_k3/` directory

### Example 3: Multiple Data Files

```bash
# Combine AMR and virulence data (example)
python StrepSuisPhyloCluster_2025_08_11.py \
  --data data/Virulence.csv data/Virulence.csv \
  --output combined_analysis
```

### Example 4: With Phylogenetic Tree

```bash
# Include phylogenetic analysis (when tree available)
python StrepSuisPhyloCluster_2025_08_11.py \
  --data data/Virulence.csv \
  --tree path/to/tree.newick \
  --output phylo_analysis
```

### Example 5: Docker Usage

```bash
# Run in Docker with data mounting
docker run -v $(pwd)/data:/data -v $(pwd)/results:/output \
  strepsuis-analyzer:latest \
  --data /data/Virulence.csv \
  --output /output \
  --clusters 4
```

## Advanced Options

### Reproducibility

All analyses are reproducible by default (seed=42). To use different seed:

```bash
python StrepSuisPhyloCluster_2025_08_11.py \
  --data your_data.csv \
  --seed 12345
```

### Large Datasets

For datasets with >500 strains or >1000 features:

1. **Increase memory**: Ensure 8GB+ RAM available
2. **Use Docker**: Better resource management
3. **Subsample**: Consider analyzing subset first

### Batch Processing

Process multiple datasets:

```bash
#!/bin/bash
for file in data/*.csv; do
    basename=$(basename "$file" .csv)
    python StrepSuisPhyloCluster_2025_08_11.py \
        --data "$file" \
        --output "results_${basename}"
done
```

## Troubleshooting

### Common Issues

**Issue**: "No module named 'pandas'"  
**Solution**: Install dependencies: `pip install -r requirements.txt`

**Issue**: "Strain_ID column not found"  
**Solution**: Ensure first column is named 'Strain_ID' in your CSV

**Issue**: "Not enough data points for clustering"  
**Solution**: Need at least 3 strains in your dataset

**Issue**: "Tree tips don't match strain IDs"  
**Solution**: Ensure tree tip labels exactly match Strain_ID values

**Issue**: "Memory error with large dataset"  
**Solution**: Try Docker or reduce dataset size

### Getting Help

1. Check this USER_GUIDE.md
2. Review TESTING.md for test examples
3. Open issue on GitHub
4. Check README.md for quick reference

## FAQ

**Q: What kind of data can I analyze?**  
A: Any binary trait data (0/1 values). Common examples: AMR genes, virulence factors, metabolic pathways.

**Q: How many strains do I need?**  
A: Minimum 3, but 20+ recommended for meaningful statistical analysis.

**Q: Do I need a phylogenetic tree?**  
A: No, it's optional. Tree adds phylogenetic context but not required.

**Q: How are clusters determined?**  
A: By default, using silhouette score to find optimal number. You can override with --clusters.

**Q: What statistical test is used?**  
A: Chi-square test for independence with Benjamini-Hochberg FDR correction.

**Q: Can I analyze continuous data?**  
A: No, this tool is designed for binary (0/1) data only.

**Q: How long does analysis take?**  
A: Typically <1 minute for <100 strains, <5 minutes for <500 strains.

**Q: Can I customize the HTML report?**  
A: Currently no, but you can modify the template in the code.

**Q: Is my data sent anywhere?**  
A: No, all analysis is local. No data is transmitted.

**Q: Can I use this for non-bacterial data?**  
A: Yes! Any binary trait data works (gene presence, phenotypes, etc.).

## Citation

If you use StrepSuis Analyzer in your research, please cite:

```
[Citation information to be added]
```

See CITATION.cff for BibTeX format.

## Support

- **Documentation**: README.md, this USER_GUIDE.md, TESTING.md
- **Issues**: GitHub issue tracker
- **Examples**: See examples/ directory

---

**Version**: 2025.8.11  
**Last Updated**: 2025-08-11
