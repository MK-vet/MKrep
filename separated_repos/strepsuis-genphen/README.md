# StrepSuis-GenPhen: Interactive Platform for Integrated Genomic-Phenotypic Analysis

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/strepsuis-genphen/blob/main/notebooks/GenPhen_Analysis.ipynb)

**Integrative genomic-phenotypic analysis platform for Streptococcus suis**

## Overview

StrepSuis-GenPhen is a production-ready Python package for advanced bioinformatics analysis. Originally developed for *Streptococcus suis* genomics but applicable to any bacterial species.

### Key Features

- ✅ **Tree-aware phylogenetic clustering with ensemble fallback**
- ✅ **Comprehensive trait profiling (chi-square, log-odds, RF importance)**
- ✅ **Association rules mining**
- ✅ **Multiple Correspondence Analysis (MCA)**
- ✅ **Interactive Bootstrap 5 UI**
- ✅ **Full CSV export capabilities**

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- 4GB RAM minimum (8GB recommended for large datasets)

### Installation

#### Option 1: From PyPI (when published)
```bash
pip install strepsuis-genphen
```

#### Option 2: From GitHub
```bash
pip install git+https://github.com/MK-vet/strepsuis-genphen.git
```

#### Option 3: From Source
```bash
git clone https://github.com/MK-vet/strepsuis-genphen.git
cd strepsuis-genphen
pip install -e .
```

#### Option 4: Docker
```bash
docker pull ghcr.io/mk-vet/strepsuis-genphen:latest
```

### Running Your First Analysis

#### Command Line

```bash
# Run analysis
strepsuis-genphen --data-dir ./data --output ./results

# With custom parameters
strepsuis-genphen \
  --data-dir ./data \
  --output ./results \
  --bootstrap 1000 \
  --fdr-alpha 0.05
```

#### Python API

```python
from strepsuis_genphen import Analyzer

# Initialize analyzer
analyzer = Analyzer(
    data_dir="./data",
    output_dir="./results"
)

# Run analysis
results = analyzer.run()

# Generate reports
analyzer.generate_html_report(results)
analyzer.generate_excel_report(results)
```

#### Google Colab (No Installation!)

Click the badge above or use this link:
[Open in Google Colab](https://colab.research.google.com/github/MK-vet/strepsuis-genphen/blob/main/notebooks/GenPhen_Analysis.ipynb)

- Upload your files
- Run all cells
- Download results automatically

### Docker

```bash
# Pull and run
docker pull mkvet/strepsuis-genphen:latest
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
    mkvet/strepsuis-genphen:latest \
    --data-dir /data --output /output

# Or build locally
docker build -t strepsuis-genphen .
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
    strepsuis-genphen --data-dir /data --output /output
```

## Input Data Format

### Required Files

Your data directory must contain:

**Mandatory:**
- `AMR_genes.csv` - Antimicrobial resistance genes
- `MIC.csv` - Minimum Inhibitory Concentration data

**Optional (but recommended):**
- `Virulence.csv` - Virulence factors
- `MLST.csv` - Multi-locus sequence typing
- `Serotype.csv` - Serological types
- `tree.newick` or `tree.nwk` - Phylogenetic tree (enables tree-aware clustering)

### File Format Requirements

All CSV files must have:
1. **Strain_ID** column (first column, required)
2. **Binary features**: 0 = absence, 1 = presence
3. No missing values (use 0 or 1 explicitly)
4. UTF-8 encoding

#### Example CSV structure:

```csv
Strain_ID,Feature1,Feature2,Feature3
Strain001,1,0,1
Strain002,0,1,1
Strain003,1,1,0
```

See [examples/](examples/) directory for complete example datasets.

## Output

Each analysis generates:

1. **HTML Report** - Interactive tables with visualizations
2. **Excel Report** - Multi-sheet workbook with methodology
3. **PNG Charts** - Publication-ready visualizations (150+ DPI)

## Documentation

See [USER_GUIDE.md](USER_GUIDE.md) for detailed installation instructions and usage examples.

- **[Examples](examples/)**

## Citation

If you use StrepSuis-GenPhen in your research, please cite:

```bibtex
@software{strepsuis_genphen2025,
  title = {StrepSuis-GenPhen: Interactive Platform for Integrated Genomic-Phenotypic Analysis},
  author = {MK-vet},
  year = {2025},
  url = {https://github.com/MK-vet/strepsuis-genphen},
  version = {1.0.0}
}
```

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

- **Issues**: [github.com/MK-vet/strepsuis-genphen/issues](https://github.com/MK-vet/strepsuis-genphen/issues)
- **Documentation**: See [USER_GUIDE.md](USER_GUIDE.md)
- **Main Project**: [StrepSuis Suite](https://github.com/MK-vet/StrepSuis_Suite)

## Development

### Running Tests Locally (Recommended)

To save GitHub Actions minutes, run tests locally before pushing:

```bash
# Install dev dependencies
pip install -e .[dev]

# Run pre-commit checks
pre-commit run --all-files

# Run tests
pytest --cov --cov-report=html

# Build Docker image
docker build -t strepsuis-genphen:test .
```

### GitHub Actions

Automated workflows run on:
- Pull requests to main
- Manual trigger (Actions tab > workflow > Run workflow)
- Release creation

**Note:** Workflows do NOT run on every commit to conserve GitHub Actions minutes.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Related Tools

Part of the StrepSuis Suite - comprehensive bioinformatics tools for bacterial genomics research.

- [StrepSuis-AMRVirKM](https://github.com/MK-vet/strepsuis-amrvirkm): K-Modes clustering
- [StrepSuis-AMRPat](https://github.com/MK-vet/strepsuis-amrpat): MDR pattern detection
- [StrepSuis-GenPhenNet](https://github.com/MK-vet/strepsuis-genphennet): Network analysis
- [StrepSuis-PhyloTrait](https://github.com/MK-vet/strepsuis-phylotrait): Phylogenetic clustering
- [StrepSuis-GenPhen](https://github.com/MK-vet/strepsuis-genphen): Genomic-phenotypic analysis
