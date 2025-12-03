"""Tests for statistical analysis module."""

import pytest
import pandas as pd
import numpy as np
from strepsuis_analyzer.statistical_analysis import StatisticalAnalyzer


class TestStatisticalAnalyzer:
    """Test suite for StatisticalAnalyzer class."""

    def test_init(self):
        """Test analyzer initialization."""
        analyzer = StatisticalAnalyzer(random_state=42)
        assert analyzer.random_state == 42

    def test_compute_correlation_pearson(self, correlation_data_perfect):
        """Test Pearson correlation with perfect correlation."""
        analyzer = StatisticalAnalyzer()
        corr, pval = analyzer.compute_correlation(
            correlation_data_perfect["x"],
            correlation_data_perfect["y"],
            method="pearson"
        )
        assert abs(corr - 1.0) < 0.001
        assert pval < 0.001

    def test_compute_correlation_spearman(self, sample_numeric_data):
        """Test Spearman correlation."""
        analyzer = StatisticalAnalyzer()
        corr, pval = analyzer.compute_correlation(
            sample_numeric_data["var_0"],
            sample_numeric_data["var_1"],
            method="spearman"
        )
        assert -1 <= corr <= 1
        assert 0 <= pval <= 1

    def test_compute_correlation_kendall(self, sample_numeric_data):
        """Test Kendall correlation."""
        analyzer = StatisticalAnalyzer()
        corr, pval = analyzer.compute_correlation(
            sample_numeric_data["var_0"],
            sample_numeric_data["var_1"],
            method="kendall"
        )
        assert -1 <= corr <= 1
        assert 0 <= pval <= 1

    def test_compute_phi_coefficient(self, sample_binary_data):
        """Test phi coefficient calculation."""
        analyzer = StatisticalAnalyzer()
        phi = analyzer.compute_phi_coefficient(
            sample_binary_data["gene_0"],
            sample_binary_data["gene_1"]
        )
        assert 0 <= abs(phi) <= 1

    def test_compute_cramers_v(self, sample_categorical_data):
        """Test Cramér's V calculation."""
        analyzer = StatisticalAnalyzer()
        np.random.seed(42)
        cat2 = pd.Series(np.random.choice(["X", "Y", "Z"], size=len(sample_categorical_data)))
        v = analyzer.compute_cramers_v(sample_categorical_data, cat2)
        assert 0 <= v <= 1

    def test_test_normality(self, normal_distribution_data):
        """Test normality testing."""
        analyzer = StatisticalAnalyzer()
        stat, pval, is_normal = analyzer.test_normality(normal_distribution_data)
        assert 0 <= pval <= 1
        assert isinstance(is_normal, bool)

    def test_perform_ttest(self, sample_numeric_data):
        """Test t-test."""
        analyzer = StatisticalAnalyzer()
        group1 = sample_numeric_data["var_0"][:25]
        group2 = sample_numeric_data["var_0"][25:]
        stat, pval = analyzer.perform_ttest(group1, group2)
        assert 0 <= pval <= 1

    def test_perform_mann_whitney(self, sample_numeric_data):
        """Test Mann-Whitney U test."""
        analyzer = StatisticalAnalyzer()
        group1 = sample_numeric_data["var_0"][:25]
        group2 = sample_numeric_data["var_0"][25:]
        stat, pval = analyzer.perform_mann_whitney(group1, group2)
        assert 0 <= pval <= 1

    def test_perform_anova(self, sample_numeric_data):
        """Test ANOVA."""
        analyzer = StatisticalAnalyzer()
        groups = [sample_numeric_data["var_0"][:15],
                  sample_numeric_data["var_0"][15:30],
                  sample_numeric_data["var_0"][30:]]
        stat, pval = analyzer.perform_anova(*groups)
        assert 0 <= pval <= 1

    def test_perform_kruskal_wallis(self, sample_numeric_data):
        """Test Kruskal-Wallis test."""
        analyzer = StatisticalAnalyzer()
        groups = [sample_numeric_data["var_0"][:15],
                  sample_numeric_data["var_0"][15:30],
                  sample_numeric_data["var_0"][30:]]
        stat, pval = analyzer.perform_kruskal_wallis(*groups)
        assert 0 <= pval <= 1

    def test_apply_multiple_testing_correction(self):
        """Test multiple testing correction."""
        analyzer = StatisticalAnalyzer()
        pvalues = [0.01, 0.05, 0.03, 0.001, 0.5]
        rejected, corrected = analyzer.apply_multiple_testing_correction(pvalues, method="fdr_bh")
        assert len(rejected) == len(pvalues)
        assert len(corrected) == len(pvalues)

    def test_compute_entropy(self, sample_categorical_data):
        """Test entropy calculation."""
        analyzer = StatisticalAnalyzer()
        entropy = analyzer.compute_entropy(sample_categorical_data)
        assert entropy >= 0
        # Maximum entropy for 4 categories is log2(4) = 2
        assert entropy <= 2

    def test_compute_mutual_information(self, sample_binary_data):
        """Test mutual information calculation."""
        analyzer = StatisticalAnalyzer()
        mi = analyzer.compute_mutual_information(
            sample_binary_data["gene_0"],
            sample_binary_data["gene_1"]
        )
        assert mi >= 0

    def test_meta_analysis_fixed_effects(self, meta_analysis_data):
        """Test fixed-effects meta-analysis."""
        analyzer = StatisticalAnalyzer()
        pooled_effect, pooled_var, pooled_se = analyzer.meta_analysis_fixed_effects(
            meta_analysis_data["effect_sizes"],
            meta_analysis_data["variances"]
        )
        assert not np.isnan(pooled_effect)
        assert pooled_var > 0
        assert pooled_se > 0

    def test_meta_analysis_random_effects(self, meta_analysis_data):
        """Test random-effects meta-analysis."""
        analyzer = StatisticalAnalyzer()
        pooled_effect, pooled_var, pooled_se, tau_sq = analyzer.meta_analysis_random_effects(
            meta_analysis_data["effect_sizes"],
            meta_analysis_data["variances"]
        )
        assert not np.isnan(pooled_effect)
        assert pooled_var > 0
        assert pooled_se > 0
        assert tau_sq >= 0

    def test_cochrans_q_test(self, meta_analysis_data):
        """Test Cochran's Q test."""
        analyzer = StatisticalAnalyzer()
        q, pval = analyzer.cochrans_q_test(
            meta_analysis_data["effect_sizes"],
            meta_analysis_data["variances"]
        )
        assert q >= 0
        assert 0 <= pval <= 1
