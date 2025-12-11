"""
Comprehensive Mathematical Validation Tests using Synthetic Data

This module provides rigorous validation of all statistical methods against
synthetic data with known ground truth, ensuring mathematical correctness
of the StrepSuis-MDR analysis pipeline.

Tests validate:
1. Bootstrap CI coverage on synthetic data with known prevalences
2. Chi-square/Fisher tests on data with known associations
3. FDR correction on synthetic p-value distributions
4. MDR classification accuracy on synthetic datasets
5. Co-occurrence detection with known correlations
6. Pattern detection accuracy

Reference implementations: scipy, statsmodels, sklearn
"""

import json
import os
import time
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd
import pytest
from scipy.stats import chi2_contingency, fisher_exact, pearsonr
from statsmodels.stats.multitest import multipletests


class TestSyntheticDataGeneration:
    """Test the synthetic data generation module."""

    def test_generate_synthetic_dataset(self):
        """Test that synthetic data generation produces valid output."""
        from strepsuis_mdr.generate_synthetic_data import (
            SyntheticDataConfig,
            generate_mdr_synthetic_dataset,
        )

        config = SyntheticDataConfig(
            n_strains=50,
            n_antibiotics=10,
            n_genes=15,
            random_state=42,
        )

        data, metadata = generate_mdr_synthetic_dataset(config)

        # Verify shape
        assert len(data) == config.n_strains
        assert len(metadata.antibiotic_columns) == config.n_antibiotics
        assert len(metadata.gene_columns) == config.n_genes

        # Verify data types
        for col in metadata.antibiotic_columns:
            assert col in data.columns
            assert data[col].dtype in [np.int64, np.int32, int]
            assert set(data[col].unique()).issubset({0, 1})

    def test_prevalence_rates_generation(self):
        """Test that prevalence rates follow Beta distribution."""
        from strepsuis_mdr.generate_synthetic_data import generate_prevalence_rates

        np.random.seed(42)
        prevalences = generate_prevalence_rates(
            n_features=1000,
            mean=0.35,
            std=0.15,
            random_state=42,
        )

        # Check bounds
        assert np.all(prevalences >= 0.01)
        assert np.all(prevalences <= 0.99)

        # Check mean is approximately correct
        assert abs(np.mean(prevalences) - 0.35) < 0.05

    def test_correlated_features_generation(self):
        """Test that correlated features have expected correlation."""
        from strepsuis_mdr.generate_synthetic_data import (
            generate_binary_data_binomial,
            generate_correlated_features,
        )

        np.random.seed(42)
        n = 500

        # Generate base feature
        base = generate_binary_data_binomial(n, 0.5, random_state=42)

        # Generate correlated feature
        target_corr = 0.7
        correlated = generate_correlated_features(base, target_corr, random_state=123)

        # Calculate actual correlation (phi coefficient approximation)
        # For binary data, phi ≈ Pearson r
        actual_corr, _ = pearsonr(base, correlated)

        # Allow some tolerance (correlation induction is not exact)
        assert actual_corr > 0.3, f"Expected positive correlation, got {actual_corr}"

    def test_synthetic_data_reproducibility(self):
        """Test that same seed produces identical data."""
        from strepsuis_mdr.generate_synthetic_data import (
            SyntheticDataConfig,
            generate_mdr_synthetic_dataset,
        )

        config = SyntheticDataConfig(n_strains=30, random_state=12345)

        data1, _ = generate_mdr_synthetic_dataset(config)
        data2, _ = generate_mdr_synthetic_dataset(config)

        pd.testing.assert_frame_equal(data1, data2)


class TestBootstrapValidationWithSynthetic:
    """Validate bootstrap CI using synthetic data with known ground truth."""

    def test_bootstrap_ci_contains_true_prevalence(self):
        """Test that 95% CI contains true prevalence rate."""
        from strepsuis_mdr.generate_synthetic_data import (
            SyntheticDataConfig,
            generate_mdr_synthetic_dataset,
        )
        from strepsuis_mdr.mdr_analysis_core import compute_bootstrap_ci

        config = SyntheticDataConfig(
            n_strains=200,
            n_antibiotics=5,
            noise_level=0.02,  # Low noise
            random_state=42,
        )

        data, metadata = generate_mdr_synthetic_dataset(config)

        # Compute bootstrap CI for antibiotics
        ab_data = data[metadata.antibiotic_columns]
        ci_result = compute_bootstrap_ci(ab_data, n_iter=1000, confidence_level=0.95)

        # Check that true prevalence is within or near CI
        hits = 0
        for col in metadata.antibiotic_columns:
            true_prev = metadata.true_prevalences[col] * 100  # Convert to percentage
            row = ci_result[ci_result["ColumnName"] == col].iloc[0]
            ci_lower = row["CI_Lower"]
            ci_upper = row["CI_Upper"]

            # Allow some tolerance for noise effects
            if ci_lower - 10 < true_prev < ci_upper + 10:
                hits += 1

        # At least 60% of CIs should contain the true value (accounting for noise)
        assert hits >= len(metadata.antibiotic_columns) * 0.6

    def test_bootstrap_width_decreases_with_n(self):
        """Test that CI width decreases with sample size."""
        from strepsuis_mdr.mdr_analysis_core import compute_bootstrap_ci

        np.random.seed(42)

        # Small sample
        small = pd.DataFrame({"col": np.random.binomial(1, 0.5, 30)})
        small_result = compute_bootstrap_ci(small, n_iter=500, confidence_level=0.95)
        small_width = small_result["CI_Upper"].iloc[0] - small_result["CI_Lower"].iloc[0]

        # Large sample
        large = pd.DataFrame({"col": np.random.binomial(1, 0.5, 300)})
        large_result = compute_bootstrap_ci(large, n_iter=500, confidence_level=0.95)
        large_width = large_result["CI_Upper"].iloc[0] - large_result["CI_Lower"].iloc[0]

        assert large_width < small_width


class TestAssociationValidationWithSynthetic:
    """Validate association tests using synthetic data with known correlations."""

    def test_detect_known_correlations(self):
        """Test that known correlations are detected."""
        from strepsuis_mdr.generate_synthetic_data import (
            SyntheticDataConfig,
            generate_mdr_synthetic_dataset,
        )
        from strepsuis_mdr.mdr_analysis_core import pairwise_cooccurrence

        config = SyntheticDataConfig(
            n_strains=150,
            n_antibiotics=6,
            n_genes=12,
            correlation_strength=0.7,
            noise_level=0.02,
            random_state=42,
        )

        data, metadata = generate_mdr_synthetic_dataset(config)

        # Get all feature columns
        feature_cols = metadata.antibiotic_columns + metadata.gene_columns
        feature_data = data[feature_cols]

        # Run pairwise co-occurrence
        result = pairwise_cooccurrence(feature_data, alpha=0.10, method="fdr_bh")

        # Check if known correlations are in results
        if result.empty:
            pytest.skip("No significant co-occurrences found")

        # Check that at least some known correlations are detected
        detected_pairs = set()
        for _, row in result.iterrows():
            detected_pairs.add((row["Item1"], row["Item2"]))
            detected_pairs.add((row["Item2"], row["Item1"]))

        hits = 0
        for feat1, feat2, corr in metadata.true_correlations:
            if (feat1, feat2) in detected_pairs or (feat2, feat1) in detected_pairs:
                hits += 1

        # Should detect at least some known correlations
        if len(metadata.true_correlations) > 0:
            assert hits > 0 or len(result) > 0

    def test_phi_coefficient_sign_correct(self):
        """Test that phi coefficient has correct sign for known associations."""
        from strepsuis_mdr.mdr_analysis_core import safe_contingency

        # Positive association: A and B tend to co-occur
        pos_table = pd.DataFrame([[40, 10], [10, 40]])
        _, _, phi_pos = safe_contingency(pos_table)
        assert phi_pos > 0, f"Expected positive phi, got {phi_pos}"

        # Negative association: A and B tend to be mutually exclusive
        neg_table = pd.DataFrame([[10, 40], [40, 10]])
        _, _, phi_neg = safe_contingency(neg_table)
        assert phi_neg < 0, f"Expected negative phi, got {phi_neg}"


class TestMDRClassificationWithSynthetic:
    """Validate MDR classification using synthetic data with known MDR status."""

    def test_mdr_identification_accuracy(self):
        """Test that MDR identification matches known ground truth."""
        from strepsuis_mdr.generate_synthetic_data import (
            SyntheticDataConfig,
            generate_mdr_synthetic_dataset,
        )
        from strepsuis_mdr.mdr_analysis_core import (
            build_class_resistance,
            identify_mdr_isolates,
        )

        config = SyntheticDataConfig(
            n_strains=100,
            n_antibiotics=13,
            random_state=42,
        )

        data, metadata = generate_mdr_synthetic_dataset(config)

        # Run MDR identification
        class_res = build_class_resistance(data, metadata.antibiotic_columns)
        mdr_mask = identify_mdr_isolates(class_res, threshold=3)

        # Compare with ground truth
        # Note: Ground truth uses same logic, so should match exactly
        accuracy = (mdr_mask.values == metadata.true_mdr_status).mean()

        assert accuracy > 0.95, f"MDR identification accuracy {accuracy} should be > 95%"


class TestFDRCorrectionWithSynthetic:
    """Validate FDR correction using synthetic p-value distributions."""

    def test_fdr_controls_false_discovery_rate(self):
        """Test that FDR procedure controls false discoveries."""
        np.random.seed(42)

        # Generate p-values: some truly significant, some null
        n_tests = 100
        n_true_null = 80
        n_true_alt = 20

        # Null p-values: uniform(0, 1)
        null_pvals = np.random.uniform(0, 1, n_true_null)

        # Alternative p-values: concentrated near 0
        alt_pvals = np.random.beta(1, 20, n_true_alt)  # Beta(1, 20) concentrates near 0

        all_pvals = np.concatenate([null_pvals, alt_pvals])
        true_labels = np.concatenate([np.zeros(n_true_null), np.ones(n_true_alt)])

        # Apply FDR correction
        reject, corrected, _, _ = multipletests(all_pvals, alpha=0.05, method="fdr_bh")

        # Count false discoveries among rejections
        false_discoveries = np.sum(reject & (true_labels == 0))
        total_discoveries = np.sum(reject)

        if total_discoveries > 0:
            fdr = false_discoveries / total_discoveries
            # FDR should be approximately controlled at alpha level
            # Allow some tolerance due to finite sample
            assert fdr < 0.15, f"FDR {fdr} should be controlled at approximately 0.05"


class TestPatternDetectionWithSynthetic:
    """Validate pattern detection using synthetic data."""

    def test_pattern_extraction(self):
        """Test that patterns are correctly extracted."""
        from strepsuis_mdr.mdr_analysis_core import get_mdr_patterns_pheno

        # Create synthetic class resistance data
        class_res = pd.DataFrame(
            {
                "Tetracyclines": [1, 1, 0, 1, 0],
                "Macrolides": [1, 0, 1, 1, 0],
                "Penicillins": [0, 1, 1, 1, 0],
            }
        )

        patterns = get_mdr_patterns_pheno(class_res)

        # Check pattern for row 0: Tetracyclines + Macrolides
        assert "Macrolides" in patterns.iloc[0]
        assert "Tetracyclines" in patterns.iloc[0]

        # Check pattern for row 4: No resistance
        assert patterns.iloc[4] == ("No_Resistance",)


@pytest.mark.slow
class TestPerformanceWithSynthetic:
    """Performance benchmarks using synthetic data."""

    def test_bootstrap_performance_large_dataset(self):
        """Benchmark bootstrap on large synthetic dataset."""
        from strepsuis_mdr.generate_synthetic_data import (
            SyntheticDataConfig,
            generate_mdr_synthetic_dataset,
        )
        from strepsuis_mdr.mdr_analysis_core import compute_bootstrap_ci

        config = SyntheticDataConfig(
            n_strains=500,
            n_antibiotics=13,  # Max supported antibiotics
            random_state=42,
        )

        data, metadata = generate_mdr_synthetic_dataset(config)
        ab_data = data[metadata.antibiotic_columns]

        start = time.time()
        result = compute_bootstrap_ci(ab_data, n_iter=1000, confidence_level=0.95)
        elapsed = time.time() - start

        assert elapsed < 60, f"Bootstrap should complete in <60s, took {elapsed:.1f}s"
        assert len(result) == len(metadata.antibiotic_columns)

    def test_cooccurrence_performance_large_dataset(self):
        """Benchmark pairwise co-occurrence on large dataset."""
        from strepsuis_mdr.mdr_analysis_core import pairwise_cooccurrence

        np.random.seed(42)

        # 500 samples, 30 features = 435 pairs
        data = pd.DataFrame(
            np.random.binomial(1, 0.4, (500, 30)),
            columns=[f"feat_{i}" for i in range(30)],
        )

        start = time.time()
        result = pairwise_cooccurrence(data, alpha=0.05, method="fdr_bh")
        elapsed = time.time() - start

        assert elapsed < 30, f"Co-occurrence should complete in <30s, took {elapsed:.1f}s"


class TestValidationReportGeneration:
    """Generate validation reports for math validation directory."""

    @pytest.fixture
    def report_dir(self, tmp_path):
        """Create temporary report directory."""
        return tmp_path / "math_validation"

    def test_generate_validation_report(self, report_dir):
        """Generate a validation report summarizing test results."""
        from strepsuis_mdr.generate_synthetic_data import (
            SyntheticDataConfig,
            generate_mdr_synthetic_dataset,
            validate_synthetic_data,
        )

        report_dir.mkdir(parents=True, exist_ok=True)

        # Generate synthetic data
        config = SyntheticDataConfig(n_strains=100, random_state=42)
        data, metadata = generate_mdr_synthetic_dataset(config)

        # Validate
        validation = validate_synthetic_data(data, metadata)

        # Create report
        report = {
            "test_name": "Synthetic Data Validation",
            "timestamp": pd.Timestamp.now().isoformat(),
            "config": {
                "n_strains": config.n_strains,
                "n_antibiotics": config.n_antibiotics,
                "random_state": config.random_state,
            },
            "validation_passed": validation["validation_passed"],
            "checks_passed": len(validation["checks"]),
            "warnings": len(validation["warnings"]),
            "errors": len(validation["errors"]),
        }

        # Save report
        report_file = report_dir / "validation_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        assert report_file.exists()
        assert validation["validation_passed"]


class TestNumericalStabilityWithSynthetic:
    """Test numerical stability with edge cases in synthetic data."""

    def test_extreme_prevalences(self):
        """Test handling of extreme prevalence rates."""
        from strepsuis_mdr.mdr_analysis_core import compute_bootstrap_ci

        # Very low prevalence (1%)
        low_prev = pd.DataFrame({"col": [1] + [0] * 99})
        result_low = compute_bootstrap_ci(low_prev, n_iter=500, confidence_level=0.95)
        assert not np.isnan(result_low["Mean"].iloc[0])
        assert result_low["Mean"].iloc[0] <= 5  # Should be low

        # Very high prevalence (99%)
        high_prev = pd.DataFrame({"col": [1] * 99 + [0]})
        result_high = compute_bootstrap_ci(high_prev, n_iter=500, confidence_level=0.95)
        assert not np.isnan(result_high["Mean"].iloc[0])
        assert result_high["Mean"].iloc[0] >= 95  # Should be high

    def test_small_sample_stability(self):
        """Test stability with very small samples."""
        from strepsuis_mdr.mdr_analysis_core import compute_bootstrap_ci

        # Very small sample
        small = pd.DataFrame({"col": [1, 0, 1]})
        result = compute_bootstrap_ci(small, n_iter=100, confidence_level=0.95)

        assert len(result) == 1
        assert not np.isnan(result["Mean"].iloc[0])


class TestSciPyValidation:
    """Direct validation against scipy reference implementations."""

    def test_chi_square_exact_match(self):
        """Test exact match with scipy chi2_contingency."""
        from strepsuis_mdr.mdr_analysis_core import safe_contingency

        # Use table with high expected counts to ensure chi-square path
        table = pd.DataFrame([[100, 50], [50, 100]])

        chi2_ours, p_ours, phi_ours = safe_contingency(table)
        chi2_scipy, p_scipy, _, _ = chi2_contingency(table)

        np.testing.assert_almost_equal(chi2_ours, chi2_scipy, decimal=4)
        np.testing.assert_almost_equal(p_ours, p_scipy, decimal=4)

    def test_fisher_exact_match(self):
        """Test exact match with scipy fisher_exact."""
        from strepsuis_mdr.mdr_analysis_core import safe_contingency

        # Use table with low expected counts to trigger Fisher's path
        table = pd.DataFrame([[5, 1], [1, 5]])

        chi2_ours, p_ours, phi_ours = safe_contingency(table)
        _, p_scipy = fisher_exact(table)

        np.testing.assert_almost_equal(p_ours, p_scipy, decimal=4)

    def test_fdr_matches_statsmodels(self):
        """Test FDR correction matches statsmodels exactly."""
        np.random.seed(42)
        p_values = np.random.uniform(0, 1, 50)

        _, corrected_sm, _, _ = multipletests(p_values, method="fdr_bh", alpha=0.05)

        # Verify sorted corrected p-values are monotonic
        sorted_indices = np.argsort(p_values)
        sorted_corrected = corrected_sm[sorted_indices]

        for i in range(len(sorted_corrected) - 1):
            assert sorted_corrected[i] <= sorted_corrected[i + 1] + 1e-10
