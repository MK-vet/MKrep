# Running the MDR Analysis

This guide explains how to execute the Multi-Drug Resistance (MDR) analysis pipeline on antimicrobial resistance data.

## Prerequisites

1. Python 3.8 or higher
2. Required packages (install via pip):
```bash
pip install pandas numpy scipy matplotlib seaborn plotly scikit-learn networkx statsmodels mlxtend jinja2 openpyxl xlsxwriter kaleido pillow python-louvain
```

## Input Data Format

The analysis requires two CSV files:
1. **MIC.csv**: Phenotypic resistance data (Minimum Inhibitory Concentration)
   - Must contain a `Strain_ID` column
   - Antibiotic columns with binary values (0=susceptible, 1=resistant)

2. **AMR_genes.csv**: Genotypic resistance data (AMR gene presence)
   - Must contain a `Strain_ID` column
   - Gene columns with binary values (0=absent, 1=present)

## Quick Start

### Option 1: Using the Wrapper Script (Recommended)

```bash
# Step 1: Merge the input files
python merge_data.py

# Step 2: Run the analysis
python run_mdr_analysis.py merged_resistance_data.csv
```

### Option 2: Using the Original Script

```bash
# Run the original script (will prompt for input file)
python MDR_2025_04_15.py
# Then enter: merged_resistance_data.csv when prompted
```

## Output Files

After successful execution, the following files will be created in the `output/` directory:

1. **HTML Report** (`mdr_analysis_hybrid_*.html`)
   - Interactive comprehensive report
   - All analyses with statistical details
   - Embedded network visualization
   - Exportable tables (CSV, Excel, PDF)

2. **Excel Report** (`MDR_Analysis_Hybrid_Report_*.xlsx`)
   - 17 sheets with all analysis results
   - Ready for further analysis
   - Formatted tables with proper headers

3. **PNG Charts** (`png_charts/hybrid_network_visualization.png`)
   - High-resolution network diagram
   - Publication-ready figure

## Analysis Components

The pipeline performs the following analyses:

1. **MDR Classification**: Identifies isolates resistant to ≥3 antibiotic classes
2. **Frequency Analysis**: Bootstrap confidence intervals (5000 iterations, 95% CI)
3. **Pattern Analysis**: Unique resistance profiles in MDR isolates
4. **Co-occurrence Analysis**: Statistical associations between resistance elements
5. **Gene-Phenotype Associations**: Cross-dataset correlations
6. **Association Rules**: Apriori algorithm for predictive patterns
7. **Hybrid Network**: Interactive resistance co-occurrence network
8. **Community Detection**: Louvain algorithm for functional modules

## Expected Runtime

- Small datasets (<100 strains): 30-60 seconds
- Medium datasets (100-500 strains): 1-3 minutes
- Large datasets (>500 strains): 5-10 minutes

## Troubleshooting

### Missing Dependencies
```bash
# Install all required packages
pip install -r requirements.txt
```

### Input File Not Found
- Ensure CSV files are in the same directory as the scripts
- Check file names match exactly (case-sensitive)

### Plotly Compatibility Issues
- The code has been updated to work with newer Plotly versions
- If issues persist, try: `pip install --upgrade plotly kaleido`

### Memory Issues
- For large datasets, consider running on a machine with >8GB RAM
- Close other applications to free up memory

## Interpreting Results

### HTML Report
- Open in any modern web browser (Chrome, Firefox, Edge, Safari)
- Use DataTables features (search, sort, export)
- Interactive network can be zoomed and panned
- Hover over nodes for detailed information

### Excel Report
- Open with Microsoft Excel, LibreOffice, or similar
- Each sheet represents a different analysis component
- Charts sheet provides index of visualizations
- All tables are formatted and ready for analysis

### Network Visualization
- Red nodes: Phenotypic resistance classes
- Blue nodes: AMR genes
- Node size: Proportional to degree (number of connections)
- Edges: Significant associations (FDR-corrected p < 0.05)

## Statistical Methods

- **Bootstrap**: Non-parametric confidence intervals (5000 iterations)
- **Association Tests**: Chi-square or Fisher's exact (depending on cell counts)
- **Effect Size**: Phi coefficient for 2×2 tables
- **Multiple Testing**: Benjamini-Hochberg FDR correction (α=0.05)
- **Community Detection**: Louvain algorithm (modularity optimization)
- **Association Rules**: Apriori algorithm (min_support=0.1, lift>1.0)

## Citation

If you use this analysis pipeline in your research, please cite:
- The specific statistical methods employed
- Software packages used (pandas, numpy, scipy, networkx, statsmodels, mlxtend, plotly)

## Support

For issues or questions:
1. Check the MDR_ANALYSIS_SUMMARY.md for detailed documentation
2. Review the HTML report's methodology sections
3. Consult the original script documentation

## Example Workflow

```bash
# Complete workflow from start to finish
cd /path/to/MKrep

# 1. Ensure you have the input files
ls MIC.csv AMR_genes.csv

# 2. Merge the input files
python merge_data.py

# 3. Run the analysis
python run_mdr_analysis.py merged_resistance_data.csv

# 4. Open the results
open output/mdr_analysis_hybrid_*.html  # macOS
xdg-open output/mdr_analysis_hybrid_*.html  # Linux
start output/mdr_analysis_hybrid_*.html  # Windows
```

## Advanced Usage

### Custom Input File
```bash
python run_mdr_analysis.py your_custom_file.csv
```

### Modifying Parameters
Edit `MDR_2025_04_15.py` to adjust:
- MDR threshold (default: 3 classes)
- Bootstrap iterations (default: 5000)
- Confidence level (default: 0.95)
- FDR alpha (default: 0.05)
- Association rule thresholds (min_support, lift)

### Batch Processing
```bash
# Process multiple files
for file in data/*.csv; do
    python run_mdr_analysis.py "$file"
done
```

## Notes

- The analysis is fully reproducible with fixed random seeds
- All output files include timestamps for version control
- Network communities are numbered sequentially (1, 2, 3, ...)
- Patterns are represented as tuples of resistance classes/genes
