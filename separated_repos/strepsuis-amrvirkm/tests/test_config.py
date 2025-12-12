"""Tests for config module."""

import tempfile
from pathlib import Path

import pytest

from strepsuis_amrvirkm.config import Config


def test_config_defaults():
    """Test default configuration values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config(data_dir=tmpdir)
        assert hasattr(config, "bootstrap_iterations")
        assert hasattr(config, "fdr_alpha")
        assert hasattr(config, "random_seed")
        assert config.bootstrap_iterations == 500
        assert config.fdr_alpha == 0.05
        assert config.random_seed == 42


def test_config_custom_values():
    """Test configuration with custom values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config(
            data_dir=tmpdir,
            output_dir=tmpdir,
            bootstrap_iterations=1000,
            fdr_alpha=0.01,
            random_seed=123,
        )
        assert config.bootstrap_iterations == 1000
        assert config.fdr_alpha == 0.01
        assert config.random_seed == 123


def test_config_data_dir_validation():
    """Test data directory validation."""
    with pytest.raises(ValueError):
        Config(data_dir="/nonexistent/directory")


def test_config_fdr_alpha_validation():
    """Test FDR alpha validation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(ValueError):
            Config(data_dir=tmpdir, fdr_alpha=1.5)
        with pytest.raises(ValueError):
            Config(data_dir=tmpdir, fdr_alpha=-0.1)


def test_config_bootstrap_validation():
    """Test bootstrap iterations validation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(ValueError):
            Config(data_dir=tmpdir, bootstrap_iterations=50)


def test_config_output_dir_creation():
    """Test output directory is created if it doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "output"
        _ = Config(data_dir=tmpdir, output_dir=str(output_dir))
        assert output_dir.exists()


def test_config_from_dict():
    """Test Config creation from dictionary."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dict = {
            "data_dir": tmpdir,
            "output_dir": tmpdir,
            "bootstrap_iterations": 200,
            "fdr_alpha": 0.1,
        }
        config = Config.from_dict(config_dict)
        assert config.bootstrap_iterations == 200
        assert config.fdr_alpha == 0.1


def test_config_reporting_parameters():
    """Test reporting configuration parameters."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config(data_dir=tmpdir)
        assert hasattr(config, "generate_html")
        assert hasattr(config, "generate_excel")
        assert hasattr(config, "save_png_charts")
        assert config.generate_html is True
        assert config.generate_excel is True


def test_config_parallel_processing():
    """Test parallel processing configuration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config(data_dir=tmpdir, n_jobs=4)
        assert config.n_jobs == 4


def test_config_max_clusters_validation():
    """Test max_clusters >= min_clusters validation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(ValueError, match="max_clusters must be >= min_clusters"):
            Config(data_dir=tmpdir, min_clusters=10, max_clusters=5)


def test_config_valid_cluster_range():
    """Test valid cluster range configuration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config(data_dir=tmpdir, min_clusters=2, max_clusters=10)
        assert config.min_clusters == 2
        assert config.max_clusters == 10


def test_config_mca_components():
    """Test MCA components configuration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config(data_dir=tmpdir, mca_components=3)
        assert config.mca_components == 3


def test_config_association_rules():
    """Test association rules configuration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config(
            data_dir=tmpdir,
            min_support=0.2,
            min_confidence=0.6
        )
        assert config.min_support == 0.2
        assert config.min_confidence == 0.6


def test_config_dpi_setting():
    """Test DPI setting for charts."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config(data_dir=tmpdir, dpi=300)
        assert config.dpi == 300


def test_config_from_dict_ignores_unknown_keys():
    """Test that from_dict ignores unknown keys."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dict = {
            "data_dir": tmpdir,
            "output_dir": tmpdir,
            "unknown_key": "some_value",  # Should be ignored
            "another_unknown": 123,  # Should be ignored
            "bootstrap_iterations": 300,
        }
        config = Config.from_dict(config_dict)
        assert config.bootstrap_iterations == 300
        # Should not raise AttributeError
        assert not hasattr(config, "unknown_key")


def test_config_fdr_alpha_boundary_values():
    """Test FDR alpha at boundary values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test lower boundary
        with pytest.raises(ValueError):
            Config(data_dir=tmpdir, fdr_alpha=0.0)
        
        # Test upper boundary
        with pytest.raises(ValueError):
            Config(data_dir=tmpdir, fdr_alpha=1.0)
        
        # Test valid boundary values
        config = Config(data_dir=tmpdir, fdr_alpha=0.001)
        assert config.fdr_alpha == 0.001
        
        config = Config(data_dir=tmpdir, fdr_alpha=0.999)
        assert config.fdr_alpha == 0.999


def test_config_bootstrap_iterations_minimum():
    """Test bootstrap iterations minimum value."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test below minimum
        with pytest.raises(ValueError, match="bootstrap_iterations should be at least 100"):
            Config(data_dir=tmpdir, bootstrap_iterations=99)
        
        # Test at minimum
        config = Config(data_dir=tmpdir, bootstrap_iterations=100)
        assert config.bootstrap_iterations == 100
        
        # Test above minimum
        config = Config(data_dir=tmpdir, bootstrap_iterations=101)
        assert config.bootstrap_iterations == 101


def test_config_all_reporting_flags():
    """Test all reporting flags can be set."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config(
            data_dir=tmpdir,
            generate_html=False,
            generate_excel=False,
            save_png_charts=False
        )
        assert config.generate_html is False
        assert config.generate_excel is False
        assert config.save_png_charts is False


def test_config_negative_n_jobs():
    """Test negative n_jobs (use all cores)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config(data_dir=tmpdir, n_jobs=-1)
        assert config.n_jobs == -1
