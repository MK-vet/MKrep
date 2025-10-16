# Interactive Analysis Colab Notebook

**No coding required!** This notebook provides a user-friendly, widget-based interface for running MKrep analyses.

## 🎯 Perfect For:

- Researchers without programming experience
- Quick exploratory analysis
- Teaching and demonstrations
- Non-technical collaborators

## 📋 What You Get:

- **Simple interface** - Upload files, select analysis, click buttons
- **No code visible** - All technical details are hidden
- **Interactive widgets** - Dropdowns, sliders, buttons
- **Visual feedback** - Progress bars and status updates
- **Automatic downloads** - Results packaged in a ZIP file

## 🚀 How to Use:

### 1. Open the Notebook

Click here to open in Google Colab:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Interactive_Analysis_Colab.ipynb)

### 2. Run Setup Cells

- **Cell 1**: Install packages (wait 1-2 minutes)
- **Cell 2**: Load analysis tools (wait 30 seconds)

Just click the ▶ button on each cell and wait for it to finish.

### 3. Upload Your Data

- **Cell 3**: Click "Choose Files" button
- Select your CSV files from your computer
- Wait for upload to complete

### 4. Select Analysis Type

- **Cell 4**: Choose from the dropdown menu
  - Cluster Analysis
  - MDR Analysis
  - Network Analysis
  - Phylogenetic Clustering
  - Streptococcus suis Analysis

### 5. Configure Parameters

- **Cell 5**: Adjust sliders and inputs
  - Max Clusters: 2-15
  - Bootstrap Iterations: 100-2000
  - MDR Threshold: 2-10
  - FDR Alpha: 0.01-0.2
  - Random Seed: Any number

### 6. Run Analysis

- **Cell 6**: Click ▶ to start
- Watch the progress bar
- Wait for completion (5-30 minutes depending on data size)

### 7. View and Download Results

- **Cell 7**: View generated files
- **Cell 8**: Click ▶ to download ZIP file
- Check your browser's download folder

## 📁 Required Files:

All CSV files must have a `Strain_ID` column and binary data (0 = absent, 1 = present).

### Cluster Analysis
- `MIC.csv` (required)
- `AMR_genes.csv` (required)
- `Virulence.csv` (required)
- `MLST.csv` (optional)
- `Serotype.csv` (optional)
- `Plasmid.csv` (optional)
- `MGE.csv` (optional)

### MDR Analysis
- `MIC.csv` (required)
- `AMR_genes.csv` (required)
- `Virulence.csv` (optional)
- `MLST.csv` (optional)

### Network Analysis
- `MGE.csv` (required)
- `MIC.csv` (required)
- `MLST.csv` (required)
- `Plasmid.csv` (required)
- `Serotype.csv` (required)
- `Virulence.csv` (required)
- `AMR_genes.csv` (required)

### Phylogenetic Clustering
- `tree.newick` (required)
- `MIC.csv` (required)
- `AMR_genes.csv` (required)
- `Virulence.csv` (required)
- `MLST.csv` (optional)
- `Serotype.csv` (optional)

### Streptococcus suis Analysis
- `tree.newick` (required)
- `MIC.csv` (required)
- `AMR_genes.csv` (required)
- `Virulence.csv` (required)
- `MLST.csv` (optional)
- `Serotype.csv` (optional)

## 📊 Output Files:

Your download will include:

1. **HTML Report** - Interactive report with tables and charts
2. **Excel Workbook** - Detailed results in spreadsheet format
3. **PNG Charts** - High-quality visualizations (in `png_charts/` folder)

## ⏱️ Expected Runtime:

| Analysis Type | Small Dataset (<100 strains) | Large Dataset (>500 strains) |
|---------------|------------------------------|------------------------------|
| Cluster       | 5-10 minutes                 | 15-30 minutes                |
| MDR           | 3-8 minutes                  | 10-20 minutes                |
| Network       | 2-5 minutes                  | 5-15 minutes                 |
| Phylogenetic  | 10-15 minutes                | 20-40 minutes                |
| StrepSuis     | 10-15 minutes                | 20-40 minutes                |

*Times are for Google Colab free tier. Colab Pro will be faster.*

## 💡 Tips:

### For Faster Analysis:
- Use Google Colab Pro for large datasets
- Reduce bootstrap iterations (100-200 for quick analysis)
- Use fewer max clusters (4-6 instead of 8-15)

### For Better Results:
- Use 500+ bootstrap iterations for publication quality
- Test multiple cluster numbers
- Include optional files when available
- Use consistent random seed for reproducibility

### Troubleshooting:

**Upload fails:**
- Check file format (must be CSV)
- Verify `Strain_ID` column exists
- Ensure data is binary (0 and 1 only)

**Analysis times out:**
- Reduce dataset size
- Lower bootstrap iterations
- Use Colab Pro
- Split into smaller batches

**Memory errors:**
- Use Colab Pro (more RAM)
- Reduce number of features
- Simplify analysis parameters

**Download doesn't start:**
- Allow popups in browser
- Check downloads folder
- Try different browser

## 🆚 Comparison with Other Options:

| Feature | Interactive Notebook | Advanced Notebooks | Local Scripts | Docker |
|---------|---------------------|-------------------|---------------|--------|
| Coding Required | ❌ No | ✅ Yes | ✅ Yes | ⚠️ Minimal |
| Setup Time | < 3 minutes | < 3 minutes | 10-30 minutes | 5-15 minutes |
| Customization | ⭐⭐ Limited | ⭐⭐⭐⭐⭐ Full | ⭐⭐⭐⭐⭐ Full | ⭐⭐⭐⭐ High |
| Learning Curve | ⭐ Very Easy | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐ Advanced | ⭐⭐⭐ Moderate |
| Best For | Beginners | Researchers | Developers | Teams |

## 📚 Additional Resources:

- [Main README](../README.md) - Project overview
- [User Guide](../USER_GUIDE.md) - Complete user guide
- [Interpretation Guide](../INTERPRETATION_GUIDE.md) - Understanding results
- [Advanced Notebooks](README.md) - For researchers who want code access
- [Docker Deployment](../DOCKER_DEPLOYMENT.md) - Containerized deployment

## 🤝 Support:

Need help?

1. Check this README first
2. Review the [User Guide](../USER_GUIDE.md)
3. Look at [Troubleshooting](#troubleshooting) above
4. Open an issue on [GitHub](https://github.com/MK-vet/MKrep/issues)

When reporting issues, include:
- Which analysis type you selected
- Size of your dataset (number of strains and features)
- Error message (if any)
- Parameter settings you used

## 📄 License:

MIT License - See [LICENSE](../LICENSE) for details

---

**Ready to start?** [Open the Interactive Notebook](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Interactive_Analysis_Colab.ipynb) and begin analyzing your data in minutes!
