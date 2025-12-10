# Algorithms Documentation

This document provides detailed algorithmic descriptions and Big-O complexity analysis
for the key computational methods in the StrepSuis-AMRVirKM module.

## Overview

All algorithms in the StrepSuis-AMRVirKM module are designed with:
- **Reproducibility**: Fixed random seeds for deterministic results
- **Numerical stability**: Careful handling of edge cases and numerical precision
- **Scalability**: Efficient implementations suitable for datasets up to 10,000+ strains

## 1. K-modes Clustering

### Purpose
Cluster categorical data (e.g., binary resistance profiles) where traditional k-means is not appropriate.

### Algorithm
```
FUNCTION kmodes_clustering(data, k, max_iter=100):
    INPUT:
        data: Binary DataFrame with n samples and m features
        k: Number of clusters
        max_iter: Maximum iterations
    
    OUTPUT:
        cluster_labels: Array of n cluster assignments
        centroids: Array of k mode vectors
    
    PROCEDURE:
        # Initialize centroids randomly from data points
        centroids = random_sample(data, k)
        
        FOR iter = 1 TO max_iter:
            # Assignment step: assign each point to nearest centroid
            FOR i = 1 TO n:
                distances = [hamming_distance(data[i], centroids[j]) for j in range(k)]
                cluster_labels[i] = argmin(distances)
            
            # Update step: compute new centroids as mode of each cluster
            old_centroids = copy(centroids)
            FOR j = 1 TO k:
                cluster_points = data[cluster_labels == j]
                centroids[j] = mode(cluster_points)  # Most frequent value per feature
            
            # Check convergence
            IF centroids == old_centroids:
                BREAK
        
        RETURN (cluster_labels, centroids)
```

### Hamming Distance
```
FUNCTION hamming_distance(a, b):
    # Count positions where values differ
    RETURN sum(a[i] != b[i] for i in range(len(a)))
```

### Complexity
- Time: O(k × n × m × max_iter)
- Space: O(k × m + n)

## 2. Optimal Cluster Selection (Silhouette-based)

### Purpose
Automatically determine the optimal number of clusters using silhouette analysis.

### Algorithm
```
FUNCTION select_optimal_k(data, k_range=(2, 10)):
    INPUT:
        data: Binary DataFrame
        k_range: Range of cluster numbers to test
    
    OUTPUT:
        best_k: Optimal number of clusters
    
    PROCEDURE:
        best_k = 2
        best_score = -1
        
        FOR k in k_range:
            labels = kmodes_clustering(data, k)
            score = silhouette_score(data, labels, metric='hamming')
            
            IF score > best_score:
                best_score = score
                best_k = k
        
        RETURN best_k
```

### Silhouette Coefficient
```
For each sample i:
    a(i) = mean distance to other points in same cluster
    b(i) = mean distance to points in nearest other cluster
    s(i) = (b(i) - a(i)) / max(a(i), b(i))
    
Silhouette score = mean(s(i)) for all i
```

### Complexity
- Time: O(k_max × (n × m × max_iter + n²))
- Space: O(n²) for distance matrix (if pre-computed)

## 3. Multiple Correspondence Analysis (MCA)

### Purpose
Dimensionality reduction for categorical data, analogous to PCA for continuous data.

### Algorithm
```
FUNCTION multiple_correspondence_analysis(data, n_components=2):
    INPUT:
        data: Binary DataFrame with n samples and m features
        n_components: Number of components to retain
    
    OUTPUT:
        row_coords: n × n_components matrix of sample coordinates
        col_coords: m × n_components matrix of feature coordinates
    
    PROCEDURE:
        # Create indicator matrix (already binary for our data)
        X = data.values
        n, m = X.shape
        
        # Row and column masses
        row_sums = X.sum(axis=1)
        col_sums = X.sum(axis=0)
        total = X.sum()
        
        # Standardized residuals
        expected = outer(row_sums, col_sums) / total
        residuals = (X - expected) / sqrt(expected)
        
        # SVD decomposition
        U, S, Vt = svd(residuals)
        
        # Extract coordinates
        row_coords = U[:, :n_components] * S[:n_components]
        col_coords = Vt[:n_components, :].T * S[:n_components]
        
        # Inertia (variance explained)
        eigenvalues = S ** 2
        inertia = eigenvalues / eigenvalues.sum()
        
        RETURN (row_coords, col_coords, inertia)
```

### Complexity
- Time: O(min(n, m) × n × m) for SVD
- Space: O(n × m + n × k + m × k) where k = n_components

## 4. Phi Correlation Matrix

### Purpose
Compute pairwise phi coefficients between all binary features for cluster characterization.

### Algorithm
```
FUNCTION compute_phi_matrix(data):
    INPUT:
        data: Binary DataFrame with m features
    
    OUTPUT:
        phi_matrix: m × m correlation matrix
    
    PROCEDURE:
        m = number of features
        phi_matrix = zeros(m, m)
        
        FOR i = 0 TO m-1:
            FOR j = i TO m-1:
                IF i == j:
                    phi_matrix[i, j] = 1.0
                ELSE:
                    # 2×2 contingency table
                    a = sum(data[:, i] == 1 AND data[:, j] == 1)
                    b = sum(data[:, i] == 1 AND data[:, j] == 0)
                    c = sum(data[:, i] == 0 AND data[:, j] == 1)
                    d = sum(data[:, i] == 0 AND data[:, j] == 0)
                    
                    # Phi coefficient
                    num = a * d - b * c
                    den = sqrt((a+b) * (c+d) * (a+c) * (b+d))
                    
                    IF den > 0:
                        phi = num / den
                    ELSE:
                        phi = 0.0
                    
                    phi_matrix[i, j] = phi
                    phi_matrix[j, i] = phi
        
        RETURN phi_matrix
```

### Complexity
- Time: O(m² × n)
- Space: O(m²)

## 5. Log-Odds Ratio Analysis

### Purpose
Quantify effect sizes for feature enrichment in clusters.

### Algorithm
```
FUNCTION compute_log_odds_ratio(cluster_data, background_data):
    INPUT:
        cluster_data: Binary data for samples in cluster
        background_data: Binary data for all samples
    
    OUTPUT:
        log_odds: Array of log-odds ratios per feature
        ci_lower: Lower confidence bounds
        ci_upper: Upper confidence bounds
    
    PROCEDURE:
        FOR each feature f:
            # Cluster counts
            a = count(cluster_data[f] == 1)
            b = count(cluster_data[f] == 0)
            
            # Background counts (excluding cluster)
            c = count(background[f] == 1)
            d = count(background[f] == 0)
            
            # Add 0.5 for continuity correction
            a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5
            
            # Log-odds ratio
            log_odds[f] = log((a * d) / (b * c))
            
            # Standard error
            se = sqrt(1/a + 1/b + 1/c + 1/d)
            
            # 95% CI
            z = 1.96
            ci_lower[f] = log_odds[f] - z * se
            ci_upper[f] = log_odds[f] + z * se
        
        RETURN (log_odds, ci_lower, ci_upper)
```

### Complexity
- Time: O(m × n)
- Space: O(m)

## 6. Cluster Stability Assessment

### Purpose
Evaluate cluster stability using bootstrap resampling.

### Algorithm
```
FUNCTION assess_cluster_stability(data, k, n_bootstrap=100):
    INPUT:
        data: Binary DataFrame
        k: Number of clusters
        n_bootstrap: Number of bootstrap samples
    
    OUTPUT:
        stability_scores: Array of stability scores per cluster
    
    PROCEDURE:
        original_labels = kmodes_clustering(data, k)
        
        co_occurrence = zeros(n, n)  # How often pairs cluster together
        
        FOR b = 1 TO n_bootstrap:
            # Bootstrap sample
            indices = random_choice(range(n), size=n, replace=True)
            boot_data = data[indices]
            
            # Cluster bootstrap sample
            boot_labels = kmodes_clustering(boot_data, k)
            
            # Match clusters using Hungarian algorithm
            matched_labels = match_clusters(boot_labels, original_labels[indices])
            
            # Update co-occurrence
            FOR i, j in combinations(range(len(indices)), 2):
                IF matched_labels[i] == matched_labels[j]:
                    co_occurrence[indices[i], indices[j]] += 1
        
        # Normalize
        co_occurrence /= n_bootstrap
        
        # Calculate per-cluster stability
        FOR cluster c:
            members = where(original_labels == c)
            within_cluster = co_occurrence[members][:, members]
            stability_scores[c] = mean(within_cluster)
        
        RETURN stability_scores
```

### Complexity
- Time: O(n_bootstrap × (k × n × m + n²))
- Space: O(n²) for co-occurrence matrix

## 7. Discriminant Features Identification

### Purpose
Identify features that best discriminate between clusters.

### Algorithm
```
FUNCTION identify_discriminant_features(data, labels, alpha=0.05):
    INPUT:
        data: Binary DataFrame
        labels: Cluster assignments
        alpha: Significance threshold
    
    OUTPUT:
        discriminant_features: List of significant features per cluster
    
    PROCEDURE:
        k = number of unique clusters
        results = empty list
        
        FOR each feature f:
            # Chi-square test for independence
            contingency = crosstab(data[f], labels)
            chi2, p_value = chi2_contingency(contingency)
            
            IF p_value < alpha:
                # Compute effect size (Cramer's V)
                n = len(data)
                min_dim = min(2, k) - 1
                cramer_v = sqrt(chi2 / (n * min_dim))
                
                # Determine which clusters are enriched
                FOR cluster c:
                    prevalence_c = mean(data[labels == c][f])
                    prevalence_other = mean(data[labels != c][f])
                    
                    IF prevalence_c > prevalence_other:
                        results.append({
                            feature: f,
                            cluster: c,
                            effect_size: cramer_v,
                            p_value: p_value
                        })
        
        # FDR correction
        corrected_results = fdr_correction(results, alpha)
        
        RETURN corrected_results
```

### Complexity
- Time: O(m × k × n)
- Space: O(m × k)

---

## Scalability Considerations

### Typical Performance

| Operation | 100 strains | 500 strains | 1000 strains |
|-----------|-------------|-------------|--------------|
| K-modes clustering (k=5) | ~0.5s | ~2s | ~5s |
| Optimal k selection (k=2-10) | ~3s | ~15s | ~40s |
| MCA (2 components) | ~0.2s | ~0.5s | ~1s |
| Phi matrix (50 features) | ~0.5s | ~1s | ~2s |
| Full pipeline | ~30s | ~90s | ~180s |

### Memory Optimization

For large datasets (>1000 strains):
1. Use sparse matrix representation for binary data
2. Chunk cluster stability assessment
3. Parallel processing for bootstrap iterations

---

## References

1. Huang, Z. (1998). Extensions to the k-means algorithm for clustering large data sets with categorical values. *Data Mining and Knowledge Discovery*, 2(3), 283-304.
2. Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. *Journal of Computational and Applied Mathematics*, 20, 53-65.
3. Greenacre, M. (2017). *Correspondence Analysis in Practice*. Chapman & Hall/CRC.
4. Yule, G. U. (1912). On the methods of measuring association between two attributes. *JRSS*, 75(6), 579-652.

---

**Version**: 1.0.0  
**Last Updated**: 2025-01-15
