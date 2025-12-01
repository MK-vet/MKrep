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

# Core clustering functions from cluster_analysis_core
from .cluster_analysis_core import (
    perform_kmodes,
    bootstrap_confidence_interval,
    chi_square_analysis,
    log_odds_ratio_analysis,
    phi_correlation_matrix,
    association_rule_mining,
    multiple_correspondence_analysis,
    analyze_cluster_importance,
)

__all__ = [
    # Existing exports
    "ClusterAnalyzer",
    "Config",
    "__version__",
    # Core clustering functions
    "perform_kmodes",
    "bootstrap_confidence_interval",
    "chi_square_analysis",
    "log_odds_ratio_analysis",
    "phi_correlation_matrix",
    "association_rule_mining",
    "multiple_correspondence_analysis",
    "analyze_cluster_importance",
]
