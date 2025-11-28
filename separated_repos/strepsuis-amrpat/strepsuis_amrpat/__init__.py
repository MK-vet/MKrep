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
from .config import Config, AnalysisConfig
from .validation_utils import validate_input_data, validate_mdr_output, get_data_summary
from .synthetic_data_utils import (
    generate_synthetic_amr_data,
    generate_cooccurrence_data,
    run_synthetic_smoke_test,
)

__all__ = [
    "MDRAnalyzer",
    "Config",
    "AnalysisConfig",
    "validate_input_data",
    "validate_mdr_output",
    "get_data_summary",
    "generate_synthetic_amr_data",
    "generate_cooccurrence_data",
    "run_synthetic_smoke_test",
    "__version__",
]
