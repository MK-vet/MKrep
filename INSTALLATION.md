# MKrep Installation Guide

Complete guide for installing and using MKrep analysis tools in different environments.

## Table of Contents

1. [Quick Verification (GitHub Actions)](#quick-verification-github-actions)
2. [Local Installation](#local-installation)
3. [Google Colab](#google-colab)
4. [Python Package](#python-package)
5. [Hugging Face Demo](#hugging-face-demo)
6. [Docker](#docker)
7. [Troubleshooting](#troubleshooting)

---

## Quick Verification (GitHub Actions)

All MKrep tools are continuously tested and can be verified running from GitHub Actions:

- **No installation needed** - View automated tests to see all tools working
- **Status badges** on README show current CI status
- **Manual demos** can be triggered from the Actions tab
- **Version information** collected automatically

**To view tools running from GitHub**:
1. Visit [MKrep Actions](https://github.com/MK-vet/MKrep/actions)
2. Select "Quick Start Demo" workflow
3. Click "Run workflow" to see interactive demonstration
4. View "CI - All Tools" for automatic test results

See [GITHUB_ACTIONS.md](GITHUB_ACTIONS.md) for complete documentation.

**Supported configurations (all verified by CI)**:
- Python 3.8, 3.9, 3.10, 3.11, 3.12 ✅
- Ubuntu, Windows, macOS ✅
- All deployment options (scripts, CLI, Voilà, notebooks) ✅

---

## Local Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning repository)

### Quick Start

```bash
# Clone repository
git clone https://github.com/MK-vet/MKrep.git
cd MKrep

# Install dependencies
pip install -r requirements.txt

# Run analysis (example)
python Cluster_MIC_AMR_Viruelnce.py
```

### Full Installation

```bash
# Create virtual environment (recommended)
python -m venv mkrep_env
source mkrep_env/bin/activate  # On Windows: mkrep_env\Scripts\activate

# Install all dependencies
pip install pandas numpy scipy matplotlib seaborn plotly
pip install scikit-learn biopython umap-learn networkx
pip install statsmodels mlxtend prince jinja2
pip install openpyxl kaleido pillow
pip install kmodes optuna python-louvain ydata-profiling
pip install joblib numba tqdm psutil xlsxwriter

# Verify installation
python -c "import pandas, numpy, sklearn, plotly; print('✓ All packages installed')"
```

### requirements.txt

Create a `requirements.txt` file:

```
pandas>=1.3.0
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.4.0
seaborn>=0.11.0
plotly>=5.0.0
scikit-learn>=1.0.0
biopython>=1.79
umap-learn>=0.5.0
networkx>=2.6.0
statsmodels>=0.13.0
mlxtend>=0.19.0
prince>=0.7.0
jinja2>=3.0.0
openpyxl>=3.0.0
kaleido>=0.2.0
pillow>=8.0.0
tqdm>=4.62.0
kmodes>=0.12.0
optuna>=3.0.0
python-louvain>=0.15
ydata-profiling>=4.0.0
joblib>=1.1.0
numba>=0.55.0
psutil>=5.8.0
xlsxwriter>=3.0.0
```

Then install: `pip install -r requirements.txt`

---

## Google Colab

### Quick Start

1. Open [Google Colab](https://colab.research.google.com/)
2. Click **File → Open notebook → GitHub**
3. Enter: `MK-vet/MKrep`
4. Select a notebook from `colab_notebooks/`
5. Run all cells

### Direct Links

- [Cluster Analysis](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Cluster_Analysis_Colab.ipynb)
- [MDR Analysis](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/MDR_Analysis_Colab.ipynb)
- [Network Analysis](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Network_Analysis_Colab.ipynb)
- [Phylogenetic Clustering](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Phylogenetic_Clustering_Colab.ipynb)
- [StrepSuis Analysis](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/StrepSuis_Analysis_Colab.ipynb)

### Features

- ✓ No installation required
- ✓ Free GPU/TPU access
- ✓ File upload/download
- ✓ Google Drive integration
- ✓ Automatic package installation

### Tips

1. **GPU Runtime**: Runtime → Change runtime type → GPU (for faster processing)
2. **Save Results**: Download frequently or mount Google Drive
3. **Session Limits**: ~12 hours, re-run cells if disconnected
4. **Large Files**: Use Google Drive for datasets > 100 MB

---

## Python Package

### Installation from PyPI (when published)

```bash
pip install mkrep
```

### Installation from Source

```bash
# Clone repository
git clone https://github.com/MK-vet/MKrep.git
cd MKrep/python_package

# Install package
pip install -e .

# Verify installation
mkrep --version
```

### Usage

#### Command Line

```bash
# Cluster analysis
mkrep-cluster --data-dir ./data --output ./results

# MDR analysis
mkrep-mdr --data-dir ./data --output ./results

# Network analysis
mkrep-network --data-dir ./data --output ./results

# Phylogenetic clustering
mkrep-phylo --tree tree.newick --data-dir ./data --output ./results

# StrepSuis analysis
mkrep-strepsuis --tree tree.newick --data-dir ./data --output ./results
```

#### Python API

```python
from mkrep.analysis import ClusterAnalyzer

# Initialize analyzer
analyzer = ClusterAnalyzer(
    data_dir="./data",
    output_dir="./results",
    max_clusters=8,
    bootstrap_iterations=500
)

# Run analysis
results = analyzer.run()

# Generate reports
analyzer.generate_html_report(results)
analyzer.generate_excel_report(results)
```

### Configuration File

Create `config.json`:

```json
{
  "data_dir": "./data",
  "output_dir": "./results",
  "clustering": {
    "max_clusters": 10,
    "bootstrap_iterations": 500
  },
  "statistics": {
    "fdr_alpha": 0.05
  }
}
```

Use: `mkrep-cluster --config config.json`

---

## Hugging Face Demo

### Access Online

Visit: https://huggingface.co/spaces/MK-vet/mkrep-demo

### Run Locally

```bash
# Install Voilà
pip install voila ipywidgets

# Clone repository
git clone https://github.com/MK-vet/MKrep.git
cd MKrep/huggingface_demo

# Install dependencies
pip install -r requirements.txt

# Launch dashboard
voila MKrep_Dashboard.ipynb --port 8866
```

Open: http://localhost:8866

### Features

- ✓ Web-based interface
- ✓ File upload with drag-and-drop
- ✓ Interactive parameter configuration
- ✓ Real-time analysis progress
- ✓ Report download (HTML, Excel)
- ✓ Interactive visualizations

---

## Docker

### Using Docker

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone repository
RUN git clone https://github.com/MK-vet/MKrep.git .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set entrypoint
CMD ["python"]
```

Build and run:

```bash
# Build image
docker build -t mkrep .

# Run analysis
docker run -v $(pwd)/data:/app/data -v $(pwd)/results:/app/results mkrep \
    python Cluster_MIC_AMR_Viruelnce.py
```

### Docker Compose

```yaml
version: '3.8'

services:
  mkrep:
    build: .
    volumes:
      - ./data:/app/data
      - ./results:/app/results
    environment:
      - OUTPUT_DIR=/app/results
```

Run: `docker-compose up`

---

## Troubleshooting

### Common Issues

#### 1. "Module not found: kmodes"

```bash
pip install kmodes
```

#### 2. "Cannot save plotly figure as PNG"

Install kaleido:
```bash
pip install kaleido
```

Or use fallback HTML output (automatic).

#### 3. "Memory error" during analysis

- Reduce dataset size
- Increase system RAM
- Use data chunking
- Reduce bootstrap iterations

#### 4. "Permission denied" when saving results

```bash
# Check permissions
ls -la output/

# Fix permissions
chmod -R 755 output/
```

#### 5. Python version issues

MKrep requires Python >= 3.8. Check:
```bash
python --version
```

Upgrade if needed:
```bash
# Ubuntu/Debian
sudo apt-get install python3.9

# macOS
brew install python@3.9
```

#### 6. Dependency conflicts

Create isolated environment:
```bash
python -m venv mkrep_env
source mkrep_env/bin/activate
pip install -r requirements.txt
```

### Platform-Specific Issues

#### Windows

- Use `py` instead of `python`
- Use backslashes in paths: `.\data` instead of `./data`
- Install Visual C++ Build Tools if required

#### macOS

- Install Xcode Command Line Tools: `xcode-select --install`
- Use Homebrew for Python: `brew install python@3.9`

#### Linux

- Install build dependencies: `sudo apt-get install build-essential python3-dev`
- For CentOS/RHEL: `sudo yum install gcc python3-devel`

### Getting Help

1. Check [GitHub Issues](https://github.com/MK-vet/MKrep/issues)
2. Review documentation in repository README
3. Open a new issue with:
   - Error message (full traceback)
   - Python version
   - Operating system
   - Steps to reproduce

---

## Performance Tips

### Speed Optimization

1. **Use fewer bootstrap iterations** for testing:
   ```bash
   mkrep-cluster --bootstrap 100  # Instead of 500
   ```

2. **Reduce data dimensions** before analysis:
   - Remove constant features
   - Filter low-variance features

3. **Use parallel processing** (automatic in most scripts)

4. **GPU acceleration** (Google Colab):
   - Runtime → Change runtime type → GPU

### Memory Optimization

1. **Process data in chunks**
2. **Remove intermediate files** after analysis
3. **Use data type optimization**:
   ```python
   df = pd.read_csv('data.csv', dtype={'feature': 'int8'})
   ```

---

## Next Steps

After installation:

1. **Read the documentation**: [README.md](../README.md)
2. **Try example notebooks**: Start with Colab notebooks
3. **Run on your data**: Follow data format guidelines
4. **Explore results**: HTML and Excel reports
5. **Cite the tool**: See repository for citation

---

## Updates

Check for updates regularly:

```bash
cd MKrep
git pull origin main
pip install -r requirements.txt --upgrade
```

---

**Last Updated**: 2025-01-07  
**Version**: 1.0.0
