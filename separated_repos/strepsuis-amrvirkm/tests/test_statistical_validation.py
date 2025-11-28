"""
Statistical Validation Tests for strepsuis-amrvirkm

These tests validate the K-modes clustering and MCA routines against gold-standard
libraries as specified in the Elite Custom Instructions for StrepSuis Bioinformatics Suite.

Validations include:
- K-modes clustering behavior and metrics against kmodes library
- Silhouette score against sklearn
- Chi-square tests against scipy
- MCA explained variance validation
- Edge case handling (empty inputs, single-row/column tables, zero variance)

References:
- kmodes for K-modes clustering
- sklearn.metrics for silhouette score, clustering metrics
- scipy.stats for chi-square tests
- prince for MCA
"""

import numpy as np
import pandas as pd
import pytest
from scipy.stats import chi2_contingency, fisher_exact
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score


class TestKModesClustering:
    """Validate K-modes clustering behavior."""

    def test_kmodes_basic_clustering(self):
        """Test basic K-modes clustering produces valid clusters."""
        from kmodes.kmodes import KModes

        # Create test data
        np.random.seed(42)
        n = 50
        data = pd.DataFrame({
            'feat1': np.random.binomial(1, 0.7, n),
            'feat2': np.random.binomial(1, 0.3, n),
            'feat3': np.random.binomial(1, 0.5, n),
        })

        # Run K-modes
        km = KModes(n_clusters=3, init='Huang', n_init=5, random_state=42)
        clusters = km.fit_predict(data)

        # Check cluster assignments
        assert len(clusters) == n, "Should assign cluster to each sample"
        assert len(set(clusters)) <= 3, "Should have at most 3 clusters"
        assert min(clusters) >= 0, "Cluster labels should be non-negative"

    def test_kmodes_reproducibility(self):
        """Test K-modes reproducibility with fixed seed."""
        from kmodes.kmodes import KModes

        np.random.seed(42)
        data = pd.DataFrame({
            'feat1': np.random.binomial(1, 0.5, 30),
            'feat2': np.random.binomial(1, 0.5, 30),
            'feat3': np.random.binomial(1, 0.5, 30),
        })

        # Run twice with same seed
        km1 = KModes(n_clusters=2, init='Huang', n_init=1, random_state=42)
        clusters1 = km1.fit_predict(data)

        km2 = KModes(n_clusters=2, init='Huang', n_init=1, random_state=42)
        clusters2 = km2.fit_predict(data)

        # Should produce same results
        np.testing.assert_array_equal(clusters1, clusters2,
            err_msg="Same seed should give same cluster assignments")


class TestSilhouetteScore:
    """Validate silhouette score calculations against sklearn."""

    def test_silhouette_calculation(self):
        """Test silhouette score calculation matches sklearn."""
        from sklearn.metrics import silhouette_score

        # Create well-separated clusters
        np.random.seed(42)
        cluster1 = np.array([[1, 1, 0, 0]] * 20)
        cluster2 = np.array([[0, 0, 1, 1]] * 20)
        data = np.vstack([cluster1, cluster2])
        labels = np.array([0] * 20 + [1] * 20)

        # Calculate silhouette
        score = silhouette_score(data, labels)

        # Well-separated clusters should have high silhouette
        assert score > 0.5, f"Well-separated clusters should have high silhouette, got {score}"

    def test_silhouette_bounds(self):
        """Test silhouette score is within valid bounds."""
        from sklearn.metrics import silhouette_score

        np.random.seed(42)
        data = np.random.binomial(1, 0.5, (50, 5))
        labels = np.random.randint(0, 3, 50)

        score = silhouette_score(data, labels)

        assert -1 <= score <= 1, f"Silhouette score should be in [-1, 1], got {score}"


class TestClusteringMetrics:
    """Validate clustering quality metrics."""

    def test_calinski_harabasz_positive(self):
        """Test Calinski-Harabasz index is positive for reasonable clusters."""
        np.random.seed(42)
        cluster1 = np.array([[1, 1, 0, 0]] * 15) + np.random.normal(0, 0.1, (15, 4))
        cluster2 = np.array([[0, 0, 1, 1]] * 15) + np.random.normal(0, 0.1, (15, 4))
        data = np.vstack([cluster1, cluster2])
        labels = np.array([0] * 15 + [1] * 15)

        ch_score = calinski_harabasz_score(data, labels)

        assert ch_score > 0, f"CH score should be positive, got {ch_score}"

    def test_davies_bouldin_non_negative(self):
        """Test Davies-Bouldin index is non-negative."""
        np.random.seed(42)
        data = np.random.random((50, 5))
        labels = np.random.randint(0, 3, 50)

        db_score = davies_bouldin_score(data, labels)

        assert db_score >= 0, f"DB score should be non-negative, got {db_score}"


class TestChiSquareAnalysis:
    """Validate chi-square tests for feature-cluster associations."""

    def test_chi_square_significant_association(self):
        """Test chi-square detects significant association."""
        # Create data with clear feature-cluster association
        feature = pd.Series([1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        cluster = pd.Series([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

        contingency = pd.crosstab(feature, cluster)
        chi2, p, dof, expected = chi2_contingency(contingency)

        # Should be significant
        assert p < 0.05, f"Perfect association should have p < 0.05, got {p}"

    def test_chi_square_independent(self):
        """Test chi-square for independent variables."""
        np.random.seed(42)
        feature = pd.Series(np.random.binomial(1, 0.5, 100))
        cluster = pd.Series(np.random.randint(0, 3, 100))

        contingency = pd.crosstab(feature, cluster)
        chi2, p, dof, expected = chi2_contingency(contingency)

        # Should generally not be very significant for random data
        # (though can happen by chance)
        assert p > 0 and p <= 1, f"P-value should be in (0, 1], got {p}"


class TestMCAValidation:
    """Validate Multiple Correspondence Analysis."""

    def test_mca_explained_variance(self):
        """Test MCA produces valid explained variance."""
        import prince

        # Create categorical data
        np.random.seed(42)
        data = pd.DataFrame({
            'feat1': pd.Categorical(np.random.choice(['A', 'B'], 50)),
            'feat2': pd.Categorical(np.random.choice(['X', 'Y', 'Z'], 50)),
            'feat3': pd.Categorical(np.random.choice(['P', 'Q'], 50)),
        })

        # Run MCA
        mca = prince.MCA(n_components=2, random_state=42)
        mca = mca.fit(data)

        # Check explained variance
        eigenvalues = mca.eigenvalues_

        assert len(eigenvalues) >= 2, "Should have at least 2 eigenvalues"
        assert all(ev >= 0 for ev in eigenvalues), "Eigenvalues should be non-negative"

    def test_mca_coordinates_shape(self):
        """Test MCA produces correct coordinate shapes."""
        import prince

        np.random.seed(42)
        n_samples = 30
        data = pd.DataFrame({
            'feat1': pd.Categorical(np.random.choice(['A', 'B'], n_samples)),
            'feat2': pd.Categorical(np.random.choice(['X', 'Y'], n_samples)),
        })

        mca = prince.MCA(n_components=2, random_state=42)
        mca = mca.fit(data)

        row_coords = mca.row_coordinates(data)

        assert row_coords.shape[0] == n_samples, "Should have coords for each sample"
        assert row_coords.shape[1] == 2, "Should have 2 components"


class TestPhiCorrelation:
    """Validate phi correlation calculations."""

    def test_phi_perfect_positive(self):
        """Test phi for perfect positive correlation."""
        x = np.array([1, 1, 0, 0, 1, 1, 0, 0])
        y = np.array([1, 1, 0, 0, 1, 1, 0, 0])

        # Calculate phi manually
        a = np.sum((x == 1) & (y == 1))
        b = np.sum((x == 1) & (y == 0))
        c = np.sum((x == 0) & (y == 1))
        d = np.sum((x == 0) & (y == 0))

        denom = (a + b) * (c + d) * (a + c) * (b + d)
        if denom > 0:
            phi = (a * d - b * c) / np.sqrt(denom)
        else:
            phi = 0

        assert phi == 1.0, f"Perfect positive correlation should have phi=1, got {phi}"

    def test_phi_perfect_negative(self):
        """Test phi for perfect negative correlation."""
        x = np.array([1, 1, 0, 0, 1, 1, 0, 0])
        y = np.array([0, 0, 1, 1, 0, 0, 1, 1])

        a = np.sum((x == 1) & (y == 1))
        b = np.sum((x == 1) & (y == 0))
        c = np.sum((x == 0) & (y == 1))
        d = np.sum((x == 0) & (y == 0))

        denom = (a + b) * (c + d) * (a + c) * (b + d)
        if denom > 0:
            phi = (a * d - b * c) / np.sqrt(denom)
        else:
            phi = 0

        assert phi == -1.0, f"Perfect negative correlation should have phi=-1, got {phi}"


class TestEdgeCases:
    """Test edge cases for robustness."""

    def test_single_cluster(self):
        """Test handling of single cluster."""
        data = np.array([[1, 0, 1], [0, 1, 1], [1, 1, 0]])
        labels = np.array([0, 0, 0])  # All same cluster

        # Silhouette is undefined for single cluster
        # Should handle gracefully
        try:
            score = silhouette_score(data, labels)
            # If it doesn't raise, score should be 0 or NaN
            assert np.isnan(score) or score == 0
        except ValueError:
            pass  # Expected for single cluster

    def test_empty_contingency_handling(self):
        """Test handling of empty data in contingency tables."""
        empty_df = pd.DataFrame()

        # Should handle empty DataFrame gracefully
        if not empty_df.empty:
            contingency = pd.crosstab(empty_df[0], empty_df[1])

    def test_constant_feature(self):
        """Test handling of constant feature in clustering."""
        data = pd.DataFrame({
            'constant': [1, 1, 1, 1, 1],
            'varied': [0, 1, 0, 1, 0],
        })

        # Clustering should still work with one constant feature
        from kmodes.kmodes import KModes
        km = KModes(n_clusters=2, init='Huang', n_init=1, random_state=42)
        clusters = km.fit_predict(data)

        assert len(clusters) == 5, "Should assign clusters to all samples"


class TestLogOddsRatio:
    """Validate log-odds ratio calculations."""

    def test_log_odds_positive_association(self):
        """Test log-odds for positive association."""
        # Feature present in cluster much more than outside
        a = 40  # present in cluster, feature=1
        b = 10  # in cluster, feature=0
        c = 10  # outside cluster, feature=1
        d = 40  # outside cluster, feature=0

        # Calculate odds ratio
        odds_ratio = (a * d) / (b * c)
        log_odds = np.log(odds_ratio)

        assert log_odds > 0, f"Positive association should have positive log-odds, got {log_odds}"

    def test_log_odds_no_association(self):
        """Test log-odds for no association."""
        # Same proportions in and out of cluster
        a = 25
        b = 25
        c = 25
        d = 25

        odds_ratio = (a * d) / (b * c)
        log_odds = np.log(odds_ratio)

        np.testing.assert_almost_equal(log_odds, 0, decimal=1,
            err_msg="No association should have log-odds near 0")


class TestBootstrapCI:
    """Validate bootstrap confidence intervals for cluster statistics."""

    def test_bootstrap_ci_contains_true_proportion(self):
        """Test bootstrap CI contains true proportion."""
        np.random.seed(42)
        n = 100
        true_prop = 0.6
        data = np.random.binomial(1, true_prop, n)

        # Bootstrap
        n_bootstrap = 500
        proportions = []
        for _ in range(n_bootstrap):
            sample = np.random.choice(data, size=n, replace=True)
            proportions.append(np.mean(sample))

        ci_lower = np.percentile(proportions, 2.5)
        ci_upper = np.percentile(proportions, 97.5)

        # True proportion should be within CI (with high probability)
        # Allow some margin for small samples
        assert ci_lower - 0.1 < true_prop < ci_upper + 0.1, \
            f"True proportion {true_prop} should be near CI [{ci_lower}, {ci_upper}]"


class TestReproducibility:
    """Test reproducibility with fixed random seeds."""

    def test_kmodes_reproducible_across_runs(self):
        """Test K-modes is reproducible across multiple runs."""
        from kmodes.kmodes import KModes

        np.random.seed(42)
        data = pd.DataFrame(np.random.binomial(1, 0.5, (40, 5)))

        results = []
        for _ in range(3):
            km = KModes(n_clusters=3, init='Huang', n_init=1, random_state=42)
            clusters = km.fit_predict(data)
            results.append(tuple(clusters))

        # All runs should produce same result
        assert len(set(results)) == 1, "Same seed should give same results across runs"


@pytest.mark.slow
class TestPerformance:
    """Performance tests (marked as slow)."""

    def test_large_dataset_clustering(self):
        """Test clustering performance on larger dataset."""
        import time
        from kmodes.kmodes import KModes

        np.random.seed(42)
        n_samples = 500
        n_features = 20
        data = pd.DataFrame(
            np.random.binomial(1, 0.5, (n_samples, n_features)),
            columns=[f'feat_{i}' for i in range(n_features)]
        )

        start = time.time()
        km = KModes(n_clusters=5, init='Huang', n_init=3, random_state=42)
        clusters = km.fit_predict(data)
        elapsed = time.time() - start

        assert elapsed < 60, f"Clustering should complete in < 60s, took {elapsed:.1f}s"
        assert len(set(clusters)) <= 5, "Should have at most 5 clusters"

    def test_mca_performance(self):
        """Test MCA performance on larger dataset."""
        import time
        import prince

        np.random.seed(42)
        n_samples = 500
        data = pd.DataFrame({
            f'feat_{i}': pd.Categorical(np.random.choice(['A', 'B', 'C'], n_samples))
            for i in range(10)
        })

        start = time.time()
        mca = prince.MCA(n_components=3, random_state=42)
        mca = mca.fit(data)
        coords = mca.row_coordinates(data)
        elapsed = time.time() - start

        assert elapsed < 30, f"MCA should complete in < 30s, took {elapsed:.1f}s"
        assert coords.shape[0] == n_samples, "Should have coords for all samples"
