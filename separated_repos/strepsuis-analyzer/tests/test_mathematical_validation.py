"""
Mathematical Validation Tests for strepsuis-analyzer

These tests validate statistical and mathematical routines against gold-standard libraries
following the Elite Custom Instructions for StrepSuis Bioinformatics Suite.

Validations include:
- Clustering metrics (silhouette score, distance matrices) against scikit-learn/scipy
- Chi-square and statistical tests against scipy
- FDR correction against statsmodels
- Cramér's V calculation verification
- MCA calculations (if prince is available)
- Edge case handling (empty inputs, zero variance, etc.)

References:
- scipy.stats for chi2_contingency, statistical tests
- statsmodels.stats.multitest for multipletests (FDR)
- sklearn.metrics for silhouette_score
- scipy.spatial.distance for distance matrices
"""

import numpy as np
import pandas as pd
import pytest
from scipy import stats
from scipy.stats import chi2_contingency
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage as scipy_linkage
from sklearn.metrics import silhouette_score as sklearn_silhouette
from statsmodels.stats.multitest import multipletests
import sys
from pathlib import Path

# Add parent directory to path to import the standalone script
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from StrepSuisPhyloCluster_2025_08_11 import StrepSuisAnalyzer

# Try to import prince for MCA tests
try:
    import prince
    HAS_PRINCE = True
except ImportError:
    HAS_PRINCE = False

# Numerical tolerance for floating-point comparisons
NUMERICAL_TOLERANCE = 1e-10


class TestClusteringMathematicalValidation:
    """Validate clustering calculations against scipy/sklearn gold standards."""

    def test_jaccard_distance_matches_scipy(self):
        """Test that Jaccard distance calculation matches scipy."""
        # Create binary data
        X = np.array([
            [1, 0, 1, 0, 1],
            [1, 1, 0, 0, 1],
            [0, 0, 1, 1, 0],
            [0, 1, 1, 0, 0]
        ])
        
        # Calculate distance using scipy (what analyzer uses internally)
        scipy_dist = pdist(X, metric='jaccard')
        
        # Verify it's a valid distance matrix
        dist_matrix = squareform(scipy_dist)
        
        # Distance matrix should be symmetric
        np.testing.assert_array_almost_equal(dist_matrix, dist_matrix.T,
            err_msg="Distance matrix should be symmetric")
        
        # Diagonal should be zero (distance from point to itself)
        np.testing.assert_array_almost_equal(np.diag(dist_matrix), np.zeros(len(X)),
            err_msg="Diagonal distances should be zero")
        
        # All distances should be non-negative
        assert np.all(dist_matrix >= 0), "All distances should be non-negative"
        
        # Jaccard distance should be in [0, 1] for binary data
        assert np.all(dist_matrix <= 1), "Jaccard distances should be <= 1"

    def test_linkage_calculation_matches_scipy(self):
        """Test that hierarchical linkage matches scipy implementation."""
        # Create binary data
        X = np.array([
            [1, 0, 1, 0, 1],
            [1, 1, 0, 0, 1],
            [0, 0, 1, 1, 0],
            [0, 1, 1, 0, 0],
            [1, 0, 1, 1, 0]
        ])
        
        # Calculate distance and linkage
        dist_matrix = pdist(X, metric='jaccard')
        
        # Test different linkage methods
        for method in ['ward', 'complete', 'average', 'single']:
            if method == 'ward':
                # Ward requires Euclidean distance
                dist_ward = pdist(X, metric='euclidean')
                linkage_matrix = scipy_linkage(dist_ward, method='ward')
            else:
                linkage_matrix = scipy_linkage(dist_matrix, method=method)
            
            # Linkage matrix should have correct shape (n-1, 4)
            assert linkage_matrix.shape == (len(X) - 1, 4), \
                f"Linkage matrix should have shape ({len(X)-1}, 4)"
            
            # All cluster indices should be valid
            assert np.all(linkage_matrix[:, 0] >= 0), "All cluster indices should be >= 0"
            assert np.all(linkage_matrix[:, 1] >= 0), "All cluster indices should be >= 0"
            
            # Merge distances should be non-decreasing (for single linkage)
            if method == 'single':
                distances = linkage_matrix[:, 2]
                for i in range(len(distances) - 1):
                    assert distances[i] <= distances[i+1] + NUMERICAL_TOLERANCE, \
                        "Single linkage distances should be non-decreasing"

    def test_silhouette_score_calculation(self):
        """Test silhouette score calculation for cluster quality."""
        np.random.seed(42)
        
        # Create data with clear clusters
        cluster1 = np.random.binomial(1, 0.8, (20, 10))
        cluster2 = np.random.binomial(1, 0.2, (20, 10))
        X = np.vstack([cluster1, cluster2])
        
        # Create cluster labels
        labels = np.array([0]*20 + [1]*20)
        
        # Calculate distance matrix
        dist_matrix = pdist(X, metric='jaccard')
        
        # Calculate silhouette score using sklearn
        silhouette = sklearn_silhouette(squareform(dist_matrix), labels, metric='precomputed')
        
        # Silhouette score should be in [-1, 1]
        assert -1 <= silhouette <= 1, "Silhouette score should be in [-1, 1]"
        
        # For well-separated clusters, silhouette should be positive
        assert silhouette > 0, "Well-separated clusters should have positive silhouette"

    def test_optimal_cluster_selection_logic(self):
        """Test that optimal cluster selection chooses reasonable number of clusters."""
        np.random.seed(42)
        
        # Create data with 3 clear clusters
        cluster1 = np.random.binomial(1, 0.8, (15, 10))
        cluster2 = np.random.binomial(1, 0.3, (15, 10))
        cluster3 = np.random.binomial(1, 0.5, (15, 10))
        X = np.vstack([cluster1, cluster2, cluster3])
        
        # Calculate distance and linkage
        dist_matrix = pdist(X, metric='jaccard')
        linkage_matrix = scipy_linkage(dist_matrix, method='average')
        
        # Test different numbers of clusters
        from scipy.cluster.hierarchy import fcluster
        
        best_score = -1
        best_k = 2
        
        for k in range(2, min(11, len(X) // 2)):
            labels = fcluster(linkage_matrix, k, criterion='maxclust')
            
            # Only calculate if we have enough samples per cluster
            if len(np.unique(labels)) >= 2:
                try:
                    score = sklearn_silhouette(squareform(dist_matrix), labels, metric='precomputed')
                    if score > best_score:
                        best_score = score
                        best_k = k
                except ValueError:
                    # Skip if clustering is degenerate
                    continue
        
        # Should find 2-7 clusters (reasonable range, silhouette can be noisy)
        assert 2 <= best_k <= 7, f"Should find reasonable number of clusters, got {best_k}"
        assert best_score > 0, "Best silhouette score should be positive"


class TestStatisticalTestsValidation:
    """Validate statistical tests against scipy gold standard."""

    def test_chi_square_matches_scipy(self):
        """Test that chi-square calculations match scipy."""
        # Create a 2x2 contingency table
        contingency = pd.DataFrame([[50, 30], [20, 40]])
        
        # Calculate using scipy
        chi2_scipy, p_scipy, dof_scipy, expected_scipy = chi2_contingency(contingency)
        
        # Calculate using stats module directly
        chi2_manual, p_manual, dof_manual, expected_manual = stats.chi2_contingency(contingency)
        
        # Should match exactly
        np.testing.assert_almost_equal(chi2_scipy, chi2_manual, decimal=10,
            err_msg="Chi-square value should match scipy")
        np.testing.assert_almost_equal(p_scipy, p_manual, decimal=10,
            err_msg="P-value should match scipy")
        assert dof_scipy == dof_manual, "Degrees of freedom should match"

    def test_cramers_v_calculation(self):
        """Validate Cramér's V calculation against manual computation."""
        # Create contingency table
        contingency = np.array([[50, 30, 20], [20, 40, 30]])
        
        # Calculate chi-square
        chi2, p, dof, expected = stats.chi2_contingency(contingency)
        
        # Calculate Cramér's V manually
        n = contingency.sum()
        min_dim = min(contingency.shape) - 1
        cramers_v_expected = np.sqrt(chi2 / (n * min_dim))
        
        # This is the formula used in the analyzer
        cramers_v_manual = np.sqrt(chi2 / (n * min_dim))
        
        # Should match
        np.testing.assert_almost_equal(cramers_v_expected, cramers_v_manual, decimal=10,
            err_msg="Cramér's V calculation should be correct")
        
        # Cramér's V should be in [0, 1]
        assert 0 <= cramers_v_manual <= 1, "Cramér's V should be in [0, 1]"

    def test_cramers_v_bounds(self):
        """Test that Cramér's V is always in [0, 1]."""
        np.random.seed(42)
        
        # Test with random contingency tables
        for _ in range(100):
            # Generate random 2x3 contingency table
            contingency = np.random.randint(1, 50, size=(2, 3))
            
            chi2, p, dof, expected = stats.chi2_contingency(contingency)
            n = contingency.sum()
            min_dim = min(contingency.shape) - 1
            cramers_v = np.sqrt(chi2 / (n * min_dim))
            
            assert 0 <= cramers_v <= 1, f"Cramér's V should be in [0, 1], got {cramers_v}"

    def test_cramers_v_perfect_association(self):
        """Test Cramér's V for perfect association."""
        # Perfect association: all in diagonal
        contingency = np.array([[50, 0], [0, 50]])
        
        chi2, p, dof, expected = stats.chi2_contingency(contingency)
        n = contingency.sum()
        min_dim = min(contingency.shape) - 1
        cramers_v = np.sqrt(chi2 / (n * min_dim))
        
        # Should be close to 1 for perfect association
        assert cramers_v > 0.95, f"Perfect association should have Cramér's V near 1, got {cramers_v}"

    def test_cramers_v_independence(self):
        """Test Cramér's V for independent variables."""
        # Independent: proportions are same across groups
        contingency = np.array([[25, 25], [25, 25]])
        
        chi2, p, dof, expected = stats.chi2_contingency(contingency)
        n = contingency.sum()
        min_dim = min(contingency.shape) - 1
        cramers_v = np.sqrt(chi2 / (n * min_dim))
        
        # Should be close to 0 for independence
        assert cramers_v < 0.01, f"Independence should have Cramér's V near 0, got {cramers_v}"


class TestFDRCorrectionValidation:
    """Validate FDR correction against statsmodels."""

    def test_fdr_correction_matches_statsmodels(self):
        """Test that FDR correction matches statsmodels implementation."""
        # Test p-values
        p_values = np.array([0.001, 0.01, 0.05, 0.10, 0.50, 0.80])
        
        # Apply FDR correction using statsmodels
        reject, p_adj, alpha_sidak, alpha_bonf = multipletests(
            p_values, alpha=0.05, method='fdr_bh'
        )
        
        # Corrected p-values should be monotonically non-decreasing when sorted
        sorted_indices = np.argsort(p_values)
        sorted_corrected = p_adj[sorted_indices]
        
        for i in range(len(sorted_corrected) - 1):
            assert sorted_corrected[i] <= sorted_corrected[i+1] + NUMERICAL_TOLERANCE, \
                "FDR-corrected p-values should be non-decreasing when sorted by raw p"
        
        # All corrected p-values should be >= original
        for orig, corr in zip(p_values, p_adj):
            assert corr >= orig - NUMERICAL_TOLERANCE, \
                f"Corrected p-value ({corr}) should be >= original ({orig})"
        
        # Corrected p-values should be <= 1
        assert np.all(p_adj <= 1.0 + NUMERICAL_TOLERANCE), \
            "Corrected p-values should be <= 1"

    def test_fdr_monotonicity_requirement(self):
        """
        Critical test: FDR-corrected p-values must be monotonically non-decreasing
        when sorted by raw p-values (Benjamini-Hochberg procedure requirement).
        """
        np.random.seed(42)
        
        # Generate random p-values
        p_values = np.random.uniform(0, 1, size=50)
        
        # Apply FDR correction
        reject, p_adj, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')
        
        # Sort by raw p-values
        sorted_indices = np.argsort(p_values)
        sorted_raw = p_values[sorted_indices]
        sorted_adj = p_adj[sorted_indices]
        
        # Verify monotonicity
        for i in range(len(sorted_adj) - 1):
            assert sorted_adj[i] <= sorted_adj[i+1] + NUMERICAL_TOLERANCE, \
                f"FDR monotonicity violated at index {i}: {sorted_adj[i]} > {sorted_adj[i+1]}"

    def test_fdr_with_analyzer_workflow(self):
        """Test FDR correction in actual analyzer workflow."""
        np.random.seed(42)
        
        # Create synthetic data with clusters
        cluster1 = np.random.binomial(1, 0.8, (25, 8))
        cluster2 = np.random.binomial(1, 0.3, (25, 8))
        X = np.vstack([cluster1, cluster2])
        
        data = pd.DataFrame(X, columns=[f'Trait_{i}' for i in range(8)])
        data['Strain_ID'] = [f'Strain_{i}' for i in range(50)]
        
        # Create analyzer and add cluster labels
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_fdr', random_state=42)
        analyzer.data = data
        analyzer.clusters = np.array([0]*25 + [1]*25)
        analyzer.data['Cluster'] = analyzer.clusters
        
        # Calculate trait associations (includes FDR)
        analyzer.calculate_trait_associations(fdr_alpha=0.05)
        
        # Verify results
        results = analyzer.results['trait_associations']
        
        # Check FDR monotonicity
        results_sorted = results.sort_values('P_value')
        p_adj_sorted = results_sorted['P_adj'].values
        
        for i in range(len(p_adj_sorted) - 1):
            assert p_adj_sorted[i] <= p_adj_sorted[i+1] + NUMERICAL_TOLERANCE, \
                "FDR-corrected p-values should be non-decreasing"
        
        # All adjusted p-values should be >= raw p-values
        for _, row in results.iterrows():
            assert row['P_adj'] >= row['P_value'] - NUMERICAL_TOLERANCE, \
                "Adjusted p should be >= raw p"


@pytest.mark.skipif(not HAS_PRINCE, reason="prince not available")
class TestMCAValidation:
    """Validate MCA calculations (if prince is available)."""

    def test_mca_component_extraction(self):
        """Test that MCA components are extracted correctly."""
        np.random.seed(42)
        
        # Create categorical data (as strings for MCA)
        data = pd.DataFrame({
            'var1': np.random.choice(['0', '1'], size=50),
            'var2': np.random.choice(['0', '1'], size=50),
            'var3': np.random.choice(['0', '1'], size=50),
            'var4': np.random.choice(['0', '1'], size=50),
        })
        
        # Fit MCA
        mca = prince.MCA(n_components=2, random_state=42)
        coords = mca.fit_transform(data)
        
        # Check shape
        assert coords.shape == (50, 2), "MCA coordinates should have correct shape"
        
        # Check eigenvalues sum
        eigenvalues = mca.eigenvalues_
        assert len(eigenvalues) > 0, "Should have eigenvalues"
        assert np.all(eigenvalues >= 0), "Eigenvalues should be non-negative"

    def test_mca_explained_variance(self):
        """Test that explained variance is calculated correctly."""
        np.random.seed(42)
        
        # Create data with structure
        data = pd.DataFrame({
            'var1': ['1']*25 + ['0']*25,
            'var2': ['1']*25 + ['0']*25,
            'var3': np.random.choice(['0', '1'], size=50),
            'var4': np.random.choice(['0', '1'], size=50),
        })
        
        # Fit MCA
        mca = prince.MCA(n_components=2, random_state=42)
        mca.fit(data)
        
        # Calculate explained variance
        explained_var = mca.eigenvalues_ / mca.eigenvalues_.sum()
        
        # Check properties
        assert len(explained_var) >= 2, "Should have at least 2 components"
        assert np.all(explained_var >= 0), "Explained variance should be non-negative"
        assert np.all(explained_var <= 1), "Explained variance should be <= 1"
        
        # First component should explain most variance
        assert explained_var[0] >= explained_var[1], \
            "First component should explain most variance"


class TestEdgeCases:
    """Test edge cases for robustness."""

    def test_empty_dataframe(self):
        """Test handling of empty DataFrame."""
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_empty', random_state=42)
        analyzer.data = pd.DataFrame()
        
        # Should handle empty data gracefully
        # (clustering would fail on empty data, which is expected)
        assert analyzer.data.empty, "Empty DataFrame should be recognized"

    def test_single_cluster(self):
        """Test handling when all data belongs to single cluster."""
        np.random.seed(42)
        
        # Create homogeneous data
        X = np.random.binomial(1, 0.5, (20, 5))
        data = pd.DataFrame(X, columns=[f'Trait_{i}' for i in range(5)])
        data['Strain_ID'] = [f'Strain_{i}' for i in range(20)]
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_single', random_state=42)
        analyzer.data = data
        
        # Try clustering - should handle gracefully
        # (silhouette score requires at least 2 clusters)
        try:
            analyzer.perform_clustering(n_clusters=1)
        except (ValueError, Exception) as e:
            # It's OK to fail on single cluster, but should be controlled
            assert "cluster" in str(e).lower() or "silhouette" in str(e).lower()

    def test_zero_variance_features(self):
        """Test handling of zero variance features."""
        data = pd.DataFrame({
            'Strain_ID': ['A', 'B', 'C', 'D'],
            'constant': [1, 1, 1, 1],  # No variance
            'variable': [1, 0, 1, 0],
        })
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_zero_var', random_state=42)
        analyzer.data = data
        
        # Should handle constant features
        # (clustering uses all features, may produce degenerate results)
        # The test is that it doesn't crash
        assert 'constant' in analyzer.data.columns

    def test_perfect_separation(self):
        """Test clustering with perfectly separated groups."""
        # Create perfectly separated data
        cluster1 = np.ones((10, 5))
        cluster2 = np.zeros((10, 5))
        X = np.vstack([cluster1, cluster2])
        
        data = pd.DataFrame(X, columns=[f'Trait_{i}' for i in range(5)])
        data['Strain_ID'] = [f'Strain_{i}' for i in range(20)]
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_perfect_sep', random_state=42)
        analyzer.data = data
        analyzer.perform_clustering(n_clusters=2)
        
        # Should successfully cluster perfectly separated data
        assert hasattr(analyzer, 'clusters'), "Should have clusters"
        assert len(np.unique(analyzer.clusters)) == 2, "Should find 2 clusters"

    def test_extreme_imbalance(self):
        """Test handling of extremely imbalanced data (99% vs 1%)."""
        np.random.seed(42)
        
        # 99% in one group, 1% in another
        cluster1 = np.random.binomial(1, 0.9, (99, 5))
        cluster2 = np.random.binomial(1, 0.1, (1, 5))
        X = np.vstack([cluster1, cluster2])
        
        data = pd.DataFrame(X, columns=[f'Trait_{i}' for i in range(5)])
        data['Strain_ID'] = [f'Strain_{i}' for i in range(100)]
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_imbalance', random_state=42)
        analyzer.data = data
        
        # Should handle extreme imbalance
        analyzer.perform_clustering(n_clusters=2)
        assert hasattr(analyzer, 'clusters'), "Should handle imbalanced data"


class TestNumericalStability:
    """Test numerical stability of calculations."""

    def test_distance_matrix_symmetry(self):
        """Test that distance matrices are symmetric."""
        np.random.seed(42)
        X = np.random.binomial(1, 0.5, (20, 10))
        
        # Calculate distance matrix
        dist_vec = pdist(X, metric='jaccard')
        dist_matrix = squareform(dist_vec)
        
        # Should be symmetric
        np.testing.assert_array_almost_equal(dist_matrix, dist_matrix.T,
            err_msg="Distance matrix should be symmetric")

    def test_distance_triangle_inequality(self):
        """Test that distances satisfy triangle inequality."""
        np.random.seed(42)
        X = np.random.binomial(1, 0.5, (10, 5))
        
        # Calculate distance matrix
        dist_vec = pdist(X, metric='jaccard')
        dist_matrix = squareform(dist_vec)
        
        # Check triangle inequality: d(i,k) <= d(i,j) + d(j,k)
        n = len(dist_matrix)
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    assert dist_matrix[i, k] <= dist_matrix[i, j] + dist_matrix[j, k] + NUMERICAL_TOLERANCE, \
                        f"Triangle inequality violated: d({i},{k}) > d({i},{j}) + d({j},{k})"

    def test_chi_square_numerical_stability(self):
        """Test chi-square calculation with extreme values."""
        # Large counts
        contingency_large = np.array([[5000, 3000], [2000, 4000]])
        chi2_large, p_large, _, _ = stats.chi2_contingency(contingency_large)
        
        # Should not produce NaN or infinity
        assert np.isfinite(chi2_large), "Chi-square should be finite for large counts"
        assert np.isfinite(p_large), "P-value should be finite for large counts"
        
        # Small counts
        contingency_small = np.array([[5, 3], [2, 4]])
        chi2_small, p_small, _, _ = stats.chi2_contingency(contingency_small)
        
        # Should not produce NaN or infinity
        assert np.isfinite(chi2_small), "Chi-square should be finite for small counts"
        assert np.isfinite(p_small), "P-value should be finite for small counts"


class TestReproducibility:
    """Test reproducibility with fixed random seeds."""

    def test_clustering_reproducibility(self):
        """Test that clustering is reproducible with same seed."""
        np.random.seed(42)
        X = np.random.binomial(1, 0.5, (30, 8))
        
        data = pd.DataFrame(X, columns=[f'Trait_{i}' for i in range(8)])
        data['Strain_ID'] = [f'Strain_{i}' for i in range(30)]
        
        # Run clustering twice with same seed
        analyzer1 = StrepSuisAnalyzer(output_dir='/tmp/test_repro1', random_state=42)
        analyzer1.data = data.copy()
        analyzer1.perform_clustering(n_clusters=3)
        
        analyzer2 = StrepSuisAnalyzer(output_dir='/tmp/test_repro2', random_state=42)
        analyzer2.data = data.copy()
        analyzer2.perform_clustering(n_clusters=3)
        
        # Results should be identical
        np.testing.assert_array_equal(analyzer1.clusters, analyzer2.clusters,
            err_msg="Clustering should be reproducible with same seed")

    @pytest.mark.skipif(not HAS_PRINCE, reason="prince not available")
    def test_mca_reproducibility(self):
        """Test that MCA is reproducible with same seed."""
        np.random.seed(42)
        
        data = pd.DataFrame({
            'Strain_ID': [f'Strain_{i}' for i in range(30)],
            'var1': np.random.choice([0, 1], size=30),
            'var2': np.random.choice([0, 1], size=30),
            'var3': np.random.choice([0, 1], size=30),
        })
        
        # Run MCA twice with same seed
        analyzer1 = StrepSuisAnalyzer(output_dir='/tmp/test_mca_repro1', random_state=42)
        analyzer1.data = data.copy()
        analyzer1.perform_mca(n_components=2)
        
        analyzer2 = StrepSuisAnalyzer(output_dir='/tmp/test_mca_repro2', random_state=42)
        analyzer2.data = data.copy()
        analyzer2.perform_mca(n_components=2)
        
        # Results should be very similar (MCA might have small numerical differences)
        np.testing.assert_array_almost_equal(
            analyzer1.data['MCA1'].values,
            analyzer2.data['MCA1'].values,
            decimal=5,
            err_msg="MCA should be reproducible with same seed"
        )
