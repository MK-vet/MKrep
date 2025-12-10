"""
Performance and Stress Testing Module for StrepSuis-MDR

This module provides comprehensive performance benchmarks and stress tests
for the MDR analysis pipeline, including:

1. Execution time benchmarks with Big O verification
2. Memory footprint measurements  
3. Stress tests with large datasets
4. Performance graphs and metrics generation

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


@dataclass
class PerformanceReport:
    """Comprehensive performance report."""
    
    benchmark_name: str
    timestamp: str
    results: List[BenchmarkResult]
    summary: Dict[str, Any]


def measure_execution(func: Callable, *args, **kwargs) -> Tuple[float, Any]:
    """
    Measure execution time of a function.
    
    Parameters:
        func: Function to measure
        *args, **kwargs: Arguments to pass to function
        
    Returns:
        Tuple of (elapsed_time_seconds, function_result)
    """
    gc.collect()
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return elapsed, result


def measure_memory(func: Callable, *args, **kwargs) -> Tuple[float, Any]:
    """
    Measure peak memory usage of a function.
    
    Parameters:
        func: Function to measure
        *args, **kwargs: Arguments to pass to function
        
    Returns:
        Tuple of (peak_memory_mb, function_result)
    """
    gc.collect()
    tracemalloc.start()
    
    result = func(*args, **kwargs)
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return peak / (1024 * 1024), result  # Convert to MB


def generate_test_data(n_samples: int, n_features: int, seed: int = 42) -> pd.DataFrame:
    """
    Generate random binary test data for benchmarking.
    
    Parameters:
        n_samples: Number of rows
        n_features: Number of columns
        seed: Random seed
        
    Returns:
        DataFrame with binary data
    """
    np.random.seed(seed)
    data = np.random.randint(0, 2, size=(n_samples, n_features))
    return pd.DataFrame(
        data,
        columns=[f"Feature_{i:03d}" for i in range(n_features)]
    )


class TestExecutionTimeBenchmarks:
    """Execution time benchmarks for key operations."""

    @pytest.mark.performance
    def test_bootstrap_ci_scaling(self):
        """Test bootstrap CI scaling with sample size (O(n) expected)."""
        from strepsuis_mdr.mdr_analysis_core import compute_bootstrap_ci
        
        sizes = [50, 100, 200, 400]
        times = []
        
        for n in sizes:
            data = generate_test_data(n, 5)
            elapsed, _ = measure_execution(
                compute_bootstrap_ci, data, n_iter=500, confidence_level=0.95
            )
            times.append(elapsed)
        
        # Check that time scales approximately linearly with n
        # (doubling n should approximately double time)
        ratio_1 = times[1] / times[0] if times[0] > 0 else float('inf')
        ratio_2 = times[2] / times[1] if times[1] > 0 else float('inf')
        
        # Allow some tolerance for overhead
        assert ratio_1 < 4, f"Bootstrap should scale linearly, ratio was {ratio_1}"
        assert ratio_2 < 4, f"Bootstrap should scale linearly, ratio was {ratio_2}"

    @pytest.mark.performance
    def test_pairwise_cooccurrence_scaling(self):
        """Test pairwise co-occurrence scaling (O(n * k^2) expected)."""
        from strepsuis_mdr.mdr_analysis_core import pairwise_cooccurrence
        
        # Fix n, vary k (number of features)
        n = 100
        feature_counts = [5, 10, 15]
        times = []
        
        for k in feature_counts:
            data = generate_test_data(n, k)
            elapsed, _ = measure_execution(pairwise_cooccurrence, data, alpha=0.05)
            times.append(elapsed)
        
        # k^2 scaling: 4x features should take ~16x time
        # But allow tolerance for overhead and FDR correction
        assert times[2] < times[0] * 50, "Co-occurrence scaling is reasonable"

    @pytest.mark.performance
    def test_contingency_table_throughput(self):
        """Test throughput of contingency table calculations."""
        from strepsuis_mdr.mdr_analysis_core import safe_contingency
        
        # Generate many random tables
        np.random.seed(42)
        n_tables = 1000
        
        start = time.perf_counter()
        for _ in range(n_tables):
            table = pd.DataFrame(np.random.randint(10, 100, size=(2, 2)))
            safe_contingency(table)
        elapsed = time.perf_counter() - start
        
        throughput = n_tables / elapsed
        
        # Should process at least 100 tables per second
        assert throughput > 100, f"Throughput {throughput:.0f} tables/s should be > 100"


class TestMemoryBenchmarks:
    """Memory usage benchmarks."""

    @pytest.mark.performance
    def test_bootstrap_memory_usage(self):
        """Test memory usage of bootstrap computation."""
        from strepsuis_mdr.mdr_analysis_core import compute_bootstrap_ci
        
        data = generate_test_data(500, 20)
        
        memory_mb, result = measure_memory(
            compute_bootstrap_ci, data, n_iter=1000, confidence_level=0.95
        )
        
        # Should use less than 500 MB
        assert memory_mb < 500, f"Memory usage {memory_mb:.1f} MB should be < 500 MB"
        assert len(result) == 20

    @pytest.mark.performance
    def test_large_dataframe_memory(self):
        """Test memory usage with large DataFrames."""
        # Create large dataset
        data = generate_test_data(5000, 100)
        
        # Just measure the data size
        data_memory = data.memory_usage(deep=True).sum() / (1024 * 1024)
        
        # Should be reasonable (< 50 MB for 5000 x 100 binary data)
        assert data_memory < 50, f"Data memory {data_memory:.1f} MB should be < 50 MB"


@pytest.mark.slow
class TestStressTests:
    """Stress tests with large datasets."""

    def test_large_sample_stress(self):
        """Stress test with large number of samples."""
        from strepsuis_mdr.mdr_analysis_core import compute_bootstrap_ci
        
        # 10,000 samples, 10 features
        data = generate_test_data(10000, 10)
        
        start = time.perf_counter()
        result = compute_bootstrap_ci(data, n_iter=500, confidence_level=0.95)
        elapsed = time.perf_counter() - start
        
        assert len(result) == 10
        assert elapsed < 120, f"Should complete in < 2 minutes, took {elapsed:.1f}s"

    def test_many_features_stress(self):
        """Stress test with many features."""
        from strepsuis_mdr.mdr_analysis_core import compute_bootstrap_ci
        
        # 500 samples, 100 features
        data = generate_test_data(500, 100)
        
        start = time.perf_counter()
        result = compute_bootstrap_ci(data, n_iter=500, confidence_level=0.95)
        elapsed = time.perf_counter() - start
        
        assert len(result) == 100
        assert elapsed < 300, f"Should complete in < 5 minutes, took {elapsed:.1f}s"

    def test_large_pairwise_stress(self):
        """Stress test pairwise co-occurrence with many features."""
        from strepsuis_mdr.mdr_analysis_core import pairwise_cooccurrence
        
        # 200 samples, 50 features = 1225 pairs
        data = generate_test_data(200, 50)
        
        start = time.perf_counter()
        result = pairwise_cooccurrence(data, alpha=0.05, method="fdr_bh")
        elapsed = time.perf_counter() - start
        
        assert elapsed < 120, f"Should complete in < 2 minutes, took {elapsed:.1f}s"


class TestBigOVerification:
    """Verify Big O complexity of algorithms."""

    @pytest.mark.performance
    def test_bootstrap_linear_complexity(self):
        """Verify bootstrap has O(n) complexity in sample size."""
        from strepsuis_mdr.mdr_analysis_core import compute_bootstrap_ci
        
        sizes = [100, 200, 400, 800]
        times = []
        
        for n in sizes:
            data = generate_test_data(n, 5)
            total_time = 0
            for _ in range(3):  # Average over 3 runs
                elapsed, _ = measure_execution(
                    compute_bootstrap_ci, data, n_iter=200, confidence_level=0.95
                )
                total_time += elapsed
            times.append(total_time / 3)
        
        # Linear complexity: time should roughly double when n doubles
        ratios = [times[i+1] / times[i] for i in range(len(times)-1)]
        
        # All ratios should be less than 3 (allowing overhead)
        for i, ratio in enumerate(ratios):
            assert ratio < 3.5, f"Time ratio {ratio:.2f} at size {sizes[i+1]} suggests super-linear complexity"

    @pytest.mark.performance
    def test_pairwise_quadratic_complexity(self):
        """Verify pairwise co-occurrence has O(k^2) complexity in features."""
        from strepsuis_mdr.mdr_analysis_core import pairwise_cooccurrence
        
        n = 100
        feature_counts = [10, 20, 30]
        times = []
        
        for k in feature_counts:
            data = generate_test_data(n, k)
            total_time = 0
            for _ in range(3):
                elapsed, _ = measure_execution(pairwise_cooccurrence, data, alpha=0.10)
                total_time += elapsed
            times.append(total_time / 3)
        
        # Quadratic complexity: time should quadruple when k doubles
        # k: 10 -> 20 -> 30 means pairs: 45 -> 190 -> 435
        # Ratio of pairs: 4.2x, 2.3x
        # Times should scale similarly
        if times[0] > 0.001:  # Only check if measurable
            ratio = times[1] / times[0]
            # Should be around 4-5x for doubling features
            assert ratio < 8, f"Ratio {ratio:.2f} is reasonable for quadratic scaling"


class PerformanceReportGenerator:
    """Generate performance reports in various formats."""

    def __init__(self, output_dir: str = "tests/reports/performance"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_benchmarks(self) -> PerformanceReport:
        """Run all benchmarks and generate report."""
        from strepsuis_mdr.mdr_analysis_core import (
            compute_bootstrap_ci,
            pairwise_cooccurrence,
            safe_contingency,
        )
        
        results = []
        
        # Bootstrap benchmarks
        for n in [50, 100, 200, 500]:
            data = generate_test_data(n, 10)
            try:
                elapsed, result = measure_execution(
                    compute_bootstrap_ci, data, n_iter=500, confidence_level=0.95
                )
                memory, _ = measure_memory(
                    compute_bootstrap_ci, data, n_iter=500, confidence_level=0.95
                )
                results.append(BenchmarkResult(
                    name="bootstrap_ci",
                    input_size=n,
                    execution_time_seconds=elapsed,
                    peak_memory_mb=memory,
                    success=True,
                    additional_metrics={"n_features": 10, "n_iter": 500}
                ))
            except Exception as e:
                results.append(BenchmarkResult(
                    name="bootstrap_ci",
                    input_size=n,
                    execution_time_seconds=0,
                    peak_memory_mb=0,
                    success=False,
                    error_message=str(e)
                ))
        
        # Co-occurrence benchmarks
        for k in [10, 20, 30]:
            data = generate_test_data(100, k)
            try:
                elapsed, result = measure_execution(
                    pairwise_cooccurrence, data, alpha=0.05
                )
                memory, _ = measure_memory(
                    pairwise_cooccurrence, data, alpha=0.05
                )
                results.append(BenchmarkResult(
                    name="pairwise_cooccurrence",
                    input_size=k,
                    execution_time_seconds=elapsed,
                    peak_memory_mb=memory,
                    success=True,
                    additional_metrics={"n_samples": 100, "n_pairs": k*(k-1)//2}
                ))
            except Exception as e:
                results.append(BenchmarkResult(
                    name="pairwise_cooccurrence",
                    input_size=k,
                    execution_time_seconds=0,
                    peak_memory_mb=0,
                    success=False,
                    error_message=str(e)
                ))
        
        # Calculate summary
        bootstrap_results = [r for r in results if r.name == "bootstrap_ci" and r.success]
        cooccurrence_results = [r for r in results if r.name == "pairwise_cooccurrence" and r.success]
        
        summary = {
            "total_benchmarks": len(results),
            "successful": sum(1 for r in results if r.success),
            "failed": sum(1 for r in results if not r.success),
            "avg_bootstrap_time": np.mean([r.execution_time_seconds for r in bootstrap_results]) if bootstrap_results else 0,
            "avg_cooccurrence_time": np.mean([r.execution_time_seconds for r in cooccurrence_results]) if cooccurrence_results else 0,
        }
        
        return PerformanceReport(
            benchmark_name="strepsuis-mdr-performance",
            timestamp=datetime.now().isoformat(),
            results=results,
            summary=summary
        )

    def save_report(self, report: PerformanceReport) -> Dict[str, str]:
        """Save report in multiple formats."""
        saved_files = {}
        
        # Save as JSON
        json_file = self.output_dir / "benchmark_results.json"
        with open(json_file, "w") as f:
            json.dump({
                "benchmark_name": report.benchmark_name,
                "timestamp": report.timestamp,
                "summary": report.summary,
                "results": [
                    {
                        "name": r.name,
                        "input_size": r.input_size,
                        "execution_time_seconds": r.execution_time_seconds,
                        "peak_memory_mb": r.peak_memory_mb,
                        "success": r.success,
                        "error_message": r.error_message,
                        "additional_metrics": r.additional_metrics
                    }
                    for r in report.results
                ]
            }, f, indent=2)
        saved_files["json"] = str(json_file)
        
        # Save as CSV
        csv_file = self.output_dir / "benchmark_results.csv"
        rows = []
        for r in report.results:
            rows.append({
                "name": r.name,
                "input_size": r.input_size,
                "execution_time_seconds": r.execution_time_seconds,
                "peak_memory_mb": r.peak_memory_mb,
                "success": r.success,
            })
        pd.DataFrame(rows).to_csv(csv_file, index=False)
        saved_files["csv"] = str(csv_file)
        
        # Generate and save graph
        try:
            self._save_performance_graph(report)
            saved_files["graph"] = str(self.output_dir / "performance_graph.png")
        except ImportError:
            pass  # matplotlib not available
        
        return saved_files

    def _save_performance_graph(self, report: PerformanceReport):
        """Generate performance graph as PNG."""
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        # Bootstrap scaling
        bootstrap_results = [r for r in report.results if r.name == "bootstrap_ci" and r.success]
        if bootstrap_results:
            sizes = [r.input_size for r in bootstrap_results]
            times = [r.execution_time_seconds for r in bootstrap_results]
            axes[0].plot(sizes, times, 'bo-', linewidth=2, markersize=8)
            axes[0].set_xlabel("Sample Size (n)")
            axes[0].set_ylabel("Execution Time (seconds)")
            axes[0].set_title("Bootstrap CI Scaling")
            axes[0].grid(True, alpha=0.3)
        
        # Co-occurrence scaling
        cooccurrence_results = [r for r in report.results if r.name == "pairwise_cooccurrence" and r.success]
        if cooccurrence_results:
            sizes = [r.input_size for r in cooccurrence_results]
            times = [r.execution_time_seconds for r in cooccurrence_results]
            axes[1].plot(sizes, times, 'ro-', linewidth=2, markersize=8)
            axes[1].set_xlabel("Number of Features (k)")
            axes[1].set_ylabel("Execution Time (seconds)")
            axes[1].set_title("Pairwise Co-occurrence Scaling")
            axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "performance_graph.png", dpi=150)
        plt.close()


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
    
    assert data["summary"]["successful"] > 0
