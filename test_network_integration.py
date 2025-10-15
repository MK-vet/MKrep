#!/usr/bin/env python3
"""
Integration test for Network Analysis reporting system.
Creates mock data to test the full reporting pipeline.
"""

import sys
import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Mock google.colab module for testing
class MockFiles:
    def upload(self):
        return {}
    def download(self, filename):
        print(f"  Mock download: {filename}")

class MockColab:
    files = MockFiles()

sys.modules['google'] = type(sys)('google')
sys.modules['google.colab'] = MockColab()

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Network_Analysis_2025_06_26 import (
    generate_report_with_cluster_stats,
    generate_excel_report_with_cluster_stats,
    setup_logging
)

def create_mock_data():
    """Create mock data for testing"""
    print("Creating mock data...")
    
    # Chi-square results
    chi2_df = pd.DataFrame({
        'Feature1': ['feat1', 'feat2', 'feat3'] * 3,
        'Category1': ['cat1', 'cat2', 'cat3'] * 3,
        'Feature2': ['feat4', 'feat5', 'feat6'] * 3,
        'Category2': ['cat4', 'cat5', 'cat6'] * 3,
        'P_value': np.random.rand(9) * 0.1,
        'Phi_coefficient': np.random.rand(9) * 0.5 + 0.3,
        'CI_Lower': np.random.rand(9) * 0.3,
        'CI_Upper': np.random.rand(9) * 0.5 + 0.5,
        'Significant': [True, True, False, True, False, True, True, False, True],
        'P_adjusted': np.random.rand(9) * 0.1
    })
    
    # Network results
    network_df = pd.DataFrame({
        'Feature': ['feat1', 'feat2', 'feat3', 'feat4', 'feat5'],
        'Category': ['cat1', 'cat2', 'cat3', 'cat1', 'cat2'],
        'Cluster': [1, 1, 2, 2, 3],
        'Degree_Centrality': np.random.rand(5) * 0.5 + 0.3,
        'Betweenness_Centrality': np.random.rand(5) * 0.5,
        'Closeness_Centrality': np.random.rand(5) * 0.5 + 0.4,
        'Eigenvector_Centrality': np.random.rand(5) * 0.5 + 0.2
    })
    
    # Entropy results
    entropy_df = pd.DataFrame({
        'Feature1': ['feat1', 'feat2'] * 2,
        'Category1': ['cat1', 'cat2'] * 2,
        'Feature2': ['feat3', 'feat4'] * 2,
        'Category2': ['cat3', 'cat4'] * 2,
        'Entropy': np.random.rand(4) * 2,
        'Entropy_Normalized': np.random.rand(4),
        'Conditional_Entropy': np.random.rand(4) * 1.5,
        'Information_Gain': np.random.rand(4) * 0.5,
        'Normalized_Mutual_Information': np.random.rand(4) * 0.5,
        'Significant': [True, False, True, True],
        'P_adjusted': np.random.rand(4) * 0.1
    })
    
    # Cramér's V results
    cramers_df = pd.DataFrame({
        'Feature1': ['feat1', 'feat2', 'feat3'],
        'Category1': ['cat1', 'cat2', 'cat3'],
        'Feature2': ['feat4', 'feat5', 'feat6'],
        'Category2': ['cat4', 'cat5', 'cat6'],
        'Cramers_V': np.random.rand(3) * 0.5 + 0.2,
        'CI_Lower': np.random.rand(3) * 0.3,
        'CI_Upper': np.random.rand(3) * 0.5 + 0.5,
        'Significant': [True, True, False],
        'P_adjusted': np.random.rand(3) * 0.1
    })
    
    # Feature summary
    feature_summary_df = pd.DataFrame({
        'Category': ['MIC', 'AMR_genes', 'Virulence', 'MGE', 'MLST'],
        'Number_of_Features': [10, 15, 8, 5, 12]
    })
    
    # Mutually exclusive pairs
    excl2_df = pd.DataFrame({
        'Feature_1': ['feat1', 'feat2'],
        'Category_1': ['cat1', 'cat2'],
        'Feature_2': ['feat3', 'feat4'],
        'Category_2': ['cat3', 'cat4']
    })
    
    # Mutually exclusive triplets
    excl3_df = pd.DataFrame({
        'Feature_1': ['feat1'],
        'Category_1': ['cat1'],
        'Feature_2': ['feat2'],
        'Category_2': ['cat2'],
        'Feature_3': ['feat3'],
        'Category_3': ['cat3']
    })
    
    # Hubs
    hubs_df = pd.DataFrame({
        'Cluster': [1, 1, 2],
        'Feature': ['feat1', 'feat2', 'feat3'],
        'Category': ['cat1', 'cat2', 'cat3'],
        'Degree_Centrality': [0.8, 0.7, 0.75]
    })
    
    # Summaries
    chi2_summary = {
        "Total pairs": len(chi2_df),
        "Significant (FDR)": int(chi2_df['Significant'].sum()),
        "Phi mean": 0.456,
        "Phi min/max": "0.300 / 0.800"
    }
    
    entropy_summary = {
        "Pairs analyzed": len(entropy_df),
        "Significant (FDR)": int(entropy_df['Significant'].sum()),
        "IG mean": 0.234,
        "NMI mean": 0.345
    }
    
    cramers_summary = {
        "Pairs analyzed": len(cramers_df),
        "Significant (FDR)": int(cramers_df['Significant'].sum()),
        "V mean": 0.456,
        "V min/max": "0.200 / 0.700"
    }
    
    excl2_summary = {"Number of mutually exclusive pairs": len(excl2_df)}
    excl3_summary = {"Number of mutually exclusive triplets": len(excl3_df)}
    
    network_summary = {
        "Edges (significant)": 10,
        "Nodes": 5,
        "Clusters": 3,
        "Max cluster size": 2,
        "Min cluster size": 1
    }
    
    hubs_summary = {
        "Total hubs (top 3/cluster)": len(hubs_df),
        "Clusters": 3
    }
    
    # Category and feature summaries
    chi2_cat = {"cat1": "Count: 3, mean: 0.456, min/max: 0.3/0.8"}
    chi2_feat = {"feat1": "Count: 3, mean: 0.456, min/max: 0.3/0.8"}
    
    entropy_cat = {"cat1": "Count: 2, mean: 0.234, min/max: 0.1/0.4"}
    entropy_feat = {"feat1": "Count: 2, mean: 0.234, min/max: 0.1/0.4"}
    
    cramers_cat = {"cat1": "Count: 1, mean: 0.456, min/max: 0.2/0.7"}
    cramers_feat = {"feat1": "Count: 1, mean: 0.456, min/max: 0.2/0.7"}
    
    excl2_cat = {"cat1": "Count: 1"}
    excl2_feat = {"feat1": "Count: 1"}
    
    excl3_cat = {"cat1": "Count: 1"}
    excl3_feat = {"feat1": "Count: 1"}
    
    network_cat = {"cat1": "Count: 2, mean degree: 0.678, min/max degree: 0.5/0.8"}
    network_feat = {"feat1": "degree: 0.678"}
    
    return (
        chi2_df, network_df, entropy_df, cramers_df, feature_summary_df,
        excl2_df, excl3_df, hubs_df,
        chi2_summary, entropy_summary, cramers_summary, excl2_summary,
        excl3_summary, network_summary, hubs_summary,
        chi2_cat, chi2_feat, entropy_cat, entropy_feat, cramers_cat,
        cramers_feat, excl2_cat, excl2_feat, excl3_cat, excl3_feat,
        network_cat, network_feat
    )

def test_html_report():
    """Test HTML report generation"""
    print("\n" + "="*80)
    print("Testing HTML Report Generation")
    print("="*80)
    
    (chi2_df, network_df, entropy_df, cramers_df, feature_summary_df,
     excl2_df, excl3_df, hubs_df,
     chi2_summary, entropy_summary, cramers_summary, excl2_summary,
     excl3_summary, network_summary, hubs_summary,
     chi2_cat, chi2_feat, entropy_cat, entropy_feat, cramers_cat,
     cramers_feat, excl2_cat, excl2_feat, excl3_cat, excl3_feat,
     network_cat, network_feat) = create_mock_data()
    
    network_html = '<div>Mock network visualization</div>'
    
    html_report = generate_report_with_cluster_stats(
        chi2_df, network_df, entropy_df, cramers_df, feature_summary_df,
        excl2_df, excl3_df, hubs_df, network_html,
        chi2_summary, entropy_summary, cramers_summary, excl2_summary,
        excl3_summary, network_summary, hubs_summary,
        chi2_cat, chi2_feat, entropy_cat, entropy_feat, cramers_cat,
        cramers_feat, excl2_cat, excl2_feat, excl3_cat, excl3_feat,
        network_cat, network_feat
    )
    
    # Save report
    with open('test_report.html', 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    print("✓ HTML report generated successfully")
    print(f"  File size: {len(html_report)} bytes")
    print(f"  Saved to: test_report.html")
    
    # Verify content
    assert '<!DOCTYPE html>' in html_report
    assert 'Chi-square' in html_report
    assert 'Network Analysis' in html_report
    assert 'data-table' in html_report or 'DataTable' in html_report
    print("✓ HTML report contains expected content")
    
    return True

def test_excel_report():
    """Test Excel report generation"""
    print("\n" + "="*80)
    print("Testing Excel Report Generation")
    print("="*80)
    
    setup_logging()
    
    (chi2_df, network_df, entropy_df, cramers_df, feature_summary_df,
     excl2_df, excl3_df, hubs_df,
     chi2_summary, entropy_summary, cramers_summary, excl2_summary,
     excl3_summary, network_summary, hubs_summary,
     chi2_cat, chi2_feat, entropy_cat, entropy_feat, cramers_cat,
     cramers_feat, excl2_cat, excl2_feat, excl3_cat, excl3_feat,
     network_cat, network_feat) = create_mock_data()
    
    excel_path = generate_excel_report_with_cluster_stats(
        chi2_df, network_df, entropy_df, cramers_df, feature_summary_df,
        excl2_df, excl3_df, hubs_df, None,  # No figure for now
        chi2_summary, entropy_summary, cramers_summary, excl2_summary,
        excl3_summary, network_summary, hubs_summary,
        chi2_cat, chi2_feat, entropy_cat, entropy_feat, cramers_cat,
        cramers_feat, excl2_cat, excl2_feat, excl3_cat, excl3_feat,
        network_cat, network_feat
    )
    
    print(f"✓ Excel report generated successfully")
    print(f"  Saved to: {excel_path}")
    
    # Verify file exists
    assert os.path.exists(excel_path)
    file_size = os.path.getsize(excel_path)
    print(f"  File size: {file_size} bytes")
    print("✓ Excel file exists and has content")
    
    # Check for png_charts directory
    png_dir = os.path.join('output', 'png_charts')
    assert os.path.exists(png_dir)
    print(f"✓ PNG charts directory exists: {png_dir}")
    
    return True

def main():
    """Run integration tests"""
    print("="*80)
    print("Network Analysis Integration Tests")
    print("="*80)
    
    try:
        test_html_report()
        test_excel_report()
        
        print("\n" + "="*80)
        print("ALL INTEGRATION TESTS PASSED!")
        print("="*80)
        print("\nGenerated files:")
        print("  - test_report.html")
        print("  - output/Network_Analysis_Report_*.xlsx")
        print("  - output/png_charts/ (directory)")
        print("  - output/network_analysis_log.txt")
        print("="*80)
        
        return 0
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
