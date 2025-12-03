"""Tests for data validation module."""

import pandas as pd
import pytest
from strepsuis_analyzer.data_validator import DataValidator


class TestDataValidator:
    """Test suite for DataValidator class."""

    @pytest.mark.unit
    def test_init(self):
        """Test DataValidator initialization."""
        validator = DataValidator()
        assert isinstance(validator, DataValidator)
        assert len(validator.validation_errors) == 0
        assert len(validator.validation_warnings) == 0

    @pytest.mark.unit
    def test_validate_dataframe_valid(self, sample_numeric_data):
        """Test validation of valid DataFrame."""
        validator = DataValidator()
        is_valid, errors, warnings = validator.validate_dataframe(sample_numeric_data)
        assert is_valid
        assert len(errors) == 0

    @pytest.mark.unit
    def test_validate_dataframe_empty(self):
        """Test validation of empty DataFrame."""
        validator = DataValidator()
        empty_df = pd.DataFrame()
        is_valid, errors, warnings = validator.validate_dataframe(empty_df)
        assert not is_valid
        assert len(errors) > 0

    @pytest.mark.unit
    def test_validate_dataframe_min_rows(self, sample_numeric_data):
        """Test minimum rows validation."""
        validator = DataValidator()
        is_valid, errors, _ = validator.validate_dataframe(
            sample_numeric_data, min_rows=100
        )
        assert not is_valid
        assert len(errors) > 0

    @pytest.mark.unit
    def test_validate_dataframe_required_columns(self, sample_numeric_data):
        """Test required columns validation."""
        validator = DataValidator()
        is_valid, errors, _ = validator.validate_dataframe(
            sample_numeric_data, required_columns=["var_0", "missing_col"]
        )
        assert not is_valid
        assert any("missing_col" in str(e) for e in errors)

    @pytest.mark.unit
    def test_validate_binary_matrix_valid(self, sample_binary_data):
        """Test binary matrix validation with valid data."""
        validator = DataValidator()
        is_valid, errors, warnings = validator.validate_binary_matrix(sample_binary_data)
        assert is_valid
        assert len(errors) == 0

    @pytest.mark.unit
    def test_validate_binary_matrix_invalid(self, sample_numeric_data):
        """Test binary matrix validation with non-binary data."""
        validator = DataValidator()
        is_valid, errors, warnings = validator.validate_binary_matrix(sample_numeric_data)
        assert not is_valid
        assert len(errors) > 0

    @pytest.mark.unit
    def test_validate_numeric_matrix(self, sample_numeric_data):
        """Test numeric matrix validation."""
        validator = DataValidator()
        is_valid, errors, warnings = validator.validate_numeric_matrix(sample_numeric_data)
        assert is_valid

    @pytest.mark.unit
    def test_validate_numeric_matrix_range(self):
        """Test numeric matrix range validation."""
        validator = DataValidator()
        df = pd.DataFrame({"col1": [1, 2, 3, 100]})
        is_valid, errors, _ = validator.validate_numeric_matrix(
            df, min_value=0, max_value=50
        )
        assert not is_valid

    @pytest.mark.unit
    def test_validate_categorical_column(self, sample_categorical_data):
        """Test categorical column validation."""
        validator = DataValidator()
        is_valid, errors, warnings = validator.validate_categorical_column(
            sample_categorical_data
        )
        assert is_valid

    @pytest.mark.unit
    def test_validate_categorical_column_allowed_values(self, sample_categorical_data):
        """Test categorical column with allowed values."""
        validator = DataValidator()
        is_valid, errors, _ = validator.validate_categorical_column(
            sample_categorical_data, allowed_values=["A", "B"]
        )
        assert not is_valid

    @pytest.mark.unit
    def test_validate_newick_tree_valid(self, sample_tree_newick):
        """Test Newick tree validation with valid tree."""
        validator = DataValidator()
        is_valid, errors, warnings = validator.validate_newick_tree(sample_tree_newick)
        assert is_valid

    @pytest.mark.unit
    def test_validate_newick_tree_invalid(self):
        """Test Newick tree validation with invalid tree."""
        validator = DataValidator()
        invalid_tree = "((A:0.1,B:0.2):0.3"  # Missing closing paren and semicolon
        is_valid, errors, warnings = validator.validate_newick_tree(invalid_tree)
        assert not is_valid

    @pytest.mark.unit
    def test_reset(self):
        """Test reset method."""
        validator = DataValidator()
        validator.validation_errors = ["error1"]
        validator.validation_warnings = ["warning1"]
        validator.reset()
        assert len(validator.validation_errors) == 0
        assert len(validator.validation_warnings) == 0
