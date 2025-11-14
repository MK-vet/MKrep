#!/usr/bin/env python3
"""
StrepSuis-AMRVirKM Command Line Interface

This module provides the CLI for running cluster analysis on AMR and virulence data.
"""

import argparse
import sys
from pathlib import Path
from .analysis import ClusterAnalyzer


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="StrepSuis-AMRVirKM: K-Modes Clustering Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  strepsuis-amrvirkm --data-dir ./data --output ./results
  
  # Advanced options
  strepsuis-amrvirkm --data-dir ./data --output ./results \\
      --max-clusters 10 --bootstrap 500 --min-support 0.3
  
  # With configuration file
  strepsuis-amrvirkm --config config.yaml

For more information, visit: https://github.com/MK-vet/strepsuis-amrvirkm
        """
    )
    
    # Required arguments
    parser.add_argument(
        "--data-dir",
        type=str,
        required=True,
        help="Directory containing input CSV files (MIC.csv, AMR_genes.csv, Virulence.csv)"
    )
    
    # Optional arguments
    parser.add_argument(
        "--output",
        type=str,
        default="./results",
        help="Output directory for results (default: ./results)"
    )
    
    parser.add_argument(
        "--max-clusters",
        type=int,
        default=8,
        help="Maximum number of clusters to test (default: 8)"
    )
    
    parser.add_argument(
        "--bootstrap",
        type=int,
        default=200,
        help="Number of bootstrap iterations (default: 200)"
    )
    
    parser.add_argument(
        "--min-support",
        type=float,
        default=0.3,
        help="Minimum support for association rules (default: 0.3)"
    )
    
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.5,
        help="Minimum confidence for association rules (default: 0.5)"
    )
    
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    args = parser.parse_args()
    
    try:
        # Validate paths
        data_dir = Path(args.data_dir)
        if not data_dir.exists():
            print(f"Error: Data directory '{data_dir}' does not exist", file=sys.stderr)
            sys.exit(1)
        
        # Create output directory
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"StrepSuis-AMRVirKM v1.0.0")
        print(f"=" * 60)
        print(f"Data directory: {data_dir}")
        print(f"Output directory: {output_dir}")
        print(f"Max clusters: {args.max_clusters}")
        print(f"Bootstrap iterations: {args.bootstrap}")
        print(f"=" * 60)
        print()
        
        # Initialize analyzer
        analyzer = ClusterAnalyzer(
            data_dir=str(data_dir),
            output_dir=str(output_dir),
            max_clusters=args.max_clusters,
            bootstrap_iterations=args.bootstrap,
            min_support=args.min_support,
            min_confidence=args.min_confidence,
            random_seed=args.seed
        )
        
        # Run analysis
        print("Running cluster analysis...")
        results = analyzer.run()
        
        # Generate reports
        print("Generating HTML report...")
        analyzer.generate_html_report(results)
        
        print("Generating Excel report...")
        analyzer.generate_excel_report(results)
        
        print()
        print(f"✓ Analysis complete!")
        print(f"✓ Results saved to: {output_dir}")
        print()
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
