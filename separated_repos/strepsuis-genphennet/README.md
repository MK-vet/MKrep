# StrepSuis-GenPhenNet: Network-Based Integration of Genome-Phenome Data

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/strepsuis-genphennet/blob/main/notebooks/GenPhenNet_Analysis.ipynb)

**Statistical network analysis for genomic-phenotypic associations**

## Overview

StrepSuis-GenPhenNet is a production-ready Python package for advanced bioinformatics analysis. Originally developed for *Streptococcus suis* genomics but applicable to any bacterial species.

### Key Features

- ✅ **Chi-square and Fisher exact tests with FDR correction**\n- ✅ **Information theory metrics (entropy, mutual information, Cramér's V)**\n- ✅ **Mutually exclusive pattern detection**\n- ✅ **3D network visualization with Plotly**\n- ✅ **Community detection algorithms**\n- ✅ **Interactive HTML reports**

## Quick Start

### Installation

```bash
# Install from PyPI
pip install strepsuis-genphennet

# Or install from source
git clone https://github.com/MK-vet/strepsuis-genphennet.git
cd strepsuis-genphennet
pip install -e .
```

### Usage

#### Command Line Interface

```bash
# Run analysis
strepsuis-genphennet --data-dir ./data --output ./results

# With custom parameters
strepsuis-genphennet \
  --data-dir ./data \
  --output ./results \
  --bootstrap 1000 \
  --fdr-alpha 0.05
```

#### Python API

```python
from strepsuis_genphennet import Analyzer

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
[Open in Google Colab](https://colab.research.google.com/github/MK-vet/strepsuis-genphennet/blob/main/notebooks/GenPhenNet_Analysis.ipynb)

- Upload your files
- Run all cells
- Download results automatically

### Docker

```bash
# Pull and run
docker pull mkvet/strepsuis-genphennet:latest
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
    mkvet/strepsuis-genphennet:latest \
    --data-dir /data --output /output

# Or build locally
docker build -t strepsuis-genphennet .
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
    strepsuis-genphennet --data-dir /data --output /output
```

## Input Data Format

Required files:
- `MIC.csv`\n- `AMR_genes.csv`\n- `Virulence.csv`

- `MLST.csv` (optional)\n- `Serotype.csv` (optional)\n- `Plasmid.csv` (optional)\n- `MGE.csv` (optional)

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

See [USER_GUIDE.md](USER_GUIDE.md) for detailed installation instructions and usage examples.

- **[Examples](examples/)**

## Citation

If you use StrepSuis-GenPhenNet in your research, please cite:

```bibtex
@software{strepsuis_genphennet2025,
  title = {StrepSuis-GenPhenNet: Network-Based Integration of Genome-Phenome Data},
  author = {MK-vet},
  year = {2025},
  url = {https://github.com/MK-vet/strepsuis-genphennet},
  version = {1.0.0}
}
```

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

- **GitHub Issues**: [github.com/MK-vet/strepsuis-genphennet/issues](https://github.com/MK-vet/strepsuis-genphennet/issues)
- **Documentation**: [Full Documentation](https://mk-vet.github.io/strepsuis-genphennet/)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Related Tools

Part of the StrepSuis Suite - comprehensive bioinformatics tools for bacterial genomics research.

- [StrepSuis-AMRVirKM](https://github.com/MK-vet/strepsuis-amrvirkm): K-Modes clustering
- [StrepSuis-AMRPat](https://github.com/MK-vet/strepsuis-amrpat): MDR pattern detection
- [StrepSuis-GenPhenNet](https://github.com/MK-vet/strepsuis-genphennet): Network analysis
- [StrepSuis-PhyloTrait](https://github.com/MK-vet/strepsuis-phylotrait): Phylogenetic clustering
- [StrepSuis-GenPhen](https://github.com/MK-vet/strepsuis-genphen): Genomic-phenotypic analysis
