"""
Mathematical validation tests for StrepSuisAnalyzer.

Tests mathematical properties and invariants of statistical functions.
"""

import pytest
import pandas as pd
import numpy as np
from strepsuis_analyzer.statistical_analysis import StatisticalAnalyzer
from strepsuis_analyzer.phylogenetic_utils import PhylogeneticAnalyzer


@pytest.mark.mathematical
class TestMathematicalValidation:
    """Test mathematical properties and invariants."""

    def test_entropy_bounds(self):
        """Test that entropy is non-negative and bounded by log2(n)."""
        analyzer = StatisticalAnalyzer(random_state=42)

        # Uniform distribution over n categories should give log2(n)
        n = 8
        uniform = np.repeat(range(n), 100)  # Each category appears 100 times
        entropy = analyzer.compute_entropy(uniform)

        assert entropy >= 0, "Entropy must be non-negative"
        assert entropy <= np.log2(n) + 0.01, f"Entropy must be <= log2({n})"

        # Single value should give entropy = 0
        constant = np.ones(100)
        entropy_zero = analyzer.compute_entropy(constant)
        assert abs(entropy_zero) < 0.001, "Entropy of constant should be ~0"

    def test_mutual_information_symmetry(self):
        """Test that MI(X,Y) = MI(Y,X)."""
        analyzer = StatisticalAnalyzer(random_state=42)

        np.random.seed(42)
        x = np.random.randint(0, 5, 100)
        y = np.random.randint(0, 3, 100)

        mi_xy = analyzer.compute_mutual_information(x, y)
        mi_yx = analyzer.compute_mutual_information(y, x)

        assert abs(mi_xy - mi_yx) < 0.001, "Mutual information must be symmetric"

    def test_mutual_information_non_negative(self):
        """Test that mutual information is non-negative."""
        analyzer = StatisticalAnalyzer(random_state=42)

        np.random.seed(42)
        x = np.random.randint(0, 5, 100)
        y = np.random.randint(0, 3, 100)

        mi = analyzer.compute_mutual_information(x, y)

        assert mi >= 0, "Mutual information must be non-negative"

    def test_cramers_v_bounds(self):
        """Test that Cramér's V is between 0 and 1."""
        analyzer = StatisticalAnalyzer(random_state=42)

        np.random.seed(42)
        x = np.random.choice(["A", "B", "C"], size=100)
        y = np.random.choice(["X", "Y", "Z"], size=100)

        v = analyzer.compute_cramers_v(x, y)

        assert 0 <= v <= 1, "Cramér's V must be between 0 and 1"

    def test_cramers_v_perfect_association(self):
        """Test that Cramér's V = 1 for perfect association."""
        analyzer = StatisticalAnalyzer(random_state=42)

        # Perfect 1-to-1 mapping
        x = np.array(["A", "A", "B", "B", "C", "C"])
        y = np.array(["X", "X", "Y", "Y", "Z", "Z"])

        v = analyzer.compute_cramers_v(x, y)

        assert v > 0.99, "Cramér's V should be ~1 for perfect association"

    def test_cramers_v_no_association(self):
        """Test that Cramér's V ≈ 0 for independent variables."""
        analyzer = StatisticalAnalyzer(random_state=42)

        np.random.seed(42)
        # Large sample for independence
        x = np.random.choice(["A", "B"], size=10000)
        y = np.random.choice(["X", "Y"], size=10000)

        v = analyzer.compute_cramers_v(x, y)

        assert v < 0.1, "Cramér's V should be ~0 for independent variables"

    def test_phi_coefficient_bounds(self):
        """Test that phi coefficient is between -1 and 1."""
        analyzer = StatisticalAnalyzer(random_state=42)

        np.random.seed(42)
        x = np.random.randint(0, 2, 100)
        y = np.random.randint(0, 2, 100)

        phi = analyzer.compute_phi_coefficient(x, y)

        assert -1 <= phi <= 1, "Phi coefficient must be between -1 and 1"

    def test_phi_coefficient_perfect_positive(self):
        """Test phi coefficient for perfectly positively associated variables."""
        analyzer = StatisticalAnalyzer(random_state=42)

        x = np.array([0, 0, 1, 1, 0, 0, 1, 1])
        y = np.array([0, 0, 1, 1, 0, 0, 1, 1])

        phi = analyzer.compute_phi_coefficient(x, y)

        assert phi > 0.99, "Phi should be ~1 for perfect positive association"

    def test_correlation_bounds(self):
        """Test that correlation coefficients are between -1 and 1."""
        analyzer = StatisticalAnalyzer(random_state=42)

        np.random.seed(42)
        x = np.random.randn(100)
        y = np.random.randn(100)

        for method in ["pearson", "spearman", "kendall"]:
            corr, pval = analyzer.compute_correlation(x, y, method=method)

            assert -1 <= corr <= 1, f"{method} correlation must be in [-1, 1]"
            assert 0 <= pval <= 1, "P-value must be in [0, 1]"

    def test_correlation_perfect_positive(self):
        """Test perfect positive correlation."""
        analyzer = StatisticalAnalyzer(random_state=42)

        x = np.linspace(0, 10, 100)
        y = 2 * x + 3  # Perfect linear relationship

        corr, pval = analyzer.compute_correlation(x, y, method="pearson")

        assert abs(corr - 1.0) < 0.001, "Perfect positive correlation should be ~1"

    def test_correlation_perfect_negative(self):
        """Test perfect negative correlation."""
        analyzer = StatisticalAnalyzer(random_state=42)

        x = np.linspace(0, 10, 100)
        y = -2 * x + 3  # Perfect negative linear relationship

        corr, pval = analyzer.compute_correlation(x, y, method="pearson")

        assert abs(corr - (-1.0)) < 0.001, "Perfect negative correlation should be ~-1"

    def test_pvalue_bounds_ttest(self):
        """Test that t-test p-values are in [0, 1]."""
        analyzer = StatisticalAnalyzer(random_state=42)

        np.random.seed(42)
        group1 = np.random.randn(30)
        group2 = np.random.randn(30)

        stat, pval = analyzer.perform_ttest(group1, group2)

        assert 0 <= pval <= 1, "P-value must be in [0, 1]"

    def test_pvalue_bounds_anova(self):
        """Test that ANOVA p-values are in [0, 1]."""
        analyzer = StatisticalAnalyzer(random_state=42)

        np.random.seed(42)
        groups = [np.random.randn(20) for _ in range(3)]

        stat, pval = analyzer.perform_anova(*groups)

        assert 0 <= pval <= 1, "P-value must be in [0, 1]"
        assert stat >= 0, "F-statistic must be non-negative"

    def test_pvalue_bounds_kruskal(self):
        """Test that Kruskal-Wallis p-values are in [0, 1]."""
        analyzer = StatisticalAnalyzer(random_state=42)

        np.random.seed(42)
        groups = [np.random.randn(20) for _ in range(3)]

        stat, pval = analyzer.perform_kruskal_wallis(*groups)

        assert 0 <= pval <= 1, "P-value must be in [0, 1]"
        assert stat >= 0, "H-statistic must be non-negative"

    def test_robinson_foulds_distance_bounds(self, sample_tree_newick):
        """Test that Robinson-Foulds distance is non-negative."""
        analyzer = PhylogeneticAnalyzer()

        # Identical trees should have RF distance = 0
        rf = analyzer.compute_robinson_foulds_distance(
            sample_tree_newick, sample_tree_newick
        )

        if not np.isnan(rf):
            assert rf >= 0, "RF distance must be non-negative"
            assert abs(rf) < 0.001, "Identical trees should have RF distance = 0"

    def test_robinson_foulds_normalized_bounds(self, sample_tree_newick):
        """Test that normalized RF distance is in [0, 1]."""
        analyzer = PhylogeneticAnalyzer()

        rf = analyzer.compute_robinson_foulds_distance(
            sample_tree_newick, sample_tree_newick, normalize=True
        )

        if not np.isnan(rf):
            assert 0 <= rf <= 1, "Normalized RF distance must be in [0, 1]"

    def test_meta_analysis_variance_positive(self, meta_analysis_data):
        """Test that meta-analysis variances are positive."""
        analyzer = StatisticalAnalyzer(random_state=42)

        # Fixed effects
        _, var_fe, se_fe = analyzer.meta_analysis_fixed_effects(
            meta_analysis_data["effect_sizes"],
            meta_analysis_data["variances"]
        )

        assert var_fe > 0, "Fixed-effects variance must be positive"
        assert se_fe > 0, "Fixed-effects SE must be positive"

        # Random effects
        _, var_re, se_re, tau_sq = analyzer.meta_analysis_random_effects(
            meta_analysis_data["effect_sizes"],
            meta_analysis_data["variances"]
        )

        assert var_re > 0, "Random-effects variance must be positive"
        assert se_re > 0, "Random-effects SE must be positive"
        assert tau_sq >= 0, "Tau-squared must be non-negative"

    def test_cochrans_q_bounds(self, meta_analysis_data):
        """Test that Cochran's Q and p-value are in valid ranges."""
        analyzer = StatisticalAnalyzer(random_state=42)

        q, pval = analyzer.cochrans_q_test(
            meta_analysis_data["effect_sizes"],
            meta_analysis_data["variances"]
        )

        assert q >= 0, "Cochran's Q must be non-negative"
        assert 0 <= pval <= 1, "P-value must be in [0, 1]"

    def test_multiple_testing_correction_bounds(self):
        """Test that corrected p-values are in [0, 1]."""
        analyzer = StatisticalAnalyzer(random_state=42)

        pvalues = [0.001, 0.01, 0.05, 0.1, 0.5]

        for method in ["bonferroni", "fdr_bh"]:
            rejected, corrected = analyzer.apply_multiple_testing_correction(
                pvalues, method=method
            )

            # Remove NaN values
            valid_corrected = corrected[~np.isnan(corrected)]

            assert np.all((valid_corrected >= 0) & (valid_corrected <= 1)), \
                f"Corrected p-values must be in [0, 1] for {method}"
