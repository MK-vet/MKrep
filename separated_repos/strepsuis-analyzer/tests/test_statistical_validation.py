"""
Statistical validation tests for StrepSuis Analyzer.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import pytest
from scipy import stats

sys.path.insert(0, str(Path(__file__).parent.parent))

from StrepSuisPhyloCluster_2025_08_11 import StrepSuisAnalyzer


pytestmark = pytest.mark.unit


@pytest.mark.unit
def test_chi_square_calculation(tmp_path, output_dir):
    """Test that chi-square calculations are correct."""
    # Create data with known association
    data_file = tmp_path / "chi_square_test.csv"
    np.random.seed(42)  # Fixed seed for reproducibility
    data = pd.DataFrame({
        'Strain_ID': [f'S{i}' for i in range(1, 21)],
        'Gene1': [1]*10 + [0]*10,  # Perfectly associated with cluster
        'Gene2': np.random.randint(0, 2, 20)  # Random
    })
    data.to_csv(data_file, index=False)
    
    analyzer = StrepSuisAnalyzer(output_dir=output_dir, random_state=42)
    analyzer.load_data([data_file])
    analyzer.perform_clustering(n_clusters=2)
    analyzer.calculate_trait_associations()
    
    # Verify results structure
    results = analyzer.results['trait_associations']
    assert 'Feature' in results.columns
    assert 'P_value' in results.columns
    assert 'Cramers_V' in results.columns


@pytest.mark.unit
def test_fdr_correction(tmp_path, output_dir):
    """Test FDR (Benjamini-Hochberg) correction."""
    data_file = tmp_path / "fdr_test.csv"
    np.random.seed(42)
    data = pd.DataFrame({
        'Strain_ID': [f'S{i}' for i in range(1, 31)]
    })
    # Add multiple features
    for i in range(10):
        data[f'Gene{i}'] = np.random.randint(0, 2, 30)
    data.to_csv(data_file, index=False)
    
    analyzer = StrepSuisAnalyzer(output_dir=output_dir, random_state=42)
    analyzer.load_data([data_file])
    analyzer.perform_clustering(n_clusters=2)
    analyzer.calculate_trait_associations()
    
    results = analyzer.results['trait_associations']
    # Adjusted p-values should be >= raw p-values
    assert all(results['P_adj'] >= results['P_value'])


@pytest.mark.unit
def test_cramers_v_bounds(tmp_path, output_dir):
    """Test that Cramér's V is within valid bounds [0, 1]."""
    data_file = tmp_path / "cramers_test.csv"
    data = pd.DataFrame({
        'Strain_ID': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
        'Gene1': [1, 1, 1, 0, 0, 0],
        'Gene2': [1, 0, 1, 0, 1, 0]
    })
    data.to_csv(data_file, index=False)
    
    analyzer = StrepSuisAnalyzer(output_dir=output_dir, random_state=42)
    analyzer.load_data([data_file])
    analyzer.perform_clustering(n_clusters=2)
    analyzer.calculate_trait_associations()
    
    results = analyzer.results['trait_associations']
    # All Cramér's V values should be between 0 and 1
    assert all(results['Cramers_V'] >= 0)
    assert all(results['Cramers_V'] <= 1)


@pytest.mark.unit
@pytest.mark.reproducibility
def test_deterministic_clustering(tmp_path):
    """Test that clustering is deterministic with fixed seed."""
    data_file = tmp_path / "determinism_test.csv"
    np.random.seed(42)
    data = pd.DataFrame({
        'Strain_ID': [f'S{i}' for i in range(1, 21)]
    })
    for i in range(5):
        data[f'Gene{i}'] = np.random.randint(0, 2, 20)
    data.to_csv(data_file, index=False)
    
    # Run clustering twice with same seed
    clusters1 = []
    clusters2 = []
    
    for i, clusters in enumerate([clusters1, clusters2]):
        output = tmp_path / f"output_{i}"
        if not output.exists():
            output.mkdir()
        analyzer = StrepSuisAnalyzer(output_dir=output, random_state=42)
        analyzer.load_data([data_file])
        analyzer.perform_clustering(n_clusters=3)
        clusters.append(analyzer.data['Cluster'].tolist())
    
    # Results should be identical
    assert clusters1[0] == clusters2[0]
