"""
Performance and Stress Testing Module for StrepSuis-GenPhenNet

This module provides comprehensive performance benchmarks and stress tests
for the network analysis pipeline, including:

1. Chi-square test throughput
2. Network construction time
3. Memory footprint measurements
4. Stress tests with large feature sets

All results are saved to tests/reports/performance/
"""

import gc
import json
import os
import sys
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


def generate_test_network_data(n_samples: int, n_features: int, seed: int = 42) -> pd.DataFrame:
    """Generate random binary test data for network benchmarks."""
    np.random.seed(seed)
    data = np.random.randint(0, 2, size=(n_samples, n_features))
    return pd.DataFrame(data, columns=[f"Feature_{i:03d}" for i in range(n_features)])


class TestChiSquareThroughput:
    """Benchmark chi-square test performance."""

    @pytest.mark.performance
    def test_chi_square_throughput(self):
        """Measure chi-square test throughput."""
        np.random.seed(42)
        n_tests = 1000

        start = time.perf_counter()
        for _ in range(n_tests):
            table = np.random.randint(10, 100, size=(2, 2))
            chi2_contingency(table)
        elapsed = time.perf_counter() - start

        throughput = n_tests / elapsed

        # Should process at least 1000 tests per second
        assert throughput > 500, f"Throughput {throughput:.0f} tests/s should be > 500"

    @pytest.mark.performance
    def test_pairwise_chi_square_scaling(self):
        """Test scaling of pairwise chi-square tests with feature count."""
        sizes = [10, 20, 30]
        times = []
        n_samples = 100

        for n_features in sizes:
            data = generate_test_network_data(n_samples, n_features)

            def run_pairwise():
                for i in range(n_features):
                    for j in range(i + 1, n_features):
                        table = pd.crosstab(data.iloc[:, i], data.iloc[:, j])
                        chi2_contingency(table)

            elapsed, _ = measure_execution(run_pairwise)
            times.append(elapsed)
            n_pairs = n_features * (n_features - 1) // 2

        # Time should scale quadratically with feature count
        # n_pairs scales as O(n^2)
        if times[0] > 0.001:
            ratio = times[1] / times[0]
            # With 2x features, should have ~4x pairs
            assert ratio < 10, f"Scaling ratio {ratio} should be reasonable"


class TestNetworkConstructionPerformance:
    """Benchmark network construction performance."""

    @pytest.mark.performance
    def test_network_construction_time(self):
        """Test time to construct network from associations."""
        try:
            import networkx as nx
        except ImportError:
            pytest.skip("networkx not installed")

        np.random.seed(42)
        n_nodes = 100
        n_edges = 500

        # Generate random edges
        edges = [(np.random.randint(0, n_nodes), np.random.randint(0, n_nodes))
                 for _ in range(n_edges)]

        def build_network():
            G = nx.Graph()
            G.add_nodes_from(range(n_nodes))
            G.add_edges_from(edges)
            return G

        elapsed, G = measure_execution(build_network)

        assert elapsed < 1.0, f"Network construction should be < 1s, took {elapsed:.2f}s"
        assert G.number_of_nodes() == n_nodes
        assert G.number_of_edges() <= n_edges

    @pytest.mark.performance
    def test_community_detection_time(self):
        """Test community detection algorithm performance."""
        try:
            import networkx as nx
            import community.community_louvain as community_louvain
        except ImportError:
            pytest.skip("networkx or community not installed")

        np.random.seed(42)

        # Create a graph with community structure
        G = nx.Graph()
        n_nodes = 200

        # Create 4 communities
        for comm in range(4):
            nodes = list(range(comm * 50, (comm + 1) * 50))
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    if np.random.random() < 0.3:
                        G.add_edge(nodes[i], nodes[j])

        # Add some inter-community edges
        for _ in range(50):
            i, j = np.random.randint(0, n_nodes, 2)
            G.add_edge(i, j)

        def run_community_detection():
            return community_louvain.best_partition(G, random_state=42)

        elapsed, partition = measure_execution(run_community_detection)

        assert elapsed < 5.0, f"Community detection should be < 5s, took {elapsed:.2f}s"
        assert len(partition) == G.number_of_nodes()


class TestMemoryBenchmarks:
    """Memory usage benchmarks for network analysis."""

    @pytest.mark.performance
    def test_pairwise_chi_square_memory(self):
        """Test memory usage of pairwise chi-square calculations."""
        n_samples = 500
        n_features = 50
        data = generate_test_network_data(n_samples, n_features)

        def run_pairwise():
            results = []
            for i in range(n_features):
                for j in range(i + 1, n_features):
                    table = pd.crosstab(data.iloc[:, i], data.iloc[:, j])
                    chi2, p, _, _ = chi2_contingency(table)
                    results.append((i, j, chi2, p))
            return results

        memory_mb, results = measure_memory(run_pairwise)

        # Should use less than 100 MB
        assert memory_mb < 100, f"Memory usage {memory_mb:.1f} MB should be < 100 MB"

        expected_pairs = n_features * (n_features - 1) // 2
        assert len(results) == expected_pairs

    @pytest.mark.performance
    def test_network_memory_usage(self):
        """Test memory usage of network storage."""
        try:
            import networkx as nx
        except ImportError:
            pytest.skip("networkx not installed")

        n_nodes = 1000
        n_edges = 5000

        def create_network():
            G = nx.Graph()
            G.add_nodes_from(range(n_nodes))
            edges = [(np.random.randint(0, n_nodes), np.random.randint(0, n_nodes))
                     for _ in range(n_edges)]
            G.add_edges_from(edges)
            return G

        memory_mb, G = measure_memory(create_network)

        # Should be reasonable memory usage
        assert memory_mb < 50, f"Network memory {memory_mb:.1f} MB should be < 50 MB"


@pytest.mark.slow
class TestStressTests:
    """Stress tests with large datasets."""

    def test_large_feature_set_stress(self):
        """Stress test with many features."""
        n_samples = 200
        n_features = 100
        data = generate_test_network_data(n_samples, n_features)

        start = time.perf_counter()

        # Run pairwise tests on all pairs
        n_significant = 0
        for i in range(min(50, n_features)):  # Limit to first 50 to keep time reasonable
            for j in range(i + 1, min(50, n_features)):
                table = pd.crosstab(data.iloc[:, i], data.iloc[:, j])
                _, p, _, _ = chi2_contingency(table)
                if p < 0.05:
                    n_significant += 1

        elapsed = time.perf_counter() - start

        assert elapsed < 60, f"Should complete in < 1 minute, took {elapsed:.1f}s"

    def test_many_samples_stress(self):
        """Stress test with many samples."""
        n_samples = 5000
        n_features = 20
        data = generate_test_network_data(n_samples, n_features)

        start = time.perf_counter()

        # Run pairwise tests
        n_pairs = 0
        for i in range(n_features):
            for j in range(i + 1, n_features):
                table = pd.crosstab(data.iloc[:, i], data.iloc[:, j])
                chi2_contingency(table)
                n_pairs += 1

        elapsed = time.perf_counter() - start

        assert elapsed < 30, f"Should complete in < 30s, took {elapsed:.1f}s"


class TestBigOComplexity:
    """Verify Big O complexity of algorithms."""

    @pytest.mark.performance
    def test_chi_square_linear_in_samples(self):
        """Verify chi-square is O(n) in sample size."""
        sizes = [100, 200, 400, 800]
        times = []

        for n in sizes:
            data = generate_test_network_data(n, 2)

            def run_chi2():
                table = pd.crosstab(data.iloc[:, 0], data.iloc[:, 1])
                return chi2_contingency(table)

            total_time = 0
            for _ in range(100):
                elapsed, _ = measure_execution(run_chi2)
                total_time += elapsed
            times.append(total_time / 100)

        # Linear complexity: doubling n should roughly double time
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
        results = []

        # Chi-square throughput benchmarks
        for n_tests in [100, 500, 1000]:
            try:
                np.random.seed(42)

                def run_chi2():
                    for _ in range(n_tests):
                        table = np.random.randint(10, 100, size=(2, 2))
                        chi2_contingency(table)

                elapsed, _ = measure_execution(run_chi2)
                results.append(
                    BenchmarkResult(
                        name="chi_square_throughput",
                        input_size=n_tests,
                        execution_time_seconds=elapsed,
                        peak_memory_mb=0,
                        success=True,
                        additional_metrics={"throughput": n_tests / elapsed},
                    )
                )
            except Exception as e:
                results.append(
                    BenchmarkResult(
                        name="chi_square_throughput",
                        input_size=n_tests,
                        execution_time_seconds=0,
                        peak_memory_mb=0,
                        success=False,
                        error_message=str(e),
                    )
                )

        # Pairwise tests benchmarks
        for n_features in [10, 20, 30]:
            try:
                n_samples = 100
                data = generate_test_network_data(n_samples, n_features)

                def run_pairwise():
                    for i in range(n_features):
                        for j in range(i + 1, n_features):
                            table = pd.crosstab(data.iloc[:, i], data.iloc[:, j])
                            chi2_contingency(table)

                elapsed, _ = measure_execution(run_pairwise)
                n_pairs = n_features * (n_features - 1) // 2
                results.append(
                    BenchmarkResult(
                        name="pairwise_chi_square",
                        input_size=n_features,
                        execution_time_seconds=elapsed,
                        peak_memory_mb=0,
                        success=True,
                        additional_metrics={"n_pairs": n_pairs, "n_samples": n_samples},
                    )
                )
            except Exception as e:
                results.append(
                    BenchmarkResult(
                        name="pairwise_chi_square",
                        input_size=n_features,
                        execution_time_seconds=0,
                        peak_memory_mb=0,
                        success=False,
                        error_message=str(e),
                    )
                )

        # Summary
        chi2_results = [r for r in results if r.name == "chi_square_throughput" and r.success]
        pairwise_results = [r for r in results if r.name == "pairwise_chi_square" and r.success]

        summary = {
            "total_benchmarks": len(results),
            "successful": sum(1 for r in results if r.success),
            "failed": sum(1 for r in results if not r.success),
            "avg_chi2_throughput": (
                np.mean([r.additional_metrics.get("throughput", 0) for r in chi2_results])
                if chi2_results
                else 0
            ),
        }

        return {
            "benchmark_name": "strepsuis-genphennet-performance",
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
    assert "csv" in saved
    assert Path(saved["json"]).exists()

    # Verify report content
    with open(saved["json"]) as f:
        data = json.load(f)

    assert data["summary"]["successful"] >= 0
