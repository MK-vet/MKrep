"""
Integration tests for StrepSuis Analyzer complete workflows.
"""

import sys
from pathlib import Path
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from StrepSuisPhyloCluster_2025_08_11 import StrepSuisAnalyzer


pytestmark = pytest.mark.integration


@pytest.mark.integration
def test_full_workflow_mini_data(mini_dataset, output_dir):
    """Test complete analysis workflow with mini dataset."""
    # Initialize analyzer
    analyzer = StrepSuisAnalyzer(output_dir=output_dir, random_state=42)
    
    # Load data
    analyzer.load_data([mini_dataset])
    assert analyzer.data is not None
    assert len(analyzer.data) == 6
    
    # Perform clustering
    analyzer.perform_clustering(n_clusters=2)
    assert 'Cluster' in analyzer.data.columns
    assert analyzer.data['Cluster'].nunique() == 2
    
    # Calculate associations
    analyzer.calculate_trait_associations()
    assert 'trait_associations' in analyzer.results
    
    # Generate outputs
    analyzer.save_csv_outputs()
    assert (output_dir / 'clustered_data.csv').exists()
    assert (output_dir / 'trait_associations.csv').exists()


@pytest.mark.integration
def test_excel_report_generation(mini_dataset, output_dir):
    """Test Excel report generation."""
    analyzer = StrepSuisAnalyzer(output_dir=output_dir, random_state=42)
    analyzer.load_data([mini_dataset])
    analyzer.perform_clustering(n_clusters=2)
    analyzer.calculate_trait_associations()
    analyzer.generate_excel_report()
    
    excel_path = output_dir / 'analysis_results.xlsx'
    assert excel_path.exists()
    
    # Verify sheets
    excel_data = pd.ExcelFile(excel_path)
    assert 'Clustered_Data' in excel_data.sheet_names
    assert 'Cluster_Summary' in excel_data.sheet_names


@pytest.mark.integration
def test_html_report_generation(mini_dataset, output_dir):
    """Test HTML report generation."""
    analyzer = StrepSuisAnalyzer(output_dir=output_dir, random_state=42)
    analyzer.load_data([mini_dataset])
    analyzer.perform_clustering(n_clusters=2)
    analyzer.calculate_trait_associations()
    analyzer.perform_mca()
    analyzer.generate_html_report()
    
    html_path = output_dir / 'analysis_report.html'
    assert html_path.exists()
    
    # Verify HTML content
    with open(html_path, 'r') as f:
        content = f.read()
        assert 'StrepSuis' in content
        assert 'Cluster' in content


@pytest.mark.integration
@pytest.mark.reproducibility
def test_reproducibility(mini_dataset, tmp_path):
    """Test that results are reproducible with fixed seed."""
    # Run analysis twice with same seed
    results1 = []
    results2 = []
    
    for i, results in enumerate([results1, results2]):
        output = tmp_path / f"run{i}"
        output.mkdir()
        analyzer = StrepSuisAnalyzer(output_dir=output, random_state=42)
        analyzer.load_data([mini_dataset])
        analyzer.perform_clustering(n_clusters=2)
        results.append(analyzer.data['Cluster'].tolist())
    
    # Results should be identical
    assert results1[0] == results2[0]
