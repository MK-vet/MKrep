"""
Visualization utilities for StrepSuisAnalyzer.

Provides comprehensive visualization capabilities including statistical plots,
heatmaps, phylogenetic trees, and interactive visualizations.
"""

from typing import Dict, List, Optional, Union
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from scipy import stats


class Visualizer:
    """Creates visualizations for genomic and phenotypic data analysis."""

    def __init__(self, style: str = "seaborn-v0_8-darkgrid"):
        """
        Initialize the Visualizer.

        Args:
            style: Matplotlib style to use
        """
        try:
            plt.style.use(style)
        except Exception:
            plt.style.use("default")

        self.fig = None
        self.ax = None

    def create_histogram(
        self,
        data: Union[pd.Series, np.ndarray],
        bins: int = 30,
        title: str = "Histogram",
        xlabel: str = "Value",
        ylabel: str = "Frequency",
        color: str = "steelblue",
    ) -> plt.Figure:
        """
        Create a histogram.

        Args:
            data: Data to plot
            bins: Number of bins
            title: Plot title
            xlabel: X-axis label
            ylabel: Y-axis label
            color: Bar color

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        data_arr = np.asarray(data)
        data_clean = data_arr[~np.isnan(data_arr)]

        ax.hist(data_clean, bins=bins, color=color, edgecolor="black", alpha=0.7)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def create_scatter_plot(
        self,
        x: Union[pd.Series, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        title: str = "Scatter Plot",
        xlabel: str = "X",
        ylabel: str = "Y",
        color: str = "steelblue",
        show_regression: bool = False,
    ) -> plt.Figure:
        """
        Create a scatter plot.

        Args:
            x: X-axis data
            y: Y-axis data
            title: Plot title
            xlabel: X-axis label
            ylabel: Y-axis label
            color: Point color
            show_regression: Whether to show regression line

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        x_arr = np.asarray(x)
        y_arr = np.asarray(y)

        # Remove NaN
        mask = ~(np.isnan(x_arr) | np.isnan(y_arr))
        x_clean = x_arr[mask]
        y_clean = y_arr[mask]

        ax.scatter(x_clean, y_clean, color=color, alpha=0.6, s=50, edgecolors="black")

        if show_regression and len(x_clean) > 2:
            # Add regression line
            z = np.polyfit(x_clean, y_clean, 1)
            p = np.poly1d(z)
            x_line = np.linspace(x_clean.min(), x_clean.max(), 100)
            ax.plot(x_line, p(x_line), "r--", linewidth=2, label="Regression line")
            ax.legend()

        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def create_box_plot(
        self,
        data_dict: Dict[str, Union[pd.Series, np.ndarray]],
        title: str = "Box Plot",
        ylabel: str = "Value",
    ) -> plt.Figure:
        """
        Create a box plot for multiple groups.

        Args:
            data_dict: Dictionary mapping group names to data
            title: Plot title
            ylabel: Y-axis label

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        data_list = []
        labels = []
        for label, data in data_dict.items():
            data_arr = np.asarray(data)
            data_clean = data_arr[~np.isnan(data_arr)]
            if len(data_clean) > 0:
                data_list.append(data_clean)
                labels.append(label)

        if data_list:
            bp = ax.boxplot(data_list, labels=labels, patch_artist=True)
            for patch in bp["boxes"]:
                patch.set_facecolor("lightblue")
                patch.set_alpha(0.7)

        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, alpha=0.3, axis="y")

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        return fig

    def create_violin_plot(
        self,
        data_dict: Dict[str, Union[pd.Series, np.ndarray]],
        title: str = "Violin Plot",
        ylabel: str = "Value",
    ) -> plt.Figure:
        """
        Create a violin plot for multiple groups.

        Args:
            data_dict: Dictionary mapping group names to data
            title: Plot title
            ylabel: Y-axis label

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        # Prepare data for seaborn
        df_list = []
        for label, data in data_dict.items():
            data_arr = np.asarray(data)
            data_clean = data_arr[~np.isnan(data_arr)]
            if len(data_clean) > 0:
                df_list.append(pd.DataFrame({"Group": label, "Value": data_clean}))

        if df_list:
            df = pd.concat(df_list, ignore_index=True)
            sns.violinplot(data=df, x="Group", y="Value", ax=ax)

        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, alpha=0.3, axis="y")

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        return fig

    def create_heatmap(
        self,
        data: pd.DataFrame,
        title: str = "Heatmap",
        cmap: str = "viridis",
        annot: bool = False,
        fmt: str = ".2f",
    ) -> plt.Figure:
        """
        Create a heatmap.

        Args:
            data: Data to plot (2D DataFrame)
            title: Plot title
            cmap: Color map
            annot: Whether to annotate cells
            fmt: Format string for annotations

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(12, 10))

        sns.heatmap(data, cmap=cmap, annot=annot, fmt=fmt, ax=ax, cbar_kws={"shrink": 0.8})

        ax.set_title(title, fontsize=14, fontweight="bold")
        plt.tight_layout()
        return fig

    def create_qq_plot(
        self, data: Union[pd.Series, np.ndarray], title: str = "Q-Q Plot"
    ) -> plt.Figure:
        """
        Create a Q-Q plot.

        Args:
            data: Data to plot
            title: Plot title

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(8, 8))

        data_arr = np.asarray(data)
        data_clean = data_arr[~np.isnan(data_arr)]

        stats.probplot(data_clean, dist="norm", plot=ax)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def create_correlation_heatmap(
        self,
        df: pd.DataFrame,
        method: str = "pearson",
        title: str = "Correlation Heatmap",
    ) -> plt.Figure:
        """
        Create a correlation matrix heatmap.

        Args:
            df: DataFrame with numeric columns
            method: Correlation method
            title: Plot title

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(12, 10))

        # Compute correlation matrix
        corr = df.corr(method=method)

        # Create heatmap
        sns.heatmap(
            corr,
            cmap="coolwarm",
            center=0,
            annot=True,
            fmt=".2f",
            ax=ax,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
        )

        ax.set_title(title, fontsize=14, fontweight="bold")
        plt.tight_layout()
        return fig

    def create_plotly_scatter(
        self,
        x: Union[pd.Series, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        title: str = "Interactive Scatter Plot",
        xlabel: str = "X",
        ylabel: str = "Y",
        hover_text: Optional[List[str]] = None,
    ) -> go.Figure:
        """
        Create an interactive scatter plot using Plotly.

        Args:
            x: X-axis data
            y: Y-axis data
            title: Plot title
            xlabel: X-axis label
            ylabel: Y-axis label
            hover_text: Optional hover text for each point

        Returns:
            Plotly figure
        """
        fig = go.Figure()

        x_arr = np.asarray(x)
        y_arr = np.asarray(y)

        fig.add_trace(
            go.Scatter(
                x=x_arr,
                y=y_arr,
                mode="markers",
                marker=dict(size=8, color="steelblue", opacity=0.6),
                text=hover_text,
                hovertemplate="<b>%{text}</b><br>" + f"{xlabel}: %{{x}}<br>{ylabel}: %{{y}}"
                if hover_text
                else None,
            )
        )

        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            template="plotly_white",
            hovermode="closest",
        )

        return fig

    def create_bar_plot(
        self,
        categories: List[str],
        values: List[float],
        title: str = "Bar Plot",
        xlabel: str = "Category",
        ylabel: str = "Value",
        color: str = "steelblue",
    ) -> plt.Figure:
        """
        Create a bar plot.

        Args:
            categories: Category labels
            values: Values for each category
            title: Plot title
            xlabel: X-axis label
            ylabel: Y-axis label
            color: Bar color

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        x_pos = np.arange(len(categories))
        ax.bar(x_pos, values, color=color, alpha=0.7, edgecolor="black")

        ax.set_xticks(x_pos)
        ax.set_xticklabels(categories, rotation=45, ha="right")
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, alpha=0.3, axis="y")

        plt.tight_layout()
        return fig

    def save_figure(self, fig, filepath: str, dpi: int = 300):
        """
        Save a matplotlib figure to file.

        Args:
            fig: Matplotlib figure
            filepath: Output file path
            dpi: Resolution in dots per inch
        """
        fig.savefig(filepath, dpi=dpi, bbox_inches="tight")

    def close_all_figures(self):
        """Close all matplotlib figures."""
        plt.close("all")
