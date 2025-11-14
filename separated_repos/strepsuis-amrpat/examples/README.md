# Example Data for StrepSuis-AMRVirKM

This directory contains example datasets for testing and demonstration purposes.

## Files

- `MIC.csv`: Minimum Inhibitory Concentration data
- `AMR_genes.csv`: Antimicrobial resistance genes
- `Virulence.csv`: Virulence factors
- `MLST.csv`: Multi-locus sequence typing (optional)
- `Serotype.csv`: Serological types (optional)
- `Plasmid.csv`: Plasmid presence/absence (optional)
- `MGE.csv`: Mobile genetic elements (optional)

## Data Format

All CSV files must have:
- **Strain_ID** column (required): Unique identifier for each bacterial strain
- **Binary features** (0 = absence, 1 = presence)

Example structure:

```csv
Strain_ID,Feature1,Feature2,Feature3
Strain001,1,0,1
Strain002,0,1,1
Strain003,1,1,0
```

## Usage

### Python API
```python
from strepsuis_amrvirkm import ClusterAnalyzer

analyzer = ClusterAnalyzer(
    data_dir="examples",
    output_dir="output"
)
results = analyzer.run()
```

### Command Line
```bash
strepsuis-amrvirkm --data-dir examples --output results
```

### Google Colab
Upload these files when prompted in the Colab notebook.

## Data Source

These are example datasets for *Streptococcus suis* strains, demonstrating the expected data format and structure.
