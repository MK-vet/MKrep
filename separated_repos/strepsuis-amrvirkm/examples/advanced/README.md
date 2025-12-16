# Advanced Example Dataset

This directory contains the complete set of example data files for comprehensive analysis with StrepSuis-AMRVirKM.

## Files Included

| File | Description | Features | Strains |
|------|-------------|----------|---------|
| `AMR_genes.csv` | Antimicrobial resistance gene presence/absence | ~21 genes | ~91 strains |
| `MIC.csv` | Minimum inhibitory concentration data | ~14 features | ~91 strains |
| `Virulence.csv` | Virulence factor presence/absence | ~90 factors | ~91 strains |
| `MLST.csv` | Multi-locus sequence typing data | ~7 alleles | ~91 strains |
| `Serotype.csv` | Serotype classification | ~6 types | ~91 strains |
| `MGE.csv` | Mobile genetic elements | ~8 elements | ~91 strains |
| `Plasmid.csv` | Plasmid presence/absence | ~3 plasmids | ~91 strains |

## Data Format

All files follow the required format:
- **First column**: `Strain_ID` - Unique strain identifier
- **Values**: Binary (0 = absent, 1 = present)
- **Encoding**: UTF-8
- **No missing values**

## Usage

### Command Line

```bash
# Run advanced analysis from this directory
cd examples/advanced
strepsuis-amrvirkm --data-dir . --output results/

# Or from the package root directory
strepsuis-amrvirkm --data-dir examples/advanced/ --output results_advanced/
```

### Python API

```python
from strepsuis_amrvirkm import Analyzer

analyzer = Analyzer(
    data_dir='examples/advanced/',
    output_dir='results_advanced/',
    bootstrap_iterations=1000,
    fdr_alpha=0.05
)
results = analyzer.run()
```

## Expected Runtime

- **Time**: 5-8 minutes
- **Memory**: ~1 GB

## Expected Output

See `expected_output.txt` for details on what results you should see.

## What You'll Learn

This advanced example demonstrates:
- Comprehensive K-modes clustering with all 7 data types
- MCA (Multiple Correspondence Analysis) visualization
- Complete metadata integration
- Advanced statistical associations
- Publication-ready charts and reports

## Data Integration

This example shows how different data types integrate:
- **AMR + Virulence**: Core resistance and virulence profiles
- **MLST + Serotype**: Phylogenetic context
- **MGE + Plasmid**: Mobile genetic element analysis

## Best Practices

1. **Memory**: Ensure at least 2 GB RAM available
2. **Output**: Use a dedicated output directory to avoid overwriting
3. **Interpretation**: Review the HTML report for interactive visualizations
