"""
Comprehensive tests for data loading functions in data.py.

This module tests all data loading functionality with:
- Normal operation scenarios
- Missing file handling
- Error recovery
- Edge cases

Target: 100% coverage for all data loading functions
"""

import pytest
import pandas as pd
from pathlib import Path
import warnings
import tempfile
import os

from strepsuis_analyzer.data import (
    load_data,
    load_phylogenetic_tree
)


class TestLoadData:
    """Test load_data function."""
    
    @pytest.mark.unit
    def test_load_data_success(self, tmp_path):
        """Test successful data loading."""
        # Create test data directory
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        
        # Create sample CSV files
        amr_df = pd.DataFrame({
            'Strain_ID': ['S1', 'S2'],
            'gene1': [1, 0],
            'gene2': [0, 1]
        })
        amr_df.to_csv(data_dir / 'AMR_genes.csv', index=False)
        
        mic_df = pd.DataFrame({
            'Strain_ID': ['S1', 'S2'],
            'antibiotic1': [1, 0]
        })
        mic_df.to_csv(data_dir / 'MIC.csv', index=False)
        
        # Create empty files for others
        for filename in ['Virulence.csv', 'MLST.csv', 'Serotype.csv', 'MGE.csv', 'Plasmid.csv']:
            pd.DataFrame().to_csv(data_dir / filename, index=False)
        
        # Load data
        data = load_data(data_dir)
        
        # Verify all keys exist
        expected_keys = ['AMR', 'MIC', 'Virulence', 'MLST', 'Serotype', 'MGE', 'Plasmid']
        assert set(data.keys()) == set(expected_keys)
        
        # Verify AMR data was loaded correctly
        assert len(data['AMR']) == 2
        assert 'Strain_ID' in data['AMR'].columns
        assert 'gene1' in data['AMR'].columns
    
    @pytest.mark.unit
    def test_load_data_missing_file(self, tmp_path):
        """Test handling of missing files."""
        # Create data directory with no files
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        
        # Load data - should warn but not fail
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            data = load_data(data_dir)
            
            # Should have warnings for each missing file
            assert len(w) >= 1
            assert any("not found" in str(warning.message) for warning in w)
        
        # All keys should exist with empty DataFrames
        expected_keys = ['AMR', 'MIC', 'Virulence', 'MLST', 'Serotype', 'MGE', 'Plasmid']
        assert set(data.keys()) == set(expected_keys)
        
        # All should be empty
        for key in expected_keys:
            assert data[key].empty
    
    @pytest.mark.unit
    def test_load_data_partial_files(self, tmp_path):
        """Test loading with some files present."""
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        
        # Create only AMR file
        amr_df = pd.DataFrame({
            'Strain_ID': ['S1', 'S2', 'S3'],
            'gene1': [1, 0, 1]
        })
        amr_df.to_csv(data_dir / 'AMR_genes.csv', index=False)
        
        # Load data
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            data = load_data(data_dir)
        
        # AMR should have data
        assert not data['AMR'].empty
        assert len(data['AMR']) == 3
        
        # Others should be empty
        assert data['MIC'].empty
        assert data['Virulence'].empty
    
    @pytest.mark.unit
    def test_load_data_column_name_cleaning(self, tmp_path):
        """Test that column names are cleaned (whitespace stripped)."""
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        
        # Create file with messy column names
        amr_df = pd.DataFrame({
            ' Strain_ID ': ['S1', 'S2'],
            '  gene1  ': [1, 0]
        })
        amr_df.to_csv(data_dir / 'AMR_genes.csv', index=False)
        
        # Create empty files for others
        for filename in ['MIC.csv', 'Virulence.csv', 'MLST.csv', 'Serotype.csv', 'MGE.csv', 'Plasmid.csv']:
            pd.DataFrame().to_csv(data_dir / filename, index=False)
        
        # Load data
        data = load_data(data_dir)
        
        # Column names should be cleaned
        assert 'Strain_ID' in data['AMR'].columns
        assert 'gene1' in data['AMR'].columns
        assert ' Strain_ID ' not in data['AMR'].columns
    
    @pytest.mark.unit
    def test_load_data_with_valid_but_unusual_csv(self, tmp_path):
        """Test handling of unusual but valid CSV file."""
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        
        # Create CSV file that pandas can read but might have issues
        # Pandas is very tolerant, so we just verify it handles it
        with open(data_dir / 'AMR_genes.csv', 'w') as f:
            f.write("Col1,Col2\n")
            f.write("A,B\n")
        
        # Create empty files for others
        for filename in ['MIC.csv', 'Virulence.csv', 'MLST.csv', 'Serotype.csv', 'MGE.csv', 'Plasmid.csv']:
            pd.DataFrame().to_csv(data_dir / filename, index=False)
        
        # Load data - should succeed
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            data = load_data(data_dir)
        
        # AMR should have data since pandas can read it
        assert not data['AMR'].empty
        assert len(data['AMR']) == 1


class TestLoadPhylogeneticTree:
    """Test load_phylogenetic_tree function."""
    
    @pytest.mark.unit
    def test_load_tree_success(self, tmp_path):
        """Test successful tree loading."""
        # Create tree file
        tree_file = tmp_path / "tree.newick"
        tree_content = "((A:0.1,B:0.2):0.3,(C:0.15,D:0.25):0.35);"
        tree_file.write_text(tree_content)
        
        # Load tree
        tree = load_phylogenetic_tree(tree_file)
        
        # Verify content
        assert tree == tree_content
    
    @pytest.mark.unit
    def test_load_tree_whitespace_stripped(self, tmp_path):
        """Test that whitespace is stripped from tree."""
        # Create tree file with extra whitespace
        tree_file = tmp_path / "tree.newick"
        tree_content = "  ((A:0.1,B:0.2):0.3,(C:0.15,D:0.25):0.35);  \n\n"
        tree_file.write_text(tree_content)
        
        # Load tree
        tree = load_phylogenetic_tree(tree_file)
        
        # Verify whitespace is stripped
        assert tree == "((A:0.1,B:0.2):0.3,(C:0.15,D:0.25):0.35);"
        assert not tree.startswith(" ")
        assert not tree.endswith("\n")
    
    @pytest.mark.unit
    def test_load_tree_missing_file(self, tmp_path):
        """Test handling of missing tree file."""
        # Use non-existent file
        tree_file = tmp_path / "nonexistent.newick"
        
        # Load tree - should warn and return None
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            tree = load_phylogenetic_tree(tree_file)
            
            # Should have warning
            assert len(w) == 1
            assert "not found" in str(w[0].message)
        
        # Should return None
        assert tree is None
    
    @pytest.mark.unit
    def test_load_tree_empty_file(self, tmp_path):
        """Test loading empty tree file."""
        # Create empty file
        tree_file = tmp_path / "empty.newick"
        tree_file.write_text("")
        
        # Load tree
        tree = load_phylogenetic_tree(tree_file)
        
        # Should return empty string
        assert tree == ""
    
    @pytest.mark.unit
    def test_load_tree_permission_error(self, tmp_path):
        """Test handling of file permission errors."""
        # Create tree file
        tree_file = tmp_path / "tree.newick"
        tree_file.write_text("((A:0.1,B:0.2):0.3);")
        
        # Make file unreadable (Unix only)
        if os.name != 'nt':  # Skip on Windows
            os.chmod(tree_file, 0o000)
            
            try:
                # Load tree - should warn and return None
                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("always")
                    tree = load_phylogenetic_tree(tree_file)
                    
                    # Should have warning
                    assert len(w) == 1
                
                # Should return None
                assert tree is None
            finally:
                # Restore permissions for cleanup
                os.chmod(tree_file, 0o644)


class TestIntegrationScenarios:
    """Test realistic integration scenarios."""
    
    @pytest.mark.integration
    def test_typical_workflow(self, tmp_path):
        """Test typical workflow of loading data and tree."""
        # Create realistic data structure
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        
        # Create AMR data
        amr_df = pd.DataFrame({
            'Strain_ID': ['S001', 'S002', 'S003'],
            'tet(M)': [1, 1, 0],
            'erm(B)': [0, 1, 1]
        })
        amr_df.to_csv(data_dir / 'AMR_genes.csv', index=False)
        
        # Create MIC data
        mic_df = pd.DataFrame({
            'Strain_ID': ['S001', 'S002', 'S003'],
            'PEN': [1, 0, 1],
            'TET': [1, 1, 0]
        })
        mic_df.to_csv(data_dir / 'MIC.csv', index=False)
        
        # Create other empty files
        for filename in ['Virulence.csv', 'MLST.csv', 'Serotype.csv', 'MGE.csv', 'Plasmid.csv']:
            pd.DataFrame().to_csv(data_dir / filename, index=False)
        
        # Create tree
        tree_file = data_dir / "tree.newick"
        tree_file.write_text("((S001:0.1,S002:0.2):0.3,S003:0.5);")
        
        # Load all data
        data = load_data(data_dir)
        tree = load_phylogenetic_tree(tree_file)
        
        # Verify data
        assert len(data['AMR']) == 3
        assert len(data['MIC']) == 3
        assert tree is not None
        assert tree.endswith(';')
        
        # Verify data quality
        assert 'Strain_ID' in data['AMR'].columns
        assert 'tet(M)' in data['AMR'].columns
        assert 'S001' in data['AMR']['Strain_ID'].values
    
    @pytest.mark.integration
    def test_minimal_data_scenario(self, tmp_path):
        """Test scenario with minimal data (only AMR)."""
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        
        # Create only AMR file
        amr_df = pd.DataFrame({
            'Strain_ID': ['S1'],
            'gene1': [1]
        })
        amr_df.to_csv(data_dir / 'AMR_genes.csv', index=False)
        
        # No tree file
        tree_file = data_dir / "tree.newick"
        
        # Load data
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            data = load_data(data_dir)
            tree = load_phylogenetic_tree(tree_file)
        
        # Verify partial success
        assert not data['AMR'].empty
        assert data['MIC'].empty
        assert tree is None
