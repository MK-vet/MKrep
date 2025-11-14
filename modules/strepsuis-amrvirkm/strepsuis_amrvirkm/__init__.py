"""
StrepSuis-AMRVirKM: K-Modes Clustering of Antimicrobial Resistance and Virulence Profiles

This package provides comprehensive clustering analysis for bacterial genomic data,
specializing in antimicrobial resistance and virulence factor profiling.
"""

__version__ = "1.0.0"
__author__ = "MK-vet"
__license__ = "MIT"

from .analysis import ClusterAnalyzer

__all__ = ["ClusterAnalyzer", "__version__"]
