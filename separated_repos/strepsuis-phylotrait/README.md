# StrepSuis-PhyloTrait: Integrated Phylogenetic and Binary Trait Analysis

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/strepsuis-phylotrait/blob/main/notebooks/PhyloTrait_Analysis.ipynb)

**Complete phylogenetic and binary trait analysis with tree-aware clustering**

## Overview

StrepSuis-PhyloTrait is a production-ready Python package for advanced bioinformatics analysis. Originally developed for *Streptococcus suis* genomics but applicable to any bacterial species.

### Key Features

- ✅ **Tree-aware clustering with evolutionary metrics**\n- ✅ **Faith's Phylogenetic Diversity calculations**\n- ✅ **Pairwise phylogenetic distance matrices**\n- ✅ **Binary trait analysis for AMR and virulence factors**\n- ✅ **UMAP dimensionality reduction**\n- ✅ **Interactive HTML reports with DataTables and Plotly**

## Quick Start

### Installation

```bash
# Install from PyPI
pip install strepsuis-phylotrait

# Or install from source
git clone https://github.com/MK-vet/strepsuis-phylotrait.git
cd strepsuis-phylotrait
pip install -e .
```

### Usage

#### Command Line Interface

```bash
# Run analysis
strepsuis-phylotrait --data-dir ./data --output ./results

# With custom parameters
strepsuis-phylotrait \
  --data-dir ./data \
  --output ./results \
  --bootstrap 1000 \
  --fdr-alpha 0.05
```

#### Python API

```python
from strepsuis_phylotrait import Analyzer

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
[Open in Google Colab](https://colab.research.google.com/github/MK-vet/strepsuis-phylotrait/blob/main/notebooks/PhyloTrait_Analysis.ipynb)

- Upload your files
- Run all cells
- Download results automatically

### Docker

```bash
# Pull and run
docker pull mkvet/strepsuis-phylotrait:latest
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
    mkvet/strepsuis-phylotrait:latest \
    --data-dir /data --output /output

# Or build locally
docker build -t strepsuis-phylotrait .
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
    strepsuis-phylotrait --data-dir /data --output /output
```

## Input Data Format

Required files:
- `tree.newick`\n- `MIC.csv`\n- `AMR_genes.csv`\n- `Virulence.csv`

- `MLST.csv` (optional)\n- `Serotype.csv` (optional)

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

If you use StrepSuis-PhyloTrait in your research, please cite:

```bibtex
@software{strepsuis_phylotrait2025,
  title = {StrepSuis-PhyloTrait: Integrated Phylogenetic and Binary Trait Analysis},
  author = {MK-vet},
  year = {2025},
  url = {https://github.com/MK-vet/strepsuis-phylotrait},
  version = {1.0.0}
}
```

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

- **GitHub Issues**: [github.com/MK-vet/strepsuis-phylotrait/issues](https://github.com/MK-vet/strepsuis-phylotrait/issues)
- **Documentation**: [Full Documentation](https://mk-vet.github.io/strepsuis-phylotrait/)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Related Tools

Part of the StrepSuis Suite - comprehensive bioinformatics tools for bacterial genomics research.

- [StrepSuis-AMRVirKM](https://github.com/MK-vet/strepsuis-amrvirkm): K-Modes clustering
- [StrepSuis-AMRPat](https://github.com/MK-vet/strepsuis-amrpat): MDR pattern detection
- [StrepSuis-GenPhenNet](https://github.com/MK-vet/strepsuis-genphennet): Network analysis
- [StrepSuis-PhyloTrait](https://github.com/MK-vet/strepsuis-phylotrait): Phylogenetic clustering
- [StrepSuis-GenPhen](https://github.com/MK-vet/strepsuis-genphen): Genomic-phenotypic analysis
