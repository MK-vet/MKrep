# Performance Benchmarks

This document provides runtime and memory benchmarks for the StrepSuis-GenPhenNet module
across different dataset sizes.

## Benchmark Environment

- **Python**: 3.11+
- **Platform**: Linux x86_64
- **CPU**: Multi-core (parallelized operations use all available cores)
- **Memory**: 16GB+ recommended for large datasets

## Core Operations

### 1. Pairwise Association Testing

`compute_pairwise_associations(data, alpha=0.05)`

| Strains | Features | Pairs | Time (s) | Memory (MB) |
|---------|----------|-------|----------|-------------|
| 50 | 20 | 190 | 0.3 | 10 |
| 100 | 30 | 435 | 0.8 | 15 |
| 200 | 50 | 1,225 | 2.5 | 30 |
| 500 | 75 | 2,775 | 6.0 | 60 |
| 1000 | 100 | 4,950 | 12.0 | 100 |
| 5000 | 150 | 11,175 | 55.0 | 400 |

**Notes**:
- Uses chi-square or Fisher's exact based on expected cell counts
- Fisher's exact adds overhead for sparse tables
- Memory for storing all p-values: O(m²)

### 2. FDR Correction

`fdr_correction(p_values, alpha=0.05)`

| Tests | Time (s) | Memory (MB) |
|-------|----------|-------------|
| 100 | 0.001 | 0.1 |
| 1,000 | 0.005 | 0.5 |
| 10,000 | 0.03 | 3 |
| 100,000 | 0.3 | 30 |

**Notes**:
- Dominated by sorting: O(n log n)
- Negligible memory overhead

### 3. Network Construction

`build_association_network(data, alpha=0.05)`

| Features | Significant Edges | Time (s) | Memory (MB) |
|----------|-------------------|----------|-------------|
| 20 | 15-30 | 0.5 | 10 |
| 50 | 50-100 | 2.0 | 25 |
| 100 | 150-300 | 6.0 | 60 |
| 200 | 400-800 | 20.0 | 150 |

**Notes**:
- Time includes pairwise tests + FDR + network building
- NetworkX graph memory scales with edges

### 4. Community Detection (Louvain)

`detect_communities(network, resolution=1.0)`

| Nodes | Edges | Time (s) | Communities |
|-------|-------|----------|-------------|
| 20 | 30 | 0.01 | 2-4 |
| 50 | 100 | 0.03 | 3-6 |
| 100 | 300 | 0.08 | 4-8 |
| 200 | 800 | 0.25 | 5-12 |
| 500 | 2000 | 1.0 | 8-20 |

**Notes**:
- Fast for sparse networks
- Resolution parameter affects community count

### 5. Centrality Calculations

`compute_centralities(network)`

| Nodes | Edges | Metric | Time (s) |
|-------|-------|--------|----------|
| 50 | 100 | Degree | 0.001 |
| 50 | 100 | Betweenness | 0.05 |
| 50 | 100 | Eigenvector | 0.01 |
| 100 | 300 | All | 0.3 |
| 200 | 800 | All | 1.5 |
| 500 | 2000 | All | 10.0 |

**Notes**:
- Betweenness centrality is most expensive: O(n × e)
- Eigenvector uses power iteration

### 6. Information Theory Metrics

`compute_information_metrics(data)`

| Strains | Features | Pairs | Time (s) | Memory (MB) |
|---------|----------|-------|----------|-------------|
| 100 | 20 | 190 | 0.5 | 10 |
| 100 | 50 | 1,225 | 2.5 | 25 |
| 500 | 50 | 1,225 | 5.0 | 35 |
| 1000 | 100 | 4,950 | 18.0 | 80 |

**Notes**:
- Includes entropy, MI, and normalized MI
- O(n) per pair for probability estimation

### 7. Full Analysis Pipeline

`run_network_analysis()` (complete pipeline)

| Strains | Features | Total Time (s) | Peak Memory (MB) |
|---------|----------|----------------|------------------|
| 50 | 25 | 15 | 150 |
| 92 | 40 | 30 | 250 |
| 200 | 60 | 75 | 400 |
| 500 | 80 | 150 | 700 |
| 1000 | 100 | 350 | 1200 |

**Notes**:
- Includes association testing, network construction, analysis, visualization
- Report generation adds ~15-25s

## Report Generation

### HTML Report

| Components | Time (s) | File Size (KB) |
|------------|----------|----------------|
| Small (1 network, basic stats) | 3 | 250 |
| Medium (1 network, communities) | 5 | 450 |
| Large (multiple views) | 10 | 800 |

### Excel Report

| Sheets | Time (s) | File Size (MB) |
|--------|----------|----------------|
| 5 | 3 | 0.5 |
| 8 | 5 | 1.0 |
| 12 | 8 | 1.8 |

### Network Visualization

| Nodes | Edges | PNG (s) | Interactive HTML (s) |
|-------|-------|---------|----------------------|
| 30 | 50 | 2 | 3 |
| 75 | 150 | 4 | 6 |
| 150 | 400 | 8 | 12 |

## Scaling Recommendations

### Small Datasets (< 100 strains)
- Use default parameters
- Full analysis in < 30 seconds
- Memory: 256MB sufficient

### Medium Datasets (100-500 strains)
- Network visualization may require layout optimization
- Full analysis: 1-3 minutes
- Memory: 512MB-1GB recommended

### Large Datasets (500-1000 strains)
- Pre-filter features by prevalence
- Increase FDR stringency to reduce edge count
- Full analysis: 3-10 minutes
- Memory: 2-4GB recommended

### Very Large Datasets (> 1000 strains)
- Feature selection essential
- Consider hierarchical network construction
- Full analysis: 10-30 minutes
- Memory: 4-8GB recommended

## Optimization Tips

1. **Filter Features**: Remove features with < 5% or > 95% prevalence
2. **Stricter FDR**: Use alpha=0.01 for cleaner networks
3. **Skip Visualization**: For large networks, export data and visualize externally
4. **Parallel Tests**: Enable multi-core for pairwise calculations
5. **Prune Network**: Remove edges below phi threshold

## Profiling Commands

```bash
# Basic timing
time python -c "from strepsuis_genphennet import run_smoke_test; run_smoke_test()"

# Memory profiling
python -m memory_profiler run_analysis.py

# Detailed profiling
python -m cProfile -o profile.stats run_analysis.py
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumtime').print_stats(20)"
```

## Benchmark Data Sources

- All benchmarks performed on synthetic data with planted associations
- Real-world networks are typically sparser than worst-case
- Fisher's exact tests dominate for sparse binary data

---

**Version**: 1.0.0  
**Last Benchmarked**: 2025-01-15  
**Benchmark System**: Ubuntu 22.04, Python 3.11, 8-core CPU, 16GB RAM
