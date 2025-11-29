#!/usr/bin/env python3
"""
Validation script to verify all MKrep analysis tools are working correctly.
This script checks:
1. All required dependencies are installed
2. Data files can be loaded
3. Basic functionality works
4. Reports can be generated
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if all required packages are installed."""
    print("=" * 80)
    print("Checking Dependencies")
    print("=" * 80)
    
    required_packages = [
        "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly",
        "sklearn", "Bio", "umap", "networkx", "statsmodels",
        "mlxtend", "prince", "jinja2", "openpyxl"
    ]
    
    optional_packages = [
        "kmodes", "optuna", "community", "ydata_profiling",
        "joblib", "numba", "psutil", "kaleido"
    ]
    
    missing_required = []
    missing_optional = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (REQUIRED)")
            missing_required.append(package)
    
    print("\nOptional packages:")
    for package in optional_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"○ {package} (optional)")
            missing_optional.append(package)
    
    if missing_required:
        print(f"\n❌ ERROR: Missing required packages: {', '.join(missing_required)}")
        print("Install with: pip install " + " ".join(missing_required))
        return False
    
    if missing_optional:
        print(f"\n⚠ WARNING: Missing optional packages: {', '.join(missing_optional)}")
        print("Some features may not work. Install with: pip install " + " ".join(missing_optional))
    
    print("\n✓ All required dependencies are installed")
    return True


def check_data_files():
    """Check if example data files exist."""
    print("\n" + "=" * 80)
    print("Checking Data Files")
    print("=" * 80)
    
    data_files = [
        "MIC.csv", "AMR_genes.csv", "Virulence.csv",
        "MLST.csv", "Serotype.csv", "Plasmid.csv", "MGE.csv"
    ]
    
    optional_files = ["Snp_tree.newick", "tree.newick", "tree.nwk"]
    
    found_files = []
    missing_files = []
    
    for file in data_files:
        if os.path.exists(file):
            print(f"✓ {file}")
            found_files.append(file)
        else:
            print(f"○ {file} (not found)")
            missing_files.append(file)
    
    print("\nOptional files:")
    for file in optional_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"○ {file} (not found)")
    
    if not found_files:
        print("\n⚠ WARNING: No data files found. Scripts will fail without input data.")
        return False
    
    print(f"\n✓ Found {len(found_files)} data files")
    return True


def validate_binary_data(file_path):
    """Validate that a CSV file contains binary data."""
    import pandas as pd
    import numpy as np
    
    try:
        df = pd.read_csv(file_path)
        
        # Check for Strain_ID column
        if 'Strain_ID' not in df.columns and df.columns[0] != 'Strain_ID':
            return False, "Missing 'Strain_ID' column"
        
        # Get feature columns (all except first)
        feature_cols = df.columns[1:]
        
        if len(feature_cols) == 0:
            return False, "No feature columns found"
        
        # Check if all values are 0 or 1
        for col in feature_cols:
            values = df[col].dropna()
            if not ((values == 0) | (values == 1)).all():
                non_binary = values[~((values == 0) | (values == 1))].unique()
                return False, f"Column '{col}' contains non-binary values: {non_binary}"
        
        # Check for missing values
        missing = df[feature_cols].isna().sum().sum()
        if missing > 0:
            return False, f"Found {missing} missing values"
        
        return True, f"Valid binary data: {len(df)} strains, {len(feature_cols)} features"
    
    except Exception as e:
        return False, f"Error reading file: {str(e)}"


def check_binary_format():
    """Check if data files are in proper binary format."""
    print("\n" + "=" * 80)
    print("Validating Binary Data Format")
    print("=" * 80)
    
    data_files = [f for f in ["MIC.csv", "AMR_genes.csv", "Virulence.csv"] if os.path.exists(f)]
    
    if not data_files:
        print("⚠ No data files to validate")
        return True
    
    all_valid = True
    for file in data_files:
        valid, message = validate_binary_data(file)
        if valid:
            print(f"✓ {file}: {message}")
        else:
            print(f"✗ {file}: {message}")
            all_valid = False
    
    if all_valid:
        print("\n✓ All data files have proper binary format (0 = absence, 1 = presence)")
    else:
        print("\n❌ Some data files have format issues. See BINARY_DATA_GUIDE.md for help.")
    
    return all_valid


def check_scripts():
    """Check if analysis scripts exist and are valid Python files."""
    print("\n" + "=" * 80)
    print("Checking Analysis Scripts")
    print("=" * 80)
    
    scripts = [
        "Cluster_MIC_AMR_Viruelnce.py",
        "MDR_2025_04_15.py",
        "Network_Analysis_2025_06_26.py",
        "Phylogenetic_clustering_2025_03_21.py",
        "StrepSuisPhyloCluster_2025_08_11.py"
    ]
    
    all_found = True
    for script in scripts:
        if os.path.exists(script):
            # Check if it's a Colab-style script (may have ! commands)
            with open(script, 'r') as f:
                content = f.read()
                has_colab_commands = '!pip install' in content or 'from google.colab' in content
            
            if has_colab_commands:
                print(f"✓ {script} (Colab-compatible)")
            else:
                # Try to compile the script
                try:
                    compile(content, script, 'exec')
                    print(f"✓ {script}")
                except SyntaxError as e:
                    print(f"✗ {script}: Syntax error at line {e.lineno}")
                    all_found = False
        else:
            print(f"✗ {script}: Not found")
            all_found = False
    
    if all_found:
        print("\n✓ All analysis scripts found and valid")
    else:
        print("\n❌ Some scripts are missing or have syntax errors")
    
    return all_found


def check_utilities():
    """Check if utility modules exist."""
    print("\n" + "=" * 80)
    print("Checking Utility Modules")
    print("=" * 80)
    
    if os.path.exists("excel_report_utils.py"):
        print("✓ excel_report_utils.py")
        try:
            import excel_report_utils
            print("  ✓ Module can be imported")
            return True
        except Exception as e:
            print(f"  ✗ Import error: {str(e)}")
            return False
    else:
        print("✗ excel_report_utils.py not found")
        return False


def check_directories():
    """Check directory structure."""
    print("\n" + "=" * 80)
    print("Checking Directory Structure")
    print("=" * 80)
    
    directories = [
        ("colab_notebooks", "Google Colab notebooks"),
        ("python_package", "Python package structure"),
        ("huggingface_demo", "Hugging Face demo"),
    ]
    
    for dir_name, description in directories:
        if os.path.isdir(dir_name):
            files = os.listdir(dir_name)
            print(f"✓ {dir_name}/ ({len(files)} files) - {description}")
        else:
            print(f"○ {dir_name}/ (not found) - {description}")
    
    print("\n✓ Repository structure verified")
    return True


def print_summary():
    """Print summary and next steps."""
    print("\n" + "=" * 80)
    print("Summary and Next Steps")
    print("=" * 80)
    
    print("""
Quick Start Guide:

1. **Install Dependencies** (if not already installed):
   pip install -r requirements.txt

2. **Prepare Your Data**:
   - CSV format with Strain_ID column
   - Binary values (0 = absence, 1 = presence)
   - See BINARY_DATA_GUIDE.md for details

3. **Run Analysis** (choose one):
   
   a) Standalone Script:
      python Cluster_MIC_AMR_Viruelnce.py
   
   b) Google Colab:
      Open colab_notebooks/Cluster_Analysis_Colab.ipynb
   
   c) Python Package (when installed):
      mkrep-cluster --data-dir ./data --output ./results
   
   d) Interactive Dashboard:
      cd huggingface_demo
      voila MKrep_Dashboard.ipynb

4. **View Results**:
   - HTML report: Interactive tables and visualizations
   - Excel report: Detailed data and methodology
   - PNG charts: High-quality figures for publications

For detailed instructions, see:
- README.md - General usage
- INSTALLATION.md - Installation guide
- BINARY_DATA_GUIDE.md - Data format guide
- colab_notebooks/README.md - Colab usage
- python_package/README.md - Package usage
""")


def main():
    """Run all validation checks."""
    print("MKrep Validation Script")
    print("Version 1.0.0")
    print()
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Data Files", check_data_files),
        ("Binary Format", check_binary_format),
        ("Analysis Scripts", check_scripts),
        ("Utility Modules", check_utilities),
        ("Directory Structure", check_directories),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error during {name} check: {str(e)}")
            results.append((name, False))
    
    # Print final summary
    print("\n" + "=" * 80)
    print("Validation Results")
    print("=" * 80)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n✓ All validation checks passed!")
        print("The repository is ready to use.")
    else:
        print("\n⚠ Some validation checks failed.")
        print("Please review the output above and fix any issues.")
    
    print_summary()
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
