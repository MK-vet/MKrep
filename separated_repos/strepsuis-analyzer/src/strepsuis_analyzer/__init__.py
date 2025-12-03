"""
StrepSuisAnalyzer: Interactive Streamlit Application for Comprehensive Analysis.

This package provides interactive analysis tools for Streptococcus suis genomic
and phenotypic data, including statistical analysis, phylogenetic analysis,
visualization, and reporting capabilities.
"""

__version__ = "1.0.0"
__author__ = "MK-vet"
__email__ = "support@strepsuis-suite.org"

from strepsuis_analyzer.data_validator import DataValidator
from strepsuis_analyzer.statistical_analysis import StatisticalAnalyzer
from strepsuis_analyzer.phylogenetic_utils import PhylogeneticAnalyzer
from strepsuis_analyzer.visualization import Visualizer
from strepsuis_analyzer.report_generator import ReportGenerator

# Import new modules for core functionality
from strepsuis_analyzer import stats
from strepsuis_analyzer import data

__all__ = [
    "DataValidator",
    "StatisticalAnalyzer",
    "PhylogeneticAnalyzer",
    "Visualizer",
    "ReportGenerator",
    "stats",
    "data",
]
