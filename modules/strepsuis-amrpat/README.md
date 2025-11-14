# StrepSuis-AMRPat: Automated Detection of Antimicrobial Resistance Patterns

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/strepsuis-amrpat/blob/main/notebooks/mdr_analysis.ipynb)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://hub.docker.com)

## Overview

Automated Detection of Antimicrobial Resistance Patterns for *Streptococcus suis* and other bacterial genomics data.

This tool is part of the StrepSuis Suite of bioinformatics analysis tools, designed for comprehensive genomic and phenotypic analysis.

### Key Features

- Professional, publication-ready reports (HTML and Excel)
- High-quality visualizations (150+ DPI PNG exports)
- Statistical rigor with bootstrap confidence intervals
- Comprehensive documentation and examples
- Multiple deployment options (Colab, Docker, CLI, Local)

## Quick Start

### Option 1: Google Colab (Recommended) ⭐

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/strepsuis-amrpat/blob/main/notebooks/mdr_analysis.ipynb)

**No installation required!** Just click the badge and follow the notebook instructions.

### Option 2: Python Package

```bash
# Install from GitHub
pip install git+https://github.com/MK-vet/strepsuis-amrpat.git

# Run analysis
strepsuis-amrpat --data-dir ./data --output ./results
```

### Option 3: Docker

```bash
# Build and run
docker build -t strepsuis-amrpat:latest .
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
    strepsuis-amrpat:latest --data-dir /data --output /output
```

### Option 4: Local Installation

```bash
git clone https://github.com/MK-vet/strepsuis-amrpat.git
cd strepsuis-amrpat
pip install -r requirements.txt
python -m strepsuis_amrpat.cli --data-dir ./examples/data --output ./results
```

## Input Data Format

See [docs/USAGE.md](docs/USAGE.md) for detailed data format requirements.

Required files:
- Binary CSV files with `Strain_ID` column
- Values: 0 (absence) or 1 (presence)


## Output Files

- Interactive HTML report
- Excel workbook with multiple sheets
- High-quality PNG charts (150+ DPI)

## Documentation

- [README.md](README.md) - This file
- [docs/USAGE.md](docs/USAGE.md) - Detailed usage guide
- [docs/API.md](docs/API.md) - Python API documentation
- [docs/EXAMPLES.md](docs/EXAMPLES.md) - Example analyses
- [notebooks/README.md](notebooks/README.md) - Colab notebook guide

## Citation

```bibtex
@software{strepsuis_amrpat2025,
  title = {StrepSuis-AMRPat: Automated Detection of Antimicrobial Resistance Patterns},
  author = {MK-vet},
  year = {2025},
  url = {https://github.com/MK-vet/strepsuis-amrpat},
  version = {1.0.0}
}
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Related Projects

- **StrepSuis-AMRVirKM**: K-Modes clustering
- **StrepSuis-AMRPat**: MDR pattern detection
- **StrepSuis-GenPhenNet**: Network analysis
- **StrepSuis-PhyloTrait**: Phylogenetic clustering
- **StrepSuis-GenPhen**: Integrated analysis

---

**Version**: 1.0.0  
**Last Updated**: 2025-01-14  
**Maintainer**: MK-vet
