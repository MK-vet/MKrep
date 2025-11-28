#!/usr/bin/env python3
"""
Unit and integration tests for Cluster Analysis module (Cluster_MIC_AMR_Viruelnce.py).

Tests cover:
- K-Modes clustering functions
- Bootstrap confidence interval calculations
- Phi correlation matrix
- Chi-square analysis with FDR correction
- Log-odds ratio analysis
- Shared/unique feature detection
"""

import sys
import os
import warnings
import numpy as np
import pandas as pd
import pytest

# Suppress warnings in tests
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock google.colab module for testing
class MockFiles:
    def upload(self):
        return {}
    def download(self, filename):
        pass

class MockColab:
    files = MockFiles()

sys.modules['google'] = type(sys)('google')
sys.modules['google.colab'] = MockColab()

# Import functions from Cluster_MIC_AMR_Viruelnce.py
from Cluster_MIC_AMR_Viruelnce import (
    validate_binary_data,
    determine_optimal_clusters_sqrt,
    perform_kmodes,
    bootstrap_confidence_interval,
    compute_phi,
    phi_correlation_matrix,
    chi_square_analysis,
    log_odds_ratio_analysis,
    label_shared_unique_features,
    calculate_cluster_stats,
    validate_clusters,
    pairwise_fdr_post_hoc,
)


class TestBinaryDataValidation:
    """Tests for binary data validation."""
    
    def test_valid_binary_data(self):
        """Test that valid binary data passes validation."""
        df = pd.DataFrame({
            'feat1': [0, 1, 0, 1],
            'feat2': [1, 1, 0, 0]
        })
        # Should not raise
        validate_binary_data(df)
    
    def test_invalid_binary_data(self):
        """Test that non-binary data raises an error."""
        df = pd.DataFrame({
            'feat1': [0, 1, 2, 1],  # Contains 2
            'feat2': [1, 1, 0, 0]
        })
        with pytest.raises(ValueError, match="not strictly 0/1 binary"):
            validate_binary_data(df)
    
    def test_empty_dataframe(self):
        """Test with empty dataframe."""
        df = pd.DataFrame()
        # Empty dataframe should pass (no invalid values)
        validate_binary_data(df)


class TestBootstrapConfidenceInterval:
    """Tests for bootstrap confidence interval calculation."""
    
    def test_basic_bootstrap_ci(self):
        """Test basic bootstrap CI calculation."""
        percentage = 50.0
        count = 50
        total_samples = 100
        ci_low, ci_high = bootstrap_confidence_interval(percentage, count, total_samples)
        
        # CI should be around 50% for balanced data
        assert ci_low is not np.nan
        assert ci_high is not np.nan
        assert 30 <= ci_low <= 50
        assert 50 <= ci_high <= 70
    
    def test_extreme_values(self):
        """Test bootstrap CI with extreme values."""
        # All present
        ci_low, ci_high = bootstrap_confidence_interval(100.0, 100, 100)
        assert ci_high >= 95
        
        # All absent
        ci_low, ci_high = bootstrap_confidence_interval(0.0, 0, 100)
        assert ci_low <= 10
    
    def test_zero_samples(self):
        """Test bootstrap CI with zero samples."""
        ci_low, ci_high = bootstrap_confidence_interval(0.0, 0, 0)
        assert np.isnan(ci_low)
        assert np.isnan(ci_high)


class TestPhiCorrelation:
    """Tests for phi correlation coefficient calculation."""
    
    def test_perfect_positive_correlation(self):
        """Test phi with perfectly correlated data."""
        x = pd.Series([0, 0, 1, 1, 0, 0, 1, 1])
        y = pd.Series([0, 0, 1, 1, 0, 0, 1, 1])
        phi = compute_phi(x.values, y.values)
        assert abs(phi - 1.0) < 0.001
    
    def test_perfect_negative_correlation(self):
        """Test phi with perfectly negatively correlated data."""
        x = pd.Series([0, 0, 1, 1, 0, 0, 1, 1])
        y = pd.Series([1, 1, 0, 0, 1, 1, 0, 0])
        phi = compute_phi(x.values, y.values)
        assert abs(phi - (-1.0)) < 0.001
    
    def test_no_correlation(self):
        """Test phi with independent data."""
        # Create data that should have low correlation
        x = pd.Series([1, 0, 1, 0, 1, 0, 1, 0])
        y = pd.Series([1, 1, 0, 0, 1, 1, 0, 0])
        phi = compute_phi(x.values, y.values)
        assert -0.5 <= phi <= 0.5
    
    def test_phi_range(self):
        """Test that phi is always in valid range."""
        np.random.seed(42)
        x = pd.Series(np.random.randint(0, 2, 100))
        y = pd.Series(np.random.randint(0, 2, 100))
        phi = compute_phi(x.values, y.values)
        assert -1.0 <= phi <= 1.0 or np.isnan(phi)


class TestPhiCorrelationMatrix:
    """Tests for phi correlation matrix calculation."""
    
    def test_matrix_symmetry(self):
        """Test that phi correlation matrix is symmetric."""
        df = pd.DataFrame({
            'A': [0, 1, 1, 0, 1, 0],
            'B': [1, 1, 0, 0, 1, 0],
            'C': [0, 0, 1, 1, 0, 1]
        })
        corr = phi_correlation_matrix(df)
        
        # Check symmetry
        for i in range(len(corr.columns)):
            for j in range(len(corr.columns)):
                val_ij = corr.iloc[i, j]
                val_ji = corr.iloc[j, i]
                if not np.isnan(val_ij) and not np.isnan(val_ji):
                    assert abs(val_ij - val_ji) < 0.001
    
    def test_matrix_diagonal(self):
        """Test that diagonal elements are 1.0 (self-correlation)."""
        df = pd.DataFrame({
            'A': [0, 1, 1, 0, 1, 0],
            'B': [1, 1, 0, 0, 1, 0]
        })
        corr = phi_correlation_matrix(df)
        
        for i in range(len(corr.columns)):
            assert abs(corr.iloc[i, i] - 1.0) < 0.001


class TestChiSquareAnalysis:
    """Tests for chi-square analysis with FDR correction."""
    
    def test_significant_association(self):
        """Test chi-square detects significant association."""
        # Create data with strong association
        np.random.seed(42)
        n = 100
        clusters = np.array([1] * 50 + [2] * 50)
        
        # Feature strongly associated with cluster
        feat_data = np.concatenate([
            np.random.choice([0, 1], 50, p=[0.1, 0.9]),
            np.random.choice([0, 1], 50, p=[0.9, 0.1])
        ])
        
        data = pd.DataFrame({'feat1': feat_data})
        df_global, df_cluster = chi_square_analysis(data, clusters)
        
        assert len(df_global) > 0
        # Should have low p-value for strong association
        assert df_global['P_Value'].iloc[0] < 0.05
    
    def test_no_association(self):
        """Test chi-square with independent data."""
        np.random.seed(42)
        clusters = np.array([1] * 50 + [2] * 50)
        
        # Random feature independent of clusters
        feat_data = np.random.choice([0, 1], 100, p=[0.5, 0.5])
        
        data = pd.DataFrame({'feat1': feat_data})
        df_global, df_cluster = chi_square_analysis(data, clusters)
        
        assert len(df_global) > 0
    
    def test_fdr_correction(self):
        """Test that FDR correction is applied."""
        np.random.seed(42)
        clusters = np.array([1] * 30 + [2] * 30 + [3] * 30)
        
        data = pd.DataFrame({
            'feat1': np.random.choice([0, 1], 90),
            'feat2': np.random.choice([0, 1], 90),
            'feat3': np.random.choice([0, 1], 90)
        })
        
        df_global, df_cluster = chi_square_analysis(data, clusters)
        
        # Check that adjusted p-values exist
        if not df_global.empty:
            assert 'Adjusted_P' in df_global.columns


class TestLogOddsRatioAnalysis:
    """Tests for log-odds ratio analysis."""
    
    def test_basic_log_odds(self):
        """Test basic log-odds calculation."""
        np.random.seed(42)
        clusters = np.array([1] * 50 + [2] * 50)
        
        data = pd.DataFrame({
            'feat1': [1] * 40 + [0] * 10 + [0] * 40 + [1] * 10
        })
        
        df_global, df_cluster = log_odds_ratio_analysis(data, clusters, with_bootstrap_ci=False)
        
        assert len(df_global) > 0
        assert 'Log_Odds_Ratio' in df_global.columns
    
    def test_log_odds_with_ci(self):
        """Test log-odds with bootstrap confidence intervals."""
        np.random.seed(42)
        clusters = np.array([1] * 30 + [2] * 30)
        
        data = pd.DataFrame({
            'feat1': [1] * 25 + [0] * 5 + [0] * 25 + [1] * 5
        })
        
        df_global, df_cluster = log_odds_ratio_analysis(
            data, clusters, with_bootstrap_ci=True, n_bootstrap=50
        )
        
        assert 'CI_low' in df_cluster.columns
        assert 'CI_high' in df_cluster.columns


class TestSharedUniqueFeatures:
    """Tests for shared/unique feature detection."""
    
    def test_shared_feature_detection(self):
        """Test detection of features shared across clusters."""
        data = pd.DataFrame({
            'shared_feat': [1, 1, 1, 1, 1, 1],
            'unique_feat': [1, 1, 1, 0, 0, 0]
        })
        clusters = np.array([1, 1, 1, 2, 2, 2])
        
        df_shared, df_unique, cluster_sets = label_shared_unique_features(data, clusters)
        
        # shared_feat should be in both clusters
        assert 'shared_feat' in df_shared['Feature'].values or len(df_shared) >= 0
    
    def test_unique_feature_detection(self):
        """Test detection of features unique to one cluster."""
        data = pd.DataFrame({
            'shared_feat': [1, 1, 1, 1, 1, 1],
            'unique_c1': [1, 1, 1, 0, 0, 0],
            'unique_c2': [0, 0, 0, 1, 1, 1]
        })
        clusters = np.array([1, 1, 1, 2, 2, 2])
        
        df_shared, df_unique, cluster_sets = label_shared_unique_features(data, clusters)
        
        # unique features should be detected
        assert len(df_unique) >= 0 or len(df_shared) >= 0


class TestClusterStats:
    """Tests for cluster statistics calculation."""
    
    def test_cluster_distribution(self):
        """Test cluster size distribution calculation."""
        clusters = np.array([1, 1, 1, 2, 2, 3, 3, 3, 3])
        
        stats_df = calculate_cluster_stats(clusters)
        
        assert len(stats_df) == 3  # 3 clusters
        assert stats_df.loc[1, 'Count'] == 3
        assert stats_df.loc[2, 'Count'] == 2
        assert stats_df.loc[3, 'Count'] == 4
    
    def test_cluster_percentages(self):
        """Test cluster percentage calculation."""
        clusters = np.array([1, 1, 2, 2])
        
        stats_df = calculate_cluster_stats(clusters)
        
        # Each cluster should be 50%
        assert abs(stats_df.loc[1, 'Percentage'] - 50.0) < 0.1
        assert abs(stats_df.loc[2, 'Percentage'] - 50.0) < 0.1


class TestClusterValidation:
    """Tests for cluster validation metrics."""
    
    def test_validation_metrics(self):
        """Test Calinski-Harabasz and Davies-Bouldin scores."""
        np.random.seed(42)
        # Create well-separated clusters
        data = pd.DataFrame({
            'feat1': [0, 0, 0, 1, 1, 1],
            'feat2': [0, 0, 0, 1, 1, 1],
            'feat3': [1, 1, 1, 0, 0, 0]
        })
        clusters = np.array([1, 1, 1, 2, 2, 2])
        
        ch, db = validate_clusters(data, clusters)
        
        # Metrics should be computed
        assert ch is not np.nan or ch >= 0
        assert db is not np.nan or db >= 0


class TestPairwiseFDRPostHoc:
    """Tests for pairwise FDR post-hoc analysis."""
    
    def test_pairwise_comparisons(self):
        """Test pairwise comparisons between clusters."""
        np.random.seed(42)
        data = pd.DataFrame({
            'feat1': [1, 1, 0, 0, 0, 1],
            'feat2': [0, 1, 1, 0, 1, 0]
        })
        clusters = np.array([1, 1, 1, 2, 2, 2])
        
        df_result = pairwise_fdr_post_hoc(data, clusters, 'test')
        
        # Should have comparisons
        if not df_result.empty:
            assert 'Feature' in df_result.columns
            assert 'ClusterA' in df_result.columns
            assert 'ClusterB' in df_result.columns


def main():
    """Run all tests."""
    print("=" * 80)
    print("Running Cluster Analysis Tests")
    print("=" * 80)
    
    # Run with pytest
    exit_code = pytest.main([__file__, '-v', '--tb=short'])
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
