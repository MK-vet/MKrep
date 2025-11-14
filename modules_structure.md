# Modules Structure

This directory contains 5 independent modules, each ready to be published as a separate repository.

## Module 1: strepsuis-amrvirkm (K-Modes Clustering)
- **Repository Name**: strepsuis-amrvirkm
- **Main Script**: Cluster_MIC_AMR_Viruelnce.py
- **Description**: K-Modes Clustering of Antimicrobial Resistance and Virulence Profiles

## Module 2: strepsuis-amrpat (MDR Analysis)
- **Repository Name**: strepsuis-amrpat
- **Main Script**: MDR_2025_04_15.py
- **Description**: Automated Detection of Antimicrobial Resistance Patterns

## Module 3: strepsuis-genphennet (Network Analysis)
- **Repository Name**: strepsuis-genphennet
- **Main Script**: Network_Analysis_2025_06_26.py
- **Description**: Network-Based Integration of Genome–Phenome Data

## Module 4: strepsuis-phylotrait (Phylogenetic Clustering)
- **Repository Name**: strepsuis-phylotrait
- **Main Script**: Phylgenetic_clustering_2025_03_21.py
- **Description**: Integrated Phylogenetic and Binary Trait Analysis

## Module 5: strepsuis-genphen (Integrated Analysis)
- **Repository Name**: strepsuis-genphen
- **Main Script**: StrepSuisPhyloCluster_2025_08_11.py
- **Description**: Interactive Platform for Integrated Genomic–Phenotypic Analysis

## Directory Structure for Each Module

```
module-name/
├── README.md                          # Professional English documentation
├── LICENSE                            # MIT License
├── pyproject.toml                     # Python package configuration
├── setup.py                           # Alternative setup file
├── Dockerfile                         # Dynamic package installation
├── docker-compose.yml                 # Docker orchestration
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore file
├── module_name/                       # Python package
│   ├── __init__.py
│   ├── analysis.py                    # Main analysis code
│   ├── cli.py                         # Command-line interface
│   └── utils.py                       # Utility functions
├── notebooks/                         # Google Colab notebooks
│   ├── module_analysis.ipynb          # Main Colab notebook
│   └── README.md                      # Notebook documentation
├── examples/                          # Example data and usage
│   ├── data/                          # Example datasets
│   │   ├── MIC.csv
│   │   ├── AMR_genes.csv
│   │   └── Virulence.csv
│   └── README.md                      # Usage examples
└── docs/                              # Additional documentation
    ├── USAGE.md                       # Detailed usage guide
    ├── API.md                         # API documentation
    └── EXAMPLES.md                    # Example outputs
```
