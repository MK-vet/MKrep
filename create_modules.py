#!/usr/bin/env python3
"""
Template generator for creating separate repository structures.
This script automates the creation of the remaining 4 modules.
"""

import os
import shutil
from pathlib import Path
from typing import Dict

# Module configurations
MODULES = {
    "strepsuis-mdr": {
        "name": "StrepSuis-AMRPat",
        "title": "Automated Detection of Antimicrobial Resistance Patterns",
        "description": "Advanced multidrug resistance pattern detection with bootstrap resampling and network analysis",
        "cli_command": "strepsuis-mdr",
        "package_name": "strepsuis_mdr",
        "original_script": "MDR_2025_04_15.py",
        "notebook_name": "AMRPat_Analysis.ipynb",
        "features": [
            "Bootstrap resampling for robust prevalence estimation",
            "Co-occurrence analysis for phenotypes and resistance genes",
            "Association rule mining for resistance patterns",
            "Hybrid co-resistance network construction",
            "Louvain community detection",
            "Publication-quality network visualizations"
        ],
        "required_files": ["MIC.csv", "AMR_genes.csv"],
        "optional_files": ["Virulence.csv", "MLST.csv", "Serotype.csv"]
    },
    "strepsuis-genphennet": {
        "name": "StrepSuis-GenPhenNet",
        "title": "Network-Based Integration of Genome-Phenome Data",
        "description": "Statistical network analysis for genomic-phenotypic associations",
        "cli_command": "strepsuis-genphennet",
        "package_name": "strepsuis_genphennet",
        "original_script": "Network_Analysis_2025_06_26.py",
        "notebook_name": "GenPhenNet_Analysis.ipynb",
        "features": [
            "Chi-square and Fisher exact tests with FDR correction",
            "Information theory metrics (entropy, mutual information, Cramér's V)",
            "Mutually exclusive pattern detection",
            "3D network visualization with Plotly",
            "Community detection algorithms",
            "Interactive HTML reports"
        ],
        "required_files": ["MIC.csv", "AMR_genes.csv", "Virulence.csv"],
        "optional_files": ["MLST.csv", "Serotype.csv", "Plasmid.csv", "MGE.csv"]
    },
    "strepsuis-phylotrait": {
        "name": "StrepSuis-PhyloTrait",
        "title": "Integrated Phylogenetic and Binary Trait Analysis",
        "description": "Complete phylogenetic and binary trait analysis with tree-aware clustering",
        "cli_command": "strepsuis-phylotrait",
        "package_name": "strepsuis_phylotrait",
        "original_script": "Phylogenetic_clustering_2025_03_21.py",
        "notebook_name": "PhyloTrait_Analysis.ipynb",
        "features": [
            "Tree-aware clustering with evolutionary metrics",
            "Faith's Phylogenetic Diversity calculations",
            "Pairwise phylogenetic distance matrices",
            "Binary trait analysis for AMR and virulence factors",
            "UMAP dimensionality reduction",
            "Interactive HTML reports with DataTables and Plotly"
        ],
        "required_files": ["tree.newick", "MIC.csv", "AMR_genes.csv", "Virulence.csv"],
        "optional_files": ["MLST.csv", "Serotype.csv"]
    },
    "strepsuis-genphen": {
        "name": "StrepSuis-GenPhen",
        "title": "Interactive Platform for Integrated Genomic-Phenotypic Analysis",
        "description": "Integrative genomic-phenotypic analysis platform for Streptococcus suis",
        "cli_command": "strepsuis-genphen",
        "package_name": "strepsuis_genphen",
        "original_script": "StrepSuisPhyloCluster_2025_08_11.py",
        "notebook_name": "GenPhen_Analysis.ipynb",
        "features": [
            "Tree-aware phylogenetic clustering with ensemble fallback",
            "Comprehensive trait profiling (chi-square, log-odds, RF importance)",
            "Association rules mining",
            "Multiple Correspondence Analysis (MCA)",
            "Interactive Bootstrap 5 UI",
            "Full CSV export capabilities"
        ],
        "required_files": ["tree.newick", "MIC.csv", "AMR_genes.csv", "Virulence.csv"],
        "optional_files": ["MLST.csv", "Serotype.csv", "Plasmid.csv", "MGE.csv"]
    }
}


def create_module_structure(module_key: str, module_config: Dict, base_dir: Path):
    """Create directory structure for a module."""
    module_dir = base_dir / module_key
    
    # Create main directories
    dirs = [
        module_dir,
        module_dir / module_config["package_name"],
        module_dir / "examples",
        module_dir / "notebooks",
        module_dir / "tests",
        module_dir / "docker",
        module_dir / ".github" / "workflows"
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created: {dir_path}")


def generate_readme(module_config: Dict) -> str:
    """Generate README.md content for a module."""
    features_list = "\\n".join([f"- ✅ **{f}**" for f in module_config["features"]])
    required_files_list = "\\n".join([f"- `{f}`" for f in module_config["required_files"]])
    optional_files_list = "\\n".join([f"- `{f}` (optional)" for f in module_config.get("optional_files", [])])
    
    return f"""# {module_config['name']}: {module_config['title']}

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/{module_config['cli_command']}/blob/main/notebooks/{module_config['notebook_name']})

**{module_config['description']}**

## Overview

{module_config['name']} is a production-ready Python package for advanced bioinformatics analysis. Originally developed for *Streptococcus suis* genomics but applicable to any bacterial species.

### Key Features

{features_list}

## Quick Start

### Installation

```bash
# Install from PyPI
pip install {module_config['cli_command']}

# Or install from source
git clone https://github.com/MK-vet/{module_config['cli_command']}.git
cd {module_config['cli_command']}
pip install -e .
```

### Usage

#### Command Line Interface

```bash
# Run analysis
{module_config['cli_command']} --data-dir ./data --output ./results

# With custom parameters
{module_config['cli_command']} \\
  --data-dir ./data \\
  --output ./results \\
  --bootstrap 1000 \\
  --fdr-alpha 0.05
```

#### Python API

```python
from {module_config['package_name']} import Analyzer

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
[Open in Google Colab](https://colab.research.google.com/github/MK-vet/{module_config['cli_command']}/blob/main/notebooks/{module_config['notebook_name']})

- Upload your files
- Run all cells
- Download results automatically

### Docker

```bash
# Pull and run
docker pull mkvet/{module_config['cli_command']}:latest
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \\
    mkvet/{module_config['cli_command']}:latest \\
    --data-dir /data --output /output

# Or build locally
docker build -t {module_config['cli_command']} .
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \\
    {module_config['cli_command']} --data-dir /data --output /output
```

## Input Data Format

Required files:
{required_files_list}

{optional_files_list if module_config.get('optional_files') else ''}

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

If you use {module_config['name']} in your research, please cite:

```bibtex
@software{{{module_config['package_name']}2025,
  title = {{{module_config['name']}: {module_config['title']}}},
  author = {{MK-vet}},
  year = {{2025}},
  url = {{https://github.com/MK-vet/{module_config['cli_command']}}},
  version = {{1.0.0}}
}}
```

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

- **GitHub Issues**: [github.com/MK-vet/{module_config['cli_command']}/issues](https://github.com/MK-vet/{module_config['cli_command']}/issues)
- **Documentation**: [Full Documentation](https://mk-vet.github.io/{module_config['cli_command']}/)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Related Tools

Part of the StrepSuis Suite - comprehensive bioinformatics tools for bacterial genomics research.

- [StrepSuis-AMRVirKM](https://github.com/MK-vet/strepsuis-amrvirkm): K-Modes clustering
- [StrepSuis-AMRPat](https://github.com/MK-vet/strepsuis-mdr): MDR pattern detection
- [StrepSuis-GenPhenNet](https://github.com/MK-vet/strepsuis-genphennet): Network analysis
- [StrepSuis-PhyloTrait](https://github.com/MK-vet/strepsuis-phylotrait): Phylogenetic clustering
- [StrepSuis-GenPhen](https://github.com/MK-vet/strepsuis-genphen): Genomic-phenotypic analysis
"""


def main():
    """Main function to generate all module structures."""
    base_dir = Path("/home/runner/work/MKrep/MKrep/separated_repos")
    
    for module_key, module_config in MODULES.items():
        print(f"\\nCreating structure for {module_config['name']}...")
        print("=" * 60)
        
        # Create directory structure
        create_module_structure(module_key, module_config, base_dir)
        
        # Generate README
        readme_content = generate_readme(module_config)
        readme_path = base_dir / module_key / "README.md"
        readme_path.write_text(readme_content)
        print(f"Generated: {readme_path}")
        
    print("\\n" + "=" * 60)
    print("✓ All module structures created successfully!")


if __name__ == "__main__":
    main()
