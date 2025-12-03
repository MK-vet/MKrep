"""
Streptococcus suis Genomic and Phenotypic Data Analysis Platform

A comprehensive Streamlit application for analyzing genomic and phenotypic data
of Streptococcus suis strains, including AMR genes, virulence factors, MIC values,
MLST profiles, serotypes, and phylogenetic relationships.

Author: MK-vet
License: MIT
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="StrepSuis Analyzer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
DATA_DIR = Path(__file__).parent / "data"
RANDOM_STATE = 42


# ==================== Data Loading Functions ====================

@st.cache_data
def load_data() -> Dict[str, pd.DataFrame]:
    """
    Load all CSV data files from the data directory.
    
    Returns:
        Dictionary mapping data type to DataFrame
    """
    data_files = {
        'AMR': 'AMR_genes.csv',
        'MIC': 'MIC.csv',
        'Virulence': 'Virulence.csv',
        'MLST': 'MLST.csv',
        'Serotype': 'Serotype.csv',
        'MGE': 'MGE.csv',
        'Plasmid': 'Plasmid.csv'
    }
    
    data = {}
    for key, filename in data_files.items():
        filepath = DATA_DIR / filename
        try:
            df = pd.read_csv(filepath)
            # Clean column names
            df.columns = df.columns.str.strip()
            data[key] = df
        except FileNotFoundError:
            st.error(f"Data file not found: {filename}")
            data[key] = pd.DataFrame()
    
    return data


@st.cache_data
def load_phylogenetic_tree() -> Optional[str]:
    """
    Load the phylogenetic tree in Newick format.
    
    Returns:
        Tree string in Newick format or None if not found
    """
    tree_file = DATA_DIR / "Snp_tree.newick"
    try:
        with open(tree_file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        st.warning("Phylogenetic tree file not found")
        return None


# ==================== Statistical Functions ====================

def calculate_shannon_diversity(data: np.ndarray, random_state: int = RANDOM_STATE) -> float:
    """
    Calculate Shannon diversity index for a binary presence/absence matrix.
    
    H = -Σ(p_i * log(p_i))
    
    Args:
        data: Binary numpy array (samples x features)
        random_state: Random seed for reproducibility (reserved for API consistency)
        
    Returns:
        Shannon diversity index
        
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


def calculate_simpson_diversity(data: np.ndarray, random_state: int = RANDOM_STATE) -> float:
    """
    Calculate Simpson diversity index (1 - D) for a binary presence/absence matrix.
    
    D = Σ(p_i^2)
    Simpson = 1 - D
    
    Args:
        data: Binary numpy array (samples x features)
        random_state: Random seed for reproducibility (reserved for API consistency)
        
    Returns:
        Simpson diversity index (1-D)
        
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
    
    Distance = 1 - (intersection / union)
    
    Args:
        x: First binary vector
        y: Second binary vector
        
    Returns:
        Jaccard distance (0-1)
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
    
    Distance = (number of differing positions) / (total positions)
    
    Args:
        x: First binary vector
        y: Second binary vector
        
    Returns:
        Normalized Hamming distance (0-1)
    """
    if len(x) == 0 or len(y) == 0:
        return 1.0
    
    if len(x) != len(y):
        raise ValueError("Vectors must have the same length")
    
    distance = np.sum(x != y) / len(x)
    return float(distance)


def calculate_pairwise_distances(data: np.ndarray, metric: str = 'jaccard') -> np.ndarray:
    """
    Calculate pairwise distance matrix for binary data.
    
    Args:
        data: Binary numpy array (samples x features)
        metric: Distance metric ('jaccard' or 'hamming')
        
    Returns:
        Symmetric distance matrix
    """
    n_samples = data.shape[0]
    distances = np.zeros((n_samples, n_samples))
    
    distance_func = calculate_jaccard_distance if metric == 'jaccard' else calculate_hamming_distance
    
    for i in range(n_samples):
        for j in range(i + 1, n_samples):
            dist = distance_func(data[i], data[j])
            distances[i, j] = dist
            distances[j, i] = dist
    
    return distances


def calculate_prevalence(data: pd.DataFrame, exclude_cols: List[str] = ['Strain_ID']) -> pd.Series:
    """
    Calculate prevalence (%) of each feature in the dataset.
    
    Args:
        data: DataFrame with binary features
        exclude_cols: Columns to exclude from calculation
        
    Returns:
        Series with prevalence percentages
    """
    feature_cols = [col for col in data.columns if col not in exclude_cols]
    
    if len(feature_cols) == 0:
        return pd.Series(dtype=float)
    
    prevalence = (data[feature_cols].sum() / len(data) * 100).sort_values(ascending=False)
    return prevalence


def calculate_correlation_matrix(data: pd.DataFrame, exclude_cols: List[str] = ['Strain_ID']) -> pd.DataFrame:
    """
    Calculate correlation matrix for binary features.
    
    Args:
        data: DataFrame with binary features
        exclude_cols: Columns to exclude from calculation
        
    Returns:
        Correlation matrix
    """
    feature_cols = [col for col in data.columns if col not in exclude_cols]
    
    if len(feature_cols) == 0:
        return pd.DataFrame()
    
    corr_matrix = data[feature_cols].corr()
    return corr_matrix


# ==================== Visualization Functions ====================

def plot_prevalence_bar(prevalence: pd.Series, title: str, top_n: int = 20) -> go.Figure:
    """
    Create a horizontal bar chart for feature prevalence.
    
    Args:
        prevalence: Series with prevalence values
        title: Chart title
        top_n: Number of top features to display
        
    Returns:
        Plotly figure
    """
    top_features = prevalence.head(top_n)
    
    fig = go.Figure(data=[
        go.Bar(
            y=top_features.index,
            x=top_features.values,
            orientation='h',
            marker=dict(
                color=top_features.values,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Prevalence (%)")
            )
        )
    ])
    
    fig.update_layout(
        title=title,
        xaxis_title="Prevalence (%)",
        yaxis_title="Feature",
        height=max(400, top_n * 20),
        showlegend=False
    )
    
    return fig


def plot_heatmap(data: pd.DataFrame, title: str, color_scale: str = 'RdYlBu_r') -> go.Figure:
    """
    Create a heatmap visualization.
    
    Args:
        data: Data to visualize
        title: Chart title
        color_scale: Plotly color scale
        
    Returns:
        Plotly figure
    """
    fig = go.Figure(data=go.Heatmap(
        z=data.values,
        x=data.columns,
        y=data.index,
        colorscale=color_scale,
        hoverongaps=False
    ))
    
    fig.update_layout(
        title=title,
        height=max(400, len(data) * 15),
        xaxis_title="Features",
        yaxis_title="Features"
    )
    
    return fig


def plot_distance_heatmap(distances: np.ndarray, labels: List[str], title: str) -> go.Figure:
    """
    Create a heatmap for distance matrix.
    
    Args:
        distances: Distance matrix
        labels: Sample labels
        title: Chart title
        
    Returns:
        Plotly figure
    """
    fig = go.Figure(data=go.Heatmap(
        z=distances,
        x=labels,
        y=labels,
        colorscale='Blues',
        reversescale=False,
        hoverongaps=False
    ))
    
    fig.update_layout(
        title=title,
        height=600,
        xaxis_title="Strains",
        yaxis_title="Strains"
    )
    
    return fig


def plot_distribution(data: pd.Series, title: str, bins: int = 30) -> go.Figure:
    """
    Create a histogram for data distribution.
    
    Args:
        data: Data series
        title: Chart title
        bins: Number of bins
        
    Returns:
        Plotly figure
    """
    fig = go.Figure(data=[go.Histogram(x=data, nbinsx=bins)])
    
    fig.update_layout(
        title=title,
        xaxis_title="Value",
        yaxis_title="Count",
        showlegend=False
    )
    
    return fig


def plot_pie_chart(data: pd.Series, title: str) -> go.Figure:
    """
    Create a pie chart.
    
    Args:
        data: Value counts series
        title: Chart title
        
    Returns:
        Plotly figure
    """
    fig = go.Figure(data=[go.Pie(labels=data.index, values=data.values)])
    
    fig.update_layout(
        title=title,
        height=400
    )
    
    return fig


# ==================== Main Application ====================

def main():
    """Main Streamlit application"""
    
    # Header
    st.title("🧬 Streptococcus suis Genomic and Phenotypic Data Analyzer")
    st.markdown("""
    Comprehensive platform for analyzing genomic and phenotypic data of *Streptococcus suis* strains.
    Explore AMR genes, virulence factors, MIC profiles, MLST types, serotypes, and phylogenetic relationships.
    """)
    
    # Load data
    with st.spinner("Loading data..."):
        data = load_data()
        tree = load_phylogenetic_tree()
    
    # Sidebar
    st.sidebar.header("📊 Analysis Options")
    
    analysis_type = st.sidebar.selectbox(
        "Select Analysis Type",
        [
            "Overview",
            "AMR Analysis",
            "Virulence Analysis",
            "MIC Analysis",
            "MLST & Serotype",
            "Comparative Analysis",
            "Statistical Summary"
        ]
    )
    
    # Main content based on selection
    if analysis_type == "Overview":
        show_overview(data, tree)
    
    elif analysis_type == "AMR Analysis":
        show_amr_analysis(data)
    
    elif analysis_type == "Virulence Analysis":
        show_virulence_analysis(data)
    
    elif analysis_type == "MIC Analysis":
        show_mic_analysis(data)
    
    elif analysis_type == "MLST & Serotype":
        show_mlst_serotype_analysis(data)
    
    elif analysis_type == "Comparative Analysis":
        show_comparative_analysis(data)
    
    elif analysis_type == "Statistical Summary":
        show_statistical_summary(data)


def show_overview(data: Dict[str, pd.DataFrame], tree: Optional[str]):
    """Display overview of all datasets"""
    st.header("📋 Dataset Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Strains", len(data.get('AMR', pd.DataFrame())))
    
    with col2:
        n_amr = len([col for col in data.get('AMR', pd.DataFrame()).columns if col != 'Strain_ID'])
        st.metric("AMR Genes Tracked", n_amr)
    
    with col3:
        n_vir = len([col for col in data.get('Virulence', pd.DataFrame()).columns if col != 'Strain_ID'])
        st.metric("Virulence Factors Tracked", n_vir)
    
    st.subheader("Dataset Summary")
    
    for name, df in data.items():
        if not df.empty:
            with st.expander(f"{name} Dataset ({len(df)} strains)"):
                st.write(f"**Columns:** {len(df.columns)}")
                st.write(f"**Features:** {len(df.columns) - 1}")  # Exclude Strain_ID
                st.dataframe(df.head(10))
    
    if tree:
        st.subheader("Phylogenetic Tree")
        st.text_area("Newick Format", tree, height=100)


def show_amr_analysis(data: Dict[str, pd.DataFrame]):
    """Display AMR gene analysis"""
    st.header("💊 Antimicrobial Resistance (AMR) Analysis")
    
    amr_data = data.get('AMR')
    if amr_data is None or amr_data.empty:
        st.error("AMR data not available")
        return
    
    # Calculate prevalence
    prevalence = calculate_prevalence(amr_data)
    
    st.subheader("AMR Gene Prevalence")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        top_n = st.slider("Number of genes to display", 5, 30, 20)
        fig = plot_prevalence_bar(prevalence, "Top AMR Genes by Prevalence", top_n)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.metric("Total AMR Genes", len(prevalence))
        st.metric("Most Prevalent Gene", prevalence.index[0] if len(prevalence) > 0 else "N/A")
        st.metric("Max Prevalence", f"{prevalence.iloc[0]:.1f}%" if len(prevalence) > 0 else "N/A")
        
        # Diversity metrics
        amr_matrix = amr_data.drop(columns=['Strain_ID']).values
        shannon = calculate_shannon_diversity(amr_matrix)
        simpson = calculate_simpson_diversity(amr_matrix)
        
        st.metric("Shannon Diversity", f"{shannon:.3f}")
        st.metric("Simpson Diversity", f"{simpson:.3f}")
    
    # Correlation analysis
    st.subheader("AMR Gene Co-occurrence")
    
    if st.checkbox("Show correlation heatmap", value=False):
        corr_matrix = calculate_correlation_matrix(amr_data)
        
        # Filter to top genes only
        top_genes = prevalence.head(15).index.tolist()
        filtered_corr = corr_matrix.loc[top_genes, top_genes]
        
        fig = plot_heatmap(filtered_corr, "AMR Gene Correlation Matrix (Top 15)")
        st.plotly_chart(fig, use_container_width=True)


def show_virulence_analysis(data: Dict[str, pd.DataFrame]):
    """Display virulence factor analysis"""
    st.header("🦠 Virulence Factor Analysis")
    
    vir_data = data.get('Virulence')
    if vir_data is None or vir_data.empty:
        st.error("Virulence data not available")
        return
    
    # Calculate prevalence
    prevalence = calculate_prevalence(vir_data)
    
    st.subheader("Virulence Factor Prevalence")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        top_n = st.slider("Number of factors to display", 5, 30, 20)
        fig = plot_prevalence_bar(prevalence, "Top Virulence Factors by Prevalence", top_n)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.metric("Total Virulence Factors", len(prevalence))
        st.metric("Most Prevalent Factor", prevalence.index[0] if len(prevalence) > 0 else "N/A")
        st.metric("Max Prevalence", f"{prevalence.iloc[0]:.1f}%" if len(prevalence) > 0 else "N/A")
        
        # Diversity metrics
        vir_matrix = vir_data.drop(columns=['Strain_ID']).values
        shannon = calculate_shannon_diversity(vir_matrix)
        simpson = calculate_simpson_diversity(vir_matrix)
        
        st.metric("Shannon Diversity", f"{shannon:.3f}")
        st.metric("Simpson Diversity", f"{simpson:.3f}")


def show_mic_analysis(data: Dict[str, pd.DataFrame]):
    """Display MIC analysis"""
    st.header("🔬 Minimum Inhibitory Concentration (MIC) Analysis")
    
    mic_data = data.get('MIC')
    if mic_data is None or mic_data.empty:
        st.error("MIC data not available")
        return
    
    # Calculate prevalence (resistance)
    prevalence = calculate_prevalence(mic_data)
    
    st.subheader("Antibiotic Resistance Prevalence")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = plot_prevalence_bar(prevalence, "Resistance Prevalence by Antibiotic", len(prevalence))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.metric("Total Antibiotics", len(prevalence))
        resistant_count = (prevalence > 50).sum()
        st.metric("Antibiotics with >50% Resistance", resistant_count)
        
        # Calculate MDR strains (resistant to 3+ antibiotics)
        resistance_per_strain = mic_data.drop(columns=['Strain_ID']).sum(axis=1)
        mdr_strains = (resistance_per_strain >= 3).sum()
        st.metric("MDR Strains (≥3 resistances)", mdr_strains)
        st.metric("MDR Prevalence", f"{mdr_strains / len(mic_data) * 100:.1f}%")
    
    # Distribution of resistance per strain
    st.subheader("Resistance Distribution")
    fig = plot_distribution(resistance_per_strain, "Number of Resistances per Strain")
    st.plotly_chart(fig, use_container_width=True)


def show_mlst_serotype_analysis(data: Dict[str, pd.DataFrame]):
    """Display MLST and serotype analysis"""
    st.header("🔍 MLST and Serotype Analysis")
    
    mlst_data = data.get('MLST')
    serotype_data = data.get('Serotype')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("MLST Distribution")
        if mlst_data is not None and not mlst_data.empty:
            mlst_counts = mlst_data['MLST'].value_counts()
            st.metric("Unique MLST Types", len(mlst_counts))
            
            fig = plot_pie_chart(mlst_counts.head(10), "Top 10 MLST Types")
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("View MLST distribution table"):
                st.dataframe(mlst_counts.reset_index().rename(columns={'index': 'MLST', 'MLST': 'Count'}))
        else:
            st.error("MLST data not available")
    
    with col2:
        st.subheader("Serotype Distribution")
        if serotype_data is not None and not serotype_data.empty:
            serotype_counts = serotype_data['Serotype'].value_counts()
            st.metric("Unique Serotypes", len(serotype_counts))
            
            fig = plot_pie_chart(serotype_counts, "Serotype Distribution")
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("View serotype distribution table"):
                st.dataframe(serotype_counts.reset_index().rename(columns={'index': 'Serotype', 'Serotype': 'Count'}))
        else:
            st.error("Serotype data not available")


def show_comparative_analysis(data: Dict[str, pd.DataFrame]):
    """Display comparative analysis between datasets"""
    st.header("📊 Comparative Analysis")
    
    st.subheader("Strain Similarity Analysis")
    
    # Dataset selection
    dataset = st.selectbox(
        "Select dataset for similarity analysis",
        ["AMR", "Virulence"]
    )
    
    selected_data = data.get(dataset)
    if selected_data is None or selected_data.empty:
        st.error(f"{dataset} data not available")
        return
    
    # Calculate distances
    metric = st.radio("Distance metric", ["Jaccard", "Hamming"])
    metric_lower = metric.lower()
    
    strain_ids = selected_data['Strain_ID'].values
    feature_matrix = selected_data.drop(columns=['Strain_ID']).values
    
    with st.spinner("Calculating pairwise distances..."):
        distances = calculate_pairwise_distances(feature_matrix, metric=metric_lower)
    
    # Display distance heatmap
    n_samples = len(strain_ids)
    if n_samples > 50:
        st.warning(f"Dataset has {n_samples} strains. Showing first 50 for visualization.")
        distances = distances[:50, :50]
        strain_ids = strain_ids[:50]
    
    fig = plot_distance_heatmap(
        distances,
        [str(s) for s in strain_ids],
        f"{dataset} Strain Similarity ({metric} Distance)"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary statistics
    st.subheader("Distance Statistics")
    col1, col2, col3 = st.columns(3)
    
    # Get upper triangle (excluding diagonal)
    triu_indices = np.triu_indices_from(distances, k=1)
    distances_upper = distances[triu_indices]
    
    with col1:
        st.metric("Mean Distance", f"{np.mean(distances_upper):.3f}")
    
    with col2:
        st.metric("Median Distance", f"{np.median(distances_upper):.3f}")
    
    with col3:
        st.metric("Std Dev", f"{np.std(distances_upper):.3f}")


def show_statistical_summary(data: Dict[str, pd.DataFrame]):
    """Display comprehensive statistical summary"""
    st.header("📈 Statistical Summary")
    
    st.subheader("Diversity Indices")
    
    # Create summary table
    summary_data = []
    
    for dataset_name in ['AMR', 'Virulence', 'MIC']:
        dataset = data.get(dataset_name)
        if dataset is not None and not dataset.empty:
            feature_matrix = dataset.drop(columns=['Strain_ID']).values
            
            shannon = calculate_shannon_diversity(feature_matrix)
            simpson = calculate_simpson_diversity(feature_matrix)
            n_features = feature_matrix.shape[1]
            mean_prevalence = np.mean(feature_matrix) * 100
            
            summary_data.append({
                'Dataset': dataset_name,
                'Features': n_features,
                'Shannon Index': f"{shannon:.3f}",
                'Simpson Index': f"{simpson:.3f}",
                'Mean Prevalence (%)': f"{mean_prevalence:.1f}"
            })
    
    summary_df = pd.DataFrame(summary_data)
    st.table(summary_df)
    
    st.subheader("Feature Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**AMR Genes**")
        amr_data = data.get('AMR')
        if amr_data is not None and not amr_data.empty:
            prevalence = calculate_prevalence(amr_data)
            st.write(f"- Total genes: {len(prevalence)}")
            st.write(f"- Genes present in >50% strains: {(prevalence > 50).sum()}")
            st.write(f"- Genes present in <10% strains: {(prevalence < 10).sum()}")
    
    with col2:
        st.write("**Virulence Factors**")
        vir_data = data.get('Virulence')
        if vir_data is not None and not vir_data.empty:
            prevalence = calculate_prevalence(vir_data)
            st.write(f"- Total factors: {len(prevalence)}")
            st.write(f"- Factors present in >50% strains: {(prevalence > 50).sum()}")
            st.write(f"- Factors present in <10% strains: {(prevalence < 10).sum()}")
    
    st.subheader("Resistance Profile")
    
    mic_data = data.get('MIC')
    if mic_data is not None and not mic_data.empty:
        resistance_per_strain = mic_data.drop(columns=['Strain_ID']).sum(axis=1)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Mean Resistances/Strain", f"{resistance_per_strain.mean():.1f}")
        
        with col2:
            st.metric("Median Resistances/Strain", f"{resistance_per_strain.median():.0f}")
        
        with col3:
            st.metric("Max Resistances/Strain", f"{resistance_per_strain.max():.0f}")


if __name__ == "__main__":
    main()
