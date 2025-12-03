"""
ETL (Extract, Transform, Load) operations for StrepSuisAnalyzer.

Provides data transformation utilities including pivoting, aggregation,
window functions, and custom formulas.
"""

from typing import Dict, List, Optional, Union, Callable, Any
import pandas as pd
import numpy as np


class ETLOperations:
    """Performs ETL operations on data."""

    def __init__(self):
        """Initialize ETLOperations."""
        pass

    def pivot_table(
        self,
        df: pd.DataFrame,
        index: Union[str, List[str]],
        columns: Union[str, List[str]],
        values: Union[str, List[str]],
        aggfunc: Union[str, Callable] = "mean",
        fill_value: Optional[Any] = None,
    ) -> pd.DataFrame:
        """
        Create a pivot table.

        Args:
            df: Input DataFrame
            index: Column(s) to use as index
            columns: Column(s) to use as columns
            values: Column(s) to aggregate
            aggfunc: Aggregation function
            fill_value: Value to replace missing values

        Returns:
            Pivot table DataFrame
        """
        return pd.pivot_table(
            df, index=index, columns=columns, values=values, aggfunc=aggfunc, fill_value=fill_value
        )

    def aggregate_data(
        self,
        df: pd.DataFrame,
        group_by: Union[str, List[str]],
        agg_dict: Dict[str, Union[str, List[str], Callable]],
    ) -> pd.DataFrame:
        """
        Aggregate data by groups.

        Args:
            df: Input DataFrame
            group_by: Column(s) to group by
            agg_dict: Dictionary mapping columns to aggregation functions

        Returns:
            Aggregated DataFrame
        """
        return df.groupby(group_by).agg(agg_dict).reset_index()

    def apply_window_function(
        self,
        df: pd.DataFrame,
        column: str,
        window_size: int,
        function: str = "mean",
        min_periods: Optional[int] = None,
    ) -> pd.Series:
        """
        Apply rolling window function.

        Args:
            df: Input DataFrame
            column: Column to apply window function
            window_size: Size of the rolling window
            function: Window function ('mean', 'sum', 'std', 'min', 'max')
            min_periods: Minimum number of observations in window

        Returns:
            Series with window function results
        """
        rolling = df[column].rolling(window=window_size, min_periods=min_periods)

        if function == "mean":
            return rolling.mean()
        elif function == "sum":
            return rolling.sum()
        elif function == "std":
            return rolling.std()
        elif function == "min":
            return rolling.min()
        elif function == "max":
            return rolling.max()
        else:
            raise ValueError(f"Unsupported window function: {function}")

    def apply_custom_formula(
        self, df: pd.DataFrame, formula: str, new_column: str
    ) -> pd.DataFrame:
        """
        Apply custom formula to create new column.

        Args:
            df: Input DataFrame
            formula: Formula string (uses df.eval syntax)
            new_column: Name for new column

        Returns:
            DataFrame with new column

        Example:
            formula = "col1 + col2 * 2"
            formula = "col1 / col2"
        """
        df_copy = df.copy()
        df_copy[new_column] = df_copy.eval(formula)
        return df_copy

    def normalize_columns(
        self, df: pd.DataFrame, columns: List[str], method: str = "zscore"
    ) -> pd.DataFrame:
        """
        Normalize specified columns.

        Args:
            df: Input DataFrame
            columns: Columns to normalize
            method: Normalization method ('zscore', 'minmax', 'robust')

        Returns:
            DataFrame with normalized columns
        """
        df_copy = df.copy()

        for col in columns:
            if col not in df_copy.columns:
                continue

            if method == "zscore":
                df_copy[col] = (df_copy[col] - df_copy[col].mean()) / df_copy[col].std()
            elif method == "minmax":
                df_copy[col] = (df_copy[col] - df_copy[col].min()) / (
                    df_copy[col].max() - df_copy[col].min()
                )
            elif method == "robust":
                median = df_copy[col].median()
                q75, q25 = df_copy[col].quantile([0.75, 0.25])
                iqr = q75 - q25
                df_copy[col] = (df_copy[col] - median) / iqr
            else:
                raise ValueError(f"Unsupported normalization method: {method}")

        return df_copy

    def merge_dataframes(
        self,
        left: pd.DataFrame,
        right: pd.DataFrame,
        how: str = "inner",
        on: Optional[Union[str, List[str]]] = None,
        left_on: Optional[Union[str, List[str]]] = None,
        right_on: Optional[Union[str, List[str]]] = None,
    ) -> pd.DataFrame:
        """
        Merge two DataFrames.

        Args:
            left: Left DataFrame
            right: Right DataFrame
            how: Type of merge ('left', 'right', 'outer', 'inner')
            on: Column(s) to merge on
            left_on: Left DataFrame columns to merge on
            right_on: Right DataFrame columns to merge on

        Returns:
            Merged DataFrame
        """
        return pd.merge(left, right, how=how, on=on, left_on=left_on, right_on=right_on)

    def filter_rows(
        self, df: pd.DataFrame, condition: str
    ) -> pd.DataFrame:
        """
        Filter rows based on condition.

        Args:
            df: Input DataFrame
            condition: Filter condition (uses df.query syntax)

        Returns:
            Filtered DataFrame

        Example:
            condition = "age > 30 and salary < 50000"
        """
        return df.query(condition)

    def handle_missing_values(
        self,
        df: pd.DataFrame,
        strategy: str = "drop",
        fill_value: Optional[Any] = None,
        columns: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        Handle missing values.

        Args:
            df: Input DataFrame
            strategy: Strategy ('drop', 'fill', 'forward_fill', 'backward_fill')
            fill_value: Value to use for filling (if strategy='fill')
            columns: Columns to apply strategy (None for all)

        Returns:
            DataFrame with missing values handled
        """
        df_copy = df.copy()

        if columns is None:
            columns = df_copy.columns.tolist()

        if strategy == "drop":
            df_copy = df_copy.dropna(subset=columns)
        elif strategy == "fill":
            df_copy[columns] = df_copy[columns].fillna(fill_value)
        elif strategy == "forward_fill":
            df_copy[columns] = df_copy[columns].ffill()
        elif strategy == "backward_fill":
            df_copy[columns] = df_copy[columns].bfill()
        else:
            raise ValueError(f"Unsupported strategy: {strategy}")

        return df_copy

    def reshape_wide_to_long(
        self,
        df: pd.DataFrame,
        id_vars: List[str],
        value_vars: List[str],
        var_name: str = "variable",
        value_name: str = "value",
    ) -> pd.DataFrame:
        """
        Reshape DataFrame from wide to long format.

        Args:
            df: Input DataFrame
            id_vars: Columns to use as identifier variables
            value_vars: Columns to unpivot
            var_name: Name for variable column
            value_name: Name for value column

        Returns:
            Reshaped DataFrame
        """
        return pd.melt(
            df, id_vars=id_vars, value_vars=value_vars, var_name=var_name, value_name=value_name
        )

    def reshape_long_to_wide(
        self,
        df: pd.DataFrame,
        index: Union[str, List[str]],
        columns: str,
        values: str,
    ) -> pd.DataFrame:
        """
        Reshape DataFrame from long to wide format.

        Args:
            df: Input DataFrame
            index: Column(s) to use as index
            columns: Column to use for new column names
            values: Column to use for values

        Returns:
            Reshaped DataFrame
        """
        return df.pivot(index=index, columns=columns, values=values).reset_index()

    def create_derived_features(
        self, df: pd.DataFrame, feature_dict: Dict[str, str]
    ) -> pd.DataFrame:
        """
        Create derived features using formulas.

        Args:
            df: Input DataFrame
            feature_dict: Dictionary mapping new column names to formulas

        Returns:
            DataFrame with derived features

        Example:
            feature_dict = {
                'bmi': 'weight / (height ** 2)',
                'age_group': 'age // 10 * 10'
            }
        """
        df_copy = df.copy()

        for new_col, formula in feature_dict.items():
            df_copy[new_col] = df_copy.eval(formula)

        return df_copy
