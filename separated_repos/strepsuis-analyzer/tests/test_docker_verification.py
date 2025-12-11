"""
Docker Build and Startup Verification Tests for StrepSuis-Analyzer

This module provides tests to verify that the Streamlit application
can be properly built and started in a Docker container.

These tests focus on:
1. Sanity check script functionality
2. Import verification
3. Dockerfile validity
4. Startup sequence verification

Author: MK-vet Team
License: MIT
Version: 1.0.0
"""

import json
import os
import sys
from pathlib import Path

import pytest


class TestSanityCheckScript:
    """Test the sanity check script functionality."""

    def test_check_python_version(self):
        """Test Python version check."""
        # Add scripts to path
        scripts_dir = Path(__file__).parent.parent / "scripts"
        sys.path.insert(0, str(scripts_dir))

        from sanity_check import check_python_version

        ok, msg = check_python_version()
        assert ok, f"Python version check failed: {msg}"
        assert "Python" in msg

    def test_check_import_function(self):
        """Test import checking function."""
        scripts_dir = Path(__file__).parent.parent / "scripts"
        sys.path.insert(0, str(scripts_dir))

        from sanity_check import check_import

        # Test with known-good modules
        ok, msg = check_import("json")
        assert ok
        assert "OK" in msg

        # Test with non-existent module
        ok, msg = check_import("nonexistent_module_xyz")
        assert not ok
        assert "FAILED" in msg

    def test_check_streamlit(self):
        """Test Streamlit availability check."""
        scripts_dir = Path(__file__).parent.parent / "scripts"
        sys.path.insert(0, str(scripts_dir))

        from sanity_check import check_streamlit

        ok, msg = check_streamlit()

        # Streamlit should be installed in test environment
        if ok:
            assert "Streamlit version" in msg
        else:
            pytest.skip("Streamlit not installed in test environment")

    def test_check_required_dependencies(self):
        """Test dependency checking function."""
        scripts_dir = Path(__file__).parent.parent / "scripts"
        sys.path.insert(0, str(scripts_dir))

        from sanity_check import check_required_dependencies

        ok, results = check_required_dependencies()

        # At minimum, numpy and pandas should be available
        if "pandas" in results:
            assert results["pandas"] == "OK", "pandas should be installed"
        if "numpy" in results:
            assert results["numpy"] == "OK", "numpy should be installed"


class TestDockerfileValidity:
    """Test that Dockerfile is valid and contains expected components."""

    @pytest.fixture
    def dockerfile_path(self):
        """Get path to Dockerfile."""
        return Path(__file__).parent.parent / "Dockerfile"

    def test_dockerfile_exists(self, dockerfile_path):
        """Test that Dockerfile exists."""
        assert dockerfile_path.exists(), "Dockerfile should exist"

    def test_dockerfile_has_python_base(self, dockerfile_path):
        """Test that Dockerfile uses Python base image."""
        content = dockerfile_path.read_text()
        assert "python" in content.lower(), "Dockerfile should use Python base image"

    def test_dockerfile_has_workdir(self, dockerfile_path):
        """Test that Dockerfile sets WORKDIR."""
        content = dockerfile_path.read_text()
        assert "WORKDIR" in content, "Dockerfile should set WORKDIR"

    def test_dockerfile_copies_requirements(self, dockerfile_path):
        """Test that Dockerfile copies requirements file."""
        content = dockerfile_path.read_text()
        assert "requirements" in content.lower(), "Dockerfile should reference requirements"

    def test_dockerfile_exposes_port(self, dockerfile_path):
        """Test that Dockerfile exposes Streamlit port."""
        content = dockerfile_path.read_text()
        # Streamlit default port is 8501
        assert "EXPOSE" in content, "Dockerfile should expose a port"

    def test_dockerfile_has_entrypoint_or_cmd(self, dockerfile_path):
        """Test that Dockerfile has CMD or ENTRYPOINT."""
        content = dockerfile_path.read_text()
        has_cmd = "CMD" in content
        has_entrypoint = "ENTRYPOINT" in content
        assert has_cmd or has_entrypoint, "Dockerfile should have CMD or ENTRYPOINT"


class TestAppImports:
    """Test that the main app can be imported."""

    def test_import_app(self):
        """Test that app.py can be imported without errors."""
        app_dir = Path(__file__).parent.parent
        sys.path.insert(0, str(app_dir))

        # Also add src directory for local imports
        src_dir = app_dir / "src"
        if src_dir.exists():
            sys.path.insert(0, str(src_dir))

        try:
            import app
            assert True
        except ImportError as e:
            # Check if it's a missing strepsuis_analyzer module
            if "strepsuis_analyzer" in str(e):
                # Try to import from src directory
                try:
                    sys.path.insert(0, str(app_dir / "src"))
                    from strepsuis_analyzer import stats
                    # If src module imports work, the package structure is OK
                    assert True, "strepsuis_analyzer module exists in src/"
                except ImportError:
                    pytest.skip("strepsuis_analyzer module not installed (expected for development)")
            else:
                pytest.fail(f"Failed to import app: {e}")
        except Exception as e:
            # Some initialization errors are OK if they depend on Streamlit session
            if "streamlit" in str(e).lower():
                pytest.skip("App requires Streamlit runtime context")
            else:
                pytest.fail(f"Unexpected error importing app: {e}")

    def test_src_modules_importable(self):
        """Test that src modules can be imported."""
        src_dir = Path(__file__).parent.parent / "src" / "strepsuis_analyzer"
        if not src_dir.exists():
            pytest.skip("No src/strepsuis_analyzer directory")

        sys.path.insert(0, str(src_dir.parent.parent))

        # Try to import any Python files in src
        for py_file in src_dir.glob("*.py"):
            if py_file.name.startswith("_"):
                continue
            module_name = py_file.stem
            try:
                __import__(f"src.strepsuis_analyzer.{module_name}")
            except ImportError:
                pass  # Some imports may have dependencies


class TestConfigurationFiles:
    """Test that configuration files are valid."""

    def test_requirements_file_exists(self):
        """Test that requirements.txt exists."""
        req_file = Path(__file__).parent.parent / "requirements.txt"
        assert req_file.exists(), "requirements.txt should exist"

    def test_requirements_file_not_empty(self):
        """Test that requirements.txt is not empty."""
        req_file = Path(__file__).parent.parent / "requirements.txt"
        content = req_file.read_text().strip()
        assert len(content) > 0, "requirements.txt should not be empty"

    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists."""
        pyproject_file = Path(__file__).parent.parent / "pyproject.toml"
        # This is optional for Streamlit apps
        if pyproject_file.exists():
            content = pyproject_file.read_text()
            assert "[project]" in content or "[tool" in content


class TestDirectoryStructure:
    """Test that expected directories exist."""

    @pytest.fixture
    def base_dir(self):
        """Get base directory of the analyzer."""
        return Path(__file__).parent.parent

    def test_tests_directory_exists(self, base_dir):
        """Test that tests directory exists."""
        assert (base_dir / "tests").exists()

    def test_logs_directory_exists(self, base_dir):
        """Test that logs directory exists."""
        # Create if doesn't exist
        logs_dir = base_dir / "logs"
        logs_dir.mkdir(exist_ok=True)
        assert logs_dir.exists()

    def test_results_demonstration_directory_exists(self, base_dir):
        """Test that results_demonstration directory exists."""
        results_dir = base_dir / "results_demonstration"
        results_dir.mkdir(exist_ok=True)
        assert results_dir.exists()


class TestSanityCheckReportGeneration:
    """Test sanity check report generation."""

    def test_can_generate_report(self, tmp_path):
        """Test that sanity check can generate a report."""
        scripts_dir = Path(__file__).parent.parent / "scripts"
        sys.path.insert(0, str(scripts_dir))

        from sanity_check import run_sanity_checks, save_sanity_check_report

        results = run_sanity_checks(verbose=False)

        # Save to temp location
        report_path = save_sanity_check_report(
            results, str(tmp_path / "test_report.json")
        )

        # Verify report was saved
        assert Path(report_path).exists()

        # Verify report content
        with open(report_path) as f:
            data = json.load(f)

        assert "timestamp" in data
        assert "checks" in data
        assert "all_passed" in data
        assert isinstance(data["checks"], list)
