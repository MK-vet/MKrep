"""
Comprehensive Unit Tests for cluster_analysis_core.py

This module provides extensive test coverage for all core clustering analysis functions,
including:
- K-modes clustering
- Silhouette score optimization
- Bootstrap confidence intervals
- Chi-square analysis
- Log-odds ratios
- MCA (Multiple Correspondence Analysis)
- Feature importance via Random Forest
- Association rule mining
- Phi correlation

Target: 95%+ coverage for cluster_analysis_core.py
"""

import numpy as np
import pandas as pd
import pytest
from scipy.stats import chi2_contingency, fisher_exact
from statsmodels.stats.multitest import multipletests


# ============================================================================
# Test validate_binary_data function
# ============================================================================
class TestValidateBinaryData:
    """Test the binary data validation function."""

    def test_valid_binary_data(self):
        """Test with valid 0/1 binary data."""
        from strepsuis_amrvirkm.cluster_analysis_core import validate_binary_data
        
        df = pd.DataFrame({
            'A': [0, 1, 0, 1],
            'B': [1, 0, 1, 0],
        })
        # Should not raise any exception
        validate_binary_data(df)

    def test_invalid_non_binary_data(self):
        """Test with non-binary data raises ValueError."""
        from strepsuis_amrvirkm.cluster_analysis_core import validate_binary_data
        
        df = pd.DataFrame({
            'A': [0, 1, 2, 3],  # Non-binary
            'B': [1, 0, 1, 0],
        })
        with pytest.raises(ValueError, match="Data is not strictly 0/1 binary"):
            validate_binary_data(df)

    def test_invalid_negative_values(self):
        """Test with negative values raises ValueError."""
        from strepsuis_amrvirkm.cluster_analysis_core import validate_binary_data
        
        df = pd.DataFrame({
            'A': [-1, 0, 1, 0],
            'B': [1, 0, 1, 0],
        })
        with pytest.raises(ValueError, match="Data is not strictly 0/1 binary"):
            validate_binary_data(df)

    def test_invalid_float_values(self):
        """Test with float values raises ValueError."""
        from strepsuis_amrvirkm.cluster_analysis_core import validate_binary_data
        
        df = pd.DataFrame({
            'A': [0.5, 1, 0, 1],
            'B': [1, 0, 1, 0],
        })
        with pytest.raises(ValueError, match="Data is not strictly 0/1 binary"):
            validate_binary_data(df)


# ============================================================================
# Test retry_operation function
# ============================================================================
class TestRetryOperation:
    """Test the retry operation decorator."""

    def test_successful_operation(self):
        """Test that successful operation returns result."""
        from strepsuis_amrvirkm.cluster_analysis_core import retry_operation
        
        def successful_func():
            return 42
        
        result = retry_operation(successful_func)
        assert result == 42

    def test_eventually_successful_operation(self):
        """Test operation that fails then succeeds."""
        from strepsuis_amrvirkm.cluster_analysis_core import retry_operation
        
        attempt_count = [0]
        
        def failing_then_success():
            attempt_count[0] += 1
            if attempt_count[0] < 3:
                raise ValueError("Not yet!")
            return "success"
        
        result = retry_operation(failing_then_success, max_attempts=3)
        assert result == "success"
        assert attempt_count[0] == 3

    def test_always_failing_operation(self):
        """Test operation that always fails raises after max attempts."""
        from strepsuis_amrvirkm.cluster_analysis_core import retry_operation
        
        def always_fail():
            raise ValueError("Always fails")
        
        with pytest.raises(ValueError, match="Always fails"):
            retry_operation(always_fail, max_attempts=3)


# ============================================================================
# Test bootstrap_confidence_interval function
# ============================================================================
class TestBootstrapConfidenceInterval:
    """Test bootstrap confidence interval calculation."""

    def test_basic_bootstrap_ci(self):
        """Test basic bootstrap CI calculation."""
        from strepsuis_amrvirkm.cluster_analysis_core import bootstrap_confidence_interval
        
        ci_low, ci_high = bootstrap_confidence_interval(
            percentage=50.0, count=50, total_samples=100, num_bootstrap=500
        )
        
        # CI should be reasonable (around 50%)
        assert ci_low < 50.0
        assert ci_high > 50.0
        assert ci_low >= 0
        assert ci_high <= 100

    def test_zero_samples_returns_nan(self):
        """Test with zero total samples returns NaN."""
        from strepsuis_amrvirkm.cluster_analysis_core import bootstrap_confidence_interval
        
        ci_low, ci_high = bootstrap_confidence_interval(
            percentage=0.0, count=0, total_samples=0
        )
        
        assert np.isnan(ci_low)
        assert np.isnan(ci_high)

    def test_high_percentage_ci(self):
        """Test CI for high percentage."""
        from strepsuis_amrvirkm.cluster_analysis_core import bootstrap_confidence_interval
        
        ci_low, ci_high = bootstrap_confidence_interval(
            percentage=90.0, count=90, total_samples=100, num_bootstrap=500
        )
        
        # CI should be high (around 90%)
        assert ci_low > 70
        assert ci_high <= 100


# ============================================================================
# Test perform_kmodes function
# ============================================================================
class TestPerformKmodes:
    """Test K-modes clustering function."""

    def test_basic_kmodes(self):
        """Test basic K-modes clustering."""
        from strepsuis_amrvirkm.cluster_analysis_core import perform_kmodes
        
        # Create simple binary data
        np.random.seed(42)
        data = pd.DataFrame({
            'A': [1, 1, 1, 0, 0, 0],
            'B': [1, 1, 0, 0, 0, 1],
            'C': [0, 0, 1, 1, 1, 0],
        })
        
        model, clusters = perform_kmodes(data, n_clusters=2)
        
        # Clusters should be 1-based
        assert min(clusters) >= 1
        assert len(clusters) == len(data)
        
        # Should have correct number of clusters
        assert len(np.unique(clusters)) <= 2

    def test_kmodes_deterministic_with_seed(self):
        """Test that K-modes is deterministic with same seed."""
        from strepsuis_amrvirkm.cluster_analysis_core import perform_kmodes
        
        np.random.seed(42)
        data = pd.DataFrame({
            'A': [1, 1, 1, 0, 0, 0, 1, 0],
            'B': [1, 1, 0, 0, 0, 1, 1, 0],
        })
        
        _, clusters1 = perform_kmodes(data, n_clusters=2)
        
        np.random.seed(42)
        _, clusters2 = perform_kmodes(data, n_clusters=2)
        
        np.testing.assert_array_equal(clusters1, clusters2)


# ============================================================================
# Test extract_characteristic_patterns function
# ============================================================================
class TestExtractCharacteristicPatterns:
    """Test pattern extraction from clustering."""

    def test_basic_pattern_extraction(self):
        """Test basic pattern extraction."""
        from strepsuis_amrvirkm.cluster_analysis_core import (
            perform_kmodes, extract_characteristic_patterns
        )
        
        data = pd.DataFrame({
            'A': [1, 1, 1, 0, 0, 0],
            'B': [1, 1, 0, 0, 0, 1],
            'C': [0, 0, 1, 1, 1, 0],
        })
        
        model, clusters = perform_kmodes(data, n_clusters=2)
        patterns = extract_characteristic_patterns(model, data)
        
        assert isinstance(patterns, dict)
        # Should have at least one cluster with patterns
        assert len(patterns) > 0


# ============================================================================
# Test compute_phi function
# ============================================================================
class TestComputePhi:
    """Test phi coefficient computation."""

    def test_perfect_positive_association(self):
        """Test phi = 1 for perfect positive association."""
        from strepsuis_amrvirkm.cluster_analysis_core import compute_phi
        
        x = np.array([1, 1, 0, 0])
        y = np.array([1, 1, 0, 0])  # Same as x
        
        phi = compute_phi(x, y)
        np.testing.assert_almost_equal(phi, 1.0, decimal=5)

    def test_perfect_negative_association(self):
        """Test phi = -1 for perfect negative association."""
        from strepsuis_amrvirkm.cluster_analysis_core import compute_phi
        
        x = np.array([1, 1, 0, 0])
        y = np.array([0, 0, 1, 1])  # Opposite of x
        
        phi = compute_phi(x, y)
        np.testing.assert_almost_equal(phi, -1.0, decimal=5)

    def test_independence(self):
        """Test phi ≈ 0 for independence."""
        from strepsuis_amrvirkm.cluster_analysis_core import compute_phi
        
        x = np.array([1, 0, 1, 0])
        y = np.array([1, 1, 0, 0])
        
        phi = compute_phi(x, y)
        np.testing.assert_almost_equal(phi, 0.0, decimal=5)

    def test_zero_denominator_returns_nan(self):
        """Test returns NaN when denominator is zero."""
        from strepsuis_amrvirkm.cluster_analysis_core import compute_phi
        
        x = np.array([1, 1, 1, 1])  # All ones
        y = np.array([0, 0, 0, 0])  # All zeros
        
        phi = compute_phi(x, y)
        assert np.isnan(phi)


# ============================================================================
# Test phi_correlation_matrix function
# ============================================================================
class TestPhiCorrelationMatrix:
    """Test phi correlation matrix computation."""

    def test_basic_correlation_matrix(self):
        """Test basic phi correlation matrix."""
        from strepsuis_amrvirkm.cluster_analysis_core import phi_correlation_matrix
        
        df = pd.DataFrame({
            'A': [1, 1, 0, 0],
            'B': [1, 1, 0, 0],  # Same as A
            'C': [0, 0, 1, 1],  # Opposite of A
        })
        
        corr = phi_correlation_matrix(df)
        
        # Should be square matrix
        assert corr.shape == (3, 3)
        
        # Diagonal should be 1.0 (self-correlation)
        for col in corr.columns:
            np.testing.assert_almost_equal(corr.loc[col, col], 1.0, decimal=3)
        
        # A and B should be highly correlated
        assert corr.loc['A', 'B'] > 0.9
        
        # A and C should be negatively correlated
        assert corr.loc['A', 'C'] < -0.9


# ============================================================================
# Test chi_square_analysis function
# ============================================================================
class TestChiSquareAnalysis:
    """Test chi-square analysis function."""

    def test_basic_chi_square_analysis(self):
        """Test basic chi-square analysis."""
        from strepsuis_amrvirkm.cluster_analysis_core import chi_square_analysis
        
        data = pd.DataFrame({
            'A': [1, 1, 1, 0, 0, 0, 1, 0],
            'B': [1, 1, 0, 0, 0, 1, 1, 0],
        })
        clusters = np.array([1, 1, 1, 1, 2, 2, 2, 2])
        
        global_results, cluster_results = chi_square_analysis(data, clusters)
        
        # Should have results for each feature
        assert isinstance(global_results, pd.DataFrame)
        assert isinstance(cluster_results, pd.DataFrame)


# ============================================================================
# Test log_odds_ratio_analysis function
# ============================================================================
class TestLogOddsRatioAnalysis:
    """Test log-odds ratio analysis function."""

    def test_basic_log_odds(self):
        """Test basic log-odds calculation."""
        from strepsuis_amrvirkm.cluster_analysis_core import log_odds_ratio_analysis
        
        data = pd.DataFrame({
            'A': [1, 1, 1, 0, 0, 0, 1, 0],
            'B': [1, 1, 0, 0, 0, 1, 1, 0],
        })
        clusters = np.array([1, 1, 1, 1, 2, 2, 2, 2])
        
        global_lo, cluster_lo = log_odds_ratio_analysis(
            data, clusters, with_bootstrap_ci=True, n_bootstrap=100
        )
        
        assert isinstance(global_lo, pd.DataFrame)
        assert isinstance(cluster_lo, pd.DataFrame)
        
        # Should have Log_Odds_Ratio column
        assert 'Log_Odds_Ratio' in cluster_lo.columns


# ============================================================================
# Test calculate_cluster_stats function
# ============================================================================
class TestCalculateClusterStats:
    """Test cluster statistics calculation."""

    def test_basic_cluster_stats(self):
        """Test basic cluster statistics."""
        from strepsuis_amrvirkm.cluster_analysis_core import calculate_cluster_stats
        
        clusters = np.array([1, 1, 1, 2, 2])
        stats = calculate_cluster_stats(clusters)
        
        assert 'Count' in stats.columns
        assert 'Percentage' in stats.columns
        
        # Should have correct counts
        assert stats.loc[1, 'Count'] == 3
        assert stats.loc[2, 'Count'] == 2


# ============================================================================
# Test validate_clusters function
# ============================================================================
class TestValidateClusters:
    """Test cluster validation metrics."""

    def test_basic_validation(self):
        """Test basic cluster validation."""
        from strepsuis_amrvirkm.cluster_analysis_core import validate_clusters
        
        np.random.seed(42)
        data = pd.DataFrame({
            'A': [1, 1, 1, 0, 0, 0],
            'B': [1, 1, 0, 0, 0, 1],
        })
        clusters = np.array([1, 1, 1, 2, 2, 2])
        
        ch_score, db_score = validate_clusters(data, clusters)
        
        # Scores should be numeric (may be nan for degenerate cases)
        assert isinstance(ch_score, (float, int)) or np.isnan(ch_score)
        assert isinstance(db_score, (float, int)) or np.isnan(db_score)


# ============================================================================
# Test label_shared_unique_features function
# ============================================================================
class TestLabelSharedUniqueFeatures:
    """Test shared/unique feature identification."""

    def test_basic_shared_unique(self):
        """Test identifying shared and unique features."""
        from strepsuis_amrvirkm.cluster_analysis_core import label_shared_unique_features
        
        data = pd.DataFrame({
            'shared': [1, 1, 1, 1, 1, 1],  # Present in both clusters
            'unique1': [1, 1, 1, 0, 0, 0],  # Only in cluster 1
            'unique2': [0, 0, 0, 1, 1, 1],  # Only in cluster 2
        })
        clusters = np.array([1, 1, 1, 2, 2, 2])
        
        shared_df, unique_df, cluster_sets = label_shared_unique_features(data, clusters)
        
        assert isinstance(shared_df, pd.DataFrame)
        assert isinstance(unique_df, pd.DataFrame)
        assert isinstance(cluster_sets, dict)


# ============================================================================
# Test pairwise_fdr_post_hoc function
# ============================================================================
class TestPairwiseFdrPostHoc:
    """Test pairwise FDR post-hoc analysis."""

    def test_basic_pairwise_fdr(self):
        """Test basic pairwise FDR analysis."""
        from strepsuis_amrvirkm.cluster_analysis_core import pairwise_fdr_post_hoc
        
        np.random.seed(42)
        data = pd.DataFrame({
            'A': [1, 1, 1, 1, 0, 0, 0, 0],
            'B': [1, 1, 0, 0, 0, 0, 1, 1],
        })
        clusters = np.array([1, 1, 1, 1, 2, 2, 2, 2])
        
        result = pairwise_fdr_post_hoc(data, clusters, "test")
        
        assert isinstance(result, pd.DataFrame)

    def test_single_cluster_returns_empty(self):
        """Test that single cluster returns empty DataFrame."""
        from strepsuis_amrvirkm.cluster_analysis_core import pairwise_fdr_post_hoc
        
        data = pd.DataFrame({
            'A': [1, 1, 0, 0],
        })
        clusters = np.array([1, 1, 1, 1])  # Single cluster
        
        result = pairwise_fdr_post_hoc(data, clusters, "test")
        
        assert len(result) == 0


# ============================================================================
# Test association_rule_mining function
# ============================================================================
class TestAssociationRuleMining:
    """Test association rule mining function."""

    def test_basic_association_rules(self):
        """Test basic association rule mining."""
        from strepsuis_amrvirkm.cluster_analysis_core import association_rule_mining
        
        np.random.seed(42)
        data = pd.DataFrame({
            'A': [1] * 40 + [0] * 10,
            'B': [1] * 38 + [0] * 12,
            'C': [1] * 35 + [0] * 15,
        })
        clusters = np.array([1] * 25 + [2] * 25)
        
        result = association_rule_mining(data, clusters, min_support=0.3, min_confidence=0.7)
        
        assert isinstance(result, pd.DataFrame)

    def test_empty_cluster_data(self):
        """Test with cluster that has no data."""
        from strepsuis_amrvirkm.cluster_analysis_core import association_rule_mining
        
        data = pd.DataFrame({'A': [1, 0]})
        clusters = np.array([1, 1])
        
        result = association_rule_mining(data, clusters)
        assert isinstance(result, pd.DataFrame)


# ============================================================================
# Test multiple_correspondence_analysis function
# ============================================================================
class TestMCA:
    """Test MCA (Multiple Correspondence Analysis)."""

    def test_basic_mca(self):
        """Test basic MCA analysis."""
        from strepsuis_amrvirkm.cluster_analysis_core import multiple_correspondence_analysis
        
        np.random.seed(42)
        data = pd.DataFrame({
            'A': [1, 1, 0, 0, 1, 0, 1, 0],
            'B': [1, 0, 1, 0, 1, 0, 1, 0],
            'C': [0, 1, 1, 0, 0, 1, 1, 0],
        })
        clusters = np.array([1, 1, 1, 1, 2, 2, 2, 2])
        
        row_coords, mca_plot_html, heatmap_html = multiple_correspondence_analysis(
            data, clusters, "test"
        )
        
        # Should return DataFrame with coordinates
        if not row_coords.empty:
            assert 'Component_1' in row_coords.columns
            assert 'Component_2' in row_coords.columns


# ============================================================================
# Test logistic_regression_feature_selection function
# ============================================================================
class TestLogisticRegressionFeatureSelection:
    """Test logistic regression for feature selection."""

    def test_basic_logistic_regression(self):
        """Test basic logistic regression feature selection."""
        from strepsuis_amrvirkm.cluster_analysis_core import logistic_regression_feature_selection
        
        np.random.seed(42)
        data = pd.DataFrame({
            'A': [1, 1, 1, 1, 0, 0, 0, 0],
            'B': [1, 1, 0, 0, 0, 0, 1, 1],
            'C': [0, 0, 1, 1, 1, 1, 0, 0],
        })
        clusters = np.array([1, 1, 1, 1, 2, 2, 2, 2])
        
        result = logistic_regression_feature_selection(
            data, clusters, with_ci=True, n_bootstrap=20
        )
        
        assert isinstance(result, pd.DataFrame)
        assert 'Feature' in result.columns
        assert 'Coefficient' in result.columns


# ============================================================================
# Test analyze_cluster_importance function (Random Forest)
# ============================================================================
class TestAnalyzeClusterImportance:
    """Test Random Forest cluster importance analysis."""

    def test_basic_rf_importance(self):
        """Test basic Random Forest importance."""
        from strepsuis_amrvirkm.cluster_analysis_core import analyze_cluster_importance
        
        np.random.seed(42)
        data = pd.DataFrame({
            'A': [1, 1, 1, 1, 0, 0, 0, 0],
            'B': [1, 1, 0, 0, 0, 0, 1, 1],
        })
        clusters = np.array([1, 1, 1, 1, 2, 2, 2, 2])
        
        result = analyze_cluster_importance(data, clusters)
        
        assert isinstance(result, pd.DataFrame)
        assert 'Feature' in result.columns
        assert 'Importance' in result.columns


# ============================================================================
# Test patterns_to_dataframe function
# ============================================================================
class TestPatternsToDataframe:
    """Test pattern to DataFrame conversion."""

    def test_basic_patterns_to_df(self):
        """Test basic patterns to DataFrame conversion."""
        from strepsuis_amrvirkm.cluster_analysis_core import (
            perform_kmodes, extract_characteristic_patterns, patterns_to_dataframe
        )
        
        data = pd.DataFrame({
            'A': [1, 1, 1, 0, 0, 0],
            'B': [1, 1, 0, 0, 0, 1],
        })
        
        model, clusters = perform_kmodes(data, n_clusters=2)
        patterns = extract_characteristic_patterns(model, data)
        
        if patterns:  # Only test if patterns found
            result = patterns_to_dataframe(patterns, "test", data, clusters)
            
            assert isinstance(result, pd.DataFrame)
            assert 'Cluster' in result.columns
            assert 'Size' in result.columns


# ============================================================================
# Test format_association_rules function
# ============================================================================
class TestFormatAssociationRules:
    """Test association rules formatting."""

    def test_format_rules(self):
        """Test formatting association rules."""
        from strepsuis_amrvirkm.cluster_analysis_core import format_association_rules
        
        df = pd.DataFrame({
            'antecedent': [frozenset(['A', 'B']), frozenset(['C'])],
            'consequent': [frozenset(['C']), frozenset(['A', 'B'])],
        })
        
        result = format_association_rules(df)
        
        # Should convert frozensets to sorted comma-separated strings
        assert isinstance(result['antecedent'].iloc[0], str)
        assert isinstance(result['consequent'].iloc[0], str)


# ============================================================================
# Test print_memory_usage function
# ============================================================================
class TestPrintMemoryUsage:
    """Test memory usage printing function."""

    def test_print_memory_usage_runs(self):
        """Test that print_memory_usage runs without error."""
        from strepsuis_amrvirkm.cluster_analysis_core import print_memory_usage
        
        # Should not raise any exception
        print_memory_usage()


# ============================================================================
# Test save_rounded_csv function
# ============================================================================
class TestSaveRoundedCsv:
    """Test CSV saving with rounding."""

    def test_save_rounded_csv(self, tmp_path):
        """Test saving CSV with rounded values."""
        from strepsuis_amrvirkm.cluster_analysis_core import save_rounded_csv
        
        df = pd.DataFrame({
            'A': [1.123456, 2.987654],
            'B': [3.111111, 4.999999],
        })
        
        filepath = tmp_path / "test.csv"
        save_rounded_csv(df, str(filepath))
        
        # Read back and verify rounding
        result = pd.read_csv(filepath)
        assert result['A'].iloc[0] == 1.12
        assert result['B'].iloc[1] == 5.0


# ============================================================================
# Integration tests
# ============================================================================
class TestIntegration:
    """Integration tests for combined functionality."""

    def test_full_analysis_pipeline(self):
        """Test a simplified full analysis pipeline."""
        from strepsuis_amrvirkm.cluster_analysis_core import (
            validate_binary_data,
            perform_kmodes,
            calculate_cluster_stats,
            chi_square_analysis,
            validate_clusters,
        )
        
        np.random.seed(42)
        n = 20
        data = pd.DataFrame({
            'MIC_A': np.random.binomial(1, 0.6, n),
            'MIC_B': np.random.binomial(1, 0.5, n),
            'AMR_C': np.random.binomial(1, 0.4, n),
            'VIR_D': np.random.binomial(1, 0.3, n),
        })
        
        # Step 1: Validate binary data
        validate_binary_data(data)
        
        # Step 2: Perform clustering
        model, clusters = perform_kmodes(data, n_clusters=2)
        assert len(clusters) == n
        
        # Step 3: Calculate cluster stats
        stats = calculate_cluster_stats(clusters)
        assert stats['Count'].sum() == n
        
        # Step 4: Chi-square analysis
        global_chi2, cluster_chi2 = chi_square_analysis(data, clusters)
        assert isinstance(global_chi2, pd.DataFrame)
        
        # Step 5: Validate clusters
        ch_score, db_score = validate_clusters(data, clusters)
        # Scores may be nan for small datasets
        assert isinstance(ch_score, (float, np.floating)) or np.isnan(ch_score)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
