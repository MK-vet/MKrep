# StrepSuis-GenPhen: Interactive Platform for Integrated Genomic-Phenotypic Analysis

> **Current Location**: This module is currently part of the [MKrep repository](https://github.com/MK-vet/MKrep) under `separated_repos/strepsuis-genphen/`. It is designed to become a standalone repository in the future.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/separated_repos/strepsuis-genphen/notebooks/GenPhen_Analysis.ipynb)
[![Coverage](https://img.shields.io/badge/coverage-32%25-orange)]()

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

> **Note**: This module is currently part of the MKrep repository. Install from the MKrep repository using the instructions below. Future standalone installation will be available once the module is published to its own repository.

#### Option 1: From Current Location (MKrep Repository)
```bash
# Clone the main repository
git clone https://github.com/MK-vet/MKrep.git
cd MKrep/separated_repos/strepsuis-genphen
pip install -e .
```

#### Option 2: From PyPI (when published)
```bash
pip install strepsuis-genphen
```

#### Option 3: From Standalone GitHub Repo (future)
```bash
pip install git+https://github.com/MK-vet/strepsuis-genphen.git
```

#### Option 4: Docker (future)
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

**Current test coverage: 32%** (See badge above) ⚠️ Needs Improvement

**Coverage Breakdown**:
- Config & CLI: **83-100%** ✅ Excellent
- Core Orchestration: **78%** ✅ Good  
- Analysis Algorithms: **6%** ⚠️ Limited (validated via E2E tests)
- Overall: **32%**

**What's Tested**:
- ✅ **100+ tests** covering critical paths
- ✅ **Configuration validation** (100% coverage)
- ✅ **CLI interface** (83 coverage)
- ✅ **Workflow orchestration** (78% coverage)
- ✅ **10+ end-to-end tests** validating complete pipelines
- ✅ **Integration tests** with real 92-strain dataset
- ✅ **Error handling** and edge cases

**What's Validated via E2E Tests** (not line-covered):
- Phylogenetic tree processing
- Tree-aware clustering
- Chi-square trait associations
- Random Forest feature importance
- MCA and ensemble methods
- Interactive HTML reports

**Running Coverage Analysis**:
```bash
# Generate HTML coverage report
pytest --cov --cov-report=html
open htmlcov/index.html

# View detailed coverage
pytest --cov --cov-report=term-missing

# Coverage for specific module
pytest --cov=strepsuis_genphen tests/test_analyzer.py -v
```

**Coverage Improvement Goals**:
- Current: 32%
- 🎯 Phase 2 Target: 60%
- 🚀 Phase 3 Target: 80%+

See [../COVERAGE_RESULTS.md](../COVERAGE_RESULTS.md) for detailed coverage analysis across all modules.


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
