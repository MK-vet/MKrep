"""
Configuration module

Handles all configuration parameters for analysis using Pydantic for validation.
"""

import os
from dataclasses import dataclass
from typing import List, Optional

try:
    from pydantic import BaseModel, Field, field_validator
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False


@dataclass
class Config:
    """Configuration for analysis (dataclass version for backward compatibility)."""

    # Directories
    data_dir: str = "."
    output_dir: str = "./output"

    # Statistical parameters
    bootstrap_iterations: int = 500
    fdr_alpha: float = 0.05
    random_seed: int = 42

    # Reporting parameters
    generate_html: bool = True
    generate_excel: bool = True
    save_png_charts: bool = True
    dpi: int = 150

    # Parallel processing
    n_jobs: int = -1

    def __post_init__(self):
        """Validate configuration after initialization."""
        if not os.path.exists(self.data_dir):
            raise ValueError(f"Data directory does not exist: {self.data_dir}")

        os.makedirs(self.output_dir, exist_ok=True)

        if not 0 < self.fdr_alpha < 1:
            raise ValueError("fdr_alpha must be between 0 and 1")

        if self.bootstrap_iterations < 100:
            raise ValueError("bootstrap_iterations should be at least 100")

    @classmethod
    def from_dict(cls, config_dict: dict) -> "Config":
        """Create Config from dictionary."""
        return cls(**{k: v for k, v in config_dict.items() if k in cls.__dataclass_fields__})


if PYDANTIC_AVAILABLE:
    class AnalysisConfig(BaseModel):
        """
        Pydantic-based configuration model for analysis parameters.
        
        Provides runtime validation and type checking for all analysis settings.
        Use this class for new code; Config dataclass is maintained for backward compatibility.
        
        Attributes:
            n_bootstrap: Number of bootstrap iterations (min 1000, max 100000, default 5000)
            confidence_level: Confidence level for CIs (default 0.95)
            fdr_alpha: False Discovery Rate threshold (default 0.05)
            max_missing_pct: Maximum allowed missing value percentage (default 0.2)
            random_seed: Random seed for reproducibility (default 42)
            min_support: Minimum support for association rules (default 0.1)
            lift_threshold: Minimum lift for association rules (default 1.0)
            output_dir: Output directory path
            generate_html: Whether to generate HTML reports
            generate_excel: Whether to generate Excel reports
            save_png_charts: Whether to save PNG charts
            dpi: DPI for saved charts (default 150)
        """
        
        n_bootstrap: int = Field(default=5000, ge=1000, le=100000, 
                                  description="Number of bootstrap iterations")
        confidence_level: float = Field(default=0.95, gt=0, lt=1,
                                         description="Confidence level for intervals")
        fdr_alpha: float = Field(default=0.05, gt=0, lt=1,
                                  description="FDR significance threshold")
        max_missing_pct: float = Field(default=0.2, ge=0, le=1,
                                        description="Maximum allowed missing value percentage")
        random_seed: int = Field(default=42, ge=0,
                                  description="Random seed for reproducibility")
        min_support: float = Field(default=0.1, gt=0, lt=1,
                                    description="Minimum support for association rules")
        lift_threshold: float = Field(default=1.0, ge=0,
                                       description="Minimum lift for association rules")
        output_dir: str = Field(default="./output",
                                description="Output directory path")
        generate_html: bool = Field(default=True,
                                     description="Generate HTML reports")
        generate_excel: bool = Field(default=True,
                                      description="Generate Excel reports")
        save_png_charts: bool = Field(default=True,
                                       description="Save PNG charts")
        dpi: int = Field(default=150, ge=72, le=600,
                         description="DPI for saved charts")
        
        @field_validator("confidence_level")
        @classmethod
        def validate_ci(cls, v: float) -> float:
            """Validate confidence level is in typical range."""
            if not 0.9 <= v <= 0.99:
                import warnings
                warnings.warn(
                    f"Confidence level {v} is unusual. "
                    "Typical values are between 0.90 and 0.99.",
                    UserWarning
                )
            return v
        
        @field_validator("output_dir")
        @classmethod
        def ensure_output_dir(cls, v: str) -> str:
            """Ensure output directory exists."""
            os.makedirs(v, exist_ok=True)
            return v
        
        model_config = {"validate_assignment": True}
        
        def to_config(self) -> Config:
            """Convert to legacy Config dataclass."""
            return Config(
                output_dir=self.output_dir,
                bootstrap_iterations=self.n_bootstrap,
                fdr_alpha=self.fdr_alpha,
                random_seed=self.random_seed,
                generate_html=self.generate_html,
                generate_excel=self.generate_excel,
                save_png_charts=self.save_png_charts,
                dpi=self.dpi,
            )
else:
    # Fallback: use dataclass if Pydantic is not available
    AnalysisConfig = Config  # type: ignore
