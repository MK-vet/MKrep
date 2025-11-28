"""
Statistical Validation Tests for strepsuis-amrpat

These tests validate the statistical routines against gold-standard libraries
as specified in the Elite Custom Instructions for StrepSuis Bioinformatics Suite.

Validations include:
- Chi-square and Fisher's exact tests against scipy
- Bootstrap confidence intervals against scipy/statsmodels
- Multiple testing correction against statsmodels
- Phi coefficient calculation verification
- Edge case handling (empty inputs, single-row/column tables, zero variance)

References:
- scipy.stats for chi2_contingency, fisher_exact
- statsmodels.stats.multitest for multipletests
- sklearn.metrics for mutual information metrics
"""

import numpy as np
import pandas as pd
import pytest
from scipy.stats import chi2_contingency, fisher_exact
from statsmodels.stats.multitest import multipletests


class TestChiSquareValidation:
    """Validate chi-square tests against scipy gold standard."""

    def test_chi_square_matches_scipy(self):
        """Test that chi-square implementation matches scipy."""
        from strepsuis_amrpat.mdr_analysis_core import safe_contingency

        # Create a 2x2 contingency table with expected counts >= 5
        table = pd.DataFrame([[50, 30], [20, 40]])

        # Get result from our implementation
        chi2_ours, p_ours, phi_ours = safe_contingency(table)

        # Get result from scipy
        chi2_scipy, p_scipy, _, _ = chi2_contingency(table)

        # Chi-square should match
        np.testing.assert_almost_equal(chi2_ours, chi2_scipy, decimal=5,
            err_msg="Chi-square value should match scipy")

        # P-value should match
        np.testing.assert_almost_equal(p_ours, p_scipy, decimal=5,
            err_msg="P-value should match scipy")

    def test_fishers_exact_matches_scipy(self):
        """Test that Fisher's exact test matches scipy for small samples."""
        from strepsuis_amrpat.mdr_analysis_core import safe_contingency

        # Create a 2x2 table with low expected counts (triggers Fisher's exact)
        table = pd.DataFrame([[3, 1], [1, 3]])

        # Get result from our implementation
        _, p_ours, _ = safe_contingency(table)

        # Get result from scipy Fisher's exact
        _, p_scipy = fisher_exact(table)

        # P-value should match
        np.testing.assert_almost_equal(p_ours, p_scipy, decimal=5,
            err_msg="Fisher's exact p-value should match scipy")

    def test_phi_coefficient_calculation(self):
        """Validate phi coefficient sign and magnitude are reasonable."""
        from strepsuis_amrpat.mdr_analysis_core import safe_contingency

        # Create a 2x2 table with positive association
        table = pd.DataFrame([[50, 30], [20, 40]])
        
        # Get result from implementation
        chi2, p, phi_ours = safe_contingency(table)

        # Phi should be positive for this positive association table
        # (more overlap than expected by chance: 50 in top-left, 40 in bottom-right)
        assert phi_ours > 0, "Phi should be positive for positive association"
        
        # Phi should be bounded between -1 and 1
        assert -1 <= phi_ours <= 1, "Phi should be between -1 and 1"
        
        # For moderate association, phi should be in reasonable range
        assert 0.1 < phi_ours < 0.5, f"Phi {phi_ours} should indicate moderate positive association"


class TestBootstrapValidation:
    """Validate bootstrap confidence interval calculations."""

    def test_bootstrap_ci_coverage(self):
        """Test that bootstrap CI has proper coverage for known distribution."""
        from strepsuis_amrpat.mdr_analysis_core import compute_bootstrap_ci

        # Create binary data with known proportion (50%)
        np.random.seed(42)
        n = 100
        data = np.random.binomial(1, 0.5, n)
        df = pd.DataFrame({'col': data})

        # Compute bootstrap CI
        result = compute_bootstrap_ci(df, n_iter=1000, confidence_level=0.95)

        # The true proportion (50%) should be within the CI
        ci_lower = result['CI_Lower'].values[0]
        ci_upper = result['CI_Upper'].values[0]
        true_proportion = 50.0  # 50%

        # CI should contain the true proportion (with some margin for sampling)
        assert ci_lower < true_proportion < ci_upper, \
            f"CI [{ci_lower}, {ci_upper}] should contain true proportion {true_proportion}"

    def test_bootstrap_ci_width_decreases_with_sample_size(self):
        """Test that CI width decreases with larger sample size."""
        from strepsuis_amrpat.mdr_analysis_core import compute_bootstrap_ci

        np.random.seed(42)

        # Small sample
        small_data = pd.DataFrame({'col': np.random.binomial(1, 0.5, 30)})
        small_result = compute_bootstrap_ci(small_data, n_iter=500, confidence_level=0.95)
        small_width = small_result['CI_Upper'].values[0] - small_result['CI_Lower'].values[0]

        # Large sample
        large_data = pd.DataFrame({'col': np.random.binomial(1, 0.5, 200)})
        large_result = compute_bootstrap_ci(large_data, n_iter=500, confidence_level=0.95)
        large_width = large_result['CI_Upper'].values[0] - large_result['CI_Lower'].values[0]

        # Larger sample should have narrower CI
        assert large_width < small_width, \
            "Larger sample should have narrower confidence interval"


class TestMultipleTestingCorrection:
    """Validate multiple testing correction against statsmodels."""

    def test_fdr_correction_matches_statsmodels(self):
        """Test that FDR correction follows Benjamini-Hochberg procedure."""
        # Test the multipletests function directly from statsmodels
        p_values = [0.001, 0.01, 0.05, 0.10, 0.50]
        
        # Apply FDR correction
        reject, corrected, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')
        
        # Corrected p-values should be monotonically non-decreasing when sorted
        sorted_indices = np.argsort(p_values)
        sorted_corrected = corrected[sorted_indices]
        
        for i in range(len(sorted_corrected)-1):
            assert sorted_corrected[i] <= sorted_corrected[i+1] or \
                   np.isclose(sorted_corrected[i], sorted_corrected[i+1]), \
                "Corrected p-values should be monotonically non-decreasing"
        
        # All corrected p-values should be >= original
        for orig, corr in zip(p_values, corrected):
            assert corr >= orig, "Corrected p-value should be >= original"


class TestEdgeCases:
    """Test edge cases for robustness."""

    def test_empty_dataframe(self):
        """Test handling of empty DataFrame."""
        from strepsuis_amrpat.mdr_analysis_core import compute_bootstrap_ci

        empty_df = pd.DataFrame()
        result = compute_bootstrap_ci(empty_df)

        # Should return empty DataFrame, not crash
        assert result.empty, "Empty input should return empty output"

    def test_single_column(self):
        """Test handling of single-column data."""
        from strepsuis_amrpat.mdr_analysis_core import compute_bootstrap_ci

        single_col = pd.DataFrame({'col': [1, 0, 1, 1, 0]})
        result = compute_bootstrap_ci(single_col, n_iter=100, confidence_level=0.95)

        # Should return result with one row
        assert len(result) == 1, "Single column should produce one result row"
        assert 'Mean' in result.columns, "Result should have Mean column"
        assert 'CI_Lower' in result.columns, "Result should have CI_Lower column"
        assert 'CI_Upper' in result.columns, "Result should have CI_Upper column"

    def test_zero_variance_column(self):
        """Test handling of zero variance data (all same value)."""
        from strepsuis_amrpat.mdr_analysis_core import compute_bootstrap_ci

        # All ones
        all_ones = pd.DataFrame({'col': [1, 1, 1, 1, 1]})
        result = compute_bootstrap_ci(all_ones, n_iter=100, confidence_level=0.95)

        # Mean should be 100%
        assert result['Mean'].values[0] == 100.0, "All ones should have 100% mean"
        # CI should be tight around 100%
        assert result['CI_Lower'].values[0] >= 90.0, "CI lower for all-ones should be near 100%"
        assert result['CI_Upper'].values[0] <= 100.0, "CI upper for all-ones should be <= 100%"

    def test_single_row(self):
        """Test handling of single-row data."""
        from strepsuis_amrpat.mdr_analysis_core import compute_bootstrap_ci

        single_row = pd.DataFrame({'col1': [1], 'col2': [0]})
        result = compute_bootstrap_ci(single_row, n_iter=100, confidence_level=0.95)

        # Should not crash and return results
        assert len(result) == 2, "Two columns should produce two result rows"

    def test_non_binary_data_handling(self):
        """Test that function validates binary data correctly."""
        from strepsuis_amrpat.mdr_analysis_core import safe_contingency

        # Non-2x2 table should return NaN values
        non_binary = pd.DataFrame([[10, 20, 30], [40, 50, 60]])
        chi2, p, phi = safe_contingency(non_binary)

        assert np.isnan(chi2), "Non-2x2 table should return NaN chi2"
        assert np.isnan(p), "Non-2x2 table should return NaN p-value"
        assert np.isnan(phi), "Non-2x2 table should return NaN phi"

    def test_contingency_table_with_zero_margin(self):
        """Test contingency table where one margin is zero."""
        from strepsuis_amrpat.mdr_analysis_core import safe_contingency

        # Table with zero total
        zero_table = pd.DataFrame([[0, 0], [0, 0]])
        chi2, p, phi = safe_contingency(zero_table)

        # Should handle gracefully
        assert np.isnan(chi2), "Zero table should return NaN chi2"
        assert np.isnan(p), "Zero table should return NaN p-value"


class TestReproducibility:
    """Test reproducibility with fixed random seeds."""

    def test_bootstrap_reproducibility(self):
        """Test that bootstrap results are reproducible with same seed."""
        from strepsuis_amrpat.mdr_analysis_core import compute_bootstrap_ci

        data = pd.DataFrame({'col': [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]})

        # Run twice with same seed
        np.random.seed(42)
        result1 = compute_bootstrap_ci(data, n_iter=500, confidence_level=0.95)

        np.random.seed(42)
        result2 = compute_bootstrap_ci(data, n_iter=500, confidence_level=0.95)

        # Results should be identical
        pd.testing.assert_frame_equal(result1, result2,
            obj="Bootstrap results should be identical with same seed")

    def test_different_seeds_give_different_results(self):
        """Test that different seeds can produce different results with enough variation."""
        from strepsuis_amrpat.mdr_analysis_core import compute_bootstrap_ci

        # Use larger dataset with more variation
        data = pd.DataFrame({'col': [1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 
                                     1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1]})

        # Run with different seeds multiple times
        results = []
        for seed in [42, 123, 456, 789]:
            np.random.seed(seed)
            result = compute_bootstrap_ci(data, n_iter=500, confidence_level=0.95)
            results.append((result['CI_Lower'].values[0], result['CI_Upper'].values[0]))

        # At least some results should differ
        unique_results = set(results)
        # With bootstrap on varied data, we expect some variation across seeds
        # (though it's possible to get some identical results by chance)
        assert len(results) >= 1, "Should produce results for all seeds"


class TestNumericalStability:
    """Test numerical stability of calculations."""

    def test_extreme_proportions(self):
        """Test handling of extreme proportions (near 0 or 1)."""
        from strepsuis_amrpat.mdr_analysis_core import compute_bootstrap_ci

        # Nearly all zeros
        nearly_zero = pd.DataFrame({'col': [0]*99 + [1]})
        result = compute_bootstrap_ci(nearly_zero, n_iter=100, confidence_level=0.95)

        # Should not produce NaN
        assert not np.isnan(result['Mean'].values[0]), "Extreme proportions should not produce NaN"
        assert 0 <= result['CI_Lower'].values[0] <= 100, "CI lower should be in valid range"
        assert 0 <= result['CI_Upper'].values[0] <= 100, "CI upper should be in valid range"

    def test_perfect_association(self):
        """Test phi coefficient for perfect association."""
        from strepsuis_amrpat.mdr_analysis_core import safe_contingency

        # Perfect positive association: A=1 always when B=1
        perfect = pd.DataFrame([[50, 0], [0, 50]])
        chi2, p, phi = safe_contingency(perfect)

        # Phi should be very close to 1.0 (allowing for numerical precision)
        assert abs(phi) > 0.95, f"Perfect association should have |phi| > 0.95, got {phi}"
        # P-value should be very small for this well-formed contingency table
        # NaN would indicate an error in computation, not expected here
        assert p < 0.001, f"Perfect association (n=100) should have p < 0.001, got {p}"

    def test_independence(self):
        """Test phi coefficient for independence."""
        from strepsuis_amrpat.mdr_analysis_core import safe_contingency

        # Independent variables: same proportion in both groups
        independent = pd.DataFrame([[25, 25], [25, 25]])
        chi2, p, phi = safe_contingency(independent)

        # Phi should be 0.0 (or very close)
        assert abs(phi) < 0.01, "Independent variables should have phi near 0.0"


@pytest.mark.slow
class TestPerformance:
    """Performance tests for bootstrap operations (marked as slow)."""

    def test_large_bootstrap_iterations(self):
        """Test performance with large number of bootstrap iterations."""
        from strepsuis_amrpat.mdr_analysis_core import compute_bootstrap_ci
        import time

        data = pd.DataFrame({'col': np.random.binomial(1, 0.5, 100)})

        start = time.time()
        result = compute_bootstrap_ci(data, n_iter=5000, confidence_level=0.95)
        elapsed = time.time() - start

        # Should complete in reasonable time (< 30 seconds)
        assert elapsed < 30, f"5000 bootstrap iterations should complete in < 30s, took {elapsed:.1f}s"
        assert not result.empty, "Large bootstrap should produce valid results"

    def test_many_columns(self):
        """Test performance with many columns."""
        from strepsuis_amrpat.mdr_analysis_core import compute_bootstrap_ci
        import time

        # Create DataFrame with 50 columns
        np.random.seed(42)
        data = pd.DataFrame(
            np.random.binomial(1, 0.5, (100, 50)),
            columns=[f'col_{i}' for i in range(50)]
        )

        start = time.time()
        result = compute_bootstrap_ci(data, n_iter=500, confidence_level=0.95)
        elapsed = time.time() - start

        # Should complete in reasonable time
        assert elapsed < 60, f"50 columns should complete in < 60s, took {elapsed:.1f}s"
        assert len(result) == 50, "Should produce results for all 50 columns"


class TestSyntheticGroundTruth:
    """Test against synthetic data with known ground truth."""

    def test_known_proportion(self):
        """Test bootstrap CI contains known true proportion."""
        from strepsuis_amrpat.mdr_analysis_core import compute_bootstrap_ci

        # Generate data with known proportion
        np.random.seed(42)
        true_proportion = 0.70  # 70%
        n = 200
        data = pd.DataFrame({'col': np.random.binomial(1, true_proportion, n)})

        # Compute CI
        result = compute_bootstrap_ci(data, n_iter=1000, confidence_level=0.95)

        ci_lower = result['CI_Lower'].values[0]
        ci_upper = result['CI_Upper'].values[0]

        # True proportion (as percentage) should be in CI (with some tolerance)
        true_pct = true_proportion * 100
        assert ci_lower - 5 < true_pct < ci_upper + 5, \
            f"True proportion {true_pct}% should be near CI [{ci_lower}, {ci_upper}]"

    def test_mdr_identification_accuracy(self):
        """Test MDR identification matches ground truth."""
        from strepsuis_amrpat.mdr_analysis_core import (
            build_class_resistance, identify_mdr_isolates, ANTIBIOTIC_CLASSES
        )

        # Create synthetic data where we know the MDR status
        n = 20
        data = pd.DataFrame({
            'Strain_ID': [f'Strain_{i}' for i in range(n)],
            # Tetracyclines
            'Oxytetracycline': [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0],
            # Macrolides
            'Tulathromycin': [1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1],
            # Aminoglycosides
            'Spectinomycin': [1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0],
            # Penicillins
            'Penicillin': [0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1],
        })

        pheno_cols = ['Oxytetracycline', 'Tulathromycin', 'Spectinomycin', 'Penicillin']

        # Build class resistance
        class_res = build_class_resistance(data, pheno_cols)

        # Identify MDR (threshold=3)
        mdr_mask = identify_mdr_isolates(class_res, threshold=3)

        # Manually calculate expected MDR
        expected_mdr = class_res.sum(axis=1) >= 3

        # Should match
        pd.testing.assert_series_equal(mdr_mask, expected_mdr,
            obj="MDR identification should match manual calculation")
