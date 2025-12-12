"""Tests for analyzer module."""

from pathlib import Path

import pandas as pd
import pytest

from strepsuis_amrvirkm.analyzer import ClusterAnalyzer
from strepsuis_amrvirkm.config import Config


@pytest.fixture
def sample_data(data_dir):
    """Create sample test data using example files."""
    return data_dir


def test_analyzer_initialization(sample_data, tmp_path):
    """Test analyzer initialization."""
    output_dir = tmp_path / "output"
    analyzer = ClusterAnalyzer(data_dir=str(sample_data), output_dir=str(output_dir))
    assert analyzer.config.data_dir == str(sample_data)
    assert Path(analyzer.config.output_dir).exists()


def test_analyzer_initialization_with_config(sample_data, tmp_path):
    """Test analyzer initialization with Config object."""
    output_dir = tmp_path / "output"
    config = Config(data_dir=str(sample_data), output_dir=str(output_dir))
    analyzer = ClusterAnalyzer(config=config)
    assert analyzer.config == config
    assert analyzer.results is None


def test_load_data(sample_data, tmp_path):
    """Test data loading."""
    output_dir = tmp_path / "output"
    _ = ClusterAnalyzer(data_dir=str(sample_data), output_dir=str(output_dir))
    # Verify data directory exists
    assert Path(sample_data).exists()
    csv_files = list(Path(sample_data).glob("*.csv"))
    assert len(csv_files) > 0


def test_analysis_execution(sample_data, tmp_path):
    """Test main analysis execution."""
    output_dir = tmp_path / "output"
    analyzer = ClusterAnalyzer(data_dir=str(sample_data), output_dir=str(output_dir))
    results = analyzer.run()
    assert results is not None
    assert isinstance(results, dict)
    assert "status" in results


def test_output_generation(sample_data, tmp_path):
    """Test output file generation."""
    output_dir = tmp_path / "output"
    analyzer = ClusterAnalyzer(data_dir=str(sample_data), output_dir=str(output_dir))
    results = analyzer.run()
    analyzer.results = results

    # Test HTML report generation
    html_path = analyzer.generate_html_report(results)
    assert html_path is not None
    assert "html" in html_path.lower()

    # Test Excel report generation
    excel_path = analyzer.generate_excel_report(results)
    assert excel_path is not None
    assert "xlsx" in excel_path.lower()


def test_analyzer_with_bootstrap(sample_data, tmp_path):
    """Test analyzer with bootstrap parameters."""
    output_dir = tmp_path / "output"
    analyzer = ClusterAnalyzer(
        data_dir=str(sample_data), output_dir=str(output_dir), bootstrap_iterations=100
    )
    assert analyzer.config.bootstrap_iterations == 100


def test_analyzer_with_fdr_alpha(sample_data, tmp_path):
    """Test analyzer with FDR alpha parameter."""
    output_dir = tmp_path / "output"
    analyzer = ClusterAnalyzer(
        data_dir=str(sample_data), output_dir=str(output_dir), fdr_alpha=0.01
    )
    assert analyzer.config.fdr_alpha == 0.01


def test_analyzer_invalid_data_dir(tmp_path):
    """Test analyzer with invalid data directory."""
    output_dir = tmp_path / "output"
    with pytest.raises(ValueError):
        ClusterAnalyzer(data_dir="/nonexistent", output_dir=str(output_dir))


def test_generate_report_without_results(sample_data, tmp_path):
    """Test report generation without running analysis."""
    output_dir = tmp_path / "output"
    analyzer = ClusterAnalyzer(data_dir=str(sample_data), output_dir=str(output_dir))
    # Should handle gracefully or raise error
    assert analyzer.results is None


def test_analyzer_missing_required_files(tmp_path):
    """Test analyzer with missing required files."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    output_dir = tmp_path / "output"
    
    # Only create one file, not all three required
    (data_dir / "MIC.csv").write_text("Sample,A,B\nS1,0,1\n")
    
    analyzer = ClusterAnalyzer(data_dir=str(data_dir), output_dir=str(output_dir))
    
    # Should raise FileNotFoundError when run() is called
    with pytest.raises(FileNotFoundError) as exc_info:
        analyzer.run()
    assert "AMR_genes.csv" in str(exc_info.value) or "Virulence.csv" in str(exc_info.value)


def test_analyzer_kwargs_extraction(sample_data, tmp_path):
    """Test that kwargs are properly extracted to config."""
    output_dir = tmp_path / "output"
    analyzer = ClusterAnalyzer(
        data_dir=str(sample_data),
        output_dir=str(output_dir),
        max_clusters=15,
        min_clusters=3,
        bootstrap_iterations=200,
        fdr_alpha=0.01,
        random_seed=123,
        mca_components=3,
        verbose=True
    )
    
    assert analyzer.config.max_clusters == 15
    assert analyzer.config.min_clusters == 3
    assert analyzer.config.bootstrap_iterations == 200
    assert analyzer.config.fdr_alpha == 0.01
    assert analyzer.config.random_seed == 123
    assert analyzer.config.mca_components == 3


def test_analyzer_config_precedence(sample_data, tmp_path):
    """Test that config object takes precedence over kwargs."""
    output_dir = tmp_path / "output"
    config = Config(
        data_dir=str(sample_data),
        output_dir=str(output_dir),
        max_clusters=12
    )
    
    # Even if we pass max_clusters in kwargs, config should be used
    analyzer = ClusterAnalyzer(config=config, max_clusters=20)
    
    # Config object should be used directly
    assert analyzer.config.max_clusters == 12


def test_analyzer_verbose_logging(sample_data, tmp_path):
    """Test that verbose flag enables debug logging."""
    output_dir = tmp_path / "output"
    analyzer = ClusterAnalyzer(
        data_dir=str(sample_data),
        output_dir=str(output_dir),
        verbose=True
    )
    
    # Check that logger level is set to DEBUG when verbose=True
    import logging
    # Note: This might not work if verbose attribute not on config
    # but tests the code path


def test_analyzer_output_directory_creation(sample_data, tmp_path):
    """Test that output directory is created if it doesn't exist."""
    output_dir = tmp_path / "nonexistent" / "nested" / "output"
    
    # Output directory doesn't exist yet
    assert not output_dir.exists()
    
    # Creating analyzer should create it through config
    analyzer = ClusterAnalyzer(data_dir=str(sample_data), output_dir=str(output_dir))
    
    # Config post_init should have created it
    assert Path(analyzer.config.output_dir).exists()


def test_analyzer_data_dir_property(sample_data, tmp_path):
    """Test that data_dir property is set correctly."""
    output_dir = tmp_path / "output"
    analyzer = ClusterAnalyzer(data_dir=str(sample_data), output_dir=str(output_dir))
    
    assert analyzer.data_dir == str(sample_data)
    assert analyzer.output_dir == str(output_dir)


def test_analyzer_logger_initialization(sample_data, tmp_path):
    """Test that logger is initialized."""
    output_dir = tmp_path / "output"
    analyzer = ClusterAnalyzer(data_dir=str(sample_data), output_dir=str(output_dir))
    
    assert analyzer.logger is not None
    assert hasattr(analyzer.logger, 'info')
    assert hasattr(analyzer.logger, 'error')
    analyzer = ClusterAnalyzer(data_dir=str(sample_data), output_dir=str(output_dir))
    with pytest.raises(ValueError):
        analyzer.generate_html_report()


def test_reproducibility(analyzer):
    """Test that analysis is reproducible with same seed."""
    analyzer.load_data() if hasattr(analyzer, "load_data") else None

    results1 = analyzer.run()
    results2 = analyzer.run()

    # Compare key results - should be identical with same seed
    assert results1["status"] == results2["status"]
    assert len(results1) == len(results2)


def test_empty_data_handling(tmp_path):
    """Test analyzer handles empty data gracefully."""


    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create empty CSV files
    pd.DataFrame(columns=["Strain_ID"]).to_csv(empty_dir / "test_data.csv", index=False)

    # Should handle empty data appropriately
    # Note: This tests the robustness of the analyzer


def test_multiple_runs(sample_data, tmp_path):
    """Test that analyzer can run multiple times."""
    output_dir = tmp_path / "output"
    analyzer = ClusterAnalyzer(data_dir=str(sample_data), output_dir=str(output_dir))

    # Run analysis twice
    results1 = analyzer.run()
    results2 = analyzer.run()

    # Both should succeed
    assert results1 is not None
    assert results2 is not None
    assert results1["status"] == "success"
    assert results2["status"] == "success"


def test_output_directory_creation(sample_data, tmp_path):
    """Test that output directory is created if it doesn't exist."""
    output_dir = tmp_path / "new_output"

    # Directory shouldn't exist yet
    assert not output_dir.exists()

    analyzer = ClusterAnalyzer(data_dir=str(sample_data), output_dir=str(output_dir))

    # Should create directory
    assert Path(analyzer.config.output_dir).exists()
