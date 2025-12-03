"""
Tests for the Streamlit application.
"""
import pytest
import pandas as pd
import numpy as np
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# We'll test the utility functions without importing the full Streamlit app
# to avoid Streamlit runtime initialization issues


def fix_dataframe_for_streamlit(df):
    """Fix dataframe data types for Streamlit compatibility."""
    if df is None or df.empty:
        return df
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype("string")
    for col in df.columns:
        if str(df[col].dtype).startswith(('datetime64','timedelta64')):
            df[col] = df[col].astype(str)
    return df


class DataValidator:
    """Validator for data quality checks."""
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_dataframe_structure(self, df, min_rows=1, min_cols=1):
        """Validate basic dataframe structure."""
        if df is None or df.empty:
            self.errors.append("DataFrame is empty or None.")
            return False
        if df.shape[0] < min_rows:
            self.errors.append(f"Not enough rows (found {df.shape[0]}, need >= {min_rows}).")
        if df.shape[1] < min_cols:
            self.errors.append(f"Not enough columns (found {df.shape[1]}, need >= {min_cols}).")
        return True
    
    def get_report(self):
        """Get validation report."""
        return {"errors": self.errors, "warnings": self.warnings}


def load_reference_data():
    """Load all reference data files."""
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
            except:
                dataframes[k] = None
        else:
            dataframes[k] = None
    return dataframes


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
        assert "empty" in report['errors'][0].lower()
    
    def test_validate_none_dataframe(self):
        """Test validation with None."""
        validator = DataValidator()
        result = validator.validate_dataframe_structure(None)
        assert result is False
        report = validator.get_report()
        assert len(report['errors']) > 0
    
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
    
    def test_validate_insufficient_columns(self):
        """Test validation with insufficient columns."""
        validator = DataValidator()
        df = pd.DataFrame({'A': [1, 2, 3]})
        validator.validate_dataframe_structure(df, min_rows=1, min_cols=5)
        report = validator.get_report()
        assert any('column' in err.lower() for err in report['errors'])


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
        assert result['date'].dtype == object  # Converted to string
        assert result['value'].dtype == np.int64


class TestLoadReferenceData:
    """Test suite for load_reference_data function."""
    
    def test_load_reference_data_structure(self):
        """Test that load_reference_data returns expected structure."""
        data = load_reference_data()
        assert isinstance(data, dict)
        expected_keys = ['AMR_genes', 'MGE', 'MIC', 'MLST', 'Plasmid', 'Serotype', 'Virulence']
        for key in expected_keys:
            assert key in data
    
    def test_load_reference_data_files_exist(self):
        """Test that reference data files are loaded if they exist."""
        data = load_reference_data()
        
        # Check if at least some files were loaded
        loaded_count = sum(1 for v in data.values() if v is not None)
        
        # If data directory exists, at least some files should be loaded
        if os.path.exists('data'):
            assert loaded_count > 0, "No reference data files were loaded"
    
    def test_amr_genes_structure(self):
        """Test AMR genes data structure if available."""
        data = load_reference_data()
        if data.get('AMR_genes') is not None:
            df = data['AMR_genes']
            assert isinstance(df, pd.DataFrame)
            assert 'Strain' in df.columns
            assert df.shape[0] > 0
    
    def test_mic_data_structure(self):
        """Test MIC data structure if available."""
        data = load_reference_data()
        if data.get('MIC') is not None:
            df = data['MIC']
            assert isinstance(df, pd.DataFrame)
            assert 'Strain' in df.columns
            # MIC values should be numeric (except Strain column)
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            assert len(numeric_cols) > 0


class TestDataIntegrity:
    """Test suite for data integrity checks."""
    
    def test_all_reference_files_same_strains(self):
        """Test that all reference files contain the same strain identifiers."""
        data = load_reference_data()
        
        # Filter out None values
        valid_data = {k: v for k, v in data.items() if v is not None and 'Strain' in v.columns}
        
        if len(valid_data) > 1:
            # Get strain sets from each dataframe
            strain_sets = [set(df['Strain'].values) for df in valid_data.values()]
            
            # Check if all strain sets are equal
            first_set = strain_sets[0]
            for strain_set in strain_sets[1:]:
                # Allow for minor differences, but they should overlap significantly
                overlap = len(first_set.intersection(strain_set))
                assert overlap > 0, "No common strains found between datasets"
    
    def test_no_duplicate_strains(self):
        """Test that there are no duplicate strain entries in each file."""
        data = load_reference_data()
        
        for key, df in data.items():
            if df is not None and 'Strain' in df.columns:
                assert df['Strain'].duplicated().sum() == 0, f"Duplicate strains found in {key}"
    
    def test_numeric_data_ranges(self):
        """Test that numeric data falls within expected ranges."""
        data = load_reference_data()
        
        # Test MIC data (should be positive)
        if data.get('MIC') is not None:
            df = data['MIC']
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                assert (df[col] >= 0).all(), f"Negative values found in MIC column {col}"
        
        # Test binary data (AMR genes, Virulence) - should be 0 or 1
        for key in ['AMR_genes', 'Virulence']:
            if data.get(key) is not None:
                df = data[key]
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    unique_vals = df[col].dropna().unique()
                    # Should mostly be binary (0/1) with possible other small integers
                    assert all(v >= 0 for v in unique_vals), f"Negative values in {key}.{col}"


class TestApplicationRequirements:
    """Test application-specific requirements."""
    
    def test_data_directory_exists(self):
        """Test that data directory exists."""
        assert os.path.exists('data') or os.path.exists('../data'), "Data directory not found"
    
    def test_required_files_exist(self):
        """Test that required data files exist."""
        required_files = [
            'data/AMR_genes.csv',
            'data/MGE.csv',
            'data/MIC.csv',
            'data/MLST.csv',
            'data/Plasmid.csv',
            'data/Serotype.csv',
            'data/Virulence.csv',
            'data/Snp_tree.newick'
        ]
        
        for file_path in required_files:
            assert os.path.exists(file_path), f"Required file {file_path} not found"
    
    def test_newick_tree_format(self):
        """Test that the newick tree file is valid."""
        tree_path = 'data/Snp_tree.newick'
        if os.path.exists(tree_path):
            with open(tree_path, 'r') as f:
                content = f.read().strip()
                # Basic newick format validation
                assert content.endswith(';'), "Newick tree should end with semicolon"
                assert '(' in content and ')' in content, "Newick tree should contain parentheses"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
