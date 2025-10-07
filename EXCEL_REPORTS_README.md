# Excel Report Generation Updates

## Overview

All Python analysis scripts in this repository have been updated to generate comprehensive Excel reports (.xlsx) with PNG charts in addition to the existing HTML reports. This provides users with detailed, structured data that can be easily analyzed in spreadsheet applications.

## What Changed

### 1. New Shared Utility Module: `excel_report_utils.py`

A new module providing the `ExcelReportGenerator` class with the following features:

- **Excel Report Creation**: Generate multi-sheet Excel workbooks with metadata, methodology, and data
- **PNG Chart Saving**: Save matplotlib and plotly figures as high-quality PNG files
- **Automatic Formatting**: Auto-adjust column widths, round numeric values, add descriptions
- **Chart Indexing**: Create a sheet listing all generated PNG charts
- **Sheet Name Sanitization**: Ensure Excel sheet name compliance (max 31 chars, no invalid chars)

### 2. Updated Analysis Scripts

All 5 Python analysis scripts now generate both HTML and Excel reports:

#### Network_Analysis_2025_06_26.py
- **Excel Sheets**: Feature summary, Chi-square results, Entropy, Cramér's V, Exclusive patterns (k=2 and k=3), Network analysis, Cluster hubs
- **PNG Charts**: 3D network visualization with cluster labels
- **Methodology**: Chi-square/Fisher tests, Information theory, Mutually exclusive patterns, Network analysis, Hub identification

#### MDR_2025_04_15.py
- **Excel Sheets**: Dataset overview, Frequency analyses (all/MDR), Pattern analyses, Co-occurrence matrices, Association rules, Network edges/communities, Network statistics
- **PNG Charts**: Hybrid co-resistance network (phenotype-gene interactions)
- **Methodology**: Bootstrap resampling, Association testing, Pattern analysis, Co-occurrence analysis, Association rules, Hybrid network construction

#### Cluster_MIC_AMR_Viruelnce.py
- **Excel Sheets**: Integrated clusters, Category-specific results (Chi-square, Log-odds, Feature importance, Association rules, MCA), All CSV outputs
- **PNG Charts**: MCA scatter plots, Correlation heatmaps
- **Methodology**: K-Modes clustering, Statistical tests, Log-odds ratios, Logistic regression, MCA, Random Forest, Association rules, Bootstrap CIs

#### StrepSuisPhyloCluster_2025_08_11.py
- **Excel Sheets**: All CSV files from analysis (clusters, traits, evolutionary metrics, etc.)
- **PNG Charts**: Phylogenetic tree with color-coded clusters
- **Methodology**: Tree-aware clustering, Ensemble fallback, Evolutionary metrics, Trait profiling, Association rules, MCA

#### Phylgenetic_clustering_2025_03_21.py
- **Excel Sheets**: All CSV files from analysis (clusters, outliers, PD, pairwise distances, traits, etc.)
- **PNG Charts**: Phylogenetic tree, UMAP embedding
- **Methodology**: Phylogenetic clustering, Outlier detection, Ensemble clustering, Evolutionary metrics, Binary trait analysis, Association rules, MCA, Statistical corrections

## Report Structure

Each Excel report contains the following standardized sheets:

1. **Metadata Sheet**: Report information, analysis date, configuration parameters
2. **Methodology Sheet**: Detailed descriptions of all statistical methods and algorithms used
3. **Data Sheets**: Multiple sheets with analysis results (specific to each script)
4. **Chart_Index Sheet**: List of all generated PNG files with paths

## PNG Charts

All charts and visualizations are saved as high-quality PNG files in a `png_charts` subfolder within the output directory:

- **Format**: PNG (Portable Network Graphics)
- **Resolution**: 150 DPI for matplotlib, 1200x800 pixels (scale=2) for plotly
- **Location**: `<output_folder>/png_charts/`
- **Naming**: Descriptive names (e.g., `network_3d_visualization.png`, `phylogenetic_tree.png`)

## Usage

No changes are required to run the scripts. Simply execute them as before:

```python
python Network_Analysis_2025_06_26.py
```

Each script will now generate:
1. An HTML report (for interactive features)
2. An Excel report (for detailed data analysis)
3. PNG files for all charts/visualizations

## Technical Details

### Dependencies

The following packages are required (automatically installed by most scripts):
- `openpyxl`: Excel file writing
- `xlsxwriter`: Alternative Excel writer (optional)
- `kaleido`: Plotly PNG export (with fallback to HTML)
- `pillow`: Image processing for PNG extraction

### Excel File Specifications

- **Engine**: openpyxl
- **Max Sheets**: Unlimited (limited by Excel application)
- **Sheet Names**: Max 31 characters, sanitized to remove invalid characters (`:`, `\`, `/`, `?`, `*`, `[`, `]`)
- **Numeric Precision**: 4 decimal places (adjustable)
- **Column Widths**: Auto-adjusted to content (max 100 characters)

### Performance Considerations

- Excel generation adds minimal overhead (typically < 5 seconds)
- PNG chart generation time depends on chart complexity
- Memory usage is efficient with proper cleanup
- Large datasets may produce large Excel files (consider filtering/aggregation)

## Example Output

After running an analysis script, you will find:

```
output/
├── <script_name>_Report_<timestamp>.xlsx
├── <script_name>_report.html
└── png_charts/
    ├── network_3d_visualization.png
    ├── phylogenetic_tree.png
    ├── mca_scatter_MIC.png
    └── heatmap_AMR.png
```

## Benefits

1. **Excel Format**: Easy to analyze, filter, and manipulate data in Excel/Google Sheets/LibreOffice
2. **PNG Charts**: High-quality static images for publications and presentations
3. **Structured Data**: Organized sheets with clear descriptions and metadata
4. **Reproducibility**: Complete methodology documentation in each report
5. **Flexibility**: Both HTML (interactive) and Excel (structured) formats available

## Troubleshooting

### "Module not found: openpyxl"
```bash
pip install openpyxl
```

### "Cannot save plotly figure as PNG"
This is expected if kaleido is not installed. The script will fallback to saving as HTML:
```bash
pip install kaleido
```

### "Invalid sheet name"
Sheet names are automatically sanitized. If you see warnings, they can be safely ignored.

### Large Excel files
If Excel files are too large:
- Check the Chart_Index sheet to see which CSV files are included
- Consider excluding large intermediate files
- Use data aggregation/filtering before report generation

## Future Enhancements

Potential improvements for future versions:
- Excel chart embedding (instead of PNG references)
- Conditional formatting for statistical significance
- Hyperlinks from data sheets to PNG files
- Summary dashboard sheet with key metrics
- PDF export of Excel reports

## Support

For questions or issues related to Excel report generation:
1. Check that all dependencies are installed
2. Verify output folder has write permissions
3. Check the console output for error messages
4. Review the generated Excel file's Metadata sheet for configuration details
