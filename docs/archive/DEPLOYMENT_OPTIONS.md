# MKrep Deployment Options

This document describes all available methods to access and run MKrep analysis tools.

## Overview

MKrep provides **multiple deployment options** to accommodate different user needs, technical skills, and computational resources:

1. **Interactive Web Portal** - For quick access and browsing
2. **Google Colab** - Cloud-based, no installation required
3. **Binder** - Alternative cloud platform with JupyterLab
4. **Docker** - Containerized deployment for reproducibility
5. **Local Installation** - Full control and customization
6. **Python Package (CLI)** - Command-line interface
7. **Voilà Dashboard** - Interactive web interface
8. **GitHub Actions** - Automated workflows

## 1. Interactive Web Portal 🌐

**Best for:** First-time users, researchers reading articles, quick overview

**URL:** https://mk-vet.github.io/MKrep/

**Features:**
- Browse all 5 analysis tools
- Read detailed documentation
- Download demo datasets
- View example results
- One-click access to Colab/Binder

**No installation required** - Just open in web browser

**Pros:**
- Easiest to access
- Comprehensive documentation
- Links to all other options
- Perfect for scientific articles

**Cons:**
- Documentation only (must use other methods to run analyses)

---

## 2. Google Colab ☁️

**Best for:** Beginners, quick analyses, users without local Python setup

**Access:**
- [Interactive Analysis Notebook](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Interactive_Analysis_Colab.ipynb)
- Individual tool notebooks in `colab_notebooks/` directory

**Features:**
- No installation required
- Free GPU access
- Easy file upload/download
- Save to Google Drive
- Collaborative editing

**Requirements:**
- Google account (free)
- Web browser
- Internet connection

**Pros:**
- Zero setup time
- Free computational resources
- Good for moderate datasets
- Shareable notebook links
- Colab Pro available for large datasets

**Cons:**
- Session timeout after inactivity
- Limited to Colab environment
- Requires Google account
- Files not persistent (use Google Drive)

**Quick Start:**
1. Click Colab link
2. Run all cells (Runtime → Run all)
3. Upload your CSV files
4. Download results ZIP

---

## 3. Binder 🚀

**Best for:** Users who prefer open-source alternatives to Colab

**URL:** [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/MK-vet/MKrep/main)

**Features:**
- No account required
- Open-source platform
- JupyterLab interface
- Works with all notebooks

**Requirements:**
- Web browser
- Internet connection

**Pros:**
- No account needed
- Familiar Jupyter interface
- Open-source infrastructure
- Good for teaching/workshops

**Cons:**
- Can take 5-10 minutes to build environment
- Limited computational resources
- Session timeout
- Slower than Colab

**Quick Start:**
1. Click "Launch Binder" badge
2. Wait for environment to build (~5-10 min first time)
3. Open any notebook
4. Upload data and run analysis

---

## 4. Docker Container 🐳

**Best for:** Reproducible research, deployment on any platform, HPC clusters

**Repository:** https://github.com/MK-vet/MKrep

**Build:**
```bash
docker build -t mkrep:latest .
```

**Run:**
```bash
# Cluster analysis
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
    mkrep:latest mkrep-cluster --data-dir /data --output /output

# With Docker Compose
docker-compose up mkrep-cluster
```

**Requirements:**
- Docker installed
- Input data in local directory

**Pros:**
- Guaranteed reproducibility
- Isolated environment
- Works on any OS with Docker
- Ideal for HPC clusters
- Can run in Google Colab with Docker

**Cons:**
- Requires Docker knowledge
- Initial setup time
- Storage space for images

**See:** [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for complete guide

---

## 5. Local Installation 💻

**Best for:** Power users, custom workflows, large datasets, offline work

**Install:**
```bash
# Clone repository
git clone https://github.com/MK-vet/MKrep.git
cd MKrep

# Install dependencies
pip install -r requirements.txt

# Run analysis
python Cluster_MIC_AMR_Viruelnce.py
```

**Requirements:**
- Python 3.8+ installed
- ~500MB disk space
- Administrator/sudo access (optional, for system packages)

**Pros:**
- Full control over environment
- Fastest execution
- Works offline after setup
- Can modify source code
- No session limits
- Handle very large datasets

**Cons:**
- Requires Python knowledge
- Manual dependency management
- Platform-specific issues possible

**See:** [INSTALLATION.md](INSTALLATION.md) for detailed instructions

---

## 6. Python Package (CLI) 📦

**Best for:** Automation, scripting, batch processing, integration

**Install:**
```bash
pip install mkrep  # When published to PyPI
```

**Use:**
```bash
# Run analyses from command line
mkrep-cluster --data-dir ./data --output ./results
mkrep-mdr --data-dir ./data --output ./results --mdr-threshold 3
mkrep-network --data-dir ./data --output ./results
mkrep-phylo --tree tree.newick --data-dir ./data --output ./results
mkrep-strepsuis --tree tree.newick --data-dir ./data --output ./results
```

**Requirements:**
- Python 3.8+ with pip

**Pros:**
- Clean command-line interface
- Easy to script
- Pipeline integration
- Consistent with Unix philosophy
- Good for automation

**Cons:**
- Less interactive than notebooks
- Requires command-line comfort
- Not yet published to PyPI

**See:** [python_package/README.md](python_package/README.md)

---

## 7. Voilà Dashboard 🎨

**Best for:** Non-programmers, interactive exploration, parameter tuning

**Setup:**
```bash
cd huggingface_demo
pip install -r requirements.txt
voila MKrep_Dashboard.ipynb --port 8866
```

**Access:** http://localhost:8866

**Features:**
- Drag-and-drop file upload
- Parameter sliders and dropdowns
- Real-time progress tracking
- Professional report generation
- No code visible

**Requirements:**
- Local installation
- voila package installed

**Pros:**
- User-friendly GUI
- No coding required
- Interactive parameter adjustment
- Professional interface
- Can deploy to cloud

**Cons:**
- Requires local setup
- Limited to dashboard features
- Not as flexible as scripts

**See:** [huggingface_demo/README.md](huggingface_demo/README.md)

---

## 8. GitHub Actions 🔄

**Best for:** Automated testing, CI/CD, demonstration

**Workflows:**
- `ci.yml` - Continuous integration testing
- `deployment.yml` - Deployment validation
- `quickstart-demo.yml` - Manual demonstration
- `pages.yml` - Documentation portal deployment

**Features:**
- Automatic testing on push
- Cross-platform validation
- Demo tool execution
- Example result generation

**Access:**
- GitHub repository Actions tab
- Triggered automatically or manually

**Pros:**
- Automatic validation
- No local resources needed
- Demonstrates functionality
- Version tracking

**Cons:**
- Not for user analyses
- Limited to demo data
- GitHub account required

**See:** [GITHUB_ACTIONS.md](GITHUB_ACTIONS.md)

---

## Comparison Table

| Feature | Portal | Colab | Binder | Docker | Local | CLI | Dashboard | Actions |
|---------|--------|-------|--------|--------|-------|-----|-----------|---------|
| No Installation | ✅ | ✅ | ✅ | ⚠️ | ❌ | ⚠️ | ❌ | ✅ |
| No Account | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Runs Analysis | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| Offline Work | N/A | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Large Datasets | N/A | ⚠️ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Customization | N/A | ⚠️ | ⚠️ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Ease of Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Setup Time | 0 min | 0 min | 5-10 min | 10-15 min | 15-30 min | 5-10 min | 15-30 min | 0 min |

✅ = Yes/Excellent, ⚠️ = Partial/Limited, ❌ = No/Not Available

---

## Decision Guide

### "I'm reading a scientific article and want to quickly understand the tools"
→ **Use Interactive Web Portal**

### "I want to try the tools without installing anything"
→ **Use Google Colab** (if you have Google account)  
→ **Use Binder** (if you prefer no account)

### "I need to run many analyses with my own data"
→ **Use Local Installation** or **CLI Package**

### "I'm not comfortable with code"
→ **Use Voilà Dashboard** (after local setup)  
→ **Use Google Colab Interactive Notebook**

### "I need guaranteed reproducibility for my publication"
→ **Use Docker Container**

### "I want to integrate tools into my pipeline"
→ **Use CLI Package** or **Local Installation**

### "I need to demonstrate the tools to others"
→ **Use Interactive Web Portal** + **Colab Links**

### "I need maximum computational power"
→ **Use Local Installation** with high-performance hardware  
→ **Use Google Colab Pro** for cloud resources

---

## Technical Support

### For Portal Issues
- GitHub Issues: https://github.com/MK-vet/MKrep/issues
- Check browser console for errors

### For Colab Issues
- See [colab_notebooks/README.md](colab_notebooks/README.md)
- Check Colab runtime type and reset if needed

### For Installation Issues
- See [INSTALLATION.md](INSTALLATION.md)
- Verify Python version (3.8+)
- Check dependency conflicts

### For Docker Issues
- See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)
- Verify Docker installation
- Check volume mounting

---

## Additional Resources

- **Main README:** [README.md](README.md)
- **User Guide:** [USER_GUIDE.md](USER_GUIDE.md)
- **Portal Guide:** [TOOL_PORTAL_GUIDE.md](TOOL_PORTAL_GUIDE.md)
- **Quick Start:** [QUICK_START.md](QUICK_START.md)
- **Features List:** [FEATURES.md](FEATURES.md)

---

**Last Updated:** 2025-10-17  
**Version:** 1.0.0  
**Status:** Production Ready ✅
