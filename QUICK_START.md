# MKrep Quick Start Guide

**Welcome to MKrep!** This guide will help you get started in 5 minutes.

## 🎯 Choose Your Path

### Option 1: Interactive Colab (No Coding Required) ⭐ **RECOMMENDED FOR BEGINNERS**
**Perfect for**: Non-programmers, quick analysis, demonstrations

1. Click: [Interactive Analysis Colab](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Interactive_Analysis_Colab.ipynb)
2. Run the first 2 cells (installation, ~2 minutes)
3. Upload your CSV files with the upload button
4. Select analysis type from dropdown
5. Adjust parameters with sliders
6. Click "Run Analysis"
7. Download results

**No programming knowledge required!**

---

### Option 2: Google Colab Notebooks (Code-Based)
**Perfect for**: Beginners who want to understand the code

1. Click: [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Cluster_Analysis_Colab.ipynb)
2. Click **Runtime → Run all**
3. Upload your CSV files when prompted
4. Wait 5-10 minutes
5. Download results.zip

---

### Option 3: Docker Container 🐳 **RECOMMENDED FOR TEAMS**
**Perfect for**: Consistent environments, team collaboration, production use

```bash
# Clone repository
git clone https://github.com/MK-vet/MKrep.git
cd MKrep

# Prepare data
mkdir -p data output
cp your_data/*.csv data/

# Build and run
docker build -t mkrep:latest .
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
    mkrep:latest mkrep-cluster --data-dir /data --output /output

# OR use Docker Compose
docker-compose up mkrep-cluster
```

See [Docker Deployment Guide](DOCKER_DEPLOYMENT.md) for details.

---

### Option 4: Command Line (Best for Automation)
**Perfect for**: Batch processing, HPC clusters, reproducible workflows

```bash
# Install
pip install -r requirements.txt

# Run analysis
python Cluster_MIC_AMR_Viruelnce.py

# Or use CLI (when package is installed)
mkrep-cluster --data-dir ./data --output ./results
```

---

### Option 5: Interactive Dashboard
**Perfect for**: Exploration, parameter tuning, visualization

```bash
pip install voila ipywidgets
cd huggingface_demo
voila MKrep_Dashboard.ipynb --port 8866
```

Open http://localhost:8866 in your browser.

---

## 📊 What You Need

### Required: CSV Files
Your data must be in CSV format with:
- **First column**: `Strain_ID` (unique identifier)
- **Other columns**: Binary values (0 = absence, 1 = presence)

Example:
```csv
Strain_ID,Gene1,Gene2,Resistance1
Strain001,1,0,1
Strain002,0,1,1
Strain003,1,1,0
```

### Supported Files
- `MIC.csv` - Minimum Inhibitory Concentration
- `AMR_genes.csv` - Antimicrobial resistance genes
- `Virulence.csv` - Virulence factors
- `MLST.csv` - Multi-locus sequence typing
- `Serotype.csv` - Serological types
- `Plasmid.csv` - Plasmid presence/absence
- `MGE.csv` - Mobile genetic elements
- `tree.newick` - Phylogenetic tree (for phylo analyses)

---

## 🎁 What You Get

After running an analysis, you'll receive:

1. **📄 HTML Report**
   - Interactive tables (sort, filter, search)
   - Export buttons (CSV, Excel, PDF)
   - Beautiful charts (Plotly)
   - Self-contained (one file)

2. **📊 Excel Workbook**
   - Multiple sheets with organized data
   - Methodology documentation
   - All results in one file
   - Easy to share with collaborators

3. **🖼️ PNG Charts**
   - High-quality images
   - Publication-ready
   - Separate files for each figure

---

## 🚀 5-Minute Tutorial

### Step 1: Get the Code
```bash
git clone https://github.com/MK-vet/MKrep.git
cd MKrep
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Check Everything Works
```bash
python validate.py
```

### Step 4: Run Example Analysis
```bash
# Using provided example data
python Cluster_MIC_AMR_Viruelnce.py
```

### Step 5: View Results
Open the generated HTML file in your browser!

---

## 📚 Need More Help?

- **Installation issues?** → Read [INSTALLATION.md](INSTALLATION.md)
- **Data format questions?** → Read [BINARY_DATA_GUIDE.md](BINARY_DATA_GUIDE.md)
- **Want all features?** → Read [FEATURES.md](FEATURES.md)
- **Complete overview?** → Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **Main documentation?** → Read [README.md](README.md)

---

## 🔍 Analysis Types

### 1. Cluster Analysis
**What**: Groups strains by similarity
**When**: You want to find patterns in your data
**File**: `Cluster_MIC_AMR_Viruelnce.py`
**Colab**: [Cluster_Analysis_Colab.ipynb](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Cluster_Analysis_Colab.ipynb)

### 2. MDR Analysis
**What**: Multi-drug resistance patterns
**When**: You study antibiotic resistance
**File**: `MDR_2025_04_15.py`
**Colab**: [MDR_Analysis_Colab.ipynb](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/MDR_Analysis_Colab.ipynb)

### 3. Network Analysis
**What**: Gene-phenotype associations
**When**: You want to find connections between features
**File**: `Network_Analysis_2025_06_26.py`
**Colab**: [Network_Analysis_Colab.ipynb](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Network_Analysis_Colab.ipynb)

### 4. Phylogenetic Clustering
**What**: Tree-based strain grouping
**When**: You have a phylogenetic tree
**File**: `Phylogenetic_clustering_2025_03_21.py`
**Colab**: [Phylogenetic_Clustering_Colab.ipynb](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Phylogenetic_Clustering_Colab.ipynb)

### 5. StrepSuis Analysis
**What**: *Streptococcus suis* specific
**When**: You work with *S. suis* strains
**File**: `StrepSuisPhyloCluster_2025_08_11.py`
**Colab**: [StrepSuis_Analysis_Colab.ipynb](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/StrepSuis_Analysis_Colab.ipynb)

---

## ⚠️ Common Issues

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Data is not binary"
Your CSV must have only 0 and 1 values (except Strain_ID column).
See [BINARY_DATA_GUIDE.md](BINARY_DATA_GUIDE.md) for conversion help.

### "File not found"
Make sure your CSV files are in the same directory as the script,
or specify the path with `--data-dir` option.

### "Out of memory"
Reduce bootstrap iterations:
```bash
mkrep-cluster --bootstrap 100  # instead of 500
```

---

## 💡 Pro Tips

1. **Start with Colab** if you're new to Python
2. **Use validation script** before running analysis: `python validate.py`
3. **Check example data** to see the required format
4. **Read binary data guide** if you have continuous data
5. **Use CLI for automation** of multiple datasets
6. **Mount Google Drive** in Colab to save results permanently

---

## 🎓 Learning Path

1. **Day 1**: Try Google Colab with example data
2. **Day 2**: Upload your own data to Colab
3. **Day 3**: Install locally and run scripts
4. **Day 4**: Explore CLI options and parameters
5. **Day 5**: Read full documentation and customize

---

## 📞 Get Help

- **Issues**: https://github.com/MK-vet/MKrep/issues
- **Discussions**: https://github.com/MK-vet/MKrep/discussions
- **Documentation**: See all `.md` files in repository

---

## ✅ Checklist

Before asking for help, verify:
- [ ] Ran `python validate.py`
- [ ] Checked data format (CSV with 0/1 values)
- [ ] Installed all dependencies (`pip install -r requirements.txt`)
- [ ] Read [INSTALLATION.md](INSTALLATION.md)
- [ ] Read [BINARY_DATA_GUIDE.md](BINARY_DATA_GUIDE.md)
- [ ] Tried example data first
- [ ] Checked error messages in terminal/console

---

**Ready to start?** Choose your path above and begin analyzing! 🚀
