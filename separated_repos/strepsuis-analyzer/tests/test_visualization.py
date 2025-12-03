"""Tests for visualization module."""

import numpy as np
import pytest
import matplotlib.pyplot as plt
from strepsuis_analyzer.visualization import Visualizer


class TestVisualizer:
    """Test suite for Visualizer class."""

    @pytest.mark.unit
    def test_init(self):
        """Test visualizer initialization."""
        viz = Visualizer()
        assert isinstance(viz, Visualizer)

    @pytest.mark.unit
    def test_create_histogram(self, sample_numeric_data):
        """Test histogram creation."""
        viz = Visualizer()
        fig = viz.create_histogram(sample_numeric_data["var_0"])

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    @pytest.mark.unit
    def test_create_scatter_plot(self, sample_numeric_data):
        """Test scatter plot creation."""
        viz = Visualizer()
        fig = viz.create_scatter_plot(
            sample_numeric_data["var_0"],
            sample_numeric_data["var_1"]
        )

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    @pytest.mark.unit
    def test_create_box_plot(self, sample_numeric_data):
        """Test box plot creation."""
        viz = Visualizer()
        data_dict = {
            "Group1": sample_numeric_data["var_0"][:25],
            "Group2": sample_numeric_data["var_0"][25:],
        }
        fig = viz.create_box_plot(data_dict)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    @pytest.mark.unit
    def test_create_heatmap(self, sample_numeric_data):
        """Test heatmap creation."""
        viz = Visualizer()
        fig = viz.create_heatmap(sample_numeric_data.corr())

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    @pytest.mark.unit
    def test_close_all_figures(self):
        """Test closing all figures."""
        viz = Visualizer()
        viz.create_histogram(np.random.randn(100))
        viz.close_all_figures()

        # Should have no open figures
        assert len(plt.get_fignums()) == 0
