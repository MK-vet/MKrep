# Google Colab Notebooks for MKrep Analysis

This directory contains Google Colab-compatible Jupyter notebooks for running all analysis scripts in the cloud.

## Available Notebooks:

### Interactive (No Coding Required)
1. **Interactive_Analysis_Colab.ipynb** ⭐ **NEW!** - User-friendly interface with widgets
   - Perfect for non-programmers
   - Upload files with buttons
   - Select analysis from dropdown
   - Configure with sliders
   - One-click execution
   - Automatic download

### Advanced (Full Code Access)
2. **Cluster_Analysis_Colab.ipynb** - K-Modes clustering for MIC, AMR, and virulence data
3. **MDR_Analysis_Colab.ipynb** - Multi-drug resistance analysis with hybrid networks
4. **Network_Analysis_Colab.ipynb** - Feature association network analysis
5. **Phylogenetic_Clustering_Colab.ipynb** - Tree-based clustering with evolutionary metrics
6. **StrepSuis_Analysis_Colab.ipynb** - Streptococcus suis specific analysis

## How to Use:

### Option 1: Direct Upload to Colab
1. Go to [Google Colab](https://colab.research.google.com/)
2. Click `File → Upload notebook`
3. Select one of the `.ipynb` files from this directory
4. Follow the instructions in the notebook

### Option 2: Open from GitHub
1. Go to [Google Colab](https://colab.research.google.com/)
2. Click `File → Open notebook → GitHub`
3. Enter: `MK-vet/MKrep`
4. Select the notebook you want to run

### Option 3: Direct Links
Click on these links to open notebooks directly in Colab:

#### For Non-Programmers:
- [**Interactive Analysis**](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Interactive_Analysis_Colab.ipynb) ⭐ **START HERE!**

#### For Researchers (Advanced):
- [Cluster Analysis](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Cluster_Analysis_Colab.ipynb)
- [MDR Analysis](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/MDR_Analysis_Colab.ipynb)
- [Network Analysis](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Network_Analysis_Colab.ipynb)
- [Phylogenetic Clustering](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Phylogenetic_Clustering_Colab.ipynb)
- [StrepSuis Analysis](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/StrepSuis_Analysis_Colab.ipynb)

## Requirements:

- Google account (free)
- Data files in CSV format (binary: 0 = absence, 1 = presence)
- All files must have a `Strain_ID` column

## Features:

✓ **No local installation required** - Everything runs in the cloud  
✓ **Interactive widgets** - Easy parameter configuration  
✓ **File upload/download** - Simple data transfer  
✓ **Free GPU/TPU** - Available for computational acceleration  
✓ **Persistent storage** - Mount Google Drive for saving results  

## Data Format:

All input files should be CSV format with:
- First column: `Strain_ID` (unique identifier for each strain)
- Other columns: Binary features (0 = absence, 1 = presence)

Example:
```csv
Strain_ID,Gene1,Gene2,Gene3,Antibiotic1
Strain001,1,0,1,1
Strain002,0,1,1,0
Strain003,1,1,0,1
```

## Output:

Each notebook generates:
1. **HTML Report** - Interactive tables with sorting, filtering, and export
2. **Excel Report** - Multi-sheet workbook with detailed results
3. **PNG Charts** - High-quality visualizations
4. **CSV Files** - Intermediate results and data tables

All outputs are packaged in a ZIP file for easy download.

## Support:

For issues or questions:
- Open an issue on [GitHub](https://github.com/MK-vet/MKrep/issues)
- Check the documentation in each notebook
- Review the main [README.md](../README.md) for detailed information

## Tips for Colab Users:

1. **Runtime**: Use GPU runtime for faster processing (Runtime → Change runtime type → GPU)
2. **Session timeout**: Colab sessions timeout after ~12 hours of inactivity
3. **Save results**: Download results frequently or mount Google Drive
4. **Large datasets**: Consider splitting data or using high-RAM runtime
5. **Reconnect**: If disconnected, re-run all cells or use Runtime → Run all

### Google Colab Pro for Heavy Computations

For computationally intensive analyses with large datasets, **Google Colab Pro** is recommended:

- **High-RAM Runtime**: Up to 52GB RAM for large datasets
- **Priority GPU Access**: Faster GPUs (T4, P100, V100) with longer runtimes
- **Extended Sessions**: Longer timeout periods for long-running analyses
- **Background Execution**: Continue computation even after closing browser

To use Colab Pro features:
1. Subscribe to Google Colab Pro at https://colab.research.google.com/signup
2. Open any notebook from this repository
3. Select Runtime → Change runtime type → Select GPU/TPU and High-RAM
4. Run your analysis with enhanced computational resources

All notebooks in this repository are **production-ready** and fully functional with both free and Pro versions of Google Colab.

---

**Note:** These notebooks automatically download required scripts and utilities from the main repository. Ensure you have a stable internet connection.
