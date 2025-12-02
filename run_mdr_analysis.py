#!/usr/bin/env python3
"""
Wrapper script to run MDR analysis with non-interactive mode.
This script modifies the setup_environment function to accept a default CSV path.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Monkey-patch the setup_environment function before importing
def patched_setup_environment():
    """Modified version that accepts a default CSV path."""
    import logging
    
    # Create output directories
    try:
        os.makedirs("output", exist_ok=True)
        os.makedirs("output/figures", exist_ok=True)
        os.makedirs("output/data", exist_ok=True)
    except Exception as e:
        logging.error(f"Could not create output directories: {e}")
        raise

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        handlers=[
            logging.FileHandler(os.path.join("output", "analysis_log.txt")),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Use command-line argument or default to merged file in data directory
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        csv_path = "data/merged_resistance_data.csv"
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File not found: {csv_path}")
    
    logging.info(f"Using CSV file: {csv_path}")
    return csv_path

# Import and patch the module
from src import mdr_analysis
mdr_analysis.setup_environment = patched_setup_environment

# Run the main function
if __name__ == "__main__":
    mdr_analysis.main()
