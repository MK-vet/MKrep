"""
Main Streamlit application for StrepSuisAnalyzer.

Provides interactive web interface for comprehensive genomic and phenotypic analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from statistical_analysis import StatisticalAnalyzer
from phylogenetic_utils import PhylogeneticAnalyzer
from visualization import Visualizer
from report_generator import ReportGenerator

# Page configuration
st.set_page_config(
    page_title="StrepSuisAnalyzer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False
if "dataframes" not in st.session_state:
    st.session_state.dataframes = {}


def main():
    """Main application function."""
    st.title("🧬 StrepSuisAnalyzer")
    st.markdown("### Interactive Analysis of *Streptococcus suis* Genomic and Phenotypic Data")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Select Analysis",
        [
            "Home",
            "Data Loading",
            "Data Explorer",
            "Statistical Analysis",
            "Visualization",
            "Clustering",
            "Phylogenetic Analysis",
            "Report Generation",
        ],
    )

    if page == "Home":
        show_home()
    elif page == "Data Loading":
        show_data_loading()
    elif page == "Data Explorer":
        show_data_explorer()
    elif page == "Statistical Analysis":
        show_statistical_analysis()
    elif page == "Visualization":
        show_visualization()
    elif page == "Clustering":
        show_clustering()
    elif page == "Phylogenetic Analysis":
        show_phylogenetic_analysis()
    elif page == "Report Generation":
        show_report_generation()


def show_home():
    """Show home page."""
    st.header("Welcome to StrepSuisAnalyzer")

    st.markdown("""
    **StrepSuisAnalyzer** is a comprehensive interactive tool for analyzing *Streptococcus suis*
    genomic and phenotypic data.

    ### Features:
    - 📊 **Exploratory Data Analysis**: Descriptive statistics, normality tests, correlations
    - 📈 **Visualization**: Histograms, scatter plots, heatmaps, Q-Q plots
    - 🧪 **Statistical Tests**: t-tests, ANOVA, Mann-Whitney U, Kruskal-Wallis
    - 🔬 **Meta-Analysis**: Fixed and random effects models
    - 🌳 **Phylogenetic Analysis**: Tree visualization, RF distance, bipartition comparison
    - 📋 **Clustering**: K-Means, K-Modes, Hierarchical, DBSCAN
    - 📄 **Report Generation**: Export results to Excel and HTML

    ### Getting Started:
    1. Navigate to **Data Loading** to upload your datasets
    2. Explore your data in **Data Explorer**
    3. Perform statistical analyses and create visualizations
    4. Generate comprehensive reports

    ### Supported Data Types:
    - AMR genes (binary presence/absence)
    - MIC values (numeric)
    - Virulence factors (binary)
    - MLST data
    - Serotypes
    - Plasmid data
    - Mobile genetic elements (MGE)
    - Phylogenetic trees (Newick format)
    """)


def show_data_loading():
    """Show data loading page."""
    st.header("Data Loading")

    st.markdown("Upload your datasets or use example data")

    # Option to use example data
    use_example = st.checkbox("Use example data")

    if use_example:
        st.info("Loading example datasets...")
        data_dir = Path(__file__).parent.parent.parent / "data"

        # Load example data files
        try:
            if (data_dir / "AMR_genes.csv").exists():
                st.session_state.dataframes["AMR_genes"] = pd.read_csv(
                    data_dir / "AMR_genes.csv", index_col=0
                )
            if (data_dir / "MIC.csv").exists():
                st.session_state.dataframes["MIC"] = pd.read_csv(
                    data_dir / "MIC.csv", index_col=0
                )
            if (data_dir / "Virulence.csv").exists():
                st.session_state.dataframes["Virulence"] = pd.read_csv(
                    data_dir / "Virulence.csv", index_col=0
                )
            if (data_dir / "MLST.csv").exists():
                st.session_state.dataframes["MLST"] = pd.read_csv(
                    data_dir / "MLST.csv", index_col=0
                )
            if (data_dir / "Serotype.csv").exists():
                st.session_state.dataframes["Serotype"] = pd.read_csv(
                    data_dir / "Serotype.csv", index_col=0
                )

            st.session_state.data_loaded = True
            st.success(f"Loaded {len(st.session_state.dataframes)} datasets")

        except Exception as e:
            st.error(f"Error loading example data: {e}")

    # File uploaders
    st.subheader("Upload Custom Data")

    uploaded_files = st.file_uploader(
        "Upload CSV files",
        type=["csv"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                df = pd.read_csv(uploaded_file, index_col=0)
                name = uploaded_file.name.replace(".csv", "")
                st.session_state.dataframes[name] = df
                st.success(f"Loaded {name}: {df.shape[0]} rows × {df.shape[1]} columns")
            except Exception as e:
                st.error(f"Error loading {uploaded_file.name}: {e}")

        st.session_state.data_loaded = True

    # Show loaded datasets
    if st.session_state.dataframes:
        st.subheader("Loaded Datasets")
        for name, df in st.session_state.dataframes.items():
            st.write(f"**{name}**: {df.shape[0]} rows × {df.shape[1]} columns")


def show_data_explorer():
    """Show data explorer page."""
    st.header("Data Explorer")

    if not st.session_state.data_loaded:
        st.warning("Please load data first in the Data Loading page")
        return

    # Select dataset
    dataset_name = st.selectbox("Select Dataset", list(st.session_state.dataframes.keys()))

    if dataset_name:
        df = st.session_state.dataframes[dataset_name]

        # Display basic info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", df.shape[0])
        with col2:
            st.metric("Columns", df.shape[1])
        with col3:
            st.metric("Missing Values", df.isnull().sum().sum())

        # Show data
        st.subheader("Data Preview")
        st.dataframe(df.head(20))

        # Descriptive statistics
        st.subheader("Descriptive Statistics")
        st.dataframe(df.describe())


def show_statistical_analysis():
    """Show statistical analysis page."""
    st.header("Statistical Analysis")

    if not st.session_state.data_loaded:
        st.warning("Please load data first")
        return

    analysis_type = st.selectbox(
        "Select Analysis",
        [
            "Correlation Analysis",
            "Normality Test",
            "T-Test",
            "ANOVA",
            "Mann-Whitney U",
            "Kruskal-Wallis",
        ],
    )

    dataset_name = st.selectbox("Select Dataset", list(st.session_state.dataframes.keys()))
    df = st.session_state.dataframes[dataset_name]

    analyzer = StatisticalAnalyzer(random_state=42)

    if analysis_type == "Correlation Analysis":
        st.subheader("Correlation Analysis")

        method = st.selectbox("Method", ["pearson", "spearman", "kendall"])

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if len(numeric_cols) >= 2:
            col1 = st.selectbox("Variable 1", numeric_cols, key="corr_col1")
            col2 = st.selectbox("Variable 2", numeric_cols, key="corr_col2")

            if st.button("Calculate Correlation"):
                corr, pval = analyzer.compute_correlation(df[col1], df[col2], method=method)

                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Correlation Coefficient", f"{corr:.4f}")
                with col_b:
                    st.metric("P-value", f"{pval:.4e}")

    elif analysis_type == "Normality Test":
        st.subheader("Shapiro-Wilk Normality Test")

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        col = st.selectbox("Select Variable", numeric_cols)

        if st.button("Test Normality"):
            stat, pval, is_normal = analyzer.test_normality(df[col])

            st.write(f"**Statistic:** {stat:.4f}")
            st.write(f"**P-value:** {pval:.4e}")
            st.write(f"**Is Normal (α=0.05):** {is_normal}")


def show_visualization():
    """Show visualization page."""
    st.header("Data Visualization")

    if not st.session_state.data_loaded:
        st.warning("Please load data first")
        return

    viz_type = st.selectbox(
        "Select Visualization",
        ["Histogram", "Scatter Plot", "Box Plot", "Heatmap", "Q-Q Plot"],
    )

    dataset_name = st.selectbox("Select Dataset", list(st.session_state.dataframes.keys()))
    df = st.session_state.dataframes[dataset_name]

    visualizer = Visualizer()

    if viz_type == "Histogram":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        col = st.selectbox("Select Variable", numeric_cols)
        bins = st.slider("Number of Bins", 10, 100, 30)

        if st.button("Create Histogram"):
            fig = visualizer.create_histogram(df[col], bins=bins, title=f"Histogram of {col}")
            st.pyplot(fig)

    elif viz_type == "Scatter Plot":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if len(numeric_cols) >= 2:
            x_col = st.selectbox("X Variable", numeric_cols, key="scatter_x")
            y_col = st.selectbox("Y Variable", numeric_cols, key="scatter_y")
            show_regression = st.checkbox("Show Regression Line")

            if st.button("Create Scatter Plot"):
                fig = visualizer.create_scatter_plot(
                    df[x_col],
                    df[y_col],
                    xlabel=x_col,
                    ylabel=y_col,
                    show_regression=show_regression,
                )
                st.pyplot(fig)


def show_clustering():
    """Show clustering analysis page."""
    st.header("Clustering Analysis")

    if not st.session_state.data_loaded:
        st.warning("Please load data first")
        return

    st.markdown("Clustering analysis will be performed on selected dataset")

    dataset_name = st.selectbox("Select Dataset", list(st.session_state.dataframes.keys()))

    cluster_method = st.selectbox("Select Method", ["K-Means", "K-Modes", "Hierarchical", "DBSCAN"])

    st.info(f"Selected: {cluster_method} on dataset {dataset_name}")


def show_phylogenetic_analysis():
    """Show phylogenetic analysis page."""
    st.header("Phylogenetic Analysis")

    st.markdown("Upload phylogenetic tree in Newick format")

    tree_file = st.file_uploader("Upload Tree (Newick)", type=["newick", "nwk", "tree", "txt"])

    if tree_file:
        tree_string = tree_file.read().decode("utf-8")

        analyzer = PhylogeneticAnalyzer()

        if analyzer.load_tree_from_newick(tree_string):
            st.success("Tree loaded successfully")

            leaf_names = analyzer.get_leaf_names()
            st.write(f"**Number of taxa:** {len(leaf_names)}")
            st.write(f"**Tree depth:** {analyzer.get_tree_depth():.4f}")

            with st.expander("Leaf Names"):
                st.write(leaf_names)
        else:
            st.error("Failed to load tree")


def show_report_generation():
    """Show report generation page."""
    st.header("Report Generation")

    if not st.session_state.data_loaded:
        st.warning("Please load data first")
        return

    st.markdown("Generate comprehensive analysis reports")

    report_gen = ReportGenerator()

    # Select datasets to include
    selected_datasets = st.multiselect(
        "Select datasets to include", list(st.session_state.dataframes.keys())
    )

    report_name = st.text_input("Report Name", "analysis_report")

    if st.button("Generate Excel Report"):
        if selected_datasets:
            for name in selected_datasets:
                report_gen.add_dataframe(name, st.session_state.dataframes[name])

            output_path = f"{report_name}.xlsx"
            report_gen.export_to_excel(output_path)

            st.success(f"Report generated: {output_path}")

            # Provide download button
            with open(output_path, "rb") as f:
                st.download_button(
                    "Download Report",
                    f,
                    file_name=output_path,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
        else:
            st.warning("Please select at least one dataset")


if __name__ == "__main__":
    main()
