"""
Statistical analysis utilities for StrepSuisAnalyzer.

Provides comprehensive statistical tests including correlations, hypothesis tests,
meta-analysis, and multiple testing corrections.
"""

from typing import Dict, List, Optional, Tuple, Union
import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency, shapiro, pearsonr, spearmanr, kendalltau
from statsmodels.stats.multitest import multipletests
import warnings


class StatisticalAnalyzer:
    """Performs statistical analysis on genomic and phenotypic data."""

    def __init__(self, random_state: Optional[int] = None):
        """
        Initialize the StatisticalAnalyzer.

        Args:
            random_state: Random seed for reproducibility
        """
        self.random_state = random_state
        if random_state is not None:
            np.random.seed(random_state)

    def compute_correlation(
        self,
        x: Union[pd.Series, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        method: str = "pearson",
    ) -> Tuple[float, float]:
        """
        Compute correlation coefficient between two variables.

        Args:
            x: First variable
            y: Second variable
            method: Correlation method ('pearson', 'spearman', 'kendall')

        Returns:
            Tuple of (correlation_coefficient, p_value)

        Raises:
            ValueError: If method is not supported
        """
        # Convert to numpy arrays and remove NaN
        x_arr = np.asarray(x)
        y_arr = np.asarray(y)

        mask = ~(np.isnan(x_arr) | np.isnan(y_arr))
        x_clean = x_arr[mask]
        y_clean = y_arr[mask]

        if len(x_clean) < 3:
            return np.nan, np.nan

        if method == "pearson":
            corr, pval = pearsonr(x_clean, y_clean)
        elif method == "spearman":
            corr, pval = spearmanr(x_clean, y_clean)
        elif method == "kendall":
            corr, pval = kendalltau(x_clean, y_clean)
        else:
            raise ValueError(f"Unsupported correlation method: {method}")

        return float(corr), float(pval)

    def compute_phi_coefficient(
        self, x: Union[pd.Series, np.ndarray], y: Union[pd.Series, np.ndarray]
    ) -> float:
        """
        Compute phi coefficient for two binary variables.

        Args:
            x: First binary variable
            y: Second binary variable

        Returns:
            Phi coefficient value

        Raises:
            ValueError: If variables are not binary
        """
        x_arr = np.asarray(x).astype(float)
        y_arr = np.asarray(y).astype(float)

        # Remove NaN
        mask = ~(np.isnan(x_arr) | np.isnan(y_arr))
        x_clean = x_arr[mask]
        y_clean = y_arr[mask]

        # Check if binary
        unique_x = np.unique(x_clean)
        unique_y = np.unique(y_clean)

        if not (set(unique_x).issubset({0, 1, 0.0, 1.0}) and set(unique_y).issubset({0, 1, 0.0, 1.0})):
            raise ValueError("Variables must be binary (0/1)")

        # Create contingency table
        contingency = pd.crosstab(x_clean, y_clean)

        # Ensure 2x2 table
        for val in [0, 1]:
            if val not in contingency.index:
                contingency.loc[val] = 0
            if val not in contingency.columns:
                contingency[val] = 0

        contingency = contingency.loc[[0, 1], [0, 1]]

        # Compute phi coefficient manually
        n = contingency.sum().sum()
        if n == 0:
            return np.nan

        a = contingency.loc[0, 0]
        b = contingency.loc[0, 1]
        c = contingency.loc[1, 0]
        d = contingency.loc[1, 1]

        # Phi = (ad - bc) / sqrt((a+b)(c+d)(a+c)(b+d))
        numerator = (a * d) - (b * c)
        denominator = np.sqrt((a + b) * (c + d) * (a + c) * (b + d))

        if denominator == 0:
            return 0.0

        phi = numerator / denominator

        return float(phi)

    def compute_cramers_v(
        self, x: Union[pd.Series, np.ndarray], y: Union[pd.Series, np.ndarray]
    ) -> float:
        """
        Compute Cramér's V for categorical variables.

        Args:
            x: First categorical variable
            y: Second categorical variable

        Returns:
            Cramér's V value (0 to 1)
        """
        x_arr = np.asarray(x)
        y_arr = np.asarray(y)

        # Remove NaN
        mask = ~(pd.isna(x_arr) | pd.isna(y_arr))
        x_clean = x_arr[mask]
        y_clean = y_arr[mask]

        if len(x_clean) < 2:
            return np.nan

        # Create contingency table
        contingency = pd.crosstab(x_clean, y_clean)

        # Compute chi-square
        chi2, _, _, _ = chi2_contingency(contingency)
        n = contingency.sum().sum()

        # Cramér's V
        min_dim = min(contingency.shape[0] - 1, contingency.shape[1] - 1)
        if min_dim == 0:
            return 0.0

        cramers_v = np.sqrt(chi2 / (n * min_dim))

        return float(np.clip(cramers_v, 0, 1))

    def test_normality(
        self, data: Union[pd.Series, np.ndarray]
    ) -> Tuple[float, float, bool]:
        """
        Test normality using Shapiro-Wilk test.

        Args:
            data: Data to test

        Returns:
            Tuple of (statistic, p_value, is_normal)
        """
        data_arr = np.asarray(data).astype(float)
        data_clean = data_arr[~np.isnan(data_arr)]

        if len(data_clean) < 3:
            return np.nan, np.nan, False

        stat, pval = shapiro(data_clean)
        is_normal = bool(pval > 0.05)

        return float(stat), float(pval), is_normal

    def perform_ttest(
        self,
        group1: Union[pd.Series, np.ndarray],
        group2: Union[pd.Series, np.ndarray],
        paired: bool = False,
    ) -> Tuple[float, float]:
        """
        Perform t-test.

        Args:
            group1: First group
            group2: Second group
            paired: Whether to perform paired t-test

        Returns:
            Tuple of (statistic, p_value)
        """
        g1 = np.asarray(group1)
        g2 = np.asarray(group2)

        g1_clean = g1[~np.isnan(g1)]
        g2_clean = g2[~np.isnan(g2)]

        if len(g1_clean) < 2 or len(g2_clean) < 2:
            return np.nan, np.nan

        if paired:
            if len(g1_clean) != len(g2_clean):
                raise ValueError("Paired t-test requires equal sample sizes")
            stat, pval = stats.ttest_rel(g1_clean, g2_clean)
        else:
            stat, pval = stats.ttest_ind(g1_clean, g2_clean)

        return float(stat), float(pval)

    def perform_mann_whitney(
        self, group1: Union[pd.Series, np.ndarray], group2: Union[pd.Series, np.ndarray]
    ) -> Tuple[float, float]:
        """
        Perform Mann-Whitney U test.

        Args:
            group1: First group
            group2: Second group

        Returns:
            Tuple of (statistic, p_value)
        """
        g1 = np.asarray(group1)
        g2 = np.asarray(group2)

        g1_clean = g1[~np.isnan(g1)]
        g2_clean = g2[~np.isnan(g2)]

        if len(g1_clean) < 2 or len(g2_clean) < 2:
            return np.nan, np.nan

        stat, pval = stats.mannwhitneyu(g1_clean, g2_clean, alternative="two-sided")

        return float(stat), float(pval)

    def perform_anova(self, *groups) -> Tuple[float, float]:
        """
        Perform one-way ANOVA.

        Args:
            *groups: Variable number of groups

        Returns:
            Tuple of (F_statistic, p_value)
        """
        clean_groups = []
        for group in groups:
            g = np.asarray(group)
            g_clean = g[~np.isnan(g)]
            if len(g_clean) >= 2:
                clean_groups.append(g_clean)

        if len(clean_groups) < 2:
            return np.nan, np.nan

        stat, pval = stats.f_oneway(*clean_groups)

        return float(stat), float(pval)

    def perform_kruskal_wallis(self, *groups) -> Tuple[float, float]:
        """
        Perform Kruskal-Wallis H test.

        Args:
            *groups: Variable number of groups

        Returns:
            Tuple of (H_statistic, p_value)
        """
        clean_groups = []
        for group in groups:
            g = np.asarray(group)
            g_clean = g[~np.isnan(g)]
            if len(g_clean) >= 2:
                clean_groups.append(g_clean)

        if len(clean_groups) < 2:
            return np.nan, np.nan

        stat, pval = stats.kruskal(*clean_groups)

        return float(stat), float(pval)

    def apply_multiple_testing_correction(
        self, pvalues: List[float], method: str = "fdr_bh", alpha: float = 0.05
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Apply multiple testing correction.

        Args:
            pvalues: List of p-values
            method: Correction method ('bonferroni', 'fdr_bh', 'fdr_by')
            alpha: Significance level

        Returns:
            Tuple of (rejected, corrected_pvalues)
        """
        pvalues_arr = np.asarray(pvalues)

        # Remove NaN
        valid_mask = ~np.isnan(pvalues_arr)
        valid_pvalues = pvalues_arr[valid_mask]

        if len(valid_pvalues) == 0:
            return np.array([]), np.array([])

        rejected, corrected, _, _ = multipletests(
            valid_pvalues, alpha=alpha, method=method, is_sorted=False
        )

        # Reconstruct full arrays with NaN
        full_rejected = np.full(len(pvalues_arr), False)
        full_corrected = np.full(len(pvalues_arr), np.nan)

        full_rejected[valid_mask] = rejected
        full_corrected[valid_mask] = corrected

        return full_rejected, full_corrected

    def compute_entropy(self, data: Union[pd.Series, np.ndarray]) -> float:
        """
        Compute Shannon entropy.

        Args:
            data: Data array

        Returns:
            Entropy value (bits)
        """
        # Convert to array and handle numeric/categorical data
        if isinstance(data, pd.Series):
            data_arr = data.values
        else:
            data_arr = np.asarray(data)

        # Remove NaN values for numeric data
        try:
            data_clean = data_arr[~pd.isna(data_arr)]
        except TypeError:
            # Handle non-numeric data
            data_clean = data_arr[pd.notna(data_arr)]

        if len(data_clean) == 0:
            return 0.0

        # Get value counts
        values, counts = np.unique(data_clean, return_counts=True)
        probabilities = counts / len(data_clean)

        # Compute entropy
        entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))

        return float(entropy)

    def compute_mutual_information(
        self, x: Union[pd.Series, np.ndarray], y: Union[pd.Series, np.ndarray]
    ) -> float:
        """
        Compute mutual information between two variables.

        Args:
            x: First variable
            y: Second variable

        Returns:
            Mutual information value (bits)
        """
        x_arr = np.asarray(x)
        y_arr = np.asarray(y)

        # Remove NaN
        mask = ~(np.isnan(x_arr) | np.isnan(y_arr))
        x_clean = x_arr[mask]
        y_clean = y_arr[mask]

        if len(x_clean) == 0:
            return 0.0

        # Compute entropies
        h_x = self.compute_entropy(x_clean)
        h_y = self.compute_entropy(y_clean)

        # Joint entropy
        xy_pairs = list(zip(x_clean, y_clean))
        unique_pairs, counts = np.unique(xy_pairs, axis=0, return_counts=True)
        probabilities = counts / len(xy_pairs)
        h_xy = -np.sum(probabilities * np.log2(probabilities + 1e-10))

        # Mutual information
        mi = h_x + h_y - h_xy

        return float(max(0.0, mi))  # MI cannot be negative

    def meta_analysis_fixed_effects(
        self, effect_sizes: List[float], variances: List[float]
    ) -> Tuple[float, float, float]:
        """
        Perform fixed-effects meta-analysis.

        Args:
            effect_sizes: List of effect sizes
            variances: List of variances

        Returns:
            Tuple of (pooled_effect, pooled_variance, pooled_se)
        """
        effect_sizes_arr = np.asarray(effect_sizes)
        variances_arr = np.asarray(variances)

        # Remove invalid values
        mask = ~(np.isnan(effect_sizes_arr) | np.isnan(variances_arr) | (variances_arr <= 0))
        es = effect_sizes_arr[mask]
        var = variances_arr[mask]

        if len(es) == 0:
            return np.nan, np.nan, np.nan

        # Weights = 1 / variance
        weights = 1.0 / var

        # Pooled effect
        pooled_effect = np.sum(weights * es) / np.sum(weights)

        # Pooled variance
        pooled_variance = 1.0 / np.sum(weights)

        # Pooled SE
        pooled_se = np.sqrt(pooled_variance)

        return float(pooled_effect), float(pooled_variance), float(pooled_se)

    def meta_analysis_random_effects(
        self, effect_sizes: List[float], variances: List[float]
    ) -> Tuple[float, float, float, float]:
        """
        Perform random-effects meta-analysis using DerSimonian-Laird method.

        Args:
            effect_sizes: List of effect sizes
            variances: List of variances

        Returns:
            Tuple of (pooled_effect, pooled_variance, pooled_se, tau_squared)
        """
        effect_sizes_arr = np.asarray(effect_sizes)
        variances_arr = np.asarray(variances)

        # Remove invalid values
        mask = ~(np.isnan(effect_sizes_arr) | np.isnan(variances_arr) | (variances_arr <= 0))
        es = effect_sizes_arr[mask]
        var = variances_arr[mask]

        if len(es) < 2:
            return np.nan, np.nan, np.nan, np.nan

        # Fixed-effects estimate
        weights = 1.0 / var
        fe_effect = np.sum(weights * es) / np.sum(weights)

        # Cochran's Q
        q = np.sum(weights * (es - fe_effect) ** 2)
        df = len(es) - 1

        # Tau-squared (between-study variance)
        c = np.sum(weights) - np.sum(weights**2) / np.sum(weights)
        tau_squared = max(0, (q - df) / c)

        # Random-effects weights
        re_weights = 1.0 / (var + tau_squared)

        # Pooled effect
        pooled_effect = np.sum(re_weights * es) / np.sum(re_weights)

        # Pooled variance
        pooled_variance = 1.0 / np.sum(re_weights)

        # Pooled SE
        pooled_se = np.sqrt(pooled_variance)

        return float(pooled_effect), float(pooled_variance), float(pooled_se), float(tau_squared)

    def cochrans_q_test(
        self, effect_sizes: List[float], variances: List[float]
    ) -> Tuple[float, float]:
        """
        Perform Cochran's Q test for heterogeneity.

        Args:
            effect_sizes: List of effect sizes
            variances: List of variances

        Returns:
            Tuple of (Q_statistic, p_value)
        """
        effect_sizes_arr = np.asarray(effect_sizes)
        variances_arr = np.asarray(variances)

        # Remove invalid values
        mask = ~(np.isnan(effect_sizes_arr) | np.isnan(variances_arr) | (variances_arr <= 0))
        es = effect_sizes_arr[mask]
        var = variances_arr[mask]

        if len(es) < 2:
            return np.nan, np.nan

        # Fixed-effects estimate
        weights = 1.0 / var
        fe_effect = np.sum(weights * es) / np.sum(weights)

        # Cochran's Q
        q = np.sum(weights * (es - fe_effect) ** 2)
        df = len(es) - 1

        # P-value from chi-square distribution
        pval = 1 - stats.chi2.cdf(q, df)

        return float(q), float(pval)
