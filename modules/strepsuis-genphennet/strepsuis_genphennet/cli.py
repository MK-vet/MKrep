#!/usr/bin/env python3
"""
StrepSuis-GenPhenNet: Network-Based Integration of Genome–Phenome Data - Command Line Interface
"""

import argparse
import sys
from pathlib import Path
from .analysis import NetworkAnalyzer


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Network-Based Integration of Genome–Phenome Data",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--data-dir", required=True, help="Input data directory")
    parser.add_argument("--output", default="./results", help="Output directory")
    
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    
    args = parser.parse_args()
    
    try:
        data_dir = Path(args.data_dir)
        if not data_dir.exists():
            print(f"Error: Data directory not found: {data_dir}", file=sys.stderr)
            sys.exit(1)
        
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"StrepSuis-GenPhenNet: Network-Based Integration of Genome–Phenome Data")
        print("=" * 60)
        print(f"Data: {data_dir}")
        print(f"Output: {output_dir}")
        print("=" * 60)
        
        analyzer = NetworkAnalyzer(
            data_dir=str(data_dir),
            output_dir=str(output_dir),
            
            random_seed=args.seed
        )
        
        print("Running analysis...")
        results = analyzer.run()
        
        print("Generating reports...")
        analyzer.generate_html_report(results)
        analyzer.generate_excel_report(results)
        
        print("\n✓ Analysis complete!")
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
