"""
Integration tests for complete workflows.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import (
    load_data,
    calculate_prevalence,
    calculate_shannon_diversity,
    calculate_simpson_diversity,
    calculate_pairwise_distances,
    calculate_correlation_matrix,
    plot_prevalence_bar,
    plot_heatmap
)


class TestCompleteWorkflow:
    """Test complete analysis workflows."""
    
    @pytest.mark.integration
    def test_amr_analysis_workflow(self):
        """Test complete AMR analysis workflow."""
        # Load data
        data = load_data()
        amr_data = data['AMR']
        
        if amr_data.empty:
            pytest.skip("AMR data not available")
        
        # Calculate prevalence
        prevalence = calculate_prevalence(amr_data)
        assert len(prevalence) > 0
        
        # Calculate diversity
        feature_matrix = amr_data.drop(columns=['Strain_ID']).values
        shannon = calculate_shannon_diversity(feature_matrix)
        simpson = calculate_simpson_diversity(feature_matrix)
        
        assert shannon >= 0
        assert isinstance(simpson, float)
        
        # Calculate correlation
        corr = calculate_correlation_matrix(amr_data)
        assert not corr.empty
        
        # Create visualizations
        fig1 = plot_prevalence_bar(prevalence, "AMR Genes", top_n=10)
        assert fig1 is not None
    
    @pytest.mark.integration
    def test_comparative_analysis_workflow(self):
        """Test comparative analysis workflow."""
        # Load data
        data = load_data()
        amr_data = data['AMR']
        
        if amr_data.empty or len(amr_data) < 2:
            pytest.skip("Insufficient AMR data")
        
        # Get feature matrix
        strain_ids = amr_data['Strain_ID'].values
        feature_matrix = amr_data.drop(columns=['Strain_ID']).values
        
        # Calculate distances
        jaccard_distances = calculate_pairwise_distances(feature_matrix, metric='jaccard')
        hamming_distances = calculate_pairwise_distances(feature_matrix, metric='hamming')
        
        # Check shapes
        n_samples = len(strain_ids)
        assert jaccard_distances.shape == (n_samples, n_samples)
        assert hamming_distances.shape == (n_samples, n_samples)
        
        # Check properties
        assert np.allclose(jaccard_distances, jaccard_distances.T)
        assert np.allclose(hamming_distances, hamming_distances.T)
    
    @pytest.mark.integration
    def test_mdr_detection_workflow(self):
        """Test MDR strain detection workflow."""
        # Load data
        data = load_data()
        mic_data = data['MIC']
        
        if mic_data.empty:
            pytest.skip("MIC data not available")
        
        # Calculate resistances per strain
        resistance_per_strain = mic_data.drop(columns=['Strain_ID']).sum(axis=1)
        
        # Detect MDR strains (≥3 resistances)
        mdr_strains = (resistance_per_strain >= 3).sum()
        
        assert mdr_strains >= 0
        assert mdr_strains <= len(mic_data)
        
        # Calculate MDR prevalence
        mdr_prevalence = mdr_strains / len(mic_data) * 100
        
        assert 0 <= mdr_prevalence <= 100
    
    @pytest.mark.integration
    def test_multi_dataset_analysis(self):
        """Test analysis across multiple datasets."""
        # Load all data
        data = load_data()
        
        results = {}
        
        for dataset_name in ['AMR', 'Virulence', 'MIC']:
            dataset = data.get(dataset_name)
            
            if dataset is not None and not dataset.empty:
                # Calculate diversity metrics
                feature_matrix = dataset.drop(columns=['Strain_ID']).values
                
                shannon = calculate_shannon_diversity(feature_matrix)
                simpson = calculate_simpson_diversity(feature_matrix)
                
                results[dataset_name] = {
                    'shannon': shannon,
                    'simpson': simpson,
                    'n_features': feature_matrix.shape[1],
                    'n_samples': feature_matrix.shape[0]
                }
        
        # Check that we got results for at least one dataset
        assert len(results) > 0
        
        # Validate all results
        for dataset_name, metrics in results.items():
            assert metrics['shannon'] >= 0
            assert isinstance(metrics['simpson'], float)
            assert metrics['n_features'] > 0
            assert metrics['n_samples'] > 0


class TestSyntheticDataValidation:
    """Test with synthetic data to validate edge cases."""
    
    @pytest.mark.unit
    def test_perfect_correlation_workflow(self):
        """Test workflow with perfectly correlated features."""
        # Create synthetic data with perfect correlation
        df = pd.DataFrame({
            'Strain_ID': [f'S{i:03d}' for i in range(10)],
            'gene1': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            'gene2': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],  # Identical to gene1
            'gene3': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],  # Opposite of gene1
        })
        
        # Calculate correlation
        corr = calculate_correlation_matrix(df)
        
        # gene1 and gene2 should be perfectly correlated
        assert abs(corr.loc['gene1', 'gene2'] - 1.0) < 1e-10
        
        # gene1 and gene3 should be negatively correlated
        assert corr.loc['gene1', 'gene3'] < 0
    
    @pytest.mark.unit
    def test_high_diversity_workflow(self):
        """Test workflow with high diversity data."""
        np.random.seed(42)
        
        # Create highly diverse synthetic data
        n_samples = 50
        n_features = 20
        
        # Each feature has random prevalence
        data = np.random.randint(0, 2, (n_samples, n_features))
        
        shannon = calculate_shannon_diversity(data, random_state=42)
        simpson = calculate_simpson_diversity(data, random_state=42)
        
        # High diversity should give reasonable values
        assert shannon > 0
        assert isinstance(simpson, float)
    
    @pytest.mark.unit
    def test_low_diversity_workflow(self):
        """Test workflow with low diversity data."""
        # Create low diversity data (most features are the same)
        df = pd.DataFrame({
            'Strain_ID': [f'S{i:03d}' for i in range(10)],
            'common_gene': [1] * 10,  # Present in all
            'rare_gene1': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Present in 1
            'rare_gene2': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # Present in 1
        })
        
        feature_matrix = df.drop(columns=['Strain_ID']).values
        
        shannon = calculate_shannon_diversity(feature_matrix)
        
        # Low diversity, but still positive
        assert shannon >= 0
    
    @pytest.mark.unit
    def test_sparse_data_workflow(self):
        """Test workflow with very sparse data."""
        # Create sparse data (most values are 0)
        np.random.seed(42)
        
        n_samples = 100
        n_features = 50
        
        # Only 5% of values are 1
        data = (np.random.rand(n_samples, n_features) < 0.05).astype(int)
        
        # Calculate metrics
        prevalence_vals = np.mean(data, axis=0) * 100
        shannon = calculate_shannon_diversity(data, random_state=42)
        
        # Most features should have low prevalence
        assert np.median(prevalence_vals) < 10
        
        # Shannon should still be computable
        assert shannon >= 0
    
    @pytest.mark.unit
    def test_dense_data_workflow(self):
        """Test workflow with very dense data."""
        # Create dense data (most values are 1)
        np.random.seed(42)
        
        n_samples = 100
        n_features = 50
        
        # 95% of values are 1
        data = (np.random.rand(n_samples, n_features) < 0.95).astype(int)
        
        # Calculate metrics
        prevalence_vals = np.mean(data, axis=0) * 100
        simpson = calculate_simpson_diversity(data, random_state=42)
        
        # Most features should have high prevalence
        assert np.median(prevalence_vals) > 90
        
        # Simpson should still be computable
        assert isinstance(simpson, float)


class TestStressTests:
    """Stress tests with extreme conditions."""
    
    @pytest.mark.slow
    def test_large_dataset_performance(self):
        """Test performance with large dataset."""
        np.random.seed(42)
        
        # Create large dataset
        n_samples = 500
        n_features = 100
        
        data = np.random.randint(0, 2, (n_samples, n_features))
        
        # Should complete without hanging
        shannon = calculate_shannon_diversity(data, random_state=42)
        simpson = calculate_simpson_diversity(data, random_state=42)
        
        assert isinstance(shannon, float)
        assert isinstance(simpson, float)
    
    @pytest.mark.slow
    def test_distance_matrix_large(self):
        """Test distance matrix calculation with larger dataset."""
        np.random.seed(42)
        
        # 100 samples x 50 features
        data = np.random.randint(0, 2, (100, 50))
        
        # Calculate distances
        distances = calculate_pairwise_distances(data, metric='jaccard')
        
        # Check properties
        assert distances.shape == (100, 100)
        assert np.allclose(distances, distances.T)
        assert np.allclose(np.diag(distances), 0.0)
    
    @pytest.mark.unit
    def test_edge_case_single_strain(self):
        """Test edge case with single strain."""
        df = pd.DataFrame({
            'Strain_ID': ['S001'],
            'gene1': [1],
            'gene2': [0],
            'gene3': [1]
        })
        
        prevalence = calculate_prevalence(df)
        
        # Should handle single strain
        assert len(prevalence) == 3
        
        # Prevalence should be 0 or 100
        assert all(p in [0.0, 100.0] for p in prevalence.values)
    
    @pytest.mark.unit
    def test_edge_case_two_strains(self):
        """Test edge case with only two strains."""
        df = pd.DataFrame({
            'Strain_ID': ['S001', 'S002'],
            'gene1': [1, 0],
            'gene2': [1, 1],
            'gene3': [0, 0]
        })
        
        feature_matrix = df.drop(columns=['Strain_ID']).values
        
        # Calculate distances
        distances = calculate_pairwise_distances(feature_matrix, metric='jaccard')
        
        assert distances.shape == (2, 2)
        assert distances[0, 0] == 0.0
        assert distances[1, 1] == 0.0
