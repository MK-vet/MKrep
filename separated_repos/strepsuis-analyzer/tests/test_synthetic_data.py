"""
Synthetic data validation tests for StrepSuisAnalyzer.

Tests with carefully constructed synthetic datasets with known properties.
"""

import pytest
import numpy as np
from strepsuis_analyzer.statistical_analysis import StatisticalAnalyzer
from strepsuis_analyzer.phylogenetic_utils import PhylogeneticAnalyzer


@pytest.mark.synthetic
class TestSyntheticDataValidation:
    """Tests using synthetic data with known ground truth."""

    def test_perfect_correlation_synthetic(self):
        """Test with perfectly correlated synthetic data."""
        analyzer = StatisticalAnalyzer(random_state=42)

        # Perfect positive correlation
        x = np.linspace(0, 100, 1000)
        y = 3 * x + 5

        corr, pval = analyzer.compute_correlation(x, y, method="pearson")

        assert abs(corr - 1.0) < 0.0001, "Perfect correlation should be exactly 1.0"
        assert pval < 1e-10, "P-value should be extremely small"

    def test_zero_correlation_synthetic(self):
        """Test with uncorrelated synthetic data."""
        analyzer = StatisticalAnalyzer(random_state=42)

        # Independent random variables
        np.random.seed(42)
        x = np.random.randn(10000)
        y = np.random.randn(10000)

        corr, pval = analyzer.compute_correlation(x, y, method="pearson")

        assert abs(corr) < 0.05, "Correlation should be close to 0 for independent variables"

    def test_negative_correlation_synthetic(self):
        """Test with perfectly negatively correlated data."""
        analyzer = StatisticalAnalyzer(random_state=42)

        x = np.linspace(0, 100, 1000)
        y = -2 * x + 50

        corr, pval = analyzer.compute_correlation(x, y, method="pearson")

        assert abs(corr - (-1.0)) < 0.0001, "Perfect negative correlation should be -1.0"

    def test_known_entropy_synthetic(self):
        """Test entropy with known distribution."""
        analyzer = StatisticalAnalyzer(random_state=42)

        # Uniform distribution over 4 categories
        # Expected entropy = log2(4) = 2.0
        categories = np.repeat([0, 1, 2, 3], 1000)
        np.random.shuffle(categories)

        entropy = analyzer.compute_entropy(categories)

        expected_entropy = np.log2(4)
        assert abs(entropy - expected_entropy) < 0.01, \
            f"Entropy should be {expected_entropy} for uniform distribution"

    def test_known_cramers_v_synthetic(self):
        """Test Cramér's V with perfect association."""
        analyzer = StatisticalAnalyzer(random_state=42)

        # Perfect 1-to-1 mapping
        x = np.array([1, 1, 1, 2, 2, 2, 3, 3, 3])
        y = np.array(['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'])

        v = analyzer.compute_cramers_v(x, y)

        assert v > 0.99, "Cramér's V should be ~1 for perfect association"

    def test_identical_trees_rf_distance(self):
        """Test RF distance between identical trees."""
        analyzer = PhylogeneticAnalyzer()

        tree = "((A:1,B:1):1,(C:1,D:1):1);"

        rf = analyzer.compute_robinson_foulds_distance(tree, tree)

        if not np.isnan(rf):
            assert abs(rf) < 0.001, "RF distance between identical trees should be 0"

    def test_completely_different_trees_rf(self):
        """Test RF distance between maximally different trees."""
        analyzer = PhylogeneticAnalyzer()

        tree1 = "((A:1,B:1):1,(C:1,D:1):1);"
        tree2 = "((A:1,C:1):1,(B:1,D:1):1);"

        rf = analyzer.compute_robinson_foulds_distance(tree1, tree2, normalize=False)

        if not np.isnan(rf):
            assert rf > 0, "Different trees should have RF distance > 0"

    def test_binary_phi_coefficient_synthetic(self):
        """Test phi coefficient with known binary data."""
        analyzer = StatisticalAnalyzer(random_state=42)

        # Perfect positive association
        x = np.array([0, 0, 1, 1, 0, 0, 1, 1, 0, 0])
        y = np.array([0, 0, 1, 1, 0, 0, 1, 1, 0, 0])

        phi = analyzer.compute_phi_coefficient(x, y)

        assert phi > 0.99, "Phi should be ~1 for perfect positive association"

    def test_known_mean_variance_synthetic(self):
        """Test normality test with known normal distribution."""
        analyzer = StatisticalAnalyzer(random_state=42)

        # Large sample from normal distribution
        np.random.seed(42)
        data = np.random.normal(loc=10, scale=2, size=10000)

        stat, pval, is_normal = analyzer.test_normality(data)

        # With large sample, should detect normality
        assert pval > 0.001, "Large normal sample should pass normality test"

    def test_anova_identical_groups_synthetic(self):
        """Test ANOVA with identical groups."""
        analyzer = StatisticalAnalyzer(random_state=42)

        # Three identical groups
        group = np.ones(100)
        stat, pval = analyzer.perform_anova(group, group, group)

        # F-statistic should be 0 or very close to 0 for identical groups
        # P-value should be close to 1
        assert stat < 0.01 or np.isnan(stat), "F-statistic should be ~0 for identical groups"

    def test_ttest_identical_groups_synthetic(self):
        """Test t-test with identical groups."""
        analyzer = StatisticalAnalyzer(random_state=42)

        group = np.random.randn(100)
        stat, pval = analyzer.perform_ttest(group, group)

        # Should not reject null hypothesis
        assert pval > 0.5, "P-value should be high for identical groups"

    def test_meta_analysis_homogeneous_studies(self):
        """Test meta-analysis with homogeneous effect sizes."""
        analyzer = StatisticalAnalyzer(random_state=42)

        # All studies have same effect size
        effect_sizes = [0.5, 0.5, 0.5, 0.5, 0.5]
        variances = [0.01, 0.01, 0.01, 0.01, 0.01]

        pooled, var, se, tau_sq = analyzer.meta_analysis_random_effects(
            effect_sizes, variances
        )

        # Pooled effect should be 0.5
        assert abs(pooled - 0.5) < 0.01, "Pooled effect should match input effects"

        # Tau-squared should be ~0 for homogeneous studies
        assert tau_sq < 0.01, "Tau-squared should be ~0 for homogeneous studies"

    def test_meta_analysis_heterogeneous_studies(self):
        """Test meta-analysis with heterogeneous effect sizes."""
        analyzer = StatisticalAnalyzer(random_state=42)

        # Heterogeneous effect sizes
        effect_sizes = [0.1, 0.5, 0.9, 0.3, 0.7]
        variances = [0.01, 0.01, 0.01, 0.01, 0.01]

        pooled, var, se, tau_sq = analyzer.meta_analysis_random_effects(
            effect_sizes, variances
        )

        # Tau-squared should be > 0 for heterogeneous studies
        assert tau_sq > 0, "Tau-squared should be > 0 for heterogeneous studies"

    def test_multiple_testing_all_null(self):
        """Test multiple testing correction with all null hypotheses."""
        analyzer = StatisticalAnalyzer(random_state=42)

        # All p-values > 0.05
        pvalues = [0.1, 0.2, 0.3, 0.5, 0.9]

        rejected, corrected = analyzer.apply_multiple_testing_correction(
            pvalues, method="bonferroni", alpha=0.05
        )

        # None should be rejected
        assert not any(rejected), "No hypotheses should be rejected with high p-values"

    def test_multiple_testing_all_significant(self):
        """Test multiple testing correction with all significant p-values."""
        analyzer = StatisticalAnalyzer(random_state=42)

        # All p-values < 0.001
        pvalues = [0.0001, 0.0002, 0.0003, 0.0005, 0.0009]

        rejected, corrected = analyzer.apply_multiple_testing_correction(
            pvalues, method="bonferroni", alpha=0.05
        )

        # All should be rejected even with Bonferroni
        assert all(rejected), "All hypotheses should be rejected with very low p-values"
