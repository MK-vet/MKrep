#!/usr/bin/env python3
"""
Upgrade All StrepSuis Modules to Software X Publication Standards

This script systematically upgrades all 5 modules to publication standards.
"""

import os
import sys
import json
import subprocess
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PublicationStandardsUpgrader:
    """Upgrades StrepSuis modules to Software X publication standards."""
    
    CALC_MODULES = [
        'strepsuis-mdr',
        'strepsuis-amrvirkm', 
        'strepsuis-genphennet',
        'strepsuis-phylotrait'
    ]
    
    STREAMLIT_MODULE = 'strepsuis-analyzer'
    
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.modules_dir = self.base_dir
        
        if not self.modules_dir.exists():
            raise ValueError(f"Directory {self.modules_dir} does not exist")
        
        logger.info(f"Initialized upgrader in {self.modules_dir}")
    
    def upgrade_module(self, module_name: str) -> bool:
        """Upgrade a single module to publication standards."""
        logger.info(f"\n{'='*60}")
        logger.info(f"Upgrading {module_name} to publication standards")
        logger.info(f"{'='*60}")
        
        module_path = self.modules_dir / module_name
        if not module_path.exists():
            logger.error(f"Module {module_name} not found at {module_path}")
            return False
        
        try:
            # Phase 1: Directory structure
            self._create_directory_structure(module_path)
            
            # Phase 2: Synthetic datasets
            self._create_basic_synthetic_datasets(module_path / "synthetic_data")
            
            # Phase 3: Deployment artifacts (for calc modules)
            if module_name in self.CALC_MODULES:
                self._create_colab_notebook(module_path, module_name)
            
            logger.info(f"✓ Successfully upgraded {module_name}")
            return True
            
        except Exception as e:
            logger.error(f"✗ Failed to upgrade {module_name}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _create_directory_structure(self, module_path: Path):
        """Create required directory structure."""
        logger.info("  Creating directory structure...")
        
        directories = [
            'tests/reports',
            'tests/performance',
            'synthetic_data',
            'validation_results',
            'notebooks'
        ]
        
        for dir_name in directories:
            dir_path = module_path / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
        
        logger.info("  ✓ Directory structure created")
    
    def _create_basic_synthetic_datasets(self, synthetic_dir: Path):
        """Create basic synthetic datasets."""
        logger.info("    Generating synthetic datasets...")
        
        # Check if already exist
        if (synthetic_dir / "clean_dataset.csv").exists():
            logger.info("    Synthetic datasets already exist, skipping")
            return
        
        np.random.seed(42)
        
        n_samples = 200
        n_features = 20
        
        # Clean dataset
        clean_data = np.random.binomial(1, 0.3, (n_samples, n_features))
        clean_df = pd.DataFrame(
            clean_data,
            columns=[f"Feature_{i+1}" for i in range(n_features)]
        )
        clean_df.insert(0, 'Strain_ID', [f"Strain_{i+1}" for i in range(n_samples)])
        clean_df.to_csv(synthetic_dir / "clean_dataset.csv", index=False)
        
        # Noisy dataset
        noisy_data = clean_data.copy()
        noise_mask = np.random.rand(*noisy_data.shape) < 0.1
        noisy_data[noise_mask] = 1 - noisy_data[noise_mask]
        noisy_df = pd.DataFrame(
            noisy_data,
            columns=[f"Feature_{i+1}" for i in range(n_features)]
        )
        noisy_df.insert(0, 'Strain_ID', [f"Strain_{i+1}" for i in range(n_samples)])
        noisy_df.to_csv(synthetic_dir / "noisy_dataset.csv", index=False)
        
        # Adversarial dataset
        adversarial_data = np.random.binomial(1, 0.05, (n_samples, n_features))
        adversarial_data[:, 1] = adversarial_data[:, 0]
        adversarial_df = pd.DataFrame(
            adversarial_data,
            columns=[f"Feature_{i+1}" for i in range(n_features)]
        )
        adversarial_df.insert(0, 'Strain_ID', [f"Strain_{i+1}" for i in range(n_samples)])
        adversarial_df.to_csv(synthetic_dir / "adversarial_dataset.csv", index=False)
        
        # Metadata
        metadata = {
            'created': str(pd.Timestamp.now()),
            'n_samples': n_samples,
            'n_features': n_features,
            'datasets': {
                'clean': 'No noise, clear patterns',
                'noisy': '10% random bit flips',
                'adversarial': 'Extreme imbalance (5% prevalence), perfect correlations'
            },
            'ground_truth': {
                'clean_prevalence': float(clean_data.mean()),
                'noisy_prevalence': float(noisy_data.mean()),
                'adversarial_prevalence': float(adversarial_data.mean())
            }
        }
        
        with open(synthetic_dir / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"    ✓ Created synthetic datasets in {synthetic_dir}")
    
    def _create_colab_notebook(self, module_path: Path, module_name: str):
        """Create Google Colab notebook."""
        notebook_path = module_path / "notebooks" / f"{module_name}_colab_demo.ipynb"
        
        if notebook_path.exists():
            logger.info(f"    Colab notebook already exists")
            return
        
        logger.info(f"    Creating Colab notebook")
        
        cli_command = module_name
        
        notebook = {
            "nbformat": 4,
            "nbformat_minor": 0,
            "metadata": {
                "colab": {
                    "name": f"{module_name} Demonstration",
                    "provenance": []
                },
                "kernelspec": {
                    "name": "python3",
                    "display_name": "Python 3"
                }
            },
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        f"# {module_name} - Google Colab Demonstration\n\n",
                        f"This notebook demonstrates the {module_name} package."
                    ]
                },
                {
                    "cell_type": "code",
                    "metadata": {},
                    "source": [
                        f"!pip install git+https://github.com/MK-vet/{module_name}.git"
                    ],
                    "execution_count": None,
                    "outputs": []
                },
                {
                    "cell_type": "code",
                    "metadata": {},
                    "source": [
                        f"!{cli_command} --version"
                    ],
                    "execution_count": None,
                    "outputs": []
                },
                {
                    "cell_type": "code",
                    "metadata": {},
                    "source": [
                        f"!{cli_command} --help"
                    ],
                    "execution_count": None,
                    "outputs": []
                }
            ]
        }
        
        with open(notebook_path, 'w') as f:
            json.dump(notebook, f, indent=2)
        
        logger.info(f"    ✓ Created Colab notebook")
    
    def upgrade_all_modules(self) -> Dict[str, bool]:
        """Upgrade all modules."""
        results = {}
        
        all_modules = self.CALC_MODULES + [self.STREAMLIT_MODULE]
        
        for module_name in all_modules:
            success = self.upgrade_module(module_name)
            results[module_name] = success
        
        return results
    
    def generate_summary_report(self, results: Dict[str, bool]):
        """Generate summary report."""
        from datetime import datetime
        
        report_path = self.modules_dir / "PUBLICATION_UPGRADE_SUMMARY.md"
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        lines = [
            f"# Publication Standards Upgrade Summary\n",
            f"\n**Generated:** {timestamp}\n",
            "\n## Upgrade Results\n\n"
        ]
        
        for module_name, success in results.items():
            status = "✓ SUCCESS" if success else "✗ FAILED"
            lines.append(f"- **{module_name}**: {status}\n")
        
        all_success = all(results.values())
        lines.append(f"\n**Status:** {'✓ All modules upgraded' if all_success else '✗ Some failed'}\n")
        
        with open(report_path, 'w') as f:
            f.writelines(lines)
        
        logger.info(f"\nSummary report saved to {report_path}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Upgrade StrepSuis modules to Software X publication standards"
    )
    parser.add_argument(
        'module',
        nargs='?',
        help='Module name to upgrade (default: all modules)'
    )
    
    args = parser.parse_args()
    
    script_dir = Path(__file__).parent
    
    upgrader = PublicationStandardsUpgrader(script_dir)
    
    if args.module:
        success = upgrader.upgrade_module(args.module)
        sys.exit(0 if success else 1)
    else:
        results = upgrader.upgrade_all_modules()
        upgrader.generate_summary_report(results)
        
        all_success = all(results.values())
        sys.exit(0 if all_success else 1)


if __name__ == "__main__":
    main()
