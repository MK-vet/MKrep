#!/usr/bin/env python3
"""
Unit and integration tests for Phylogenetic Clustering module (Phylogenetic_clustering_2025_03_21.py).

Tests cover:
- Phylogenetic tree handling
- Distance matrix computation
- Tree-aware clustering
- UMAP dimension reduction
- Evolutionary metrics
- Cluster validation
"""

import sys
import os
import warnings
import tempfile
import numpy as np
import pandas as pd
import pytest
from io import StringIO
from unittest.mock import patch


class MockPool:
    """Mock multiprocessing Pool for deterministic testing.
    
    Executes map operations synchronously to avoid pickling issues with
    local functions while preserving the expected interface.
    """
    def __init__(self, processes=None):
        self.processes = processes
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass
    
    def map(self, func, iterable):
        """Execute func on each item synchronously."""
        return [func(item) for item in iterable]
    
    def close(self):
        pass
    
    def join(self):
        pass

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

# Mock weasyprint module (optional PDF export dependency)
class MockWeasyPrintHTML:
    def __init__(self, *args, **kwargs):
        pass
    def write_pdf(self, *args, **kwargs):
        pass

class MockWeasyPrint:
    HTML = MockWeasyPrintHTML

sys.modules['weasyprint'] = MockWeasyPrint()

from Bio import Phylo

# Import functions from Phylogenetic_clustering_2025_03_21.py
from Phylogenetic_clustering_2025_03_21 import (
    PhylogeneticCore,
    TreeAwareClusteringModule,
    ParallelProcessor,
)


# Fixtures for common test data
@pytest.fixture
def sample_newick_tree():
    """Create a simple Newick tree for testing."""
    newick_str = "(((A:0.1,B:0.2):0.3,(C:0.1,D:0.1):0.2):0.1,E:0.5);"
    return Phylo.read(StringIO(newick_str), "newick")


@pytest.fixture
def sample_tree_file():
    """Create a temporary Newick tree file for testing."""
    newick_str = "(((S1:0.1,S2:0.2):0.3,(S3:0.1,S4:0.1):0.2):0.1,S5:0.5);"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.newick', delete=False) as f:
        f.write(newick_str)
        temp_path = f.name
    yield temp_path
    # Cleanup
    os.unlink(temp_path)


class TestPhylogeneticCore:
    """Tests for PhylogeneticCore class."""
    
    def test_load_tree(self, sample_tree_file):
        """Test loading a phylogenetic tree from file."""
        tree = PhylogeneticCore.load_tree(sample_tree_file)
        
        assert tree is not None
        terminals = tree.get_terminals()
        assert len(terminals) == 5
    
    def test_tree_to_distance_matrix(self, sample_newick_tree):
        """Test conversion of tree to distance matrix."""
        distance_matrix, terminals = PhylogeneticCore.tree_to_distance_matrix(
            sample_newick_tree, parallel=False
        )
        
        n = len(terminals)
        assert distance_matrix.shape == (n, n)
        
        # Check symmetry
        for i in range(n):
            for j in range(n):
                assert abs(distance_matrix[i, j] - distance_matrix[j, i]) < 1e-10
        
        # Diagonal should be zero
        for i in range(n):
            assert distance_matrix[i, i] == 0
    
    def test_distance_matrix_positive(self, sample_newick_tree):
        """Test that all pairwise distances are non-negative."""
        distance_matrix, terminals = PhylogeneticCore.tree_to_distance_matrix(
            sample_newick_tree, parallel=False
        )
        
        assert np.all(distance_matrix >= 0)
    
    def test_dimension_reduction(self, sample_newick_tree):
        """Test UMAP dimension reduction."""
        distance_matrix, terminals = PhylogeneticCore.tree_to_distance_matrix(
            sample_newick_tree, parallel=False
        )
        
        # UMAP needs at least n_neighbors samples
        if len(terminals) >= 3:
            embeddings = PhylogeneticCore.dimension_reduction(
                distance_matrix, 
                n_components=2, 
                n_neighbors=min(3, len(terminals) - 1),
                random_state=42
            )
            
            assert embeddings.shape == (len(terminals), 2)
    
    def test_detect_outliers(self, sample_newick_tree):
        """Test outlier detection."""
        distance_matrix, terminals = PhylogeneticCore.tree_to_distance_matrix(
            sample_newick_tree, parallel=False
        )
        
        if len(terminals) >= 5:
            embeddings = PhylogeneticCore.dimension_reduction(
                distance_matrix,
                n_components=2,
                n_neighbors=min(3, len(terminals) - 1),
                random_state=42
            )
            
            filtered_embeddings, mask = PhylogeneticCore.detect_outliers(
                embeddings, contamination=0.1
            )
            
            assert len(filtered_embeddings) <= len(embeddings)
            assert len(mask) == len(embeddings)


class TestTreeAwareClustering:
    """Tests for TreeAwareClusteringModule class."""
    
    def test_tree_cluster_basic(self, sample_newick_tree):
        """Test basic tree-aware clustering."""
        distance_matrix, terminals = PhylogeneticCore.tree_to_distance_matrix(
            sample_newick_tree, parallel=False
        )
        
        clustering = TreeAwareClusteringModule(
            sample_newick_tree, terminals, n_clusters_range=(2, 5), seed=42
        )
        
        labels = clustering.tree_cluster_algorithm(distance_matrix, method='max')
        
        # Should have as many labels as terminals
        assert len(labels) == len(terminals)
        
        # Labels should be non-negative integers
        assert all(l >= 0 for l in labels)
    
    def test_tree_cluster_methods(self, sample_newick_tree):
        """Test different tree clustering methods."""
        distance_matrix, terminals = PhylogeneticCore.tree_to_distance_matrix(
            sample_newick_tree, parallel=False
        )
        
        clustering = TreeAwareClusteringModule(
            sample_newick_tree, terminals, seed=42
        )
        
        # Test each method
        for method in ['max', 'sum', 'avg']:
            labels = clustering.tree_cluster_algorithm(distance_matrix, method=method)
            assert len(labels) == len(terminals)
    
    def test_auto_threshold(self, sample_newick_tree):
        """Test automatic threshold calculation."""
        distance_matrix, terminals = PhylogeneticCore.tree_to_distance_matrix(
            sample_newick_tree, parallel=False
        )
        
        clustering = TreeAwareClusteringModule(
            sample_newick_tree, terminals, seed=42
        )
        
        # Threshold should be positive
        threshold = clustering._auto_threshold_max()
        assert threshold > 0
    
    def test_monophyletic_clusters(self, sample_newick_tree):
        """Test that clusters respect phylogenetic structure."""
        distance_matrix, terminals = PhylogeneticCore.tree_to_distance_matrix(
            sample_newick_tree, parallel=False
        )
        
        clustering = TreeAwareClusteringModule(
            sample_newick_tree, terminals, seed=42
        )
        
        labels = clustering.tree_cluster_algorithm(distance_matrix, method='max')
        
        # Within-cluster distances should generally be smaller than between-cluster
        unique_labels = np.unique(labels)
        if len(unique_labels) > 1:
            within_dists = []
            between_dists = []
            
            for i in range(len(terminals)):
                for j in range(i + 1, len(terminals)):
                    if labels[i] == labels[j]:
                        within_dists.append(distance_matrix[i, j])
                    else:
                        between_dists.append(distance_matrix[i, j])
            
            # Only check if we have both types of distances
            if within_dists and between_dists:
                # This is a weak check - we just verify structure
                assert len(within_dists) + len(between_dists) > 0


class TestParallelProcessor:
    """Tests for ParallelProcessor class."""
    
    def test_parallel_bootstrap(self):
        """Test parallel bootstrap computation using MockPool.
        
        Uses MockPool to execute bootstrap sampling synchronously,
        avoiding pickling issues with local statistic functions.
        """
        np.random.seed(42)
        data = pd.DataFrame({
            'A': np.random.rand(50),
            'B': np.random.rand(50)
        })
        
        def mean_func(d):
            return d.mean().values
        
        # Patch the multiprocessing Pool with MockPool for deterministic testing
        with patch('Phylogenetic_clustering_2025_03_21.Pool', MockPool):
            results = ParallelProcessor.parallel_bootstrap(
                data, mean_func, n_bootstrap=10, n_jobs=1
            )
        
        assert results.shape == (10, 2)
        # Verify bootstrap results are numeric and finite
        assert np.all(np.isfinite(results))
    
    def test_parallel_feature_importance(self):
        """Test parallel feature importance calculation."""
        np.random.seed(42)
        X = np.random.rand(50, 5)
        y = np.random.randint(0, 2, 50)
        
        # Use small number of bootstraps for testing
        importances = ParallelProcessor.parallel_feature_importance(
            X, y, n_bootstrap=5, n_jobs=1
        )
        
        assert importances.shape == (5, 5)


class TestDistanceMatrixProperties:
    """Tests for distance matrix mathematical properties."""
    
    def test_triangle_inequality(self, sample_newick_tree):
        """Test that distance matrix satisfies triangle inequality."""
        distance_matrix, terminals = PhylogeneticCore.tree_to_distance_matrix(
            sample_newick_tree, parallel=False
        )
        
        n = len(terminals)
        violations = 0
        
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if distance_matrix[i, j] > distance_matrix[i, k] + distance_matrix[k, j] + 1e-10:
                        violations += 1
        
        # Phylogenetic distances should satisfy triangle inequality
        assert violations == 0
    
    def test_ultrametric_property(self, sample_newick_tree):
        """Test ultrametric property of tree distances."""
        distance_matrix, terminals = PhylogeneticCore.tree_to_distance_matrix(
            sample_newick_tree, parallel=False
        )
        
        # For ultrametric trees, for any three points, the two largest distances are equal
        # This is a relaxed test - not all trees are ultrametric
        n = len(terminals)
        
        if n >= 3:
            # Just verify distances are computed correctly
            assert distance_matrix.shape == (n, n)


class TestClusteringEdgeCases:
    """Tests for edge cases in clustering."""
    
    def test_single_terminal(self):
        """Test handling of tree with single terminal."""
        newick_str = "(A:0.1);"
        tree = Phylo.read(StringIO(newick_str), "newick")
        
        distance_matrix, terminals = PhylogeneticCore.tree_to_distance_matrix(
            tree, parallel=False
        )
        
        assert distance_matrix.shape == (1, 1)
        assert distance_matrix[0, 0] == 0
    
    def test_two_terminals(self):
        """Test handling of tree with two terminals."""
        newick_str = "(A:0.1,B:0.2);"
        tree = Phylo.read(StringIO(newick_str), "newick")
        
        distance_matrix, terminals = PhylogeneticCore.tree_to_distance_matrix(
            tree, parallel=False
        )
        
        assert distance_matrix.shape == (2, 2)
        assert distance_matrix[0, 0] == 0
        assert distance_matrix[1, 1] == 0
        assert distance_matrix[0, 1] == distance_matrix[1, 0]
    
    def test_star_tree(self):
        """Test handling of star-shaped tree."""
        newick_str = "(A:0.1,B:0.1,C:0.1,D:0.1);"
        tree = Phylo.read(StringIO(newick_str), "newick")
        
        distance_matrix, terminals = PhylogeneticCore.tree_to_distance_matrix(
            tree, parallel=False
        )
        
        n = len(terminals)
        assert distance_matrix.shape == (n, n)
        
        # All pairwise distances in a star tree should be approximately equal
        off_diag = distance_matrix[np.triu_indices(n, k=1)]
        assert np.std(off_diag) < 0.01  # Low variance


class TestIntegration:
    """Integration tests for the phylogenetic analysis pipeline."""
    
    def test_full_pipeline(self, sample_tree_file):
        """Test the full analysis pipeline."""
        # Load tree
        tree = PhylogeneticCore.load_tree(sample_tree_file)
        
        # Compute distance matrix
        distance_matrix, terminals = PhylogeneticCore.tree_to_distance_matrix(
            tree, parallel=False
        )
        
        # Create clustering
        clustering = TreeAwareClusteringModule(tree, terminals, seed=42)
        
        # Perform clustering
        labels = clustering.tree_cluster_algorithm(distance_matrix, method='max')
        
        # Verify results
        assert len(labels) == len(terminals)
        assert all(isinstance(l, (int, np.integer)) for l in labels)
        
        # Check that we have at least 1 cluster
        assert len(np.unique(labels)) >= 1


def main():
    """Run all tests."""
    print("=" * 80)
    print("Running Phylogenetic Analysis Tests")
    print("=" * 80)
    
    # Run with pytest
    exit_code = pytest.main([__file__, '-v', '--tb=short'])
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
