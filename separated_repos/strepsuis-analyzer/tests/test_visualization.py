"""
Tests for visualization functions.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import (
    plot_prevalence_bar,
    plot_heatmap,
    plot_distance_heatmap,
    plot_distribution,
    plot_pie_chart
)


class TestPlotPrevalenceBar:
    """Test prevalence bar chart creation."""
    
    @pytest.mark.unit
    def test_plot_creates_figure(self):
        """Test that plot_prevalence_bar creates a figure."""
        prevalence = pd.Series([80, 60, 40, 20], index=['gene1', 'gene2', 'gene3', 'gene4'])
        
        fig = plot_prevalence_bar(prevalence, "Test Title", top_n=4)
        
        assert fig is not None
        assert hasattr(fig, 'data')
    
    @pytest.mark.unit
    def test_plot_respects_top_n(self):
        """Test that plot only shows top_n features."""
        prevalence = pd.Series(
            [90, 80, 70, 60, 50, 40, 30, 20, 10, 5],
            index=[f'gene{i}' for i in range(10)]
        )
        
        top_n = 5
        fig = plot_prevalence_bar(prevalence, "Test Title", top_n=top_n)
        
        # Should have one trace with top_n data points
        assert len(fig.data[0].y) == top_n
    
    @pytest.mark.unit
    def test_plot_handles_empty_series(self):
        """Test that plot handles empty series gracefully."""
        prevalence = pd.Series([], dtype=float)
        
        fig = plot_prevalence_bar(prevalence, "Test Title", top_n=10)
        
        assert fig is not None


class TestPlotHeatmap:
    """Test heatmap visualization."""
    
    @pytest.mark.unit
    def test_heatmap_creates_figure(self):
        """Test that plot_heatmap creates a figure."""
        data = pd.DataFrame(np.random.rand(5, 5))
        
        fig = plot_heatmap(data, "Test Heatmap")
        
        assert fig is not None
        assert hasattr(fig, 'data')
    
    @pytest.mark.unit
    def test_heatmap_handles_correlation_matrix(self):
        """Test heatmap with correlation matrix."""
        corr = pd.DataFrame(
            [[1.0, 0.5, -0.3],
             [0.5, 1.0, 0.2],
             [-0.3, 0.2, 1.0]],
            index=['A', 'B', 'C'],
            columns=['A', 'B', 'C']
        )
        
        fig = plot_heatmap(corr, "Correlation Matrix")
        
        assert fig is not None
        assert len(fig.data) > 0


class TestPlotDistanceHeatmap:
    """Test distance heatmap visualization."""
    
    @pytest.mark.unit
    def test_distance_heatmap_creates_figure(self):
        """Test that plot_distance_heatmap creates a figure."""
        distances = np.array([
            [0.0, 0.5, 0.8],
            [0.5, 0.0, 0.3],
            [0.8, 0.3, 0.0]
        ])
        labels = ['S1', 'S2', 'S3']
        
        fig = plot_distance_heatmap(distances, labels, "Distance Matrix")
        
        assert fig is not None
        assert hasattr(fig, 'data')
    
    @pytest.mark.unit
    def test_distance_heatmap_labels(self):
        """Test that distance heatmap uses provided labels."""
        distances = np.eye(3)  # Identity matrix
        labels = ['A', 'B', 'C']
        
        fig = plot_distance_heatmap(distances, labels, "Test")
        
        # Check that labels are used
        assert fig.data[0].x[0] == 'A'
        assert fig.data[0].y[0] == 'A'


class TestPlotDistribution:
    """Test distribution histogram."""
    
    @pytest.mark.unit
    def test_distribution_creates_figure(self):
        """Test that plot_distribution creates a figure."""
        data = pd.Series(np.random.randn(100))
        
        fig = plot_distribution(data, "Test Distribution", bins=20)
        
        assert fig is not None
        assert hasattr(fig, 'data')
    
    @pytest.mark.unit
    def test_distribution_handles_small_data(self):
        """Test distribution with small dataset."""
        data = pd.Series([1, 2, 3, 4, 5])
        
        fig = plot_distribution(data, "Small Dataset")
        
        assert fig is not None


class TestPlotPieChart:
    """Test pie chart visualization."""
    
    @pytest.mark.unit
    def test_pie_chart_creates_figure(self):
        """Test that plot_pie_chart creates a figure."""
        data = pd.Series([30, 20, 15, 10], index=['A', 'B', 'C', 'D'])
        
        fig = plot_pie_chart(data, "Test Pie Chart")
        
        assert fig is not None
        assert hasattr(fig, 'data')
    
    @pytest.mark.unit
    def test_pie_chart_labels(self):
        """Test that pie chart uses correct labels."""
        data = pd.Series([50, 30, 20], index=['Type1', 'Type2', 'Type3'])
        
        fig = plot_pie_chart(data, "Types")
        
        # Check labels
        assert 'Type1' in fig.data[0].labels
        assert 'Type2' in fig.data[0].labels
    
    @pytest.mark.unit
    def test_pie_chart_values(self):
        """Test that pie chart has correct values."""
        data = pd.Series([40, 30, 30], index=['A', 'B', 'C'])
        
        fig = plot_pie_chart(data, "Test")
        
        # Check values
        assert 40 in fig.data[0].values
        assert 30 in fig.data[0].values


class TestVisualizationIntegration:
    """Integration tests for visualizations with real data."""
    
    @pytest.mark.integration
    def test_visualizations_with_sample_data(self, sample_amr_data):
        """Test all visualizations with sample AMR data."""
        from app import calculate_prevalence, calculate_correlation_matrix
        
        # Calculate metrics
        prevalence = calculate_prevalence(sample_amr_data)
        corr = calculate_correlation_matrix(sample_amr_data)
        
        # Create visualizations
        fig1 = plot_prevalence_bar(prevalence, "AMR Prevalence", top_n=4)
        fig2 = plot_heatmap(corr, "AMR Correlation")
        
        # Check figures are created
        assert fig1 is not None
        assert fig2 is not None
    
    @pytest.mark.integration
    def test_distance_heatmap_with_real_distances(self, sample_amr_data):
        """Test distance heatmap with calculated distances."""
        from app import calculate_pairwise_distances
        
        # Get feature matrix
        feature_matrix = sample_amr_data.drop(columns=['Strain_ID']).values
        strain_ids = sample_amr_data['Strain_ID'].values
        
        # Calculate distances
        distances = calculate_pairwise_distances(feature_matrix, metric='jaccard')
        
        # Create visualization
        fig = plot_distance_heatmap(distances, [str(s) for s in strain_ids], "Strain Distances")
        
        assert fig is not None
        assert len(fig.data) > 0
