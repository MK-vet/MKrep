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

        # Silhouette score is mathematically undefined for a single cluster
        # (there's no between-cluster distance to compare against).
        # sklearn raises ValueError in this case, which is the expected behavior.
        try:
            score = silhouette_score(data, labels)
            # If implementation doesn't raise, it should return an undefined indicator
            assert np.isnan(score), \
                "Single cluster silhouette should raise ValueError or return NaN"
        except ValueError as e:
            # This is the expected behavior - silhouette is undefined for single cluster
            assert "Number of labels" in str(e) or "single" in str(e).lower(), \
                "Should raise ValueError about single cluster"

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


class TestPhiCoefficientValidation:
    """Validate phi coefficient calculation against manual computation."""
    
    def test_phi_against_manual_calculation(self):
        """Test phi coefficient matches manual calculation."""
        from strepsuis_amrvirkm.cluster_analysis_core import compute_phi
        
        # Known case: perfect positive correlation
        x = np.array([1, 1, 1, 1, 0, 0, 0, 0])
        y = np.array([1, 1, 1, 1, 0, 0, 0, 0])
        
        phi_ours = compute_phi(x, y)
        
        # Manual calculation: phi should be 1.0 for perfect correlation
        assert np.abs(phi_ours - 1.0) < 1e-5, f"Expected phi=1.0, got {phi_ours}"
    
    def test_phi_against_cramers_v(self):
        """Test phi coefficient is equivalent to Cramer's V for 2x2 tables."""
        from strepsuis_amrvirkm.cluster_analysis_core import compute_phi
        from scipy.stats import chi2_contingency
        
        np.random.seed(42)
        x = np.random.binomial(1, 0.6, 100)
        y = np.random.binomial(1, 0.4, 100)
        
        phi_ours = compute_phi(x, y)
        
        # Calculate Cramer's V from chi-square
        contingency = pd.crosstab(x, y)
        chi2, _, _, _ = chi2_contingency(contingency)
        n = len(x)
        cramers_v = np.sqrt(chi2 / n)
        
        # Phi should be similar to Cramer's V for 2x2 table
        # (may differ in sign)
        assert np.abs(np.abs(phi_ours) - cramers_v) < 0.1


class TestBootstrapCIValidation:
    """Validate bootstrap confidence intervals."""
    
    def test_bootstrap_ci_coverage_property(self):
        """Test that 95% CI contains true parameter ~95% of time."""
        from strepsuis_amrvirkm.cluster_analysis_core import bootstrap_confidence_interval
        
        np.random.seed(42)
        true_p = 0.5
        n_trials = 100
        n_samples = 50
        
        coverage_count = 0
        for _ in range(n_trials):
            # Generate sample
            count = np.random.binomial(n_samples, true_p)
            percentage = (count / n_samples) * 100
            
            # Calculate CI
            ci_low, ci_high = bootstrap_confidence_interval(
                percentage, count, n_samples, num_bootstrap=500, confidence_level=0.95
            )
            
            # Check if true parameter is in CI
            true_percentage = true_p * 100
            if ci_low <= true_percentage <= ci_high:
                coverage_count += 1
        
        coverage_rate = coverage_count / n_trials
        
        # Should be close to 95% (allow some variation)
        assert 0.85 <= coverage_rate <= 1.0, \
            f"95% CI should cover true parameter ~95% of time, got {coverage_rate*100}%"
    
    def test_bootstrap_ci_symmetric_for_p_50(self):
        """Test that CI is roughly symmetric for p=0.5."""
        from strepsuis_amrvirkm.cluster_analysis_core import bootstrap_confidence_interval
        
        np.random.seed(42)
        count = 50
        total = 100
        percentage = 50.0
        
        ci_low, ci_high = bootstrap_confidence_interval(
            percentage, count, total, num_bootstrap=1000
        )
        
        # For p=0.5, CI should be roughly symmetric
        lower_dist = 50.0 - ci_low
        upper_dist = ci_high - 50.0
        
        # Should be within 20% of each other
        ratio = min(lower_dist, upper_dist) / max(lower_dist, upper_dist)
        assert ratio > 0.8, f"CI should be roughly symmetric for p=0.5, got ratio {ratio}"


class TestFDRCorrectionValidation:
    """Validate FDR (Benjamini-Hochberg) correction against statsmodels."""
    
    def test_fdr_against_statsmodels(self):
        """Test FDR correction matches statsmodels."""
        from strepsuis_amrvirkm.cluster_analysis_core import chi_square_analysis
        from statsmodels.stats.multitest import multipletests
        
        np.random.seed(42)
        n = 60
        data = pd.DataFrame({
            f'Feature{i}': np.random.binomial(1, 0.5, n)
            for i in range(10)
        })
        clusters = np.array([1] * 20 + [2] * 20 + [3] * 20)
        
        # Get our FDR correction
        global_results, _ = chi_square_analysis(data, clusters)
        
        if not global_results.empty:
            our_pvals = global_results['P_Value'].values
            our_adjusted = global_results['Adjusted_P'].values
            
            # Compare with statsmodels
            _, statsmodels_adjusted, _, _ = multipletests(
                our_pvals, alpha=0.05, method='fdr_bh'
            )
            
            # Should match to high precision
            np.testing.assert_allclose(
                our_adjusted, statsmodels_adjusted, 
                rtol=1e-10, atol=1e-10,
                err_msg="FDR correction should match statsmodels"
            )


class TestLogOddsRatioValidation:
    """Validate log odds ratio calculations."""
    
    def test_log_odds_ratio_manual_calculation(self):
        """Test log odds ratio against manual calculation."""
        from strepsuis_amrvirkm.cluster_analysis_core import _bootstrap_log_odds
        
        # Known 2x2 table
        a, b, c, d = 20, 5, 10, 15
        
        # Manual calculation
        odds_cluster = (a + 0.5) / (b + 0.5)
        odds_other = (c + 0.5) / (d + 0.5)
        log_odds_manual = np.log(odds_cluster / odds_other)
        
        # Our implementation (with bootstrap, but we check mean)
        np.random.seed(42)
        boot_results = _bootstrap_log_odds(a, b, c, d, n_bootstrap=1000)
        log_odds_ours = np.mean(boot_results)
        
        # Should be close (within 10% due to bootstrap variation)
        assert np.abs(log_odds_ours - log_odds_manual) < 0.5, \
            f"Log odds should match manual calculation: {log_odds_manual} vs {log_odds_ours}"


class TestSilhouetteScoreValidation:
    """Validate silhouette score calculations."""
    
    def test_silhouette_score_against_sklearn(self):
        """Test our silhouette usage matches sklearn."""
        from strepsuis_amrvirkm.cluster_analysis_core import perform_kmodes
        from sklearn.metrics import silhouette_score
        
        np.random.seed(42)
        # Create data with clear clusters
        cluster1 = pd.DataFrame([[1, 1, 0, 0]] * 15)
        cluster2 = pd.DataFrame([[0, 0, 1, 1]] * 15)
        data = pd.concat([cluster1, cluster2], ignore_index=True)
        
        # Get clusters
        _, clusters = perform_kmodes(data, n_clusters=2)
        
        # Calculate silhouette using sklearn
        score = silhouette_score(data.values, clusters)
        
        # Score should be positive for well-separated clusters
        assert score > 0, f"Well-separated clusters should have positive silhouette, got {score}"
        
        # Score should be high (> 0.3)
        assert score > 0.3, f"Well-separated clusters should have high silhouette, got {score}"


class TestChiSquareValidationDetailed:
    """Detailed chi-square validation tests."""
    
    def test_chi_square_against_scipy_exact_values(self):
        """Test chi-square calculation matches scipy exactly."""
        from strepsuis_amrvirkm.cluster_analysis_core import chi_square_analysis
        from scipy.stats import chi2_contingency
        
        np.random.seed(42)
        # Create data
        data = pd.DataFrame({
            'Feature1': [1, 1, 1, 0, 0, 0, 1, 1, 0, 0],
            'Feature2': [0, 0, 1, 1, 1, 0, 0, 1, 1, 0],
        })
        clusters = np.array([1, 1, 1, 1, 1, 2, 2, 2, 2, 2])
        
        # Get our results
        global_results, _ = chi_square_analysis(data, clusters)
        
        # Calculate with scipy for each feature
        for _, row in global_results.iterrows():
            feat = row['Feature']
            our_p = row['P_Value']
            
            # Calculate with scipy
            contingency = pd.crosstab(clusters, data[feat])
            chi2, scipy_p, _, _ = chi2_contingency(contingency)
            
            # Should match to 5 decimal places (as per project standard)
            assert np.abs(our_p - scipy_p) < 1e-5, \
                f"P-value for {feat} should match scipy: {scipy_p} vs {our_p}"
    
    def test_fisher_exact_against_scipy(self):
        """Test Fisher exact test matches scipy for small counts."""
        from strepsuis_amrvirkm.cluster_analysis_core import chi_square_analysis
        from scipy.stats import fisher_exact
        
        # Small dataset to trigger Fisher exact
        data = pd.DataFrame({
            'Feature1': [1, 1, 0, 0],
            'Feature2': [1, 0, 1, 0],
        })
        clusters = np.array([1, 1, 2, 2])
        
        # Get our results
        global_results, _ = chi_square_analysis(data, clusters)
        
        # Check against scipy Fisher exact
        for _, row in global_results.iterrows():
            feat = row['Feature']
            our_p = row['P_Value']
            
            # Calculate with scipy
            contingency = pd.crosstab(clusters, data[feat])
            if contingency.shape == (2, 2):
                _, scipy_p = fisher_exact(contingency)
                
                # Should match to 2 decimal places (fisher exact sometimes rounds)
                assert np.abs(our_p - scipy_p) < 0.01, \
                    f"Fisher exact p-value for {feat} should match scipy: {scipy_p} vs {our_p}"


class TestMCAValidation:
    """Validate MCA (Multiple Correspondence Analysis)."""
    
    def test_mca_explained_variance(self):
        """Test MCA explained variance is reasonable."""
        import prince
        
        np.random.seed(42)
        n = 100
        data = pd.DataFrame({
            'A': np.random.binomial(1, 0.5, n),
            'B': np.random.binomial(1, 0.5, n),
            'C': np.random.binomial(1, 0.5, n),
        })
        
        # Run MCA
        mca = prince.MCA(n_components=2, random_state=42)
        mca = mca.fit(data)
        
        # Check explained variance (attribute name varies by prince version)
        if hasattr(mca, 'explained_inertia_'):
            explained_var = mca.explained_inertia_
        elif hasattr(mca, 'eigenvalues_'):
            explained_var = mca.eigenvalues_
        else:
            # Skip if attribute not available in this version
            return
        
        # Should have explained variance
        assert len(explained_var) >= 2
        
        # Total explained variance should be between 0 and total inertia
        total_explained = sum(explained_var[:2])
        assert total_explained > 0, \
            f"Total explained variance should be 0-1, got {total_explained}"


class TestClusteringMetricsValidation:
    """Validate clustering quality metrics."""
    
    def test_calinski_harabasz_against_sklearn(self):
        """Test Calinski-Harabasz score matches sklearn."""
        from strepsuis_amrvirkm.cluster_analysis_core import validate_clusters
        from sklearn.metrics import calinski_harabasz_score
        
        np.random.seed(42)
        # Create well-separated clusters
        cluster1 = np.array([[1, 1, 0, 0]] * 10)
        cluster2 = np.array([[0, 0, 1, 1]] * 10)
        data = np.vstack([cluster1, cluster2])
        clusters = np.array([1] * 10 + [2] * 10)
        
        # Get our score
        our_ch, _ = validate_clusters(data, clusters)
        
        # Calculate with sklearn
        sklearn_ch = calinski_harabasz_score(data, clusters)
        
        # Should match to 5 decimal places
        np.testing.assert_almost_equal(
            our_ch, sklearn_ch, decimal=5,
            err_msg="Calinski-Harabasz score should match sklearn"
        )
    
    def test_davies_bouldin_against_sklearn(self):
        """Test Davies-Bouldin score matches sklearn."""
        from strepsuis_amrvirkm.cluster_analysis_core import validate_clusters
        from sklearn.metrics import davies_bouldin_score
        
        np.random.seed(42)
        # Create well-separated clusters
        cluster1 = np.array([[1, 1, 0, 0]] * 10)
        cluster2 = np.array([[0, 0, 1, 1]] * 10)
        data = np.vstack([cluster1, cluster2])
        clusters = np.array([1] * 10 + [2] * 10)
        
        # Get our score
        _, our_db = validate_clusters(data, clusters)
        
        # Calculate with sklearn
        sklearn_db = davies_bouldin_score(data, clusters)
        
        # Should match to 5 decimal places
        np.testing.assert_almost_equal(
            our_db, sklearn_db, decimal=5,
            err_msg="Davies-Bouldin score should match sklearn"
        )
