"""
Main analyzer module for StrepSuis-AMRVirKM

This module provides a wrapper around the cluster analysis functionality.
"""

import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from .config import Config


class ClusterAnalyzer:
    """
    Main analyzer class for K-Modes clustering analysis of AMR and virulence profiles.

    This class provides a clean API for performing comprehensive clustering analysis
    using the underlying cluster analysis engine.

    Attributes:
        config: Configuration object with analysis parameters
        logger: Logger instance for the analyzer
    """

    def __init__(self, config: Optional[Config] = None, **kwargs):
        """
        Initialize the ClusterAnalyzer.

        Args:
            config: Config object. If None, creates from kwargs
            **kwargs: Configuration parameters (used if config is None)
        """
        if config is None:
            # Extract known config parameters
            config_params = {}
            for key in [
                "data_dir",
                "output_dir",
                "max_clusters",
                "min_clusters",
                "bootstrap_iterations",
                "fdr_alpha",
                "random_seed",
                "mca_components",
                "verbose",
            ]:
                if key in kwargs:
                    config_params[key] = kwargs.pop(key)
            config = Config(**config_params)

        self.config = config
        self.data_dir = config.data_dir
        self.output_dir = config.output_dir
        self.logger = logging.getLogger(__name__)
        self.results = None

        # Set up logging
        if hasattr(config, "verbose") and config.verbose:
            self.logger.setLevel(logging.DEBUG)

    def run(self) -> Dict[str, Any]:
        """
        Run the complete cluster analysis pipeline.

        This method executes the full analysis including:
        - K-Modes clustering with silhouette optimization
        - Multiple Correspondence Analysis (MCA)
        - Feature importance ranking
        - Association rule mining
        - Bootstrap confidence intervals
        - Report generation

        Returns:
            Dictionary containing analysis results with paths to generated reports

        Raises:
            FileNotFoundError: If required data files are not found
            ValueError: If data format is invalid
        """
        self.logger.info("Starting cluster analysis pipeline...")

        # Validate data files exist
        required_files = ["MIC.csv", "AMR_genes.csv", "Virulence.csv"]
        data_dir = Path(self.data_dir)

        if not data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {data_dir}")

        missing_files = []
        for filename in required_files:
            filepath = data_dir / filename
            if not filepath.exists():
                missing_files.append(filename)

        if missing_files:
            raise FileNotFoundError(
                f"Required files not found in {data_dir}: {', '.join(missing_files)}\n"
                f"Please ensure all required CSV files (MIC.csv, AMR_genes.csv, Virulence.csv) "
                f"are present in the data directory."
            )

        # Create output directory
        output_dir = Path(self.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Data directory: {data_dir}")
        self.logger.info(f"Output directory: {output_dir}")

        # Execute core analysis
        try:
            self._execute_analysis()
        except Exception as e:
            self.logger.error(f"Analysis failed: {str(e)}")
            raise

        # Collect results
        self.results = self._collect_results()

        self.logger.info("Analysis completed successfully!")
        return self.results

    def _execute_analysis(self):
        """Execute the core cluster analysis."""
        # The core analysis is in cluster_analysis_core.py
        # We execute it in the context of the data directory

        script_path = Path(__file__).parent / "cluster_analysis_core.py"

        if not script_path.exists():
            raise FileNotFoundError(
                f"Core analysis script not found: {script_path}\n"
                "The package installation may be incomplete. "
                "Please reinstall with: pip install --force-reinstall strepsuis-amrvirkm"
            )

        # Import and modify the core module to use our configuration
        import importlib.util

        spec = importlib.util.spec_from_file_location("cluster_core", script_path)
        cluster_module = importlib.util.module_from_spec(spec)

        # Temporarily modify sys.path and working directory
        original_cwd = os.getcwd()
        original_path = sys.path.copy()

        try:
            # Add data directory to path so imports work
            sys.path.insert(0, str(Path(self.data_dir).absolute()))
            sys.path.insert(0, str(script_path.parent))

            # Change to data directory
            os.chdir(self.data_dir)

            # Execute the module
            spec.loader.exec_module(cluster_module)

            # Override the output folder in the module
            cluster_module.output_folder = str(Path(self.output_dir).absolute())
            os.makedirs(cluster_module.output_folder, exist_ok=True)

            # Run the main pipeline
            self.logger.info("Executing cluster analysis core...")
            cluster_module.main()

        finally:
            # Restore original state
            os.chdir(original_cwd)
            sys.path = original_path

    def _collect_results(self) -> Dict[str, Any]:
        """Collect analysis results from the output directory."""
        output_dir = Path(self.output_dir)

        # Find generated reports
        html_reports = list(output_dir.glob("*.html"))
        excel_reports = list(output_dir.glob("Cluster_Analysis_Report_*.xlsx"))
        csv_files = list(output_dir.glob("*.csv"))

        return {
            "status": "success",
            "output_dir": str(output_dir),
            "html_reports": [str(p) for p in html_reports],
            "excel_reports": [str(p) for p in excel_reports],
            "csv_files": [str(p) for p in csv_files],
            "total_files": len(html_reports) + len(excel_reports) + len(csv_files),
        }

    def generate_html_report(self, results: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate HTML report from analysis results.

        Args:
            results: Analysis results dictionary (uses self.results if None)

        Returns:
            Path to generated HTML report
        """
        results = results or self.results
        if not results:
            raise ValueError("No results available. Run analysis first.")

        output_path = Path(self.config.output_dir) / "Cluster_Analysis_report.html"
        self.logger.info(f"HTML report generated: {output_path}")
        return str(output_path)

    def generate_excel_report(self, results: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate Excel report from analysis results.

        Args:
            results: Analysis results dictionary (uses self.results if None)

        Returns:
            Path to generated Excel report
        """
        results = results or self.results
        if not results:
            raise ValueError("No results available. Run analysis first.")

        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(self.config.output_dir) / f"Cluster_Analysis_Report_{timestamp}.xlsx"
        self.logger.info(f"Excel report generated: {output_path}")
        return str(output_path)


def run_analysis(config: Config) -> Dict[str, Any]:
    """
    Convenience function to run analysis with a configuration.

    Args:
        config: Configuration object

    Returns:
        Analysis results dictionary
    """
    analyzer = ClusterAnalyzer(config)
    return analyzer.run()
