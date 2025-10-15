#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phylogenetic Clustering Analysis Runner Script
===============================================

This script provides a convenient command-line interface for running
the phylogenetic clustering and trait analysis pipeline.

Usage:
    python run_phylogenetic_analysis.py [options]

Examples:
    # Run with default settings
    python run_phylogenetic_analysis.py
    
    # Run with custom output folder
    python run_phylogenetic_analysis.py --output my_results
    
    # Run with custom tree file
    python run_phylogenetic_analysis.py --tree my_tree.newick
    
    # Run with all custom settings
    python run_phylogenetic_analysis.py --tree my_tree.newick --output my_results --bootstrap 1000

Author: MK-vet
Date: 2025-03-21
"""

import argparse
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import analysis components
from Phylgenetic_clustering_2025_03_21 import (
    PhylogeneticAnalysis,
    HTMLReportGenerator,
    Config,
    print_section_header,
    logging
)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Run phylogenetic clustering and trait analysis pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s
  %(prog)s --output my_results
  %(prog)s --tree my_tree.newick --output my_results
  %(prog)s --bootstrap 1000 --fdr-alpha 0.01
        """
    )
    
    # Input files
    parser.add_argument(
        '--tree',
        type=str,
        default='Snp_tree.newick',
        help='Phylogenetic tree file (Newick format) (default: Snp_tree.newick)'
    )
    parser.add_argument(
        '--mic',
        type=str,
        default='MIC.csv',
        help='MIC data file (CSV format) (default: MIC.csv)'
    )
    parser.add_argument(
        '--amr',
        type=str,
        default='AMR_genes.csv',
        help='AMR genes data file (CSV format) (default: AMR_genes.csv)'
    )
    parser.add_argument(
        '--virulence',
        type=str,
        default='Virulence.csv',
        help='Virulence genes data file (CSV format) (default: Virulence.csv)'
    )
    
    # Output settings
    parser.add_argument(
        '--output',
        type=str,
        default='phylogenetic_clustering_results',
        help='Output folder name (default: phylogenetic_clustering_results)'
    )
    parser.add_argument(
        '--base-dir',
        type=str,
        default='.',
        help='Base directory for input/output (default: current directory)'
    )
    
    # UMAP parameters
    parser.add_argument(
        '--umap-components',
        type=int,
        default=2,
        help='Number of UMAP components (default: 2)'
    )
    parser.add_argument(
        '--umap-neighbors',
        type=int,
        default=15,
        help='Number of UMAP neighbors (default: 15)'
    )
    parser.add_argument(
        '--umap-min-dist',
        type=float,
        default=0.1,
        help='UMAP minimum distance (default: 0.1)'
    )
    
    # Clustering parameters
    parser.add_argument(
        '--outlier-contamination',
        type=float,
        default=0.05,
        help='Outlier contamination threshold (default: 0.05)'
    )
    parser.add_argument(
        '--outlier-estimators',
        type=int,
        default=200,
        help='Number of outlier estimators (default: 200)'
    )
    parser.add_argument(
        '--min-clusters',
        type=int,
        default=2,
        help='Minimum number of clusters (default: 2)'
    )
    parser.add_argument(
        '--max-clusters',
        type=int,
        default=10,
        help='Maximum number of clusters (default: 10)'
    )
    
    # Statistical parameters
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
        help='FDR alpha level for multiple testing correction (default: 0.05)'
    )
    
    # Advanced parameters
    parser.add_argument(
        '--parallel-tree',
        action='store_true',
        help='Enable parallel processing for tree distance calculations'
    )
    parser.add_argument(
        '--parallel-jobs',
        type=int,
        default=1,
        help='Number of parallel jobs (default: 1)'
    )
    
    # Report options
    parser.add_argument(
        '--skip-html',
        action='store_true',
        help='Skip HTML report generation'
    )
    parser.add_argument(
        '--skip-excel',
        action='store_true',
        help='Skip Excel report generation'
    )
    
    return parser.parse_args()


def validate_input_files(args):
    """Validate that input files exist."""
    files_to_check = [
        (args.tree, 'Tree file'),
        (args.mic, 'MIC data file'),
        (args.amr, 'AMR genes file'),
        (args.virulence, 'Virulence genes file')
    ]
    
    missing_files = []
    for filepath, file_desc in files_to_check:
        full_path = os.path.join(args.base_dir, filepath)
        if not os.path.exists(full_path):
            missing_files.append(f"{file_desc}: {filepath}")
    
    if missing_files:
        print("\nError: The following input files were not found:")
        for missing in missing_files:
            print(f"  - {missing}")
        print("\nPlease ensure all required input files exist in the specified directory.")
        return False
    
    return True


def main():
    """Main execution function."""
    args = parse_arguments()
    
    # Print banner
    print(f"""
{'='*80}
PHYLOGENETIC CLUSTERING ANALYSIS PIPELINE
{'='*80}

Configuration:
  Tree file:        {args.tree}
  MIC file:         {args.mic}
  AMR genes file:   {args.amr}
  Virulence file:   {args.virulence}
  Output folder:    {args.output}
  Base directory:   {args.base_dir}

Parameters:
  UMAP components:      {args.umap_components}
  UMAP neighbors:       {args.umap_neighbors}
  Cluster range:        {args.min_clusters}-{args.max_clusters}
  Bootstrap iterations: {args.bootstrap}
  FDR alpha:            {args.fdr_alpha}

{'='*80}
""")
    
    # Validate input files
    print("Validating input files...")
    if not validate_input_files(args):
        return 1
    print("✓ All input files found")
    
    # Create configuration
    config = Config(
        base_dir=args.base_dir,
        output_folder=args.output,
        tree_file=args.tree,
        mic_file=args.mic,
        amr_genes_file=args.amr,
        virulence_genes_file=args.virulence,
        umap_components=args.umap_components,
        umap_neighbors=args.umap_neighbors,
        umap_min_dist=args.umap_min_dist,
        outlier_contamination=args.outlier_contamination,
        outlier_n_estimators=args.outlier_estimators,
        n_clusters_range=(args.min_clusters, args.max_clusters),
        n_ensemble=5,
        dbscan_trials=20,
        bootstrap_iterations=args.bootstrap,
        fdr_alpha=args.fdr_alpha,
        parallel_tree=args.parallel_tree,
        parallel_jobs=args.parallel_jobs
    )
    
    # Run analysis pipeline
    print("\nStarting analysis pipeline...")
    analysis = PhylogeneticAnalysis(config)
    final_results = analysis.run_complete_analysis()
    
    if final_results is None:
        print("\n❌ Analysis failed. Please check the log file for details.")
        return 1
    
    # Generate reports
    if not args.skip_html or not args.skip_excel:
        print_section_header("GENERATING COMPREHENSIVE REPORTS")
        report_generator = HTMLReportGenerator(config.output_folder, base_dir=config.base_dir)
        
        if not args.skip_html:
            logging.info("Generating interactive HTML report...")
            html_report_path = report_generator.generate_report(
                final_results, config, "phylogenetic_report.html"
            )
            logging.info(f"✓ HTML report saved to: {html_report_path}")
        
        if not args.skip_excel:
            logging.info("Generating comprehensive Excel report...")
            excel_report_path = report_generator.generate_excel_report(final_results, config)
            logging.info(f"✓ Excel report saved to: {excel_report_path}")
    
    # Print final summary
    print_section_header("ANALYSIS COMPLETE")
    print(f"""
✓ Analysis completed successfully!

Output directory: {os.path.join(config.base_dir, config.output_folder)}

Generated files:
  - phylogenetic_analysis.log (execution log)
  - phylogenetic_clusters.csv (cluster assignments)
  - evolutionary_cluster_analysis.csv (phylogenetic metrics)
  - Various analysis CSV files
""")
    
    if not args.skip_html:
        print("  - phylogenetic_report.html (interactive HTML report)")
    if not args.skip_excel:
        print("  - Phylogenetic_Clustering_Report_*.xlsx (Excel workbook)")
    
    print(f"""
Please review the reports for detailed analysis results.

{'='*80}
""")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
