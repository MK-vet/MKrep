"""
Extended Tests for Config Module

Tests configuration constants, settings, and validation.
"""

import pytest
from strepsuis_analyzer import config


class TestDefaultConfig:
    """Test default configuration settings."""

    def test_default_config_exists(self):
        """Test that DEFAULT_CONFIG exists."""
        assert hasattr(config, 'DEFAULT_CONFIG')
        assert isinstance(config.DEFAULT_CONFIG, dict)

    def test_default_config_has_random_state(self):
        """Test that default config has random_state."""
        assert 'random_state' in config.DEFAULT_CONFIG
        assert isinstance(config.DEFAULT_CONFIG['random_state'], int)
        assert config.DEFAULT_CONFIG['random_state'] >= 0

    def test_default_config_has_fdr_alpha(self):
        """Test that default config has fdr_alpha."""
        assert 'fdr_alpha' in config.DEFAULT_CONFIG
        assert 0 < config.DEFAULT_CONFIG['fdr_alpha'] < 1

    def test_default_config_has_mca_components(self):
        """Test that default config has n_mca_components."""
        assert 'n_mca_components' in config.DEFAULT_CONFIG
        assert config.DEFAULT_CONFIG['n_mca_components'] >= 1

    def test_default_config_has_clustering_method(self):
        """Test that default config has clustering_method."""
        assert 'clustering_method' in config.DEFAULT_CONFIG
        assert config.DEFAULT_CONFIG['clustering_method'] in ['ward', 'average', 'complete', 'single']

    def test_default_config_has_distance_metric(self):
        """Test that default config has distance_metric."""
        assert 'distance_metric' in config.DEFAULT_CONFIG
        assert config.DEFAULT_CONFIG['distance_metric'] in ['jaccard', 'hamming', 'euclidean']


class TestDataFilePatterns:
    """Test data file patterns configuration."""

    def test_data_file_patterns_exists(self):
        """Test that DATA_FILE_PATTERNS exists."""
        assert hasattr(config, 'DATA_FILE_PATTERNS')
        assert isinstance(config.DATA_FILE_PATTERNS, list)

    def test_data_file_patterns_not_empty(self):
        """Test that there are data file patterns."""
        assert len(config.DATA_FILE_PATTERNS) > 0

    def test_data_file_patterns_are_strings(self):
        """Test that all patterns are strings."""
        for pattern in config.DATA_FILE_PATTERNS:
            assert isinstance(pattern, str)

    def test_data_file_patterns_have_csv_extension(self):
        """Test that patterns have .csv extension."""
        for pattern in config.DATA_FILE_PATTERNS:
            assert pattern.endswith('.csv')


class TestTreeFilePattern:
    """Test tree file pattern configuration."""

    def test_tree_file_pattern_exists(self):
        """Test that TREE_FILE_PATTERN exists."""
        assert hasattr(config, 'TREE_FILE_PATTERN')
        assert isinstance(config.TREE_FILE_PATTERN, str)

    def test_tree_file_pattern_has_newick_extension(self):
        """Test that tree pattern has .newick extension."""
        assert config.TREE_FILE_PATTERN.endswith('.newick')


class TestOutputFiles:
    """Test output file configuration."""

    def test_output_files_exists(self):
        """Test that OUTPUT_FILES exists."""
        assert hasattr(config, 'OUTPUT_FILES')
        assert isinstance(config.OUTPUT_FILES, dict)

    def test_output_files_has_html_report(self):
        """Test that output files include HTML report."""
        assert 'html_report' in config.OUTPUT_FILES
        assert config.OUTPUT_FILES['html_report'].endswith('.html')

    def test_output_files_has_excel_report(self):
        """Test that output files include Excel report."""
        assert 'excel_report' in config.OUTPUT_FILES
        assert config.OUTPUT_FILES['excel_report'].endswith('.xlsx')

    def test_output_files_has_csv_outputs(self):
        """Test that output files include CSV outputs."""
        csv_outputs = [v for v in config.OUTPUT_FILES.values() if v.endswith('.csv')]
        assert len(csv_outputs) > 0


class TestPlotConfig:
    """Test plot configuration settings."""

    def test_plot_config_exists(self):
        """Test that PLOT_CONFIG exists."""
        assert hasattr(config, 'PLOT_CONFIG')
        assert isinstance(config.PLOT_CONFIG, dict)

    def test_plot_config_has_dpi(self):
        """Test that plot config has DPI setting."""
        assert 'dpi' in config.PLOT_CONFIG
        assert isinstance(config.PLOT_CONFIG['dpi'], int)
        assert config.PLOT_CONFIG['dpi'] > 0

    def test_plot_config_has_figure_format(self):
        """Test that plot config has figure format."""
        assert 'figure_format' in config.PLOT_CONFIG
        assert config.PLOT_CONFIG['figure_format'] in ['png', 'svg', 'pdf']

    def test_plot_config_has_plotly_template(self):
        """Test that plot config has plotly template."""
        assert 'plotly_template' in config.PLOT_CONFIG
        assert isinstance(config.PLOT_CONFIG['plotly_template'], str)

    def test_plot_config_has_color_palette(self):
        """Test that plot config has color palette."""
        assert 'color_palette' in config.PLOT_CONFIG
        assert isinstance(config.PLOT_CONFIG['color_palette'], str)


class TestBootstrapConfig:
    """Test bootstrap configuration settings."""

    def test_bootstrap_config_exists(self):
        """Test that BOOTSTRAP_CONFIG exists."""
        assert hasattr(config, 'BOOTSTRAP_CONFIG')
        assert isinstance(config.BOOTSTRAP_CONFIG, dict)

    def test_bootstrap_config_has_n_iterations(self):
        """Test that bootstrap config has n_iterations."""
        assert 'n_iterations' in config.BOOTSTRAP_CONFIG
        assert config.BOOTSTRAP_CONFIG['n_iterations'] >= 100

    def test_bootstrap_config_has_confidence_level(self):
        """Test that bootstrap config has confidence_level."""
        assert 'confidence_level' in config.BOOTSTRAP_CONFIG
        assert 0 < config.BOOTSTRAP_CONFIG['confidence_level'] < 1


class TestConfigValidation:
    """Test configuration validation logic."""

    def test_fdr_alpha_bounds(self):
        """Test FDR alpha is in valid range."""
        fdr = config.DEFAULT_CONFIG['fdr_alpha']
        assert 0 < fdr < 1, f"FDR alpha should be in (0, 1), got {fdr}"

    def test_confidence_level_bounds(self):
        """Test confidence level is in valid range."""
        conf = config.BOOTSTRAP_CONFIG['confidence_level']
        assert 0 < conf < 1, f"Confidence level should be in (0, 1), got {conf}"

    def test_n_mca_components_positive(self):
        """Test MCA components is positive."""
        n_comp = config.DEFAULT_CONFIG['n_mca_components']
        assert n_comp > 0, f"MCA components should be positive, got {n_comp}"

    def test_bootstrap_iterations_reasonable(self):
        """Test bootstrap iterations is reasonable (not too low)."""
        n_iter = config.BOOTSTRAP_CONFIG['n_iterations']
        assert n_iter >= 100, f"Bootstrap iterations should be >= 100, got {n_iter}"
        assert n_iter <= 100000, f"Bootstrap iterations should be <= 100000, got {n_iter}"


class TestConfigConsistency:
    """Test configuration consistency across settings."""

    def test_all_output_files_have_extensions(self):
        """Test that all output files have file extensions."""
        for key, filename in config.OUTPUT_FILES.items():
            assert '.' in filename, f"Output file '{key}' should have extension: {filename}"

    def test_data_file_patterns_unique(self):
        """Test that data file patterns are unique."""
        patterns = config.DATA_FILE_PATTERNS
        assert len(patterns) == len(set(patterns)), "Data file patterns should be unique"

    def test_reasonable_default_values(self):
        """Test that default values are reasonable."""
        # Random state should be a common seed
        assert config.DEFAULT_CONFIG['random_state'] in [0, 42, 123]
        
        # FDR alpha should be standard value
        assert config.DEFAULT_CONFIG['fdr_alpha'] in [0.01, 0.05, 0.10]
        
        # MCA components should be 2 or 3 (standard for visualization)
        assert config.DEFAULT_CONFIG['n_mca_components'] in [2, 3]
