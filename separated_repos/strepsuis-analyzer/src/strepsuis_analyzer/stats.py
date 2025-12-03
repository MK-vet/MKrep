"""
Statistical functions for genomic and phenotypic data analysis.

This module provides core statistical calculations for diversity indices,
distance metrics, prevalence, and correlation analysis of binary and
continuous data.

All functions are deterministic and use strict type hints for clarity and
type safety. Where applicable, functions accept a random_state parameter
for API consistency and future extensions.
"""

import numpy as np
import pandas as pd
from typing import Union, Literal
from scipy.spatial.distance import pdist, squareform


# Type aliases for clarity
DistanceMetric = Literal['jaccard', 'hamming']


def calculate_shannon_diversity(
    data: np.ndarray, 
    random_state: int = 42
) -> float:
    """
    Calculate Shannon diversity index for a binary presence/absence matrix.
    
    The Shannon diversity index is computed as:
        H = -Σ(p_i * log(p_i))
    
    where p_i is the proportion of presence for feature i across all samples.
    
    Args:
        data: Binary numpy array (samples x features). Values should be 0 or 1.
        random_state: Random seed for reproducibility (reserved for API consistency).
                     Currently unused as this calculation is deterministic.
        
    Returns:
        Shannon diversity index as a float. Returns 0.0 for empty data or data
        with no variance.
        
    Mathematical Properties:
        - H >= 0 (non-negative)
        - H = 0 when all features have the same presence/absence pattern
        - H increases with evenness of feature distribution
        
    Examples:
        >>> data = np.array([[1, 1, 0, 0], [0, 0, 1, 1]])
        >>> shannon = calculate_shannon_diversity(data)
        >>> shannon > 0
        True
        
    Note:
        The random_state parameter is included for API consistency with other
        functions but is not currently used as this calculation is deterministic.
    """
    # Note: random_state is reserved for future extensions
    # Current implementation is deterministic
    _ = random_state  # Acknowledge parameter for API consistency
    
    if data.size == 0:
        return 0.0
    
    # Calculate proportion of presence for each feature
    proportions = np.mean(data, axis=0)
    
    # Filter out zero proportions to avoid log(0)
    proportions = proportions[proportions > 0]
    
    if len(proportions) == 0:
        return 0.0
    
    # Calculate Shannon index
    shannon = -np.sum(proportions * np.log(proportions))
    
    return float(shannon)


def calculate_simpson_diversity(
    data: np.ndarray, 
    random_state: int = 42
) -> float:
    """
    Calculate Simpson diversity index (1 - D) for a binary presence/absence matrix.
    
    The Simpson diversity index is computed as:
        D = Σ(p_i^2)
        Simpson = 1 - D
    
    where p_i is the proportion of presence for feature i across all samples.
    
    Args:
        data: Binary numpy array (samples x features). Values should be 0 or 1.
        random_state: Random seed for reproducibility (reserved for API consistency).
                     Currently unused as this calculation is deterministic.
        
    Returns:
        Simpson diversity index (1-D) as a float. Can be negative when the sum
        of squared proportions exceeds 1.
        
    Mathematical Properties:
        - Higher values indicate greater diversity
        - Range: typically [-n+1, 1] where n is the number of features
        - Simpson = 1 when features are maximally even
        
    Examples:
        >>> data = np.array([[1, 0], [0, 1]])
        >>> simpson = calculate_simpson_diversity(data)
        >>> isinstance(simpson, float)
        True
        
    Note:
        The random_state parameter is included for API consistency with other
        functions but is not currently used as this calculation is deterministic.
    """
    # Note: random_state is reserved for future extensions
    # Current implementation is deterministic
    _ = random_state  # Acknowledge parameter for API consistency
    
    if data.size == 0:
        return 0.0
    
    # Calculate proportion of presence for each feature
    proportions = np.mean(data, axis=0)
    
    # Calculate Simpson index (1 - D)
    simpson = 1.0 - np.sum(proportions ** 2)
    
    return float(simpson)


def calculate_jaccard_distance(x: np.ndarray, y: np.ndarray) -> float:
    """
    Calculate Jaccard distance between two binary vectors.
    
    The Jaccard distance is computed as:
        Distance = 1 - (intersection / union)
    
    where intersection is the count of positions where both vectors are 1,
    and union is the count of positions where at least one vector is 1.
    
    Args:
        x: First binary vector (1-dimensional numpy array).
        y: Second binary vector (1-dimensional numpy array).
        
    Returns:
        Jaccard distance as a float in the range [0, 1].
        Returns 0.0 when both vectors have no set bits (union is 0).
        Returns 1.0 for empty vectors.
        
    Mathematical Properties:
        - Symmetric: d(x,y) = d(y,x)
        - Range: [0, 1]
        - d(x,x) = 0 (distance to self is zero)
        - d(x,y) = 1 when vectors have no overlap
        
    Examples:
        >>> x = np.array([1, 1, 0, 0])
        >>> y = np.array([1, 0, 1, 0])
        >>> dist = calculate_jaccard_distance(x, y)
        >>> 0 <= dist <= 1
        True
        
    Raises:
        No explicit exceptions raised. Empty vectors return 1.0.
    """
    if len(x) == 0 or len(y) == 0:
        return 1.0
    
    intersection = np.sum(np.logical_and(x, y))
    union = np.sum(np.logical_or(x, y))
    
    if union == 0:
        return 0.0
    
    jaccard_sim = intersection / union
    return float(1.0 - jaccard_sim)


def calculate_hamming_distance(x: np.ndarray, y: np.ndarray) -> float:
    """
    Calculate normalized Hamming distance between two binary vectors.
    
    The normalized Hamming distance is computed as:
        Distance = (number of differing positions) / (total positions)
    
    Args:
        x: First binary vector (1-dimensional numpy array).
        y: Second binary vector (1-dimensional numpy array).
        
    Returns:
        Normalized Hamming distance as a float in the range [0, 1].
        Returns 1.0 for empty vectors.
        
    Mathematical Properties:
        - Symmetric: d(x,y) = d(y,x)
        - Range: [0, 1]
        - d(x,x) = 0 (distance to self is zero)
        - d(x,y) = 1 when all positions differ
        
    Examples:
        >>> x = np.array([1, 0, 1, 0])
        >>> y = np.array([1, 1, 1, 0])
        >>> dist = calculate_hamming_distance(x, y)
        >>> dist == 0.25  # 1 position differs out of 4
        True
        
    Raises:
        ValueError: If vectors have different lengths.
    """
    if len(x) == 0 or len(y) == 0:
        return 1.0
    
    if len(x) != len(y):
        raise ValueError("Vectors must have the same length")
    
    distance = np.sum(x != y) / len(x)
    return float(distance)


def calculate_pairwise_distances(
    data: np.ndarray, 
    metric: DistanceMetric = 'jaccard'
) -> np.ndarray:
    """
    Calculate pairwise distance matrix for binary data.
    
    This function efficiently computes all pairwise distances between samples
    using scipy's optimized implementations. For n samples, it computes n*(n-1)/2
    unique distances and constructs a symmetric matrix.
    
    Args:
        data: Binary numpy array (samples x features). Each row is a sample.
        metric: Distance metric to use. Either 'jaccard' or 'hamming'.
        
    Returns:
        Symmetric distance matrix as a 2D numpy array with shape (n_samples, n_samples).
        The diagonal contains zeros (distance to self).
        
    Mathematical Properties:
        - Symmetric: distances[i, j] == distances[j, i]
        - Diagonal is zero: distances[i, i] == 0
        - All values in range [0, 1]
        
    Performance:
        Uses scipy.spatial.distance.pdist for O(n²) complexity with optimized
        C implementations, significantly faster than pure Python loops.
        
    Examples:
        >>> data = np.array([[1, 0, 1], [0, 1, 0], [1, 1, 1]])
        >>> distances = calculate_pairwise_distances(data, metric='jaccard')
        >>> distances.shape == (3, 3)
        True
        >>> np.allclose(distances, distances.T)  # Symmetric
        True
        >>> np.allclose(np.diag(distances), 0)  # Diagonal is zero
        True
        
    Raises:
        ValueError: If metric is not 'jaccard' or 'hamming'.
    """
    if metric not in ('jaccard', 'hamming'):
        raise ValueError(f"metric must be 'jaccard' or 'hamming', got '{metric}'")
    
    n_samples = data.shape[0]
    
    # Handle edge case of single sample
    if n_samples == 1:
        return np.zeros((1, 1))
    
    # Use scipy's optimized pdist for vectorized calculation
    # pdist computes condensed distance matrix (upper triangle only)
    condensed_distances = pdist(data, metric=metric)
    
    # Convert to square form (full symmetric matrix)
    distances = squareform(condensed_distances)
    
    return distances


def calculate_prevalence(
    data: pd.DataFrame, 
    exclude_cols: list[str] = ['Strain_ID']
) -> pd.Series:
    """
    Calculate prevalence (%) of each feature in the dataset.
    
    Prevalence is the percentage of samples in which a feature is present
    (has value 1 in binary data).
    
    Args:
        data: DataFrame with binary features. Each column is a feature,
              each row is a sample.
        exclude_cols: Column names to exclude from calculation (e.g., IDs).
        
    Returns:
        Series with prevalence percentages, sorted in descending order.
        Index contains feature names, values are percentages (0-100).
        
    Examples:
        >>> df = pd.DataFrame({
        ...     'Strain_ID': ['S1', 'S2', 'S3'],
        ...     'gene1': [1, 1, 0],
        ...     'gene2': [0, 0, 0]
        ... })
        >>> prevalence = calculate_prevalence(df)
        >>> prevalence['gene1'] == 100 * (2/3)
        True
        
    Note:
        Returns empty Series if no feature columns exist.
    """
    feature_cols = [col for col in data.columns if col not in exclude_cols]
    
    if len(feature_cols) == 0:
        return pd.Series(dtype=float)
    
    prevalence = (data[feature_cols].sum() / len(data) * 100).sort_values(ascending=False)
    return prevalence


def calculate_correlation_matrix(
    data: pd.DataFrame, 
    exclude_cols: list[str] = ['Strain_ID']
) -> pd.DataFrame:
    """
    Calculate correlation matrix for binary features.
    
    Computes Pearson correlation coefficients between all pairs of features.
    For binary data, this measures the tendency of features to co-occur.
    
    Args:
        data: DataFrame with binary features. Each column is a feature,
              each row is a sample.
        exclude_cols: Column names to exclude from calculation (e.g., IDs).
        
    Returns:
        Correlation matrix as a DataFrame. Both index and columns contain
        feature names. Values are correlation coefficients in range [-1, 1].
        
    Mathematical Properties:
        - Symmetric: corr[i, j] == corr[j, i]
        - Diagonal is 1: corr[i, i] == 1
        - Range: [-1, 1]
        - corr = 1: perfect positive correlation
        - corr = -1: perfect negative correlation
        - corr ≈ 0: no linear correlation
        
    Examples:
        >>> df = pd.DataFrame({
        ...     'Strain_ID': ['S1', 'S2', 'S3', 'S4'],
        ...     'gene1': [1, 0, 1, 0],
        ...     'gene2': [1, 0, 1, 0]  # Identical to gene1
        ... })
        >>> corr = calculate_correlation_matrix(df)
        >>> abs(corr.loc['gene1', 'gene2'] - 1.0) < 1e-10
        True
        
    Note:
        Returns empty DataFrame if no feature columns exist.
    """
    feature_cols = [col for col in data.columns if col not in exclude_cols]
    
    if len(feature_cols) == 0:
        return pd.DataFrame()
    
    corr_matrix = data[feature_cols].corr()
    return corr_matrix
