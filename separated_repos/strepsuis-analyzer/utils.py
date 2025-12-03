"""
Utility functions for the Streptococcus suis Analyzer application.
This module contains testable utility functions separated from the Streamlit app.
"""
import pandas as pd
import numpy as np
import os


def fix_dataframe_for_streamlit(df):
    """
    Fix dataframe data types for Streamlit compatibility.
    
    Args:
        df: pandas DataFrame to fix
        
    Returns:
        Fixed DataFrame with proper data types
    """
    if df is None or df.empty:
        return df
    
    # Convert object columns to string
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype("string")
    
    # Convert datetime columns to string
    for col in df.columns:
        if str(df[col].dtype).startswith(('datetime64', 'timedelta64')):
            df[col] = df[col].astype(str)
    
    return df


class DataValidator:
    """Validator for data quality checks."""
    
    def __init__(self):
        """Initialize validator with empty error and warning lists."""
        self.errors = []
        self.warnings = []
    
    def validate_dataframe_structure(self, df, min_rows=1, min_cols=1):
        """
        Validate basic dataframe structure.
        
        Args:
            df: DataFrame to validate
            min_rows: Minimum required rows
            min_cols: Minimum required columns
            
        Returns:
            bool: True if validation passes basic checks
        """
        if df is None or df.empty:
            self.errors.append("DataFrame is empty or None.")
            return False
        
        if df.shape[0] < min_rows:
            self.errors.append(
                f"Not enough rows (found {df.shape[0]}, need >= {min_rows})."
            )
        
        if df.shape[1] < min_cols:
            self.errors.append(
                f"Not enough columns (found {df.shape[1]}, need >= {min_cols})."
            )
        
        return True
    
    def get_report(self):
        """
        Get validation report.
        
        Returns:
            dict: Dictionary containing errors and warnings
        """
        return {"errors": self.errors, "warnings": self.warnings}


def load_reference_data():
    """
    Load all reference data files from the data directory.
    
    Returns:
        dict: Dictionary mapping dataset names to DataFrames
    """
    file_paths = {
        "AMR_genes": "data/AMR_genes.csv",
        "MGE": "data/MGE.csv",
        "MIC": "data/MIC.csv",
        "MLST": "data/MLST.csv",
        "Plasmid": "data/Plasmid.csv",
        "Serotype": "data/Serotype.csv",
        "Virulence": "data/Virulence.csv"
    }
    
    dataframes = {}
    for k, p in file_paths.items():
        if os.path.exists(p):
            try:
                df_tmp = pd.read_csv(p)
                df_tmp = fix_dataframe_for_streamlit(df_tmp)
                dataframes[k] = df_tmp
            except Exception:
                dataframes[k] = None
        else:
            dataframes[k] = None
    
    return dataframes


def calculate_correlation(data1, data2):
    """
    Calculate Pearson correlation between two data series.
    
    Args:
        data1: First data series (array-like)
        data2: Second data series (array-like)
        
    Returns:
        tuple: (correlation coefficient, p-value)
    """
    from scipy import stats
    
    # Remove NaN values
    data1 = np.array(data1)
    data2 = np.array(data2)
    
    # Find valid indices
    valid_idx = ~(np.isnan(data1) | np.isnan(data2))
    data1 = data1[valid_idx]
    data2 = data2[valid_idx]
    
    if len(data1) < 2:
        return np.nan, np.nan
    
    return stats.pearsonr(data1, data2)


def calculate_descriptive_stats(data):
    """
    Calculate descriptive statistics for a data series.
    
    Args:
        data: Data series (array-like)
        
    Returns:
        dict: Dictionary containing mean, median, std, min, max
    """
    data = np.array(data)
    data = data[~np.isnan(data)]  # Remove NaN values
    
    if len(data) == 0:
        return {
            'mean': np.nan,
            'median': np.nan,
            'std': np.nan,
            'min': np.nan,
            'max': np.nan,
            'count': 0
        }
    
    return {
        'mean': np.mean(data),
        'median': np.median(data),
        'std': np.std(data, ddof=1) if len(data) > 1 else 0,
        'min': np.min(data),
        'max': np.max(data),
        'count': len(data)
    }


def perform_ttest(group1, group2, equal_var=True):
    """
    Perform independent samples t-test.
    
    Args:
        group1: First group data (array-like)
        group2: Second group data (array-like)
        equal_var: Whether to assume equal variance
        
    Returns:
        tuple: (t-statistic, p-value)
    """
    from scipy import stats
    
    group1 = np.array(group1)
    group2 = np.array(group2)
    
    # Remove NaN values
    group1 = group1[~np.isnan(group1)]
    group2 = group2[~np.isnan(group2)]
    
    if len(group1) < 2 or len(group2) < 2:
        return np.nan, np.nan
    
    return stats.ttest_ind(group1, group2, equal_var=equal_var)


def perform_anova(*groups):
    """
    Perform one-way ANOVA.
    
    Args:
        *groups: Variable number of group data arrays
        
    Returns:
        tuple: (F-statistic, p-value)
    """
    from scipy import stats
    
    # Clean groups
    cleaned_groups = []
    for group in groups:
        group = np.array(group)
        group = group[~np.isnan(group)]
        if len(group) > 0:
            cleaned_groups.append(group)
    
    if len(cleaned_groups) < 2:
        return np.nan, np.nan
    
    return stats.f_oneway(*cleaned_groups)


def validate_newick_tree(tree_string):
    """
    Validate a Newick format tree string.
    
    Args:
        tree_string: Newick format tree string
        
    Returns:
        bool: True if valid Newick format
    """
    tree_string = tree_string.strip()
    
    # Basic validation
    if not tree_string.endswith(';'):
        return False
    
    if '(' not in tree_string or ')' not in tree_string:
        return False
    
    # Check balanced parentheses
    balance = 0
    for char in tree_string:
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
        if balance < 0:
            return False
    
    return balance == 0
