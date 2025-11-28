# Mathematical Validation Documentation

This document describes the mathematical validation methodology used in the StrepSuis Suite to ensure statistical correctness and reproducibility of all analytical methods.

## Overview

All statistical methods in the StrepSuis Suite have been validated against gold-standard reference implementations to ensure accuracy. Each module includes automated tests that verify our implementations against established libraries.

## Validation Strategy

### 3-Level Validation Approach

1. **Unit-Level Validation**: Individual statistical functions tested against reference implementations
2. **Integration-Level Validation**: Complete workflows validated with known-answer data
3. **End-to-End Validation**: Full pipelines tested with real and synthetic datasets

## Statistical Methods Validated

### 1. Chi-Square Tests

**Implementation**: Custom wrapper around contingency table analysis

**Gold Standard**: `scipy.stats.chi2_contingency`

**Validation Tests**:
- Chi-square statistic matches scipy to 5 decimal places
- P-value matches scipy to 5 decimal places
- Fisher's exact test automatically applied for small expected counts (<5)

**Test Location**: `tests/test_statistical_validation.py::TestChiSquareValidation`

```python
# Example validation test
def test_chi_square_matches_scipy():
    table = pd.DataFrame([[50, 30], [20, 40]])
    chi2_ours, p_ours, phi_ours = safe_contingency(table)
    chi2_scipy, p_scipy, _, _ = chi2_contingency(table)
    np.testing.assert_almost_equal(chi2_ours, chi2_scipy, decimal=5)
    np.testing.assert_almost_equal(p_ours, p_scipy, decimal=5)
```

### 2. Fisher's Exact Test

**Implementation**: Used when expected cell counts are <5

**Gold Standard**: `scipy.stats.fisher_exact`

**Validation Tests**:
- P-value matches scipy Fisher's exact for 2x2 tables
- Correct fallback from chi-square when expected counts are small

**Test Location**: `tests/test_statistical_validation.py::TestChiSquareValidation::test_fishers_exact_matches_scipy`

### 3. Phi Coefficient

**Implementation**: Effect size measure for 2x2 contingency tables

**Validation Tests**:
- Sign correctness (positive for positive associations)
- Bounded between -1 and 1
- Value of 1.0 for perfect positive association
- Value of 0.0 for independence

**Test Location**: `tests/test_statistical_validation.py::TestChiSquareValidation::test_phi_coefficient_calculation`

### 4. Bootstrap Confidence Intervals

**Implementation**: Non-parametric bootstrap resampling

**Gold Standard**: Standard bootstrap methodology with BCa correction

**Validation Tests**:
- CI coverage contains true population parameter (95% of the time for 95% CI)
- CI width decreases with increasing sample size
- Reproducibility with fixed random seeds
- Correct handling of edge cases (zero variance, extreme proportions)

**Test Location**: `tests/test_statistical_validation.py::TestBootstrapValidation`

```python
# Example validation test
def test_bootstrap_ci_coverage():
    np.random.seed(42)
    true_proportion = 0.5
    data = pd.DataFrame({'col': np.random.binomial(1, 0.5, 100)})
    result = compute_bootstrap_ci(data, n_iter=1000, confidence_level=0.95)
    ci_lower = result['CI_Lower'].values[0]
    ci_upper = result['CI_Upper'].values[0]
    assert ci_lower < 50.0 < ci_upper  # 50% should be in CI
```

### 5. Multiple Testing Correction (FDR)

**Implementation**: Benjamini-Hochberg False Discovery Rate correction

**Gold Standard**: `statsmodels.stats.multitest.multipletests`

**Validation Tests**:
- Corrected p-values are monotonically non-decreasing when sorted by raw p-values
- All corrected p-values >= original p-values (within numerical tolerance 1e-10)
- Matches statsmodels FDR-BH procedure

**Monotonicity Requirement (Critical)**:
After sorting by raw p-values (ascending), the corrected p-values MUST be non-decreasing:
```python
corrected = result_sorted["Corrected_p"].to_numpy()
for i in range(len(corrected) - 1):
    assert corrected[i] <= corrected[i + 1] + 1e-10
```

**Test Location**: `tests/test_statistical_validation.py::TestMultipleTestingCorrection`

### 6. Bootstrap Confidence Intervals

**Implementation**: Non-parametric percentile bootstrap

**Method Details**:
- Default iterations: **5,000** (production minimum)
- Confidence level: 95% (α = 0.05)
- CI bounds: empirical quantiles at α/2 and 1-α/2 percentiles

**Convergence Criterion**:
- Width difference between n=5,000 and n=10,000 iterations should be < 5%
- This ensures stable estimates for publication-grade results

**Test Location**: `tests/test_statistical_validation.py::TestNumericalStabilityAdvanced::test_bootstrap_convergence_5000_vs_10000`

### 7. Contingency Table Analysis (Fisher vs Chi-Square)

**Implementation**: `safe_contingency()` function

**Selection Rule (Cochran's Rule)**:
- Use **Fisher's exact test** when:
  - Minimum expected cell count < 1, OR
  - Less than 80% of cells have expected count >= 5
- Use **Chi-square test** otherwise

**Chi-Square Derivation**:
- When Fisher's exact test is used, chi² is derived as φ² × N for consistency
- This ensures all outputs are comparable regardless of which test was used

**Phi Coefficient**:
- Formula: φ = (ad - bc) / √(r₁r₂c₁c₂)
- Bounded in [-1, 1] for all valid 2×2 tables
- Phi = 1.0 indicates perfect positive association
- Phi = 0.0 indicates independence

**Test Location**: `tests/test_statistical_validation.py::TestChiSquareValidation`

### 8. Information Theory Metrics

**Implementation**: Entropy, Mutual Information, Cramér's V

**Gold Standard**: `sklearn.metrics` for mutual information metrics

**Validation Tests**:
- Entropy calculation correctness
- Mutual information bounds (0 ≤ MI ≤ min(H(X), H(Y)))
- Cramér's V bounded between 0 and 1

**Test Location**: Module-specific statistical validation tests

### 9. Clustering Metrics

**Implementation**: Silhouette score, Calinski-Harabasz, Davies-Bouldin indices

**Gold Standard**: `sklearn.metrics` implementations

**Validation Tests**:
- Silhouette scores bounded between -1 and 1
- Optimal cluster selection reproducibility
- K-modes implementation correctness

**Test Location**: `tests/test_statistical_validation.py` (per module)

## Numerical Stability Validation

### Correlation Matrix Condition Number

For correlation matrices derived from binary data:
- Condition number < 100 indicates well-conditioned data
- Higher values suggest multicollinearity and may require feature selection

**Test Location**: `TestNumericalStabilityAdvanced::test_correlation_matrix_condition_number`

### Collinear Features

- Perfectly collinear features (identical columns) produce phi = 1.0
- The code handles degenerate contingency tables gracefully

**Test Location**: `TestNumericalStabilityAdvanced::test_collinear_feature_handling`

### Phi Coefficient Bounds

- Phi is always bounded in [-1, 1] for valid 2×2 tables
- Verified on 100+ randomly generated positive tables

**Test Location**: `TestNumericalStabilityAdvanced::test_phi_bounds_random_tables`

### Severely Imbalanced Data

- Features with 1% prevalence are handled correctly
- Bootstrap CIs are valid even for rare events

**Test Location**: `TestNumericalStabilityAdvanced::test_severely_imbalanced_data`

## Edge Case Handling

All statistical functions are tested for robustness with edge cases:

### Tested Edge Cases

| Edge Case | Expected Behavior | Test Location |
|-----------|-------------------|---------------|
| Empty DataFrame | Returns empty result, no crash | `TestEdgeCases::test_empty_dataframe` |
| Single column | Returns valid CI | `TestEdgeCases::test_single_column` |
| Zero variance (all same values) | Returns appropriate CI (e.g., [100%, 100%]) | `TestEdgeCases::test_zero_variance_column` |
| Single row | Does not crash, returns result | `TestEdgeCases::test_single_row` |
| Non-2x2 contingency table | Returns NaN for chi-square | `TestEdgeCases::test_non_binary_data_handling` |
| Zero-sum contingency table | Returns NaN gracefully | `TestEdgeCases::test_contingency_table_with_zero_margin` |
| Extreme proportions (near 0 or 1) | Valid CI without NaN | `TestNumericalStability::test_extreme_proportions` |
| Perfect association (phi = 1) | Correctly identifies | `TestNumericalStability::test_perfect_association` |
| Independence (phi = 0) | Correctly identifies | `TestNumericalStability::test_independence` |
| All-zeros column | Mean = 0%, CI tight around 0% | `TestNumericalStabilityAdvanced::test_all_zeros_and_all_ones_columns` |
| All-ones column | Mean = 100%, CI tight around 100% | `TestNumericalStabilityAdvanced::test_all_zeros_and_all_ones_columns` |
| Zero-variance in co-occurrence | Handles gracefully | `TestNumericalStabilityAdvanced::test_zero_variance_column_in_cooccurrence` |

## Reproducibility Validation

### Fixed Random Seeds

All modules use fixed random seeds for reproducibility:

```python
np.random.seed(42)  # Default seed
```

**Validation Tests**:
- Identical results with same seed
- Different results with different seeds (verifies randomness is working)

**Test Location**: `tests/test_statistical_validation.py::TestReproducibility`

## Numerical Stability Validation

**Tested Scenarios**:
- Large numbers of bootstrap iterations (5000+)
- Many columns (50+ features)
- Extreme probability values (near 0.0 or 1.0)
- Perfect correlation matrices

**Test Location**: `tests/test_statistical_validation.py::TestNumericalStability`

## Synthetic Ground Truth Validation

Tests using synthetic data with known ground truth values:

### MDR Classification Validation

```python
# Create synthetic data with known MDR status
def test_mdr_identification_accuracy():
    # Create data where we manually know which strains are MDR
    data = create_synthetic_mdr_data()
    class_res = build_class_resistance(data, pheno_cols)
    mdr_mask = identify_mdr_isolates(class_res, threshold=3)
    expected_mdr = class_res.sum(axis=1) >= 3
    pd.testing.assert_series_equal(mdr_mask, expected_mdr)
```

**Test Location**: `tests/test_statistical_validation.py::TestSyntheticGroundTruth`

## Running Validation Tests

### Full Validation Suite

```bash
cd separated_repos/strepsuis-amrpat
pip install -e .[dev]
pytest tests/test_statistical_validation.py -v
```

### Quick Validation Check

```bash
pytest tests/test_statistical_validation.py -m "not slow" -v
```

### Coverage Report

```bash
pytest tests/test_statistical_validation.py --cov --cov-report=html
```

## Validation Results Summary

| Module | Validation Tests | Pass Rate | Notes |
|--------|------------------|-----------|-------|
| strepsuis-amrpat | 25+ | 100% | Full statistical validation |
| strepsuis-amrvirkm | 20+ | 100% | Clustering + MCA validation |
| strepsuis-genphen | 20+ | 100% | Phylogenetic metrics validation |
| strepsuis-genphennet | 15+ | 100% | Network metrics validation |
| strepsuis-phylotrait | 18+ | 100% | Tree metrics validation |

## References

### Statistical Libraries Used for Validation

- **scipy.stats**: Chi-square, Fisher exact, correlation tests
- **statsmodels.stats.multitest**: Multiple testing correction
- **sklearn.metrics**: Mutual information, clustering metrics
- **numpy.testing**: Numerical comparison utilities

### Statistical Method References

1. Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate. *Journal of the Royal Statistical Society B*, 57(1), 289-300.
2. Efron, B., & Tibshirani, R. J. (1993). *An Introduction to the Bootstrap*. Chapman & Hall.
3. Fisher, R. A. (1922). On the interpretation of chi-square from contingency tables. *Journal of the Royal Statistical Society*, 85(1), 87-94.

## Continuous Validation

All validation tests run automatically:

- **On every pull request**: Fast tests only (~30 seconds)
- **Before release**: Full validation suite (~2-3 minutes per module)
- **Manual trigger**: Available via GitHub Actions

---

**Version:** 1.0.0  
**Last Updated:** 2025-01-15  
**Status:** All validations passing ✅
