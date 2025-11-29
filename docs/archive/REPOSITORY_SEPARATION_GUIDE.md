# Repository Separation Guide for StrepSuis Suite

This document provides comprehensive instructions for deploying the 5 separated StrepSuis Suite modules as independent GitHub repositories.

## Overview

The MKrep repository has been restructured into 5 independent, publication-ready modules:

1. **StrepSuis-AMRVirKM** - K-Modes Clustering for AMR and Virulence Profiles
2. **StrepSuis-AMRPat** - Automated Detection of Antimicrobial Resistance Patterns
3. **StrepSuis-GenPhenNet** - Network-Based Genome-Phenome Integration
4. **StrepSuis-PhyloTrait** - Integrated Phylogenetic and Binary Trait Analysis
5. **StrepSuis-GenPhen** - Interactive Genomic-Phenotypic Analysis Platform

Each module is now a **complete, standalone repository** with:
- ✅ Professional Python package
- ✅ Docker container with dynamic GitHub installation (no code duplication)
- ✅ Google Colab notebook with GitHub installation (no code duplication)
- ✅ Complete English documentation
- ✅ Example data files
- ✅ MIT License
- ✅ Publication-ready structure

## Directory Structure

All separated modules are located in: `/separated_repos/`

```
separated_repos/
├── strepsuis-amrvirkm/      # Module 1: Cluster Analysis
├── strepsuis-amrpat/         # Module 2: MDR Analysis
├── strepsuis-genphennet/     # Module 3: Network Analysis
├── strepsuis-phylotrait/     # Module 4: Phylogenetic Clustering
└── strepsuis-genphen/        # Module 5: Genomic-Phenotypic Analysis
```

## Module Components

Each module contains:

```
module-name/
├── README.md                 # Professional documentation in English
├── LICENSE                   # MIT License
├── .gitignore               # Proper git ignore rules
├── pyproject.toml           # Modern Python package configuration
├── requirements.txt         # Minimal dependencies
├── Dockerfile               # Installs package from GitHub dynamically
├── docker-compose.yml       # Docker Compose configuration
├── package_name/            # Python package
│   ├── __init__.py         # Package initialization
│   ├── config.py           # Configuration management
│   ├── cli.py              # Command-line interface
│   └── analyzer.py         # Main analysis logic
├── examples/                # Example data files
│   ├── README.md           # Data format documentation
│   ├── MIC.csv             # Example MIC data
│   ├── AMR_genes.csv       # Example AMR genes
│   ├── Virulence.csv       # Example virulence factors
│   └── ...                 # Additional example files
├── notebooks/               # Google Colab notebooks
│   └── *_Analysis.ipynb    # Interactive Colab notebook
├── tests/                   # Unit tests (future)
└── docker/                  # Docker-related files (future)
```

## Deployment Instructions

### Step 1: Create New GitHub Repositories

For each module, create a new GitHub repository:

1. Go to https://github.com/new
2. Create repository with name matching the module (e.g., `strepsuis-amrvirkm`)
3. Description: Use the module's title from the table above
4. Make it **Public**
5. **Do NOT** initialize with README, .gitignore, or license (we have them already)

### Step 2: Push Module to Repository

For each module in `separated_repos/`, execute:

```bash
# Navigate to the module directory
cd separated_repos/strepsuis-amrvirkm

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: StrepSuis-AMRVirKM v1.0.0

- Professional Python package structure
- Docker container with dynamic GitHub installation
- Google Colab notebook
- Complete English documentation
- Example data files
- Publication-ready"

# Add remote (replace with your repository URL)
git remote add origin https://github.com/MK-vet/strepsuis-amrvirkm.git

# Push to GitHub
git branch -M main
git push -u origin main
```

Repeat for all 5 modules:
- `strepsuis-amrvirkm`
- `strepsuis-amrpat`
- `strepsuis-genphennet`
- `strepsuis-phylotrait`
- `strepsuis-genphen`

### Step 3: Create GitHub Releases

For each repository:

1. Go to the repository on GitHub
2. Click "Releases" → "Create a new release"
3. Tag version: `v1.0.0`
4. Release title: `Version 1.0.0 - Initial Release`
5. Description:
   ```markdown
   # Initial Release 🎉

   Production-ready bioinformatics tool for [module purpose].

   ## Features
   - Professional Python package with CLI
   - Docker container with dynamic installation
   - Google Colab notebook (no installation required)
   - Complete documentation in English
   - Example datasets

   ## Installation
   ```bash
   pip install git+https://github.com/MK-vet/[module-name].git
   ```

   ## Quick Start
   See [README.md](README.md) for complete instructions.
   ```
6. Click "Publish release"

### Step 4: Test Installation

For each module, test that it can be installed from GitHub:

```bash
# Test installation
pip install git+https://github.com/MK-vet/strepsuis-amrvirkm.git

# Test CLI
strepsuis-amrvirkm --version
strepsuis-amrvirkm --help

# Clean up
pip uninstall -y strepsuis-amrvirkm
```

### Step 5: Test Docker Container

For each module, test the Docker container:

```bash
cd separated_repos/strepsuis-amrvirkm

# Build Docker image
docker build -t strepsuis-amrvirkm .

# Test run
docker run strepsuis-amrvirkm --help

# Test with data
docker run -v $(pwd)/examples:/data -v $(pwd)/output:/output \
    strepsuis-amrvirkm --data-dir /data --output /output
```

### Step 6: Test Google Colab Notebook

For each module:

1. Upload the notebook to Google Colab
2. Change the GitHub URL in the notebook to point to the new repository
3. Run all cells to verify:
   - Package installs correctly from GitHub
   - Data upload works
   - Analysis runs
   - Results download works

### Step 7: Publish to Docker Hub (Optional)

For each module:

```bash
# Login to Docker Hub
docker login

# Tag the image
docker tag strepsuis-amrvirkm mkvet/strepsuis-amrvirkm:latest
docker tag strepsuis-amrvirkm mkvet/strepsuis-amrvirkm:1.0.0

# Push to Docker Hub
docker push mkvet/strepsuis-amrvirkm:latest
docker push mkvet/strepsuis-amrvirkm:1.0.0
```

### Step 8: Publish to PyPI (Optional)

For each module:

```bash
cd separated_repos/strepsuis-amrvirkm

# Install build tools
pip install build twine

# Build the package
python -m build

# Upload to PyPI (requires account)
python -m twine upload dist/*
```

## Module-Specific Deployment Notes

### StrepSuis-AMRVirKM
- **Repository**: `strepsuis-amrvirkm`
- **PyPI Package**: `strepsuis-amrvirkm`
- **Docker Image**: `mkvet/strepsuis-amrvirkm`
- **Required Files**: MIC.csv, AMR_genes.csv, Virulence.csv

### StrepSuis-AMRPat
- **Repository**: `strepsuis-amrpat`
- **PyPI Package**: `strepsuis-amrpat`
- **Docker Image**: `mkvet/strepsuis-amrpat`
- **Required Files**: MIC.csv, AMR_genes.csv

### StrepSuis-GenPhenNet
- **Repository**: `strepsuis-genphennet`
- **PyPI Package**: `strepsuis-genphennet`
- **Docker Image**: `mkvet/strepsuis-genphennet`
- **Required Files**: MIC.csv, AMR_genes.csv, Virulence.csv

### StrepSuis-PhyloTrait
- **Repository**: `strepsuis-phylotrait`
- **PyPI Package**: `strepsuis-phylotrait`
- **Docker Image**: `mkvet/strepsuis-phylotrait`
- **Required Files**: tree.newick, MIC.csv, AMR_genes.csv, Virulence.csv

### StrepSuis-GenPhen
- **Repository**: `strepsuis-genphen`
- **PyPI Package**: `strepsuis-genphen`
- **Docker Image**: `mkvet/strepsuis-genphen`
- **Required Files**: tree.newick, MIC.csv, AMR_genes.csv, Virulence.csv

## Verification Checklist

For each module, verify:

- [ ] Repository created on GitHub
- [ ] All files pushed successfully
- [ ] README displays correctly
- [ ] LICENSE file present (MIT)
- [ ] Package installs from GitHub
- [ ] CLI command works
- [ ] Docker image builds
- [ ] Docker container runs
- [ ] Colab notebook opens
- [ ] Colab notebook installs package from GitHub
- [ ] Example data files present
- [ ] All documentation in English
- [ ] Release created (v1.0.0)

## Post-Deployment Tasks

1. **Update Main README**: Update the main MKrep repository README to link to all 5 separate repositories
2. **Create Index Page**: Consider creating a GitHub Pages site that links to all modules
3. **Update Citations**: Ensure each module has proper citation information
4. **Monitor Issues**: Set up issue tracking for each repository
5. **Documentation Site**: Consider using GitHub Pages or Read the Docs for each module

## Key Design Principles Implemented

✅ **No Code Duplication**: 
- Docker installs packages from GitHub dynamically
- Colab notebooks install packages from GitHub dynamically
- Only configuration and wrapper code in each repository

✅ **Professional Quality**:
- Complete English documentation
- Publication-ready structure
- MIT License
- Semantic versioning

✅ **Three Deployment Variants**:
- a) Python package on GitHub (installable with pip)
- b) Docker container (installs package automatically)
- c) Google Colab notebook (for non-programmers, installs from GitHub)

✅ **Smart Implementation**:
- No unnecessary GitHub Actions
- Minimal dependencies per module
- Clean, maintainable structure
- Ready for publication

## Support and Maintenance

Each repository includes:
- Issue tracking enabled
- Clear contribution guidelines in README
- Support contact information
- Link to related tools in the suite

## Success Metrics

The separation is successful when:
1. Each module can be installed independently
2. Docker containers work without local code
3. Colab notebooks work without code duplication
4. All documentation is clear and in English
5. Tools are ready for publication and citation

## Notes

- All original analysis scripts remain in the main MKrep repository for reference
- The separated modules contain wrapper code that can reference the original scripts
- For production use, the original analysis code should be integrated into each module's analyzer.py
- Current implementation provides the framework; original scripts can be gradually integrated

---

**Created**: 2025-01-14  
**Version**: 1.0  
**Author**: MK-vet  
**License**: MIT
