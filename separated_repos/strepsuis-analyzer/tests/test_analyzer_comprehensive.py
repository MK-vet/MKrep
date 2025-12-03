"""
Comprehensive Tests for Analyzer Module

Tests analyzer.py import mechanisms and fallback behavior.
"""

import pytest
import sys
import warnings

from strepsuis_analyzer import analyzer


class TestAnalyzerImport:
    """Test analyzer module import and re-export."""

    def test_analyzer_module_exists(self):
        """Test that analyzer module exists."""
        assert analyzer is not None

    def test_strepsuis_analyzer_class_available(self):
        """Test that StrepSuisAnalyzer class is available."""
        assert hasattr(analyzer, 'StrepSuisAnalyzer')

    def test_strepsuis_analyzer_is_importable(self):
        """Test that StrepSuisAnalyzer can be imported."""
        from strepsuis_analyzer.analyzer import StrepSuisAnalyzer
        assert StrepSuisAnalyzer is not None

    def test_strepsuis_analyzer_can_be_instantiated(self):
        """Test that StrepSuisAnalyzer can be instantiated."""
        from strepsuis_analyzer.analyzer import StrepSuisAnalyzer
        
        # Should be able to create instance
        analyzer_instance = StrepSuisAnalyzer(output_dir='test_output', random_state=42)
        assert analyzer_instance is not None
        assert analyzer_instance.random_state == 42

    def test_analyzer_has_all_attribute(self):
        """Test that analyzer module has __all__ defined."""
        assert hasattr(analyzer, '__all__')
        assert 'StrepSuisAnalyzer' in analyzer.__all__

    def test_analyzer_class_methods(self):
        """Test that analyzer class has expected methods."""
        from strepsuis_analyzer.analyzer import StrepSuisAnalyzer
        
        # Check for key methods
        assert hasattr(StrepSuisAnalyzer, 'load_data')
        assert hasattr(StrepSuisAnalyzer, 'load_tree')
        assert hasattr(StrepSuisAnalyzer, 'perform_clustering')
        assert hasattr(StrepSuisAnalyzer, 'calculate_trait_associations')
        assert hasattr(StrepSuisAnalyzer, 'perform_mca')
        assert hasattr(StrepSuisAnalyzer, 'generate_html_report')
        assert hasattr(StrepSuisAnalyzer, 'generate_excel_report')
        assert hasattr(StrepSuisAnalyzer, 'run_full_analysis')


class TestAnalyzerFallback:
    """Test analyzer fallback behavior."""

    def test_analyzer_import_path_handling(self):
        """Test that analyzer handles import path correctly."""
        from strepsuis_analyzer import analyzer as ana_module
        
        # Should have modified sys.path
        assert ana_module is not None

    def test_analyzer_can_create_instance_with_defaults(self):
        """Test creating analyzer with default parameters."""
        from strepsuis_analyzer.analyzer import StrepSuisAnalyzer
        
        analyzer_instance = StrepSuisAnalyzer()
        assert analyzer_instance.random_state == 42  # Default
        assert analyzer_instance.output_dir.name == 'output'  # Default

    def test_analyzer_can_create_instance_with_custom_params(self):
        """Test creating analyzer with custom parameters."""
        from strepsuis_analyzer.analyzer import StrepSuisAnalyzer
        
        analyzer_instance = StrepSuisAnalyzer(
            output_dir='custom_output',
            random_state=123
        )
        assert analyzer_instance.random_state == 123
        assert 'custom_output' in str(analyzer_instance.output_dir)


class TestAnalyzerIntegration:
    """Integration tests for analyzer module."""

    def test_analyzer_workflow_basic(self):
        """Test basic analyzer workflow."""
        import tempfile
        import shutil
        import pandas as pd
        from pathlib import Path
        from strepsuis_analyzer.analyzer import StrepSuisAnalyzer
        
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Create test data
            test_data = pd.DataFrame({
                'Strain_ID': ['S1', 'S2', 'S3', 'S4', 'S5'],
                'Gene1': [1, 0, 1, 0, 1],
                'Gene2': [0, 1, 1, 0, 0],
                'Gene3': [1, 1, 0, 0, 1]
            })
            test_csv = Path(temp_dir) / 'test.csv'
            test_data.to_csv(test_csv, index=False)
            
            output_dir = Path(temp_dir) / 'output'
            
            # Create analyzer
            analyzer = StrepSuisAnalyzer(output_dir=str(output_dir), random_state=42)
            
            # Load data
            analyzer.load_data([str(test_csv)])
            
            # Verify data loaded
            assert analyzer.data is not None
            assert len(analyzer.data) == 5
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_analyzer_state_management(self):
        """Test that analyzer manages state correctly."""
        from strepsuis_analyzer.analyzer import StrepSuisAnalyzer
        
        analyzer = StrepSuisAnalyzer()
        
        # Initial state
        assert analyzer.data is None
        assert analyzer.tree is None
        assert analyzer.clusters is None
        assert analyzer.results == {}
