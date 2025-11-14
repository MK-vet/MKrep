"""
StrepSuis-GenPhen: Interactive Platform for Integrated Genomic-Phenotypic Analysis

Integrative genomic-phenotypic analysis platform for Streptococcus suis

Author: MK-vet
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "MK-vet"
__license__ = "MIT"

from .analyzer import GenPhenAnalyzer
from .config import Config

__all__ = [
    "GenPhenAnalyzer",
    "Config",
    "__version__"
]
