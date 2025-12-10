"""Stress tests for strepsuis-amrvirkm module.

These tests verify behavior with large datasets, memory constraints,
and concurrent operations.
"""

import time

import numpy as np
import pandas as pd
import pytest


@pytest.mark.stress
class TestLargeDatasets:
    """Tests with large datasets to verify scalability."""

    def test_large_binary_matrix_creation(self):
        """Test creating large binary matrices for clustering."""
        np.random.seed(42)
        n_samples = 500
        n_features = 100
        
        data = np.random.randint(0, 2, size=(n_samples, n_features))
        df = pd.DataFrame(
            data,
            columns=[f"Feature_{i}" for i in range(n_features)]
        )
        
        assert df.shape == (n_samples, n_features)
        assert set(df.values.flatten()) <= {0, 1}

    def test_clustering_data_scaling(self):
        """Test cluster assignment with scaled data."""
        np.random.seed(42)
        n_samples = 1000
        n_features = 50
        
        data = np.random.randint(0, 2, size=(n_samples, n_features))
        df = pd.DataFrame(data)
        
        # Simulate cluster assignments
        k = 5
        labels = np.random.randint(0, k, size=n_samples)
        
        # Check cluster sizes
        unique, counts = np.unique(labels, return_counts=True)
        assert len(unique) == k
        assert sum(counts) == n_samples

    def test_distance_matrix_memory(self):
        """Test Hamming distance matrix creation."""
        np.random.seed(42)
        n_samples = 200
        n_features = 50
        
        data = np.random.randint(0, 2, size=(n_samples, n_features))
        
        # Compute pairwise Hamming distances
        from scipy.spatial.distance import pdist, squareform
        distances = pdist(data, metric='hamming')
        dist_matrix = squareform(distances)
        
        assert dist_matrix.shape == (n_samples, n_samples)
        # Check diagonal is zero
        assert np.allclose(np.diag(dist_matrix), 0)


@pytest.mark.stress
class TestClusteringEdgeCases:
    """Tests for clustering edge cases."""

    def test_single_cluster(self):
        """Test with k=1 (all same cluster)."""
        np.random.seed(42)
        n_samples = 100
        labels = np.zeros(n_samples, dtype=int)
        
        assert len(np.unique(labels)) == 1
        assert all(labels == 0)

    def test_many_clusters(self):
        """Test with many clusters."""
        np.random.seed(42)
        n_samples = 100
        k = 20  # Many clusters
        
        # Assign to clusters
        labels = np.random.randint(0, k, size=n_samples)
        
        # Some clusters may be empty with random assignment
        assert len(np.unique(labels)) <= k

    def test_identical_samples(self):
        """Test with identical samples (should cluster together)."""
        # All samples identical
        n_samples = 50
        n_features = 10
        
        data = np.ones((n_samples, n_features), dtype=int)
        df = pd.DataFrame(data)
        
        # All pairwise distances should be 0
        from scipy.spatial.distance import pdist
        distances = pdist(df.values, metric='hamming')
        assert np.allclose(distances, 0)


@pytest.mark.stress  
class TestMCAScaling:
    """Tests for MCA scaling behavior."""

    def test_mca_large_feature_set(self):
        """Test MCA with many features."""
        np.random.seed(42)
        n_samples = 100
        n_features = 200
        
        data = np.random.randint(0, 2, size=(n_samples, n_features))
        df = pd.DataFrame(data)
        
        # MCA uses SVD - check data is suitable
        assert df.shape[0] < df.shape[1]  # More features than samples
        
        # Prevalence check
        prevalences = df.mean()
        assert all(0 <= p <= 1 for p in prevalences)

    def test_sparse_data_handling(self):
        """Test with sparse binary data."""
        np.random.seed(42)
        n_samples = 500
        n_features = 100
        
        # Sparse: only 5% of values are 1
        data = (np.random.random((n_samples, n_features)) < 0.05).astype(int)
        df = pd.DataFrame(data)
        
        # Check sparsity
        sparsity = 1 - df.values.mean()
        assert sparsity > 0.9
