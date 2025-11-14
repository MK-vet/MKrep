"""
StrepSuis-AMRPat: Automated Detection of Antimicrobial Resistance Patterns

Advanced multidrug resistance pattern detection with bootstrap resampling and network analysis

Author: MK-vet
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "MK-vet"
__license__ = "MIT"

from .analyzer import MDRAnalyzer
from .config import Config

__all__ = [
    "MDRAnalyzer",
    "Config",
    "__version__"
]
