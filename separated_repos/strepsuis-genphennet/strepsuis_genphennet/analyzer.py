"""
Main analyzer module for StrepSuis-GenPhenNet
"""

import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from .config import Config


class NetworkAnalyzer:
    """
    Main analyzer class for network-based genomic-phenotypic association analysis.

    Performs:
    - Chi-square and Fisher exact tests with FDR correction
    - Information theory metrics
    - Mutually exclusive pattern detection
    - 3D network visualization with community detection
    """

    def __init__(self, config: Optional[Config] = None, **kwargs):
        """
        Initialize the analyzer.

        Args:
            config: Config object. If None, creates from kwargs
            **kwargs: Configuration parameters (used if config is None)
        """
        if config is None:
            config_params = {}
            for key in [
                "data_dir",
                "output_dir",
                "fdr_alpha",
                "min_support",
                "min_confidence",
                "network_threshold",
                "verbose",
            ]:
                if key in kwargs:
                    config_params[key] = kwargs.pop(key)
            config = Config(**config_params)

        self.config = config
        self.data_dir = config.data_dir
        self.output_dir = config.output_dir
        self.logger = logging.getLogger(__name__)
        self.results: Optional[Dict[str, Any]] = None

    def run(self) -> Dict[str, Any]:
        """
        Run the complete network analysis pipeline.

        Returns:
            Dictionary containing analysis results
        """
        self.logger.info("Starting network analysis pipeline...")

        # Validate data files
        required_files = ["MIC.csv", "AMR_genes.csv", "Virulence.csv"]
        data_dir = Path(self.data_dir)

        if not data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {data_dir}")

        missing_files = []
        for filename in required_files:
            if not (data_dir / filename).exists():
                missing_files.append(filename)

        if missing_files:
            raise FileNotFoundError(f"Required files not found: {', '.join(missing_files)}")

        # Create output directory
        output_dir = Path(self.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Execute core analysis
        self._execute_analysis()

        # Collect results
        self.results = self._collect_results()

        self.logger.info("Analysis completed successfully!")
        return self.results

    def _execute_analysis(self):
        """Execute the core network analysis."""
        script_path = Path(__file__).parent / "network_analysis_core.py"

        if not script_path.exists():
            raise FileNotFoundError(f"Core analysis script not found: {script_path}")

        import importlib.util

        spec = importlib.util.spec_from_file_location("network_core", script_path)
        network_module = importlib.util.module_from_spec(spec)

        original_cwd = os.getcwd()
        original_path = sys.path.copy()

        try:
            sys.path.insert(0, str(Path(self.data_dir).absolute()))
            sys.path.insert(0, str(script_path.parent))
            os.chdir(self.data_dir)

            spec.loader.exec_module(network_module)

            network_module.OUTPUT_DIR = str(Path(self.output_dir).absolute())
            os.makedirs(network_module.OUTPUT_DIR, exist_ok=True)

            self.logger.info("Executing network analysis core...")
            network_module.main()

        finally:
            os.chdir(original_cwd)
            sys.path = original_path

    def _collect_results(self) -> Dict[str, Any]:
        """Collect analysis results."""
        output_dir = Path(self.output_dir)

        html_reports = list(output_dir.glob("*.html"))
        excel_reports = list(output_dir.glob("*Network*.xlsx"))
        csv_files = list(output_dir.glob("*.csv"))

        return {
            "status": "success",
            "output_dir": str(output_dir),
            "html_reports": [str(p) for p in html_reports],
            "excel_reports": [str(p) for p in excel_reports],
            "csv_files": [str(p) for p in csv_files],
            "total_files": len(html_reports) + len(excel_reports) + len(csv_files),
        }
