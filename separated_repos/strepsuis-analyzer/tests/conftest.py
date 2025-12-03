"""
Pytest configuration and fixtures for StrepSuisAnalyzer tests.
"""

import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_binary_data():
    """Create sample binary data for testing."""
    np.random.seed(42)
    data = pd.DataFrame(
        np.random.randint(0, 2, size=(50, 10)),
        columns=[f"gene_{i}" for i in range(10)],
        index=[f"strain_{i}" for i in range(50)],
    )
    return data


@pytest.fixture
def sample_amr_data():
    """Create sample AMR data for testing."""
    return pd.DataFrame({
        'Strain_ID': ['S1', 'S2', 'S3', 'S4', 'S5'],
        'tet(M)': [1, 1, 1, 0, 0],
        'erm(B)': [1, 0, 1, 1, 0],
        'aph(3\')': [0, 1, 0, 1, 0],
        'tet(O)': [0, 0, 1, 0, 0]
    })


@pytest.fixture
def sample_numeric_data():
    """Create sample numeric data for testing."""
    np.random.seed(42)
    data = pd.DataFrame(
        np.random.randn(50, 5) * 10 + 50,
        columns=[f"var_{i}" for i in range(5)],
        index=[f"sample_{i}" for i in range(50)],
    )
    return data


@pytest.fixture
def sample_categorical_data():
    """Create sample categorical data for testing."""
    np.random.seed(42)
    categories = ["A", "B", "C", "D"]
    data = pd.Series(
        np.random.choice(categories, size=100), name="category", index=[f"sample_{i}" for i in range(100)]
    )
    return data


@pytest.fixture
def sample_tree_newick():
    """Create sample Newick tree string."""
    return "((A:0.1,B:0.2):0.3,(C:0.15,D:0.25):0.35);"


@pytest.fixture
def sample_tree_newick_large():
    """Create larger sample Newick tree."""
    return "((((A:0.1,B:0.2):0.15,C:0.25):0.1,(D:0.3,E:0.2):0.2):0.1,(F:0.4,((G:0.1,H:0.15):0.2,I:0.3):0.1):0.2);"


@pytest.fixture
def correlation_data_perfect():
    """Create perfectly correlated data for testing."""
    np.random.seed(42)
    x = np.linspace(0, 10, 100)
    y = 2 * x + 1  # Perfect linear relationship
    return pd.DataFrame({"x": x, "y": y})


@pytest.fixture
def correlation_data_no_correlation():
    """Create uncorrelated data for testing."""
    np.random.seed(42)
    x = np.random.randn(100)
    y = np.random.randn(100)
    return pd.DataFrame({"x": x, "y": y})


@pytest.fixture
def normal_distribution_data():
    """Create normally distributed data."""
    np.random.seed(42)
    return pd.Series(np.random.normal(0, 1, 1000), name="normal")


@pytest.fixture
def non_normal_distribution_data():
    """Create non-normally distributed data."""
    np.random.seed(42)
    return pd.Series(np.random.exponential(1, 1000), name="exponential")


@pytest.fixture
def meta_analysis_data():
    """Create sample meta-analysis data."""
    effect_sizes = [0.5, 0.6, 0.4, 0.7, 0.55]
    variances = [0.01, 0.02, 0.015, 0.012, 0.018]
    return {"effect_sizes": effect_sizes, "variances": variances}
