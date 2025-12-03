# FINAL UNIFIED STREAMLIT APP (ENGLISH VERSION) - UPDATED
#   (1) Unique keys for side-by-side user & reference tree
#   (2) Flexible "Report & Global Export" with user-selected items
#   (3) REPLACED JupyterLab with a Streamlit-Ace Python Editor

import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['DISPLAY'] = ':0'
os.environ["XDG_RUNTIME_DIR"] = "/tmp/runtime-user"

import sys
import io
import requests
from datetime import datetime
import time
import traceback
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from kmodes.kmodes import KModes
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score

try:
    import statsmodels
    from statsmodels.stats.meta_analysis import combine_effects
    statsmodels_available = True
except ImportError:
    combine_effects = None
    statsmodels_available = False

try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    plotly_available = True
except ImportError:
    plotly_available = False

try:
    from st_aggrid import AgGrid, GridOptionsBuilder
    aggrid_available = True
except ImportError:
    aggrid_available = False

try:
    from Bio import Phylo
    bio_available = True
except ImportError:
    bio_available = False

try:
    from ete3 import Tree, TreeStyle
    ete_available = True
except ImportError:
    ete_available = False

try:
    import dendropy
    from dendropy.calculate import treecompare
    dendropy_available = True
except ImportError:
    dendropy_available = False

if dendropy_available:
    GLOBAL_TAXON_NAMESPACE = dendropy.TaxonNamespace()
else:
    GLOBAL_TAXON_NAMESPACE = None

try:
    import openpyxl
except ImportError:
    pass

try:
    from streamlit_ace import st_ace
    ace_available = True
except ImportError:
    ace_available = False

st.set_page_config(page_title="Advanced Data + PhyloViz Analysis", layout="wide")

SESSION_INFO = {
    "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
    "user": "MK-vet"
}

custom_css = """
<style>
    :root {
        --primary-color: #3498db;
        --background-color: #f8f9fa;
        --text-color: #2c3e50;
        --metric-card-bg: white;
    }
    [data-theme="dark"] {
        --primary-color: #1abc9c;
        --background-color: #2c3e50;
        --text-color: #ecf0f1;
        --metric-card-bg: #34495e;
    }
    .main { background-color: var(--background-color) !important; padding: 1rem 3%; }
    h1 { color: var(--primary-color); border-bottom: 2px solid var(--primary-color); }
    .metric-card { background: var(--metric-card-bg); color: var(--text-color); padding: 10px; border-radius: 5px; margin: 5px; }
    .stButton>button {
        background-color: #333333;
        color: #FFFFFF;
    }
    table.dataframe tr th, table.dataframe tr td {
        text-align: left !important;
        white-space: nowrap;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

def show_notification(message, level="info"):
    """Display notification messages with appropriate styling."""
    icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "🚫"}
    icon = icons.get(level, "ℹ️")
    if level == "info":
        st.info(f"{icon} {message}")
    elif level == "success":
        st.success(f"{icon} {message}")
    elif level == "warning":
        st.warning(f"{icon} {message}")
    elif level == "error":
        st.error(f"{icon} {message}")

def handle_analysis_errors(func):
    """Decorator for handling errors in analysis functions."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"Error in {func.__name__}: {e}")
            st.exception(e)
            return None
    return wrapper

def display_table(df, key, use_container_width=True):
    """Display dataframe with AgGrid if available, otherwise use st.dataframe."""
    if df is None or df.empty:
        st.write("DataFrame is empty.")
        return
    if aggrid_available:
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(filter=True, sortable=True, resizable=True)
        gb.configure_grid_options(domLayout='autoHeight')
        gridOptions = gb.build()
        AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True, key=key)
    else:
        st.data_editor(df, use_container_width=use_container_width, key=key)

def fix_dataframe_for_streamlit(df):
    """Fix dataframe data types for Streamlit compatibility."""
    if df is None or df.empty:
        return df
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype("string")
    for col in df.columns:
        if str(df[col].dtype).startswith(('datetime64','timedelta64')):
            df[col] = df[col].astype(str)
    return df

class DataValidator:
    """Validator for data quality checks."""
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_dataframe_structure(self, df, min_rows=1, min_cols=1):
        """Validate basic dataframe structure."""
        if df is None or df.empty:
            self.errors.append("DataFrame is empty or None.")
            return False
        if df.shape[0] < min_rows:
            self.errors.append(f"Not enough rows (found {df.shape[0]}, need >= {min_rows}).")
        if df.shape[1] < min_cols:
            self.errors.append(f"Not enough columns (found {df.shape[1]}, need >= {min_cols}).")
        return True
    
    def get_report(self):
        """Get validation report."""
        return {"errors": self.errors, "warnings": self.warnings}

@st.cache_data
def load_reference_data():
    """Load all reference data files."""
    file_paths = {
        "AMR_genes": "data/AMR_genes.csv",
        "MGE": "data/MGE.csv",
        "MIC": "data/MIC.csv",
        "MLST": "data/MLST.csv",
        "Plasmid": "data/Plasmid.csv",
        "Serotype": "data/Serotype.csv",
        "Virulence": "data/Virulence.csv"
    }
    dataframes = {}
    for k, p in file_paths.items():
        if os.path.exists(p):
            try:
                df_tmp = pd.read_csv(p)
                df_tmp = fix_dataframe_for_streamlit(df_tmp)
                dataframes[k] = df_tmp
            except:
                dataframes[k] = None
        else:
            dataframes[k] = None
    return dataframes

REFERENCE_DATA_DICT = load_reference_data()

# Sidebar configuration
st.sidebar.markdown(f"**Session Info**\n- Date/Time: {SESSION_INFO['timestamp']}\n- User: {SESSION_INFO['user']}")
analysis_mode = st.sidebar.radio("Select Analysis Mode", ["Reference Data Only", "User Data Only", "Compare Reference with User Data"], key="analysis_mode")

st.sidebar.header("Reference Data")
ref_keys_all = [k for k in REFERENCE_DATA_DICT if REFERENCE_DATA_DICT[k] is not None]
sel_refs = st.sidebar.multiselect("Select reference datasets", ref_keys_all, default=ref_keys_all)
ref_dfs = {k: REFERENCE_DATA_DICT[k].copy() for k in sel_refs if REFERENCE_DATA_DICT[k] is not None}

if analysis_mode == "Reference Data Only":
    df_ref = pd.concat(ref_dfs.values(), ignore_index=True) if ref_dfs else pd.DataFrame()
else:
    df_ref = next(iter(ref_dfs.values()), pd.DataFrame()) if ref_dfs else pd.DataFrame()

st.sidebar.header("User Data")
uploaded_user = st.sidebar.file_uploader("Upload user data", type=["csv", "xlsx"])
if uploaded_user:
    try:
        ext = uploaded_user.name.split(".")[-1].lower()
        if ext == "csv":
            df_user = pd.read_csv(uploaded_user)
        else:
            df_user = pd.read_excel(uploaded_user)
        df_user = fix_dataframe_for_streamlit(df_user)
    except Exception as e:
        st.error(f"Error loading user data: {e}")
        df_user = None
else:
    df_user = None

if analysis_mode == "Reference Data Only":
    df_eda = df_viz = df_ref
elif analysis_mode == "User Data Only":
    df_eda = df_viz = df_user
else:
    if (df_user is not None) and (not df_user.empty):
        df_eda = df_viz = df_user
    else:
        df_eda = df_viz = df_ref

# Main tabs
main_tabs = st.tabs(["ETL", "EDA", "Visualizations", "Classification & Clustering", "Statistical Tests", "Phylogenetic Analysis", "Report & Export", "Python Editor"])

# ETL Tab
with main_tabs[0]:
    st.header("ETL (Extract, Transform, Load)")
    current_df = df_ref if df_ref is not None else df_user
    if current_df is not None and not current_df.empty:
        st.write("Data loaded successfully.")
        display_table(current_df.head(20), "etl_preview")
        
        validator = DataValidator()
        validator.validate_dataframe_structure(current_df)
        report = validator.get_report()
        if report['errors']:
            st.error("Validation Errors: " + str(report['errors']))
        else:
            st.success("Data validation passed!")
    else:
        st.warning("No data available. Please load reference or user data.")

# EDA Tab
with main_tabs[1]:
    st.header("Exploratory Data Analysis (EDA)")
    if df_eda is not None and not df_eda.empty:
        st.subheader("Data Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", df_eda.shape[0])
        with col2:
            st.metric("Columns", df_eda.shape[1])
        with col3:
            st.metric("Missing Values", df_eda.isnull().sum().sum())
        
        st.subheader("Statistical Summary")
        st.dataframe(df_eda.describe())
        
        st.subheader("Data Types")
        st.write(df_eda.dtypes)
        
        st.subheader("Missing Values Heatmap")
        if df_eda.isnull().sum().sum() > 0:
            fig = Figure(figsize=(10, 6))
            ax = fig.add_subplot(111)
            sns.heatmap(df_eda.isnull(), cbar=True, cmap="viridis", ax=ax)
            st.pyplot(fig)
        else:
            st.success("No missing values detected!")
    else:
        st.warning("No data available for EDA.")

# Visualizations Tab
with main_tabs[2]:
    st.header("Data Visualizations")
    if df_viz is not None and not df_viz.empty:
        numeric_cols = df_viz.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols:
            st.subheader("Distribution Plots")
            selected_col = st.selectbox("Select column for distribution", numeric_cols, key="dist_col")
            
            fig = Figure(figsize=(10, 6))
            ax = fig.add_subplot(111)
            df_viz[selected_col].hist(bins=30, ax=ax, edgecolor='black')
            ax.set_xlabel(selected_col)
            ax.set_ylabel("Frequency")
            ax.set_title(f"Distribution of {selected_col}")
            st.pyplot(fig)
            
            st.subheader("Correlation Heatmap")
            if len(numeric_cols) > 1:
                fig = Figure(figsize=(12, 8))
                ax = fig.add_subplot(111)
                corr_matrix = df_viz[numeric_cols].corr()
                sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax, fmt='.2f')
                st.pyplot(fig)
            else:
                st.info("Need at least 2 numeric columns for correlation analysis.")
        else:
            st.warning("No numeric columns available for visualization.")
    else:
        st.warning("No data available for visualization.")

# Classification & Clustering Tab
with main_tabs[3]:
    st.header("Classification & Clustering")
    if df_viz is not None and not df_viz.empty:
        numeric_cols = df_viz.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) >= 2:
            st.subheader("K-Means Clustering")
            n_clusters = st.slider("Number of clusters", 2, 10, 3, key="kmeans_clusters")
            
            # Prepare data for clustering
            X = df_viz[numeric_cols].fillna(0)
            
            if st.button("Run K-Means", key="run_kmeans"):
                kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                clusters = kmeans.fit_predict(X)
                
                st.write(f"Cluster assignments: {np.bincount(clusters)}")
                
                # PCA for visualization
                if len(numeric_cols) > 2:
                    pca = PCA(n_components=2)
                    X_pca = pca.fit_transform(X)
                    
                    fig = Figure(figsize=(10, 6))
                    ax = fig.add_subplot(111)
                    scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='viridis')
                    ax.set_xlabel('PC1')
                    ax.set_ylabel('PC2')
                    ax.set_title('K-Means Clustering (PCA)')
                    fig.colorbar(scatter, ax=ax)
                    st.pyplot(fig)
                else:
                    fig = Figure(figsize=(10, 6))
                    ax = fig.add_subplot(111)
                    scatter = ax.scatter(X.iloc[:, 0], X.iloc[:, 1], c=clusters, cmap='viridis')
                    ax.set_xlabel(numeric_cols[0])
                    ax.set_ylabel(numeric_cols[1])
                    ax.set_title('K-Means Clustering')
                    fig.colorbar(scatter, ax=ax)
                    st.pyplot(fig)
        else:
            st.warning("Need at least 2 numeric columns for clustering.")
    else:
        st.warning("No data available for classification/clustering.")

# Statistical Tests Tab
with main_tabs[4]:
    st.header("Statistical Tests")
    if df_viz is not None and not df_viz.empty:
        numeric_cols = df_viz.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) >= 2:
            st.subheader("Correlation Analysis")
            col1_select = st.selectbox("Select first variable", numeric_cols, key="corr_col1")
            col2_select = st.selectbox("Select second variable", numeric_cols, key="corr_col2", index=1 if len(numeric_cols) > 1 else 0)
            
            if st.button("Calculate Correlation", key="calc_corr"):
                data1 = df_viz[col1_select].dropna()
                data2 = df_viz[col2_select].dropna()
                
                # Align the data
                common_idx = data1.index.intersection(data2.index)
                data1 = data1.loc[common_idx]
                data2 = data2.loc[common_idx]
                
                if len(data1) > 2:
                    corr_coef, p_value = stats.pearsonr(data1, data2)
                    
                    st.write(f"**Pearson Correlation Coefficient:** {corr_coef:.4f}")
                    st.write(f"**P-value:** {p_value:.4f}")
                    
                    if p_value < 0.05:
                        st.success("Statistically significant correlation (p < 0.05)")
                    else:
                        st.info("No statistically significant correlation (p >= 0.05)")
                    
                    # Scatter plot
                    fig = Figure(figsize=(8, 6))
                    ax = fig.add_subplot(111)
                    ax.scatter(data1, data2, alpha=0.6)
                    ax.set_xlabel(col1_select)
                    ax.set_ylabel(col2_select)
                    ax.set_title(f'Correlation: {corr_coef:.4f}')
                    
                    # Add regression line
                    z = np.polyfit(data1, data2, 1)
                    p = np.poly1d(z)
                    ax.plot(data1, p(data1), "r--", alpha=0.8)
                    st.pyplot(fig)
                else:
                    st.warning("Not enough data points for correlation analysis.")
            
            st.subheader("T-Test (Independent Samples)")
            st.info("For t-test, please provide grouping variable in your data.")
            
        else:
            st.warning("Need at least 2 numeric columns for statistical tests.")
    else:
        st.warning("No data available for statistical testing.")

# Phylogenetic Analysis Tab
with main_tabs[5]:
    st.header("Phylogenetic Analysis")
    
    tree_file_path = "data/Snp_tree.newick"
    if os.path.exists(tree_file_path):
        st.subheader("Reference Phylogenetic Tree")
        
        try:
            if bio_available:
                # Read and display tree using Biopython
                tree = Phylo.read(tree_file_path, "newick")
                
                st.write("**Tree Statistics:**")
                st.write(f"- Total branches: {tree.count_terminals()}")
                st.write(f"- Total depth: {tree.total_branch_length():.6f}")
                
                # Create matplotlib figure for tree
                fig = Figure(figsize=(12, 8))
                ax = fig.add_subplot(111)
                Phylo.draw(tree, axes=ax, do_show=False)
                st.pyplot(fig)
                
                # Display tree in text format
                with st.expander("View Tree Structure (Text)"):
                    tree_str = io.StringIO()
                    Phylo.draw_ascii(tree, file=tree_str)
                    st.text(tree_str.getvalue())
            else:
                st.warning("Biopython not available. Install it for phylogenetic tree visualization.")
                # Display raw newick string
                with open(tree_file_path, 'r') as f:
                    st.text(f"Tree (Newick format):\n{f.read()}")
        except Exception as e:
            st.error(f"Error loading phylogenetic tree: {e}")
            with open(tree_file_path, 'r') as f:
                st.text(f"Tree (Newick format):\n{f.read()}")
    else:
        st.warning(f"Tree file not found at {tree_file_path}")
    
    st.subheader("Upload Custom Tree")
    uploaded_tree = st.file_uploader("Upload Newick tree file", type=["newick", "nwk", "tree"], key="tree_upload")
    if uploaded_tree and bio_available:
        try:
            tree_content = uploaded_tree.read().decode('utf-8')
            tree = Phylo.read(io.StringIO(tree_content), "newick")
            
            fig = Figure(figsize=(12, 8))
            ax = fig.add_subplot(111)
            Phylo.draw(tree, axes=ax, do_show=False)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error parsing uploaded tree: {e}")

# Report & Export Tab
with main_tabs[6]:
    st.header("Report & Export")
    
    st.subheader("Session Summary")
    st.write(f"**Analysis Mode:** {analysis_mode}")
    st.write(f"**Timestamp:** {SESSION_INFO['timestamp']}")
    st.write(f"**User:** {SESSION_INFO['user']}")
    
    if df_viz is not None and not df_viz.empty:
        st.subheader("Export Data")
        
        export_format = st.selectbox("Select export format", ["CSV", "Excel"], key="export_format")
        
        if st.button("Export Current Data", key="export_data"):
            if export_format == "CSV":
                csv = df_viz.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"strepsuis_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                # Excel export
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_viz.to_excel(writer, index=False, sheet_name='Data')
                excel_data = output.getvalue()
                st.download_button(
                    label="Download Excel",
                    data=excel_data,
                    file_name=f"strepsuis_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    else:
        st.warning("No data available for export.")

# Python Editor Tab
with main_tabs[7]:
    st.header("Python Editor")
    
    if ace_available:
        st.info("Write and execute Python code below. You have access to the loaded data as 'df_viz'.")
        
        default_code = """# Example: Basic data analysis
import pandas as pd
import numpy as np

# Access loaded data
if df_viz is not None:
    print("Data shape:", df_viz.shape)
    print("\\nFirst 5 rows:")
    print(df_viz.head())
    print("\\nColumn names:")
    print(df_viz.columns.tolist())
else:
    print("No data loaded")
"""
        
        code = st_ace(
            value=default_code,
            language="python",
            theme="monokai",
            keybinding="vscode",
            font_size=14,
            tab_size=4,
            show_gutter=True,
            show_print_margin=True,
            wrap=False,
            auto_update=False,
            readonly=False,
            key="python_editor"
        )
        
        if st.button("Execute Code", key="execute_code"):
            try:
                # Create a safe execution environment
                exec_globals = {
                    'df_viz': df_viz,
                    'df_ref': df_ref,
                    'df_user': df_user,
                    'pd': pd,
                    'np': np,
                    'st': st
                }
                
                # Capture output
                old_stdout = sys.stdout
                sys.stdout = captured_output = io.StringIO()
                
                exec(code, exec_globals)
                
                sys.stdout = old_stdout
                output = captured_output.getvalue()
                
                if output:
                    st.subheader("Output:")
                    st.text(output)
                else:
                    st.success("Code executed successfully (no output)")
                    
            except Exception as e:
                st.error(f"Error executing code: {e}")
                st.exception(e)
    else:
        st.warning("streamlit-ace not available. Install it to enable the Python editor.")
        st.info("You can install it with: pip install streamlit-ace")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Streptococcus suis Analyzer**")
st.sidebar.markdown("Version 1.0.0")
st.sidebar.markdown("© 2024 MK-vet")
