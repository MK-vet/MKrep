"""
Main analyzer module for StrepSuis-PhyloTrait
"""

import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from .config import Config


class PhyloTraitAnalyzer:
    """
    Main analyzer class for phylogenetic and binary trait analysis.

    Performs:
    - Tree-aware clustering with evolutionary metrics
    - Faith's Phylogenetic Diversity calculations
    - Binary trait analysis for AMR and virulence factors
    - Interactive visualization with DataTables and Plotly
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
                "tree_file",
                "data_dir",
                "output_dir",
                "max_clusters",
                "min_clusters",
                "bootstrap_iterations",
                "fdr_alpha",
                "verbose",
            ]:
                if key in kwargs:
                    config_params[key] = kwargs.pop(key)
            config = Config(**config_params)

        self.config = config
        self.tree_file = getattr(config, "tree_file", None)
        self.data_dir = config.data_dir
        self.output_dir = config.output_dir
        self.logger = logging.getLogger(__name__)
        self.results: Optional[Dict[str, Any]] = None

    def run(self) -> Dict[str, Any]:
        """
        Run the complete phylogenetic trait analysis pipeline.

        Returns:
            Dictionary containing analysis results
        """
        self.logger.info("Starting phylogenetic trait analysis pipeline...")

        # Validate required files
        data_dir = Path(self.data_dir)

        if not data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {data_dir}")

        # Check for tree file
        if self.tree_file:
            tree_path = Path(self.tree_file)
            if not tree_path.exists():
                # Try in data directory
                tree_path = data_dir / self.tree_file
                if not tree_path.exists():
                    raise FileNotFoundError(f"Tree file not found: {self.tree_file}")
        else:
            # Look for tree file in data directory
            tree_files = (
                list(data_dir.glob("*.newick"))
                + list(data_dir.glob("*.nwk"))
                + list(data_dir.glob("*.tree"))
            )
            if tree_files:
                tree_path = tree_files[0]
                self.logger.info(f"Using tree file: {tree_path}")
            else:
                raise FileNotFoundError(
                    "No tree file found. Please provide a .newick, .nwk, or .tree file"
                )

        # Check data files
        required_files = ["MIC.csv", "AMR_genes.csv", "Virulence.csv"]
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
        """Execute the core phylogenetic analysis."""
        script_path = Path(__file__).parent / "phylo_analysis_core.py"

        if not script_path.exists():
            raise FileNotFoundError(f"Core analysis script not found: {script_path}")

        import importlib.util

        spec = importlib.util.spec_from_file_location("phylo_core", script_path)
        phylo_module = importlib.util.module_from_spec(spec)

        original_cwd = os.getcwd()
        original_path = sys.path.copy()

        try:
            sys.path.insert(0, str(Path(self.data_dir).absolute()))
            sys.path.insert(0, str(script_path.parent))
            os.chdir(self.data_dir)

            spec.loader.exec_module(phylo_module)

            phylo_module.OUTPUT_DIR = str(Path(self.output_dir).absolute())
            os.makedirs(phylo_module.OUTPUT_DIR, exist_ok=True)

            self.logger.info("Executing phylogenetic analysis core...")
            phylo_module.main()

        finally:
            os.chdir(original_cwd)
            sys.path = original_path

    def _collect_results(self) -> Dict[str, Any]:
        """Collect analysis results."""
        output_dir = Path(self.output_dir)

        html_reports = list(output_dir.glob("*.html"))
        excel_reports = list(output_dir.glob("*Phylo*.xlsx"))
        csv_files = list(output_dir.glob("*.csv"))

        return {
            "status": "success",
            "output_dir": str(output_dir),
            "html_reports": [str(p) for p in html_reports],
            "excel_reports": [str(p) for p in excel_reports],
            "csv_files": [str(p) for p in csv_files],
            "total_files": len(html_reports) + len(excel_reports) + len(csv_files),
        }
