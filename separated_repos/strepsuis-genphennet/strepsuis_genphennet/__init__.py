"""
StrepSuis-GenPhenNet: Network-Based Integration of Genome-Phenome Data

Statistical network analysis for genomic-phenotypic associations

Author: MK-vet
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "MK-vet"
__license__ = "MIT"

from .analyzer import NetworkAnalyzer
from .config import Config

__all__ = ["NetworkAnalyzer", "Config", "__version__"]
