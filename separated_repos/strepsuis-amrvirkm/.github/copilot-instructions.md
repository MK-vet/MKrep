# Copilot Instructions for StrepSuis-AMRVirKM

K-Modes clustering of antimicrobial resistance and virulence profiles for bacterial genomics.

## Project Overview

- **Language**: Python 3.8+
- **Domain**: Bioinformatics, genomics, clustering analysis
- **Package name**: `strepsuis-amrvirkm`
- **CLI command**: `strepsuis-amrvirkm`

## Code Style and Conventions

- Follow PEP 8 style guidelines
- Use type hints for function signatures
- Include docstrings for all public functions and classes
- Use descriptive variable names reflecting biological terminology
- Line length: 100 characters (black formatter)

## Repository Structure

- **`strepsuis_amrvirkm/`**: Main package source code
  - `cli.py`: Command-line interface
  - `config.py`: Configuration and validation
  - `analyzer.py`: Core analysis logic
- **`tests/`**: Test suite (pytest)
- **`data/`**: Example datasets
- **`notebooks/`**: Jupyter notebooks for Google Colab
- **`examples/`**: Usage examples

## Building and Testing

### Install Package
```bash
pip install -e .
pip install -e .[dev]  # With development dependencies
```

### Run Tests
```bash
pytest
pytest --cov --cov-report=html
pytest -m "not slow"  # Fast tests only
```

### Code Quality
```bash
pre-commit run --all-files
black .
isort .
ruff check .
```

## Key Features

- K-Modes clustering with automatic silhouette optimization
- Multiple Correspondence Analysis (MCA)
- Feature importance ranking (Random Forest, chi-square)
- Association rule discovery (Apriori algorithm)
- Bootstrap confidence intervals

## Data Format Conventions

- **Input files**: CSV format with `Strain_ID` column
- **Binary data**: `0 = Absence`, `1 = Presence`
- **Required files**: `AMR_genes.csv`, `MIC.csv`
- **Optional files**: `Virulence.csv`, `MLST.csv`, `Serotype.csv`

## Output Files

- HTML report with Bootstrap 5 styling
- Excel workbook with multiple sheets
- PNG charts (150+ DPI) in `png_charts/` subfolder

## Important Guidelines

- Maintain statistical method documentation
- Use fixed random seeds for reproducibility
- Ensure publication-quality visualizations
- Test across Python 3.8-3.12
- Update CHANGELOG.md for significant changes
