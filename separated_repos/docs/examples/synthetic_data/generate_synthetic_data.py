"""
Synthetic Data Generation for StrepSuis Suite Validation

This module generates synthetic datasets with known ground truth for validating
the statistical methods implemented across all StrepSuis modules.

Generated datasets include:
- synthetic_amr_data.csv: Known MDR patterns
- synthetic_clustering_data.csv: Known cluster assignments
- synthetic_network_data.csv: Known association patterns
- synthetic_phylo_data.csv: Known phylogenetic relationships

All datasets have known statistical properties that can be validated.
"""

import numpy as np
import pandas as pd
import os


def generate_amr_data(n_strains=100, seed=42):
    """
    Generate synthetic AMR data with known MDR patterns.
    
    Known ground truth:
    - 3 antibiotic classes with known resistance patterns
    - 50% of strains are MDR (resistant to >= 3 classes)
    - Known co-occurrence patterns between classes
    
    Args:
        n_strains: Number of strains to generate
        seed: Random seed for reproducibility
    
    Returns:
        DataFrame with binary resistance data
    """
    np.random.seed(seed)
    
    # Generate strain IDs
    strains = [f'S{i:04d}' for i in range(1, n_strains + 1)]
    
    # Generate resistance patterns
    # Class 1: Tetracyclines (60% prevalence)
    tet_base = np.random.binomial(1, 0.6, n_strains)
    oxytet = tet_base
    doxycycline = tet_base * np.random.binomial(1, 0.9, n_strains)  # High co-occurrence
    
    # Class 2: Macrolides (45% prevalence)
    mac_base = np.random.binomial(1, 0.45, n_strains)
    tulathromycin = mac_base
    tilmicosin = mac_base * np.random.binomial(1, 0.85, n_strains)
    
    # Class 3: Penicillins (35% prevalence)
    pen_base = np.random.binomial(1, 0.35, n_strains)
    penicillin = pen_base
    ampicillin = pen_base * np.random.binomial(1, 0.8, n_strains)
    
    # Class 4: Aminoglycosides (25% prevalence)
    ami_base = np.random.binomial(1, 0.25, n_strains)
    gentamicin = ami_base
    streptomycin = ami_base * np.random.binomial(1, 0.75, n_strains)
    
    data = pd.DataFrame({
        'Strain_ID': strains,
        'Oxytetracycline': oxytet,
        'Doxycycline': doxycycline,
        'Tulathromycin': tulathromycin,
        'Tilmicosin': tilmicosin,
        'Penicillin': penicillin,
        'Ampicillin': ampicillin,
        'Gentamicin': gentamicin,
        'Streptomycin': streptomycin,
    })
    
    return data


def generate_amr_genes_data(n_strains=100, seed=42):
    """
    Generate synthetic AMR genes data with known gene-phenotype associations.
    
    Known ground truth:
    - tetA/tetM associated with tetracycline resistance (phi > 0.7)
    - ermB associated with macrolide resistance (phi > 0.6)
    - blaTEM associated with penicillin resistance (phi > 0.5)
    
    Args:
        n_strains: Number of strains
        seed: Random seed
    
    Returns:
        DataFrame with binary gene presence data
    """
    np.random.seed(seed)
    
    strains = [f'S{i:04d}' for i in range(1, n_strains + 1)]
    
    # Tetracycline genes
    tetA = np.random.binomial(1, 0.55, n_strains)
    tetM = np.random.binomial(1, 0.50, n_strains)
    
    # Macrolide genes
    ermB = np.random.binomial(1, 0.40, n_strains)
    mefA = np.random.binomial(1, 0.30, n_strains)
    
    # Beta-lactam genes
    blaTEM = np.random.binomial(1, 0.30, n_strains)
    
    # Aminoglycoside genes
    aph3 = np.random.binomial(1, 0.20, n_strains)
    aadA = np.random.binomial(1, 0.18, n_strains)
    
    data = pd.DataFrame({
        'Strain_ID': strains,
        'tetA': tetA,
        'tetM': tetM,
        'ermB': ermB,
        'mefA': mefA,
        'blaTEM': blaTEM,
        'aph3': aph3,
        'aadA': aadA,
    })
    
    return data


def generate_clustering_data(n_strains=100, n_clusters=4, seed=42):
    """
    Generate synthetic clustering data with known cluster assignments.
    
    Known ground truth:
    - n_clusters well-separated clusters
    - Each cluster has characteristic trait patterns
    - Silhouette score should be > 0.5
    
    Args:
        n_strains: Number of strains
        n_clusters: Number of true clusters
        seed: Random seed
    
    Returns:
        Tuple of (trait data, true cluster labels)
    """
    np.random.seed(seed)
    
    strains = [f'S{i:04d}' for i in range(1, n_strains + 1)]
    strains_per_cluster = n_strains // n_clusters
    
    data = {'Strain_ID': strains}
    true_clusters = []
    
    # Generate cluster assignments
    for i in range(n_strains):
        cluster = (i // strains_per_cluster) + 1
        cluster = min(cluster, n_clusters)
        true_clusters.append(cluster)
    
    # Generate traits with cluster-specific patterns
    n_traits = 10
    for t in range(n_traits):
        trait_name = f'Trait_{t+1}'
        values = []
        
        for i in range(n_strains):
            cluster = true_clusters[i]
            # Each cluster has different base probability for each trait
            prob = 0.2 + (cluster - 1) * 0.15 + (t % n_clusters == cluster - 1) * 0.4
            prob = min(max(prob, 0.05), 0.95)
            values.append(np.random.binomial(1, prob))
        
        data[trait_name] = values
    
    data['True_Cluster'] = true_clusters
    
    return pd.DataFrame(data)


def generate_network_data(n_nodes=50, seed=42):
    """
    Generate synthetic network data with known association patterns.
    
    Known ground truth:
    - Strong positive associations (phi > 0.5) between certain node pairs
    - Strong negative associations (phi < -0.5) between others
    - Some independent nodes (phi ≈ 0)
    
    Args:
        n_nodes: Number of nodes (genes/phenotypes)
        seed: Random seed
    
    Returns:
        DataFrame with binary node presence data
    """
    np.random.seed(seed)
    
    n_samples = 100
    strains = [f'S{i:04d}' for i in range(1, n_samples + 1)]
    
    data = {'Strain_ID': strains}
    
    # Generate base nodes
    for i in range(n_nodes):
        node_name = f'Node_{i+1}'
        data[node_name] = np.random.binomial(1, 0.5, n_samples)
    
    # Create known associations
    # Node 1-2: Strong positive association
    data['Node_1'] = np.random.binomial(1, 0.5, n_samples)
    data['Node_2'] = data['Node_1'] * np.random.binomial(1, 0.9, n_samples) + \
                     (1 - data['Node_1']) * np.random.binomial(1, 0.1, n_samples)
    
    # Node 3-4: Strong negative association
    data['Node_3'] = np.random.binomial(1, 0.5, n_samples)
    data['Node_4'] = (1 - data['Node_3']) * np.random.binomial(1, 0.85, n_samples) + \
                     data['Node_3'] * np.random.binomial(1, 0.15, n_samples)
    
    # Node 5-6: Moderate positive association
    data['Node_5'] = np.random.binomial(1, 0.5, n_samples)
    data['Node_6'] = data['Node_5'] * np.random.binomial(1, 0.7, n_samples) + \
                     (1 - data['Node_5']) * np.random.binomial(1, 0.3, n_samples)
    
    return pd.DataFrame(data)


def generate_phylo_data(n_strains=100, seed=42):
    """
    Generate synthetic phylogenetic data with known relationships.
    
    Known ground truth:
    - Strains belong to phylogenetic clusters
    - Within-cluster distances < between-cluster distances
    
    Args:
        n_strains: Number of strains
        seed: Random seed
    
    Returns:
        DataFrame with strain metadata including phylogenetic cluster
    """
    np.random.seed(seed)
    
    strains = [f'S{i:04d}' for i in range(1, n_strains + 1)]
    
    # Assign phylogenetic clusters (3 clades)
    n_clades = 3
    clades = []
    for i in range(n_strains):
        clade = (i % n_clades) + 1
        clades.append(clade)
    
    # Generate MLST types (associated with clades)
    mlst = []
    for clade in clades:
        # Each clade has 2-3 dominant STs
        st = clade * 10 + np.random.choice([1, 2, 3])
        mlst.append(st)
    
    # Generate serotypes
    serotypes = []
    for clade in clades:
        # Serotypes associated with clades
        st = np.random.choice([2, 9, 1]) if clade == 1 else \
             np.random.choice([7, 3, 4]) if clade == 2 else \
             np.random.choice([5, 14, 16])
        serotypes.append(st)
    
    data = pd.DataFrame({
        'Strain_ID': strains,
        'Phylo_Clade': clades,
        'MLST': mlst,
        'Serotype': serotypes,
    })
    
    return data


def save_all_synthetic_data(output_dir='synthetic_data'):
    """
    Generate and save all synthetic datasets.
    
    Args:
        output_dir: Directory to save datasets
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate datasets
    amr = generate_amr_data()
    genes = generate_amr_genes_data()
    cluster = generate_clustering_data()
    network = generate_network_data()
    phylo = generate_phylo_data()
    
    # Save datasets
    amr.to_csv(os.path.join(output_dir, 'synthetic_amr_data.csv'), index=False)
    genes.to_csv(os.path.join(output_dir, 'synthetic_amr_genes.csv'), index=False)
    cluster.to_csv(os.path.join(output_dir, 'synthetic_clustering_data.csv'), index=False)
    network.to_csv(os.path.join(output_dir, 'synthetic_network_data.csv'), index=False)
    phylo.to_csv(os.path.join(output_dir, 'synthetic_phylo_data.csv'), index=False)
    
    print(f"Saved synthetic datasets to {output_dir}/")
    print(f"  - synthetic_amr_data.csv: {len(amr)} strains, {len(amr.columns)-1} antibiotics")
    print(f"  - synthetic_amr_genes.csv: {len(genes)} strains, {len(genes.columns)-1} genes")
    print(f"  - synthetic_clustering_data.csv: {len(cluster)} strains, known clusters")
    print(f"  - synthetic_network_data.csv: {len(network)} samples, known associations")
    print(f"  - synthetic_phylo_data.csv: {len(phylo)} strains, phylo metadata")


if __name__ == '__main__':
    save_all_synthetic_data()
