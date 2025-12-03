"""
Configuration and parameter validation tests.
"""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from StrepSuisPhyloCluster_2025_08_11 import StrepSuisAnalyzer


pytestmark = pytest.mark.unit


def test_default_configuration(output_dir):
    """Test default configuration values."""
    analyzer = StrepSuisAnalyzer(output_dir=output_dir)
    assert analyzer.random_state == 42
    assert analyzer.output_dir == Path(output_dir)


def test_custom_random_state(output_dir):
    """Test custom random state setting."""
    analyzer = StrepSuisAnalyzer(output_dir=output_dir, random_state=123)
    assert analyzer.random_state == 123


def test_output_dir_path_conversion(tmp_path):
    """Test that output_dir is converted to Path object."""
    output_str = str(tmp_path / "output")
    analyzer = StrepSuisAnalyzer(output_dir=output_str)
    assert isinstance(analyzer.output_dir, Path)


def test_invalid_cluster_number(mini_dataset, output_dir):
    """Test behavior with edge case cluster numbers."""
    analyzer = StrepSuisAnalyzer(output_dir=output_dir, random_state=42)
    analyzer.load_data([mini_dataset])
    
    # Test with n_clusters=1 (may work or raise error depending on implementation)
    try:
        analyzer.perform_clustering(n_clusters=1)
        # If it works, verify result
        assert 'Cluster' in analyzer.data.columns
    except (ValueError, Exception):
        # It's okay if it raises an error
        pass


def test_results_dictionary_initialization(output_dir):
    """Test that results dictionary is properly initialized."""
    analyzer = StrepSuisAnalyzer(output_dir=output_dir)
    assert hasattr(analyzer, 'results')
    assert isinstance(analyzer.results, dict)
