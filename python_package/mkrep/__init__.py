"""MKrep package - Microbial genomics analysis tools."""

__version__ = "1.0.0"
__author__ = "MK-vet"
__email__ = "contact@example.com"

from mkrep.analysis.cluster_analyzer import ClusterAnalyzer
from mkrep.analysis.mdr_analyzer import MDRAnalyzer
from mkrep.analysis.network_analyzer import NetworkAnalyzer
from mkrep.analysis.phylo_analyzer import PhyloAnalyzer
from mkrep.analysis.strepsuis_analyzer import StrepSuisAnalyzer

__all__ = [
    "ClusterAnalyzer",
    "MDRAnalyzer",
    "NetworkAnalyzer",
    "PhyloAnalyzer",
    "StrepSuisAnalyzer",
]
