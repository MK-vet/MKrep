#!/usr/bin/env python3
"""Quick workflow coverage tests - optimized for speed and coverage increase"""

import pytest
import pandas as pd
from pathlib import Path


@pytest.fixture
def example_data():
    """Load example data if available"""
    base_dir = Path(__file__).parent.parent
    examples_dir = base_dir / "examples"
    
    # Try to find data files
    data_files = list(examples_dir.glob("*.csv"))
    if not data_files:
        pytest.skip("Example data not available")
    
    data = {}
    for f in data_files:
        try:
            data[f.stem] = pd.read_csv(f)
        except:
            pass
    
    data["examples_dir"] = str(examples_dir)
    return data


class TestQuickWorkflow:
    """Quick workflow tests to increase coverage"""
    
    def test_config_and_analyzer_init(self, example_data, tmp_path):
        """Test configuration and analyzer initialization"""
        from strepsuis_amrvirkm.config import Config
        from strepsuis_amrvirkm.analyzer import get_analyzer
        
        config = Config(
            data_dir=example_data["examples_dir"],
            output_dir=str(tmp_path),
            bootstrap_iterations=10,
            random_seed=42
        )
        
        analyzer = get_analyzer(config)
        assert analyzer is not None
        assert analyzer.config == config
    
    def test_module_imports(self):
        """Test that core modules import successfully"""
        import strepsuis_amrvirkm
        from strepsuis_amrvirkm import config
        from strepsuis_amrvirkm import cli
        from strepsuis_amrvirkm import analyzer
        
        # Verify modules loaded
        assert config is not None
        assert cli is not None
        assert analyzer is not None
    
    def test_utilities_coverage(self):
        """Test utility functions to increase coverage"""
        from strepsuis_amrvirkm.config import Config
        
        # Test config creation
        config = Config()
        assert config.bootstrap_iterations > 0
        assert config.fdr_alpha > 0
        assert config.random_seed is not None
        
        # Test from_dict
        config_dict = {
            "data_dir": "/tmp/test",
            "output_dir": "/tmp/output"
        }
        config2 = Config.from_dict(config_dict)
        assert config2.data_dir == "/tmp/test"
