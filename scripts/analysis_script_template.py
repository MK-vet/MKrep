"""
MKrep Analysis Script Template

This template provides a standardized structure for all MKrep analysis scripts.
Follow this structure to ensure consistency, reproducibility, and ease of use.

Key Principles:
1. Self-contained and runnable as standalone script
2. Clear documentation and usage instructions
3. Reproducible with fixed random seeds
4. Consistent report generation (1 HTML + 1 Excel)
5. Professional appearance with shared templates
6. Interpretation included in reports
7. All text in English
"""

# =============================================================================
# SECTION 1: SCRIPT HEADER AND DOCUMENTATION
# =============================================================================

"""
[ANALYSIS NAME] - MKrep Analysis Tool

Purpose:
    [Brief description of what this analysis does]

Features:
    - [Feature 1]
    - [Feature 2]
    - [Feature 3]

Required Input Files:
    - file1.csv: [Description]
    - file2.csv: [Description]

Optional Input Files:
    - optional1.csv: [Description]

Output Files:
    - [analysis]_report.html: Interactive HTML report
    - [analysis]_Report_YYYYMMDD_HHMMSS.xlsx: Excel workbook
    - png_charts/: PNG visualizations

Usage:
    python [script_name].py

Configuration:
    Edit the CONFIG section below to customize parameters.

Reproducibility:
    Set RANDOM_SEED to a fixed value for reproducible results.

Author: MKrep Team
Version: 1.0.0
Date: 2025-01-15
License: MIT
"""

# =============================================================================
# SECTION 2: IMPORTS
# =============================================================================

# Standard library
import os
import sys
import logging
import warnings
from datetime import datetime
from pathlib import Path

# Data handling
import pandas as pd
import numpy as np

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

# Statistics and ML
from scipy import stats
from sklearn.metrics import silhouette_score
import statsmodels.api as sm

# MKrep modules
from report_templates import (
    get_html_head, get_html_scripts, create_header,
    create_section, create_interpretation_box,
    create_methodology_box, create_stats_grid,
    df_to_html_table, create_alert, create_footer,
    create_full_report
)
from excel_report_utils import ExcelReportGenerator

# Configuration
warnings.filterwarnings('ignore')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# =============================================================================
# SECTION 3: CONFIGURATION
# =============================================================================

class Config:
    """Analysis configuration parameters"""
    
    # Input/Output
    INPUT_DIR = "."
    OUTPUT_DIR = "analysis_output"
    
    # Required files
    REQUIRED_FILES = [
        "file1.csv",
        "file2.csv"
    ]
    
    # Optional files
    OPTIONAL_FILES = [
        "optional1.csv"
    ]
    
    # Analysis parameters
    RANDOM_SEED = 42
    BOOTSTRAP_ITERATIONS = 500
    FDR_ALPHA = 0.05
    
    # Report settings
    REPORT_TITLE = "[Analysis Name]"
    REPORT_SUBTITLE = "[Brief description]"
    
    # Visualization
    DPI = 150
    FIGURE_WIDTH = 12
    FIGURE_HEIGHT = 8


# =============================================================================
# SECTION 4: UTILITY FUNCTIONS
# =============================================================================

def validate_binary_data(df, filename="data"):
    """
    Validate that data is binary (0 or 1).
    
    Args:
        df: pandas DataFrame
        filename: Name for error messages
        
    Returns:
        tuple: (is_valid, error_messages)
    """
    errors = []
    
    # Check for Strain_ID column
    if 'Strain_ID' not in df.columns:
        errors.append(f"{filename}: Missing 'Strain_ID' column")
        return False, errors
    
    # Check binary values (excluding Strain_ID)
    data_cols = [col for col in df.columns if col != 'Strain_ID']
    if len(data_cols) > 0:
        for col in data_cols:
            unique_vals = df[col].unique()
            if not all(val in [0, 1, '0', '1'] for val in unique_vals):
                errors.append(f"{filename}: Column '{col}' contains non-binary values")
    
    if errors:
        return False, errors
    
    return True, []


def load_and_validate_data(config):
    """
    Load and validate all required input files.
    
    Args:
        config: Config object
        
    Returns:
        dict: Dictionary of DataFrames
    """
    logging.info("Loading and validating data files...")
    
    data = {}
    
    # Load required files
    for filename in config.REQUIRED_FILES:
        filepath = os.path.join(config.INPUT_DIR, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Required file not found: {filepath}")
        
        logging.info(f"  Loading {filename}...")
        df = pd.read_csv(filepath)
        
        # Validate
        is_valid, errors = validate_binary_data(df, filename)
        if not is_valid:
            raise ValueError(f"Data validation failed:\\n" + "\\n".join(errors))
        
        data[filename] = df
        logging.info(f"    ✓ Loaded {len(df)} strains, {len(df.columns)-1} features")
    
    # Load optional files
    for filename in config.OPTIONAL_FILES:
        filepath = os.path.join(config.INPUT_DIR, filename)
        
        if os.path.exists(filepath):
            logging.info(f"  Loading optional file {filename}...")
            df = pd.read_csv(filepath)
            data[filename] = df
    
    logging.info(f"✓ All data loaded successfully")
    return data


def setup_output_directory(config):
    """
    Create output directory and subdirectories.
    
    Args:
        config: Config object
    """
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(config.OUTPUT_DIR, "png_charts"), exist_ok=True)
    logging.info(f"Output directory: {config.OUTPUT_DIR}")


# =============================================================================
# SECTION 5: ANALYSIS FUNCTIONS
# =============================================================================

def perform_analysis(data, config):
    """
    Main analysis function.
    
    Args:
        data: Dictionary of DataFrames
        config: Config object
        
    Returns:
        dict: Analysis results
    """
    logging.info("Starting analysis...")
    
    # Set random seed for reproducibility
    np.random.seed(config.RANDOM_SEED)
    
    results = {}
    
    # TODO: Implement analysis steps here
    # Example structure:
    
    # Step 1: Data preprocessing
    logging.info("  Step 1: Data preprocessing")
    # ... preprocessing code ...
    
    # Step 2: Statistical analysis
    logging.info("  Step 2: Statistical analysis")
    # ... analysis code ...
    
    # Step 3: Visualization
    logging.info("  Step 3: Generating visualizations")
    # ... visualization code ...
    
    logging.info("✓ Analysis completed")
    return results


# =============================================================================
# SECTION 6: VISUALIZATION FUNCTIONS
# =============================================================================

def create_visualizations(results, config):
    """
    Create all visualizations and save as PNG.
    
    Args:
        results: Analysis results dictionary
        config: Config object
        
    Returns:
        dict: Dictionary of figure objects
    """
    logging.info("Creating visualizations...")
    
    figures = {}
    
    # TODO: Create visualizations
    # Example:
    # fig, ax = plt.subplots(figsize=(config.FIGURE_WIDTH, config.FIGURE_HEIGHT))
    # ... plotting code ...
    # png_path = os.path.join(config.OUTPUT_DIR, "png_charts", "figure1.png")
    # fig.savefig(png_path, dpi=config.DPI, bbox_inches='tight')
    # figures['figure1'] = fig
    
    logging.info(f"✓ Created {len(figures)} visualizations")
    return figures


# =============================================================================
# SECTION 7: REPORT GENERATION
# =============================================================================

def generate_interpretation(results, config):
    """
    Generate interpretation text for results.
    
    Args:
        results: Analysis results
        config: Config object
        
    Returns:
        str: HTML interpretation text
    """
    # TODO: Generate interpretation based on results
    # Example:
    
    interpretation = f"""
    <p><strong>Summary:</strong> [Brief summary of findings]</p>
    
    <p><strong>Key Findings:</strong></p>
    <ul>
        <li>[Finding 1]</li>
        <li>[Finding 2]</li>
        <li>[Finding 3]</li>
    </ul>
    
    <p><strong>Interpretation:</strong></p>
    <ul>
        <li>[Interpretation 1]</li>
        <li>[Interpretation 2]</li>
    </ul>
    
    <p><strong>Recommendations:</strong></p>
    <ul>
        <li>[Recommendation 1]</li>
        <li>[Recommendation 2]</li>
    </ul>
    """
    
    return interpretation


def generate_methodology_text(config):
    """
    Generate methodology description.
    
    Args:
        config: Config object
        
    Returns:
        str: HTML methodology text
    """
    methodology = f"""
    <h4>Statistical Methods</h4>
    <ul>
        <li><strong>Method 1:</strong> [Description]</li>
        <li><strong>Method 2:</strong> [Description]</li>
    </ul>
    
    <h4>Parameters</h4>
    <ul>
        <li><strong>Random Seed:</strong> {config.RANDOM_SEED}</li>
        <li><strong>Bootstrap Iterations:</strong> {config.BOOTSTRAP_ITERATIONS}</li>
        <li><strong>FDR Alpha:</strong> {config.FDR_ALPHA}</li>
    </ul>
    
    <h4>Reproducibility</h4>
    <p>This analysis is fully reproducible. To replicate:</p>
    <ol>
        <li>Use the same input data files</li>
        <li>Set random seed to {config.RANDOM_SEED}</li>
        <li>Use the same parameter values listed above</li>
    </ol>
    """
    
    return methodology


def generate_html_report(results, config):
    """
    Generate HTML report using shared templates.
    
    Args:
        results: Analysis results
        config: Config object
        
    Returns:
        str: Path to HTML report
    """
    logging.info("Generating HTML report...")
    
    # Prepare sections
    sections_data = []
    
    # Section 1: Summary
    summary_stats = {
        "Statistic 1": "Value 1",
        "Statistic 2": "Value 2",
        "Statistic 3": "Value 3"
    }
    summary_content = create_stats_grid(summary_stats)
    sections_data.append(("summary", "Summary", summary_content))
    
    # Section 2: Methodology
    methodology_content = create_methodology_box(generate_methodology_text(config))
    sections_data.append(("methodology", "Methodology", methodology_content))
    
    # Section 3: Results
    # TODO: Add results tables and visualizations
    results_content = "<p>[Results content]</p>"
    sections_data.append(("results", "Results", results_content))
    
    # Section 4: Interpretation
    interpretation_content = create_interpretation_box(generate_interpretation(results, config))
    sections_data.append(("interpretation", "Interpretation", interpretation_content))
    
    # Create full report
    analysis_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = create_full_report(
        title=config.REPORT_TITLE,
        subtitle=config.REPORT_SUBTITLE,
        sections_data=sections_data,
        analysis_date=analysis_date
    )
    
    # Save report
    report_path = os.path.join(config.OUTPUT_DIR, "analysis_report.html")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logging.info(f"✓ HTML report saved: {report_path}")
    return report_path


def generate_excel_report(results, config):
    """
    Generate Excel report using shared utilities.
    
    Args:
        results: Analysis results
        config: Config object
        
    Returns:
        str: Path to Excel report
    """
    logging.info("Generating Excel report...")
    
    # Initialize Excel generator
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_filename = f"analysis_Report_{timestamp}.xlsx"
    excel_path = os.path.join(config.OUTPUT_DIR, excel_filename)
    
    excel_gen = ExcelReportGenerator(excel_path)
    
    # Add metadata
    metadata = {
        "Analysis Script": "[script_name].py",
        "Analysis Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Output Folder": config.OUTPUT_DIR,
        "Random Seed": config.RANDOM_SEED,
        "Bootstrap Iterations": config.BOOTSTRAP_ITERATIONS,
        "FDR Alpha": config.FDR_ALPHA
    }
    excel_gen.add_metadata_sheet(metadata)
    
    # Add methodology
    methodology_text = generate_methodology_text(config)
    excel_gen.add_methodology_sheet(methodology_text)
    
    # Add data sheets
    # TODO: Add result tables
    # excel_gen.add_data_sheet(df, "Sheet_Name", "Description")
    
    # Add chart index
    png_dir = os.path.join(config.OUTPUT_DIR, "png_charts")
    excel_gen.add_chart_index(png_dir)
    
    # Save workbook
    excel_gen.save()
    
    logging.info(f"✓ Excel report saved: {excel_path}")
    return excel_path


# =============================================================================
# SECTION 8: MAIN FUNCTION
# =============================================================================

def main():
    """
    Main execution function.
    """
    print("=" * 80)
    print(f"{Config.REPORT_TITLE}")
    print("=" * 80)
    print()
    
    try:
        # Setup
        config = Config()
        setup_output_directory(config)
        
        # Load data
        data = load_and_validate_data(config)
        
        # Run analysis
        results = perform_analysis(data, config)
        
        # Create visualizations
        figures = create_visualizations(results, config)
        
        # Generate reports
        html_path = generate_html_report(results, config)
        excel_path = generate_excel_report(results, config)
        
        # Summary
        print()
        print("=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
        print()
        print("Output files:")
        print(f"  HTML report:  {html_path}")
        print(f"  Excel report: {excel_path}")
        print(f"  PNG charts:   {os.path.join(config.OUTPUT_DIR, 'png_charts/')}")
        print()
        print("✓ All reports generated successfully")
        print()
        
    except Exception as e:
        logging.error(f"Analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


# =============================================================================
# SECTION 9: SCRIPT EXECUTION
# =============================================================================

if __name__ == "__main__":
    main()
