#!/usr/bin/env python3
"""
Example: Running StrepSuis Analyzer with sample data

This script demonstrates how to use the StrepSuis Analyzer
with the included Virulence.csv data.
"""

import sys
from pathlib import Path

# Add the script to path
sys.path.insert(0, str(Path(__file__).parent))

from StrepSuisPhyloCluster_2025_08_11 import StrepSuisAnalyzer


def main():
    """Run example analysis."""
    
    print("="*60)
    print("StrepSuis Analyzer - Example Analysis")
    print("="*60)
    
    # Initialize analyzer
    analyzer = StrepSuisAnalyzer(
        output_dir="example_output",
        random_state=42
    )
    
    # Check if data file exists
    data_file = Path(__file__).parent / "data" / "Virulence.csv"
    
    if not data_file.exists():
        print(f"\nError: Data file not found: {data_file}")
        print("Please ensure Virulence.csv is in the data/ directory")
        return 1
    
    print(f"\nUsing data file: {data_file}")
    
    # Run full analysis
    analyzer.run_full_analysis(
        data_files=[str(data_file)],
        tree_file=None,  # No tree file in this example
        n_clusters=None  # Auto-determine optimal clusters
    )
    
    print("\n" + "="*60)
    print("Example analysis complete!")
    print("="*60)
    print("\nCheck the 'example_output' directory for results:")
    print("  - analysis_report.html (Interactive web report)")
    print("  - analysis_results.xlsx (Excel workbook)")
    print("  - clustered_data.csv (Cluster assignments)")
    print("  - trait_associations.csv (Statistical results)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
