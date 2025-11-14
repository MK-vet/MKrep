"""
Pytest configuration and fixtures.
"""

import pytest
from pathlib import Path


@pytest.fixture
def data_dir(tmp_path):
    """Create a temporary data directory."""
    data = tmp_path / "data"
    data.mkdir()
    return data


@pytest.fixture
def output_dir(tmp_path):
    """Create a temporary output directory."""
    output = tmp_path / "output"
    output.mkdir()
    return output


@pytest.fixture
def sample_csv_data():
    """Provide sample CSV data."""
    return """Strain_ID,Feature1,Feature2,Feature3
Strain001,1,0,1
Strain002,0,1,1
Strain003,1,1,0
Strain004,0,0,1
Strain005,1,1,1"""
