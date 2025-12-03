"""
Basic tests for StrepSuis Analyzer
"""

import os
import sys
import tempfile
from pathlib import Path
import pandas as pd
import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from StrepSuisPhyloCluster_2025_08_11 import StrepSuisAnalyzer


def test_analyzer_initialization():
    """Test that analyzer initializes correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        analyzer = StrepSuisAnalyzer(output_dir=tmpdir, random_state=42)
        assert analyzer.output_dir == Path(tmpdir)
        assert analyzer.random_state == 42
        assert analyzer.data is None
        assert analyzer.tree is None


def test_load_data_single_file():
    """Test loading a single CSV file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test data
        test_data = pd.DataFrame({
            'Strain_ID': ['S1', 'S2', 'S3'],
            'Gene1': [1, 0, 1],
            'Gene2': [0, 1, 1]
        })
        test_file = os.path.join(tmpdir, 'test.csv')
        test_data.to_csv(test_file, index=False)
        
        # Load data
        analyzer = StrepSuisAnalyzer(output_dir=tmpdir)
        analyzer.load_data([test_file])
        
        assert analyzer.data is not None
        assert len(analyzer.data) == 3
        assert 'Strain_ID' in analyzer.data.columns
        assert 'Gene1' in analyzer.data.columns


def test_load_data_multiple_files():
    """Test loading and merging multiple CSV files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test data files
        data1 = pd.DataFrame({
            'Strain_ID': ['S1', 'S2', 'S3'],
            'Gene1': [1, 0, 1],
        })
        data2 = pd.DataFrame({
            'Strain_ID': ['S1', 'S2', 'S3'],
            'Gene2': [0, 1, 1]
        })
        
        file1 = os.path.join(tmpdir, 'data1.csv')
        file2 = os.path.join(tmpdir, 'data2.csv')
        data1.to_csv(file1, index=False)
        data2.to_csv(file2, index=False)
        
        # Load data
        analyzer = StrepSuisAnalyzer(output_dir=tmpdir)
        analyzer.load_data([file1, file2])
        
        assert analyzer.data is not None
        assert len(analyzer.data) == 3
        assert 'Gene1' in analyzer.data.columns
        assert 'Gene2' in analyzer.data.columns


def test_clustering():
    """Test clustering functionality."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test data
        test_data = pd.DataFrame({
            'Strain_ID': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
            'Gene1': [1, 1, 1, 0, 0, 0],
            'Gene2': [1, 1, 0, 0, 0, 1],
            'Gene3': [0, 1, 1, 1, 0, 0]
        })
        test_file = os.path.join(tmpdir, 'test.csv')
        test_data.to_csv(test_file, index=False)
        
        # Run clustering
        analyzer = StrepSuisAnalyzer(output_dir=tmpdir)
        analyzer.load_data([test_file])
        analyzer.perform_clustering(n_clusters=2)
        
        assert analyzer.clusters is not None
        assert len(analyzer.clusters) == 6
        assert 'Cluster' in analyzer.data.columns
        assert analyzer.data['Cluster'].nunique() == 2


def test_trait_associations():
    """Test trait association analysis."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test data with clear associations
        test_data = pd.DataFrame({
            'Strain_ID': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
            'Gene1': [1, 1, 1, 0, 0, 0],
            'Gene2': [1, 1, 0, 0, 0, 1],
            'Gene3': [0, 1, 1, 1, 0, 0]
        })
        test_file = os.path.join(tmpdir, 'test.csv')
        test_data.to_csv(test_file, index=False)
        
        # Run analysis
        analyzer = StrepSuisAnalyzer(output_dir=tmpdir)
        analyzer.load_data([test_file])
        analyzer.perform_clustering(n_clusters=2)
        analyzer.calculate_trait_associations()
        
        assert 'trait_associations' in analyzer.results
        results = analyzer.results['trait_associations']
        assert 'Feature' in results.columns
        assert 'P_value' in results.columns
        assert 'P_adj' in results.columns
        assert 'Significant' in results.columns


def test_csv_output():
    """Test CSV output generation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test data
        test_data = pd.DataFrame({
            'Strain_ID': ['S1', 'S2', 'S3'],
            'Gene1': [1, 0, 1],
            'Gene2': [0, 1, 1]
        })
        test_file = os.path.join(tmpdir, 'test.csv')
        test_data.to_csv(test_file, index=False)
        
        # Run analysis
        analyzer = StrepSuisAnalyzer(output_dir=tmpdir)
        analyzer.load_data([test_file])
        analyzer.perform_clustering(n_clusters=2)
        analyzer.calculate_trait_associations()
        analyzer.save_csv_outputs()
        
        # Check outputs
        assert os.path.exists(os.path.join(tmpdir, 'clustered_data.csv'))
        assert os.path.exists(os.path.join(tmpdir, 'trait_associations.csv'))


def test_excel_output():
    """Test Excel output generation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test data
        test_data = pd.DataFrame({
            'Strain_ID': ['S1', 'S2', 'S3'],
            'Gene1': [1, 0, 1],
            'Gene2': [0, 1, 1]
        })
        test_file = os.path.join(tmpdir, 'test.csv')
        test_data.to_csv(test_file, index=False)
        
        # Run analysis
        analyzer = StrepSuisAnalyzer(output_dir=tmpdir)
        analyzer.load_data([test_file])
        analyzer.perform_clustering(n_clusters=2)
        analyzer.calculate_trait_associations()
        analyzer.generate_excel_report()
        
        # Check output
        excel_path = os.path.join(tmpdir, 'analysis_results.xlsx')
        assert os.path.exists(excel_path)
        
        # Verify sheets
        excel_data = pd.ExcelFile(excel_path)
        assert 'Clustered_Data' in excel_data.sheet_names
        assert 'Cluster_Summary' in excel_data.sheet_names
        assert 'Trait_Associations' in excel_data.sheet_names
        assert 'Metadata' in excel_data.sheet_names


def test_html_output():
    """Test HTML output generation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test data
        test_data = pd.DataFrame({
            'Strain_ID': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
            'Gene1': [1, 1, 1, 0, 0, 0],
            'Gene2': [1, 1, 0, 0, 0, 1],
        })
        test_file = os.path.join(tmpdir, 'test.csv')
        test_data.to_csv(test_file, index=False)
        
        # Run analysis
        analyzer = StrepSuisAnalyzer(output_dir=tmpdir)
        analyzer.load_data([test_file])
        analyzer.perform_clustering(n_clusters=2)
        analyzer.calculate_trait_associations()
        analyzer.perform_mca()
        analyzer.generate_html_report()
        
        # Check output
        html_path = os.path.join(tmpdir, 'analysis_report.html')
        assert os.path.exists(html_path)
        
        # Verify HTML content
        with open(html_path, 'r') as f:
            html_content = f.read()
            assert 'StrepSuis' in html_content
            assert 'Bootstrap' in html_content  # Bootstrap CSS
            assert 'plotly' in html_content.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
