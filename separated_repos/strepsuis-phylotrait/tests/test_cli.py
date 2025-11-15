"""Tests for CLI module."""
import pytest
from click.testing import CliRunner
from strepsuis_phylotrait.cli import main
from pathlib import Path
import tempfile


def test_cli_help():
    """Test CLI help command."""
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert 'Usage:' in result.output or 'usage:' in result.output.lower()


def test_cli_version():
    """Test CLI version command."""
    runner = CliRunner()
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    assert '1.0.0' in result.output


def test_cli_missing_required_args():
    """Test CLI with missing required arguments."""
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code != 0


def test_cli_with_valid_args():
    """Test CLI with valid arguments."""
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        data_dir = Path(tmpdir) / "data"
        data_dir.mkdir()
        # Create a dummy CSV file
        import pandas as pd
        df = pd.DataFrame({'test': [1, 2, 3]})
        df.to_csv(data_dir / "test.csv", index=False)
        
        result = runner.invoke(main, [
            '--data-dir', str(data_dir),
            '--output', str(Path(tmpdir) / "output")
        ])
        assert result.exit_code == 0


def test_cli_with_bootstrap_option():
    """Test CLI with bootstrap iterations option."""
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        data_dir = Path(tmpdir) / "data"
        data_dir.mkdir()
        import pandas as pd
        df = pd.DataFrame({'test': [1, 2, 3]})
        df.to_csv(data_dir / "test.csv", index=False)
        
        result = runner.invoke(main, [
            '--data-dir', str(data_dir),
            '--output', str(Path(tmpdir) / "output"),
            '--bootstrap', '100'
        ])
        assert result.exit_code == 0


def test_cli_with_fdr_alpha_option():
    """Test CLI with FDR alpha option."""
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        data_dir = Path(tmpdir) / "data"
        data_dir.mkdir()
        import pandas as pd
        df = pd.DataFrame({'test': [1, 2, 3]})
        df.to_csv(data_dir / "test.csv", index=False)
        
        result = runner.invoke(main, [
            '--data-dir', str(data_dir),
            '--output', str(Path(tmpdir) / "output"),
            '--fdr-alpha', '0.01'
        ])
        assert result.exit_code == 0


def test_cli_with_verbose_option():
    """Test CLI with verbose option."""
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        data_dir = Path(tmpdir) / "data"
        data_dir.mkdir()
        import pandas as pd
        df = pd.DataFrame({'test': [1, 2, 3]})
        df.to_csv(data_dir / "test.csv", index=False)
        
        result = runner.invoke(main, [
            '--data-dir', str(data_dir),
            '--output', str(Path(tmpdir) / "output"),
            '--verbose'
        ])
        assert result.exit_code == 0


def test_cli_with_invalid_data_dir():
    """Test CLI with non-existent data directory."""
    runner = CliRunner()
    result = runner.invoke(main, [
        '--data-dir', '/nonexistent/path',
        '--output', '/tmp/output'
    ])
    assert result.exit_code != 0
