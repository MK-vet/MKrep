"""
Data validation tests for StrepSuis Analyzer.
"""

import sys
from pathlib import Path
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from StrepSuisPhyloCluster_2025_08_11 import StrepSuisAnalyzer


pytestmark = pytest.mark.unit


def test_binary_data_validation(tmp_path, output_dir):
    """Test that non-binary data is handled correctly."""
    # Create data with non-binary values
    data_file = tmp_path / "non_binary.csv"
    data = pd.DataFrame({
        'Strain_ID': ['S1', 'S2', 'S3'],
        'Gene1': [0, 1, 2],  # Contains value 2 (non-binary)
        'Gene2': [0, 1, 0]
    })
    data.to_csv(data_file, index=False)
    
    analyzer = StrepSuisAnalyzer(output_dir=output_dir)
    # Should load but may give warnings or convert values
    analyzer.load_data([data_file])
    assert analyzer.data is not None


def test_missing_strain_id_column(tmp_path, output_dir):
    """Test handling of missing Strain_ID column."""
    data_file = tmp_path / "no_strain_id.csv"
    data = pd.DataFrame({
        'SampleID': ['S1', 'S2', 'S3'],  # Wrong column name
        'Gene1': [0, 1, 1],
        'Gene2': [1, 0, 1]
    })
    data.to_csv(data_file, index=False)
    
    analyzer = StrepSuisAnalyzer(output_dir=output_dir)
    # Should handle missing Strain_ID column
    with pytest.raises((KeyError, ValueError, Exception)):
        analyzer.load_data([data_file])


def test_empty_dataframe(tmp_path, output_dir):
    """Test handling of empty data file."""
    data_file = tmp_path / "empty.csv"
    data = pd.DataFrame()
    data.to_csv(data_file, index=False)
    
    analyzer = StrepSuisAnalyzer(output_dir=output_dir)
    with pytest.raises((ValueError, Exception)):
        analyzer.load_data([data_file])


def test_duplicate_strain_ids(tmp_path, output_dir):
    """Test handling of duplicate strain IDs."""
    data_file = tmp_path / "duplicates.csv"
    data = pd.DataFrame({
        'Strain_ID': ['S1', 'S1', 'S2'],  # Duplicate S1
        'Gene1': [0, 1, 1],
        'Gene2': [1, 0, 1]
    })
    data.to_csv(data_file, index=False)
    
    analyzer = StrepSuisAnalyzer(output_dir=output_dir)
    # Should handle duplicates (may keep all, keep last, or raise error)
    analyzer.load_data([data_file])
    # Just verify it loaded some data
    assert len(analyzer.data) >= 2  # At least unique strains should be present


def test_missing_values_handling(tmp_path, output_dir):
    """Test handling of missing values in data."""
    data_file = tmp_path / "missing.csv"
    data = pd.DataFrame({
        'Strain_ID': ['S1', 'S2', 'S3'],
        'Gene1': [0, None, 1],  # Missing value
        'Gene2': [1, 0, 1]
    })
    data.to_csv(data_file, index=False)
    
    analyzer = StrepSuisAnalyzer(output_dir=output_dir)
    analyzer.load_data([data_file])
    # Missing values should be filled with 0
    assert analyzer.data.isna().sum().sum() == 0
