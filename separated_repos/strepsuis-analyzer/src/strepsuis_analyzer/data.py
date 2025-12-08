"""
Data loading utilities for genomic and phenotypic datasets.

This module provides functions to load CSV data files and phylogenetic trees
from the data directory. All functions include proper error handling and
return appropriate types.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Optional
import warnings


def load_data(data_dir: Path) -> Dict[str, pd.DataFrame]:
    """
    Load all CSV data files from the data directory.
    
    This function loads standard genomic and phenotypic data files including:
    - AMR_genes.csv: Antimicrobial resistance genes
    - MIC.csv: Minimum inhibitory concentrations
    - Virulence.csv: Virulence factors
    - MLST.csv: Multi-locus sequence typing profiles
    - Serotype.csv: Serotype information
    - MGE.csv: Mobile genetic elements
    - Plasmid.csv: Plasmid information
    
    Args:
        data_dir: Path to the directory containing data files.
        
    Returns:
        Dictionary mapping data type to DataFrame. Keys are:
        'AMR', 'MIC', 'Virulence', 'MLST', 'Serotype', 'MGE', 'Plasmid'.
        Each value is a pandas DataFrame with cleaned column names.
        
        If a file is not found, the corresponding DataFrame will be empty
        (but the key will still exist in the dictionary).
        
    Examples:
        >>> from pathlib import Path
        >>> data = load_data(Path('./data'))
        >>> 'AMR' in data
        True
        >>> isinstance(data['AMR'], pd.DataFrame)
        True
        
    Note:
        Column names are automatically stripped of leading/trailing whitespace.
        Missing files generate warnings but do not raise exceptions, allowing
        partial data loading to succeed.
    """
    data_files = {
        'AMR': 'AMR_genes.csv',
        'MIC': 'MIC.csv',
        'Virulence': 'Virulence.csv',
        'MLST': 'MLST.csv',
        'Serotype': 'Serotype.csv',
        'MGE': 'MGE.csv',
        'Plasmid': 'Plasmid.csv'
    }
    
    data = {}
    for key, filename in data_files.items():
        filepath = data_dir / filename
        try:
            df = pd.read_csv(filepath)
            # Clean column names
            df.columns = df.columns.str.strip()
            data[key] = df
        except FileNotFoundError:
            warnings.warn(
                f"Data file not found: {filename}. "
                f"Expected path: {filepath}",
                UserWarning,
                stacklevel=2
            )
            data[key] = pd.DataFrame()
        except Exception as e:
            warnings.warn(
                f"Error loading {filename}: {str(e)}. "
                f"Returning empty DataFrame.",
                UserWarning,
                stacklevel=2
            )
            data[key] = pd.DataFrame()
    
    return data


def load_phylogenetic_tree(tree_file: Path) -> Optional[str]:
    """
    Load the phylogenetic tree in Newick format.
    
    Reads a tree file in Newick format and returns the tree string with
    leading/trailing whitespace removed.
    
    Args:
        tree_file: Path to the Newick format tree file.
        
    Returns:
        Tree string in Newick format, or None if the file is not found
        or cannot be read.
        
    Examples:
        >>> from pathlib import Path
        >>> tree = load_phylogenetic_tree(Path('./data/tree.newick'))
        >>> tree is None or isinstance(tree, str)
        True
        >>> # If tree exists, it should end with semicolon
        >>> tree is None or tree.endswith(';')
        True
        
    Note:
        If the file is not found, a warning is issued and None is returned.
        This allows the application to continue running without tree data.
    """
    try:
        with open(tree_file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        warnings.warn(
            f"Phylogenetic tree file not found: {tree_file}",
            UserWarning,
            stacklevel=2
        )
        return None
    except Exception as e:
        warnings.warn(
            f"Error loading phylogenetic tree: {str(e)}",
            UserWarning,
            stacklevel=2
        )
        return None
