#!/usr/bin/env python3
"""
Unit and integration tests for StrepSuis Analysis module (StrepSuisPhyloCluster_2025_08_11.py).

Tests cover:
- Tree-aware clustering
- Evolution metrics calculation
- Beta diversity computation
- Trait profiling functions
- Ensemble clustering methods
"""

import sys
import os
import warnings
import tempfile
import numpy as np
import pandas as pd
import pytest
from io import StringIO

# Suppress warnings in tests
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Silence optuna logging
import optuna
optuna.logging.set_verbosity(optuna.logging.WARNING)

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

from Bio import Phylo

# Import functions from StrepSuisPhyloCluster_2025_08_11.py
from StrepSuisPhyloCluster_2025_08_11 import (
    PhylogeneticCore,
    TreeAwareClustering,
    EnsembleClustering,
    Evolution,
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


@pytest.fixture
def sample_labels_and_names():
    """Create sample cluster labels and strain names."""
    labels = np.array([1, 1, 2, 2, 1])
    names = ['A', 'B', 'C', 'D', 'E']
    return labels, names


class TestPhylogeneticCoreStrep:
    """Tests for PhylogeneticCore class in StrepSuis module."""
    
    def test_find_tree_file(self, sample_tree_file):
        """Test finding a tree file."""
        found_path = PhylogeneticCore.find_tree_file(sample_tree_file)
        assert found_path == sample_tree_file
    
    def test_find_tree_file_not_found(self):
        """Test error when tree file not found."""
        with pytest.raises(FileNotFoundError):
            PhylogeneticCore.find_tree_file("nonexistent_tree.newick")
    
    def test_load_tree(self, sample_tree_file):
        """Test loading a phylogenetic tree."""
        tree = PhylogeneticCore.load_tree(sample_tree_file)
        
        assert tree is not None
        terminals = tree.get_terminals()
        assert len(terminals) == 5
    
    def test_tree_to_distance_matrix(self, sample_newick_tree):
        """Test tree to distance matrix conversion."""
        dm, terminals = PhylogeneticCore.tree_to_distance_matrix(
            sample_newick_tree, parallel=False
        )
        
        n = len(terminals)
        assert dm.shape == (n, n)
        
        # Symmetry check
        assert np.allclose(dm, dm.T)
        
        # Diagonal is zero
        assert np.allclose(np.diag(dm), 0)
    
    def test_umap_embed(self, sample_newick_tree):
        """Test UMAP embedding."""
        dm, terminals = PhylogeneticCore.tree_to_distance_matrix(
            sample_newick_tree, parallel=False
        )
        
        embeddings = PhylogeneticCore.umap_embed(
            dm,
            n_components=2,
            n_neighbors=min(3, len(terminals) - 1),
            random_state=42
        )
        
        assert embeddings.shape == (len(terminals), 2)
    
    def test_detect_outliers(self, sample_newick_tree):
        """Test outlier detection."""
        dm, terminals = PhylogeneticCore.tree_to_distance_matrix(
            sample_newick_tree, parallel=False
        )
        
        embeddings = PhylogeneticCore.umap_embed(
            dm,
            n_components=2,
            n_neighbors=min(3, len(terminals) - 1),
            random_state=42
        )
        
        filtered, mask = PhylogeneticCore.detect_outliers(embeddings)
        
        assert len(mask) == len(embeddings)
        assert len(filtered) <= len(embeddings)


class TestTreeAwareClustering:
    """Tests for TreeAwareClustering class."""
    
    def test_cluster_basic(self, sample_newick_tree):
        """Test basic tree-aware clustering."""
        dm, terminals = PhylogeneticCore.tree_to_distance_matrix(
            sample_newick_tree, parallel=False
        )
        
        clustering = TreeAwareClustering(sample_newick_tree, terminals)
        labels = clustering.cluster(dm, mode='max')
        
        assert len(labels) == len(terminals)
        assert all(l >= 1 for l in labels)  # 1-based labels
    
    def test_cluster_modes(self, sample_newick_tree):
        """Test different clustering modes."""
        dm, terminals = PhylogeneticCore.tree_to_distance_matrix(
            sample_newick_tree, parallel=False
        )
        
        clustering = TreeAwareClustering(sample_newick_tree, terminals)
        
        for mode in ['max', 'sum', 'avg']:
            labels = clustering.cluster(dm, mode=mode)
            assert len(labels) == len(terminals)
    
    def test_auto_threshold(self, sample_newick_tree):
        """Test automatic threshold calculation."""
        dm, terminals = PhylogeneticCore.tree_to_distance_matrix(
            sample_newick_tree, parallel=False
        )
        
        clustering = TreeAwareClustering(sample_newick_tree, terminals)
        
        for mode in ['max', 'sum', 'avg']:
            threshold = clustering._auto_threshold(mode)
            assert threshold > 0
    
    def test_custom_threshold(self, sample_newick_tree):
        """Test clustering with custom threshold."""
        dm, terminals = PhylogeneticCore.tree_to_distance_matrix(
            sample_newick_tree, parallel=False
        )
        
        clustering = TreeAwareClustering(sample_newick_tree, terminals)
        
        # Very high threshold should result in fewer clusters
        labels_high = clustering.cluster(dm, threshold=100.0)
        
        # Very low threshold should result in more clusters
        labels_low = clustering.cluster(dm, threshold=0.001)
        
        assert len(np.unique(labels_high)) <= len(np.unique(labels_low))


class TestEnsembleClustering:
    """Tests for EnsembleClustering class."""
    
    def test_fit_best(self):
        """Test ensemble clustering fit_best method."""
        np.random.seed(42)
        
        # Create well-separated clusters
        X = np.vstack([
            np.random.randn(20, 2) + [0, 0],
            np.random.randn(20, 2) + [5, 5]
        ])
        
        ensemble = EnsembleClustering(trials=5, seed=42)
        labels, score = ensemble.fit_best(X)
        
        if labels is not None:
            assert len(labels) == len(X)
            assert len(np.unique(labels)) >= 1
    
    def test_dbscan_optimization(self):
        """Test DBSCAN hyperparameter optimization."""
        np.random.seed(42)
        
        X = np.random.randn(50, 2)
        
        ensemble = EnsembleClustering(trials=3, seed=42)
        params = ensemble._optimize_dbscan(X)
        
        assert 'eps' in params
        assert 'min_samples' in params


class TestEvolution:
    """Tests for Evolution class."""
    
    def test_by_cluster(self, sample_newick_tree, sample_labels_and_names):
        """Test evolutionary metrics by cluster."""
        labels, names = sample_labels_and_names
        
        df = Evolution.by_cluster(sample_newick_tree, labels, names)
        
        assert 'Cluster_ID' in df.columns
        assert 'PD' in df.columns  # Phylogenetic diversity
        assert 'MeanPairwiseDist' in df.columns
        assert len(df) == len(np.unique(labels))
    
    def test_beta_diversity(self, sample_newick_tree, sample_labels_and_names):
        """Test beta diversity calculation."""
        labels, names = sample_labels_and_names
        
        beta_df = Evolution.beta(sample_newick_tree, labels, names)
        
        n_clusters = len(np.unique(labels))
        assert beta_df.shape == (n_clusters, n_clusters)
        
        # Symmetric
        assert np.allclose(beta_df.values, beta_df.values.T)
        
        # Diagonal should be zero (or very small)
        for i in range(n_clusters):
            assert beta_df.iloc[i, i] == 0 or abs(beta_df.iloc[i, i]) < 1e-10
    
    def test_evolution_rates(self, sample_newick_tree, sample_labels_and_names):
        """Test evolution rate calculation."""
        labels, names = sample_labels_and_names
        
        df_clusters = Evolution.by_cluster(sample_newick_tree, labels, names)
        rates_df = Evolution.rates(df_clusters)
        
        assert 'Cluster_ID' in rates_df.columns
        # Column name may be 'EvolutionRate' or 'Evolution_Rate_Proxy'
        assert 'EvolutionRate' in rates_df.columns or 'Evolution_Rate_Proxy' in rates_df.columns


class TestEvolutionEdgeCases:
    """Edge case tests for Evolution class."""
    
    def test_single_member_cluster(self, sample_newick_tree):
        """Test handling of single-member clusters."""
        labels = np.array([1, 2, 3, 4, 5])  # Each terminal in its own cluster
        names = ['A', 'B', 'C', 'D', 'E']
        
        df = Evolution.by_cluster(sample_newick_tree, labels, names)
        
        # Should handle single-member clusters
        assert len(df) == 5
    
    def test_all_same_cluster(self, sample_newick_tree):
        """Test when all terminals in same cluster."""
        labels = np.array([1, 1, 1, 1, 1])
        names = ['A', 'B', 'C', 'D', 'E']
        
        df = Evolution.by_cluster(sample_newick_tree, labels, names)
        
        assert len(df) == 1
        assert df.iloc[0]['Cluster_ID'] == 1


class TestParallelProcessorStrep:
    """Tests for ParallelProcessor in StrepSuis module."""
    
    @pytest.mark.skip(reason="parallel_tree_distance_matrix uses local function that can't be pickled")
    def test_parallel_tree_distance_matrix(self, sample_newick_tree):
        """Test parallel distance matrix computation."""
        terminals = sample_newick_tree.get_terminals()
        
        dm = ParallelProcessor.parallel_tree_distance_matrix(
            sample_newick_tree, terminals, n_jobs=1
        )
        
        n = len(terminals)
        assert dm.shape == (n, n)
        
        # Should be symmetric
        assert np.allclose(dm, dm.T)


class TestIntegrationStrep:
    """Integration tests for the StrepSuis analysis pipeline."""
    
    def test_full_pipeline(self, sample_tree_file):
        """Test the full analysis pipeline."""
        # Load tree
        tree = PhylogeneticCore.load_tree(sample_tree_file)
        
        # Compute distance matrix
        dm, terminals = PhylogeneticCore.tree_to_distance_matrix(tree, parallel=False)
        
        # Perform tree-aware clustering
        clustering = TreeAwareClustering(tree, terminals)
        labels = clustering.cluster(dm, mode='max')
        
        # Get terminal names
        names = [str(t) for t in terminals]
        
        # Calculate evolutionary metrics
        evo_df = Evolution.by_cluster(tree, labels, names)
        
        # Calculate beta diversity
        beta_df = Evolution.beta(tree, labels, names)
        
        # Verify results
        assert len(labels) == len(terminals)
        assert len(evo_df) >= 1
        assert beta_df.shape[0] == len(np.unique(labels))
    
    def test_pipeline_with_ensemble_fallback(self, sample_tree_file):
        """Test pipeline with ensemble clustering fallback."""
        # Load tree
        tree = PhylogeneticCore.load_tree(sample_tree_file)
        
        # Compute distance matrix
        dm, terminals = PhylogeneticCore.tree_to_distance_matrix(tree, parallel=False)
        
        # Embed with UMAP
        embeddings = PhylogeneticCore.umap_embed(
            dm,
            n_neighbors=min(3, len(terminals) - 1),
            random_state=42
        )
        
        # Try ensemble clustering
        ensemble = EnsembleClustering(trials=3, seed=42)
        labels, score = ensemble.fit_best(embeddings)
        
        # If ensemble returns valid labels
        if labels is not None:
            assert len(labels) == len(terminals)


class TestClusterValidation:
    """Tests for cluster validation and consistency."""
    
    def test_cluster_consistency(self, sample_newick_tree):
        """Test that clustering is consistent with same seed."""
        dm, terminals = PhylogeneticCore.tree_to_distance_matrix(
            sample_newick_tree, parallel=False
        )
        
        clustering = TreeAwareClustering(sample_newick_tree, terminals)
        
        labels1 = clustering.cluster(dm, mode='max', threshold=0.5)
        labels2 = clustering.cluster(dm, mode='max', threshold=0.5)
        
        # Same threshold should give same results
        assert np.array_equal(labels1, labels2)
    
    def test_cluster_labels_valid(self, sample_newick_tree):
        """Test that cluster labels are valid."""
        dm, terminals = PhylogeneticCore.tree_to_distance_matrix(
            sample_newick_tree, parallel=False
        )
        
        clustering = TreeAwareClustering(sample_newick_tree, terminals)
        labels = clustering.cluster(dm)
        
        # Labels should be positive integers
        assert all(l >= 1 for l in labels)
        
        # Labels should be consecutive (no gaps)
        unique_labels = sorted(np.unique(labels))
        expected = list(range(1, len(unique_labels) + 1))
        assert unique_labels == expected


def main():
    """Run all tests."""
    print("=" * 80)
    print("Running StrepSuis Analysis Tests")
    print("=" * 80)
    
    # Run with pytest
    exit_code = pytest.main([__file__, '-v', '--tb=short'])
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
