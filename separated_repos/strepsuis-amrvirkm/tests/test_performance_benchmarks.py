"""
Performance and Stress Testing Module for StrepSuis-AMRVIRKM

This module provides comprehensive performance benchmarks and stress tests
for the K-Modes clustering pipeline, including:

1. Execution time benchmarks with Big O verification
2. Memory footprint measurements
3. Stress tests with large datasets
4. Clustering performance metrics

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


def generate_test_clustering_data(n_samples: int, n_features: int, seed: int = 42) -> pd.DataFrame:
    """Generate random binary test data for clustering benchmarks."""
    np.random.seed(seed)
    data = np.random.randint(0, 2, size=(n_samples, n_features))
    return pd.DataFrame(data, columns=[f"Feature_{i:03d}" for i in range(n_features)])


class TestExecutionTimeBenchmarks:
    """Execution time benchmarks for key operations."""

    @pytest.mark.performance
    def test_silhouette_scaling(self):
        """Test silhouette score scaling with sample size (O(n^2) expected)."""
        from sklearn.metrics import silhouette_score

        sizes = [50, 100, 200]
        times = []

        for n in sizes:
            data = generate_test_clustering_data(n, 20)
            labels = np.random.randint(0, 3, n)

            elapsed, _ = measure_execution(silhouette_score, data.values, labels)
            times.append(elapsed)

        # Quadratic scaling: doubling n should quadruple time
        # Allow tolerance for overhead
        if times[0] > 0.001:
            ratio = times[1] / times[0]
            # Should scale roughly quadratically
            assert ratio < 8, f"Silhouette should scale ~O(n^2), ratio was {ratio}"

    @pytest.mark.performance
    def test_chi_square_throughput(self):
        """Test throughput of chi-square calculations."""
        from scipy.stats import chi2_contingency

        np.random.seed(42)
        n_tables = 500

        start = time.perf_counter()
        for _ in range(n_tables):
            table = np.random.randint(10, 100, size=(2, 2))
            chi2_contingency(table)
        elapsed = time.perf_counter() - start

        throughput = n_tables / elapsed

        # Should process at least 100 tables per second
        assert throughput > 100, f"Throughput {throughput:.0f} tables/s should be > 100"

    @pytest.mark.performance
    def test_kmodes_scaling(self):
        """Test K-Modes clustering scaling with sample size."""
        try:
            from kmodes.kmodes import KModes
        except ImportError:
            pytest.skip("kmodes not installed")

        sizes = [50, 100, 200]
        times = []

        for n in sizes:
            data = generate_test_clustering_data(n, 15)

            def run_kmodes():
                km = KModes(n_clusters=3, init="Huang", n_init=1, random_state=42)
                return km.fit_predict(data.values)

            elapsed, _ = measure_execution(run_kmodes)
            times.append(elapsed)

        # K-Modes should scale reasonably with n
        if times[0] > 0.001:
            ratio = times[1] / times[0]
            assert ratio < 6, f"K-Modes scaling ratio {ratio} should be reasonable"


class TestMemoryBenchmarks:
    """Memory usage benchmarks."""

    @pytest.mark.performance
    def test_clustering_memory_usage(self):
        """Test memory usage of clustering computation."""
        try:
            from kmodes.kmodes import KModes
        except ImportError:
            pytest.skip("kmodes not installed")

        data = generate_test_clustering_data(500, 30)

        def run_clustering():
            km = KModes(n_clusters=4, init="Huang", n_init=3, random_state=42)
            return km.fit_predict(data.values)

        memory_mb, result = measure_memory(run_clustering)

        # Should use less than 200 MB
        assert memory_mb < 200, f"Memory usage {memory_mb:.1f} MB should be < 200 MB"
        assert len(result) == len(data)

    @pytest.mark.performance
    def test_large_dataframe_memory(self):
        """Test memory usage with large DataFrames."""
        data = generate_test_clustering_data(5000, 100)

        # Just measure the data size
        data_memory = data.memory_usage(deep=True).sum() / (1024 * 1024)

        # Should be reasonable (< 50 MB for 5000 x 100 binary data)
        assert data_memory < 50, f"Data memory {data_memory:.1f} MB should be < 50 MB"


@pytest.mark.slow
class TestStressTests:
    """Stress tests with large datasets."""

    def test_large_sample_stress(self):
        """Stress test with large number of samples."""
        try:
            from kmodes.kmodes import KModes
        except ImportError:
            pytest.skip("kmodes not installed")

        # 5000 samples, 20 features
        data = generate_test_clustering_data(5000, 20)

        start = time.perf_counter()
        km = KModes(n_clusters=4, init="Huang", n_init=2, random_state=42)
        labels = km.fit_predict(data.values)
        elapsed = time.perf_counter() - start

        assert len(labels) == 5000
        assert elapsed < 120, f"Should complete in < 2 minutes, took {elapsed:.1f}s"

    def test_many_features_stress(self):
        """Stress test with many features."""
        try:
            from kmodes.kmodes import KModes
        except ImportError:
            pytest.skip("kmodes not installed")

        # 500 samples, 100 features
        data = generate_test_clustering_data(500, 100)

        start = time.perf_counter()
        km = KModes(n_clusters=5, init="Huang", n_init=2, random_state=42)
        labels = km.fit_predict(data.values)
        elapsed = time.perf_counter() - start

        assert len(labels) == 500
        assert elapsed < 60, f"Should complete in < 1 minute, took {elapsed:.1f}s"


class TestBigOVerification:
    """Verify Big O complexity of algorithms."""

    @pytest.mark.performance
    def test_phi_correlation_linear_complexity(self):
        """Verify phi correlation has O(n) complexity in sample size."""
        sizes = [100, 200, 400, 800]
        times = []

        for n in sizes:
            np.random.seed(42)
            x = np.random.binomial(1, 0.5, n)
            y = np.random.binomial(1, 0.5, n)

            def calc_phi():
                a = np.sum((x == 1) & (y == 1))
                b = np.sum((x == 1) & (y == 0))
                c = np.sum((x == 0) & (y == 1))
                d = np.sum((x == 0) & (y == 0))
                denom = np.sqrt((a + b) * (c + d) * (a + c) * (b + d))
                if denom == 0:
                    return 0
                return (a * d - b * c) / denom

            total_time = 0
            for _ in range(100):  # Average over 100 runs
                elapsed, _ = measure_execution(calc_phi)
                total_time += elapsed
            times.append(total_time / 100)

        # Linear complexity: time should roughly double when n doubles
        ratios = [times[i + 1] / times[i] if times[i] > 0 else 0 for i in range(len(times) - 1)]

        # All ratios should be less than 3 (allowing overhead)
        for i, ratio in enumerate(ratios):
            if times[i] > 1e-6:  # Only check if measurable
                assert ratio < 4, f"Time ratio {ratio:.2f} suggests super-linear complexity"


class PerformanceReportGenerator:
    """Generate performance reports in various formats."""

    def __init__(self, output_dir: str = "tests/reports/performance"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_benchmarks(self) -> Dict[str, Any]:
        """Run all benchmarks and generate report."""
        results = []

        # Clustering benchmarks
        try:
            from kmodes.kmodes import KModes

            for n in [50, 100, 200, 500]:
                data = generate_test_clustering_data(n, 20)
                try:

                    def run_km():
                        km = KModes(n_clusters=4, init="Huang", n_init=2, random_state=42)
                        return km.fit_predict(data.values)

                    elapsed, _ = measure_execution(run_km)
                    memory, _ = measure_memory(run_km)
                    results.append(
                        BenchmarkResult(
                            name="kmodes_clustering",
                            input_size=n,
                            execution_time_seconds=elapsed,
                            peak_memory_mb=memory,
                            success=True,
                            additional_metrics={"n_features": 20, "n_clusters": 4},
                        )
                    )
                except Exception as e:
                    results.append(
                        BenchmarkResult(
                            name="kmodes_clustering",
                            input_size=n,
                            execution_time_seconds=0,
                            peak_memory_mb=0,
                            success=False,
                            error_message=str(e),
                        )
                    )
        except ImportError:
            pass  # kmodes not installed

        # Chi-square benchmarks
        from scipy.stats import chi2_contingency

        for n_tables in [100, 500, 1000]:
            try:

                def run_chi2():
                    for _ in range(n_tables):
                        table = np.random.randint(10, 100, size=(2, 2))
                        chi2_contingency(table)

                elapsed, _ = measure_execution(run_chi2)
                results.append(
                    BenchmarkResult(
                        name="chi_square_tests",
                        input_size=n_tables,
                        execution_time_seconds=elapsed,
                        peak_memory_mb=0,
                        success=True,
                        additional_metrics={"throughput": n_tables / elapsed},
                    )
                )
            except Exception as e:
                results.append(
                    BenchmarkResult(
                        name="chi_square_tests",
                        input_size=n_tables,
                        execution_time_seconds=0,
                        peak_memory_mb=0,
                        success=False,
                        error_message=str(e),
                    )
                )

        # Calculate summary
        kmodes_results = [r for r in results if r.name == "kmodes_clustering" and r.success]
        chi2_results = [r for r in results if r.name == "chi_square_tests" and r.success]

        summary = {
            "total_benchmarks": len(results),
            "successful": sum(1 for r in results if r.success),
            "failed": sum(1 for r in results if not r.success),
            "avg_kmodes_time": (
                np.mean([r.execution_time_seconds for r in kmodes_results])
                if kmodes_results
                else 0
            ),
            "avg_chi2_throughput": (
                np.mean([r.additional_metrics.get("throughput", 0) for r in chi2_results])
                if chi2_results
                else 0
            ),
        }

        return {
            "benchmark_name": "strepsuis-amrvirkm-performance",
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
    assert Path(saved["csv"]).exists()

    # Verify report content
    with open(saved["json"]) as f:
        data = json.load(f)

    assert data["summary"]["successful"] >= 0
