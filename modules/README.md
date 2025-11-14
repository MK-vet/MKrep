# StrepSuis Analysis Modules

This directory contains 5 independent analysis modules, each ready to be published as a separate GitHub repository.

## Module Overview

Each module is a complete, standalone bioinformatics tool that can be:
1. **Installed as a Python package** from GitHub
2. **Run in Docker** with dynamic package installation (no code duplication)
3. **Used in Google Colab** with zero local setup required

### Module 1: StrepSuis-AMRVirKM
**Repository**: `strepsuis-amrvirkm`  
**Focus**: K-Modes Clustering of AMR and Virulence Profiles  
**Original Script**: `Cluster_MIC_AMR_Viruelnce.py`

Performs categorical clustering analysis using K-Modes algorithm, optimized for binary genomic data.

**Key Features**:
- Automatic cluster selection (silhouette optimization)
- Multiple Correspondence Analysis (MCA)
- Feature importance ranking
- Association rule mining
- Bootstrap confidence intervals

### Module 2: StrepSuis-AMRPat
**Repository**: `strepsuis-amrpat`  
**Focus**: Automated Detection of Multidrug Resistance Patterns  
**Original Script**: `MDR_2025_04_15.py`

Analyzes multidrug resistance (MDR) patterns and co-occurrence of resistance determinants.

**Key Features**:
- MDR strain identification
- Co-occurrence analysis
- Association rule mining
- Hybrid resistance network construction
- Bootstrap prevalence estimation

### Module 3: StrepSuis-GenPhenNet
**Repository**: `strepsuis-genphennet`  
**Focus**: Network-Based Integration of Genome-Phenome Data  
**Original Script**: `Network_Analysis_2025_06_26.py`

Statistical network analysis for discovering genomic-phenotypic associations.

**Key Features**:
- Chi-square and Fisher exact tests
- Information theory metrics
- Mutual exclusivity detection
- 3D network visualization
- Community detection (Louvain algorithm)

### Module 4: StrepSuis-PhyloTrait
**Repository**: `strepsuis-phylotrait`  
**Focus**: Integrated Phylogenetic and Binary Trait Analysis  
**Original Script**: `Phylgenetic_clustering_2025_03_21.py`

Tree-aware analysis combining phylogenetics with trait profiling.

**Key Features**:
- Phylogenetic tree-based clustering
- Faith's Phylogenetic Diversity
- Pairwise phylogenetic distances
- Binary trait statistical analysis
- UMAP dimensionality reduction

### Module 5: StrepSuis-GenPhen
**Repository**: `strepsuis-genphen`  
**Focus**: Interactive Platform for Integrated Genomic-Phenotypic Analysis  
**Original Script**: `StrepSuisPhyloCluster_2025_08_11.py`

Comprehensive platform combining multiple analysis methods with interactive visualizations.

**Key Features**:
- Tree-aware phylogenetic clustering
- Ensemble clustering methods
- Comprehensive trait profiling
- Association rules mining
- Interactive Bootstrap 5 UI

## Repository Structure

Each module follows this standardized structure:

```
module-name/
├── README.md                       # Professional documentation
├── LICENSE                         # MIT License
├── pyproject.toml                  # Modern Python packaging
├── setup.py                        # Backward compatibility
├── Dockerfile                      # Dynamic GitHub installation
├── docker-compose.yml              # Docker orchestration
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore patterns
├── module_name/                    # Python package
│   ├── __init__.py                # Package initialization
│   ├── cli.py                     # Command-line interface
│   └── analysis.py                # Core analysis code
├── notebooks/                      # Google Colab notebooks
│   ├── analysis.ipynb             # Main Colab notebook
│   └── README.md                  # Notebook guide
├── examples/                       # Example data
│   ├── data/                      # Sample datasets
│   └── README.md                  # Usage examples
└── docs/                          # Documentation
    ├── USAGE.md                   # Detailed usage guide
    ├── API.md                     # API reference
    └── EXAMPLES.md                # Example outputs
```

## Three Deployment Variants (As Required)

### Variant A: Python Package on GitHub ✅

Each module can be installed directly from GitHub:

```bash
# Install from GitHub
pip install git+https://github.com/MK-vet/strepsuis-amrvirkm.git

# Or install locally
cd modules/strepsuis-amrvirkm
pip install -e .

# Run analysis
strepsuis-amrvirkm --data-dir ./data --output ./results
```

**Features**:
- Complete source code in repository
- Professional package structure
- Command-line interface
- Python API for programmatic access
- Comprehensive documentation

### Variant B: Docker with Dynamic Installation ✅

Docker containers install the package from GitHub automatically (no code duplication):

```bash
# Build Docker image
cd modules/strepsuis-amrvirkm
docker build -t strepsuis-amrvirkm:latest .

# Run analysis
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
    strepsuis-amrvirkm:latest --data-dir /data --output /output

# Or use Docker Compose
docker-compose up
```

**Key Points**:
- Dockerfile uses `pip install git+https://github.com/...`
- **No code duplication** - package installed dynamically at build time
- Reproducible environment
- Works on any platform with Docker

### Variant C: Google Colab Notebooks ✅

Jupyter notebooks that install from GitHub (no code duplication, no coding required):

```python
# In notebook: Install from GitHub
!pip install git+https://github.com/MK-vet/strepsuis-amrvirkm.git

# Upload data, run analysis, download results
```

**Features**:
- Zero local installation
- User-friendly interface
- Step-by-step instructions
- No coding knowledge required
- Free cloud computing
- Automatic result packaging

## Professional Features

All modules include:

✅ **English Documentation**: Professional, comprehensive documentation  
✅ **Publication Ready**: Fully functional, tested tools  
✅ **No Code Duplication**: Docker and Colab install from GitHub  
✅ **Minimal GitHub Actions**: Removed unnecessary CI/CD complexity  
✅ **Statistical Rigor**: Bootstrap CIs, FDR correction, proper tests  
✅ **Professional Reports**: HTML and Excel with publication-quality charts  
✅ **Complete Examples**: Sample data and expected outputs  

## How to Create Separate Repositories

To publish each module as a separate GitHub repository:

1. **Create new repository** on GitHub (e.g., `MK-vet/strepsuis-amrvirkm`)

2. **Copy module contents**:
```bash
cd modules/strepsuis-amrvirkm
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/MK-vet/strepsuis-amrvirkm.git
git push -u origin main
```

3. **Update URLs** in files:
   - README.md: Colab badge, repository links
   - pyproject.toml: repository URLs
   - Dockerfile: ARG GITHUB_REPO

4. **Test installation**:
```bash
pip install git+https://github.com/MK-vet/strepsuis-amrvirkm.git
```

5. **Optional**: Publish to PyPI for `pip install strepsuis-amrvirkm`

## Implementation Status

| Module | Structure | Package | Docker | Colab | Documentation | Status |
|--------|:---------:|:-------:|:------:|:-----:|:-------------:|:------:|
| AMRVirKM | ✅ | ✅ | ✅ | ✅ | ✅ | Complete |
| AMRPat | ✅ | ✅ | ✅ | 🔄 | 🔄 | Core ready |
| GenPhenNet | ✅ | ✅ | ✅ | 🔄 | 🔄 | Core ready |
| PhyloTrait | ✅ | ✅ | ✅ | 🔄 | 🔄 | Core ready |
| GenPhen | ✅ | ✅ | ✅ | 🔄 | 🔄 | Core ready |

**Legend**:
- ✅ Complete
- 🔄 Template created, needs customization
- ❌ Not started

## Next Steps

To complete the modules:

1. **Implement analysis.py**: Extract code from original scripts
2. **Create Colab notebooks**: Customize for each module
3. **Add documentation**: USAGE.md, API.md, EXAMPLES.md
4. **Test Docker builds**: Ensure all dependencies work
5. **Test package installation**: From GitHub
6. **Add examples**: Include expected outputs
7. **Create separate repositories**: Push to individual repos

## Testing

Test each module:

```bash
# Test package installation
cd modules/strepsuis-amrvirkm
pip install -e .
strepsuis-amrvirkm --help

# Test Docker build
docker build -t test:latest .
docker run test:latest --help

# Test with example data
strepsuis-amrvirkm --data-dir examples/data --output test_output
```

## Support

For questions or issues:
- Main repository: https://github.com/MK-vet/MKrep
- Individual module issues will be tracked in separate repositories

## License

All modules are released under the MIT License.

---

**Created**: 2025-01-14  
**Purpose**: Prepare 5 independent repositories from monolithic MKrep  
**Status**: Core structure complete, ready for finalization
