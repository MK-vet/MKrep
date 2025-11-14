#!/bin/bash

# Function to create a Colab notebook for a module
create_notebook() {
    local module=$1
    local package=$2
    local title=$3
    local notebook=$4
    
    cat > "${module}/notebooks/${notebook}" << NOTEBOOK
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {"id": "header"},
   "source": [
    "# ${title}\\n",
    "\\n",
    "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MK-vet/${module}/blob/main/notebooks/${notebook})\\n",
    "\\n",
    "---\\n",
    "\\n",
    "## Installation\\n",
    "Install directly from GitHub (no code duplication):"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {"id": "install"},
   "outputs": [],
   "source": [
    "%%capture\\n",
    "!pip install git+https://github.com/MK-vet/${module}.git"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {"id": "import"},
   "source": ["## Import Libraries"]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {"id": "imports"},
   "outputs": [],
   "source": [
    "from ${package} import Config, __version__\\n",
    "from google.colab import files\\n",
    "import os\\n",
    "\\n",
    "print(f\\\"${title} v{__version__} loaded successfully!\\\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {"id": "upload"},
   "source": ["## Upload Data Files"]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {"id": "upload_files"},
   "outputs": [],
   "source": [
    "!mkdir -p data\\n",
    "print(\\\"Please upload your CSV files:\\\")\\n",
    "uploaded = files.upload()\\n",
    "for filename in uploaded.keys():\\n",
    "    !mv \\\"{filename}\\\" data/\\n",
    "    print(f\\\"✓ {filename} uploaded\\\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {"id": "run"},
   "source": ["## Run Analysis"]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {"id": "run_analysis"},
   "outputs": [],
   "source": [
    "from ${package} import *\\n",
    "config = Config(data_dir=\\\"data\\\", output_dir=\\\"output\\\")\\n",
    "analyzer = Analyzer(config)\\n",
    "results = analyzer.run()\\n",
    "print(\\\"✓ Analysis completed!\\\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {"id": "download"},
   "source": ["## Download Results"]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {"id": "download_results"},
   "outputs": [],
   "source": [
    "import shutil\\n",
    "from datetime import datetime\\n",
    "timestamp = datetime.now().strftime(\\\"%Y%m%d_%H%M%S\\\")\\n",
    "zip_filename = f\\\"Results_{timestamp}.zip\\\"\\n",
    "shutil.make_archive(zip_filename.replace('.zip', ''), 'zip', 'output')\\n",
    "files.download(zip_filename)"
   ]
  }
 ],
 "metadata": {
  "colab": {"name": "${notebook}", "provenance": []},
  "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
 },
 "nbformat": 4,
 "nbformat_minor": 0
}
NOTEBOOK
}

# Create notebooks for each module
create_notebook "strepsuis-amrpat" "strepsuis_amrpat" "StrepSuis-AMRPat: MDR Analysis" "AMRPat_Analysis.ipynb"
create_notebook "strepsuis-genphennet" "strepsuis_genphennet" "StrepSuis-GenPhenNet: Network Analysis" "GenPhenNet_Analysis.ipynb"
create_notebook "strepsuis-phylotrait" "strepsuis_phylotrait" "StrepSuis-PhyloTrait: Phylogenetic Analysis" "PhyloTrait_Analysis.ipynb"
create_notebook "strepsuis-genphen" "strepsuis_genphen" "StrepSuis-GenPhen: Genomic-Phenotypic Analysis" "GenPhen_Analysis.ipynb"

echo "All Colab notebooks created!"
