# Strepsuis Analyzer - Module Documentation

## Overview
The `strepsuis-analyzer` module is an interactive Streamlit-based platform for comprehensive analysis of Streptococcus suis genomic and phenotypic data.

## Structure

```
strepsuis-analyzer/
├── app.py                      # Main Streamlit application
├── utils.py                    # Utility functions (testable components)
├── requirements.txt            # Python dependencies
├── README.md                   # Project description
├── .gitignore                  # Git ignore patterns
├── .coveragerc                 # Coverage configuration
├── data/                       # Reference datasets
│   ├── AMR_genes.csv          # Antimicrobial resistance genes (10 strains)
│   ├── MGE.csv                # Mobile genetic elements
│   ├── MIC.csv                # Minimum inhibitory concentrations
│   ├── MLST.csv               # Multi-locus sequence typing
│   ├── Plasmid.csv            # Plasmid presence/absence
│   ├── Serotype.csv           # Serotype information
│   ├── Virulence.csv          # Virulence factors
│   └── Snp_tree.newick        # Phylogenetic tree
└── tests/                      # Test suite
    ├── __init__.py
    ├── conftest.py
    ├── test_app.py            # Application component tests (19 tests)
    ├── test_statistics.py     # Statistical validation tests (29 tests)
    └── test_utils.py          # Utility function tests (38 tests)
```

## Features

### 1. ETL (Extract, Transform, Load)
- Data loading and validation
- DataFrame structure validation
- Data type conversion for Streamlit compatibility

### 2. EDA (Exploratory Data Analysis)
- Data overview and statistics
- Missing value analysis
- Data type inspection

### 3. Visualizations
- Distribution plots
- Correlation heatmaps
- Interactive visualizations (when Plotly is available)

### 4. Classification & Clustering
- K-Means clustering
- PCA dimensionality reduction
- Cluster visualization

### 5. Statistical Tests
- Pearson correlation analysis
- Independent samples t-tests
- ANOVA (one-way)
- Regression analysis

### 6. Phylogenetic Analysis
- Newick tree visualization (using Biopython/ETE3)
- Tree statistics
- Support for custom tree uploads

### 7. Report & Export
- CSV export
- Excel export
- Session summaries

### 8. Python Editor
- Interactive code execution (using streamlit-ace)
- Access to loaded data
- Real-time output

## Test Coverage

### Overall Coverage: 95% on utils module

#### Test Suites:
1. **test_app.py** (19 tests)
   - DataValidator tests
   - DataFrame fixing tests
   - Reference data loading tests
   - Data integrity tests
   - Application requirements tests

2. **test_statistics.py** (29 tests)
   - Correlation calculations (100% accuracy)
   - T-test calculations (100% accuracy)
   - ANOVA calculations (100% accuracy)
   - Descriptive statistics (100% accuracy)
   - Classification metrics (100% accuracy)
   - Numerical stability tests
   - Synthetic data validation

3. **test_utils.py** (38 tests)
   - All utility functions comprehensively tested
   - Edge cases covered
   - NaN handling verified
   - Mathematical accuracy validated

### Mathematical Validation
All statistical functions have been validated against known ground truth:
- Perfect correlations (r = ±1.0)
- Known t-test values
- Known ANOVA values
- Descriptive statistics accuracy
- Classification metrics accuracy

### Coverage by Component:
- **utils.py**: 95% coverage
- **Mathematical functions**: >95% coverage
- **Statistical tests**: 99% coverage

## CI/CD

### GitHub Actions Workflow
Location: `.github/workflows/strepsuis-analyzer-tests.yml`

Features:
- Multi-Python version testing (3.9, 3.10, 3.11)
- Automated test execution
- Coverage reporting (>80% threshold enforced)
- Code quality checks (black, isort, ruff)
- Smoke tests for data integrity
- Codecov integration

## Dependencies

### Core Libraries:
- streamlit==1.34.0 - Web application framework
- pandas==2.2.1 - Data manipulation
- numpy==1.26.4 - Numerical computing
- scipy (via statsmodels) - Statistical functions
- scikit-learn==1.4.1.post1 - Machine learning

### Visualization:
- matplotlib==3.8.3
- seaborn==0.13.2
- plotly==5.21.0

### Clustering:
- kmodes==0.12.2

### Statistical Analysis:
- statsmodels==0.14.1

### Phylogenetics:
- bio==1.6.0
- ete3==3.1.3
- dendropy==4.5.2

### UI Enhancement:
- streamlit-aggrid==1.1.0
- streamlit-ace==0.1.1

### File Formats:
- openpyxl==3.1.5

### Testing:
- pytest
- pytest-cov

## Usage

### Running the Application:
```bash
cd separated_repos/strepsuis-analyzer
pip install -r requirements.txt
streamlit run app.py
```

### Running Tests:
```bash
cd separated_repos/strepsuis-analyzer
pytest tests/ -v
```

### Running Tests with Coverage:
```bash
cd separated_repos/strepsuis-analyzer
pytest tests/ --cov=utils --cov-report=term --cov-report=html
```

## Data Files

All data files contain 10 Streptococcus suis strains (S001-S010) with the following characteristics:

1. **AMR_genes.csv**: Binary presence/absence of 10 antimicrobial resistance genes
2. **MGE.csv**: Counts of mobile genetic elements (IS elements, transposons)
3. **MIC.csv**: Minimum inhibitory concentration values for 5 antibiotics
4. **MLST.csv**: Sequence type and allele profiles for 7 loci
5. **Plasmid.csv**: Plasmid presence/absence data
6. **Serotype.csv**: Capsular serotype information
7. **Virulence.csv**: Binary presence/absence of 10 virulence factors
8. **Snp_tree.newick**: SNP-based phylogenetic tree

## Design Principles

1. **Separation of Concerns**: Testable logic separated into `utils.py`
2. **Type Safety**: Proper data type handling for Streamlit compatibility
3. **Error Handling**: Comprehensive error handling with user-friendly messages
4. **Validation**: Data validation at multiple levels
5. **Testing**: >95% coverage on critical mathematical functions
6. **Documentation**: Comprehensive docstrings and comments
7. **Reproducibility**: Fixed random seeds for reproducible results

## Future Enhancements

Potential additions:
1. More advanced clustering algorithms
2. Machine learning model training and evaluation
3. Comparative genomics analysis
4. Network analysis
5. Time-series analysis
6. Advanced phylogenetic tree manipulation
7. Integration with external databases
8. Batch processing capabilities

## License
MIT License

## Authors
MK-vet

## Citation
If you use this tool in your research, please cite appropriately.
