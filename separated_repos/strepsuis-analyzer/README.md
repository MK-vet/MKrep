# StrepSuis Analyzer - Streamlit Application

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive web-based platform for analyzing genomic and phenotypic data of *Streptococcus suis* strains.

## 🎯 Overview

StrepSuis Analyzer is an interactive Streamlit application designed for researchers working with *Streptococcus suis* genomic and phenotypic data. The application provides:

- **AMR Analysis**: Antimicrobial resistance gene profiling and prevalence
- **Virulence Analysis**: Virulence factor distribution and co-occurrence
- **MIC Analysis**: Minimum Inhibitory Concentration profiles and MDR detection
- **MLST & Serotype**: Multilocus sequence typing and serotype distribution
- **Comparative Analysis**: Strain similarity using Jaccard and Hamming distances
- **Statistical Summary**: Diversity indices (Shannon, Simpson) and comprehensive statistics

## 📊 Features

### Data Analysis
- **Multi-dataset Integration**: AMR genes, virulence factors, MIC values, MLST, serotypes, MGE, and plasmids
- **Diversity Metrics**: Shannon and Simpson diversity indices
- **Distance Calculations**: Jaccard and Hamming distances for strain comparison
- **Prevalence Analysis**: Gene/factor distribution across strains
- **Correlation Analysis**: Co-occurrence patterns

### Visualizations
- Interactive bar charts for prevalence
- Heatmaps for correlation and distance matrices
- Pie charts for categorical distributions
- Histograms for resistance profiles
- Color-coded visualizations with Plotly

### Statistical Functions
All statistical functions are mathematically validated:
- `calculate_shannon_diversity()`: H = -Σ(p_i * log(p_i))
- `calculate_simpson_diversity()`: D = 1 - Σ(p_i^2)
- `calculate_jaccard_distance()`: 1 - (intersection/union)
- `calculate_hamming_distance()`: Normalized position differences
- `calculate_pairwise_distances()`: Complete distance matrix computation

## 🚀 Quick Start

### Installation

1. Clone or navigate to this directory:
```bash
cd separated_repos/strepsuis-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

Launch the Streamlit app:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

### Docker Deployment (Optional)

Build and run using Docker:
```bash
docker build -t strepsuis-analyzer .
docker run -p 8501:8501 strepsuis-analyzer
```

## 📁 Data Files

The application expects the following data files in the `data/` directory:

- `AMR_genes.csv`: Antimicrobial resistance gene presence/absence
- `Virulence.csv`: Virulence factor presence/absence
- `MIC.csv`: Minimum Inhibitory Concentration binary data
- `MLST.csv`: Multilocus sequence typing data
- `Serotype.csv`: Serotype assignments
- `MGE.csv`: Mobile genetic element data
- `Plasmid.csv`: Plasmid presence data
- `Snp_tree.newick`: Phylogenetic tree (Newick format)

### Data Format

All CSV files should have a `Strain_ID` column followed by feature columns:

```csv
Strain_ID,feature1,feature2,feature3,...
strain001,0,1,0,...
strain002,1,1,1,...
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests with coverage
pytest tests/ -v --cov=. --cov-report=html --cov-report=term

# Run only mathematical validation tests
pytest tests/test_statistical_functions.py -v

# Run with specific markers
pytest tests/ -v -m unit
pytest tests/ -v -m integration
```

### Coverage Requirements

- **Total Code Coverage**: >80%
- **Mathematical/Statistical Functions**: >95%
- **Synthetic Data Validation**: 100% for edge cases

## 📖 Usage Guide

### Navigation

Use the sidebar to select different analysis types:

1. **Overview**: Dataset summary and metrics
2. **AMR Analysis**: Resistance gene prevalence and diversity
3. **Virulence Analysis**: Virulence factor distribution
4. **MIC Analysis**: Antibiotic resistance profiles and MDR detection
5. **MLST & Serotype**: Typing and serotype distributions
6. **Comparative Analysis**: Strain similarity calculations
7. **Statistical Summary**: Comprehensive statistical overview

### Analysis Workflow

1. **Load Data**: Application automatically loads all data files on startup
2. **Select Analysis**: Choose analysis type from sidebar
3. **Customize View**: Use sliders and checkboxes to adjust visualizations
4. **Export Results**: Download charts using Plotly's built-in export

### Example Analyses

**Finding MDR Strains:**
1. Navigate to "MIC Analysis"
2. View "MDR Strains" metric (≥3 resistances)
3. Examine resistance distribution histogram

**Comparing Strains:**
1. Navigate to "Comparative Analysis"
2. Select dataset (AMR or Virulence)
3. Choose distance metric (Jaccard or Hamming)
4. View distance heatmap

**Diversity Assessment:**
1. Navigate to "Statistical Summary"
2. Review Shannon and Simpson indices
3. Compare across datasets

## 🔬 Mathematical Validation

All statistical functions are rigorously validated:

### Shannon Diversity Index
```
H = -Σ(p_i * log(p_i))
```
Where p_i is the proportion of presence for feature i.

### Simpson Diversity Index
```
D = 1 - Σ(p_i^2)
```
Higher values indicate greater diversity.

### Jaccard Distance
```
J = 1 - (|A ∩ B| / |A ∪ B|)
```
Measures dissimilarity between binary vectors.

### Hamming Distance
```
H = (# differing positions) / (total positions)
```
Normalized to [0, 1] range.

## 📋 Requirements

- Python 3.8 or higher
- Streamlit 1.28+
- Pandas 1.3+
- NumPy 1.21+
- Plotly 5.0+
- SciPy 1.7+

## 🛠️ Development

### Project Structure

```
strepsuis-analyzer/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── pytest.ini             # Pytest configuration
├── pyproject.toml         # Package metadata
├── data/                  # Data directory
│   ├── AMR_genes.csv
│   ├── Virulence.csv
│   ├── MIC.csv
│   ├── MLST.csv
│   ├── Serotype.csv
│   ├── MGE.csv
│   ├── Plasmid.csv
│   └── Snp_tree.newick
└── tests/                 # Test suite
    ├── __init__.py
    ├── conftest.py
    ├── test_statistical_functions.py
    ├── test_data_loading.py
    ├── test_visualization.py
    └── test_integration.py
```

### Adding New Features

1. Add new analysis functions to `app.py`
2. Create corresponding tests in `tests/`
3. Ensure >95% coverage for mathematical functions
4. Update documentation in README.md
5. Run full test suite before committing

### Code Quality

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Include docstrings with mathematical formulas
- Validate inputs and handle edge cases
- Use random_state for reproducibility

## 🤝 Contributing

Contributions are welcome! Please ensure:

1. All tests pass with >80% coverage
2. Mathematical functions have >95% coverage
3. Code follows repository conventions
4. Documentation is updated
5. Synthetic data tests validate edge cases

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- StrepSuis bioinformatics suite
- Streamlit framework
- Plotly visualization library

## 📧 Contact

For questions or support, please open an issue on the GitHub repository.

---

**Note**: This application is part of the StrepSuis analysis suite. For the complete workflow including phylogenetic analysis, MDR detection, and network analysis, see the other modules in `separated_repos/`.
