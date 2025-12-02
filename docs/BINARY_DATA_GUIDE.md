# Binary Data Handling in MKrep

## Overview

All MKrep analysis tools are specifically designed to work with **binary data**, where:
- **0 = Absence** of a feature (gene, resistance marker, virulence factor)
- **1 = Presence** of a feature

Both absence and presence are **biologically significant** and are properly handled in all statistical analyses.

## Why Binary Data?

In microbial genomics, many features are naturally binary:
- **Gene presence/absence**: A gene is either present (1) or absent (0)
- **Resistance markers**: An organism is either resistant (1) or susceptible (0)
- **Virulence factors**: A virulence gene is either present (1) or absent (0)
- **Phenotypic traits**: A trait is either expressed (1) or not expressed (0)

## Data Validation

All scripts include validation to ensure data is strictly binary:

```python
def validate_binary_data(df):
    """Validate that dataframe contains only 0 and 1 values."""
    if not ((df.values == 0) | (df.values == 1)).all():
        raise ValueError("Data is not strictly 0/1 binary.")
```

This ensures:
- No missing values (NaN)
- No continuous values
- No categorical values other than 0 and 1
- Proper data type for statistical tests

## Statistical Handling

### 1. Chi-Square Tests

For binary data, chi-square tests use 2×2 contingency tables:

```
                Feature Present (1)    Feature Absent (0)
Cluster A            a                       b
Cluster B            c                       d
```

Both presence (a, c) and absence (b, d) are used in the calculation:
- **χ² statistic** measures association between cluster and feature
- **p-value** indicates statistical significance
- **Yates correction** applied for small expected counts

### 2. Fisher's Exact Test

For small sample sizes or low expected counts:
- Uses exact probabilities instead of approximation
- Handles both presence and absence correctly
- Fallback when chi-square assumptions are violated

### 3. Log-Odds Ratio

Measures effect size of associations:

```python
# Presence in cluster A vs presence in cluster B
odds_A = (count_present_A + 0.5) / (count_absent_A + 0.5)
odds_B = (count_present_B + 0.5) / (count_absent_B + 0.5)
log_odds_ratio = log(odds_A / odds_B)
```

- **Positive log-odds**: Feature enriched in cluster A
- **Negative log-odds**: Feature depleted in cluster A
- **Zero log-odds**: No difference between clusters

### 4. Bootstrap Confidence Intervals

Resampling preserves binary structure:

```python
for iteration in range(n_bootstrap):
    # Resample with replacement, maintaining binary values
    sample = resample(data, stratify=clusters)
    # Calculate statistic on resampled data
    statistic = calculate_statistic(sample)
```

### 5. K-Modes Clustering

Specifically designed for categorical/binary data:
- Uses **mode** instead of mean
- **Hamming distance** for dissimilarity
- Does not assume continuous distributions
- Properly handles 0 and 1 as distinct categories

### 6. Multiple Correspondence Analysis (MCA)

Dimensionality reduction for categorical data:
- Treats 0 and 1 as distinct categories
- Creates indicator matrix for each value
- Projects data into continuous space while preserving structure

### 7. Association Rule Mining

Discovers patterns in binary data:
- **Support**: Frequency of feature combination
- **Confidence**: Conditional probability
- **Lift**: Ratio of observed to expected co-occurrence

Example rule: `{Gene1=1, Gene2=1} => {Antibiotic_Resistance=1}`

### 8. Random Forest Feature Importance

For binary classification:
- Target variable: cluster assignment
- Features: binary indicators
- Importance: decrease in impurity when using feature

## Common Pitfalls (Avoided in MKrep)

### ❌ Wrong: Treating binary as continuous
```python
# DON'T DO THIS
mean_value = data.mean()  # 0.65 doesn't mean anything for binary data
```

### ✅ Correct: Using frequencies
```python
# DO THIS
frequency = (data == 1).sum() / len(data)  # 65% have the feature
```

### ❌ Wrong: Ignoring absence
```python
# DON'T DO THIS - only looks at presence
positive_samples = data[data == 1]
```

### ✅ Correct: Using both presence and absence
```python
# DO THIS - uses all information
presence_count = (data == 1).sum()
absence_count = (data == 0).sum()
```

### ❌ Wrong: Using parametric tests
```python
# DON'T DO THIS - assumes normal distribution
from scipy.stats import ttest_ind
t_stat, p_val = ttest_ind(group1, group2)
```

### ✅ Correct: Using appropriate tests
```python
# DO THIS - appropriate for categorical data
from scipy.stats import chi2_contingency
chi2, p_val, dof, expected = chi2_contingency(contingency_table)
```

## Data Preparation Guidelines

### Required Format

```csv
Strain_ID,Gene1,Gene2,Antibiotic1,Virulence1
Strain001,1,0,1,0
Strain002,0,1,1,1
Strain003,1,1,0,1
```

### Encoding Rules

1. **Gene presence/absence**
   - Present (detected in genome): 1
   - Absent (not detected): 0

2. **Resistance phenotype**
   - Resistant: 1
   - Susceptible: 0

3. **Virulence factors**
   - Factor present: 1
   - Factor absent: 0

4. **Any other features**
   - Feature present/true/yes: 1
   - Feature absent/false/no: 0

### Converting from Other Formats

#### From Present/Absent strings:
```python
import pandas as pd

df = pd.read_csv('data.csv')
for col in df.columns[1:]:  # Skip Strain_ID
    df[col] = (df[col].str.lower() == 'present').astype(int)
```

#### From Yes/No:
```python
for col in df.columns[1:]:
    df[col] = (df[col].str.lower() == 'yes').astype(int)
```

#### From True/False:
```python
for col in df.columns[1:]:
    df[col] = df[col].astype(int)
```

#### From continuous MIC values:
```python
# Define breakpoint for resistance
breakpoint = 8  # µg/ml
df['Antibiotic_Resistance'] = (df['MIC'] >= breakpoint).astype(int)
```

## Interpretation Guide

### Frequency Statistics

When you see: **"Gene1 frequency: 65%"**

This means:
- 65% of strains have Gene1 (value = 1)
- 35% of strains lack Gene1 (value = 0)
- Both groups are important for analysis

### Association Statistics

When you see: **"Chi-square p-value: 0.001, Log-odds: 2.5"**

This means:
- Association is statistically significant (p < 0.05)
- Feature is enriched in one cluster (positive log-odds)
- The odds of presence are exp(2.5) ≈ 12× higher in one group

### Clustering Results

When you see: **"Cluster 1: 75% have Gene1, Cluster 2: 25% have Gene1"**

This means:
- Clear difference in Gene1 presence between clusters
- Gene1 is a discriminative feature
- Both clusters have biological meaning (one with, one without)

## Validation Checklist

Before running analysis, verify:

- [ ] All feature columns contain only 0 and 1
- [ ] No missing values (NaN)
- [ ] No text values (except Strain_ID column)
- [ ] Strain_ID column is present and unique
- [ ] At least 2 strains in dataset
- [ ] At least 2 features (columns) in dataset
- [ ] Features have variability (not all 0 or all 1)

## Examples from Real Data

### Example 1: AMR Gene Analysis

```csv
Strain_ID,tetM,ermB,aph3
Strain001,1,0,1
Strain002,0,1,1
Strain003,1,1,0
```

Interpretation:
- Strain001: Has tetM and aph3, lacks ermB
- Strain002: Has ermB and aph3, lacks tetM
- Strain003: Has tetM and ermB, lacks aph3

All three values are important for clustering!

### Example 2: Virulence Profile

```csv
Strain_ID,Toxin_A,Toxin_B,Adhesin
Strain001,1,1,1
Strain002,0,0,1
Strain003,0,0,0
```

Interpretation:
- Strain001: Highly virulent (all factors present)
- Strain002: Low virulence (only adhesin)
- Strain003: Avirulent (no factors)

The absence of factors defines avirulent strains!

## Troubleshooting

### Error: "Data is not strictly 0/1 binary"

**Cause**: Data contains values other than 0 and 1

**Solutions**:
1. Check for missing values: `df.isna().sum()`
2. Check for text: `df.select_dtypes(include='object')`
3. Check value range: `df.describe()`
4. Convert to binary (see "Converting from Other Formats" above)

### Warning: "Low variance in feature X"

**Cause**: Feature is all 0 or all 1

**Solutions**:
1. Remove constant features (no information)
2. Check if this is expected (e.g., all strains resistant)
3. Verify data encoding is correct

### Warning: "Small sample size for chi-square"

**Cause**: Expected counts < 5 in contingency table

**Solutions**:
1. Script automatically uses Fisher's exact test (no action needed)
2. For very small samples, interpret with caution
3. Use bootstrap confidence intervals for effect sizes

## References

1. **K-Modes Clustering**: Huang, Z. (1998). Extensions to the k-means algorithm for clustering large data sets with categorical values.

2. **Multiple Correspondence Analysis**: Greenacre, M. (2007). Correspondence Analysis in Practice.

3. **Fisher's Exact Test**: Fisher, R.A. (1922). On the interpretation of χ² from contingency tables, and the calculation of P.

4. **Association Rules**: Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules.

5. **Log-Odds Ratios**: Agresti, A. (2002). Categorical Data Analysis.

## Summary

✅ **MKrep properly handles binary data** by:
- Validating data is strictly 0/1
- Using appropriate statistical tests for categorical data
- Treating both presence and absence as informative
- Applying methods designed for binary/categorical features
- Providing interpretable results for biological contexts

✅ **Both 0 and 1 are important** because:
- Absence of a gene is as informative as presence
- Susceptibility is as important as resistance
- Lack of virulence defines avirulent strains
- Pattern of presence/absence defines phenotypes

✅ **Trust the results** because:
- All calculations are mathematically correct for binary data
- Statistical tests are appropriate for categorical features
- Effect sizes are properly computed with pseudocounts
- Bootstrap methods preserve data structure
- Clustering methods are designed for categorical data

---

For questions about binary data handling, see:
- [INSTALLATION.md](INSTALLATION.md) - Setup and requirements
- [README.md](README.md) - General usage
- [EXCEL_REPORTS_README.md](EXCEL_REPORTS_README.md) - Report interpretation
