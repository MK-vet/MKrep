#!/usr/bin/env python3
"""
Module Generator Script

This script generates the complete structure for each of the 5 StrepSuis analysis modules.
Each module will be ready to be published as a separate repository.
"""

import os
import shutil
from pathlib import Path

# Module definitions
MODULES = [
    {
        "name": "strepsuis-amrvirkm",
        "package": "strepsuis_amrvirkm",
        "title": "StrepSuis-AMRVirKM: K-Modes Clustering of Antimicrobial Resistance and Virulence Profiles",
        "description": "K-Modes Clustering of Antimicrobial Resistance and Virulence Profiles",
        "script": "Cluster_MIC_AMR_Viruelnce.py",
        "keywords": ["k-modes", "clustering", "AMR", "virulence"],
        "analysis_type": "cluster",
        "command": "strepsuis-amrvirkm",
        "requires_tree": False,
        "already_created": True  # First module was created manually
    },
    {
        "name": "strepsuis-amrpat",
        "package": "strepsuis_amrpat",
        "title": "StrepSuis-AMRPat: Automated Detection of Antimicrobial Resistance Patterns",
        "description": "Automated Detection of Antimicrobial Resistance Patterns",
        "script": "MDR_2025_04_15.py",
        "keywords": ["MDR", "multidrug-resistance", "AMR", "patterns"],
        "analysis_type": "mdr",
        "command": "strepsuis-amrpat",
        "requires_tree": False,
        "already_created": False
    },
    {
        "name": "strepsuis-genphennet",
        "package": "strepsuis_genphennet",
        "title": "StrepSuis-GenPhenNet: Network-Based Integration of Genome–Phenome Data",
        "description": "Network-Based Integration of Genome–Phenome Data",
        "script": "Network_Analysis_2025_06_26.py",
        "keywords": ["network-analysis", "genome-phenome", "associations"],
        "analysis_type": "network",
        "command": "strepsuis-genphennet",
        "requires_tree": False,
        "already_created": False
    },
    {
        "name": "strepsuis-phylotrait",
        "package": "strepsuis_phylotrait",
        "title": "StrepSuis-PhyloTrait: Integrated Phylogenetic and Binary Trait Analysis",
        "description": "Integrated Phylogenetic and Binary Trait Analysis",
        "script": "Phylgenetic_clustering_2025_03_21.py",
        "keywords": ["phylogenetics", "tree-based", "evolution", "traits"],
        "analysis_type": "phylo",
        "command": "strepsuis-phylotrait",
        "requires_tree": True,
        "already_created": False
    },
    {
        "name": "strepsuis-genphen",
        "package": "strepsuis_genphen",
        "title": "StrepSuis-GenPhen: Interactive Platform for Integrated Genomic–Phenotypic Analysis",
        "description": "Interactive Platform for Integrated Genomic–Phenotypic Analysis",
        "script": "StrepSuisPhyloCluster_2025_08_11.py",
        "keywords": ["genomics", "phenomics", "integration", "interactive"],
        "analysis_type": "strepsuis",
        "command": "strepsuis-genphen",
        "requires_tree": True,
        "already_created": False
    }
]


def create_module_structure(module_info, base_dir="modules"):
    """Create the complete directory structure for a module."""
    
    if module_info["already_created"]:
        print(f"✓ {module_info['name']} - Already created, skipping")
        return
    
    module_path = Path(base_dir) / module_info["name"]
    print(f"Creating module: {module_info['name']}")
    
    # Create directories
    dirs = [
        module_path / module_info["package"],
        module_path / "notebooks",
        module_path / "examples" / "data",
        module_path / "docs",
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    return module_path


def copy_template_files(src_module="strepsuis-amrvirkm", dest_module_info=None, base_dir="modules"):
    """Copy template files from the first module and customize them."""
    
    if dest_module_info["already_created"]:
        return
    
    src_path = Path(base_dir) / src_module
    dest_path = Path(base_dir) / dest_module_info["name"]
    
    # Files to copy and customize
    files_to_copy = [
        ".gitignore",
        "LICENSE",
        "requirements.txt",
    ]
    
    for file in files_to_copy:
        src_file = src_path / file
        dest_file = dest_path / file
        if src_file.exists():
            shutil.copy2(src_file, dest_file)
            print(f"  ✓ Copied {file}")


def generate_readme(module_info, base_dir="modules"):
    """Generate customized README for a module."""
    
    if module_info["already_created"]:
        return
    
    module_path = Path(base_dir) / module_info["name"]
    
    readme_content = f"""# {module_info['title']}

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/{module_info['name']}/blob/main/notebooks/{module_info['analysis_type']}_analysis.ipynb)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://hub.docker.com)

## Overview

{module_info['description']} for *Streptococcus suis* and other bacterial genomics data.

This tool is part of the StrepSuis Suite of bioinformatics analysis tools, designed for comprehensive genomic and phenotypic analysis.

### Key Features

- Professional, publication-ready reports (HTML and Excel)
- High-quality visualizations (150+ DPI PNG exports)
- Statistical rigor with bootstrap confidence intervals
- Comprehensive documentation and examples
- Multiple deployment options (Colab, Docker, CLI, Local)

## Quick Start

### Option 1: Google Colab (Recommended) ⭐

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/{module_info['name']}/blob/main/notebooks/{module_info['analysis_type']}_analysis.ipynb)

**No installation required!** Just click the badge and follow the notebook instructions.

### Option 2: Python Package

```bash
# Install from GitHub
pip install git+https://github.com/MK-vet/{module_info['name']}.git

# Run analysis
{module_info['command']} --data-dir ./data --output ./results
```

### Option 3: Docker

```bash
# Build and run
docker build -t {module_info['name']}:latest .
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \\
    {module_info['name']}:latest --data-dir /data --output /output
```

### Option 4: Local Installation

```bash
git clone https://github.com/MK-vet/{module_info['name']}.git
cd {module_info['name']}
pip install -r requirements.txt
python -m {module_info['package']}.cli --data-dir ./examples/data --output ./results
```

## Input Data Format

See [docs/USAGE.md](docs/USAGE.md) for detailed data format requirements.

Required files:
- Binary CSV files with `Strain_ID` column
- Values: 0 (absence) or 1 (presence)
{'- Newick tree file (tree.newick or tree.nwk)' if module_info['requires_tree'] else ''}

## Output Files

- Interactive HTML report
- Excel workbook with multiple sheets
- High-quality PNG charts (150+ DPI)

## Documentation

- [README.md](README.md) - This file
- [docs/USAGE.md](docs/USAGE.md) - Detailed usage guide
- [docs/API.md](docs/API.md) - Python API documentation
- [docs/EXAMPLES.md](docs/EXAMPLES.md) - Example analyses
- [notebooks/README.md](notebooks/README.md) - Colab notebook guide

## Citation

```bibtex
@software{{{module_info['package']}2025,
  title = {{{module_info['title']}}},
  author = {{MK-vet}},
  year = {{2025}},
  url = {{https://github.com/MK-vet/{module_info['name']}}},
  version = {{1.0.0}}
}}
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Related Projects

- **StrepSuis-AMRVirKM**: K-Modes clustering
- **StrepSuis-AMRPat**: MDR pattern detection
- **StrepSuis-GenPhenNet**: Network analysis
- **StrepSuis-PhyloTrait**: Phylogenetic clustering
- **StrepSuis-GenPhen**: Integrated analysis

---

**Version**: 1.0.0  
**Last Updated**: 2025-01-14  
**Maintainer**: MK-vet
"""
    
    with open(module_path / "README.md", "w") as f:
        f.write(readme_content)
    
    print(f"  ✓ Generated README.md")


def generate_pyproject_toml(module_info, base_dir="modules"):
    """Generate pyproject.toml for a module."""
    
    if module_info["already_created"]:
        return
    
    module_path = Path(base_dir) / module_info["name"]
    
    keywords_str = '", "'.join(['bioinformatics', 'microbiology', 'genomics'] + module_info['keywords'])
    
    content = f"""[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{module_info['name']}"
version = "1.0.0"
description = "{module_info['description']}"
readme = "README.md"
requires-python = ">=3.8"
license = {{text = "MIT"}}
authors = [
    {{name = "MK-vet", email = "contact@example.com"}}
]
keywords = ["{keywords_str}"]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
]

dependencies = [
    "pandas>=1.3.0",
    "numpy>=1.21.0",
    "scipy>=1.7.0",
    "matplotlib>=3.4.0",
    "seaborn>=0.11.0",
    "plotly>=5.0.0",
    "scikit-learn>=1.0.0",
    "jinja2>=3.0.0",
    "openpyxl>=3.0.0",
    "xlsxwriter>=3.0.0",
    "kaleido>=0.2.0",
    "pillow>=8.0.0",
    "tqdm>=4.62.0",
    "statsmodels>=0.13.0",
    {'    "biopython>=1.79",' if module_info['requires_tree'] else ''}
    {'    "networkx>=2.6.0",' if module_info['analysis_type'] in ['network', 'mdr'] else ''}
    {'    "kmodes>=0.12.0",' if module_info['analysis_type'] == 'cluster' else ''}
    {'    "prince>=0.7.0",' if module_info['analysis_type'] in ['cluster', 'phylo', 'strepsuis'] else ''}
    {'    "mlxtend>=0.19.0",' if module_info['analysis_type'] in ['cluster', 'mdr'] else ''}
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=3.0.0",
    "black>=22.0.0",
    "flake8>=4.0.0",
]

[project.urls]
Homepage = "https://github.com/MK-vet/{module_info['name']}"
Documentation = "https://github.com/MK-vet/{module_info['name']}#readme"
Repository = "https://github.com/MK-vet/{module_info['name']}"
Issues = "https://github.com/MK-vet/{module_info['name']}/issues"

[project.scripts]
{module_info['command']} = "{module_info['package']}.cli:main"

[tool.setuptools]
packages = ["{module_info['package']}"]

[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311', 'py312']
"""
    
    with open(module_path / "pyproject.toml", "w") as f:
        f.write(content)
    
    print(f"  ✓ Generated pyproject.toml")


def generate_dockerfile(module_info, base_dir="modules"):
    """Generate Dockerfile for a module."""
    
    if module_info["already_created"]:
        return
    
    module_path = Path(base_dir) / module_info["name"]
    
    content = f"""# {module_info['title']}
# Dynamic installation from GitHub - no code duplication

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# Install package from GitHub (dynamic installation)
ARG GITHUB_REPO=https://github.com/MK-vet/{module_info['name']}.git
ARG BRANCH=main

RUN pip install --no-cache-dir "git+${{GITHUB_REPO}}@${{BRANCH}}"

# Create data and output directories
RUN mkdir -p /data /output

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/data
ENV OUTPUT_DIR=/output

# Default command
CMD ["{module_info['command']}", "--help"]

# Usage:
# docker build -t {module_info['name']}:latest .
# docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \\
#     {module_info['name']}:latest --data-dir /data --output /output
"""
    
    with open(module_path / "Dockerfile", "w") as f:
        f.write(content)
    
    print(f"  ✓ Generated Dockerfile")


def generate_docker_compose(module_info, base_dir="modules"):
    """Generate docker-compose.yml for a module."""
    
    if module_info["already_created"]:
        return
    
    module_path = Path(base_dir) / module_info["name"]
    
    content = f"""version: '3.8'

services:
  {module_info['name']}:
    build: .
    image: {module_info['name']}:latest
    container_name: {module_info['name']}
    volumes:
      - ./examples/data:/data:ro
      - ./output:/output
    environment:
      - PYTHONUNBUFFERED=1
    command: >
      {module_info['command']}
      --data-dir /data
      --output /output

# Usage:
# docker-compose up
"""
    
    with open(module_path / "docker-compose.yml", "w") as f:
        f.write(content)
    
    print(f"  ✓ Generated docker-compose.yml")


def generate_package_init(module_info, base_dir="modules"):
    """Generate __init__.py for the package."""
    
    if module_info["already_created"]:
        return
    
    module_path = Path(base_dir) / module_info["name"] / module_info["package"]
    
    content = f'''"""
{module_info['title']}

{module_info['description']}
"""

__version__ = "1.0.0"
__author__ = "MK-vet"
__license__ = "MIT"

from .analysis import {module_info['analysis_type'].capitalize()}Analyzer

__all__ = ["{module_info['analysis_type'].capitalize()}Analyzer", "__version__"]
'''
    
    with open(module_path / "__init__.py", "w") as f:
        f.write(content)
    
    print(f"  ✓ Generated {module_info['package']}/__init__.py")


def generate_cli(module_info, base_dir="modules"):
    """Generate CLI module."""
    
    if module_info["already_created"]:
        return
    
    module_path = Path(base_dir) / module_info["name"] / module_info["package"]
    
    content = f'''#!/usr/bin/env python3
"""
{module_info['title']} - Command Line Interface
"""

import argparse
import sys
from pathlib import Path
from .analysis import {module_info['analysis_type'].capitalize()}Analyzer


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="{module_info['description']}",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--data-dir", required=True, help="Input data directory")
    parser.add_argument("--output", default="./results", help="Output directory")
    {'parser.add_argument("--tree", required=True, help="Newick tree file")' if module_info['requires_tree'] else ''}
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    
    args = parser.parse_args()
    
    try:
        data_dir = Path(args.data_dir)
        if not data_dir.exists():
            print(f"Error: Data directory not found: {{data_dir}}", file=sys.stderr)
            sys.exit(1)
        
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"{module_info['title']}")
        print("=" * 60)
        print(f"Data: {{data_dir}}")
        print(f"Output: {{output_dir}}")
        print("=" * 60)
        
        analyzer = {module_info['analysis_type'].capitalize()}Analyzer(
            data_dir=str(data_dir),
            output_dir=str(output_dir),
            {'tree_file=args.tree,' if module_info['requires_tree'] else ''}
            random_seed=args.seed
        )
        
        print("Running analysis...")
        results = analyzer.run()
        
        print("Generating reports...")
        analyzer.generate_html_report(results)
        analyzer.generate_excel_report(results)
        
        print("\\n✓ Analysis complete!")
        return 0
        
    except Exception as e:
        print(f"Error: {{e}}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
'''
    
    with open(module_path / "cli.py", "w") as f:
        f.write(content)
    
    print(f"  ✓ Generated {module_info['package']}/cli.py")


def generate_analysis_stub(module_info, base_dir="modules"):
    """Generate analysis module stub."""
    
    if module_info["already_created"]:
        return
    
    module_path = Path(base_dir) / module_info["name"] / module_info["package"]
    
    content = f'''"""
{module_info['title']} - Analysis Module

This module contains the core analysis functionality.

NOTE: The full implementation should be extracted from the original script:
{module_info['script']}
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any
import warnings
warnings.filterwarnings('ignore')


class {module_info['analysis_type'].capitalize()}Analyzer:
    """
    {module_info['description']}
    
    This is a template class. The full implementation should be extracted
    from the original script and organized here.
    """
    
    def __init__(
        self,
        data_dir: str,
        output_dir: str = "./results",
        {'tree_file: str = None,' if module_info['requires_tree'] else ''}
        random_seed: int = 42
    ):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        {'self.tree_file = tree_file' if module_info['requires_tree'] else ''}
        self.random_seed = random_seed
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        np.random.seed(random_seed)
    
    def load_data(self) -> Dict[str, pd.DataFrame]:
        """Load input data files."""
        # TODO: Implement based on {module_info['script']}
        return {{}}
    
    def run(self) -> Dict[str, Any]:
        """Run the complete analysis."""
        print("Loading data...")
        data = self.load_data()
        
        # TODO: Implement full analysis pipeline
        # See {module_info['script']} for implementation
        
        return {{"status": "template"}}
    
    def generate_html_report(self, results: Dict[str, Any]) -> str:
        """Generate HTML report."""
        # TODO: Implement report generation
        output_file = self.output_dir / "{module_info['analysis_type']}_report.html"
        return str(output_file)
    
    def generate_excel_report(self, results: Dict[str, Any]) -> str:
        """Generate Excel report."""
        # TODO: Implement Excel generation
        output_file = self.output_dir / "{module_info['analysis_type']}_report.xlsx"
        return str(output_file)
'''
    
    with open(module_path / "analysis.py", "w") as f:
        f.write(content)
    
    print(f"  ✓ Generated {module_info['package']}/analysis.py")


def copy_example_data(module_info, base_dir="modules"):
    """Copy example data files."""
    
    if module_info["already_created"]:
        return
    
    src_data = Path(".") 
    dest_data = Path(base_dir) / module_info["name"] / "examples" / "data"
    
    # Copy CSV files
    data_files = ["MIC.csv", "AMR_genes.csv", "Virulence.csv", "MLST.csv", "Serotype.csv", "Plasmid.csv", "MGE.csv"]
    
    for file in data_files:
        src_file = src_data / file
        if src_file.exists():
            shutil.copy2(src_file, dest_data / file)
    
    # Copy tree file if needed
    if module_info['requires_tree']:
        tree_file = src_data / "Snp_tree.newick"
        if tree_file.exists():
            shutil.copy2(tree_file, dest_data / "tree.newick")
    
    print(f"  ✓ Copied example data files")


def main():
    """Main function to generate all modules."""
    print("=" * 60)
    print("StrepSuis Modules Generator")
    print("=" * 60)
    print()
    
    for module in MODULES:
        print(f"\nProcessing: {module['name']}")
        print("-" * 60)
        
        # Create directory structure
        create_module_structure(module)
        
        if not module['already_created']:
            # Copy template files
            copy_template_files(dest_module_info=module)
            
            # Generate files
            generate_readme(module)
            generate_pyproject_toml(module)
            generate_dockerfile(module)
            generate_docker_compose(module)
            generate_package_init(module)
            generate_cli(module)
            generate_analysis_stub(module)
            copy_example_data(module)
            
            print(f"✓ Module {module['name']} created successfully!")
    
    print("\n" + "=" * 60)
    print("✓ All modules generated successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review generated files in modules/ directory")
    print("2. Implement full analysis logic in each analysis.py")
    print("3. Test Docker builds: docker build -t <module>:latest modules/<module>/")
    print("4. Test package installation: pip install -e modules/<module>/")
    print("5. Create Colab notebooks for each module")


if __name__ == "__main__":
    main()
