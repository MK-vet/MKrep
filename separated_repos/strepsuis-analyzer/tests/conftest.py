"""
Test configuration and fixtures for strepsuis-analyzer tests.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path


@pytest.fixture
def data_dir():
    """Return path to data directory."""
    return Path(__file__).parent.parent / "data"


@pytest.fixture
def sample_amr_data():
    """Create sample AMR gene data for testing."""
    return pd.DataFrame({
        'Strain_ID': ['S001', 'S002', 'S003', 'S004', 'S005'],
        'tet(M)': [1, 1, 0, 1, 0],
        'erm(B)': [0, 1, 1, 1, 0],
        'aph(3\')': [1, 0, 0, 0, 1],
        'tet(O)': [1, 1, 1, 0, 0]
    })


@pytest.fixture
def sample_virulence_data():
    """Create sample virulence data for testing."""
    return pd.DataFrame({
        'Strain_ID': ['S001', 'S002', 'S003', 'S004', 'S005'],
        'MRP': [1, 1, 1, 0, 0],
        'EF': [1, 0, 1, 1, 1],
        'Sly': [0, 1, 1, 1, 0],
        'CPS': [1, 1, 0, 0, 1]
    })


@pytest.fixture
def sample_mic_data():
    """Create sample MIC data for testing."""
    return pd.DataFrame({
        'Strain_ID': ['S001', 'S002', 'S003', 'S004', 'S005'],
        'Penicillin': [0, 0, 1, 1, 0],
        'Tetracycline': [1, 1, 1, 0, 0],
        'Erythromycin': [0, 1, 1, 1, 0],
        'Gentamicin': [1, 0, 0, 0, 1]
    })


@pytest.fixture
def sample_mlst_data():
    """Create sample MLST data for testing."""
    return pd.DataFrame({
        'Strain_ID': ['S001', 'S002', 'S003', 'S004', 'S005'],
        'MLST': [1, 1, 28, 28, 94]
    })


@pytest.fixture
def sample_serotype_data():
    """Create sample serotype data for testing."""
    return pd.DataFrame({
        'Strain_ID': ['S001', 'S002', 'S003', 'S004', 'S005'],
        'Serotype': [2, 2, 7, 9, 9]
    })


@pytest.fixture
def binary_matrix_small():
    """Create a small binary matrix for testing."""
    return np.array([
        [1, 0, 1, 0],
        [1, 1, 0, 0],
        [0, 1, 1, 1]
    ])


@pytest.fixture
def binary_matrix_identical():
    """Create a matrix with identical rows for testing."""
    return np.array([
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 1, 0, 0]
    ])


@pytest.fixture
def binary_matrix_zeros():
    """Create a matrix of all zeros for testing."""
    return np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])


@pytest.fixture
def binary_matrix_ones():
    """Create a matrix of all ones for testing."""
    return np.array([
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1]
    ])


@pytest.fixture
def sample_newick_tree():
    """Create a sample Newick tree string."""
    return "((A:0.1,B:0.2):0.3,(C:0.4,D:0.5):0.6);"
