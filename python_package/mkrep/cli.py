"""Command-line interface for MKrep analysis tools."""

import argparse
import sys
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from JSON or YAML file."""
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        if config_path.suffix == '.json':
            return json.load(f)
        elif config_path.suffix in ['.yaml', '.yml']:
            import yaml
            return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported config format: {config_path.suffix}")


def setup_common_parser(parser: argparse.ArgumentParser):
    """Add common arguments to parser."""
    parser.add_argument(
        '--data-dir',
        type=str,
        required=True,
        help='Directory containing input CSV files'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='./output',
        help='Output directory for results (default: ./output)'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Configuration file (JSON/YAML)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )


def cluster_analysis():
    """Command-line interface for cluster analysis."""
    parser = argparse.ArgumentParser(
        description='K-Modes clustering analysis for MIC, AMR, and virulence data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mkrep-cluster --data-dir ./data --output ./results
  mkrep-cluster --data-dir ./data --max-clusters 8 --bootstrap 1000
  mkrep-cluster --config config.json
        """
    )
    
    setup_common_parser(parser)
    
    parser.add_argument(
        '--max-clusters',
        type=int,
        help='Maximum number of clusters to test (default: auto)'
    )
    parser.add_argument(
        '--bootstrap',
        type=int,
        default=500,
        help='Number of bootstrap iterations (default: 500)'
    )
    parser.add_argument(
        '--fdr-alpha',
        type=float,
        default=0.05,
        help='FDR correction alpha level (default: 0.05)'
    )
    parser.add_argument(
        '--mca-components',
        type=int,
        default=2,
        help='Number of MCA components (default: 2)'
    )
    
    args = parser.parse_args()
    
    # Load config if provided
    config = {}
    if args.config:
        config = load_config(args.config)
    
    # Override config with command-line arguments
    config.update({
        'data_dir': args.data_dir,
        'output_dir': args.output,
        'verbose': args.verbose,
        'max_clusters': args.max_clusters,
        'bootstrap_iterations': args.bootstrap,
        'fdr_alpha': args.fdr_alpha,
        'mca_components': args.mca_components,
    })
    
    # Remove None values
    config = {k: v for k, v in config.items() if v is not None}
    
    # Run analysis
    from mkrep.analysis.cluster_analyzer import ClusterAnalyzer
    analyzer = ClusterAnalyzer(**config)
    results = analyzer.run()
    
    print(f"\n✓ Analysis complete!")
    print(f"  HTML report: {results.get('html_report')}")
    print(f"  Excel report: {results.get('excel_report')}")
    print(f"  Output directory: {args.output}")


def mdr_analysis():
    """Command-line interface for MDR analysis."""
    parser = argparse.ArgumentParser(
        description='Multi-drug resistance analysis with hybrid networks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mkrep-mdr --data-dir ./data --output ./results
  mkrep-mdr --data-dir ./data --mdr-threshold 3 --confidence 0.6
  mkrep-mdr --config config.json
        """
    )
    
    setup_common_parser(parser)
    
    parser.add_argument(
        '--mdr-threshold',
        type=int,
        default=3,
        help='Minimum classes for MDR classification (default: 3)'
    )
    parser.add_argument(
        '--bootstrap',
        type=int,
        default=500,
        help='Number of bootstrap iterations (default: 500)'
    )
    parser.add_argument(
        '--confidence',
        type=float,
        default=0.5,
        help='Association rules confidence threshold (default: 0.5)'
    )
    parser.add_argument(
        '--support',
        type=float,
        default=0.1,
        help='Association rules support threshold (default: 0.1)'
    )
    
    args = parser.parse_args()
    
    # Load config if provided
    config = {}
    if args.config:
        config = load_config(args.config)
    
    # Override config with command-line arguments
    config.update({
        'data_dir': args.data_dir,
        'output_dir': args.output,
        'verbose': args.verbose,
        'mdr_threshold': args.mdr_threshold,
        'bootstrap_iterations': args.bootstrap,
        'confidence_threshold': args.confidence,
        'support_threshold': args.support,
    })
    
    # Remove None values
    config = {k: v for k, v in config.items() if v is not None}
    
    # Run analysis
    from mkrep.analysis.mdr_analyzer import MDRAnalyzer
    analyzer = MDRAnalyzer(**config)
    results = analyzer.run()
    
    print(f"\n✓ Analysis complete!")
    print(f"  HTML report: {results.get('html_report')}")
    print(f"  Excel report: {results.get('excel_report')}")
    print(f"  Output directory: {args.output}")


def network_analysis():
    """Command-line interface for network analysis."""
    parser = argparse.ArgumentParser(
        description='Feature association network analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mkrep-network --data-dir ./data --output ./results
  mkrep-network --data-dir ./data --chi2-threshold 0.01 --cramers-threshold 0.4
  mkrep-network --config config.json
        """
    )
    
    setup_common_parser(parser)
    
    parser.add_argument(
        '--chi2-threshold',
        type=float,
        default=0.05,
        help='Chi-square p-value threshold (default: 0.05)'
    )
    parser.add_argument(
        '--cramers-threshold',
        type=float,
        default=0.3,
        help="Cramér's V threshold (default: 0.3)"
    )
    parser.add_argument(
        '--min-degree',
        type=int,
        help='Minimum node degree for hubs (default: auto)'
    )
    
    args = parser.parse_args()
    
    # Load config if provided
    config = {}
    if args.config:
        config = load_config(args.config)
    
    # Override config with command-line arguments
    config.update({
        'data_dir': args.data_dir,
        'output_dir': args.output,
        'verbose': args.verbose,
        'chi2_threshold': args.chi2_threshold,
        'cramers_threshold': args.cramers_threshold,
        'min_degree': args.min_degree,
    })
    
    # Remove None values
    config = {k: v for k, v in config.items() if v is not None}
    
    # Run analysis
    from mkrep.analysis.network_analyzer import NetworkAnalyzer
    analyzer = NetworkAnalyzer(**config)
    results = analyzer.run()
    
    print(f"\n✓ Analysis complete!")
    print(f"  HTML report: {results.get('html_report')}")
    print(f"  Excel report: {results.get('excel_report')}")
    print(f"  Output directory: {args.output}")


def phylogenetic_analysis():
    """Command-line interface for phylogenetic clustering analysis."""
    parser = argparse.ArgumentParser(
        description='Phylogenetic tree-based clustering with evolutionary metrics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mkrep-phylo --tree tree.newick --data-dir ./data --output ./results
  mkrep-phylo --tree tree.newick --data-dir ./data --clustering kmeans --n-clusters 5
  mkrep-phylo --config config.json
        """
    )
    
    setup_common_parser(parser)
    
    parser.add_argument(
        '--tree',
        type=str,
        required=True,
        help='Phylogenetic tree file (Newick format)'
    )
    parser.add_argument(
        '--clustering',
        type=str,
        choices=['kmeans', 'dbscan', 'gmm', 'auto'],
        default='auto',
        help='Clustering method (default: auto)'
    )
    parser.add_argument(
        '--n-clusters',
        type=int,
        help='Number of clusters (default: auto)'
    )
    parser.add_argument(
        '--umap-components',
        type=int,
        default=2,
        help='UMAP dimensions (default: 2)'
    )
    parser.add_argument(
        '--bootstrap',
        type=int,
        default=500,
        help='Number of bootstrap iterations (default: 500)'
    )
    
    args = parser.parse_args()
    
    # Load config if provided
    config = {}
    if args.config:
        config = load_config(args.config)
    
    # Override config with command-line arguments
    config.update({
        'tree_file': args.tree,
        'data_dir': args.data_dir,
        'output_dir': args.output,
        'verbose': args.verbose,
        'clustering_method': args.clustering,
        'n_clusters': args.n_clusters,
        'umap_components': args.umap_components,
        'bootstrap_iterations': args.bootstrap,
    })
    
    # Remove None values
    config = {k: v for k, v in config.items() if v is not None}
    
    # Run analysis
    from mkrep.analysis.phylo_analyzer import PhyloAnalyzer
    analyzer = PhyloAnalyzer(**config)
    results = analyzer.run()
    
    print(f"\n✓ Analysis complete!")
    print(f"  HTML report: {results.get('html_report')}")
    print(f"  Excel report: {results.get('excel_report')}")
    print(f"  Output directory: {args.output}")


def strepsuis_analysis():
    """Command-line interface for Streptococcus suis analysis."""
    parser = argparse.ArgumentParser(
        description='Specialized analysis for Streptococcus suis strains',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mkrep-strepsuis --tree tree.newick --data-dir ./data --output ./results
  mkrep-strepsuis --tree tree.newick --data-dir ./data --n-clusters 6
  mkrep-strepsuis --config config.json
        """
    )
    
    setup_common_parser(parser)
    
    parser.add_argument(
        '--tree',
        type=str,
        required=True,
        help='Phylogenetic tree file (Newick format)'
    )
    parser.add_argument(
        '--n-clusters',
        type=int,
        help='Number of clusters (default: auto)'
    )
    parser.add_argument(
        '--bootstrap',
        type=int,
        default=500,
        help='Number of bootstrap iterations (default: 500)'
    )
    
    args = parser.parse_args()
    
    # Load config if provided
    config = {}
    if args.config:
        config = load_config(args.config)
    
    # Override config with command-line arguments
    config.update({
        'tree_file': args.tree,
        'data_dir': args.data_dir,
        'output_dir': args.output,
        'verbose': args.verbose,
        'n_clusters': args.n_clusters,
        'bootstrap_iterations': args.bootstrap,
    })
    
    # Remove None values
    config = {k: v for k, v in config.items() if v is not None}
    
    # Run analysis
    from mkrep.analysis.strepsuis_analyzer import StrepSuisAnalyzer
    analyzer = StrepSuisAnalyzer(**config)
    results = analyzer.run()
    
    print(f"\n✓ Analysis complete!")
    print(f"  HTML report: {results.get('html_report')}")
    print(f"  Excel report: {results.get('excel_report')}")
    print(f"  Output directory: {args.output}")


def main():
    """Main CLI entry point with subcommands."""
    parser = argparse.ArgumentParser(
        description='MKrep - Microbial Genomics Analysis Tools',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available commands:
  mkrep-cluster      K-Modes clustering analysis
  mkrep-mdr          Multi-drug resistance analysis
  mkrep-network      Network association analysis
  mkrep-phylo        Phylogenetic clustering analysis
  mkrep-strepsuis    Streptococcus suis analysis

For help on a specific command:
  mkrep-<command> --help

Examples:
  mkrep-cluster --data-dir ./data --output ./results
  mkrep-phylo --tree tree.newick --data-dir ./data --output ./results
        """
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    parser.print_help()


if __name__ == '__main__':
    main()
