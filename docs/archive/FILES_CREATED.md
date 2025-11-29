# Files Created for MDR Analysis

This document lists all the files created or modified for the MDR analysis implementation.

## Input Files (Pre-existing)
- `MIC.csv` - Phenotypic resistance data (MIC values)
- `AMR_genes.csv` - Genotypic resistance data (AMR gene presence)

## Scripts Created

### 1. merge_data.py
**Purpose**: Merges MIC.csv and AMR_genes.csv into a single dataset
**Output**: merged_resistance_data.csv
**Usage**: `python merge_data.py`

### 2. run_mdr_analysis.py
**Purpose**: Non-interactive wrapper for MDR_2025_04_15.py
**Features**:
- Accepts command-line argument for CSV path
- Creates output directories automatically
- Configures logging properly
**Usage**: `python run_mdr_analysis.py [csv_file]`
**Default**: Uses merged_resistance_data.csv if no argument provided

### 3. validate_mdr_output.py
**Purpose**: Validates all output files and data integrity
**Checks**:
- Input data presence
- Output directory existence
- HTML/Excel/PNG file generation
- Excel sheet completeness
- Data content validation
**Usage**: `python validate_mdr_output.py`

## Data Files Created

### 1. merged_resistance_data.csv
**Size**: 6.8 KB
**Rows**: 92 (including header)
**Columns**: 35 (Strain_ID + 13 phenotypic + 21 genotypic)
**Format**: Binary (0/1) resistance indicators

## Output Files Generated

### HTML Reports
**Location**: `output/mdr_analysis_hybrid_*.html`
**Size**: ~85 KB each
**Lines**: ~2548 lines
**Features**:
- Interactive DataTables (sortable, searchable, exportable)
- Embedded network visualization
- Complete statistical methodology
- Bootstrap confidence intervals
- All 12+ analysis sections

### Excel Reports
**Location**: `output/MDR_Analysis_Hybrid_Report_*.xlsx`
**Size**: ~25 KB each
**Sheets**: 17 total
1. Metadata - Analysis information
2. Methodology - Statistical methods
3. Dataset_Overview - Summary statistics
4. Freq_Pheno_All - Phenotypic frequencies (all isolates)
5. Freq_Pheno_MDR - Phenotypic frequencies (MDR subset)
6. Freq_Gene_All - Gene frequencies (all isolates)
7. Freq_Gene_MDR - Gene frequencies (MDR subset)
8. Patterns_Pheno_MDR - Phenotypic patterns in MDR
9. Patterns_Gene_MDR - Genotypic patterns in MDR
10. Coocc_Pheno_MDR - Phenotypic co-occurrence
11. Coocc_Gene_MDR - Genotypic co-occurrence
12. Gene_Pheno_Assoc - Gene-phenotype associations
13. Assoc_Rules_Pheno - Phenotypic association rules
14. Assoc_Rules_Genes - Genotypic association rules
15. Network_Edges - Network edge list
16. Network_Communities - Community assignments
17. Network_Stats - Network statistics
18. Chart_Index - Chart reference

### PNG Visualizations
**Location**: `output/png_charts/hybrid_network_visualization.png`
**Size**: ~352 KB
**Dimensions**: 2800 x 2000 pixels
**Format**: PNG, RGBA, 8-bit/color
**Features**:
- Color-coded nodes (red=phenotype, blue=genotype)
- Node size proportional to degree
- High resolution for publication

## Documentation Files

### 1. MDR_ANALYSIS_SUMMARY.md
**Size**: ~6.2 KB
**Purpose**: Comprehensive analysis overview
**Contents**:
- Input data description
- Analyses performed (9 major categories)
- Output files description
- Statistical methods summary
- Key features and reproducibility
- Usage instructions

### 2. RUN_MDR_ANALYSIS.md
**Size**: ~5.9 KB
**Purpose**: User guide for running the analysis
**Contents**:
- Prerequisites and installation
- Input data format requirements
- Quick start guide (2 options)
- Output files description
- Analysis components
- Troubleshooting section
- Example workflow
- Advanced usage

### 3. ANALYSIS_RESULTS.txt
**Size**: ~4.6 KB
**Purpose**: Key findings and results
**Contents**:
- Dataset overview statistics
- Network statistics
- Top resistance classes (top 5)
- Top AMR genes (top 5)
- Network communities
- Key findings interpretation
- Output file locations
- Methods summary

## Modified Files

### 1. MDR_2025_04_15.py
**Change**: Fixed Plotly compatibility issue
**Line**: ~1100
**Details**: Changed deprecated `titlefont` parameter to new `title` dict format
**Reason**: Compatibility with Plotly 5.x+

## File Structure

```
MKrep/
├── MIC.csv                              # Input: Phenotypic data
├── AMR_genes.csv                        # Input: Genotypic data
├── merged_resistance_data.csv           # Generated: Merged data
├── merge_data.py                        # Script: Data merging
├── run_mdr_analysis.py                  # Script: Analysis execution
├── validate_mdr_output.py               # Script: Output validation
├── MDR_2025_04_15.py                    # Modified: Plotly fix
├── MDR_ANALYSIS_SUMMARY.md              # Doc: Analysis overview
├── RUN_MDR_ANALYSIS.md                  # Doc: User guide
├── ANALYSIS_RESULTS.txt                 # Doc: Key findings
└── output/                              # Generated outputs
    ├── mdr_analysis_hybrid_*.html       # HTML reports
    ├── MDR_Analysis_Hybrid_Report_*.xlsx # Excel reports
    └── png_charts/
        └── hybrid_network_visualization.png # Network diagram
```

## File Sizes Summary

| File Type | Count | Total Size |
|-----------|-------|------------|
| Input CSV | 2 | ~13 KB |
| Merged CSV | 1 | 6.8 KB |
| Python Scripts | 3 | ~6 KB |
| Documentation | 3 | ~17 KB |
| HTML Reports | 2 | ~170 KB |
| Excel Reports | 2 | ~50 KB |
| PNG Charts | 1 | ~352 KB |
| **Total** | **14** | **~615 KB** |

## Version Control

All files have been committed to the repository in the branch:
`copilot/run-mdr-analysis-report`

**Commits**:
1. Initial plan and merged data preparation
2. Main implementation with Plotly fix
3. Documentation and validation scripts

## Dependencies

Required packages (from requirements.txt):
- pandas>=1.3.0
- numpy>=1.21.0
- scipy>=1.7.0
- matplotlib>=3.4.0
- seaborn>=0.11.0
- plotly>=5.0.0
- scikit-learn>=1.0.0
- networkx>=2.6.0
- statsmodels>=0.13.0
- mlxtend>=0.19.0
- jinja2>=3.0.0
- openpyxl>=3.0.0
- xlsxwriter>=3.0.0
- kaleido>=0.2.0
- pillow>=8.0.0
- python-louvain>=0.15

## Notes

- All output files are excluded from git via .gitignore
- Analysis is fully reproducible with fixed random seeds
- Runtime: ~30-60 seconds on standard hardware
- Memory usage: <2GB RAM
- No external API calls or internet dependencies (except for CDN in HTML)
