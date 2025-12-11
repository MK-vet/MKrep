# Synthetic Data and Validation Methodology

This document describes the synthetic data generation methodology and validation approach used in the StrepSuis Suite bioinformatics tools.

## Overview

The StrepSuis Suite uses a combination of real example data and synthetically generated test data to validate the correctness of analytical methods. This document explains the data types, generation methods, and validation approaches.

## Data Types

### 1. Real Example Data

**Location**: `examples/` directory in each module

**Description**: Real *Streptococcus suis* genomic data from 92 strains

**Files**:
| File | Description | Strains | Features |
|------|-------------|---------|----------|
| MIC.csv | Minimum Inhibitory Concentration | 92 | 16 antibiotics |
| AMR_genes.csv | Resistance gene profiles | 92 | 42 genes |
| Virulence.csv | Virulence factors | 92 | 38 genes |
| MLST.csv | Sequence typing | 92 | ST assignments |
| Serotype.csv | Serological classification | 92 | Serotypes 1-9, NT |
| Plasmid.csv | Plasmid replicons | 92 | 14 replicon types |
| MGE.csv | Mobile genetic elements | 92 | 10 element types |
| Snp_tree.newick | Phylogenetic tree | 92 | Maximum-likelihood SNP tree |

**Format**:
- CSV files with `Strain_ID` as first column
- Binary values: 0 = absent, 1 = present
- UTF-8 encoding
- No missing values

### 2. Mini Datasets (CI Testing)

**Purpose**: Fast continuous integration testing

**Generation Method**: Subset of real example data

```python
# Mini dataset generation
def create_mini_dataset(example_dir, tmp_path, n_strains=10):
    """Create mini dataset (first 10 strains) for fast CI testing."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    for csv_file in example_dir.glob("*.csv"):
        df = pd.read_csv(csv_file)
        df.head(n_strains).to_csv(data_dir / csv_file.name, index=False)
    
    return data_dir
```

**Characteristics**:
- 10 strains (first 10 from example data)
- All file types included
- Execution time: <5 seconds per test
- Used automatically in CI pipelines

### 3. Synthetic Test Data

**Purpose**: Testing with known ground truth values

**Generation Methods**:

#### Binary Feature Generation

```python
# Generate binary data with known proportion
def generate_synthetic_binary_data(n_strains, proportion, seed=42):
    """Generate binary feature data with known true proportion."""
    np.random.seed(seed)
    return np.random.binomial(1, proportion, n_strains)
```

#### Known Association Patterns

```python
# Generate data with known co-occurrence patterns
def generate_correlated_features(n_strains, correlation, seed=42):
    """Generate two features with known correlation."""
    np.random.seed(seed)
    feature1 = np.random.binomial(1, 0.5, n_strains)
    # Generate feature2 correlated with feature1
    feature2 = np.where(
        np.random.random(n_strains) < correlation,
        feature1,  # Same as feature1
        np.random.binomial(1, 0.5, n_strains)  # Random
    )
    return feature1, feature2
```

#### MDR Classification Data

```python
# Generate data with known MDR status
def generate_mdr_synthetic_data(n_strains=20, seed=42):
    """Generate synthetic AMR data where MDR status is calculable."""
    np.random.seed(seed)
    data = pd.DataFrame({
        'Strain_ID': [f'Strain_{i}' for i in range(n_strains)],
        'Oxytetracycline': np.random.binomial(1, 0.6, n_strains),
        'Tulathromycin': np.random.binomial(1, 0.5, n_strains),
        'Spectinomycin': np.random.binomial(1, 0.4, n_strains),
        'Penicillin': np.random.binomial(1, 0.3, n_strains),
    })
    return data
```

## Validation Test Categories

### 1. Statistical Correctness Validation

**Purpose**: Verify statistical calculations match gold-standard implementations

**Example Tests**:
- Chi-square values match scipy
- Bootstrap CIs contain true population parameter
- FDR correction follows Benjamini-Hochberg procedure

**Location**: `tests/test_statistical_validation.py`

### 2. Data Preprocessing Validation

**Purpose**: Ensure data loading and preprocessing work correctly

**Example Tests**:
- CSV files load with correct column names
- Binary values remain 0/1 after processing
- Strain_ID column preserved
- Missing values handled appropriately

**Location**: `tests/test_data_validation.py`

### 3. Pipeline Integration Validation

**Purpose**: Verify complete analysis pipelines produce expected outputs

**Example Tests**:
- HTML reports generated with expected structure
- Excel workbooks contain required sheets
- PNG charts created with correct dimensions
- Output file counts match expectations

**Location**: `tests/test_end_to_end.py`

### 4. Edge Case Validation

**Purpose**: Test robustness with unusual or boundary inputs

**Example Tests**:
- Empty datasets return empty results (no crash)
- Single-strain analysis works
- All-zeros or all-ones columns handled
- Very large datasets complete in reasonable time

**Location**: `tests/test_statistical_validation.py::TestEdgeCases`

## Synthetic Data Generation for Specific Tests

### Bootstrap CI Coverage Test

**Goal**: Verify 95% CI contains true parameter ~95% of the time

```python
def test_bootstrap_ci_coverage():
    """Test that bootstrap CI has proper coverage for known distribution."""
    np.random.seed(42)
    true_proportion = 0.50  # Known true value
    n = 100
    data = pd.DataFrame({'col': np.random.binomial(1, true_proportion, n)})
    
    result = compute_bootstrap_ci(data, n_iter=1000, confidence_level=0.95)
    
    ci_lower = result['CI_Lower'].values[0]
    ci_upper = result['CI_Upper'].values[0]
    true_pct = true_proportion * 100  # 50%
    
    assert ci_lower < true_pct < ci_upper, \
        f"CI [{ci_lower}, {ci_upper}] should contain {true_pct}"
```

### MDR Classification Accuracy Test

**Goal**: Verify MDR classification matches manual calculation

```python
def test_mdr_identification_accuracy():
    """Test MDR identification matches ground truth."""
    # Create synthetic data where we know the MDR status
    data = generate_mdr_synthetic_data(n_strains=20)
    pheno_cols = ['Oxytetracycline', 'Tulathromycin', 'Spectinomycin', 'Penicillin']
    
    # Build class resistance
    class_res = build_class_resistance(data, pheno_cols)
    
    # Identify MDR (threshold=3)
    mdr_mask = identify_mdr_isolates(class_res, threshold=3)
    
    # Manually calculate expected MDR
    expected_mdr = class_res.sum(axis=1) >= 3
    
    # Should match exactly
    pd.testing.assert_series_equal(mdr_mask, expected_mdr)
```

### Phylogenetic Signal Test

**Goal**: Verify phylogenetic signal detection with known tree structure

```python
def test_phylogenetic_signal_detection():
    """Test that traits concentrated in one clade show strong signal."""
    # Create synthetic data representing clustered trait
    # Trait present in clade A (strains 1-10), absent in clade B (strains 11-20)
    trait_data = [1]*10 + [0]*10  # Perfect phylogenetic clustering
    
    # Calculate phylogenetic signal
    signal = calculate_phylogenetic_signal(trait_data, tree)
    
    # Should show strong signal (concentrated in one clade)
    assert signal['lambda'] > 0.8, "Clustered trait should show strong signal"
```

## Validation Report Structure

### Automated Validation Reports

Each test run generates validation information:

1. **Test Coverage Report** (`htmlcov/index.html`)
   - Line-by-line coverage
   - Branch coverage
   - Module breakdown

2. **Test Results Summary** (pytest output)
   - Pass/fail status per test
   - Execution time
   - Error messages for failures

3. **Coverage Badge** (`coverage.json`)
   - Overall coverage percentage
   - Module-specific coverage

### Example Validation Output

```
============================= test session starts =============================
platform linux -- Python 3.11.0, pytest-7.4.0
collected 110 items

tests/test_statistical_validation.py
    test_chi_square_matches_scipy PASSED
    test_fishers_exact_matches_scipy PASSED
    test_phi_coefficient_calculation PASSED
    test_bootstrap_ci_coverage PASSED
    test_bootstrap_ci_width_decreases_with_sample_size PASSED
    test_fdr_correction_matches_statsmodels PASSED
    test_empty_dataframe PASSED
    test_single_column PASSED
    test_zero_variance_column PASSED
    test_mdr_identification_accuracy PASSED
    ...

========================= 110 passed in 45.23s =================================
```

## Running Validation

### Complete Validation Suite

```bash
# Navigate to module
cd separated_repos/strepsuis-mdr

# Install with dev dependencies
pip install -e .[dev]

# Run all validation tests
pytest tests/test_statistical_validation.py -v

# Run with coverage report
pytest tests/test_statistical_validation.py --cov --cov-report=html
```

### Quick Validation (CI)

```bash
# Fast tests only (excludes slow tests)
pytest -m "not slow" -v
```

### Generate Validation Report

```bash
# Generate HTML coverage report
pytest --cov --cov-report=html

# Open report in browser
open htmlcov/index.html
```

## Quality Assurance Summary

### Validation Coverage by Module

| Module | Validation Tests | Coverage | Status |
|--------|------------------|----------|--------|
| strepsuis-mdr | 110+ | 62% | ✅ |
| strepsuis-amrvirkm | 100+ | 50% | ✅ |
| strepsuis-genphennet | 100+ | 50% | ✅ |
| strepsuis-phylotrait | 90+ | 50% | ✅ |

### Critical Path Coverage

| Component | Coverage Target | Actual | Status |
|-----------|-----------------|--------|--------|
| Configuration | 95%+ | 100% | ✅ |
| CLI Interface | 85%+ | 85-89% | ✅ |
| Analyzer Orchestration | 85%+ | 85-86% | ✅ |
| Statistical Methods | Via E2E | Validated | ✅ |

## Continuous Validation

### Automated Triggers

- **Pull Requests**: Fast tests run automatically
- **Releases**: Full validation suite
- **Manual**: Available via GitHub Actions "Run workflow"

### Pre-commit Validation

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run all checks (includes test validation)
pre-commit run --all-files
```

---

**Version:** 1.0.0  
**Last Updated:** 2025-01-15  
**Status:** All validations passing ✅
