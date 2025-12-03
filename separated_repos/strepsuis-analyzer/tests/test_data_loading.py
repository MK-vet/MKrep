"""
Tests for data loading and file I/O operations.
"""

import pytest
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import load_data, load_phylogenetic_tree


class TestDataLoading:
    """Test data loading functions."""
    
    @pytest.mark.integration
    def test_load_data_returns_dict(self):
        """Test that load_data returns a dictionary."""
        data = load_data()
        assert isinstance(data, dict)
    
    @pytest.mark.integration
    def test_load_data_expected_keys(self):
        """Test that load_data contains expected keys."""
        data = load_data()
        
        expected_keys = {'AMR', 'MIC', 'Virulence', 'MLST', 'Serotype', 'MGE', 'Plasmid'}
        assert set(data.keys()) == expected_keys
    
    @pytest.mark.integration
    def test_load_data_all_dataframes(self):
        """Test that all loaded data are DataFrames."""
        data = load_data()
        
        for key, df in data.items():
            assert isinstance(df, pd.DataFrame)
    
    @pytest.mark.integration
    def test_load_amr_data(self):
        """Test AMR data loading."""
        data = load_data()
        amr_df = data['AMR']
        
        # Should have Strain column
        assert 'Strain' in amr_df.columns
        
        # Should have multiple rows
        assert len(amr_df) > 0
        
        # Should have gene columns
        gene_cols = [col for col in amr_df.columns if col != 'Strain']
        assert len(gene_cols) > 0
    
    @pytest.mark.integration
    def test_load_mic_data(self):
        """Test MIC data loading."""
        data = load_data()
        mic_df = data['MIC']
        
        # Should have Strain column
        assert 'Strain' in mic_df.columns
        
        # Should have antibiotic columns
        antibiotic_cols = [col for col in mic_df.columns if col != 'Strain']
        assert len(antibiotic_cols) > 0
    
    @pytest.mark.integration
    def test_load_virulence_data(self):
        """Test Virulence data loading."""
        data = load_data()
        vir_df = data['Virulence']
        
        # Should have Strain_ID column (may have spaces)
        strain_col = [col for col in vir_df.columns if 'Strain' in col]
        assert len(strain_col) > 0
        
        # Should have virulence factor columns
        assert len(vir_df.columns) > 1
    
    @pytest.mark.integration
    def test_load_mlst_data(self):
        """Test MLST data loading."""
        data = load_data()
        mlst_df = data['MLST']
        
        # Should have Strain and ST columns
        assert 'Strain' in mlst_df.columns
        assert 'ST' in mlst_df.columns
    
    @pytest.mark.integration
    def test_load_serotype_data(self):
        """Test Serotype data loading."""
        data = load_data()
        serotype_df = data['Serotype']
        
        # Should have Strain and Serotype columns
        assert 'Strain' in serotype_df.columns
        assert 'Serotype' in serotype_df.columns
    
    @pytest.mark.integration
    def test_data_consistency(self):
        """Test that all datasets have consistent strain counts."""
        data = load_data()
        
        # Get strain counts from each dataset
        counts = {}
        for key, df in data.items():
            if not df.empty and 'Strain' in df.columns:
                counts[key] = len(df)
        
        # AMR, MIC, Virulence, MLST, Serotype should have same count
        main_datasets = ['AMR', 'MIC', 'Virulence', 'MLST', 'Serotype']
        main_counts = [counts.get(k, 0) for k in main_datasets if k in counts]
        
        if len(main_counts) > 1:
            # All should be equal
            assert len(set(main_counts)) == 1
    
    @pytest.mark.integration
    def test_column_name_cleaning(self):
        """Test that column names are cleaned (no leading/trailing spaces)."""
        data = load_data()
        
        for key, df in data.items():
            if not df.empty:
                for col in df.columns:
                    # No leading or trailing spaces
                    assert col == col.strip()


class TestPhylogeneticTreeLoading:
    """Test phylogenetic tree loading."""
    
    @pytest.mark.integration
    def test_load_tree_returns_string_or_none(self):
        """Test that load_phylogenetic_tree returns string or None."""
        tree = load_phylogenetic_tree()
        assert isinstance(tree, (str, type(None)))
    
    @pytest.mark.integration
    def test_load_tree_content(self):
        """Test that loaded tree has valid content."""
        tree = load_phylogenetic_tree()
        
        if tree is not None:
            # Should be non-empty
            assert len(tree) > 0
            
            # Newick format should contain parentheses
            assert '(' in tree or ')' in tree or ',' in tree
    
    @pytest.mark.integration
    def test_tree_file_exists(self):
        """Test that tree file exists in data directory."""
        from pathlib import Path
        data_dir = Path(__file__).parent.parent / "data"
        tree_file = data_dir / "Snp_tree.newick"
        assert tree_file.exists()


class TestDataIntegrity:
    """Test data integrity and format."""
    
    @pytest.mark.integration
    def test_amr_binary_values(self):
        """Test that AMR data contains only binary values."""
        data = load_data()
        amr_df = data['AMR']
        
        if not amr_df.empty:
            # Exclude Strain column
            gene_cols = [col for col in amr_df.columns if col != 'Strain']
            
            for col in gene_cols:
                unique_vals = amr_df[col].unique()
                # Should only contain 0, 1, or NaN
                assert all(val in [0, 1] or pd.isna(val) for val in unique_vals)
    
    @pytest.mark.integration
    def test_mic_numeric_values(self):
        """Test that MIC data contains numeric values."""
        data = load_data()
        mic_df = data['MIC']
        
        if not mic_df.empty:
            # Exclude Strain column
            antibiotic_cols = [col for col in mic_df.columns if col != 'Strain']
            
            for col in antibiotic_cols:
                # Should be numeric (float or int)
                assert pd.api.types.is_numeric_dtype(mic_df[col])
    
    @pytest.mark.integration
    def test_strain_id_uniqueness(self):
        """Test that Strain IDs are unique within each dataset."""
        data = load_data()
        
        # MGE and Plasmid can have multiple rows per strain (multiple values)
        # Only check main datasets
        for key, df in data.items():
            if not df.empty and 'Strain' in df.columns and key not in ['MGE', 'Plasmid']:
                # Check for duplicates
                assert len(df['Strain']) == len(df['Strain'].unique())
    
    @pytest.mark.integration
    def test_no_null_strain_ids(self):
        """Test that there are no null Strain IDs."""
        data = load_data()
        
        for key, df in data.items():
            if not df.empty and 'Strain' in df.columns:
                assert df['Strain'].notna().all()
    
    @pytest.mark.integration
    def test_mlst_values(self):
        """Test that MLST values are valid."""
        data = load_data()
        mlst_df = data['MLST']
        
        if not mlst_df.empty and 'ST' in mlst_df.columns:
            # Should have non-null values
            assert mlst_df['ST'].notna().any()
    
    @pytest.mark.integration
    def test_serotype_values(self):
        """Test that Serotype values are valid."""
        data = load_data()
        serotype_df = data['Serotype']
        
        if not serotype_df.empty and 'Serotype' in serotype_df.columns:
            # Should have non-null values
            assert serotype_df['Serotype'].notna().any()


class TestDataCache:
    """Test data caching behavior."""
    
    @pytest.mark.integration
    def test_load_data_cached(self):
        """Test that load_data caching works."""
        # First call
        data1 = load_data()
        
        # Second call (should be cached)
        data2 = load_data()
        
        # Streamlit cache may create new dict, but content should be equivalent
        assert set(data1.keys()) == set(data2.keys())
        for key in data1.keys():
            assert data1[key].equals(data2[key])
    
    @pytest.mark.integration
    def test_load_tree_cached(self):
        """Test that load_phylogenetic_tree caching works."""
        # First call
        tree1 = load_phylogenetic_tree()
        
        # Second call (should be cached)
        tree2 = load_phylogenetic_tree()
        
        # Should return the same content (even if different objects)
        if tree1 is not None:
            assert tree1 == tree2
