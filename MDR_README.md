# MDR Analysis - Quick Reference

## Overview
This directory contains a complete implementation of Multi-Drug Resistance (MDR) analysis for antimicrobial resistance data, combining phenotypic (MIC) and genotypic (AMR genes) datasets.

## Quick Start

```bash
# 1. Merge the input files
python merge_data.py

# 2. Run the analysis
python run_mdr_analysis.py merged_resistance_data.csv

# 3. Validate the outputs
python validate_mdr_output.py
```

## Key Results (91 Strains Analyzed)

- **MDR Prevalence**: 39.6% (36/91 isolates)
- **Top Resistance**: Tetracyclines (75.8%)
- **Top AMR Gene**: erm(B) (60.5%)
- **Network Communities**: 6 distinct modules

## Output Files

- **HTML Report**: `output/mdr_analysis_hybrid_*.html` (Interactive, 85KB)
- **Excel Report**: `output/MDR_Analysis_Hybrid_Report_*.xlsx` (17 sheets, 25KB)
- **Network PNG**: `output/png_charts/hybrid_network_visualization.png` (352KB)

## Documentation

| File | Purpose |
|------|---------|
| [RUN_MDR_ANALYSIS.md](RUN_MDR_ANALYSIS.md) | Complete user guide |
| [MDR_ANALYSIS_SUMMARY.md](MDR_ANALYSIS_SUMMARY.md) | Methodology overview |
| [ANALYSIS_RESULTS.txt](ANALYSIS_RESULTS.txt) | Key findings |
| [FILES_CREATED.md](FILES_CREATED.md) | File inventory |

## Scripts

| Script | Description |
|--------|-------------|
| `merge_data.py` | Merges MIC.csv + AMR_genes.csv |
| `run_mdr_analysis.py` | Runs MDR analysis pipeline |
| `validate_mdr_output.py` | Validates output integrity |

## Statistical Methods

✓ Bootstrap CI (5000 iter, 95%)  
✓ Chi-square/Fisher's exact  
✓ Phi coefficient  
✓ FDR correction (α=0.05)  
✓ Louvain communities  
✓ Apriori rules  

## Analysis Components

1. **MDR Classification** - Identifies isolates resistant to ≥3 classes
2. **Frequency Analysis** - Bootstrap confidence intervals for all resistances
3. **Pattern Analysis** - Unique resistance profiles in MDR isolates
4. **Co-occurrence Analysis** - Statistical associations between resistance elements
5. **Gene-Phenotype Associations** - Cross-dataset correlations
6. **Association Rules** - Apriori algorithm for predictive patterns
7. **Hybrid Network** - Interactive resistance co-occurrence visualization
8. **Community Detection** - Functional resistance modules identification

## Requirements

```bash
pip install pandas numpy scipy matplotlib seaborn plotly scikit-learn \
            networkx statsmodels mlxtend jinja2 openpyxl xlsxwriter \
            kaleido pillow python-louvain
```

## Runtime

- Small datasets (<100 strains): 30-60 seconds
- Medium datasets (100-500 strains): 1-3 minutes

## Support

For detailed information:
1. Check [RUN_MDR_ANALYSIS.md](RUN_MDR_ANALYSIS.md) for usage instructions
2. Review [MDR_ANALYSIS_SUMMARY.md](MDR_ANALYSIS_SUMMARY.md) for methodology
3. See [ANALYSIS_RESULTS.txt](ANALYSIS_RESULTS.txt) for results interpretation

## Status

✅ **COMPLETE AND VALIDATED**
- All scripts functional
- All documentation complete
- All outputs verified
- Analysis results validated

---

*For questions or issues, refer to the documentation files listed above.*
