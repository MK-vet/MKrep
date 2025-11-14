# Example Data

This directory contains example datasets for testing and demonstration purposes.

## Files

### Core Data Files

- **MIC.csv** - Minimum Inhibitory Concentration data
  - Binary resistance/susceptibility data for different antibiotics
  - Format: Strain_ID, Antibiotic1, Antibiotic2, ...
  - Values: 0 (susceptible), 1 (resistant)

- **AMR_genes.csv** - Antimicrobial Resistance Genes
  - Presence/absence of resistance genes
  - Format: Strain_ID, Gene1, Gene2, ...
  - Values: 0 (absent), 1 (present)

- **Virulence.csv** - Virulence Factors
  - Presence/absence of virulence genes
  - Format: Strain_ID, Factor1, Factor2, ...
  - Values: 0 (absent), 1 (present)

### Additional Data Files

- **MLST.csv** - Multi-Locus Sequence Typing
- **Serotype.csv** - Serological types
- **Plasmid.csv** - Plasmid presence/absence
- **MGE.csv** - Mobile Genetic Elements


- **tree.newick** - Phylogenetic tree in Newick format
  - Required for phylogenetic analysis
  - Must include all strains in the dataset


## Data Format Requirements

### General Requirements

1. **File Format:** CSV (Comma-Separated Values)
2. **Encoding:** UTF-8
3. **First Column:** Must be named `Strain_ID`
4. **Strain IDs:** Must be unique
5. **No Missing Values:** Encode as 0 or 1, not NaN

### Binary Data Encoding

**IMPORTANT:** All data must be binary (0/1):

- **0** = Absence (gene not present, susceptible to antibiotic, etc.)
- **1** = Presence (gene present, resistant to antibiotic, etc.)

### Example Format

```csv
Strain_ID,Feature1,Feature2,Feature3
Strain001,1,0,1
Strain002,0,1,1
Strain003,1,1,0
```

## Using Example Data

### Command Line

```bash
# Run analysis with example data
strepsuis-phylotrait --data-dir examples/ --output results/
```

### Python API

```python
from strepsuis_phylotrait import PhyloAnalyzer

analyzer = PhyloAnalyzer(
    data_dir="examples/",
    output_dir="results/"
)

results = analyzer.run()
```

### Docker

```bash
# Run with example data
docker run -v $(pwd)/examples:/data -v $(pwd)/results:/output \
    strepsuis-phylotrait:latest --data-dir /data --output /output
```

## Data Sources

These example datasets are:

- **Synthetic data** for demonstration purposes
- **Representative** of real bacterial genomics data structure
- **Safe to share** (no real patient or strain information)
- **Suitable for testing** tool functionality

## Citation

If you publish results using modified versions of this example data, please cite the tool appropriately (see main README.md).

## Questions?

For questions about data format or requirements:
- See main [README.md](../README.md)
- See [USER_GUIDE.md](../USER_GUIDE.md)
- Open an issue on [GitHub](https://github.com/MK-vet/strepsuis-phylotrait/issues)
