#!/usr/bin/env python3
"""
Test script for Network Analysis implementation.
Tests the core functions without requiring data upload.
"""

import sys
import os
import pandas as pd
import numpy as np

# Mock google.colab module for testing
class MockFiles:
    def upload(self):
        return {}
    def download(self, filename):
        pass

class MockColab:
    files = MockFiles()

sys.modules['google'] = type(sys)('google')
sys.modules['google.colab'] = MockColab()

# Add parent directory to path to import from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import functions from src/network_analysis.py
from src.network_analysis import (
    expand_categories,
    chi2_phi,
    calculate_entropy,
    cramers_v,
    information_gain,
    normalized_mutual_info,
    find_mutually_exclusive,
    adaptive_phi_threshold,
    create_interactive_table,
    create_section_summary,
    summarize_by_category,
    summarize_by_feature,
    setup_logging
)

def test_expand_categories():
    """Test category expansion function"""
    print("Testing expand_categories...")
    df = pd.DataFrame({
        'Strain_ID': ['S1', 'S2', 'S3'],
        'MLST': ['1', '2', '1']
    })
    result = expand_categories(df, 'MLST')
    assert 'Strain_ID' in result.columns
    assert len(result.columns) > 1  # Should have binary columns
    print("  ✓ expand_categories passed")

def test_chi2_phi():
    """Test chi-square and phi coefficient calculation"""
    print("Testing chi2_phi...")
    x = pd.Series([0, 0, 1, 1, 0, 1, 1, 0])
    y = pd.Series([0, 1, 1, 1, 0, 1, 0, 0])
    p, phi, contingency, lo, hi = chi2_phi(x, y)
    assert 0 <= p <= 1, "p-value should be between 0 and 1"
    assert 0 <= phi <= 1, "Phi coefficient should be between 0 and 1"
    print(f"  ✓ chi2_phi passed (p={p:.4f}, phi={phi:.4f})")

def test_entropy():
    """Test entropy calculation"""
    print("Testing calculate_entropy...")
    series = pd.Series([0, 0, 1, 1, 1, 0])
    H, Hn = calculate_entropy(series)
    assert H >= 0, "Entropy should be non-negative"
    assert 0 <= Hn <= 1, "Normalized entropy should be between 0 and 1"
    print(f"  ✓ calculate_entropy passed (H={H:.4f}, Hn={Hn:.4f})")

def test_cramers_v():
    """Test Cramér's V calculation"""
    print("Testing cramers_v...")
    contingency = pd.DataFrame([[10, 5], [3, 8]])
    v, lo, hi = cramers_v(contingency)
    assert 0 <= v <= 1, "Cramér's V should be between 0 and 1"
    print(f"  ✓ cramers_v passed (V={v:.4f})")

def test_information_gain():
    """Test information gain calculation"""
    print("Testing information_gain...")
    x = pd.Series([0, 0, 1, 1, 1, 0, 0, 1])
    y = pd.Series([0, 1, 1, 1, 0, 0, 1, 0])
    ig = information_gain(x, y)
    assert ig >= 0, "Information gain should be non-negative"
    print(f"  ✓ information_gain passed (IG={ig:.4f})")

def test_normalized_mutual_info():
    """Test normalized mutual information"""
    print("Testing normalized_mutual_info...")
    x = pd.Series([0, 0, 1, 1, 1, 0])
    y = pd.Series([0, 1, 1, 1, 0, 0])
    nmi = normalized_mutual_info(x, y)
    assert 0 <= nmi <= 1, "NMI should be between 0 and 1"
    print(f"  ✓ normalized_mutual_info passed (NMI={nmi:.4f})")

def test_mutually_exclusive():
    """Test mutually exclusive pattern detection"""
    print("Testing find_mutually_exclusive...")
    
    # Test fixture: feature-category mapping
    TEST_FEATURE_MAPPING = {'feat1': 'cat1', 'feat2': 'cat2', 'feat3': 'cat3'}
    
    df = pd.DataFrame({
        'Strain_ID': ['S1', 'S2', 'S3', 'S4'],
        'feat1': [1, 0, 0, 0],
        'feat2': [0, 1, 0, 0],
        'feat3': [0, 0, 1, 1]
    })
    result = find_mutually_exclusive(df, ['feat1', 'feat2', 'feat3'], TEST_FEATURE_MAPPING, k=2, max_patterns=10)
    assert isinstance(result, pd.DataFrame)
    print(f"  ✓ find_mutually_exclusive passed (found {len(result)} patterns)")

def test_adaptive_threshold():
    """Test adaptive threshold selection"""
    print("Testing adaptive_phi_threshold...")
    phi_vals = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    threshold = adaptive_phi_threshold(phi_vals, method='percentile', percentile=90)
    assert 0 <= threshold <= 1, "Threshold should be between 0 and 1"
    print(f"  ✓ adaptive_phi_threshold passed (threshold={threshold:.4f})")

def test_reporting_functions():
    """Test reporting helper functions"""
    print("Testing reporting functions...")
    
    # Test create_interactive_table
    df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4.567, 5.678, 6.789]})
    html = create_interactive_table(df, 'test')
    assert '<table' in html
    assert 'col1' in html
    print("  ✓ create_interactive_table passed")
    
    # Test create_section_summary
    stats = {'stat1': 'value1', 'stat2': 'value2'}
    html = create_section_summary('Test Section', stats)
    assert 'Test Section' in html
    assert 'stat1' in html
    print("  ✓ create_section_summary passed")
    
    # Test summarize_by_category
    df = pd.DataFrame({
        'Category1': ['cat1', 'cat2', 'cat1'],
        'Category2': ['cat2', 'cat1', 'cat3'],
        'value': [0.5, 0.6, 0.7]
    })
    result = summarize_by_category(df, 'value', ['Category1', 'Category2'])
    assert isinstance(result, dict)
    print("  ✓ summarize_by_category passed")
    
    # Test summarize_by_feature
    df = pd.DataFrame({
        'Feature1': ['f1', 'f2', 'f1'],
        'Feature2': ['f2', 'f1', 'f3'],
        'value': [0.5, 0.6, 0.7]
    })
    result = summarize_by_feature(df, 'value', ['Feature1', 'Feature2'])
    assert isinstance(result, dict)
    print("  ✓ summarize_by_feature passed")

def test_logging_setup():
    """Test logging configuration"""
    print("Testing setup_logging...")
    setup_logging()
    assert os.path.exists('output'), "Output directory should be created"
    print("  ✓ setup_logging passed")

def main():
    """Run all tests"""
    print("="*80)
    print("Running Network Analysis Tests")
    print("="*80)
    
    tests = [
        test_expand_categories,
        test_chi2_phi,
        test_entropy,
        test_cramers_v,
        test_information_gain,
        test_normalized_mutual_info,
        test_mutually_exclusive,
        test_adaptive_threshold,
        test_reporting_functions,
        test_logging_setup
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} failed: {e}")
            failed += 1
    
    print("="*80)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*80)
    
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
