"""
StrepSuis-PhyloTrait: Integrated Phylogenetic and Binary Trait Analysis

Complete phylogenetic and binary trait analysis with tree-aware clustering

Author: MK-vet
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "MK-vet"
__license__ = "MIT"

from .analyzer import PhyloAnalyzer
from .config import Config

__all__ = [
    "PhyloAnalyzer",
    "Config",
    "__version__"
]
