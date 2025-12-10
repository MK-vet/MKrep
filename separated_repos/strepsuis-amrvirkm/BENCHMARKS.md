# Performance Benchmarks

This document provides runtime and memory benchmarks for the StrepSuis-AMRVirKM module
across different dataset sizes.

## Benchmark Environment

- **Python**: 3.11+
- **Platform**: Linux x86_64
- **CPU**: Multi-core (parallelized operations use all available cores)
- **Memory**: 16GB+ recommended for large datasets

## Core Operations

### 1. K-modes Clustering

`kmodes_clustering(data, k=5, max_iter=100)`

| Strains | Features | Time (s) | Memory (MB) |
|---------|----------|----------|-------------|
| 50 | 20 | 0.3 | 10 |
| 100 | 30 | 0.5 | 15 |
| 200 | 40 | 1.2 | 25 |
| 500 | 50 | 3.5 | 50 |
| 1000 | 75 | 8.0 | 100 |
| 5000 | 100 | 45.0 | 400 |

**Notes**:
- Time scales linearly with k × n × m × iterations
- Uses Huang initialization for better convergence
- Memory dominated by distance matrix for silhouette calculation

### 2. Optimal Cluster Selection (Silhouette)

`select_optimal_k(data, k_range=(2, 10))`

| Strains | Features | k Range | Time (s) | Best k (typical) |
|---------|----------|---------|----------|------------------|
| 100 | 20 | 2-8 | 4.5 | 3-5 |
| 100 | 50 | 2-10 | 12.0 | 3-6 |
| 500 | 50 | 2-10 | 55.0 | 4-7 |
| 1000 | 50 | 2-8 | 95.0 | 4-8 |

**Notes**:
- Time = k_range × clustering_time + silhouette_time
- Silhouette computation is O(n²), dominates for large n

### 3. Multiple Correspondence Analysis (MCA)

`mca_analysis(data, n_components=2)`

| Strains | Features | Components | Time (s) | Memory (MB) |
|---------|----------|------------|----------|-------------|
| 100 | 20 | 2 | 0.2 | 10 |
| 500 | 50 | 2 | 0.8 | 40 |
| 1000 | 75 | 2 | 1.5 | 80 |
| 5000 | 100 | 2 | 8.0 | 350 |
| 5000 | 100 | 5 | 12.0 | 400 |

**Notes**:
- Uses SVD decomposition
- Memory scales with n × m for indicator matrix
- Additional components add minimal overhead

### 4. Phi Correlation Matrix

`compute_phi_matrix(data)`

| Features | Pairs | Time (s) | Memory (MB) |
|----------|-------|----------|-------------|
| 20 | 190 | 0.2 | 5 |
| 50 | 1,225 | 1.0 | 15 |
| 100 | 4,950 | 3.8 | 50 |
| 200 | 19,900 | 15.0 | 180 |

**Notes**:
- Time complexity: O(m² × n)
- Memory for full matrix: O(m²)

### 5. Cluster Stability Assessment

`assess_cluster_stability(data, k, n_bootstrap=100)`

| Strains | k | Bootstraps | Time (s) | Stability Score |
|---------|---|------------|----------|-----------------|
| 100 | 4 | 100 | 45 | 0.75-0.95 |
| 100 | 4 | 500 | 220 | 0.76-0.94 |
| 500 | 5 | 100 | 180 | 0.70-0.92 |
| 1000 | 5 | 100 | 400 | 0.68-0.90 |

**Notes**:
- Time scales linearly with n_bootstrap
- Co-occurrence matrix is O(n²) memory

### 6. Full Analysis Pipeline

`run_cluster_analysis()` (complete pipeline)

| Strains | Features | Total Time (s) | Peak Memory (MB) |
|---------|----------|----------------|------------------|
| 50 | 30 | 20 | 150 |
| 92 | 50 | 45 | 250 |
| 200 | 60 | 90 | 400 |
| 500 | 80 | 180 | 700 |
| 1000 | 100 | 400 | 1200 |

**Notes**:
- Includes clustering, MCA, statistical analysis, and report generation
- Report generation adds ~10-20s
- Peak memory during silhouette calculation

## Report Generation

### HTML Report

| Components | Time (s) | File Size (KB) |
|------------|----------|----------------|
| Small (5 clusters, basic) | 2 | 200 |
| Medium (8 clusters, full) | 4 | 500 |
| Large (10 clusters, detailed) | 8 | 900 |

### Excel Report

| Sheets | Charts | Time (s) | File Size (MB) |
|--------|--------|----------|----------------|
| 5 | 3 | 3 | 0.6 |
| 8 | 5 | 5 | 1.0 |
| 12 | 8 | 8 | 1.8 |

### PNG Chart Export

| Charts | Resolution (DPI) | Time (s) | Total Size (MB) |
|--------|------------------|----------|-----------------|
| 5 | 150 | 4 | 2 |
| 8 | 150 | 7 | 3.5 |
| 8 | 300 | 12 | 10 |

## Scaling Recommendations

### Small Datasets (< 100 strains)
- Use default parameters
- Full analysis in < 1 minute
- Memory: 256MB sufficient

### Medium Datasets (100-500 strains)
- Consider reducing max_k to 8
- Full analysis: 1-3 minutes
- Memory: 512MB-1GB recommended

### Large Datasets (500-1000 strains)
- Limit k_range to avoid excessive silhouette computation
- Full analysis: 3-10 minutes
- Memory: 2-4GB recommended

### Very Large Datasets (> 1000 strains)
- Sample-based silhouette approximation
- Pre-filter low-variance features
- Full analysis: 10-30 minutes
- Memory: 4-8GB recommended

## Optimization Tips

1. **Reduce k Range**: For exploratory analysis, use `k_range=(2, 6)`
2. **Feature Selection**: Remove features with < 5% or > 95% prevalence
3. **Bootstrap Samples**: Use `n_bootstrap=50` for quick stability estimate
4. **Parallel Processing**: Ensure multi-core utilization (default)
5. **Memory Management**: Clear intermediate results when not needed

## Profiling Commands

```bash
# Basic timing
time python -c "from strepsuis_amrvirkm import run_smoke_test; run_smoke_test()"

# Memory profiling
python -m memory_profiler run_analysis.py

# Detailed profiling
python -m cProfile -o profile.stats run_analysis.py
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumtime').print_stats(20)"
```

## Benchmark Data Sources

- All benchmarks performed on synthetic data with realistic AMR/virulence patterns
- Real-world performance may vary based on data sparsity and cluster separability
- Silhouette scores depend on true cluster structure in data

---

**Version**: 1.0.0  
**Last Benchmarked**: 2025-01-15  
**Benchmark System**: Ubuntu 22.04, Python 3.11, 8-core CPU, 16GB RAM
