# Data Directory

This module uses the shared example datasets from the main MKrep repository.

## Data Location

The example datasets are located in the main repository at:
```
../../data/
```
A synchronized copy is also stored locally in `data/examples/` for tests and offline usage. The files mirror the shared datasets to keep fixtures self-contained.

## Available Datasets

The following files are available in the main data directory:

- **AMR_genes.csv** - Antimicrobial resistance gene profiles
- **MGE.csv** - Mobile genetic elements data
- **MIC.csv** - Minimum inhibitory concentration values
- **MLST.csv** - Multi-locus sequence typing data
- **Plasmid.csv** - Plasmid information
- **Serotype.csv** - Serotype classifications
- **Virulence.csv** - Virulence factor profiles
- **Snp_tree.newick** - Phylogenetic tree (for modules that need it)
- **merged_resistance_data.csv** - Pre-merged resistance data

## Usage

When running analyses, use the `--data-dir` option to point to the main data directory:

```bash
# From the module directory
strepsuis-amrvirkm cluster --data-dir ../../data/ --output ./results/

# Or from the main repository root
strepsuis-amrvirkm cluster --data-dir ./data/ --output ./separated_repos/strepsuis-amrvirkm/results/
```

## Generating Results

To generate example analysis results:

```bash
# Install the module
pip install -e .

# Run clustering analysis with example data
strepsuis-amrvirkm cluster \
  --amr-file ../../data/AMR_genes.csv \
  --virulence-file ../../data/Virulence.csv \
  --output ./results/ \
  --n-clusters 3 \
  --random-seed 42
```

Results will be saved to `./results/` and will include:
- HTML interactive report
- Excel workbook with multiple sheets
- PNG charts directory with publication-quality figures

## Note

This structure eliminates data duplication across modules while maintaining independence.
Each module can still be deployed standalone by copying the necessary data files from the main repository.
