# StrepSuis-AMRPat: Automated Detection of Antimicrobial Resistance Patterns

> **Current Location**: This module is currently part of the [MKrep repository](https://github.com/MK-vet/MKrep) under `separated_repos/strepsuis-amrpat/`. It is designed to become a standalone repository in the future.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/separated_repos/strepsuis-amrpat/notebooks/AMRPat_Analysis.ipynb)
[![Coverage](https://img.shields.io/badge/coverage-62%25-brightgreen)]()

**Advanced multidrug resistance pattern detection with bootstrap resampling and network analysis**

## Overview

StrepSuis-AMRPat is a production-ready Python package for advanced bioinformatics analysis. Originally developed for *Streptococcus suis* genomics but applicable to any bacterial species.

### Key Features

- ✅ **Bootstrap resampling for robust prevalence estimation**
- ✅ **Co-occurrence analysis for phenotypes and resistance genes**
- ✅ **Association rule mining for resistance patterns**
- ✅ **Hybrid co-resistance network construction**
- ✅ **Louvain community detection**
- ✅ **Publication-quality network visualizations**

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- 4GB RAM minimum (8GB recommended for large datasets)

### Installation

> **Note**: This module is currently part of the MKrep repository. Install from the MKrep repository using the instructions below. Future standalone installation will be available once the module is published to its own repository.

#### Option 1: From Current Location (MKrep Repository)
```bash
# Clone the main repository
git clone https://github.com/MK-vet/MKrep.git
cd MKrep/separated_repos/strepsuis-amrpat
pip install -e .
```

#### Option 2: From PyPI (when published)
```bash
pip install strepsuis-amrpat
```

#### Option 3: From Standalone GitHub Repo (future)
```bash
pip install git+https://github.com/MK-vet/strepsuis-amrpat.git
```

#### Option 4: Docker (future)
```bash
docker pull ghcr.io/mk-vet/strepsuis-amrpat:latest
```

### Running Your First Analysis

#### Command Line

```bash
# Run analysis
strepsuis-amrpat --data-dir ./data --output ./results

# With custom parameters
strepsuis-amrpat \
  --data-dir ./data \
  --output ./results \
  --bootstrap 1000 \
  --fdr-alpha 0.05
```

#### Python API

```python
from strepsuis_amrpat import MDRAnalyzer

# Initialize analyzer
analyzer = MDRAnalyzer(
    data_dir="./data",
    output_dir="./results"
)

# Run analysis
results = analyzer.run()

# Check results
print(f"Analysis status: {results['status']}")
print(f"Output directory: {results['output_dir']}")
print(f"Generated files: {results['total_files']}")
```

#### Or use Google Colab (No Installation Required!)

Click the Colab badge at the top of this README to run analysis in your browser.

### Docker

```bash
# Pull and run
docker pull mkvet/strepsuis-amrpat:latest
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
    mkvet/strepsuis-amrpat:latest \
    --data-dir /data --output /output

# Or build locally
docker build -t strepsuis-amrpat .
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
    strepsuis-amrpat --data-dir /data --output /output
```

## Input Data Format

### Required Files

Your data directory must contain:

**Mandatory:**
- `MIC.csv` - Minimum Inhibitory Concentration data (phenotypic resistance)
- `AMR_genes.csv` - Antimicrobial resistance genes (genotypic resistance)

**Optional (but recommended):**
- `Virulence.csv` - Virulence factors
- `MLST.csv` - Multi-locus sequence typing
- `Serotype.csv` - Serological types

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

## Testing

This package includes a comprehensive test suite covering unit tests, integration tests, and full workflow validation.

### Quick Start

```bash
# Install development dependencies
pip install -e .[dev]

# Run all tests
pytest

# Run with coverage
pytest --cov --cov-report=html
```

### Test Categories

- **Unit tests**: Fast tests of individual components
- **Integration tests**: Tests using real example data
- **Workflow tests**: End-to-end pipeline validation

### Running Specific Tests

```bash
# Fast tests only (for development)
pytest -m "not slow"

# Integration tests only
pytest -m integration

# Specific test file
pytest tests/test_workflow.py -v
```

For detailed testing instructions, see [TESTING.md](TESTING.md).

### Coverage

Current test coverage: See badge above or run `pytest --cov --cov-report=html`.

Target coverage: 60% minimum, 80%+ recommended for production.


## Documentation

See [USER_GUIDE.md](USER_GUIDE.md) for detailed installation instructions and usage examples.

- **[Examples](examples/)**

## Citation

If you use StrepSuis-AMRPat in your research, please cite:

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

MIT License - see [LICENSE](LICENSE) file for details

## Support

- **Issues**: [github.com/MK-vet/strepsuis-amrpat/issues](https://github.com/MK-vet/strepsuis-amrpat/issues)
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
docker build -t strepsuis-amrpat:test .
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
