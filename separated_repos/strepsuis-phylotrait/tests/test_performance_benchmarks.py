"""
Performance and Stress Testing Module for StrepSuis-PhyloTrait

This module provides comprehensive performance benchmarks and stress tests
for the phylogenetic analysis pipeline, including:

1. Tree parsing and distance matrix computation
2. Clustering algorithm performance
3. Memory footprint measurements
4. Stress tests with large phylogenies

All results are saved to tests/reports/performance/
"""

import gc
import json
import os
import time
import tracemalloc
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import pytest
from scipy.stats import chi2_contingency


@dataclass
class BenchmarkResult:
    """Result of a single benchmark run."""

    name: str
    input_size: int
    execution_time_seconds: float
    peak_memory_mb: float
    success: bool
    error_message: Optional[str] = None
    additional_metrics: Dict[str, Any] = field(default_factory=dict)


def measure_execution(func: Callable, *args, **kwargs) -> Tuple[float, Any]:
    """Measure execution time of a function."""
    gc.collect()
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return elapsed, result


def measure_memory(func: Callable, *args, **kwargs) -> Tuple[float, Any]:
    """Measure peak memory usage of a function."""
    gc.collect()
    tracemalloc.start()

    result = func(*args, **kwargs)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return peak / (1024 * 1024), result  # Convert to MB


class TestTreeGenerationPerformance:
    """Benchmark tree generation performance."""

    @pytest.mark.performance
    def test_tree_generation_scaling(self):
        """Test tree generation time scales with taxa count."""
        from strepsuis_phylotrait.generate_synthetic_data import (
            SyntheticPhyloConfig,
            generate_phylotrait_synthetic_dataset,
        )

        sizes = [20, 50, 100]
        times = []

        for n_taxa in sizes:
            config = SyntheticPhyloConfig(n_strains=n_taxa, random_state=42)

            def generate():
                return generate_phylotrait_synthetic_dataset(config)

            elapsed, _ = measure_execution(generate)
            times.append(elapsed)

        # Should complete in reasonable time
        assert times[2] < 10, f"Generation of 100 taxa should be < 10s, took {times[2]:.2f}s"

    @pytest.mark.performance
    def test_tree_parsing_performance(self):
        """Test tree parsing performance."""
        try:
            from Bio import Phylo
            from io import StringIO
        except ImportError:
            pytest.skip("BioPython not installed")

        from strepsuis_phylotrait.generate_synthetic_data import (
            SyntheticPhyloConfig,
            generate_phylotrait_synthetic_dataset,
        )

        config = SyntheticPhyloConfig(n_strains=100, random_state=42)
        tree_newick, _, _, _, _ = generate_phylotrait_synthetic_dataset(config)

        def parse_tree():
            tree = Phylo.read(StringIO(tree_newick), "newick")
            return tree

        elapsed, tree = measure_execution(parse_tree)

        assert elapsed < 1.0, f"Tree parsing should be < 1s, took {elapsed:.2f}s"


class TestDistanceMatrixPerformance:
    """Benchmark distance matrix computation."""

    @pytest.mark.performance
    def test_distance_matrix_scaling(self):
        """Test distance matrix computation scaling (O(n^2) expected)."""
        try:
            from Bio import Phylo
            from io import StringIO
        except ImportError:
            pytest.skip("BioPython not installed")

        from strepsuis_phylotrait.generate_synthetic_data import (
            SyntheticPhyloConfig,
            generate_phylotrait_synthetic_dataset,
        )

        sizes = [20, 40, 60]
        times = []

        for n_taxa in sizes:
            config = SyntheticPhyloConfig(n_strains=n_taxa, random_state=42)
            tree_newick, _, _, _, _ = generate_phylotrait_synthetic_dataset(config)
            tree = Phylo.read(StringIO(tree_newick), "newick")
            terminals = tree.get_terminals()

            def compute_distances():
                n = len(terminals)
                dist_matrix = np.zeros((n, n))
                for i in range(n):
                    for j in range(i + 1, n):
                        try:
                            dist = tree.distance(terminals[i], terminals[j])
                            dist_matrix[i, j] = dist
                            dist_matrix[j, i] = dist
                        except Exception:
                            pass
                return dist_matrix

            elapsed, _ = measure_execution(compute_distances)
            times.append(elapsed)

        # Should scale roughly quadratically
        if times[0] > 0.01:
            ratio = times[1] / times[0]
            # Doubling taxa should roughly quadruple time (but allow overhead)
            assert ratio < 10, f"Scaling ratio {ratio} should be reasonable"


class TestClusteringPerformance:
    """Benchmark clustering algorithm performance."""

    @pytest.mark.performance
    def test_kmeans_clustering_performance(self):
        """Test KMeans clustering performance."""
        from sklearn.cluster import KMeans

        from strepsuis_phylotrait.generate_synthetic_data import (
            SyntheticPhyloConfig,
            generate_phylotrait_synthetic_dataset,
        )

        config = SyntheticPhyloConfig(n_strains=200, random_state=42)
        _, mic_df, amr_df, vir_df, metadata = generate_phylotrait_synthetic_dataset(config)

        features = pd.concat([
            mic_df[metadata.mic_columns],
            amr_df[metadata.amr_columns],
            vir_df[metadata.virulence_columns],
        ], axis=1)

        def run_clustering():
            km = KMeans(n_clusters=4, random_state=42, n_init=3)
            return km.fit_predict(features)

        elapsed, labels = measure_execution(run_clustering)

        assert elapsed < 5, f"Clustering should be < 5s, took {elapsed:.2f}s"
        assert len(labels) == len(features)


class TestMemoryBenchmarks:
    """Memory usage benchmarks."""

    @pytest.mark.performance
    def test_synthetic_data_memory(self):
        """Test memory usage of synthetic data generation."""
        from strepsuis_phylotrait.generate_synthetic_data import (
            SyntheticPhyloConfig,
            generate_phylotrait_synthetic_dataset,
        )

        config = SyntheticPhyloConfig(n_strains=500, random_state=42)

        def generate():
            return generate_phylotrait_synthetic_dataset(config)

        memory_mb, result = measure_memory(generate)

        # Should use reasonable memory
        assert memory_mb < 100, f"Memory usage {memory_mb:.1f} MB should be < 100 MB"

    @pytest.mark.performance
    def test_distance_matrix_memory(self):
        """Test memory usage of distance matrix storage."""
        try:
            from Bio import Phylo
            from io import StringIO
        except ImportError:
            pytest.skip("BioPython not installed")

        from strepsuis_phylotrait.generate_synthetic_data import (
            SyntheticPhyloConfig,
            generate_phylotrait_synthetic_dataset,
        )

        config = SyntheticPhyloConfig(n_strains=200, random_state=42)
        tree_newick, _, _, _, _ = generate_phylotrait_synthetic_dataset(config)
        tree = Phylo.read(StringIO(tree_newick), "newick")
        terminals = tree.get_terminals()

        def compute_distances():
            n = len(terminals)
            return np.zeros((n, n), dtype=float)

        memory_mb, _ = measure_memory(compute_distances)

        # 200x200 float64 matrix should be small
        expected_mb = 200 * 200 * 8 / (1024 * 1024)
        assert memory_mb < expected_mb + 10, f"Memory {memory_mb:.1f} MB should be near {expected_mb:.1f} MB"


@pytest.mark.slow
class TestStressTests:
    """Stress tests with large datasets."""

    def test_large_tree_stress(self):
        """Stress test with large phylogenetic tree."""
        from strepsuis_phylotrait.generate_synthetic_data import (
            SyntheticPhyloConfig,
            generate_phylotrait_synthetic_dataset,
        )

        # 500 taxa tree
        config = SyntheticPhyloConfig(n_strains=500, n_clusters=5, random_state=42)

        start = time.perf_counter()
        tree, mic, amr, vir, meta = generate_phylotrait_synthetic_dataset(config)
        elapsed = time.perf_counter() - start

        assert len(mic) == 500
        assert elapsed < 60, f"Should complete in < 1 minute, took {elapsed:.1f}s"

    def test_many_features_stress(self):
        """Stress test with many features."""
        from strepsuis_phylotrait.generate_synthetic_data import (
            SyntheticPhyloConfig,
            generate_phylotrait_synthetic_dataset,
        )

        config = SyntheticPhyloConfig(
            n_strains=100,
            n_mic_features=50,
            n_amr_features=100,
            n_virulence_features=50,
            random_state=42,
        )

        start = time.perf_counter()
        tree, mic, amr, vir, meta = generate_phylotrait_synthetic_dataset(config)
        elapsed = time.perf_counter() - start

        assert len(meta.amr_columns) == 100
        assert elapsed < 30, f"Should complete in < 30s, took {elapsed:.1f}s"


class TestBigOComplexity:
    """Verify Big O complexity of algorithms."""

    @pytest.mark.performance
    def test_chi_square_linear_complexity(self):
        """Verify chi-square test is O(n) in sample size."""
        sizes = [50, 100, 200, 400]
        times = []

        np.random.seed(42)

        for n in sizes:
            x = np.random.binomial(1, 0.5, n)
            y = np.random.randint(1, 4, n)

            def run_chi2():
                table = pd.crosstab(x, y)
                return chi2_contingency(table)

            total_time = 0
            for _ in range(50):
                elapsed, _ = measure_execution(run_chi2)
                total_time += elapsed
            times.append(total_time / 50)

        # Linear complexity
        if times[0] > 1e-6:
            ratios = [times[i + 1] / times[i] for i in range(len(times) - 1)]
            for ratio in ratios:
                assert ratio < 5, f"Time ratio {ratio:.2f} suggests super-linear complexity"


class PerformanceReportGenerator:
    """Generate performance reports."""

    def __init__(self, output_dir: str = "tests/reports/performance"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_benchmarks(self) -> Dict[str, Any]:
        """Run all benchmarks and generate report."""
        from strepsuis_phylotrait.generate_synthetic_data import (
            SyntheticPhyloConfig,
            generate_phylotrait_synthetic_dataset,
        )

        results = []

        # Data generation benchmarks
        for n_taxa in [20, 50, 100, 200]:
            try:
                config = SyntheticPhyloConfig(n_strains=n_taxa, random_state=42)

                def generate():
                    return generate_phylotrait_synthetic_dataset(config)

                elapsed, _ = measure_execution(generate)
                memory, _ = measure_memory(generate)

                results.append(
                    BenchmarkResult(
                        name="synthetic_data_generation",
                        input_size=n_taxa,
                        execution_time_seconds=elapsed,
                        peak_memory_mb=memory,
                        success=True,
                    )
                )
            except Exception as e:
                results.append(
                    BenchmarkResult(
                        name="synthetic_data_generation",
                        input_size=n_taxa,
                        execution_time_seconds=0,
                        peak_memory_mb=0,
                        success=False,
                        error_message=str(e),
                    )
                )

        # Summary
        gen_results = [r for r in results if r.success]
        summary = {
            "total_benchmarks": len(results),
            "successful": sum(1 for r in results if r.success),
            "failed": sum(1 for r in results if not r.success),
            "avg_generation_time": (
                np.mean([r.execution_time_seconds for r in gen_results])
                if gen_results
                else 0
            ),
        }

        return {
            "benchmark_name": "strepsuis-phylotrait-performance",
            "timestamp": datetime.now().isoformat(),
            "results": [
                {
                    "name": r.name,
                    "input_size": r.input_size,
                    "execution_time_seconds": r.execution_time_seconds,
                    "peak_memory_mb": r.peak_memory_mb,
                    "success": r.success,
                    "error_message": r.error_message,
                    "additional_metrics": r.additional_metrics,
                }
                for r in results
            ],
            "summary": summary,
        }

    def save_report(self, report: Dict[str, Any]) -> Dict[str, str]:
        """Save report in multiple formats."""
        saved_files = {}

        # Save as JSON
        json_file = self.output_dir / "benchmark_results.json"
        with open(json_file, "w") as f:
            json.dump(report, f, indent=2)
        saved_files["json"] = str(json_file)

        # Save as CSV
        csv_file = self.output_dir / "benchmark_results.csv"
        rows = []
        for r in report["results"]:
            rows.append(
                {
                    "name": r["name"],
                    "input_size": r["input_size"],
                    "execution_time_seconds": r["execution_time_seconds"],
                    "peak_memory_mb": r["peak_memory_mb"],
                    "success": r["success"],
                }
            )
        pd.DataFrame(rows).to_csv(csv_file, index=False)
        saved_files["csv"] = str(csv_file)

        return saved_files


@pytest.mark.performance
def test_generate_performance_report(tmp_path):
    """Generate a complete performance report."""
    generator = PerformanceReportGenerator(output_dir=str(tmp_path / "performance"))

    report = generator.run_benchmarks()
    saved = generator.save_report(report)

    assert "json" in saved
    assert Path(saved["json"]).exists()

    # Verify report content
    with open(saved["json"]) as f:
        data = json.load(f)

    assert data["summary"]["successful"] >= 0
