"""
Tests for utility functions.
"""
import pytest
import pandas as pd
import numpy as np
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import (
    fix_dataframe_for_streamlit,
    DataValidator,
    load_reference_data,
    calculate_correlation,
    calculate_descriptive_stats,
    perform_ttest,
    perform_anova,
    validate_newick_tree
)


class TestFixDataframeForStreamlit:
    """Test suite for fix_dataframe_for_streamlit function."""
    
    def test_fix_empty_dataframe(self):
        """Test fixing empty dataframe."""
        df = pd.DataFrame()
        result = fix_dataframe_for_streamlit(df)
        assert result.empty
    
    def test_fix_none_dataframe(self):
        """Test fixing None dataframe."""
        result = fix_dataframe_for_streamlit(None)
        assert result is None
    
    def test_fix_object_columns(self):
        """Test conversion of object columns to string."""
        df = pd.DataFrame({'A': ['a', 'b', 'c'], 'B': [1, 2, 3]})
        result = fix_dataframe_for_streamlit(df)
        assert result['A'].dtype == 'string'
        assert result['B'].dtype == np.int64
    
    def test_fix_datetime_columns(self):
        """Test conversion of datetime columns to string."""
        df = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=3),
            'value': [1, 2, 3]
        })
        result = fix_dataframe_for_streamlit(df)
        assert result['date'].dtype == object
        assert result['value'].dtype == np.int64


class TestDataValidator:
    """Test suite for DataValidator class."""
    
    def test_validate_empty_dataframe(self):
        """Test validation with empty dataframe."""
        validator = DataValidator()
        df = pd.DataFrame()
        result = validator.validate_dataframe_structure(df)
        assert result is False
        report = validator.get_report()
        assert len(report['errors']) > 0
    
    def test_validate_none_dataframe(self):
        """Test validation with None."""
        validator = DataValidator()
        result = validator.validate_dataframe_structure(None)
        assert result is False
    
    def test_validate_valid_dataframe(self):
        """Test validation with valid dataframe."""
        validator = DataValidator()
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        result = validator.validate_dataframe_structure(df, min_rows=1, min_cols=1)
        assert result is True
    
    def test_validate_insufficient_rows(self):
        """Test validation with insufficient rows."""
        validator = DataValidator()
        df = pd.DataFrame({'A': [1], 'B': [2]})
        validator.validate_dataframe_structure(df, min_rows=5, min_cols=1)
        report = validator.get_report()
        assert any('rows' in err.lower() for err in report['errors'])
    
    def test_get_report_structure(self):
        """Test get_report returns correct structure."""
        validator = DataValidator()
        report = validator.get_report()
        assert 'errors' in report
        assert 'warnings' in report
        assert isinstance(report['errors'], list)
        assert isinstance(report['warnings'], list)


class TestLoadReferenceData:
    """Test suite for load_reference_data function."""
    
    def test_load_reference_data_structure(self):
        """Test that load_reference_data returns expected structure."""
        data = load_reference_data()
        assert isinstance(data, dict)
        expected_keys = ['AMR_genes', 'MGE', 'MIC', 'MLST', 'Plasmid', 'Serotype', 'Virulence']
        for key in expected_keys:
            assert key in data
    
    def test_load_existing_files(self):
        """Test loading existing data files."""
        data = load_reference_data()
        loaded_count = sum(1 for v in data.values() if v is not None)
        if os.path.exists('data'):
            assert loaded_count > 0


class TestCalculateCorrelation:
    """Test suite for calculate_correlation function."""
    
    def test_perfect_positive_correlation(self):
        """Test with perfect positive correlation."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        corr, p_value = calculate_correlation(x, y)
        assert np.isclose(corr, 1.0, atol=1e-10)
    
    def test_perfect_negative_correlation(self):
        """Test with perfect negative correlation."""
        x = [1, 2, 3, 4, 5]
        y = [10, 8, 6, 4, 2]
        corr, p_value = calculate_correlation(x, y)
        assert np.isclose(corr, -1.0, atol=1e-10)
    
    def test_with_nan_values(self):
        """Test handling of NaN values."""
        x = [1, 2, np.nan, 4, 5]
        y = [2, 4, 6, 8, 10]
        corr, p_value = calculate_correlation(x, y)
        assert not np.isnan(corr)
    
    def test_insufficient_data(self):
        """Test with insufficient data."""
        x = [1]
        y = [2]
        corr, p_value = calculate_correlation(x, y)
        assert np.isnan(corr)
    
    def test_all_nan_values(self):
        """Test with all NaN values."""
        x = [np.nan, np.nan, np.nan]
        y = [np.nan, np.nan, np.nan]
        corr, p_value = calculate_correlation(x, y)
        assert np.isnan(corr)


class TestCalculateDescriptiveStats:
    """Test suite for calculate_descriptive_stats function."""
    
    def test_basic_statistics(self):
        """Test basic statistical calculations."""
        data = [1, 2, 3, 4, 5]
        stats = calculate_descriptive_stats(data)
        
        assert np.isclose(stats['mean'], 3.0)
        assert np.isclose(stats['median'], 3.0)
        assert stats['min'] == 1
        assert stats['max'] == 5
        assert stats['count'] == 5
    
    def test_with_nan_values(self):
        """Test handling of NaN values."""
        data = [1, 2, np.nan, 4, 5]
        stats = calculate_descriptive_stats(data)
        
        assert stats['count'] == 4
        assert np.isclose(stats['mean'], 3.0)
    
    def test_empty_data(self):
        """Test with empty data."""
        data = []
        stats = calculate_descriptive_stats(data)
        
        assert np.isnan(stats['mean'])
        assert stats['count'] == 0
    
    def test_all_nan_data(self):
        """Test with all NaN data."""
        data = [np.nan, np.nan, np.nan]
        stats = calculate_descriptive_stats(data)
        
        assert np.isnan(stats['mean'])
        assert stats['count'] == 0
    
    def test_single_value(self):
        """Test with single value."""
        data = [5]
        stats = calculate_descriptive_stats(data)
        
        assert stats['mean'] == 5
        assert stats['median'] == 5
        assert stats['std'] == 0
        assert stats['count'] == 1


class TestPerformTtest:
    """Test suite for perform_ttest function."""
    
    def test_identical_groups(self):
        """Test t-test with identical groups."""
        group1 = [1, 2, 3, 4, 5]
        group2 = [1, 2, 3, 4, 5]
        t_stat, p_value = perform_ttest(group1, group2)
        
        assert np.isnan(t_stat) or np.isclose(t_stat, 0, atol=1e-10)
    
    def test_different_groups(self):
        """Test t-test with different groups."""
        group1 = [1, 2, 3, 4, 5]
        group2 = [10, 11, 12, 13, 14]
        t_stat, p_value = perform_ttest(group1, group2)
        
        assert abs(t_stat) > 5
        assert p_value < 0.001
    
    def test_with_nan_values(self):
        """Test handling of NaN values."""
        group1 = [1, 2, np.nan, 4, 5]
        group2 = [10, 11, 12, 13, 14]
        t_stat, p_value = perform_ttest(group1, group2)
        
        assert not np.isnan(t_stat)
    
    def test_insufficient_data(self):
        """Test with insufficient data."""
        group1 = [1]
        group2 = [2]
        t_stat, p_value = perform_ttest(group1, group2)
        
        assert np.isnan(t_stat)
    
    def test_unequal_variance(self):
        """Test with unequal variance option."""
        group1 = [1, 2, 3, 4, 5]
        group2 = [10, 20, 30, 40, 50]
        t_stat, p_value = perform_ttest(group1, group2, equal_var=False)
        
        assert not np.isnan(t_stat)


class TestPerformAnova:
    """Test suite for perform_anova function."""
    
    def test_identical_groups(self):
        """Test ANOVA with identical groups."""
        group1 = [1, 2, 3, 4, 5]
        group2 = [1, 2, 3, 4, 5]
        group3 = [1, 2, 3, 4, 5]
        f_stat, p_value = perform_anova(group1, group2, group3)
        
        assert np.isclose(f_stat, 0, atol=1e-10) or np.isnan(f_stat)
    
    def test_different_groups(self):
        """Test ANOVA with different groups."""
        group1 = [1, 2, 3, 4, 5]
        group2 = [6, 7, 8, 9, 10]
        group3 = [11, 12, 13, 14, 15]
        f_stat, p_value = perform_anova(group1, group2, group3)
        
        assert f_stat >= 50
        assert p_value < 0.001
    
    def test_two_groups(self):
        """Test ANOVA with two groups."""
        group1 = [1, 2, 3, 4, 5]
        group2 = [6, 7, 8, 9, 10]
        f_stat, p_value = perform_anova(group1, group2)
        
        assert not np.isnan(f_stat)
    
    def test_with_nan_values(self):
        """Test handling of NaN values."""
        group1 = [1, 2, np.nan, 4, 5]
        group2 = [6, 7, 8, 9, 10]
        group3 = [11, 12, 13, 14, 15]
        f_stat, p_value = perform_anova(group1, group2, group3)
        
        assert not np.isnan(f_stat)
    
    def test_insufficient_groups(self):
        """Test with insufficient groups."""
        group1 = [1, 2, 3]
        f_stat, p_value = perform_anova(group1)
        
        assert np.isnan(f_stat)


class TestValidateNewickTree:
    """Test suite for validate_newick_tree function."""
    
    def test_valid_simple_tree(self):
        """Test with valid simple tree."""
        tree = "(A:0.1,B:0.2):0.0;"
        assert validate_newick_tree(tree) is True
    
    def test_valid_complex_tree(self):
        """Test with valid complex tree."""
        tree = "((A:0.1,B:0.2):0.3,(C:0.4,D:0.5):0.6):0.0;"
        assert validate_newick_tree(tree) is True
    
    def test_missing_semicolon(self):
        """Test with missing semicolon."""
        tree = "(A:0.1,B:0.2):0.0"
        assert validate_newick_tree(tree) is False
    
    def test_no_parentheses(self):
        """Test with no parentheses."""
        tree = "A:0.1,B:0.2;"
        assert validate_newick_tree(tree) is False
    
    def test_unbalanced_parentheses(self):
        """Test with unbalanced parentheses."""
        tree = "((A:0.1,B:0.2):0.3;"
        assert validate_newick_tree(tree) is False
    
    def test_whitespace_handling(self):
        """Test whitespace handling."""
        tree = "  (A:0.1,B:0.2):0.0;  "
        assert validate_newick_tree(tree) is True
    
    def test_actual_data_tree(self):
        """Test with actual data tree if available."""
        tree_path = 'data/Snp_tree.newick'
        if os.path.exists(tree_path):
            with open(tree_path, 'r') as f:
                tree = f.read()
            assert validate_newick_tree(tree) is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
