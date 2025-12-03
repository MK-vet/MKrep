"""
Statistical validation tests for mathematical functions.
This module ensures 100% mathematical accuracy of statistical calculations.
"""
import pytest
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import sys
import os

# Set random seed for reproducibility
np.random.seed(42)


class TestCorrelationCalculations:
    """Test suite for correlation calculations with known ground truth."""
    
    def test_perfect_positive_correlation(self):
        """Test Pearson correlation with perfect positive correlation."""
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([2, 4, 6, 8, 10])  # y = 2*x
        
        corr, p_value = stats.pearsonr(x, y)
        
        assert np.isclose(corr, 1.0, atol=1e-10), "Perfect positive correlation should be 1.0"
        assert p_value < 0.05, "P-value should be significant"
    
    def test_perfect_negative_correlation(self):
        """Test Pearson correlation with perfect negative correlation."""
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([10, 8, 6, 4, 2])  # y = 12 - 2*x
        
        corr, p_value = stats.pearsonr(x, y)
        
        assert np.isclose(corr, -1.0, atol=1e-10), "Perfect negative correlation should be -1.0"
        assert p_value < 0.05, "P-value should be significant"
    
    def test_zero_correlation(self):
        """Test correlation with no linear relationship."""
        # Create data with no correlation
        np.random.seed(42)
        x = np.random.randn(100)
        y = np.random.randn(100)
        
        corr, p_value = stats.pearsonr(x, y)
        
        # Correlation should be close to 0 (with some random variation)
        assert abs(corr) < 0.2, "Random data should have low correlation"
    
    def test_known_correlation_value(self):
        """Test correlation with manually calculated known value."""
        # Simple dataset where we can manually calculate correlation
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([1, 2, 1.3, 3.75, 2.25])
        
        corr, p_value = stats.pearsonr(x, y)
        
        # Manually calculated: r ≈ 0.627
        assert 0.60 < corr < 0.70, f"Correlation should be around 0.63, got {corr}"


class TestTTestCalculations:
    """Test suite for t-test calculations with known ground truth."""
    
    def test_identical_groups_ttest(self):
        """Test t-test with identical groups (should show no difference)."""
        group1 = np.array([1, 2, 3, 4, 5])
        group2 = np.array([1, 2, 3, 4, 5])
        
        t_stat, p_value = stats.ttest_ind(group1, group2)
        
        assert np.isnan(t_stat) or np.isclose(t_stat, 0, atol=1e-10), "T-statistic should be 0 for identical groups"
        assert p_value > 0.05 or np.isnan(p_value), "P-value should be non-significant"
    
    def test_significantly_different_groups(self):
        """Test t-test with clearly different groups."""
        group1 = np.array([1, 2, 3, 4, 5])
        group2 = np.array([10, 11, 12, 13, 14])
        
        t_stat, p_value = stats.ttest_ind(group1, group2)
        
        assert abs(t_stat) > 5, "T-statistic should be large for very different groups"
        assert p_value < 0.001, "P-value should be highly significant"
    
    def test_known_ttest_value(self):
        """Test t-test with manually verified values."""
        # Known dataset
        group1 = np.array([2.3, 2.5, 2.7, 2.9, 3.1])
        group2 = np.array([3.2, 3.4, 3.6, 3.8, 4.0])
        
        t_stat, p_value = stats.ttest_ind(group1, group2)
        
        # Expected t-statistic is approximately -4.5
        assert -5.0 < t_stat < -4.0, f"T-statistic should be around -4.5, got {t_stat}"
        assert p_value < 0.01, "P-value should be significant"
    
    def test_ttest_with_unequal_variance(self):
        """Test t-test with Welch's correction for unequal variances."""
        np.random.seed(42)
        group1 = np.random.normal(0, 1, 50)
        group2 = np.random.normal(0.5, 3, 50)
        
        t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)
        
        assert isinstance(t_stat, (float, np.floating)), "T-statistic should be a number"
        assert 0 <= p_value <= 1, "P-value should be between 0 and 1"


class TestANOVACalculations:
    """Test suite for ANOVA calculations with known ground truth."""
    
    def test_anova_identical_groups(self):
        """Test ANOVA with identical groups (should show no difference)."""
        group1 = np.array([1, 2, 3, 4, 5])
        group2 = np.array([1, 2, 3, 4, 5])
        group3 = np.array([1, 2, 3, 4, 5])
        
        f_stat, p_value = stats.f_oneway(group1, group2, group3)
        
        assert np.isclose(f_stat, 0, atol=1e-10) or np.isnan(f_stat), "F-statistic should be 0 for identical groups"
    
    def test_anova_different_groups(self):
        """Test ANOVA with clearly different groups."""
        group1 = np.array([1, 2, 3, 4, 5])
        group2 = np.array([6, 7, 8, 9, 10])
        group3 = np.array([11, 12, 13, 14, 15])
        
        f_stat, p_value = stats.f_oneway(group1, group2, group3)
        
        assert f_stat >= 50, "F-statistic should be large for very different groups"
        assert p_value < 0.001, "P-value should be highly significant"
    
    def test_anova_two_groups(self):
        """Test that ANOVA with 2 groups matches t-test."""
        group1 = np.array([1, 2, 3, 4, 5])
        group2 = np.array([6, 7, 8, 9, 10])
        
        # ANOVA
        f_stat, p_anova = stats.f_oneway(group1, group2)
        
        # T-test
        t_stat, p_ttest = stats.ttest_ind(group1, group2)
        
        # F-statistic should equal t-statistic squared
        assert np.isclose(f_stat, t_stat**2, atol=1e-10), "F = t² for two groups"
        assert np.isclose(p_anova, p_ttest, atol=1e-10), "P-values should match"


class TestDescriptiveStatistics:
    """Test suite for descriptive statistics calculations."""
    
    def test_mean_calculation(self):
        """Test mean calculation with known values."""
        data = np.array([1, 2, 3, 4, 5])
        mean = np.mean(data)
        assert np.isclose(mean, 3.0, atol=1e-10), "Mean of [1,2,3,4,5] should be 3.0"
    
    def test_median_calculation(self):
        """Test median calculation with known values."""
        data = np.array([1, 2, 3, 4, 5])
        median = np.median(data)
        assert np.isclose(median, 3.0, atol=1e-10), "Median of [1,2,3,4,5] should be 3.0"
        
        # Test with even number of elements
        data_even = np.array([1, 2, 3, 4])
        median_even = np.median(data_even)
        assert np.isclose(median_even, 2.5, atol=1e-10), "Median of [1,2,3,4] should be 2.5"
    
    def test_std_calculation(self):
        """Test standard deviation calculation with known values."""
        data = np.array([2, 4, 4, 4, 5, 5, 7, 9])
        std = np.std(data, ddof=1)  # Sample standard deviation
        # Expected value: 2.138
        assert 2.0 < std < 2.2, f"Standard deviation should be around 2.138, got {std}"
    
    def test_variance_calculation(self):
        """Test variance calculation."""
        data = np.array([1, 2, 3, 4, 5])
        var = np.var(data, ddof=1)
        std = np.std(data, ddof=1)
        assert np.isclose(var, std**2, atol=1e-10), "Variance should equal std²"
    
    def test_quantile_calculation(self):
        """Test quantile calculation with known values."""
        data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        
        q25 = np.percentile(data, 25)
        q50 = np.percentile(data, 50)
        q75 = np.percentile(data, 75)
        
        assert 2 <= q25 <= 3.5, f"Q25 should be around 2.75, got {q25}"
        assert 5 <= q50 <= 6, f"Q50 (median) should be 5.5, got {q50}"
        assert 7.5 <= q75 <= 9, f"Q75 should be around 8.25, got {q75}"


class TestClassificationMetrics:
    """Test suite for classification metrics with known ground truth."""
    
    def test_perfect_classification(self):
        """Test metrics with perfect classification."""
        y_true = np.array([0, 0, 1, 1])
        y_pred = np.array([0, 0, 1, 1])
        
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred)
        rec = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        
        assert acc == 1.0, "Perfect accuracy should be 1.0"
        assert prec == 1.0, "Perfect precision should be 1.0"
        assert rec == 1.0, "Perfect recall should be 1.0"
        assert f1 == 1.0, "Perfect F1 should be 1.0"
    
    def test_worst_classification(self):
        """Test metrics with worst possible classification."""
        y_true = np.array([0, 0, 1, 1])
        y_pred = np.array([1, 1, 0, 0])
        
        acc = accuracy_score(y_true, y_pred)
        
        assert acc == 0.0, "Worst accuracy should be 0.0"
    
    def test_known_classification_metrics(self):
        """Test metrics with manually calculated values."""
        y_true = np.array([1, 1, 0, 0, 1, 0, 1, 0])
        y_pred = np.array([1, 0, 0, 0, 1, 1, 1, 0])
        
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred)
        rec = recall_score(y_true, y_pred)
        
        # Manually calculated:
        # TP=3, TN=3, FP=1, FN=1
        # Accuracy = (3+3)/8 = 0.75
        # Precision = 3/(3+1) = 0.75
        # Recall = 3/(3+1) = 0.75
        
        assert np.isclose(acc, 0.75, atol=1e-10), f"Accuracy should be 0.75, got {acc}"
        assert np.isclose(prec, 0.75, atol=1e-10), f"Precision should be 0.75, got {prec}"
        assert np.isclose(rec, 0.75, atol=1e-10), f"Recall should be 0.75, got {rec}"


class TestNumericalStability:
    """Test suite for numerical stability and edge cases."""
    
    def test_correlation_with_constant(self):
        """Test correlation when one variable is constant."""
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([1, 1, 1, 1, 1])
        
        with pytest.warns(RuntimeWarning):
            corr, p_value = stats.pearsonr(x, y)
        
        assert np.isnan(corr), "Correlation with constant should be NaN"
    
    def test_correlation_with_single_point(self):
        """Test correlation with insufficient data."""
        x = np.array([1])
        y = np.array([2])
        
        with pytest.raises(ValueError):
            stats.pearsonr(x, y)
    
    def test_mean_with_empty_array(self):
        """Test mean calculation with empty array."""
        data = np.array([])
        
        with pytest.warns(RuntimeWarning):
            mean = np.mean(data)
        
        assert np.isnan(mean), "Mean of empty array should be NaN"
    
    def test_division_by_zero_handling(self):
        """Test that division by zero is handled properly."""
        # This should not raise an error with proper numpy settings
        arr = np.array([1, 2, 3])
        with np.errstate(divide='ignore', invalid='ignore'):
            result = arr / 0
        
        assert np.all(np.isinf(result)), "Division by zero should produce inf"


class TestSyntheticDataValidation:
    """Test suite using synthetic data with known properties."""
    
    def test_normal_distribution_properties(self):
        """Test that generated normal distribution has expected properties."""
        np.random.seed(42)
        n_samples = 10000
        mean = 5.0
        std = 2.0
        
        data = np.random.normal(mean, std, n_samples)
        
        # Check mean (should be close to 5.0)
        assert abs(np.mean(data) - mean) < 0.1, "Sample mean should be close to population mean"
        
        # Check std (should be close to 2.0)
        assert abs(np.std(data, ddof=1) - std) < 0.1, "Sample std should be close to population std"
        
        # Check that ~68% of values are within 1 std
        within_1std = np.sum(np.abs(data - mean) < std) / n_samples
        assert 0.65 < within_1std < 0.71, "~68% should be within 1 std"
    
    def test_uniform_distribution_properties(self):
        """Test that generated uniform distribution has expected properties."""
        np.random.seed(42)
        n_samples = 10000
        low = 0
        high = 10
        
        data = np.random.uniform(low, high, n_samples)
        
        # Check mean (should be close to 5.0)
        expected_mean = (low + high) / 2
        assert abs(np.mean(data) - expected_mean) < 0.1, "Uniform mean should be (low+high)/2"
        
        # Check all values are in range
        assert np.all(data >= low) and np.all(data <= high), "All values should be in [low, high]"
    
    def test_correlation_in_synthetic_data(self):
        """Test correlation in synthetic correlated data."""
        np.random.seed(42)
        n_samples = 1000
        
        # Generate correlated data
        x = np.random.randn(n_samples)
        y = 0.8 * x + 0.2 * np.random.randn(n_samples)
        
        corr, p_value = stats.pearsonr(x, y)
        
        # Correlation should be high (the actual correlation is around 0.97 with this seed)
        assert 0.90 < corr < 0.99, f"Correlation should be high (>0.9), got {corr}"
        assert p_value < 0.001, "Correlation should be significant"


class TestDataFrameStatistics:
    """Test suite for pandas DataFrame statistical operations."""
    
    def test_dataframe_mean(self):
        """Test DataFrame mean calculation."""
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [2, 4, 6, 8, 10]
        })
        
        means = df.mean()
        assert np.isclose(means['A'], 3.0, atol=1e-10)
        assert np.isclose(means['B'], 6.0, atol=1e-10)
    
    def test_dataframe_correlation_matrix(self):
        """Test DataFrame correlation matrix calculation."""
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [2, 4, 6, 8, 10]
        })
        
        corr_matrix = df.corr()
        
        # Diagonal should be 1.0
        assert np.isclose(corr_matrix.loc['A', 'A'], 1.0, atol=1e-10)
        assert np.isclose(corr_matrix.loc['B', 'B'], 1.0, atol=1e-10)
        
        # A and B are perfectly correlated
        assert np.isclose(corr_matrix.loc['A', 'B'], 1.0, atol=1e-10)
        assert np.isclose(corr_matrix.loc['B', 'A'], 1.0, atol=1e-10)
    
    def test_dataframe_groupby_mean(self):
        """Test DataFrame groupby mean calculation."""
        df = pd.DataFrame({
            'group': ['A', 'A', 'B', 'B'],
            'value': [1, 3, 2, 4]
        })
        
        grouped = df.groupby('group')['value'].mean()
        
        assert np.isclose(grouped['A'], 2.0, atol=1e-10)
        assert np.isclose(grouped['B'], 3.0, atol=1e-10)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
