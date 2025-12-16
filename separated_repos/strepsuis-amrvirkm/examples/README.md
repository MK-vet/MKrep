# Example Usage Scripts


**Important:** The example datasets are available both in the shared data directory (`../../data/`) and in this module at `data/examples/` to keep tests self-contained. The shared `../../data/` copy is the source of truth; the local copy is synchronized from it for CI and offline testing.

This directory contains example datasets for testing and learning StrepSuis-AMRVirKM.

## Available Examples

### 1. Basic Example (`basic/`)

**Purpose:** Quick test and learning

**Files included:**
- `AMR_genes.csv`
- `MIC.csv`
- `Virulence.csv`

**Dataset size:** ~91 strains, ~21 features per file

**Expected runtime:** ~1-2 minutes

**What you'll see:**
- K-modes clustering with 3 essential data types
- Summary statistics and visualizations
- Interactive HTML reports

**Use case:** First-time users, testing installation

### 2. Advanced Example (`advanced/`)

**Purpose:** Comprehensive analysis with all data types

**Files included:**
- `AMR_genes.csv`
- `MGE.csv`
- `MIC.csv`
- `MLST.csv`
- `Plasmid.csv`
- `Serotype.csv`
- `Virulence.csv`

**Expected runtime:** ~5-8 minutes

**What you'll see:**
- Comprehensive clustering with all metadata and MCA visualization
- More detailed associations and patterns
- Complete metadata integration

**Use case:** Publication-ready analysis, exploring all features

## Using These Examples

### Command Line

```bash
# Basic example
strepsuis-amrvirkm --data-dir ../../data/ --output results_basic/

# Advanced example
strepsuis-amrvirkm --data-dir ../../data/ --output results_advanced/
```

### Python API

```python
from strepsuis_amrvirkm import Analyzer

# Basic example
analyzer = Analyzer(
    data_dir='../../data/',
    output_dir='results_basic/'
)
results = analyzer.run()

# Advanced example with custom parameters
analyzer = Analyzer(
    data_dir='../../data/',
    output_dir='results_advanced/',
    bootstrap_iterations=1000,
    fdr_alpha=0.05
)
results = analyzer.run()
```

### Google Colab
Use the download buttons in the notebook to get these files, or upload them directly.

## Data Format

All example files follow the required format:
- First column: `Strain_ID`
- Binary values: 0 (absent) / 1 (present)
- UTF-8 encoding
- No missing values

## Creating Your Own Data

Use these examples as templates:
1. Keep the same column structure
2. Replace `Strain_ID` values with your strain names
3. Update binary values (0/1) based on your data
4. Ensure no missing values

## Expected Output

Both `basic/` and `advanced/` directories contain `expected_output.txt` files describing what results you should see.

## Questions?

See [USER_GUIDE.md](../USER_GUIDE.md) for detailed data format requirements.
