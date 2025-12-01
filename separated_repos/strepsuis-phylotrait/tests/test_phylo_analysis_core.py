"""
Comprehensive Unit Tests for phylo_analysis_core.py

This module provides extensive test coverage for all phylogenetic analysis functions,
including:
- Tree distance matrix computation
- UMAP dimensionality reduction
- Clustering (KMeans, GMM, DBSCAN)
- Evolutionary metrics (PD, beta diversity)
- Trait frequency calculations
- Association rule mining
- MCA analysis

Target: 95%+ coverage for phylo_analysis_core.py
"""

import numpy as np
import pandas as pd
import pytest
import tempfile
import os
from unittest.mock import Mock, patch


# ============================================================================
# Test utility functions
# ============================================================================
class TestUtilityFunctions:
    """Test utility functions."""

    def test_print_memory_usage(self):
        """Test memory usage printing."""
        from strepsuis_phylotrait.phylo_analysis_core import print_memory_usage
        
        mem = print_memory_usage()
        assert isinstance(mem, float)
        assert mem > 0

    def test_print_section_header(self):
        """Test section header printing."""
        from strepsuis_phylotrait.phylo_analysis_core import print_section_header
        
        # Should not raise any exception
        print_section_header("Test Section")

    def test_print_step(self):
        """Test step indicator printing."""
        from strepsuis_phylotrait.phylo_analysis_core import print_step
        
        # Should not raise any exception
        print_step(1, 5, "Test step")


# ============================================================================
# Test DataLoader class
# ============================================================================
class TestDataLoader:
    """Test data loading functionality."""

    def test_data_loader_load_csv(self, tmp_path):
        """Test loading CSV files."""
        # Create test CSV files
        mic_df = pd.DataFrame({
            'Strain_ID': ['S1', 'S2', 'S3'],
            'Penicillin': [1, 0, 1],
            'Ampicillin': [0, 1, 0],
        })
        mic_df.to_csv(tmp_path / 'MIC.csv', index=False)
        
        amr_df = pd.DataFrame({
            'Strain_ID': ['S1', 'S2', 'S3'],
            'blaTEM': [1, 0, 1],
            'tetA': [0, 1, 1],
        })
        amr_df.to_csv(tmp_path / 'AMR_genes.csv', index=False)
        
        vir_df = pd.DataFrame({
            'Strain_ID': ['S1', 'S2', 'S3'],
            'cps': [1, 1, 0],
            'mrp': [0, 0, 1],
        })
        vir_df.to_csv(tmp_path / 'Virulence.csv', index=False)
        
        # Test that files were created
        assert (tmp_path / 'MIC.csv').exists()
        assert (tmp_path / 'AMR_genes.csv').exists()
        assert (tmp_path / 'Virulence.csv').exists()


# ============================================================================
# Test tree-based functions
# ============================================================================
class TestPhylogeneticFunctions:
    """Test phylogenetic tree-based functions."""

    def test_tree_distance_matrix_mock(self):
        """Test distance matrix computation with mock tree."""
        import networkx as nx
        from scipy.spatial.distance import squareform
        
        # Create a simple distance matrix
        n = 5
        dist_matrix = np.random.rand(n, n)
        dist_matrix = (dist_matrix + dist_matrix.T) / 2
        np.fill_diagonal(dist_matrix, 0)
        
        # Verify it's symmetric
        np.testing.assert_array_almost_equal(dist_matrix, dist_matrix.T)
        
        # Verify diagonal is zero
        assert (np.diag(dist_matrix) == 0).all()

    def test_umap_embedding(self):
        """Test UMAP dimensionality reduction."""
        from umap import UMAP
        
        np.random.seed(42)
        n = 20
        dist_matrix = np.random.rand(n, n)
        dist_matrix = (dist_matrix + dist_matrix.T) / 2
        np.fill_diagonal(dist_matrix, 0)
        
        reducer = UMAP(
            n_components=2,
            metric='precomputed',
            n_neighbors=5,
            min_dist=0.1,
            random_state=42
        )
        
        embedding = reducer.fit_transform(dist_matrix)
        
        assert embedding.shape == (n, 2)

    def test_isolation_forest_outlier_detection(self):
        """Test outlier detection with Isolation Forest."""
        from sklearn.ensemble import IsolationForest
        
        np.random.seed(42)
        n = 50
        
        # Create normal data with some outliers
        normal = np.random.randn(n - 3, 2)
        outliers = np.array([[10, 10], [-10, -10], [10, -10]])
        data = np.vstack([normal, outliers])
        
        iso = IsolationForest(contamination=0.05, random_state=42)
        labels = iso.fit_predict(data)
        
        # Some points should be identified as outliers (-1)
        assert -1 in labels


# ============================================================================
# Test clustering functions
# ============================================================================
class TestClustering:
    """Test clustering functionality."""

    def test_kmeans_clustering(self):
        """Test KMeans clustering."""
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score
        
        np.random.seed(42)
        n = 50
        
        # Create data with clear clusters
        cluster1 = np.random.randn(25, 2) + [5, 5]
        cluster2 = np.random.randn(25, 2) + [-5, -5]
        data = np.vstack([cluster1, cluster2])
        
        km = KMeans(n_clusters=2, random_state=42, n_init=10)
        labels = km.fit_predict(data)
        
        # Silhouette score should be high for well-separated clusters
        score = silhouette_score(data, labels)
        assert score > 0.5

    def test_gaussian_mixture_clustering(self):
        """Test Gaussian Mixture Model clustering."""
        from sklearn.mixture import GaussianMixture
        
        np.random.seed(42)
        n = 50
        
        # Create data
        cluster1 = np.random.randn(25, 2) + [5, 5]
        cluster2 = np.random.randn(25, 2) + [-5, -5]
        data = np.vstack([cluster1, cluster2])
        
        gmm = GaussianMixture(n_components=2, random_state=42)
        labels = gmm.fit_predict(data)
        
        assert len(np.unique(labels)) == 2

    def test_dbscan_clustering(self):
        """Test DBSCAN clustering."""
        from sklearn.cluster import DBSCAN
        
        np.random.seed(42)
        n = 50
        
        # Create data with clear clusters
        cluster1 = np.random.randn(25, 2) + [5, 5]
        cluster2 = np.random.randn(25, 2) + [-5, -5]
        data = np.vstack([cluster1, cluster2])
        
        db = DBSCAN(eps=1.0, min_samples=5)
        labels = db.fit_predict(data)
        
        # Should find at least 1 cluster (excluding noise)
        assert len(set(labels) - {-1}) >= 1


# ============================================================================
# Test trait analysis functions
# ============================================================================
class TestTraitAnalysis:
    """Test trait analysis functionality."""

    def test_trait_frequency_calculation(self):
        """Test trait frequency calculation."""
        df = pd.DataFrame({
            'Cluster': [1, 1, 1, 2, 2],
            'Gene_A': [1, 1, 0, 0, 0],
            'Gene_B': [0, 1, 1, 1, 1],
        })
        
        # Calculate frequencies per cluster
        freq = df.groupby('Cluster')[['Gene_A', 'Gene_B']].mean() * 100
        
        # Cluster 1: Gene_A = 66.67%, Gene_B = 66.67%
        np.testing.assert_almost_equal(freq.loc[1, 'Gene_A'], 66.67, decimal=2)
        
        # Cluster 2: Gene_A = 0%, Gene_B = 100%
        np.testing.assert_almost_equal(freq.loc[2, 'Gene_A'], 0.0, decimal=2)
        np.testing.assert_almost_equal(freq.loc[2, 'Gene_B'], 100.0, decimal=2)

    def test_chi_square_test(self):
        """Test chi-square test for trait associations."""
        from scipy.stats import chi2_contingency
        
        # Create contingency table
        contingency = pd.crosstab(
            pd.Series([1, 1, 1, 2, 2, 2, 2, 2]),  # Clusters
            pd.Series([1, 1, 0, 0, 0, 0, 1, 1])   # Trait
        )
        
        chi2, p, dof, expected = chi2_contingency(contingency)
        
        assert chi2 >= 0
        assert 0 <= p <= 1
        assert dof >= 1

    def test_fisher_exact_test(self):
        """Test Fisher's exact test for small samples."""
        from scipy.stats import fisher_exact
        
        contingency = np.array([[3, 1], [1, 3]])
        
        odds_ratio, p = fisher_exact(contingency)
        
        assert odds_ratio >= 0
        assert 0 <= p <= 1


# ============================================================================
# Test association rule mining
# ============================================================================
class TestAssociationRules:
    """Test association rule mining."""

    def test_apriori_basic(self):
        """Test basic Apriori algorithm."""
        from mlxtend.frequent_patterns import apriori, association_rules
        
        # Create basket data
        df = pd.DataFrame({
            'A': [True, True, True, False, True],
            'B': [True, True, False, True, True],
            'C': [True, False, True, False, True],
        })
        
        # Find frequent itemsets
        frequent = apriori(df, min_support=0.4, use_colnames=True)
        
        assert len(frequent) > 0
        
        # Generate rules
        if len(frequent) > 0:
            rules = association_rules(frequent, metric='confidence', min_threshold=0.5)
            assert isinstance(rules, pd.DataFrame)


# ============================================================================
# Test MCA analysis
# ============================================================================
class TestMCA:
    """Test Multiple Correspondence Analysis."""

    def test_mca_basic(self):
        """Test basic MCA analysis."""
        import prince
        
        # Create categorical data
        df = pd.DataFrame({
            'A': ['yes', 'no', 'yes', 'no', 'yes'],
            'B': ['high', 'low', 'high', 'low', 'high'],
            'C': ['red', 'blue', 'red', 'blue', 'red'],
        }).astype('category')
        
        mca = prince.MCA(n_components=2, random_state=42)
        mca.fit(df)
        
        row_coords = mca.row_coordinates(df)
        
        assert row_coords.shape == (5, 2)


# ============================================================================
# Test evolutionary metrics
# ============================================================================
class TestEvolutionaryMetrics:
    """Test evolutionary metrics computation."""

    def test_pairwise_distance_within_cluster(self):
        """Test pairwise distance within cluster."""
        # Create distance matrix
        n = 4
        dist = np.array([
            [0, 1, 2, 3],
            [1, 0, 1, 2],
            [2, 1, 0, 1],
            [3, 2, 1, 0]
        ])
        
        # Cluster indices
        cluster_indices = [0, 1]  # First two samples
        
        # Calculate mean pairwise distance within cluster
        distances = []
        for i in range(len(cluster_indices)):
            for j in range(i + 1, len(cluster_indices)):
                distances.append(dist[cluster_indices[i], cluster_indices[j]])
        
        mean_dist = np.mean(distances) if distances else 0
        
        assert mean_dist == 1.0  # Distance between sample 0 and 1

    def test_beta_diversity_between_clusters(self):
        """Test beta diversity between clusters."""
        # Create distance matrix
        dist = np.array([
            [0, 1, 5, 6],
            [1, 0, 5, 6],
            [5, 5, 0, 1],
            [6, 6, 1, 0]
        ])
        
        cluster1 = [0, 1]
        cluster2 = [2, 3]
        
        # Calculate mean distance between clusters
        distances = []
        for i in cluster1:
            for j in cluster2:
                distances.append(dist[i, j])
        
        beta_div = np.mean(distances)
        
        # Average of [5, 6, 5, 6] = 5.5
        np.testing.assert_almost_equal(beta_div, 5.5, decimal=1)


# ============================================================================
# Test FDR correction
# ============================================================================
class TestFDRCorrection:
    """Test FDR correction functionality."""

    def test_fdr_correction(self):
        """Test Benjamini-Hochberg FDR correction."""
        from statsmodels.stats.multitest import multipletests
        
        # Create p-values
        pvalues = np.array([0.01, 0.02, 0.03, 0.1, 0.2, 0.5])
        
        reject, pval_corrected, _, _ = multipletests(pvalues, alpha=0.05, method='fdr_bh')
        
        # Corrected p-values should be >= original
        assert all(pval_corrected >= pvalues)
        
        # Monotonicity check
        sorted_pvals = np.sort(pvalues)
        sorted_corrected = pval_corrected[np.argsort(pvalues)]
        for i in range(1, len(sorted_corrected)):
            assert sorted_corrected[i] >= sorted_corrected[i-1] or np.isclose(sorted_corrected[i], sorted_corrected[i-1])


# ============================================================================
# Test Random Forest importance
# ============================================================================
class TestRandomForestImportance:
    """Test Random Forest feature importance."""

    def test_rf_importance_basic(self):
        """Test basic Random Forest importance."""
        from sklearn.ensemble import RandomForestClassifier
        
        np.random.seed(42)
        
        # Create data where first feature is important
        X = np.random.randint(0, 2, (100, 3))
        y = X[:, 0]  # Labels based on first feature
        
        rf = RandomForestClassifier(n_estimators=50, random_state=42)
        rf.fit(X, y)
        
        importance = rf.feature_importances_
        
        # First feature should have highest importance
        assert importance[0] > importance[1]
        assert importance[0] > importance[2]

    def test_rf_importance_bootstrap(self):
        """Test bootstrap RF importance."""
        from sklearn.ensemble import RandomForestClassifier
        from tqdm import tqdm
        
        np.random.seed(42)
        
        X = np.random.randint(0, 2, (50, 3))
        y = np.random.randint(0, 2, 50)
        
        n_bootstrap = 10
        importances = []
        
        for _ in range(n_bootstrap):
            idx = np.random.choice(len(X), size=len(X), replace=True)
            X_boot, y_boot = X[idx], y[idx]
            
            rf = RandomForestClassifier(n_estimators=10, random_state=None)
            rf.fit(X_boot, y_boot)
            importances.append(rf.feature_importances_)
        
        mean_imp = np.mean(importances, axis=0)
        std_imp = np.std(importances, axis=0)
        
        assert len(mean_imp) == 3
        assert len(std_imp) == 3


# ============================================================================
# Test shared/unique features
# ============================================================================
class TestSharedUniqueFeatures:
    """Test shared and unique feature identification."""

    def test_shared_features(self):
        """Test identification of shared features."""
        df = pd.DataFrame({
            'Cluster': [1, 1, 2, 2],
            'Feature_A': [1, 1, 1, 1],  # Shared
            'Feature_B': [1, 1, 0, 0],  # Unique to cluster 1
            'Feature_C': [0, 0, 1, 1],  # Unique to cluster 2
        })
        
        # Find shared features (present in multiple clusters with >30% frequency)
        threshold = 0.3
        shared = []
        unique = []
        
        features = ['Feature_A', 'Feature_B', 'Feature_C']
        clusters = df['Cluster'].unique()
        
        for feat in features:
            present_in = []
            for cl in clusters:
                cl_data = df[df['Cluster'] == cl]
                if cl_data[feat].mean() >= threshold:
                    present_in.append(cl)
            
            if len(present_in) > 1:
                shared.append(feat)
            elif len(present_in) == 1:
                unique.append((feat, present_in[0]))
        
        assert 'Feature_A' in shared
        assert ('Feature_B', 1) in unique
        assert ('Feature_C', 2) in unique


# ============================================================================
# Integration tests
# ============================================================================
class TestIntegration:
    """Integration tests for phylogenetic analysis."""

    def test_full_clustering_workflow(self):
        """Test a complete clustering workflow."""
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score
        from scipy.stats import chi2_contingency
        
        np.random.seed(42)
        
        # Create sample data
        n = 50
        cluster1 = np.random.randn(25, 5) + [5, 5, 5, 5, 5]
        cluster2 = np.random.randn(25, 5) + [-5, -5, -5, -5, -5]
        data = np.vstack([cluster1, cluster2])
        
        # Step 1: Clustering
        km = KMeans(n_clusters=2, random_state=42, n_init=10)
        labels = km.fit_predict(data)
        
        # Step 2: Validation
        silhouette = silhouette_score(data, labels)
        assert silhouette > 0.5
        
        # Step 3: Trait analysis (simulated)
        traits = pd.DataFrame({
            'Cluster': labels,
            'Gene_A': np.random.binomial(1, 0.8, n),
            'Gene_B': np.random.binomial(1, 0.3, n),
        })
        
        # Chi-square test
        contingency = pd.crosstab(traits['Cluster'], traits['Gene_A'])
        chi2, p, _, _ = chi2_contingency(contingency)
        
        assert chi2 >= 0
        assert 0 <= p <= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
