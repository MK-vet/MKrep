# StrepSuis-AMRPat: Automated Detection of Antimicrobial Resistance Patterns

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/strepsuis-amrpat/blob/main/notebooks/AMRPat_Analysis.ipynb)

**Advanced multidrug resistance pattern detection with bootstrap resampling and network analysis**

## Overview

StrepSuis-AMRPat is a production-ready Python package for advanced bioinformatics analysis. Originally developed for *Streptococcus suis* genomics but applicable to any bacterial species.

### Key Features

- ✅ **Bootstrap resampling for robust prevalence estimation**\n- ✅ **Co-occurrence analysis for phenotypes and resistance genes**\n- ✅ **Association rule mining for resistance patterns**\n- ✅ **Hybrid co-resistance network construction**\n- ✅ **Louvain community detection**\n- ✅ **Publication-quality network visualizations**

## Quick Start

### Installation

```bash
# Install from PyPI
pip install strepsuis-amrpat

# Or install from source
git clone https://github.com/MK-vet/strepsuis-amrpat.git
cd strepsuis-amrpat
pip install -e .
```

### Usage

#### Command Line Interface

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
from strepsuis_amrpat import Analyzer

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
[Open in Google Colab](https://colab.research.google.com/github/MK-vet/strepsuis-amrpat/blob/main/notebooks/AMRPat_Analysis.ipynb)

- Upload your files
- Run all cells
- Download results automatically

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

Required files:
- `MIC.csv`\n- `AMR_genes.csv`

- `Virulence.csv` (optional)\n- `MLST.csv` (optional)\n- `Serotype.csv` (optional)

All CSV files must have:
- **Strain_ID** column (required): Unique identifier for each strain
- **Binary features** (0 = absence, 1 = presence)

Example:
```csv
Strain_ID,Feature1,Feature2,Feature3
Strain001,1,0,1
Strain002,0,1,1
Strain003,1,1,0
```

## Output

Each analysis generates:

1. **HTML Report** - Interactive tables with visualizations
2. **Excel Report** - Multi-sheet workbook with methodology
3. **PNG Charts** - Publication-ready visualizations (150+ DPI)

## Documentation

- **[Installation Guide](docs/INSTALLATION.md)**
- **[User Guide](docs/USER_GUIDE.md)**
- **[API Reference](docs/API.md)**
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

- **GitHub Issues**: [github.com/MK-vet/strepsuis-amrpat/issues](https://github.com/MK-vet/strepsuis-amrpat/issues)
- **Documentation**: [Full Documentation](https://mk-vet.github.io/strepsuis-amrpat/)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Related Tools

Part of the StrepSuis Suite - comprehensive bioinformatics tools for bacterial genomics research.

- [StrepSuis-AMRVirKM](https://github.com/MK-vet/strepsuis-amrvirkm): K-Modes clustering
- [StrepSuis-AMRPat](https://github.com/MK-vet/strepsuis-amrpat): MDR pattern detection
- [StrepSuis-GenPhenNet](https://github.com/MK-vet/strepsuis-genphennet): Network analysis
- [StrepSuis-PhyloTrait](https://github.com/MK-vet/strepsuis-phylotrait): Phylogenetic clustering
- [StrepSuis-GenPhen](https://github.com/MK-vet/strepsuis-genphen): Genomic-phenotypic analysis
