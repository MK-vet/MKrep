# Expected Results

This directory will contain example results after running the analysis on the example datasets.

## Generated Files

When you run the analysis, the following files will be created:

### HTML Report

**File:** `GenPhen_Analysis_report.html`

Interactive HTML report containing:
- Summary statistics
- Interactive visualizations (Plotly charts)
- Detailed results tables with DataTables
- Interpretation guide
- Methodology description

### Excel Report

**File:** `GenPhen_Analysis_Report_<timestamp>.xlsx`

Multi-sheet Excel workbook with:
- **Metadata:** Analysis parameters and settings
- **Summary:** Key statistics and findings
- **Results:** Detailed results tables
- **Methodology:** Statistical methods used
- **Interpretation:** Guide to understanding results

### PNG Charts Directory

**Directory:** `png_charts/`

High-resolution charts (150+ DPI) suitable for publication:
- Network visualizations
- Clustering plots
- Heatmaps
- Statistical plots
- Dendrograms

## File Structure

```
results/
├── GenPhen_Analysis_report.html
├── GenPhen_Analysis_Report_20250114_120000.xlsx
└── png_charts/
    ├── network_visualization.png
    ├── cluster_plot.png
    ├── heatmap.png
    ├── dendrogram.png
    └── ...
```

## Result Interpretation

See the Interpretation section in:
- HTML report (included in each report)
- [USER_GUIDE.md](../USER_GUIDE.md)
- Main [README.md](../README.md)

## Publication Quality

All outputs are production-ready:
- ✅ High-resolution figures (150+ DPI)
- ✅ Consistent professional styling
- ✅ Complete methodology documentation
- ✅ Reproducible with documented parameters
- ✅ Ready for scientific publications

## Reproducibility

To reproduce results:

1. Use the same input data
2. Set the same random seed (default: 42)
3. Use the same parameters
4. Use the same tool version (1.0.0)

Example:
```bash
strepsuis-genphen \
  --data-dir examples/ \
  --output results/ \
  --random-seed 42 \
  --bootstrap 500
```

## Questions?

For questions about results or interpretation:
- See [USER_GUIDE.md](../USER_GUIDE.md)
- See main [README.md](../README.md)
- Open an issue on [GitHub](https://github.com/MK-vet/strepsuis-genphen/issues)
