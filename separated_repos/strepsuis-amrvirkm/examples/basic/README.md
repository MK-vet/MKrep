# Basic Example Dataset

This directory contains a minimal set of example data files for quick testing and learning StrepSuis-AMRVirKM.

## Files Included

| File | Description | Features | Strains |
|------|-------------|----------|---------|
| `AMR_genes.csv` | Antimicrobial resistance gene presence/absence | ~21 genes | ~91 strains |
| `MIC.csv` | Minimum inhibitory concentration data | ~14 features | ~91 strains |
| `Virulence.csv` | Virulence factor presence/absence | ~90 factors | ~91 strains |

## Data Format

All files follow the required format:
- **First column**: `Strain_ID` - Unique strain identifier
- **Values**: Binary (0 = absent, 1 = present)
- **Encoding**: UTF-8
- **No missing values**

## Usage

### Command Line

```bash
# Run basic analysis from this directory
cd examples/basic
strepsuis-amrvirkm --data-dir . --output results/

# Or from the package root directory
strepsuis-amrvirkm --data-dir examples/basic/ --output results_basic/
```

### Python API

```python
from strepsuis_amrvirkm import Analyzer

analyzer = Analyzer(
    data_dir='examples/basic/',
    output_dir='results_basic/'
)
results = analyzer.run()
```

## Expected Runtime

- **Time**: 1-2 minutes
- **Memory**: ~500 MB

## Expected Output

See `expected_output.txt` for details on what results you should see.

## What You'll Learn

This basic example demonstrates:
- K-modes clustering with 3 essential data types
- Summary statistics and prevalence tables
- Basic visualizations
- HTML and Excel reports

## Next Steps

After completing this example, try the [advanced example](../advanced/) with all 7 data types for comprehensive analysis.
