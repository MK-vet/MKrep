#!/usr/bin/env python
"""
Verification script for strepsuis-analyzer module.
This script verifies that all components are working correctly.
"""
import sys
import os

def verify_structure():
    """Verify directory structure."""
    print("=== Verifying Directory Structure ===")
    required_dirs = ['data', 'tests']
    required_files = [
        'app.py',
        'utils.py',
        'requirements.txt',
        'README.md',
        'DOCUMENTATION.md',
        '.gitignore',
        '.coveragerc'
    ]
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✓ Directory '{dir_name}' exists")
        else:
            print(f"✗ Directory '{dir_name}' missing")
            return False
    
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✓ File '{file_name}' exists")
        else:
            print(f"✗ File '{file_name}' missing")
            return False
    
    return True

def verify_data_files():
    """Verify data files."""
    print("\n=== Verifying Data Files ===")
    data_files = [
        'data/AMR_genes.csv',
        'data/MGE.csv',
        'data/MIC.csv',
        'data/MLST.csv',
        'data/Plasmid.csv',
        'data/Serotype.csv',
        'data/Virulence.csv',
        'data/Snp_tree.newick'
    ]
    
    for file_path in data_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✓ {file_path} ({size} bytes)")
        else:
            print(f"✗ {file_path} missing")
            return False
    
    return True

def verify_tests():
    """Verify test files."""
    print("\n=== Verifying Test Files ===")
    test_files = [
        'tests/__init__.py',
        'tests/conftest.py',
        'tests/test_app.py',
        'tests/test_statistics.py',
        'tests/test_utils.py'
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            return False
    
    return True

def verify_imports():
    """Verify that utils module can be imported."""
    print("\n=== Verifying Module Imports ===")
    try:
        import utils
        print("✓ utils module imported successfully")
        
        # Check key functions
        functions = [
            'fix_dataframe_for_streamlit',
            'DataValidator',
            'load_reference_data',
            'calculate_correlation',
            'calculate_descriptive_stats',
            'perform_ttest',
            'perform_anova',
            'validate_newick_tree'
        ]
        
        for func_name in functions:
            if hasattr(utils, func_name):
                print(f"✓ Function '{func_name}' available")
            else:
                print(f"✗ Function '{func_name}' missing")
                return False
        
        return True
    except ImportError as e:
        print(f"✗ Failed to import utils: {e}")
        return False

def verify_data_loading():
    """Verify data can be loaded."""
    print("\n=== Verifying Data Loading ===")
    try:
        from utils import load_reference_data
        data = load_reference_data()
        
        expected_datasets = ['AMR_genes', 'MGE', 'MIC', 'MLST', 'Plasmid', 'Serotype', 'Virulence']
        
        for dataset_name in expected_datasets:
            if dataset_name in data and data[dataset_name] is not None:
                df = data[dataset_name]
                print(f"✓ {dataset_name}: {df.shape[0]} rows, {df.shape[1]} columns")
            else:
                print(f"✗ {dataset_name}: Failed to load")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Data loading failed: {e}")
        return False

def main():
    """Run all verifications."""
    print("Strepsuis Analyzer Module Verification")
    print("=" * 50)
    
    checks = [
        ("Directory Structure", verify_structure),
        ("Data Files", verify_data_files),
        ("Test Files", verify_tests),
        ("Module Imports", verify_imports),
        ("Data Loading", verify_data_loading)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n✗ {check_name} failed with error: {e}")
            results.append((check_name, False))
    
    print("\n" + "=" * 50)
    print("VERIFICATION SUMMARY")
    print("=" * 50)
    
    all_passed = True
    for check_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {check_name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("✓ ALL CHECKS PASSED")
        return 0
    else:
        print("✗ SOME CHECKS FAILED")
        return 1

if __name__ == '__main__':
    sys.exit(main())
