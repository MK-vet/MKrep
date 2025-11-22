"""
Unit tests for strepsuis_amrvirkm core analysis functions.
These tests target functions with low coverage to reach 50%+ overall.
"""
import os
import tempfile

import pandas as pd
import pytest

from strepsuis_amrvirkm.analyzer import ClusterAnalyzer
from strepsuis_amrvirkm.config import Config


class TestConfigValidation:
    """Test configuration validation and edge cases."""

    def test_config_with_invalid_fdr_alpha(self):
        """Test that invalid fdr_alpha raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValueError, match="fdr_alpha must be between 0 and 1"):
                Config(data_dir=tmpdir, fdr_alpha=1.5)

    def test_config_with_zero_fdr_alpha(self):
        """Test that fdr_alpha=0 raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValueError, match="fdr_alpha must be between 0 and 1"):
                Config(data_dir=tmpdir, fdr_alpha=0.0)

    def test_config_with_low_bootstrap_iterations(self):
        """Test that bootstrap_iterations < 100 raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(
                ValueError, match="bootstrap_iterations should be at least 100"
            ):
                Config(data_dir=tmpdir, bootstrap_iterations=50)

    def test_config_with_invalid_cluster_range(self):
        """Test that max_clusters < min_clusters raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValueError, match="max_clusters must be >= min_clusters"):
                Config(data_dir=tmpdir, max_clusters=2, min_clusters=5)

    def test_config_with_nonexistent_data_dir(self):
        """Test that nonexistent data_dir raises ValueError."""
        with pytest.raises(ValueError, match="Data directory does not exist"):
            Config(data_dir="/nonexistent/path")

    def test_config_creates_output_dir(self):
        """Test that Config creates output directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = os.path.join(tmpdir, "new_output")
            assert not os.path.exists(output_dir)

            config = Config(data_dir=tmpdir, output_dir=output_dir)

            assert os.path.exists(output_dir)
            assert config.output_dir == output_dir

    def test_config_from_dict(self):
        """Test creating Config from dictionary."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dict = {
                "data_dir": tmpdir,
                "output_dir": tmpdir,
                "bootstrap_iterations": 500,
                "fdr_alpha": 0.05,
                "max_clusters": 8,
                "min_clusters": 3,
            }
            config = Config.from_dict(config_dict)

            assert config.data_dir == tmpdir
            assert config.bootstrap_iterations == 500
            assert config.max_clusters == 8
            assert config.min_clusters == 3


class TestAnalyzerInitialization:
    """Test ClusterAnalyzer initialization."""

    def test_analyzer_with_config_object(self):
        """Test creating analyzer with Config object."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Config(data_dir=tmpdir)
            analyzer = ClusterAnalyzer(config=config)

            assert analyzer.config == config
            assert analyzer.data_dir == tmpdir

    def test_analyzer_with_kwargs(self):
        """Test creating analyzer with keyword arguments."""
        with tempfile.TemporaryDirectory() as tmpdir:
            analyzer = ClusterAnalyzer(
                data_dir=tmpdir, bootstrap_iterations=300, max_clusters=8
            )

            assert analyzer.config.data_dir == tmpdir
            assert analyzer.config.bootstrap_iterations == 300
            assert analyzer.config.max_clusters == 8

    def test_analyzer_without_args_uses_defaults(self):
        """Test that analyzer without args uses current directory."""
        analyzer = ClusterAnalyzer()
        assert analyzer.config is not None


class TestConfigDefaults:
    """Test default configuration values."""

    def test_default_clustering_params(self):
        """Test default clustering parameters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Config(data_dir=tmpdir)
            assert config.max_clusters == 10
            assert config.min_clusters == 2
            assert config.mca_components == 2

    def test_default_association_params(self):
        """Test default association rule parameters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Config(data_dir=tmpdir)
            assert config.min_support == 0.1
            assert config.min_confidence == 0.5

    def test_default_bootstrap_iterations(self):
        """Test default bootstrap_iterations is 500."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Config(data_dir=tmpdir)
            assert config.bootstrap_iterations == 500
