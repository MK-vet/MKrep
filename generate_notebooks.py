#!/usr/bin/env python3
"""
Generate Google Colab notebooks for all modules
"""

import json
from pathlib import Path

# Notebook template that installs from GitHub
def create_colab_notebook(module_info):
    """Create a Colab notebook for a module."""
    
    notebook = {
        "cells": [
            # Header
            {
                "cell_type": "markdown",
                "metadata": {"id": "header"},
                "source": [
                    f"# {module_info['title']}\n",
                    "\n",
                    f"[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/{module_info['name']}/blob/main/notebooks/{module_info['analysis_type']}_analysis.ipynb)\n",
                    "\n",
                    "## Overview\n",
                    "\n",
                    f"{module_info['description']} - **No coding required!**\n",
                    "\n",
                    "### How to Use\n",
                    "\n",
                    "1. Install the package (runs automatically)\n",
                    "2. Upload your data files\n",
                    "3. Run the analysis\n",
                    "4. Download results\n",
                    "\n",
                    "---\n"
                ]
            },
            # Installation
            {
                "cell_type": "markdown",
                "metadata": {"id": "install-header"},
                "source": [
                    "## Step 1: Install Package from GitHub\n",
                    "\n",
                    "This installs the package directly from GitHub - **no code duplication**.\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {"id": "install"},
                "outputs": [],
                "source": [
                    "%%capture\n",
                    f"!pip install git+https://github.com/MK-vet/{module_info['name']}.git\n",
                    "\n",
                    f"import {module_info['package']}\n",
                    f"print(f\"✓ {module_info['name']} v{{{module_info['package']}.__version__}} installed!\")\n"
                ]
            },
            # Upload
            {
                "cell_type": "markdown",
                "metadata": {"id": "upload-header"},
                "source": [
                    "## Step 2: Upload Data Files\n",
                    "\n",
                    "Upload your CSV files using the file upload button.\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {"id": "upload"},
                "outputs": [],
                "source": [
                    "from google.colab import files\n",
                    "import os\n",
                    "\n",
                    "os.makedirs('data', exist_ok=True)\n",
                    "print(\"Upload your CSV files:\")\n",
                    "uploaded = files.upload()\n",
                    "\n",
                    "for filename in uploaded.keys():\n",
                    "    os.rename(filename, f'data/{filename}')\n",
                    "    print(f\"✓ {filename} uploaded\")\n"
                ]
            },
            # Analysis
            {
                "cell_type": "markdown",
                "metadata": {"id": "analysis-header"},
                "source": ["## Step 3: Run Analysis\n"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {"id": "analysis"},
                "outputs": [],
                "source": [
                    f"from {module_info['package']} import {module_info['analysis_type'].capitalize()}Analyzer\n",
                    "import os\n",
                    "\n",
                    "os.makedirs('output', exist_ok=True)\n",
                    "\n",
                    f"analyzer = {module_info['analysis_type'].capitalize()}Analyzer(\n",
                    "    data_dir='data',\n",
                    "    output_dir='output'\n",
                    ")\n",
                    "\n",
                    "print(\"Running analysis...\")\n",
                    "results = analyzer.run()\n",
                    "\n",
                    "print(\"Generating reports...\")\n",
                    "analyzer.generate_html_report(results)\n",
                    "analyzer.generate_excel_report(results)\n",
                    "print(\"✓ Complete!\")\n"
                ]
            },
            # Download
            {
                "cell_type": "markdown",
                "metadata": {"id": "download-header"},
                "source": ["## Step 4: Download Results\n"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {"id": "download"},
                "outputs": [],
                "source": [
                    "from google.colab import files\n",
                    "import shutil\n",
                    "\n",
                    "shutil.make_archive('results', 'zip', 'output')\n",
                    "files.download('results.zip')\n",
                    "print(\"✓ Download complete!\")\n"
                ]
            },
            # Footer
            {
                "cell_type": "markdown",
                "metadata": {"id": "footer"},
                "source": [
                    "---\n",
                    "\n",
                    "## Support\n",
                    "\n",
                    f"- **Repository**: https://github.com/MK-vet/{module_info['name']}\n",
                    f"- **Issues**: https://github.com/MK-vet/{module_info['name']}/issues\n",
                    "\n",
                    "**License**: MIT | **Version**: 1.0.0\n"
                ]
            }
        ],
        "metadata": {
            "colab": {
                "name": f"{module_info['title']}",
                "provenance": []
            },
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 0
    }
    
    return notebook


# Module definitions
MODULES = [
    {
        "name": "strepsuis-amrpat",
        "package": "strepsuis_amrpat",
        "title": "StrepSuis-AMRPat: MDR Pattern Detection",
        "description": "Automated Detection of Antimicrobial Resistance Patterns",
        "analysis_type": "mdr"
    },
    {
        "name": "strepsuis-genphennet",
        "package": "strepsuis_genphennet",
        "title": "StrepSuis-GenPhenNet: Network Analysis",
        "description": "Network-Based Integration of Genome–Phenome Data",
        "analysis_type": "network"
    },
    {
        "name": "strepsuis-phylotrait",
        "package": "strepsuis_phylotrait",
        "title": "StrepSuis-PhyloTrait: Phylogenetic Analysis",
        "description": "Integrated Phylogenetic and Binary Trait Analysis",
        "analysis_type": "phylo"
    },
    {
        "name": "strepsuis-genphen",
        "package": "strepsuis_genphen",
        "title": "StrepSuis-GenPhen: Integrated Analysis",
        "description": "Interactive Platform for Integrated Genomic–Phenotypic Analysis",
        "analysis_type": "strepsuis"
    }
]


def main():
    """Generate notebooks for all modules."""
    base_dir = Path("modules")
    
    for module in MODULES:
        print(f"Creating notebook for {module['name']}...")
        
        notebook = create_colab_notebook(module)
        
        # Save notebook
        notebook_dir = base_dir / module['name'] / "notebooks"
        notebook_dir.mkdir(parents=True, exist_ok=True)
        
        notebook_path = notebook_dir / f"{module['analysis_type']}_analysis.ipynb"
        
        with open(notebook_path, 'w') as f:
            json.dump(notebook, f, indent=2)
        
        print(f"  ✓ Created {notebook_path}")
        
        # Create notebook README if it doesn't exist
        readme_path = notebook_dir / "README.md"
        if not readme_path.exists():
            with open(readme_path, 'w') as f:
                f.write(f"""# {module['title']} - Colab Notebooks

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/{module['name']}/blob/main/notebooks/{module['analysis_type']}_analysis.ipynb)

## Quick Start

1. Click the "Open in Colab" badge above
2. Follow the notebook instructions
3. No coding required!

## Features

- Automatic package installation from GitHub
- User-friendly interface
- Step-by-step guidance
- Automatic result packaging

See main [README.md](../README.md) for more information.
""")
            print(f"  ✓ Created {readme_path}")
    
    print("\n✓ All notebooks created successfully!")


if __name__ == "__main__":
    main()
