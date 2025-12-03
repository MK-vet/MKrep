"""
Basic functionality tests for StrepSuis Analyzer.
"""

import sys
from pathlib import Path
import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from StrepSuisPhyloCluster_2025_08_11 import StrepSuisAnalyzer


pytestmark = pytest.mark.unit


def test_import():
    """Test that the module can be imported."""
    assert StrepSuisAnalyzer is not None


def test_version_exists():
    """Test that version is defined."""
    from strepsuis_analyzer import __version__
    assert __version__ is not None
    assert len(__version__) > 0


def test_analyzer_class_exists():
    """Test that StrepSuisAnalyzer class exists."""
    assert hasattr(StrepSuisAnalyzer, '__init__')
    assert hasattr(StrepSuisAnalyzer, 'load_data')
    assert hasattr(StrepSuisAnalyzer, 'perform_clustering')


def test_basic_instantiation(output_dir):
    """Test basic analyzer instantiation."""
    analyzer = StrepSuisAnalyzer(output_dir=output_dir, random_state=42)
    assert analyzer is not None
    assert analyzer.random_state == 42


def test_output_dir_creation(tmp_path):
    """Test that output directory is created if it doesn't exist."""
    new_dir = tmp_path / "new_output"
    _ = StrepSuisAnalyzer(output_dir=new_dir, random_state=42)  # analyzer unused in this test
    assert new_dir.exists()
