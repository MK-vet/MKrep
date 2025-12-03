"""
Synthetic Data Validation Tests for strepsuis-analyzer

These tests validate the analyzer using synthetic datasets with known ground truth properties.
This follows the validation approach used in other strepsuis modules (strepsuis-mdr, etc.).

Test categories:
1. Synthetic data generation with known cluster structure
2. Cluster recovery validation (can we find known clusters?)
3. Trait association detection (can we find known associations?)
4. Edge case testing with synthetic data
5. Ground truth validation scenarios

References:
- Similar to test_validation_and_synthetic.py in strepsuis-mdr
- Validates against known ground truth instead of just checking for crashes
"""

import numpy as np
import pandas as pd
import pytest
import sys
from pathlib import Path
from scipy.cluster.hierarchy import fcluster
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from StrepSuisPhyloCluster_2025_08_11 import StrepSuisAnalyzer

# Try to import prince for MCA tests
try:
    import prince
    HAS_PRINCE = True
except ImportError:
    HAS_PRINCE = False


def generate_synthetic_data_with_clusters(
    n_strains: int = 60,
    n_traits: int = 12,
    n_clusters: int = 3,
    separation: float = 0.8,
    noise_level: float = 0.1,
    random_state: int = 42
) -> tuple[pd.DataFrame, np.ndarray]:
    """
    Generate synthetic binary trait data with known cluster structure.
    
    Parameters:
        n_strains: Number of strains to generate
        n_traits: Number of binary traits
        n_clusters: Number of distinct clusters
        separation: How separated clusters are (0.5 = no separation, 1.0 = perfect)
        noise_level: Proportion of random flips to add
        random_state: Random seed
    
    Returns:
        (data DataFrame, true_cluster_labels array)
    """
    rng = np.random.default_rng(random_state)
    
    # Create cluster assignments
    cluster_sizes = [n_strains // n_clusters] * n_clusters
    cluster_sizes[-1] += n_strains - sum(cluster_sizes)
    
    true_labels = np.concatenate([
        np.full(size, i) for i, size in enumerate(cluster_sizes)
    ])
    rng.shuffle(true_labels)
    
    # Create cluster-specific trait profiles
    cluster_profiles = {}
    for i in range(n_clusters):
        # Each cluster has characteristic traits
        # Use separation to control how distinct they are
        base_prob = 0.5  # Neutral
        if separation > 0.5:
            # Higher separation = more distinct profiles
            offset = (separation - 0.5) * 2  # Scale to [0, 1]
            probs = []
            for trait_idx in range(n_traits):
                # Alternate high/low probabilities for different clusters
                if (trait_idx + i) % n_clusters == 0:
                    probs.append(base_prob + offset * 0.4)
                elif (trait_idx + i) % n_clusters == 1:
                    probs.append(base_prob - offset * 0.4)
                else:
                    probs.append(base_prob)
            cluster_profiles[i] = np.clip(probs, 0.1, 0.9)
        else:
            cluster_profiles[i] = np.full(n_traits, base_prob)
    
    # Generate data
    data = []
    for strain_idx in range(n_strains):
        cluster_id = true_labels[strain_idx]
        probs = cluster_profiles[cluster_id]
        traits = rng.binomial(1, probs)
        data.append(traits)
    
    data = np.array(data)
    
    # Add noise
    n_flips = int(n_strains * n_traits * noise_level)
    for _ in range(n_flips):
        i = rng.integers(0, n_strains)
        j = rng.integers(0, n_traits)
        data[i, j] = 1 - data[i, j]
    
    # Create DataFrame
    df = pd.DataFrame(
        data,
        columns=[f'Trait_{i:02d}' for i in range(n_traits)]
    )
    df['Strain_ID'] = [f'Strain_{i:03d}' for i in range(n_strains)]
    
    return df, true_labels


def generate_synthetic_data_with_associations(
    n_strains: int = 80,
    n_traits: int = 16,
    n_clusters: int = 2,
    association_strength: float = 0.7,
    random_state: int = 42
) -> tuple[pd.DataFrame, list[tuple[str, str]]]:
    """
    Generate synthetic data with known trait-cluster associations.
    
    Parameters:
        n_strains: Number of strains
        n_traits: Number of traits
        n_clusters: Number of clusters
        association_strength: How strongly traits associate with clusters (0.5-1.0)
        random_state: Random seed
    
    Returns:
        (data DataFrame with Cluster column, list of (trait, cluster) associations)
    """
    rng = np.random.default_rng(random_state)
    
    # Create cluster assignments
    cluster_labels = rng.choice(n_clusters, size=n_strains)
    
    # Define which traits are associated with which clusters
    known_associations = []
    trait_cluster_map = {}
    
    for trait_idx in range(n_traits):
        if trait_idx < n_clusters * 3:  # First 3*n_clusters traits are associated
            associated_cluster = trait_idx % n_clusters
            trait_name = f'Trait_{trait_idx:02d}'
            trait_cluster_map[trait_name] = associated_cluster
            known_associations.append((trait_name, associated_cluster))
    
    # Generate data
    data = []
    for strain_idx in range(n_strains):
        cluster_id = cluster_labels[strain_idx]
        traits = []
        
        for trait_idx in range(n_traits):
            trait_name = f'Trait_{trait_idx:02d}'
            
            if trait_name in trait_cluster_map:
                # This trait is associated with a cluster
                associated_cluster = trait_cluster_map[trait_name]
                if cluster_id == associated_cluster:
                    # High probability if in associated cluster
                    prob = association_strength
                else:
                    # Low probability otherwise
                    prob = 1 - association_strength
            else:
                # Random trait, no association
                prob = 0.5
            
            traits.append(rng.binomial(1, prob))
        
        data.append(traits)
    
    # Create DataFrame
    df = pd.DataFrame(
        data,
        columns=[f'Trait_{i:02d}' for i in range(n_traits)]
    )
    df['Strain_ID'] = [f'Strain_{i:03d}' for i in range(n_strains)]
    df['Cluster'] = cluster_labels + 1  # 1-indexed for consistency with analyzer
    
    return df, known_associations


class TestSyntheticDataGeneration:
    """Test synthetic data generation utilities."""

    def test_generate_basic_synthetic_data(self):
        """Test basic synthetic data generation."""
        data, true_labels = generate_synthetic_data_with_clusters(
            n_strains=50, n_traits=10, n_clusters=3, random_state=42
        )
        
        assert len(data) == 50, "Should generate correct number of strains"
        assert 'Strain_ID' in data.columns, "Should have Strain_ID column"
        assert len([c for c in data.columns if c != 'Strain_ID']) == 10, "Should have correct traits"
        assert len(true_labels) == 50, "Should have labels for all strains"
        assert len(np.unique(true_labels)) == 3, "Should have 3 clusters"

    def test_synthetic_data_is_binary(self):
        """Test that synthetic data contains only binary values."""
        data, _ = generate_synthetic_data_with_clusters(
            n_strains=40, n_traits=8, random_state=42
        )
        
        trait_cols = [c for c in data.columns if c != 'Strain_ID']
        for col in trait_cols:
            unique_vals = data[col].unique()
            assert set(unique_vals).issubset({0, 1}), f"Column {col} should be binary"

    def test_synthetic_data_reproducibility(self):
        """Test that synthetic data generation is reproducible."""
        data1, labels1 = generate_synthetic_data_with_clusters(
            n_strains=30, random_state=42
        )
        data2, labels2 = generate_synthetic_data_with_clusters(
            n_strains=30, random_state=42
        )
        
        pd.testing.assert_frame_equal(data1, data2, 
            obj="Synthetic data should be reproducible")
        np.testing.assert_array_equal(labels1, labels2,
            err_msg="Labels should be reproducible")

    def test_different_seeds_produce_different_data(self):
        """Test that different seeds produce different data."""
        data1, labels1 = generate_synthetic_data_with_clusters(random_state=42)
        data2, labels2 = generate_synthetic_data_with_clusters(random_state=123)
        
        trait_cols = [c for c in data1.columns if c != 'Strain_ID']
        values1 = data1[trait_cols].values.flatten()
        values2 = data2[trait_cols].values.flatten()
        
        assert not np.array_equal(values1, values2), "Different seeds should produce different data"


class TestClusterRecovery:
    """Test that analyzer can recover known clusters from synthetic data."""

    def test_recover_well_separated_clusters(self):
        """Test cluster recovery with well-separated data (high separation)."""
        # Generate data with high separation
        data, true_labels = generate_synthetic_data_with_clusters(
            n_strains=60, n_traits=12, n_clusters=3,
            separation=0.9, noise_level=0.05, random_state=42
        )
        
        # Run analyzer
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_cluster_recovery', random_state=42)
        analyzer.data = data
        analyzer.perform_clustering(n_clusters=3)
        
        # Evaluate cluster recovery using Adjusted Rand Index (ARI)
        # ARI = 1 means perfect recovery, 0 means random
        ari = adjusted_rand_score(true_labels, analyzer.clusters - 1)  # -1 to convert to 0-indexed
        
        # For well-separated clusters, should recover well (ARI > 0.5)
        assert ari > 0.5, f"Should recover well-separated clusters (ARI={ari:.3f})"

    def test_recover_moderately_separated_clusters(self):
        """Test cluster recovery with moderately separated data."""
        data, true_labels = generate_synthetic_data_with_clusters(
            n_strains=60, n_traits=12, n_clusters=3,
            separation=0.7, noise_level=0.1, random_state=42
        )
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_moderate_recovery', random_state=42)
        analyzer.data = data
        analyzer.perform_clustering(n_clusters=3)
        
        # For moderate separation, should still recover reasonably well
        ari = adjusted_rand_score(true_labels, analyzer.clusters - 1)
        nmi = normalized_mutual_info_score(true_labels, analyzer.clusters - 1)
        
        # Should have some agreement with true clusters (binary data clustering is hard)
        assert ari > 0.05, f"Should have some cluster recovery (ARI={ari:.3f})"
        assert nmi > 0.05, f"Should have mutual information with true clusters (NMI={nmi:.3f})"

    def test_optimal_cluster_selection(self):
        """Test that automatic cluster selection finds reasonable number."""
        data, true_labels = generate_synthetic_data_with_clusters(
            n_strains=60, n_traits=12, n_clusters=3,
            separation=0.85, random_state=42
        )
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_optimal_k', random_state=42)
        analyzer.data = data
        analyzer.perform_clustering(n_clusters=None)  # Auto-select
        
        # Should find reasonable number of clusters (silhouette can select many for binary data)
        n_found = len(np.unique(analyzer.clusters))
        assert 2 <= n_found <= 15, f"Should find 2-15 clusters, found {n_found}"

    def test_cluster_sizes_reasonable(self):
        """Test that discovered cluster sizes are reasonable (no tiny clusters)."""
        data, true_labels = generate_synthetic_data_with_clusters(
            n_strains=80, n_clusters=4, random_state=42
        )
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_cluster_sizes', random_state=42)
        analyzer.data = data
        analyzer.perform_clustering(n_clusters=4)
        
        # Check cluster sizes
        cluster_counts = pd.Series(analyzer.clusters).value_counts()
        
        # No cluster should be too small (< 5% of data)
        min_cluster_size = cluster_counts.min()
        assert min_cluster_size >= 4, f"Smallest cluster has only {min_cluster_size} members"


class TestTraitAssociationDetection:
    """Test detection of known trait-cluster associations."""

    def test_detect_strong_associations(self):
        """Test detection of strong trait-cluster associations."""
        # Generate data with known associations
        data, known_associations = generate_synthetic_data_with_associations(
            n_strains=100, n_traits=12, n_clusters=2,
            association_strength=0.9, random_state=42
        )
        
        # Run analyzer (data already has Cluster column)
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_associations', random_state=42)
        analyzer.data = data
        analyzer.clusters = data['Cluster'].values
        
        # Calculate trait associations
        analyzer.calculate_trait_associations(fdr_alpha=0.05)
        
        results = analyzer.results['trait_associations']
        significant = results[results['Significant']]['Feature'].tolist()
        
        # Should detect at least some of the known associations
        known_trait_names = [trait for trait, cluster in known_associations]
        detected_count = len(set(significant) & set(known_trait_names))
        
        assert detected_count > 0, "Should detect at least some known associations"
        
        # Most known associations should be detected (allow some misses due to noise)
        detection_rate = detected_count / len(known_trait_names)
        assert detection_rate > 0.5, f"Should detect >50% of known associations (got {detection_rate:.1%})"

    def test_fdr_control_on_synthetic_data(self):
        """Test that FDR correction works correctly on synthetic data."""
        data, known_associations = generate_synthetic_data_with_associations(
            n_strains=80, n_traits=20, n_clusters=2,
            association_strength=0.75, random_state=42
        )
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_fdr', random_state=42)
        analyzer.data = data
        analyzer.clusters = data['Cluster'].values
        
        analyzer.calculate_trait_associations(fdr_alpha=0.05)
        results = analyzer.results['trait_associations']
        
        # Check FDR properties
        assert 'P_adj' in results.columns, "Should have adjusted p-values"
        assert all(results['P_adj'] >= results['P_value']), "Adjusted p should be >= raw p"
        
        # FDR-corrected p-values should be monotonic when sorted by raw p
        results_sorted = results.sort_values('P_value')
        p_adj_sorted = results_sorted['P_adj'].values
        
        for i in range(len(p_adj_sorted) - 1):
            assert p_adj_sorted[i] <= p_adj_sorted[i+1] + 1e-10, \
                f"FDR monotonicity violated at index {i}"

    def test_no_false_associations_in_random_data(self):
        """Test that random data produces few significant associations."""
        np.random.seed(42)
        
        # Generate completely random data (no real associations)
        data = pd.DataFrame({
            f'Trait_{i:02d}': np.random.binomial(1, 0.5, 60)
            for i in range(15)
        })
        data['Strain_ID'] = [f'Strain_{i}' for i in range(60)]
        data['Cluster'] = np.random.choice([1, 2, 3], size=60)
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_random', random_state=42)
        analyzer.data = data
        analyzer.clusters = data['Cluster'].values
        
        analyzer.calculate_trait_associations(fdr_alpha=0.05)
        results = analyzer.results['trait_associations']
        
        # With FDR at 0.05, should find few/no significant associations in random data
        n_significant = results['Significant'].sum()
        
        # Allow up to 1 false positive due to randomness (5% FDR on 15 traits)
        assert n_significant <= 1, f"Random data should have few significant results, got {n_significant}"


class TestEdgeCasesWithSyntheticData:
    """Test edge cases using synthetic data."""

    def test_perfect_cluster_separation(self):
        """Test with perfectly separated clusters (no overlap)."""
        # Generate perfect separation
        cluster1 = np.ones((20, 8))
        cluster2 = np.zeros((20, 8))
        X = np.vstack([cluster1, cluster2])
        
        data = pd.DataFrame(X, columns=[f'Trait_{i}' for i in range(8)])
        data['Strain_ID'] = [f'Strain_{i}' for i in range(40)]
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_perfect', random_state=42)
        analyzer.data = data
        analyzer.perform_clustering(n_clusters=2)
        
        # Should perfectly recover clusters
        true_labels = np.array([0]*20 + [1]*20)
        ari = adjusted_rand_score(true_labels, analyzer.clusters - 1)
        
        assert ari > 0.95, f"Should perfectly recover separated clusters (ARI={ari:.3f})"

    def test_complete_overlap_clusters(self):
        """Test with completely overlapping data (no structure)."""
        np.random.seed(42)
        
        # All strains have same distribution
        X = np.random.binomial(1, 0.5, (50, 10))
        
        data = pd.DataFrame(X, columns=[f'Trait_{i}' for i in range(10)])
        data['Strain_ID'] = [f'Strain_{i}' for i in range(50)]
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_overlap', random_state=42)
        analyzer.data = data
        
        # Should still complete clustering without error
        analyzer.perform_clustering(n_clusters=3)
        
        assert hasattr(analyzer, 'clusters'), "Should complete clustering"
        assert len(analyzer.clusters) == 50, "Should assign all strains"

    def test_extreme_imbalance_99_vs_1(self):
        """Test with extreme cluster imbalance (99% vs 1%)."""
        # 99 strains in one cluster, 1 in another
        cluster1 = np.random.binomial(1, 0.7, (99, 8))
        cluster2 = np.random.binomial(1, 0.3, (1, 8))
        X = np.vstack([cluster1, cluster2])
        
        data = pd.DataFrame(X, columns=[f'Trait_{i}' for i in range(8)])
        data['Strain_ID'] = [f'Strain_{i}' for i in range(100)]
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_imbalance', random_state=42)
        analyzer.data = data
        
        # Should handle extreme imbalance
        analyzer.perform_clustering(n_clusters=2)
        
        assert hasattr(analyzer, 'clusters'), "Should handle imbalanced data"

    def test_high_dimensional_data(self):
        """Test with high-dimensional data (many traits)."""
        data, true_labels = generate_synthetic_data_with_clusters(
            n_strains=50, n_traits=50, n_clusters=3, random_state=42
        )
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_highdim', random_state=42)
        analyzer.data = data
        analyzer.perform_clustering(n_clusters=3)
        
        # Should handle high dimensions
        assert hasattr(analyzer, 'clusters'), "Should handle high-dimensional data"

    def test_sparse_data(self):
        """Test with sparse data (mostly zeros)."""
        np.random.seed(42)
        
        # Generate sparse data (10% ones, 90% zeros)
        X = np.random.binomial(1, 0.1, (60, 15))
        
        data = pd.DataFrame(X, columns=[f'Trait_{i}' for i in range(15)])
        data['Strain_ID'] = [f'Strain_{i}' for i in range(60)]
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_sparse', random_state=42)
        analyzer.data = data
        analyzer.perform_clustering(n_clusters=3)
        
        # Should handle sparse data
        assert hasattr(analyzer, 'clusters'), "Should handle sparse data"

    def test_dense_data(self):
        """Test with dense data (mostly ones)."""
        np.random.seed(42)
        
        # Generate dense data (90% ones, 10% zeros)
        X = np.random.binomial(1, 0.9, (60, 15))
        
        data = pd.DataFrame(X, columns=[f'Trait_{i}' for i in range(15)])
        data['Strain_ID'] = [f'Strain_{i}' for i in range(60)]
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_dense', random_state=42)
        analyzer.data = data
        analyzer.perform_clustering(n_clusters=3)
        
        # Should handle dense data
        assert hasattr(analyzer, 'clusters'), "Should handle dense data"


class TestGroundTruthValidation:
    """Validate specific algorithmic properties using ground truth."""

    def test_cramers_v_detects_perfect_association(self):
        """Test that Cramér's V correctly identifies perfect association."""
        # Create data where Trait_00 is perfectly associated with Cluster
        data = pd.DataFrame({
            'Strain_ID': [f'Strain_{i}' for i in range(40)],
            'Trait_00': [1]*20 + [0]*20,  # Perfect association with cluster
            'Trait_01': np.random.binomial(1, 0.5, 40),  # Random
        })
        data['Cluster'] = [1]*20 + [2]*20
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_cramers', random_state=42)
        analyzer.data = data
        analyzer.clusters = data['Cluster'].values
        
        analyzer.calculate_trait_associations(fdr_alpha=0.05)
        results = analyzer.results['trait_associations']
        
        # Trait_00 should have high Cramér's V
        trait00_result = results[results['Feature'] == 'Trait_00'].iloc[0]
        
        assert trait00_result['Cramers_V'] > 0.9, \
            f"Perfect association should have Cramér's V > 0.9, got {trait00_result['Cramers_V']:.3f}"
        assert trait00_result['Significant'], "Perfect association should be significant"

    def test_chi_square_independence(self):
        """Test that chi-square correctly identifies independence."""
        np.random.seed(42)
        
        # Create independent data
        data = pd.DataFrame({
            'Strain_ID': [f'Strain_{i}' for i in range(100)],
            'Trait_00': np.random.binomial(1, 0.5, 100),  # Independent
            'Trait_01': np.random.binomial(1, 0.5, 100),  # Independent
        })
        # Random cluster assignment
        data['Cluster'] = np.random.choice([1, 2], size=100)
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_independence', random_state=42)
        analyzer.data = data
        analyzer.clusters = data['Cluster'].values
        
        analyzer.calculate_trait_associations(fdr_alpha=0.05)
        results = analyzer.results['trait_associations']
        
        # Most traits should not be significant
        n_significant = results['Significant'].sum()
        assert n_significant <= 1, f"Independent data should have few significant results"

    def test_silhouette_score_quality_metric(self):
        """Test that silhouette score reflects cluster quality."""
        from scipy.spatial.distance import pdist, squareform
        from scipy.cluster.hierarchy import fcluster
        from sklearn.metrics import silhouette_score
        
        # Well-separated clusters
        data_good, _ = generate_synthetic_data_with_clusters(
            n_strains=60, n_clusters=3, separation=0.9, random_state=42
        )
        
        # Poorly separated clusters
        data_poor, _ = generate_synthetic_data_with_clusters(
            n_strains=60, n_clusters=3, separation=0.55, random_state=123
        )
        
        # Calculate silhouette for well-separated
        trait_cols = [c for c in data_good.columns if c != 'Strain_ID']
        X_good = data_good[trait_cols].values
        dist_good = pdist(X_good, metric='jaccard')
        
        analyzer_good = StrepSuisAnalyzer(output_dir='/tmp/test_sil_good', random_state=42)
        analyzer_good.data = data_good
        analyzer_good.perform_clustering(n_clusters=3)
        
        sil_good = silhouette_score(squareform(dist_good), analyzer_good.clusters, 
                                    metric='precomputed')
        
        # Calculate silhouette for poorly separated
        X_poor = data_poor[trait_cols].values
        dist_poor = pdist(X_poor, metric='jaccard')
        
        analyzer_poor = StrepSuisAnalyzer(output_dir='/tmp/test_sil_poor', random_state=42)
        analyzer_poor.data = data_poor
        analyzer_poor.perform_clustering(n_clusters=3)
        
        sil_poor = silhouette_score(squareform(dist_poor), analyzer_poor.clusters,
                                    metric='precomputed')
        
        # Well-separated should have higher silhouette
        assert sil_good > sil_poor, \
            f"Well-separated clusters should have higher silhouette ({sil_good:.3f} vs {sil_poor:.3f})"
        assert sil_good > 0, "Well-separated clusters should have positive silhouette"


@pytest.mark.skipif(not HAS_PRINCE, reason="prince not available")
class TestMCAWithSyntheticData:
    """Test MCA using synthetic data."""

    def test_mca_on_clustered_data(self):
        """Test that MCA captures cluster structure."""
        # Generate well-separated data
        data, true_labels = generate_synthetic_data_with_clusters(
            n_strains=80, n_traits=12, n_clusters=3,
            separation=0.85, random_state=42
        )
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_mca_clusters', random_state=42)
        analyzer.data = data
        analyzer.perform_clustering(n_clusters=3)
        analyzer.perform_mca(n_components=2)
        
        # Check that MCA components were created
        assert 'MCA1' in analyzer.data.columns, "Should have MCA1 component"
        assert 'MCA2' in analyzer.data.columns, "Should have MCA2 component"
        
        # Check that MCA results are stored
        assert 'mca' in analyzer.results, "Should store MCA results"
        assert 'explained_variance' in analyzer.results['mca'], "Should have explained variance"

    def test_mca_explained_variance_properties(self):
        """Test MCA explained variance properties."""
        data, _ = generate_synthetic_data_with_clusters(
            n_strains=60, n_traits=10, n_clusters=2, random_state=42
        )
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_mca_var', random_state=42)
        analyzer.data = data
        analyzer.perform_mca(n_components=3)
        
        explained_var = analyzer.results['mca']['explained_variance']
        
        # Should be non-negative
        assert all(explained_var >= 0), "Explained variance should be non-negative"
        
        # Should be decreasing
        assert all(explained_var[i] >= explained_var[i+1] 
                  for i in range(len(explained_var)-1)), \
            "Explained variance should be decreasing"
        
        # First component should explain most
        assert explained_var[0] >= explained_var[1], \
            "First component should explain most variance"


class TestIntegrationWithRealDataPattern:
    """Test using synthetic data that mimics real AMR/virulence data patterns."""

    def test_realistic_amr_pattern(self):
        """Test with realistic AMR-like patterns (correlated resistances)."""
        np.random.seed(42)
        
        # Simulate MDR pattern: some strains resistant to multiple drugs
        n_strains = 80
        
        # Create MDR and non-MDR groups
        mdr_strains = 30
        non_mdr_strains = 50
        
        # MDR strains: high probability of multiple resistances
        mdr_data = np.random.binomial(1, 0.75, (mdr_strains, 12))
        
        # Non-MDR strains: low probability of resistances
        non_mdr_data = np.random.binomial(1, 0.2, (non_mdr_strains, 12))
        
        X = np.vstack([mdr_data, non_mdr_data])
        
        data = pd.DataFrame(X, columns=[f'Antibiotic_{i}' for i in range(12)])
        data['Strain_ID'] = [f'Strain_{i}' for i in range(n_strains)]
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_realistic', random_state=42)
        analyzer.data = data
        analyzer.perform_clustering(n_clusters=2)
        
        # Should separate MDR from non-MDR reasonably well
        true_labels = np.array([0]*mdr_strains + [1]*non_mdr_strains)
        ari = adjusted_rand_score(true_labels, analyzer.clusters - 1)
        
        # Should have some agreement
        assert ari > 0.3, f"Should detect MDR pattern (ARI={ari:.3f})"

    def test_full_workflow_on_synthetic_data(self):
        """Test complete workflow on synthetic data."""
        # Generate comprehensive synthetic dataset
        data, true_labels = generate_synthetic_data_with_clusters(
            n_strains=100, n_traits=20, n_clusters=4,
            separation=0.8, noise_level=0.1, random_state=42
        )
        
        # Run full analysis
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_full_workflow', random_state=42)
        analyzer.data = data
        
        # Clustering
        analyzer.perform_clustering(n_clusters=4)
        assert hasattr(analyzer, 'clusters'), "Should complete clustering"
        
        # Trait associations
        analyzer.calculate_trait_associations(fdr_alpha=0.05)
        assert 'trait_associations' in analyzer.results, "Should have trait associations"
        
        # MCA (if available)
        if HAS_PRINCE:
            analyzer.perform_mca(n_components=2)
            assert 'mca' in analyzer.results, "Should have MCA results"
        
        # Verify output structure
        assert len(analyzer.data) == 100, "Should preserve all strains"
        assert 'Cluster' in analyzer.data.columns, "Should have cluster assignments"
