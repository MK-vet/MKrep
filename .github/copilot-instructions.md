# Copilot Instructions for StrepSuis_Suite

This repository contains a comprehensive bioinformatics analysis suite for *Streptococcus suis* genomics, focusing on antimicrobial resistance (AMR), virulence factors, and phylogenetic relationships.

## Project Overview

- **Language**: Python 3.8+
- **Domain**: Bioinformatics, genomics, statistical analysis
- **Key dependencies**: pandas, numpy, scipy, scikit-learn, matplotlib, plotly, biopython, networkx

## Code Style and Conventions

- Follow PEP 8 style guidelines for Python code
- Use descriptive variable names that reflect biological/scientific terminology
- Include docstrings for all functions and classes
- Use type hints where appropriate
- Maintain consistent indentation (4 spaces)

## Repository Structure

- **Main analysis scripts**: `Cluster_MIC_AMR_Viruelnce.py`, `MDR_2025_04_15.py`, `Network_Analysis_2025_06_26.py`, `Phylogenetic_clustering_2025_03_21.py`, `StrepSuisPhyloCluster_2025_08_11.py`
- **Utilities**: `excel_report_utils.py`, `report_templates.py`, `merge_data.py`
- **CLI package**: `python_package/`
- **Jupyter notebooks**: `colab_notebooks/`
- **Documentation**: Various `.md` files in root directory
- **Tests**: `test_*.py`, `validate*.py`, `verify*.py`

## Building and Testing

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Check Script Syntax
```bash
python -m py_compile <script_name>.py
```

### Run Validation
```bash
python validate.py
python verify_all_modules.py
```

### Test CLI Package
```bash
cd python_package
pip install -e .
mkrep --help
```

## Data Format Conventions

- **Input files**: CSV format with `Strain_ID` column
- **Binary data**: `0 = Absence`, `1 = Presence` (both are biologically significant)
- **Tree files**: Newick format (`.newick` or `.nwk`)

## Report Generation

All analysis scripts generate:
- Interactive HTML reports with Bootstrap 5 styling
- Excel workbooks with multiple sheets
- PNG charts (150+ DPI) in `png_charts/` subfolder

## Important Guidelines

- When modifying analysis scripts, maintain consistency with existing report templates
- Keep statistical methods well-documented with references
- Ensure all visualizations are publication-quality (high DPI, proper labels)
- Preserve reproducibility by using fixed random seeds
- Update documentation when adding new features
- Test changes across Python 3.8-3.12

## File Naming

- Analysis scripts: `<Name>_<date_YYYY_MM_DD>.py`
- Reports: `<analysis>_Report_<timestamp>.xlsx` and `<analysis>_report.html`
- Documentation: Use descriptive names with `_` separators in CAPS for guides (e.g., `USER_GUIDE.md`)
