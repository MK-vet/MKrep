"""
Command-line interface for StrepSuis-AMRVirKM
"""

import argparse
import logging
import sys

from . import __version__
from .analyzer import ClusterAnalyzer
from .config import Config


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="StrepSuis-AMRVirKM: K-Modes Clustering for AMR and Virulence Profiles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  strepsuis-amrvirkm --data-dir ./data --output ./results
  
  # With custom parameters
  strepsuis-amrvirkm --data-dir ./data --output ./results --max-clusters 8 --bootstrap 1000
  
  # Verbose output
  strepsuis-amrvirkm --data-dir ./data --output ./results --verbose

For more information, visit: https://github.com/MK-vet/strepsuis-amrvirkm
        """,
    )

    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    # Required arguments
    parser.add_argument(
        "--data-dir",
        type=str,
        required=True,
        help="Directory containing input CSV files (MIC.csv, AMR_genes.csv, Virulence.csv, etc.)",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="./output",
        help="Output directory for results (default: ./output)",
    )

    # Clustering parameters
    parser.add_argument(
        "--max-clusters",
        type=int,
        default=10,
        help="Maximum number of clusters to test (default: 10)",
    )

    parser.add_argument(
        "--min-clusters",
        type=int,
        default=2,
        help="Minimum number of clusters to test (default: 2)",
    )

    # Statistical parameters
    parser.add_argument(
        "--bootstrap", type=int, default=500, help="Number of bootstrap iterations (default: 500)"
    )

    parser.add_argument(
        "--fdr-alpha", type=float, default=0.05, help="FDR correction alpha level (default: 0.05)"
    )

    parser.add_argument(
        "--random-seed", type=int, default=42, help="Random seed for reproducibility (default: 42)"
    )

    # MCA parameters
    parser.add_argument(
        "--mca-components", type=int, default=2, help="Number of MCA components (default: 2)"
    )

    # Other options
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    parser.add_argument("--no-html", action="store_true", help="Skip HTML report generation")

    parser.add_argument("--no-excel", action="store_true", help="Skip Excel report generation")

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    try:
        # Create configuration
        config = Config(
            data_dir=args.data_dir,
            output_dir=args.output,
            max_clusters=args.max_clusters,
            min_clusters=args.min_clusters,
            bootstrap_iterations=args.bootstrap,
            fdr_alpha=args.fdr_alpha,
            random_seed=args.random_seed,
            mca_components=args.mca_components,
            generate_html=not args.no_html,
            generate_excel=not args.no_excel,
        )

        logger.info(f"StrepSuis-AMRVirKM v{__version__}")
        logger.info(f"Data directory: {config.data_dir}")
        logger.info(f"Output directory: {config.output_dir}")

        # Create analyzer and run analysis
        analyzer = ClusterAnalyzer(config)
        logger.info("Starting cluster analysis...")

        _ = analyzer.run()

        logger.info("Analysis completed successfully!")
        logger.info(f"Results saved to: {config.output_dir}")

        return 0

    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}", exc_info=args.verbose)
        return 1


if __name__ == "__main__":
    sys.exit(main())
