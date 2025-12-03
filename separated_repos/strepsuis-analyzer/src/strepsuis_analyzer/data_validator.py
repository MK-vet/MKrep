"""
Data validation utilities for StrepSuisAnalyzer.

Provides comprehensive validation for genomic and phenotypic data including
shape validation, type checking, missing value detection, and data integrity checks.
"""

from typing import Dict, List, Optional, Tuple, Union
import pandas as pd
import numpy as np
from pathlib import Path


class DataValidator:
    """Validates input data for analysis."""

    def __init__(self):
        """Initialize the DataValidator."""
        self.validation_errors: List[str] = []
        self.validation_warnings: List[str] = []

    def validate_dataframe(
        self,
        df: pd.DataFrame,
        name: str = "DataFrame",
        min_rows: Optional[int] = None,
        min_cols: Optional[int] = None,
        required_columns: Optional[List[str]] = None,
        allow_missing: bool = True,
    ) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a pandas DataFrame.

        Args:
            df: DataFrame to validate
            name: Name of the DataFrame for error messages
            min_rows: Minimum required rows
            min_cols: Minimum required columns
            required_columns: List of required column names
            allow_missing: Whether to allow missing values

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        errors = []
        warnings = []

        # Check if DataFrame is empty
        if df is None or df.empty:
            errors.append(f"{name} is empty or None")
            return False, errors, warnings

        # Check minimum dimensions
        if min_rows is not None and len(df) < min_rows:
            errors.append(f"{name} has {len(df)} rows, minimum {min_rows} required")

        if min_cols is not None and len(df.columns) < min_cols:
            errors.append(f"{name} has {len(df.columns)} columns, minimum {min_cols} required")

        # Check required columns
        if required_columns:
            missing_cols = set(required_columns) - set(df.columns)
            if missing_cols:
                errors.append(f"{name} missing required columns: {missing_cols}")

        # Check for missing values
        if not allow_missing:
            missing_count = df.isnull().sum().sum()
            if missing_count > 0:
                errors.append(f"{name} contains {missing_count} missing values")
        else:
            missing_count = df.isnull().sum().sum()
            if missing_count > 0:
                warnings.append(f"{name} contains {missing_count} missing values")

        is_valid = len(errors) == 0
        return is_valid, errors, warnings

    def validate_binary_matrix(
        self, df: pd.DataFrame, name: str = "Binary matrix"
    ) -> Tuple[bool, List[str], List[str]]:
        """
        Validate that DataFrame contains only binary (0/1) values.

        Args:
            df: DataFrame to validate
            name: Name for error messages

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        errors = []
        warnings = []

        # First validate as DataFrame
        is_valid, base_errors, base_warnings = self.validate_dataframe(df, name, min_rows=1)
        errors.extend(base_errors)
        warnings.extend(base_warnings)

        if not is_valid:
            return False, errors, warnings

        # Check for binary values (excluding NaN)
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            errors.append(f"{name} contains no numeric columns")
            return False, errors, warnings

        non_binary = []
        for col in numeric_df.columns:
            valid_values = numeric_df[col].dropna().isin([0, 1, 0.0, 1.0])
            if not valid_values.all():
                non_binary.append(col)

        if non_binary:
            errors.append(
                f"{name} contains non-binary values in columns: {non_binary[:5]}"
                + (f" and {len(non_binary) - 5} more" if len(non_binary) > 5 else "")
            )

        is_valid = len(errors) == len(base_errors)
        return is_valid, errors, warnings

    def validate_numeric_matrix(
        self,
        df: pd.DataFrame,
        name: str = "Numeric matrix",
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
    ) -> Tuple[bool, List[str], List[str]]:
        """
        Validate that DataFrame contains numeric values within range.

        Args:
            df: DataFrame to validate
            name: Name for error messages
            min_value: Minimum allowed value
            max_value: Maximum allowed value

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        errors = []
        warnings = []

        # First validate as DataFrame
        is_valid, base_errors, base_warnings = self.validate_dataframe(df, name, min_rows=1)
        errors.extend(base_errors)
        warnings.extend(base_warnings)

        if not is_valid:
            return False, errors, warnings

        # Check for numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            errors.append(f"{name} contains no numeric columns")
            return False, errors, warnings

        # Check value ranges
        if min_value is not None:
            below_min = (numeric_df < min_value).sum().sum()
            if below_min > 0:
                errors.append(f"{name} contains {below_min} values below {min_value}")

        if max_value is not None:
            above_max = (numeric_df > max_value).sum().sum()
            if above_max > 0:
                errors.append(f"{name} contains {above_max} values above {max_value}")

        is_valid = len(errors) == len(base_errors)
        return is_valid, errors, warnings

    def validate_categorical_column(
        self,
        series: pd.Series,
        name: str = "Column",
        allowed_values: Optional[List] = None,
    ) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a categorical column.

        Args:
            series: Pandas Series to validate
            name: Name for error messages
            allowed_values: List of allowed values

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        errors = []
        warnings = []

        if series is None or len(series) == 0:
            errors.append(f"{name} is empty or None")
            return False, errors, warnings

        # Check for allowed values
        if allowed_values is not None:
            invalid_values = set(series.dropna().unique()) - set(allowed_values)
            if invalid_values:
                errors.append(
                    f"{name} contains invalid values: {list(invalid_values)[:10]}"
                    + (f" and {len(invalid_values) - 10} more" if len(invalid_values) > 10 else "")
                )

        # Check for missing values
        missing_count = series.isnull().sum()
        if missing_count > 0:
            warnings.append(f"{name} contains {missing_count} missing values")

        is_valid = len(errors) == 0
        return is_valid, errors, warnings

    def validate_newick_tree(self, tree_str: str) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a Newick format phylogenetic tree.

        Args:
            tree_str: Newick format tree string

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        errors = []
        warnings = []

        if not tree_str or not isinstance(tree_str, str):
            errors.append("Tree string is empty or not a string")
            return False, errors, warnings

        # Basic Newick format checks
        tree_str = tree_str.strip()

        # Must end with semicolon
        if not tree_str.endswith(";"):
            errors.append("Newick tree must end with semicolon")

        # Count parentheses
        open_paren = tree_str.count("(")
        close_paren = tree_str.count(")")
        if open_paren != close_paren:
            errors.append(
                f"Mismatched parentheses: {open_paren} opening, {close_paren} closing"
            )

        # Check for basic structure
        if open_paren == 0 and close_paren == 0:
            warnings.append("Tree has no internal nodes (single leaf?)")

        is_valid = len(errors) == 0
        return is_valid, errors, warnings

    def validate_file_exists(self, filepath: Union[str, Path]) -> Tuple[bool, List[str]]:
        """
        Validate that a file exists.

        Args:
            filepath: Path to file

        Returns:
            Tuple of (exists, errors)
        """
        errors = []
        path = Path(filepath)

        if not path.exists():
            errors.append(f"File not found: {filepath}")
            return False, errors

        if not path.is_file():
            errors.append(f"Path is not a file: {filepath}")
            return False, errors

        return True, errors

    def get_validation_summary(self) -> Dict[str, Union[int, List[str]]]:
        """
        Get summary of all validation results.

        Returns:
            Dictionary with error and warning counts and lists
        """
        return {
            "error_count": len(self.validation_errors),
            "warning_count": len(self.validation_warnings),
            "errors": self.validation_errors.copy(),
            "warnings": self.validation_warnings.copy(),
        }

    def reset(self):
        """Reset validation errors and warnings."""
        self.validation_errors = []
        self.validation_warnings = []
