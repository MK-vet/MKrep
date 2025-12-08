"""
Generate synthetic datasets matching the schema of example data.

This script creates synthetic data for testing the strepsuis-analyzer application
with deterministic, reproducible outputs.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List


def generate_synthetic_amr_genes(
    n_strains: int = 50, n_genes: int = 21, random_state: int = 42
) -> pd.DataFrame:
    """Generate synthetic AMR genes binary matrix."""
    np.random.seed(random_state)
    
    # Create strain names
    strains = [f"SynStrain_{i+1:03d}" for i in range(n_strains)]
    
    # Gene names matching example data
    genes = [
        "SAT-4", "aad9", "ant(6)-Ia", "aph(3')-III", "ermB", "lnuC", "lsaE",
        "mefA", "msrD", "tetM", "tetO", "tetW", "blaTEM", "floR", "catA3",
        "strA", "strB", "sul1", "sul2", "dfrG", "aac(6')-Ie"
    ]
    
    # Generate binary matrix with ~30% prevalence
    data = np.random.binomial(1, 0.3, size=(n_strains, len(genes)))
    
    df = pd.DataFrame(data, columns=genes)
    df.insert(0, "Strain", strains)
    
    return df


def generate_synthetic_mic(
    n_strains: int = 50, random_state: int = 42
) -> pd.DataFrame:
    """Generate synthetic MIC data with log-normal distribution."""
    np.random.seed(random_state)
    
    strains = [f"SynStrain_{i+1:03d}" for i in range(n_strains)]
    
    antibiotics = [
        "Penicillin", "Ampicillin", "Ceftiofur", "Enrofloxacin",
        "Tetracycline", "Doxycycline", "Erythromycin", "Tilmicosin",
        "Gentamicin", "Spectinomycin", "Trimethoprim-Sulfa",
        "Chloramphenicol", "Florfenicol"
    ]
    
    # Generate log-normal MIC values
    data = {}
    data["Strain"] = strains
    
    for antibiotic in antibiotics:
        # Log-normal distribution for MIC values
        mic_values = np.random.lognormal(mean=1.0, sigma=1.5, size=n_strains)
        data[antibiotic] = mic_values
    
    return pd.DataFrame(data)


def generate_synthetic_virulence(
    n_strains: int = 50, n_factors: int = 106, random_state: int = 42
) -> pd.DataFrame:
    """Generate synthetic virulence factors binary matrix."""
    np.random.seed(random_state)
    
    strains = [f"SynStrain_{i+1:03d}" for i in range(n_strains)]
    
    # Create virulence factor names matching pattern vir_A00, vir_B01, etc.
    factors = []
    for prefix in ['A', 'B', 'C', 'D', 'E']:
        for i in range(26):
            factors.append(f"vir_{prefix}{i:02d}")
        if len(factors) >= n_factors:
            break
    factors = factors[:n_factors]
    
    # Generate binary matrix with ~20% prevalence
    data = np.random.binomial(1, 0.2, size=(n_strains, len(factors)))
    
    df = pd.DataFrame(data, columns=factors)
    df.insert(0, "Strain", strains)
    
    return df


def generate_synthetic_mlst(
    n_strains: int = 50, random_state: int = 42
) -> pd.DataFrame:
    """Generate synthetic MLST data."""
    np.random.seed(random_state)
    
    strains = [f"SynStrain_{i+1:03d}" for i in range(n_strains)]
    
    # Generate random ST types (5-10 unique types)
    st_types = [f"ST{i}" for i in [25, 28, 1, 7, 94, 16, 105, 208]]
    sts = np.random.choice(st_types, size=n_strains)
    
    return pd.DataFrame({"Strain": strains, "ST": sts})


def generate_synthetic_serotype(
    n_strains: int = 50, random_state: int = 42
) -> pd.DataFrame:
    """Generate synthetic serotype data."""
    np.random.seed(random_state)
    
    strains = [f"SynStrain_{i+1:03d}" for i in range(n_strains)]
    
    # Common serotypes
    serotypes = ["2", "4", "7", "9", "11", "14", "1/2", "3"]
    seros = np.random.choice(serotypes, size=n_strains)
    
    return pd.DataFrame({"Strain": strains, "Serotype": seros})


def generate_synthetic_newick_tree(
    n_strains: int = 50, random_state: int = 42
) -> str:
    """
    Generate synthetic Newick phylogenetic tree.
    
    Creates a simple random tree structure with branch lengths.
    """
    np.random.seed(random_state)
    
    strains = [f"SynStrain_{i+1:03d}" for i in range(n_strains)]
    
    # Simple recursive tree generation
    def build_tree(taxa_list: List[str]) -> str:
        if len(taxa_list) == 1:
            return taxa_list[0]
        
        if len(taxa_list) == 2:
            bl1 = np.random.uniform(0.001, 0.3)
            bl2 = np.random.uniform(0.001, 0.3)
            return f"({taxa_list[0]}:{bl1:.6f},{taxa_list[1]}:{bl2:.6f})"
        
        # Split randomly
        split_point = np.random.randint(1, len(taxa_list))
        left = taxa_list[:split_point]
        right = taxa_list[split_point:]
        
        left_tree = build_tree(left)
        right_tree = build_tree(right)
        
        bl1 = np.random.uniform(0.001, 0.3)
        bl2 = np.random.uniform(0.001, 0.3)
        
        return f"({left_tree}:{bl1:.6f},{right_tree}:{bl2:.6f})"
    
    # Shuffle strains for random tree structure
    shuffled_strains = strains.copy()
    np.random.shuffle(shuffled_strains)
    
    tree = build_tree(shuffled_strains)
    return tree + ";"


def main():
    """Generate all synthetic datasets."""
    output_dir = Path(__file__).parent.parent / "data" / "synthetic"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating synthetic datasets...")
    
    # Generate datasets
    amr_df = generate_synthetic_amr_genes(n_strains=50, random_state=42)
    print(f"Generated AMR_genes.csv: {amr_df.shape}")
    amr_df.to_csv(output_dir / "AMR_genes.csv", index=False)
    
    mic_df = generate_synthetic_mic(n_strains=50, random_state=42)
    print(f"Generated MIC.csv: {mic_df.shape}")
    mic_df.to_csv(output_dir / "MIC.csv", index=False)
    
    vir_df = generate_synthetic_virulence(n_strains=50, n_factors=106, random_state=42)
    print(f"Generated Virulence.csv: {vir_df.shape}")
    vir_df.to_csv(output_dir / "Virulence.csv", index=False)
    
    mlst_df = generate_synthetic_mlst(n_strains=50, random_state=42)
    print(f"Generated MLST.csv: {mlst_df.shape}")
    mlst_df.to_csv(output_dir / "MLST.csv", index=False)
    
    sero_df = generate_synthetic_serotype(n_strains=50, random_state=42)
    print(f"Generated Serotype.csv: {sero_df.shape}")
    sero_df.to_csv(output_dir / "Serotype.csv", index=False)
    
    tree_newick = generate_synthetic_newick_tree(n_strains=50, random_state=42)
    print(f"Generated Snp_tree.newick: {len(tree_newick)} characters")
    with open(output_dir / "Snp_tree.newick", "w") as f:
        f.write(tree_newick)
    
    print(f"\nAll synthetic datasets saved to: {output_dir}")


if __name__ == "__main__":
    main()
