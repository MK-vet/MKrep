"""
Synthetic Data Generator for StrepSuis-AMRVIRKM - K-Modes Clustering Validation

This module generates synthetic datasets using proper statistical distributions
that mimic real biological variability for K-Modes clustering validation.

Generation Methodology:
-----------------------
1. **Binomial Distribution**: Used for binary presence/absence data (resistance phenotypes,
   gene presence). Each sample is a Bernoulli trial with success probability p.

2. **Beta Distribution**: Used to generate prevalence rates that follow biological reality
   (most resistance genes have low to moderate prevalence).

3. **Correlation Structure**: Synthetic data includes known cluster-specific patterns
   to validate clustering correctness.

4. **Known Cluster Assignments**: Ground truth clusters are embedded in the data
   for validating silhouette scores and cluster recovery.

Scientific References:
---------------------
- Huang, Z. (1998). Extensions to the k-Means Algorithm for Clustering Large Data Sets
  with Categorical Values. Data Mining and Knowledge Discovery, 2(3), 283-304.
- Kaufman, L., & Rousseeuw, P. J. (1990). Finding Groups in Data. Wiley.

Author: MK-vet Team
License: MIT
Version: 1.0.0
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


@dataclass
class SyntheticClusterConfig:
    """Configuration for synthetic clustering data generation.

    Attributes:
        n_strains: Number of bacterial strains to generate
        n_clusters: Number of true clusters to embed
        n_mic_features: Number of MIC (antibiotic resistance) features
        n_amr_features: Number of AMR gene features
        n_virulence_features: Number of virulence factor features
        cluster_separation: Strength of cluster separation (0.0 to 1.0)
        noise_level: Proportion of random noise to add (0.0 to 1.0)
        random_state: Random seed for reproducibility
    """

    n_strains: int = 100
    n_clusters: int = 4
    n_mic_features: int = 13
    n_amr_features: int = 25
    n_virulence_features: int = 15
    cluster_separation: float = 0.7
    noise_level: float = 0.05
    random_state: int = 42


@dataclass
class SyntheticClusterMetadata:
    """Metadata describing the generated synthetic data.

    Contains ground truth values that can be used to validate
    the correctness of clustering methods.

    Attributes:
        config: The configuration used to generate the data
        true_cluster_labels: Array of true cluster assignments
        cluster_centroids: Dict of cluster -> feature pattern
        mic_columns: List of MIC column names
        amr_columns: List of AMR gene column names
        virulence_columns: List of virulence factor column names
        expected_silhouette_range: Expected silhouette score range
        generation_timestamp: When the data was generated
    """

    config: SyntheticClusterConfig
    true_cluster_labels: np.ndarray = field(default_factory=lambda: np.array([]))
    cluster_centroids: Dict[int, Dict[str, float]] = field(default_factory=dict)
    mic_columns: List[str] = field(default_factory=list)
    amr_columns: List[str] = field(default_factory=list)
    virulence_columns: List[str] = field(default_factory=list)
    expected_silhouette_range: Tuple[float, float] = (0.3, 0.8)
    generation_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


def generate_cluster_centroids(
    n_clusters: int,
    n_features: int,
    separation: float = 0.7,
    random_state: Optional[int] = 42,
) -> Dict[int, np.ndarray]:
    """
    Generate cluster centroids (probability patterns) for K-Modes clustering.

    Each cluster has a characteristic pattern of feature prevalences that
    distinguish it from other clusters.

    Parameters:
        n_clusters: Number of clusters to generate
        n_features: Number of features per cluster
        separation: How distinct clusters should be (0.0 to 1.0)
        random_state: Random seed for reproducibility

    Returns:
        Dict mapping cluster ID to feature prevalence pattern
    """
    rng = np.random.default_rng(random_state)

    centroids = {}
    base_prevalence = 0.3  # Base prevalence for features

    for cluster_id in range(n_clusters):
        # Each cluster has some features with high prevalence and others with low
        pattern = np.full(n_features, base_prevalence)

        # Select subset of features to have high prevalence in this cluster
        n_high = max(2, n_features // n_clusters)
        high_indices = rng.choice(n_features, size=n_high, replace=False)

        # Set high prevalence features based on separation strength
        pattern[high_indices] = base_prevalence + (1 - base_prevalence) * separation

        # Ensure some features are low in this cluster to distinguish from others
        n_low = max(1, n_features // (n_clusters * 2))
        remaining = [i for i in range(n_features) if i not in high_indices]
        if remaining:
            low_indices = rng.choice(remaining, size=min(n_low, len(remaining)), replace=False)
            pattern[low_indices] = base_prevalence * (1 - separation * 0.5)

        centroids[cluster_id] = np.clip(pattern, 0.05, 0.95)

    return centroids


def generate_binary_data_from_centroids(
    n_samples: int,
    centroids: Dict[int, np.ndarray],
    cluster_assignments: np.ndarray,
    noise_level: float = 0.05,
    random_state: Optional[int] = 42,
) -> np.ndarray:
    """
    Generate binary data based on cluster centroids.

    For each sample, generate binary features based on the prevalence
    pattern of its assigned cluster.

    Parameters:
        n_samples: Number of samples to generate
        centroids: Cluster centroid patterns
        cluster_assignments: True cluster assignment for each sample
        noise_level: Proportion of random noise
        random_state: Random seed

    Returns:
        Binary data matrix (n_samples x n_features)
    """
    rng = np.random.default_rng(random_state)
    n_features = len(centroids[0])
    data = np.zeros((n_samples, n_features), dtype=int)

    for i in range(n_samples):
        cluster_id = cluster_assignments[i]
        pattern = centroids[cluster_id]

        # Generate binary data based on cluster pattern
        data[i] = (rng.random(n_features) < pattern).astype(int)

        # Add noise
        noise_mask = rng.random(n_features) < noise_level
        data[i, noise_mask] = 1 - data[i, noise_mask]

    return data


def generate_clustering_synthetic_dataset(
    config: Optional[SyntheticClusterConfig] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, SyntheticClusterMetadata]:
    """
    Generate a complete synthetic dataset for K-Modes clustering validation.

    This function creates realistic synthetic data with:
    - MIC (antibiotic resistance) binary data
    - AMR gene presence/absence data
    - Virulence factor data
    - Known true cluster assignments
    - Characteristic patterns per cluster

    Parameters:
        config: Configuration object. Uses defaults if None.

    Returns:
        Tuple of (mic_df, amr_df, virulence_df, metadata):
            - mic_df: MIC data DataFrame
            - amr_df: AMR genes DataFrame
            - virulence_df: Virulence factors DataFrame
            - metadata: Ground truth and generation parameters
    """
    if config is None:
        config = SyntheticClusterConfig()

    rng = np.random.default_rng(config.random_state)

    # Initialize metadata
    metadata = SyntheticClusterMetadata(config=config)

    # Generate strain IDs
    strain_ids = [f"Strain_{i:04d}" for i in range(1, config.n_strains + 1)]

    # Assign strains to clusters (balanced assignment)
    cluster_sizes = [config.n_strains // config.n_clusters] * config.n_clusters
    for i in range(config.n_strains % config.n_clusters):
        cluster_sizes[i] += 1

    cluster_labels = []
    for cluster_id, size in enumerate(cluster_sizes):
        cluster_labels.extend([cluster_id + 1] * size)  # 1-indexed clusters

    cluster_labels = np.array(cluster_labels)
    rng.shuffle(cluster_labels)
    metadata.true_cluster_labels = cluster_labels

    # Generate column names
    mic_names = [
        "Oxytetracycline",
        "Doxycycline",
        "Tulathromycin",
        "Spectinomycin",
        "Gentamicin",
        "Tiamulin",
        "Trimethoprim_Sulphamethoxazole",
        "Enrofloxacin",
        "Penicillin",
        "Ampicillin",
        "Amoxicillin_Clavulanic_acid",
        "Ceftiofur",
        "Florfenicol",
    ][: config.n_mic_features]
    metadata.mic_columns = mic_names

    amr_names = [f"AMR_Gene_{i:02d}" for i in range(1, config.n_amr_features + 1)]
    metadata.amr_columns = amr_names

    vir_names = [f"Virulence_{i:02d}" for i in range(1, config.n_virulence_features + 1)]
    metadata.virulence_columns = vir_names

    # Generate cluster centroids for each feature category
    mic_centroids = generate_cluster_centroids(
        config.n_clusters,
        config.n_mic_features,
        config.cluster_separation,
        config.random_state,
    )
    amr_centroids = generate_cluster_centroids(
        config.n_clusters,
        config.n_amr_features,
        config.cluster_separation,
        config.random_state + 100,
    )
    vir_centroids = generate_cluster_centroids(
        config.n_clusters,
        config.n_virulence_features,
        config.cluster_separation,
        config.random_state + 200,
    )

    # Store centroids in metadata (convert to 0-indexed for internal use)
    for cluster_id in range(config.n_clusters):
        metadata.cluster_centroids[cluster_id + 1] = {
            "mic": mic_centroids[cluster_id].tolist(),
            "amr": amr_centroids[cluster_id].tolist(),
            "virulence": vir_centroids[cluster_id].tolist(),
        }

    # Generate binary data (convert 1-indexed labels to 0-indexed for generation)
    mic_data = generate_binary_data_from_centroids(
        config.n_strains,
        mic_centroids,
        cluster_labels - 1,  # Convert to 0-indexed
        config.noise_level,
        config.random_state + 300,
    )
    amr_data = generate_binary_data_from_centroids(
        config.n_strains,
        amr_centroids,
        cluster_labels - 1,
        config.noise_level,
        config.random_state + 400,
    )
    vir_data = generate_binary_data_from_centroids(
        config.n_strains,
        vir_centroids,
        cluster_labels - 1,
        config.noise_level,
        config.random_state + 500,
    )

    # Create DataFrames
    mic_df = pd.DataFrame(mic_data, columns=mic_names)
    mic_df.insert(0, "Strain_ID", strain_ids)

    amr_df = pd.DataFrame(amr_data, columns=amr_names)
    amr_df.insert(0, "Strain_ID", strain_ids)

    vir_df = pd.DataFrame(vir_data, columns=vir_names)
    vir_df.insert(0, "Strain_ID", strain_ids)

    return mic_df, amr_df, vir_df, metadata


def save_synthetic_clustering_data(
    mic_df: pd.DataFrame,
    amr_df: pd.DataFrame,
    vir_df: pd.DataFrame,
    metadata: SyntheticClusterMetadata,
    output_dir: str = "synthetic_data",
) -> Dict[str, str]:
    """
    Save synthetic clustering data and metadata to files.

    Parameters:
        mic_df: MIC data DataFrame
        amr_df: AMR genes DataFrame
        vir_df: Virulence factors DataFrame
        metadata: Metadata object with ground truth
        output_dir: Directory to save files to

    Returns:
        Dict with paths to saved files
    """
    import json

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    saved_files = {}

    # Save data files
    mic_file = output_path / "synthetic_MIC.csv"
    mic_df.to_csv(mic_file, index=False)
    saved_files["mic"] = str(mic_file)

    amr_file = output_path / "synthetic_AMR_genes.csv"
    amr_df.to_csv(amr_file, index=False)
    saved_files["amr_genes"] = str(amr_file)

    vir_file = output_path / "synthetic_Virulence.csv"
    vir_df.to_csv(vir_file, index=False)
    saved_files["virulence"] = str(vir_file)

    # Save ground truth cluster assignments
    clusters_df = pd.DataFrame(
        {"Strain_ID": mic_df["Strain_ID"], "True_Cluster": metadata.true_cluster_labels}
    )
    clusters_file = output_path / "synthetic_true_clusters.csv"
    clusters_df.to_csv(clusters_file, index=False)
    saved_files["true_clusters"] = str(clusters_file)

    # Save metadata as JSON
    metadata_dict = {
        "config": {
            "n_strains": metadata.config.n_strains,
            "n_clusters": metadata.config.n_clusters,
            "n_mic_features": metadata.config.n_mic_features,
            "n_amr_features": metadata.config.n_amr_features,
            "n_virulence_features": metadata.config.n_virulence_features,
            "cluster_separation": metadata.config.cluster_separation,
            "noise_level": metadata.config.noise_level,
            "random_state": metadata.config.random_state,
        },
        "true_cluster_counts": {
            str(k): int(v) for k, v in zip(*np.unique(metadata.true_cluster_labels, return_counts=True))
        },
        "expected_silhouette_range": list(metadata.expected_silhouette_range),
        "mic_columns": metadata.mic_columns,
        "amr_columns": metadata.amr_columns,
        "virulence_columns": metadata.virulence_columns,
        "generation_timestamp": metadata.generation_timestamp,
        "generation_method": "Binomial with cluster-specific centroids",
    }

    metadata_file = output_path / "synthetic_metadata.json"
    with open(metadata_file, "w") as f:
        json.dump(metadata_dict, f, indent=2)
    saved_files["metadata"] = str(metadata_file)

    # Save methodology documentation
    methodology_content = f"""# Synthetic Data Generation Methodology for K-Modes Clustering

## Overview

This document describes the statistical methodology used to generate synthetic
data for validating K-Modes clustering analysis.

## Generation Parameters

- **Number of strains**: {metadata.config.n_strains}
- **Number of clusters**: {metadata.config.n_clusters}
- **MIC features**: {metadata.config.n_mic_features}
- **AMR gene features**: {metadata.config.n_amr_features}
- **Virulence factor features**: {metadata.config.n_virulence_features}
- **Cluster separation strength**: {metadata.config.cluster_separation:.2f}
- **Noise level**: {metadata.config.noise_level:.2f}
- **Random seed**: {metadata.config.random_state}

## Statistical Methods Used

### 1. Cluster Centroid Generation

Each cluster is defined by a characteristic pattern of feature prevalences.
Features are assigned high or low prevalences based on cluster identity:

- High prevalence features: p = base + (1 - base) × separation
- Low prevalence features: p = base × (1 - separation × 0.5)
- Base prevalence: 0.3

### 2. Binary Data Generation

For each sample, binary features are generated using Bernoulli trials:
- P(feature=1) = cluster_prevalence[feature]
- Each trial is independent

### 3. Noise Addition

A small proportion ({metadata.config.noise_level*100:.1f}%) of values are randomly
flipped to simulate measurement error and biological variability.

## Ground Truth

### Cluster Distribution
"""
    cluster_counts = np.bincount(metadata.true_cluster_labels)[1:]  # Skip 0 index
    for i, count in enumerate(cluster_counts, 1):
        methodology_content += f"- Cluster {i}: {count} strains ({count/metadata.config.n_strains*100:.1f}%)\n"

    methodology_content += f"""
## Expected Clustering Performance

- Expected silhouette score range: {metadata.expected_silhouette_range[0]:.2f} - {metadata.expected_silhouette_range[1]:.2f}
- Cluster recovery should be >{int(metadata.config.cluster_separation*100)}% accurate

## References

1. Huang, Z. (1998). Extensions to the k-Means Algorithm for Clustering Large Data Sets
   with Categorical Values. Data Mining and Knowledge Discovery.
2. Kaufman, L., & Rousseeuw, P. J. (1990). Finding Groups in Data. Wiley.

## Generation Timestamp

{metadata.generation_timestamp}

---
*This data was generated for validation and testing purposes only.*
"""

    methodology_file = output_path / "GENERATION_METHODOLOGY.md"
    with open(methodology_file, "w") as f:
        f.write(methodology_content)
    saved_files["methodology"] = str(methodology_file)

    return saved_files


def validate_synthetic_clustering_data(
    mic_df: pd.DataFrame,
    amr_df: pd.DataFrame,
    vir_df: pd.DataFrame,
    metadata: SyntheticClusterMetadata,
) -> Dict[str, Any]:
    """
    Validate that synthetic data has expected statistical properties.

    Parameters:
        mic_df: MIC data DataFrame
        amr_df: AMR genes DataFrame
        vir_df: Virulence factors DataFrame
        metadata: Metadata with ground truth

    Returns:
        Dict with validation results
    """
    results = {
        "validation_passed": True,
        "checks": [],
        "warnings": [],
        "errors": [],
    }

    # Check 1: Verify shapes
    expected_rows = metadata.config.n_strains
    for name, df, expected_cols in [
        ("MIC", mic_df, metadata.config.n_mic_features + 1),
        ("AMR", amr_df, metadata.config.n_amr_features + 1),
        ("Virulence", vir_df, metadata.config.n_virulence_features + 1),
    ]:
        if len(df) == expected_rows:
            results["checks"].append(f"✓ {name} row count: {len(df)}")
        else:
            results["errors"].append(f"✗ {name} row count: {len(df)} (expected {expected_rows})")
            results["validation_passed"] = False

        if len(df.columns) == expected_cols:
            results["checks"].append(f"✓ {name} column count: {len(df.columns)}")
        else:
            results["errors"].append(f"✗ {name} column count: {len(df.columns)} (expected {expected_cols})")
            results["validation_passed"] = False

    # Check 2: Verify binary data
    for name, df in [("MIC", mic_df), ("AMR", amr_df), ("Virulence", vir_df)]:
        feature_cols = [c for c in df.columns if c != "Strain_ID"]
        all_binary = all(set(df[col].unique()).issubset({0, 1}) for col in feature_cols)
        if all_binary:
            results["checks"].append(f"✓ {name} data is binary")
        else:
            results["warnings"].append(f"⚠ {name} has non-binary values")

    # Check 3: Verify cluster count
    unique_clusters = len(np.unique(metadata.true_cluster_labels))
    if unique_clusters == metadata.config.n_clusters:
        results["checks"].append(f"✓ Cluster count: {unique_clusters}")
    else:
        results["errors"].append(
            f"✗ Cluster count: {unique_clusters} (expected {metadata.config.n_clusters})"
        )
        results["validation_passed"] = False

    # Check 4: Verify cluster balance
    cluster_counts = np.bincount(metadata.true_cluster_labels)[1:]
    min_count = cluster_counts.min()
    max_count = cluster_counts.max()
    if max_count - min_count <= metadata.config.n_strains // metadata.config.n_clusters:
        results["checks"].append(f"✓ Clusters are balanced (range: {min_count}-{max_count})")
    else:
        results["warnings"].append(f"⚠ Cluster imbalance: {min_count}-{max_count}")

    return results


if __name__ == "__main__":
    # Generate synthetic data when run directly
    print("Generating synthetic K-Modes clustering data...")

    config = SyntheticClusterConfig(
        n_strains=100,
        n_clusters=4,
        random_state=42,
    )

    mic_df, amr_df, vir_df, metadata = generate_clustering_synthetic_dataset(config)

    print(f"Generated {len(mic_df)} strains with:")
    print(f"  - {len(metadata.mic_columns)} MIC features")
    print(f"  - {len(metadata.amr_columns)} AMR gene features")
    print(f"  - {len(metadata.virulence_columns)} virulence factor features")
    print(f"  - {metadata.config.n_clusters} true clusters")

    # Validate
    print("\nValidating synthetic data...")
    validation = validate_synthetic_clustering_data(mic_df, amr_df, vir_df, metadata)

    for check in validation["checks"]:
        print(f"  {check}")
    if validation["warnings"]:
        print(f"\nWarnings: {len(validation['warnings'])}")
    if validation["errors"]:
        print(f"Errors: {len(validation['errors'])}")

    print(f"\nValidation: {'PASSED' if validation['validation_passed'] else 'FAILED'}")

    # Save data
    print("\nSaving synthetic data...")
    output_dir = Path(__file__).parent.parent / "synthetic_data"
    saved = save_synthetic_clustering_data(mic_df, amr_df, vir_df, metadata, str(output_dir))

    for key, path in saved.items():
        print(f"  Saved {key}: {path}")

    print("\nDone!")
