# Synthetic Data Generation Methodology for K-Modes Clustering

## Overview

This document describes the statistical methodology used to generate synthetic
data for validating K-Modes clustering analysis.

## Generation Parameters

- **Number of strains**: 100
- **Number of clusters**: 4
- **MIC features**: 13
- **AMR gene features**: 25
- **Virulence factor features**: 15
- **Cluster separation strength**: 0.70
- **Noise level**: 0.05
- **Random seed**: 42

## Statistical Methods Used

### 1. Cluster Centroid Generation

Each cluster is defined by a characteristic pattern of feature prevalences.
Features are assigned high or low prevalences based on cluster identity:

- High prevalence features: p = base + (1 - base) × separation
- Low prevalence features: p = base × (1 - separation × 0.5)
- Base prevalence: 0.3

### 2. Binary Data Generation

For each sample, binary features are generated using Bernoulli trials:
- P(feature=1) = cluster_prevalence[feature]
- Each trial is independent

### 3. Noise Addition

A small proportion (5.0%) of values are randomly
flipped to simulate measurement error and biological variability.

## Ground Truth

### Cluster Distribution
- Cluster 1: 25 strains (25.0%)
- Cluster 2: 25 strains (25.0%)
- Cluster 3: 25 strains (25.0%)
- Cluster 4: 25 strains (25.0%)

## Expected Clustering Performance

- Expected silhouette score range: 0.30 - 0.80
- Cluster recovery should be >70% accurate

## References

1. Huang, Z. (1998). Extensions to the k-Means Algorithm for Clustering Large Data Sets
   with Categorical Values. Data Mining and Knowledge Discovery.
2. Kaufman, L., & Rousseeuw, P. J. (1990). Finding Groups in Data. Wiley.

## Generation Timestamp

2025-12-10T13:58:38.737448

---
*This data was generated for validation and testing purposes only.*
