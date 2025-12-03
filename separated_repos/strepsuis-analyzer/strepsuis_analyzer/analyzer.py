"""
StrepSuis Analyzer - Core Analysis Module

This module provides the StrepSuisAnalyzer class which is also implemented
in the standalone script StrepSuisPhyloCluster_2025_08_11.py.

For package usage, import from here.
For standalone usage, run the script directly.
"""

# Re-export the analyzer from the standalone script for package usage
import sys
import os
from pathlib import Path

# Add the parent directory to path to import the standalone script
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

try:
    from StrepSuisPhyloCluster_2025_08_11 import StrepSuisAnalyzer as _StrepSuisAnalyzer
    StrepSuisAnalyzer = _StrepSuisAnalyzer
except ImportError:
    # Fallback if standalone script is not available
    import warnings
    warnings.warn(
        "Could not import from standalone script. "
        "Please ensure StrepSuisPhyloCluster_2025_08_11.py is in the package root."
    )
    
    # Provide a stub class
    class StrepSuisAnalyzer:
        """Stub class - please use the standalone script."""
        def __init__(self, *args, **kwargs):
            raise NotImplementedError(
                "Analyzer not available. Please use StrepSuisPhyloCluster_2025_08_11.py directly."
            )

__all__ = ['StrepSuisAnalyzer']
