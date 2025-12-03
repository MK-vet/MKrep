# Mathematical Validation - StrepSuisAnalyzer

## Overview

This document describes the mathematical validation methodology used in StrepSuisAnalyzer to ensure statistical correctness and numerical stability.

## Mathematical Properties Validated

### 1. Entropy

**Shannon Entropy** measures information content in a distribution.

**Properties Tested:**
- **Non-negativity**: H(X) ≥ 0
- **Upper bound**: H(X) ≤ log₂(n) where n is the number of categories
- **Zero entropy**: H(X) = 0 for deterministic distributions
- **Maximum entropy**: H(X) = log₂(n) for uniform distributions

**Implementation:**
```python
H(X) = -Σ p(x) log₂(p(x))
```

**Tests:**
- Uniform distribution over n categories → H(X) ≈ log₂(n)
- Constant value → H(X) ≈ 0
- All values non-negative

### 2. Mutual Information

**Mutual Information** measures dependence between two variables.

**Properties Tested:**
- **Non-negativity**: MI(X,Y) ≥ 0
- **Symmetry**: MI(X,Y) = MI(Y,X)
- **Upper bound**: MI(X,Y) ≤ min(H(X), H(Y))
- **Independence**: MI(X,Y) = 0 for independent X and Y

**Implementation:**
```python
MI(X,Y) = H(X) + H(Y) - H(X,Y)
```

**Tests:**
- Independent variables → MI ≈ 0
- Perfect dependence → MI = H(X) = H(Y)
- Symmetry property verified

### 3. Cramér's V

**Cramér's V** measures association strength between categorical variables.

**Properties Tested:**
- **Bounds**: 0 ≤ V ≤ 1
- **Perfect association**: V = 1 for perfect 1-to-1 mapping
- **Independence**: V ≈ 0 for independent variables
- **Symmetry**: V(X,Y) = V(Y,X)

**Implementation:**
```python
V = √(χ² / (n × min(r-1, c-1)))
```

where:
- χ² = chi-square statistic
- n = sample size
- r, c = number of rows, columns in contingency table

**Tests:**
- Perfect association (1-to-1 mapping) → V = 1
- Random independent variables → V ≈ 0
- Value always in [0, 1]

### 4. Phi Coefficient

**Phi Coefficient** measures association between binary variables.

**Properties Tested:**
- **Bounds**: -1 ≤ φ ≤ 1
- **Perfect positive association**: φ = 1
- **Perfect negative association**: φ = -1
- **Independence**: φ ≈ 0
- **Relationship to chi-square**: φ² = χ² / n

**Implementation:**
```python
φ = (ad - bc) / √((a+b)(c+d)(a+c)(b+d))
```

For 2×2 contingency table:
```
      Y=0  Y=1
X=0    a    b
X=1    c    d
```

**Tests:**
- Perfectly correlated binaries → φ = 1
- Independent binaries → φ ≈ 0
- Value always in [-1, 1]

### 5. Correlation Coefficients

**Pearson, Spearman, and Kendall correlations** measure linear and monotonic relationships.

**Properties Tested:**
- **Bounds**: -1 ≤ r ≤ 1
- **Perfect positive**: r = 1 for perfect positive linear relationship
- **Perfect negative**: r = -1 for perfect negative linear relationship
- **Independence**: r ≈ 0 for uncorrelated variables
- **Symmetry**: corr(X,Y) = corr(Y,X)

**Implementation:**

Pearson:
```python
r = Σ((x - x̄)(y - ȳ)) / √(Σ(x - x̄)² × Σ(y - ȳ)²)
```

**Tests:**
- Perfect linear relationship → |r| = 1
- Uncorrelated variables → r ≈ 0
- Value always in [-1, 1]

### 6. P-values

**P-values** indicate statistical significance.

**Properties Tested:**
- **Bounds**: 0 ≤ p ≤ 1
- **Uniform distribution under null**: p ~ Uniform(0,1)
- **Consistency**: Multiple tests on same data give same p-value

**Tests Applied to:**
- t-test
- Mann-Whitney U test
- ANOVA
- Kruskal-Wallis test
- Chi-square test
- Correlation tests

**Validation:**
- All p-values in [0, 1]
- Identical groups → p ≈ 1
- Very different groups → p ≈ 0

### 7. Robinson-Foulds Distance

**Robinson-Foulds (RF) Distance** measures phylogenetic tree dissimilarity.

**Properties Tested:**
- **Non-negativity**: RF(T1,T2) ≥ 0
- **Identity**: RF(T,T) = 0
- **Symmetry**: RF(T1,T2) = RF(T2,T1)
- **Triangle inequality**: RF(T1,T3) ≤ RF(T1,T2) + RF(T2,T3)
- **Upper bound**: RF ≤ 2(n-3) for n taxa
- **Normalized bounds**: 0 ≤ RF_norm ≤ 1

**Implementation:**
```python
RF = |B₁ \ B₂| + |B₂ \ B₁|
```

where B₁, B₂ are sets of bipartitions

**Tests:**
- Identical trees → RF = 0
- Different trees → RF > 0
- Normalized RF in [0, 1]

### 8. Meta-Analysis Metrics

**Fixed and Random Effects Models** for combining study results.

**Properties Tested:**

**Variance:**
- **Positivity**: σ² > 0
- **Decreasing with sample size**: Larger studies have smaller variance

**Standard Error:**
- **Positivity**: SE > 0
- **Relationship**: SE = √σ²

**Tau-squared (Between-study variance):**
- **Non-negativity**: τ² ≥ 0
- **Homogeneity**: τ² ≈ 0 for homogeneous studies
- **Heterogeneity**: τ² > 0 for heterogeneous studies

**Cochran's Q:**
- **Non-negativity**: Q ≥ 0
- **Chi-square distribution**: Q ~ χ²(k-1) under homogeneity
- **P-value bounds**: 0 ≤ p ≤ 1

**Implementation:**

Fixed effects:
```python
θ_FE = Σ(w_i × θ_i) / Σw_i
σ²_FE = 1 / Σw_i
where w_i = 1/σ²_i
```

Random effects (DerSimonian-Laird):
```python
τ² = max(0, (Q - (k-1)) / C)
w*_i = 1/(σ²_i + τ²)
θ_RE = Σ(w*_i × θ_i) / Σw*_i
```

**Tests:**
- Homogeneous studies → τ² ≈ 0
- Heterogeneous studies → τ² > 0
- Variances always positive

### 9. Multiple Testing Correction

**Bonferroni and FDR Corrections** control family-wise error rate.

**Properties Tested:**
- **Corrected p-values**: 0 ≤ p_adj ≤ 1
- **Monotonicity**: p_adj ≥ p_raw
- **Conservative bound**: p_bonf ≤ min(1, k × p)
- **FDR control**: E[FDR] ≤ α under independence

**Implementation:**

Bonferroni:
```python
p_bonf = min(1, k × p)
```

Benjamini-Hochberg FDR:
```python
p_BH(i) = min(1, (k/i) × p(i))
```

**Tests:**
- Corrected p-values in [0, 1]
- Bonferroni ≤ 1.0
- FDR more powerful than Bonferroni

## Numerical Stability

### Log-sum-exp Trick

For probabilities and scores:
```python
log(Σ exp(x_i)) = log_max + log(Σ exp(x_i - log_max))
```

### Zero Division Protection

```python
result = numerator / (denominator + ε)
```

where ε = 1e-10

### NaN Handling

- Explicit NaN removal before calculations
- Return NaN for invalid inputs
- Document NaN behavior in docstrings

## Validation Test Suite

### Test Coverage

- **100%** coverage of mathematical properties
- **Edge cases**: Zero, infinity, NaN values
- **Boundary conditions**: Minimum and maximum values
- **Invariants**: Properties that must always hold
- **Synthetic data**: Known ground-truth validation

### Test Execution

```bash
# Run all mathematical validation tests
pytest -m mathematical -v

# Show detailed mathematical property checks
pytest tests/test_mathematical_validation.py -vv
```

## References

1. Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379-423.

2. Cramér, H. (1946). *Mathematical Methods of Statistics*. Princeton University Press.

3. Robinson, D. F., & Foulds, L. R. (1981). Comparison of phylogenetic trees. *Mathematical Biosciences*, 53(1-2), 131-147.

4. DerSimonian, R., & Laird, N. (1986). Meta-analysis in clinical trials. *Controlled Clinical Trials*, 7(3), 177-188.

5. Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A practical and powerful approach to multiple testing. *Journal of the Royal Statistical Society: Series B*, 57(1), 289-300.

## Continuous Monitoring

All mathematical properties are continuously validated through:
- Automated test suite (400+ tests)
- Pre-commit hooks
- Continuous integration (CI/CD)
- Code review requirements

Any violation of mathematical properties causes immediate test failure.
