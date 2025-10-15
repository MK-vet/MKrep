#!/usr/bin/env python3
"""
Quick Start Script for Cluster Analysis Pipeline
================================================

This script provides a simple way to run the cluster analysis
with basic error checking and user feedback.

Usage:
    python run_cluster_analysis.py

Requirements:
    - MIC.csv, AMR_genes.csv, and Virulence.csv in current directory
    - All dependencies installed (pip install -r requirements.txt)
"""

import os
import sys
import time
from datetime import datetime

# ANSI color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_color(text, color=RESET):
    """Print colored text to terminal"""
    print(f"{color}{text}{RESET}")

def check_file_exists(filename):
    """Check if a required file exists"""
    if os.path.exists(filename):
        print_color(f"✓ Found: {filename}", GREEN)
        return True
    else:
        print_color(f"✗ Missing: {filename}", RED)
        return False

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        'kmodes', 'prince', 'pandas', 'numpy', 'plotly', 
        'jinja2', 'openpyxl', 'sklearn', 'statsmodels'
    ]
    
    print_color("\n📦 Checking Python dependencies...", BLUE)
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print_color(f"✓ {package}", GREEN)
        except ImportError:
            print_color(f"✗ {package}", RED)
            missing.append(package)
    
    return len(missing) == 0, missing

def check_data_files():
    """Check if required data files exist"""
    print_color("\n📄 Checking data files...", BLUE)
    required_files = ['MIC.csv', 'AMR_genes.csv', 'Virulence.csv']
    
    all_present = True
    for filename in required_files:
        if not check_file_exists(filename):
            all_present = False
    
    return all_present

def validate_csv_format(filename):
    """Basic validation of CSV format"""
    try:
        import pandas as pd
        df = pd.read_csv(filename, nrows=5)
        
        # Check for Strain_ID column
        if 'Strain_ID' not in df.columns:
            print_color(f"  ⚠ Warning: No 'Strain_ID' column in {filename}", YELLOW)
            return False
        
        # Check for binary data in other columns
        other_cols = [col for col in df.columns if col != 'Strain_ID']
        if len(other_cols) > 0:
            sample_data = df[other_cols].values.flatten()
            unique_vals = set(sample_data[~pd.isna(sample_data)])
            if not unique_vals.issubset({0, 1, 0.0, 1.0}):
                print_color(f"  ⚠ Warning: Non-binary values detected in {filename}", YELLOW)
                print_color(f"    Found values: {unique_vals}", YELLOW)
                return False
        
        print_color(f"  ✓ Format looks good", GREEN)
        return True
        
    except Exception as e:
        print_color(f"  ⚠ Could not validate {filename}: {str(e)}", YELLOW)
        return False

def main():
    """Main execution function"""
    print_color("\n" + "="*60, BLUE)
    print_color("  Cluster Analysis Pipeline - Quick Start", BLUE)
    print_color("="*60 + "\n", BLUE)
    
    # Step 1: Check dependencies
    deps_ok, missing = check_dependencies()
    if not deps_ok:
        print_color("\n❌ Missing dependencies detected!", RED)
        print_color("\nPlease install missing packages:", YELLOW)
        print_color(f"  pip install {' '.join(missing)}", YELLOW)
        print_color("\nOr install all requirements:", YELLOW)
        print_color("  pip install -r requirements.txt", YELLOW)
        sys.exit(1)
    
    print_color("\n✓ All dependencies installed!", GREEN)
    
    # Step 2: Check data files
    if not check_data_files():
        print_color("\n❌ Required data files are missing!", RED)
        print_color("\nRequired files:", YELLOW)
        print_color("  - MIC.csv", YELLOW)
        print_color("  - AMR_genes.csv", YELLOW)
        print_color("  - Virulence.csv", YELLOW)
        print_color("\nSee BINARY_DATA_GUIDE.md for format requirements.", YELLOW)
        sys.exit(1)
    
    print_color("\n✓ All data files present!", GREEN)
    
    # Step 3: Validate CSV format
    print_color("\n🔍 Validating CSV format...", BLUE)
    for filename in ['MIC.csv', 'AMR_genes.csv', 'Virulence.csv']:
        print_color(f"\n  Checking {filename}:", BLUE)
        validate_csv_format(filename)
    
    # Step 4: Run analysis
    print_color("\n" + "="*60, BLUE)
    print_color("  Starting Cluster Analysis", BLUE)
    print_color("="*60 + "\n", BLUE)
    
    print_color("⏳ This may take a few minutes...", YELLOW)
    print_color("   - K-Modes clustering", YELLOW)
    print_color("   - Statistical tests", YELLOW)
    print_color("   - Bootstrap confidence intervals", YELLOW)
    print_color("   - MCA analysis", YELLOW)
    print_color("   - Report generation", YELLOW)
    
    start_time = time.time()
    
    try:
        # Import and run the main analysis
        import Cluster_MIC_AMR_Viruelnce as cluster_analysis
        cluster_analysis.main()
        
        elapsed_time = time.time() - start_time
        
        print_color("\n" + "="*60, GREEN)
        print_color("  ✓ Analysis Complete!", GREEN)
        print_color("="*60, GREEN)
        print_color(f"\n⏱  Time elapsed: {elapsed_time:.1f} seconds", BLUE)
        
        # Show output information
        output_folder = cluster_analysis.output_folder
        print_color(f"\n📁 Output folder: {output_folder}/", BLUE)
        print_color("\n📊 Generated files:", BLUE)
        print_color(f"  - HTML report: comprehensive_cluster_analysis_report.html", GREEN)
        
        # Find Excel report
        import glob
        excel_files = glob.glob(os.path.join(output_folder, "Cluster_Analysis_Report_*.xlsx"))
        if excel_files:
            excel_file = os.path.basename(excel_files[-1])
            print_color(f"  - Excel report: {excel_file}", GREEN)
        
        # Count CSV files
        csv_files = glob.glob(os.path.join(output_folder, "*.csv"))
        print_color(f"  - {len(csv_files)} CSV files with detailed results", GREEN)
        
        print_color("\n🎉 Success! Check the HTML report for interactive results.", GREEN)
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        print_color("\n" + "="*60, RED)
        print_color("  ❌ Analysis Failed", RED)
        print_color("="*60, RED)
        print_color(f"\n⏱  Time before error: {elapsed_time:.1f} seconds", BLUE)
        print_color(f"\nError: {str(e)}", RED)
        print_color("\n💡 Troubleshooting tips:", YELLOW)
        print_color("  1. Check the analysis.log file for details", YELLOW)
        print_color("  2. Verify your CSV files have correct format", YELLOW)
        print_color("  3. Make sure you have enough disk space", YELLOW)
        print_color("  4. See CLUSTER_ANALYSIS_README.md for help", YELLOW)
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_color("\n\n⚠️  Analysis interrupted by user", YELLOW)
        sys.exit(1)
