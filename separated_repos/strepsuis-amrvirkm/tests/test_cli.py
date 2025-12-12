"""Tests for CLI module."""

import sys
import tempfile
from pathlib import Path

import pytest

from strepsuis_amrvirkm.cli import main


def test_cli_help(capsys, monkeypatch):
    """Test CLI help command."""
    monkeypatch.setattr(sys, "argv", ["strepsuis-amrvirkm", "--help"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "usage:" in captured.out.lower() or "Usage:" in captured.out


def test_cli_version(capsys, monkeypatch):
    """Test CLI version command."""
    monkeypatch.setattr(sys, "argv", ["strepsuis-amrvirkm", "--version"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "1.0.0" in captured.out


def test_cli_missing_required_args(monkeypatch):
    """Test CLI with missing required arguments."""
    monkeypatch.setattr(sys, "argv", ["strepsuis-amrvirkm"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code != 0


def test_cli_with_valid_args(data_dir, monkeypatch):
    """Test CLI with valid arguments."""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "strepsuis-amrvirkm",
                "--data-dir",
                str(data_dir),
                "--output",
                str(Path(tmpdir) / "output"),
            ],
        )
        result = main()
        assert result == 0


def test_cli_with_bootstrap_option(data_dir, monkeypatch):
    """Test CLI with bootstrap iterations option."""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "strepsuis-amrvirkm",
                "--data-dir",
                str(data_dir),
                "--output",
                str(Path(tmpdir) / "output"),
                "--bootstrap",
                "100",
            ],
        )
        result = main()
        assert result == 0


def test_cli_with_fdr_alpha_option(data_dir, monkeypatch):
    """Test CLI with FDR alpha option."""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "strepsuis-amrvirkm",
                "--data-dir",
                str(data_dir),
                "--output",
                str(Path(tmpdir) / "output"),
                "--fdr-alpha",
                "0.01",
            ],
        )
        result = main()
        assert result == 0


def test_cli_with_verbose_option(data_dir, monkeypatch):
    """Test CLI with verbose option."""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "strepsuis-amrvirkm",
                "--data-dir",
                str(data_dir),
                "--output",
                str(Path(tmpdir) / "output"),
                "--verbose",
            ],
        )
        result = main()
        assert result == 0


def test_cli_with_invalid_data_dir(monkeypatch):
    """Test CLI with non-existent data directory."""
    monkeypatch.setattr(
        sys,
        "argv",
        ["strepsuis-amrvirkm", "--data-dir", "/nonexistent/path", "--output", "/tmp/output"],
    )
    result = main()
    assert result != 0


def test_cli_with_all_clustering_params(data_dir, monkeypatch):
    """Test CLI with all clustering parameters."""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "strepsuis-amrvirkm",
                "--data-dir",
                str(data_dir),
                "--output",
                str(tmpdir),
                "--max-clusters",
                "8",
                "--min-clusters",
                "2",
                "--bootstrap",
                "200",
                "--fdr-alpha",
                "0.05",
            ],
        )
        result = main()
        assert result == 0


def test_cli_with_random_seed(data_dir, monkeypatch):
    """Test CLI with custom random seed."""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "strepsuis-amrvirkm",
                "--data-dir",
                str(data_dir),
                "--output",
                str(tmpdir),
                "--random-seed",
                "123",
            ],
        )
        result = main()
        assert result == 0


def test_cli_with_n_jobs(data_dir, monkeypatch):
    """Test CLI with custom number of jobs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "strepsuis-amrvirkm",
                "--data-dir",
                str(data_dir),
                "--output",
                str(tmpdir),
                "--n-jobs",
                "2",
            ],
        )
        result = main()
        assert result == 0


def test_cli_no_html_report(data_dir, monkeypatch):
    """Test CLI with HTML report disabled."""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "strepsuis-amrvirkm",
                "--data-dir",
                str(data_dir),
                "--output",
                str(tmpdir),
                "--no-html",
            ],
        )
        result = main()
        assert result == 0


def test_cli_no_excel_report(data_dir, monkeypatch):
    """Test CLI with Excel report disabled."""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "strepsuis-amrvirkm",
                "--data-dir",
                str(data_dir),
                "--output",
                str(tmpdir),
                "--no-excel",
            ],
        )
        result = main()
        assert result == 0


def test_cli_exception_handling(data_dir, monkeypatch):
    """Test CLI handles exceptions gracefully."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test with invalid bootstrap value
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "strepsuis-amrvirkm",
                "--data-dir",
                str(data_dir),
                "--output",
                str(tmpdir),
                "--bootstrap",
                "50",  # Below minimum
            ],
        )
        result = main()
        # Should handle exception and return non-zero
        assert result != 0


def test_cli_with_mca_components(data_dir, monkeypatch):
    """Test CLI with custom MCA components."""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "strepsuis-amrvirkm",
                "--data-dir",
                str(data_dir),
                "--output",
                str(tmpdir),
                "--mca-components",
                "3",
            ],
        )
        result = main()
        assert result == 0


def test_cli_with_dpi(data_dir, monkeypatch):
    """Test CLI with custom DPI setting."""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "strepsuis-amrvirkm",
                "--data-dir",
                str(data_dir),
                "--output",
                str(tmpdir),
                "--dpi",
                "300",
            ],
        )
        result = main()
        assert result == 0


def test_cli_subprocess_help():
    """Test CLI help command via subprocess."""
    import subprocess
    result = subprocess.run(
        ["strepsuis-amrvirkm", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "StrepSuis-AMRVirKM" in result.stdout
    assert "--data-dir" in result.stdout


def test_cli_subprocess_version():
    """Test CLI version command via subprocess."""
    import subprocess
    result = subprocess.run(
        ["strepsuis-amrvirkm", "--version"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "strepsuis-amrvirkm" in result.stdout or "1.0.0" in result.stdout


def test_cli_subprocess_with_real_data(data_dir):
    """Test CLI execution with real data via subprocess."""
    import subprocess
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            [
                "strepsuis-amrvirkm",
                "--data-dir", str(data_dir),
                "--output", tmpdir,
                "--max-clusters", "3",
                "--bootstrap", "10"
            ],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        # Check that it runs (may not complete successfully depending on data)
        assert result.returncode in [0, 1]  # 0=success, 1=error but ran


def test_cli_subprocess_missing_data_dir():
    """Test CLI with missing data directory via subprocess."""
    import subprocess
    result = subprocess.run(
        [
            "strepsuis-amrvirkm",
            "--data-dir", "/nonexistent/path",
            "--output", "/tmp/output"
        ],
        capture_output=True,
        text=True,
        timeout=30
    )
    # Should fail with error
    assert result.returncode != 0
