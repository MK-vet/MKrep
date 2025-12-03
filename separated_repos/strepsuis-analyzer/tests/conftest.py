"""
Pytest configuration and fixtures for StrepSuis Analyzer tests.
"""

import shutil
from pathlib import Path
import pandas as pd
import numpy as np
import pytest


@pytest.fixture
def data_dir(tmp_path):
    """Create a temporary data directory with example files."""
    data = tmp_path / "data"
    data.mkdir()
    
    # Copy example data files if they exist
    example_dir = Path(__file__).parent.parent / "data"
    if example_dir.exists():
        for csv_file in example_dir.glob("*.csv"):
            shutil.copy(csv_file, data)
    
    return data


@pytest.fixture
def output_dir(tmp_path):
    """Create a temporary output directory."""
    output = tmp_path / "output"
    output.mkdir()
    return output


@pytest.fixture
def sample_csv_data():
    """Provide sample CSV data as string."""
    return """Strain_ID,Feature1,Feature2,Feature3
Strain001,1,0,1
Strain002,0,1,1
Strain003,1,1,0
Strain004,0,0,1
Strain005,1,1,1"""


@pytest.fixture
def sample_binary_data():
    """Create sample binary trait data for testing."""
    np.random.seed(42)
    n_strains = 20
    n_features = 10
    
    data = pd.DataFrame({
        'Strain_ID': [f'Strain{i:03d}' for i in range(1, n_strains + 1)]
    })
    
    # Add binary features
    for i in range(n_features):
        data[f'Feature{i+1}'] = np.random.randint(0, 2, n_strains)
    
    return data


@pytest.fixture
def sample_tree_newick():
    """Provide a sample Newick tree string."""
    return "((Strain001:0.1,Strain002:0.15):0.2,(Strain003:0.12,Strain004:0.18):0.25,Strain005:0.1);"


@pytest.fixture
def mini_dataset(tmp_path):
    """Create a minimal dataset for fast testing."""
    data_file = tmp_path / "mini_data.csv"
    data = pd.DataFrame({
        'Strain_ID': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
        'Gene1': [1, 1, 1, 0, 0, 0],
        'Gene2': [1, 1, 0, 0, 0, 1],
        'Gene3': [0, 1, 1, 1, 0, 0]
    })
    data.to_csv(data_file, index=False)
    return data_file
