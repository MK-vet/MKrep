"""
StrepSuis-AMRVirKM: K-Modes Clustering of Antimicrobial Resistance and Virulence Profiles

A professional bioinformatics package for comprehensive clustering analysis of 
antimicrobial resistance and virulence factor profiles in bacterial genomics.

Author: MK-vet
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "MK-vet"
__license__ = "MIT"

from .analyzer import ClusterAnalyzer
from .config import Config

__all__ = [
    "ClusterAnalyzer",
    "Config",
    "__version__"
]
