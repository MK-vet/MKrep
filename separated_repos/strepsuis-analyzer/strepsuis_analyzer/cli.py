"""
Command-line interface for StrepSuis Analyzer.
"""

import argparse
import sys
from pathlib import Path

# Import the analyzer from the standalone script
try:
    from StrepSuisPhyloCluster_2025_08_11 import StrepSuisAnalyzer, main as standalone_main
except ImportError:
    print("Error: Could not import StrepSuisAnalyzer. Please ensure the package is properly installed.")
    sys.exit(1)


def create_parser():
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description='StrepSuis Analyzer: General-Purpose Genomic Data Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis with one data file
  %(prog)s --data virulence.csv
  
  # Multiple data files
  %(prog)s --data amr.csv virulence.csv
  
  # With phylogenetic tree
  %(prog)s --data data.csv --tree tree.newick
  
  # Specify number of clusters and output directory
  %(prog)s --data data.csv --clusters 4 --output results/
  
  # Set custom random seed
  %(prog)s --data data.csv --seed 123

For more information, see the USER_GUIDE.md file.
        """
    )
    
    parser.add_argument(
        '--data',
        nargs='+',
        required=True,
        metavar='FILE',
        help='One or more CSV data files with binary trait data'
    )
    
    parser.add_argument(
        '--tree',
        metavar='FILE',
        help='Phylogenetic tree file in Newick format (optional)'
    )
    
    parser.add_argument(
        '--output',
        default='output',
        metavar='DIR',
        help='Output directory (default: output)'
    )
    
    parser.add_argument(
        '--clusters',
        type=int,
        metavar='N',
        help='Number of clusters (default: auto-determined by silhouette score)'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        metavar='N',
        help='Random seed for reproducibility (default: 42)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 2025.8.11'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser


def main(args=None):
    """Main entry point for CLI."""
    parser = create_parser()
    args = parser.parse_args(args)
    
    # Delegate to standalone script's main function
    # Convert args to format expected by standalone script
    sys.argv = ['strepsuis-analyzer']
    sys.argv.extend(['--data'] + args.data)
    if args.tree:
        sys.argv.extend(['--tree', args.tree])
    sys.argv.extend(['--output', args.output])
    if args.clusters:
        sys.argv.extend(['--clusters', str(args.clusters)])
    sys.argv.extend(['--seed', str(args.seed)])
    
    # Call the standalone main function
    try:
        standalone_main()
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
