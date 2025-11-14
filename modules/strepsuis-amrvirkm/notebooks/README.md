# Google Colab Notebooks

This directory contains Google Colab notebooks for running StrepSuis-AMRVirKM analysis without any local installation.

## Available Notebooks

### Main Analysis Notebook

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/strepsuis-amrvirkm/blob/main/notebooks/cluster_analysis.ipynb)

**cluster_analysis.ipynb** - Complete K-Modes clustering analysis

This notebook provides a user-friendly interface for:
- Installing the package from GitHub (no code duplication)
- Uploading data files
- Running clustering analysis
- Downloading results

## How to Use

1. **Click the "Open in Colab" badge** above
2. **Sign in to Google** (if not already signed in)
3. **Follow the notebook instructions**:
   - Run installation cell
   - Upload your CSV files
   - Configure parameters (optional)
   - Run analysis
   - Download results

## No Coding Required!

The notebooks are designed for researchers without programming experience. Just follow the step-by-step instructions.

## Requirements

- Google account (for Google Colab)
- CSV data files (MIC.csv, AMR_genes.csv, Virulence.csv)
- Internet connection

## Data Format

Your CSV files should have:
- First column: `Strain_ID` (unique identifier)
- Other columns: Binary values (0 or 1)
- 0 = absence, 1 = presence
- No missing values

## Runtime

- **Quick analysis** (8 clusters, 200 bootstrap): 5-10 minutes
- **Thorough analysis** (10 clusters, 500 bootstrap): 10-20 minutes

Free Colab is usually sufficient for most analyses.

## Output Files

The notebook generates:
1. **HTML report** - Interactive, publication-ready
2. **Excel workbook** - All data and statistics
3. **PNG charts** - High-quality visualizations

All files are packaged into a ZIP for easy download.

## Troubleshooting

### Session Timeout
If your Colab session times out:
- Re-run from the beginning
- Download results frequently
- Use Colab Pro for longer sessions

### Out of Memory
If you get memory errors:
- Reduce bootstrap iterations
- Remove low-variance features
- Use Colab Pro for more RAM

### Installation Issues
If package installation fails:
- Check internet connection
- Try running the installation cell again
- Report issues on GitHub

## Support

- **Documentation**: [Main README](../README.md)
- **Issues**: [GitHub Issues](https://github.com/MK-vet/strepsuis-amrvirkm/issues)
- **Examples**: [Example data](../examples/)

## Related Resources

- **User Guide**: [docs/USAGE.md](../docs/USAGE.md)
- **API Documentation**: [docs/API.md](../docs/API.md)
- **Example Results**: [docs/EXAMPLES.md](../docs/EXAMPLES.md)
