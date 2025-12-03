"""
Configuration settings for StrepSuis Analyzer
"""

# Default analysis parameters
DEFAULT_CONFIG = {
    'random_state': 42,
    'fdr_alpha': 0.05,
    'n_mca_components': 2,
    'clustering_method': 'ward',
    'distance_metric': 'jaccard',
    'min_support': 0.1,
    'min_confidence': 0.5,
}

# File patterns
DATA_FILE_PATTERNS = [
    'AMR_genes.csv',
    'Virulence.csv',
    'MGE.csv',
    'Plasmid.csv',
    'MLST.csv',
    'Serotype.csv',
]

TREE_FILE_PATTERN = 'Snp_tree.newick'

# Output file names
OUTPUT_FILES = {
    'html_report': 'analysis_report.html',
    'excel_report': 'analysis_results.xlsx',
    'clustered_data': 'clustered_data.csv',
    'trait_associations': 'trait_associations.csv',
}

# Visualization settings
PLOT_CONFIG = {
    'dpi': 150,
    'figure_format': 'png',
    'plotly_template': 'plotly_white',
    'color_palette': 'viridis',
}

# Bootstrap settings
BOOTSTRAP_CONFIG = {
    'n_iterations': 1000,
    'confidence_level': 0.95,
}
