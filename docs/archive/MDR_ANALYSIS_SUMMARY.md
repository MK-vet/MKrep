# MDR Analysis Report Summary

## Overview
This document summarizes the comprehensive Multi-Drug Resistance (MDR) analysis performed on the antimicrobial resistance dataset combining phenotypic (MIC) and genotypic (AMR genes) data.

## Input Data
- **MIC.csv**: Minimum Inhibitory Concentration data for 91 strains across 13 antibiotics
- **AMR_genes.csv**: AMR gene presence/absence data for 91 strains across 21 genes
- **Merged Dataset**: Combined 91 strains × 35 features (13 phenotypic + 21 genotypic)

## Analyses Performed

### 1. MDR Classification
- Built class-based resistance matrix from individual antibiotic resistances
- Identified MDR isolates (resistant to ≥3 antibiotic classes)
- Applied threshold of 3 classes as per standard MDR definition

### 2. Bootstrap Confidence Intervals (5000 iterations, 95% CI)
- Phenotypic resistance frequencies in ALL isolates
- Phenotypic resistance frequencies in MDR isolates only
- AMR gene frequencies in ALL isolates
- AMR gene frequencies in MDR isolates only

### 3. MDR Pattern Analysis
- Identified unique phenotypic resistance patterns in MDR isolates
- Identified unique genotypic resistance patterns in MDR isolates
- Calculated pattern frequencies with bootstrap confidence intervals

### 4. Co-occurrence Analysis
- Pairwise co-occurrence among antibiotic classes in MDR isolates
- Pairwise co-occurrence among AMR genes in MDR isolates
- Statistical significance testing with multiple testing correction (FDR)
- Phi coefficient calculation for association strength

### 5. Gene-Phenotype Association Analysis
- Cross-dataset analysis between AMR genes and resistance phenotypes
- Chi-square/Fisher's exact test for associations
- Multiple hypothesis testing correction (Benjamini-Hochberg FDR)
- Phi coefficient for effect size

### 6. Association Rule Mining
- Applied Apriori algorithm for phenotypic resistances
- Applied Apriori algorithm for AMR genes
- Metrics: support, confidence, lift, leverage, conviction
- Default thresholds: min_support=0.1, lift_threshold=1.0

### 7. Hybrid Network Analysis
- Constructed co-resistance network combining phenotypes and genes
- Node types: Phenotypic resistance classes (red) + AMR genes (blue)
- Edge types: Gene-Phenotype associations (primary focus)
- Statistical filtering: Only significant edges after FDR correction

### 8. Community Detection
- Louvain algorithm for network module identification
- Modularity optimization approach
- Identified functional modules of co-occurring resistances

### 9. Interactive Visualization
- Generated Plotly interactive network figure
- Color-coded nodes by type (phenotype vs. genotype)
- Node size proportional to degree centrality
- Hover information with detailed statistics

## Output Files

### HTML Report
**File**: `output/mdr_analysis_hybrid_*.html`
- Comprehensive interactive report with all results
- Embedded network visualization
- DataTables for all result tables (sortable, searchable, exportable)
- Statistical methodology documentation for each analysis
- Generated timestamp for reproducibility

### Excel Report
**File**: `output/MDR_Analysis_Hybrid_Report_*.xlsx`
- 17 sheets with complete analysis results
- Sheets include:
  - Metadata and methodology
  - Dataset overview statistics
  - All frequency tables with confidence intervals
  - Pattern analysis results
  - Co-occurrence matrices
  - Association analysis results
  - Network edges and community assignments
  - Network statistics summary
  - Chart index

### PNG Charts
**Directory**: `output/png_charts/`
- Hybrid network visualization (PNG format)
- High-resolution export suitable for publications

## Statistical Methods Summary

1. **Bootstrap Resampling**: 5000 iterations for non-parametric 95% confidence intervals
2. **Chi-square Test**: For association analysis when expected counts ≥5
3. **Fisher's Exact Test**: For association analysis when expected counts <5
4. **Phi Coefficient**: Effect size measure for 2×2 contingency tables
5. **Benjamini-Hochberg FDR**: Multiple testing correction (α=0.05)
6. **Louvain Algorithm**: Community detection via modularity optimization
7. **Apriori Algorithm**: Association rule mining with support/lift metrics

## Key Features

### MDR Definition
- **Threshold**: Resistance to ≥3 antibiotic classes
- **Classes**: 9 antibiotic classes defined (Tetracyclines, Macrolides, Aminoglycosides, Pleuromutilins, Sulfonamides, Fluoroquinolones, Penicillins, Cephalosporins, Phenicols)

### Pattern Recognition
- Unique resistance profiles identified for both phenotypes and genotypes
- Frequency estimation with statistical confidence
- Pattern-based clustering for epidemiological insights

### Network Approach
- Hybrid network integrating both data types
- Edge weights based on statistical association strength
- Community structure reveals functional resistance modules
- Interactive exploration enabled

## Reproducibility
- All random processes use fixed seeds where applicable
- Bootstrap iterations: 5000 (standard for robust estimation)
- Confidence level: 95% (standard in biomedical research)
- FDR correction: α=0.05 (standard for multiple testing)

## Data Quality
- No missing values in merged dataset
- Binary encoding (0/1) for resistance indicators
- Strain IDs maintained for traceability
- Column naming conventions preserved

## Analysis Execution
The complete pipeline was executed successfully:
- Runtime: ~30-60 seconds on standard hardware
- No errors or warnings (deprecation warnings only)
- All output files generated as expected
- Memory efficient processing

## Next Steps / Usage
1. Open the HTML report in a web browser for interactive exploration
2. Open the Excel file for detailed data analysis and custom visualizations
3. Review PNG charts for publication-ready figures
4. Export specific tables from HTML report using DataTables buttons (CSV, Excel, PDF)
5. Use network communities for focused investigation of resistance mechanisms

## Notes
- The analysis pipeline is fully automated and reproducible
- Input files must have matching Strain_ID columns for proper merging
- Binary data (0/1) format required for resistance indicators
- Network visualization supports zooming and panning for detailed exploration
