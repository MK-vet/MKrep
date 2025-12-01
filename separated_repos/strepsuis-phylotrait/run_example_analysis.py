#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example runner script for strepsuis-phylotrait analysis.
Uses the example data provided in the examples/ folder.

This script demonstrates how to run the PhylogeneticAnalysis pipeline
with the sample data included in the repository.

Usage:
    python run_example_analysis.py
"""

import os
import sys
import shutil
import tempfile

# Add the module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from strepsuis_phylotrait.phylo_analysis_core import Config, PhylogeneticAnalysis, HTMLReportGenerator


def main():
    """Run the example analysis using sample data."""
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(script_dir, "examples")
    output_dir = os.path.join(script_dir, "example_outputs")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # The DataLoader class expects Virulence3.csv, so we create a copy if needed
    # This is a workaround for the hardcoded filename in the DataLoader
    vir_src = os.path.join(base_dir, "Virulence.csv")
    vir_dst = os.path.join(base_dir, "Virulence3.csv")
    cleanup_virulence = False
    if os.path.exists(vir_src) and not os.path.exists(vir_dst):
        shutil.copy(vir_src, vir_dst)
        cleanup_virulence = True

    # Configuration
    config = Config(
        base_dir=base_dir,
        output_folder=output_dir,
        tree_file="tree.newick",
        mic_file="MIC.csv",
        amr_genes_file="AMR_genes.csv",
        virulence_genes_file="Virulence3.csv",
        umap_components=2,
        umap_neighbors=10,  # Lower for small dataset
        umap_min_dist=0.1,
        outlier_contamination=0.05,
        outlier_n_estimators=100,
        n_clusters_range=(2, 6),  # Smaller range for example
        n_ensemble=3,
        dbscan_trials=10,
        bootstrap_iterations=50,  # Fewer for speed
        fdr_alpha=0.05,
        parallel_tree=False,
        parallel_jobs=1
    )

    print("=" * 60)
    print("StrepSuis-PhyloTrait Example Analysis")
    print("=" * 60)
    print(f"Input data: {base_dir}")
    print(f"Output: {output_dir}")
    print("=" * 60)

    # Run analysis
    analysis = PhylogeneticAnalysis(config)
    results = analysis.run_complete_analysis()

    try:
        if results is not None:
            # Generate reports
            report_gen = HTMLReportGenerator(output_dir, base_dir=base_dir)

            # HTML report
            html_path = report_gen.generate_report(results, config, "example_phylogenetic_report.html")
            print(f"\nHTML report: {html_path}")

            # Excel report
            try:
                excel_path = report_gen.generate_excel_report(results, config)
                print(f"Excel report: {excel_path}")
            except Exception as e:
                print(f"Excel report generation skipped: {e}")

            print("\n" + "=" * 60)
            print("Analysis completed successfully!")
            print("=" * 60)

            # List generated files
            print("\nGenerated files:")
            for f in sorted(os.listdir(output_dir)):
                fpath = os.path.join(output_dir, f)
                if os.path.isfile(fpath):
                    size = os.path.getsize(fpath) / 1024
                    print(f"  - {f} ({size:.1f} KB)")
                else:
                    print(f"  - {f}/ (directory)")
            return 0
        else:
            print("Analysis failed!")
            return 1
    finally:
        # Clean up the temporary Virulence3.csv if we created it
        if cleanup_virulence and os.path.exists(vir_dst):
            os.remove(vir_dst)


if __name__ == "__main__":
    sys.exit(main())
