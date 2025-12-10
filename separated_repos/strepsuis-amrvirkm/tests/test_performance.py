"""Performance tests for strepsuis-amrvirkm module.

These tests measure and verify timing benchmarks for key operations.
"""

import time

import numpy as np
import pandas as pd
import pytest


@pytest.mark.performance
class TestClusteringPerformance:
    """Performance tests for clustering operations."""

    def test_hamming_distance_timing(self):
        """Test Hamming distance calculation performance."""
        from scipy.spatial.distance import pdist
        
        np.random.seed(42)
        n_samples = 500
        n_features = 50
        
        data = np.random.randint(0, 2, size=(n_samples, n_features))
        
        start = time.time()
        distances = pdist(data, metric='hamming')
        elapsed = time.time() - start
        
        expected_pairs = n_samples * (n_samples - 1) // 2
        assert len(distances) == expected_pairs
        assert elapsed < 1.0

    def test_silhouette_timing(self):
        """Test silhouette score calculation performance."""
        from sklearn.metrics import silhouette_score
        
        np.random.seed(42)
        n_samples = 200
        n_features = 30
        k = 5
        
        data = np.random.randint(0, 2, size=(n_samples, n_features))
        labels = np.random.randint(0, k, size=n_samples)
        
        start = time.time()
        score = silhouette_score(data, labels, metric='hamming')
        elapsed = time.time() - start
        
        assert -1 <= score <= 1
        assert elapsed < 2.0


@pytest.mark.performance
class TestMCAPerformance:
    """Performance tests for MCA operations."""

    def test_svd_timing(self):
        """Test SVD decomposition performance."""
        np.random.seed(42)
        n_samples = 500
        n_features = 100
        
        data = np.random.random((n_samples, n_features))
        
        start = time.time()
        u, s, vt = np.linalg.svd(data, full_matrices=False)
        elapsed = time.time() - start
        
        assert u.shape == (n_samples, min(n_samples, n_features))
        assert elapsed < 1.0

    def test_indicator_matrix_timing(self):
        """Test indicator matrix creation performance."""
        np.random.seed(42)
        n_samples = 1000
        n_features = 50
        
        data = np.random.randint(0, 2, size=(n_samples, n_features))
        df = pd.DataFrame(data)
        
        start = time.time()
        # One-hot encoding simulation
        indicators = pd.get_dummies(df.astype(str))
        elapsed = time.time() - start
        
        assert elapsed < 2.0
        assert indicators.shape[0] == n_samples


@pytest.mark.performance
class TestPhiMatrixPerformance:
    """Performance tests for phi correlation matrix."""

    def test_phi_matrix_small(self):
        """Test phi matrix for small feature set."""
        np.random.seed(42)
        n_samples = 200
        n_features = 20
        
        data = np.random.randint(0, 2, size=(n_samples, n_features))
        
        start = time.time()
        # Compute pairwise phi coefficients
        n_pairs = n_features * (n_features - 1) // 2
        for i in range(n_features):
            for j in range(i+1, n_features):
                # Count contingency
                a = np.sum((data[:, i] == 1) & (data[:, j] == 1))
                b = np.sum((data[:, i] == 1) & (data[:, j] == 0))
                c = np.sum((data[:, i] == 0) & (data[:, j] == 1))
                d = np.sum((data[:, i] == 0) & (data[:, j] == 0))
        elapsed = time.time() - start
        
        assert elapsed < 1.0

    def test_numpy_correlation_timing(self):
        """Test numpy correlation matrix performance."""
        np.random.seed(42)
        n_samples = 500
        n_features = 50
        
        data = np.random.randint(0, 2, size=(n_samples, n_features)).astype(float)
        
        start = time.time()
        corr = np.corrcoef(data.T)
        elapsed = time.time() - start
        
        assert corr.shape == (n_features, n_features)
        assert elapsed < 0.5


@pytest.mark.performance
class TestDataProcessingPerformance:
    """Performance tests for data processing."""

    def test_dataframe_groupby_timing(self):
        """Test DataFrame groupby performance."""
        np.random.seed(42)
        n_samples = 1000
        n_features = 30
        k = 5
        
        data = np.random.randint(0, 2, size=(n_samples, n_features))
        df = pd.DataFrame(data)
        df['cluster'] = np.random.randint(0, k, size=n_samples)
        
        start = time.time()
        cluster_means = df.groupby('cluster').mean()
        elapsed = time.time() - start
        
        assert cluster_means.shape[0] == k
        assert elapsed < 0.5

    def test_value_counts_timing(self):
        """Test value counting performance."""
        np.random.seed(42)
        n_samples = 10000
        k = 10
        
        labels = np.random.randint(0, k, size=n_samples)
        series = pd.Series(labels)
        
        start = time.time()
        counts = series.value_counts()
        elapsed = time.time() - start
        
        assert sum(counts) == n_samples
        assert elapsed < 0.1
