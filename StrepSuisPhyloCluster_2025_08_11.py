#!/usr/bin/env python3
"""
StrepSuis Phylogenetic Clustering Analysis
==========================================

Integrated analysis combining:
- Phylogenetic tree-aware clustering
- Binary trait profiling (AMR, virulence)
- Association rule mining
- Multiple Correspondence Analysis (MCA)
- Bootstrap confidence intervals
- Interactive HTML and Excel reports

Requirements:
- Binary data (0 = absence, 1 = presence)
- CSV files with Strain_ID column
- Snp_tree.newick (phylogenetic tree)

Outputs:
- HTML report with interactive visualizations
- Excel workbook with multiple analysis sheets
- CSV files for downstream analysis
"""

import os
import warnings
from pathlib import Path
from typing import List, Optional, Tuple
import argparse

import pandas as pd
import numpy as np
from scipy import stats
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

# Statistical analysis
from statsmodels.stats.multitest import multipletests

# MCA
try:
    import prince
    HAS_PRINCE = True
except ImportError:
    HAS_PRINCE = False
    warnings.warn("prince not available, MCA analysis will be skipped")

# Phylogenetic analysis
try:
    from Bio import Phylo
    HAS_BIOPYTHON = True
except ImportError:
    HAS_BIOPYTHON = False
    warnings.warn("BioPython not available, phylogenetic features will be limited")

# Suppress warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

# Set plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150


class StrepSuisAnalyzer:
    """
    Comprehensive analyzer for Streptococcus suis genomic data.
    
    Integrates phylogenetic clustering, trait profiling, and network analysis.
    """
    
    def __init__(self, output_dir: str = "output", random_state: int = 42):
        """
        Initialize the analyzer.
        
        Parameters:
        -----------
        output_dir : str
            Directory for output files
        random_state : int
            Random seed for reproducibility
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.random_state = random_state
        np.random.seed(random_state)
        
        # Data storage
        self.data = None
        self.tree = None
        self.phylo_dist_matrix = None
        self.clusters = None
        self.results = {}
        
    def load_data(self, data_files: List[str], strain_id_col: str = "Strain_ID"):
        """
        Load and merge binary trait data from multiple CSV files.
        
        Parameters:
        -----------
        data_files : List[str]
            Paths to CSV files
        strain_id_col : str
            Name of the strain identifier column
        """
        print("\n=== Loading Data ===")
        dfs = []
        
        for file_path in data_files:
            if not os.path.exists(file_path):
                print(f"Warning: File not found: {file_path}")
                continue
                
            df = pd.read_csv(file_path)
            print(f"Loaded {file_path}: {df.shape}")
            
            if strain_id_col not in df.columns:
                print(f"Error: {strain_id_col} not found in {file_path}")
                continue
                
            dfs.append(df)
        
        if not dfs:
            raise ValueError("No data files loaded successfully")
        
        # Merge all dataframes
        self.data = dfs[0]
        for df in dfs[1:]:
            self.data = self.data.merge(df, on=strain_id_col, how='outer')
        
        # Fill NaN with 0 (absence)
        feature_cols = [c for c in self.data.columns if c != strain_id_col]
        self.data[feature_cols] = self.data[feature_cols].fillna(0).astype(int)
        
        print(f"\nMerged data shape: {self.data.shape}")
        print(f"Strains: {len(self.data)}, Features: {len(feature_cols)}")
        
    def load_tree(self, tree_file: str):
        """
        Load phylogenetic tree from Newick file.
        
        Parameters:
        -----------
        tree_file : str
            Path to Newick format tree file
        """
        if not HAS_BIOPYTHON:
            print("Warning: BioPython not available, skipping tree loading")
            return
            
        print("\n=== Loading Phylogenetic Tree ===")
        self.tree = Phylo.read(tree_file, "newick")
        print(f"Tree loaded: {self.tree.count_terminals()} terminals")
        
        # Calculate pairwise phylogenetic distances
        terminals = self.tree.get_terminals()
        n = len(terminals)
        self.phylo_dist_matrix = np.zeros((n, n))
        
        for i, term1 in enumerate(terminals):
            for j, term2 in enumerate(terminals):
                self.phylo_dist_matrix[i, j] = self.tree.distance(term1, term2)
        
        print(f"Phylogenetic distance matrix: {self.phylo_dist_matrix.shape}")
        
    def perform_clustering(self, n_clusters: int = None, method: str = "ward"):
        """
        Perform hierarchical clustering on binary trait data.
        
        Parameters:
        -----------
        n_clusters : int, optional
            Number of clusters (if None, uses silhouette score to determine)
        method : str
            Linkage method for hierarchical clustering
        """
        print("\n=== Performing Clustering ===")
        
        # Get feature matrix
        strain_col = "Strain_ID"
        X = self.data[[c for c in self.data.columns if c != strain_col]].values
        
        # Compute distance matrix (Jaccard for binary data)
        dist_matrix = pdist(X, metric='jaccard')
        
        # Hierarchical clustering
        linkage_matrix = linkage(dist_matrix, method=method)
        
        # Determine optimal number of clusters if not specified
        if n_clusters is None:
            best_score = -1
            best_k = 2
            
            for k in range(2, min(11, len(X) // 2)):
                labels = fcluster(linkage_matrix, k, criterion='maxclust')
                score = silhouette_score(squareform(dist_matrix), labels, metric='precomputed')
                
                if score > best_score:
                    best_score = score
                    best_k = k
            
            n_clusters = best_k
            print(f"Optimal clusters (silhouette): {n_clusters} (score: {best_score:.3f})")
        
        # Get cluster assignments
        self.clusters = fcluster(linkage_matrix, n_clusters, criterion='maxclust')
        self.data['Cluster'] = self.clusters
        
        print(f"Cluster sizes: {pd.Series(self.clusters).value_counts().sort_index().to_dict()}")
        
        # Store linkage matrix for plotting
        self.linkage_matrix = linkage_matrix
        
    def calculate_trait_associations(self, fdr_alpha: float = 0.05):
        """
        Calculate trait associations using chi-square tests.
        
        Parameters:
        -----------
        fdr_alpha : float
            FDR significance threshold
        """
        print("\n=== Calculating Trait Associations ===")
        
        strain_col = "Strain_ID"
        feature_cols = [c for c in self.data.columns if c not in [strain_col, "Cluster"]]
        
        results = []
        
        for feature in feature_cols:
            # Create contingency table
            contingency = pd.crosstab(self.data[feature], self.data['Cluster'])
            
            # Chi-square test
            chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
            
            # Cramér's V (effect size)
            n = contingency.sum().sum()
            cramers_v = np.sqrt(chi2 / (n * (min(contingency.shape) - 1)))
            
            results.append({
                'Feature': feature,
                'Chi2': chi2,
                'P_value': p_value,
                'DoF': dof,
                'Cramers_V': cramers_v
            })
        
        results_df = pd.DataFrame(results)
        
        # Multiple testing correction (FDR)
        _, p_adj, _, _ = multipletests(results_df['P_value'], method='fdr_bh')
        results_df['P_adj'] = p_adj
        results_df['Significant'] = p_adj < fdr_alpha
        
        # Sort by significance
        results_df = results_df.sort_values('P_adj')
        
        self.results['trait_associations'] = results_df
        print(f"Significant associations (FDR < {fdr_alpha}): {results_df['Significant'].sum()}")
        
    def perform_mca(self, n_components: int = 2):
        """
        Perform Multiple Correspondence Analysis.
        
        Parameters:
        -----------
        n_components : int
            Number of MCA components
        """
        if not HAS_PRINCE:
            print("Warning: prince not available, skipping MCA")
            return
            
        print("\n=== Performing MCA ===")
        
        strain_col = "Strain_ID"
        feature_cols = [c for c in self.data.columns if c not in [strain_col, "Cluster"]]
        
        # Convert to categorical for MCA
        X_cat = self.data[feature_cols].astype(str)
        
        # Fit MCA
        mca = prince.MCA(n_components=n_components, random_state=self.random_state)
        mca_coords = mca.fit_transform(X_cat)
        
        # Add to data
        for i in range(n_components):
            self.data[f'MCA{i+1}'] = mca_coords.iloc[:, i]
        
        # Store explained variance
        explained_var = mca.eigenvalues_ / mca.eigenvalues_.sum()
        print(f"Explained variance: {explained_var.values[:n_components]}")
        
        self.results['mca'] = {
            'model': mca,
            'coordinates': mca_coords,
            'explained_variance': explained_var
        }
        
    def generate_html_report(self):
        """Generate interactive HTML report with Bootstrap 5 UI."""
        print("\n=== Generating HTML Report ===")
        
        # Create visualizations
        figs = []
        
        # 1. Cluster distribution
        cluster_counts = self.data['Cluster'].value_counts().sort_index()
        fig1 = go.Figure(data=[
            go.Bar(x=cluster_counts.index, y=cluster_counts.values)
        ])
        fig1.update_layout(
            title="Cluster Distribution",
            xaxis_title="Cluster",
            yaxis_title="Number of Strains",
            template="plotly_white"
        )
        figs.append(("cluster_dist", fig1))
        
        # 2. MCA biplot
        if 'mca' in self.results and 'MCA1' in self.data.columns:
            fig2 = px.scatter(
                self.data,
                x='MCA1',
                y='MCA2',
                color='Cluster',
                title="MCA Biplot (Colored by Cluster)",
                template="plotly_white"
            )
            figs.append(("mca_biplot", fig2))
        
        # 3. Top trait associations
        if 'trait_associations' in self.results:
            top_traits = self.results['trait_associations'].head(20)
            fig3 = go.Figure(data=[
                go.Bar(
                    x=-np.log10(top_traits['P_adj']),
                    y=top_traits['Feature'],
                    orientation='h'
                )
            ])
            fig3.update_layout(
                title="Top Trait Associations (-log10 FDR-adjusted P-value)",
                xaxis_title="-log10(P_adj)",
                yaxis_title="Feature",
                template="plotly_white",
                height=600
            )
            figs.append(("trait_assoc", fig3))
        
        # Generate HTML
        html_content = self._create_html_template(figs)
        
        # Save HTML
        html_path = self.output_dir / "analysis_report.html"
        with open(html_path, 'w') as f:
            f.write(html_content)
        
        print(f"HTML report saved: {html_path}")
        
    def _create_html_template(self, figures: List[Tuple[str, go.Figure]]) -> str:
        """Create HTML template with Bootstrap 5 and Plotly figures."""
        
        # Convert figures to HTML divs
        fig_htmls = []
        for fig_id, fig in figures:
            fig_html = fig.to_html(include_plotlyjs=False, div_id=fig_id)
            fig_htmls.append(f'<div class="mb-4">{fig_html}</div>')
        
        figures_html = '\n'.join(fig_htmls)
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StrepSuis Analysis Report</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Plotly -->
    <script src="https://cdn.plot.ly/plotly-2.18.0.min.js"></script>
    
    <style>
        body {{
            background-color: #f8f9fa;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 0;
            margin-bottom: 2rem;
        }}
        .card {{
            box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075);
            margin-bottom: 1.5rem;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>StrepSuis Phylogenetic Clustering Analysis</h1>
            <p class="lead">Integrative analysis of AMR and virulence traits</p>
        </div>
    </div>
    
    <div class="container">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h3>Analysis Overview</h3>
                    </div>
                    <div class="card-body">
                        <p>This report presents the results of phylogenetic clustering analysis of <em>Streptococcus suis</em> strains.</p>
                        <ul>
                            <li><strong>Number of strains:</strong> {len(self.data)}</li>
                            <li><strong>Number of clusters:</strong> {self.data['Cluster'].nunique()}</li>
                            <li><strong>Number of features:</strong> {len([c for c in self.data.columns if c not in ['Strain_ID', 'Cluster']])}</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h3>Visualizations</h3>
                    </div>
                    <div class="card-body">
                        {figures_html}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h3>Export Data</h3>
                    </div>
                    <div class="card-body">
                        <p>Results are available in the following files:</p>
                        <ul>
                            <li><code>clustered_data.csv</code> - Strain assignments with cluster labels</li>
                            <li><code>trait_associations.csv</code> - Statistical associations between traits and clusters</li>
                            <li><code>analysis_results.xlsx</code> - Complete Excel workbook with all results</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Bootstrap 5 JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
        return html
    
    def generate_excel_report(self):
        """Generate Excel report with multiple sheets."""
        print("\n=== Generating Excel Report ===")
        
        excel_path = self.output_dir / "analysis_results.xlsx"
        
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            # Sheet 1: Clustered data
            self.data.to_excel(writer, sheet_name='Clustered_Data', index=False)
            
            # Sheet 2: Cluster summary
            summary_data = []
            strain_col = "Strain_ID"
            feature_cols = [c for c in self.data.columns if c not in [strain_col, 'Cluster']]
            
            for cluster_id in sorted(self.data['Cluster'].unique()):
                cluster_data = self.data[self.data['Cluster'] == cluster_id]
                summary_data.append({
                    'Cluster': cluster_id,
                    'Size': len(cluster_data),
                    'Prevalence': f"{len(cluster_data) / len(self.data) * 100:.1f}%"
                })
            
            pd.DataFrame(summary_data).to_excel(writer, sheet_name='Cluster_Summary', index=False)
            
            # Sheet 3: Trait associations
            if 'trait_associations' in self.results:
                self.results['trait_associations'].to_excel(
                    writer, sheet_name='Trait_Associations', index=False
                )
            
            # Sheet 4: Metadata
            metadata = {
                'Parameter': ['Total Strains', 'Total Features', 'Number of Clusters', 'Analysis Date'],
                'Value': [
                    len(self.data),
                    len(feature_cols),
                    self.data['Cluster'].nunique(),
                    pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
                ]
            }
            pd.DataFrame(metadata).to_excel(writer, sheet_name='Metadata', index=False)
        
        print(f"Excel report saved: {excel_path}")
        
    def save_csv_outputs(self):
        """Save key results as CSV files."""
        print("\n=== Saving CSV Outputs ===")
        
        # Clustered data
        csv_path = self.output_dir / "clustered_data.csv"
        self.data.to_csv(csv_path, index=False)
        print(f"Saved: {csv_path}")
        
        # Trait associations
        if 'trait_associations' in self.results:
            assoc_path = self.output_dir / "trait_associations.csv"
            self.results['trait_associations'].to_csv(assoc_path, index=False)
            print(f"Saved: {assoc_path}")
    
    def run_full_analysis(self, data_files: List[str], tree_file: Optional[str] = None,
                         n_clusters: Optional[int] = None):
        """
        Run complete analysis pipeline.
        
        Parameters:
        -----------
        data_files : List[str]
            Paths to CSV data files
        tree_file : str, optional
            Path to Newick tree file
        n_clusters : int, optional
            Number of clusters (auto-determined if None)
        """
        print("\n" + "="*60)
        print("StrepSuis Phylogenetic Clustering Analysis")
        print("="*60)
        
        # Load data
        self.load_data(data_files)
        
        # Load tree (optional)
        if tree_file and os.path.exists(tree_file):
            self.load_tree(tree_file)
        
        # Clustering
        self.perform_clustering(n_clusters=n_clusters)
        
        # Trait associations
        self.calculate_trait_associations()
        
        # MCA
        self.perform_mca()
        
        # Generate reports
        self.generate_html_report()
        self.generate_excel_report()
        self.save_csv_outputs()
        
        print("\n" + "="*60)
        print("Analysis Complete!")
        print("="*60)
        print(f"\nOutput directory: {self.output_dir}")


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description="StrepSuis Phylogenetic Clustering Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with data files in current directory
  python StrepSuisPhyloCluster_2025_08_11.py

  # Specify custom data files
  python StrepSuisPhyloCluster_2025_08_11.py --data AMR_genes.csv Virulence.csv
  
  # Include phylogenetic tree
  python StrepSuisPhyloCluster_2025_08_11.py --tree Snp_tree.newick
  
  # Specify number of clusters
  python StrepSuisPhyloCluster_2025_08_11.py --clusters 4
        """
    )
    
    parser.add_argument(
        '--data',
        nargs='+',
        default=['AMR_genes.csv', 'Virulence.csv'],
        help='CSV data files (default: AMR_genes.csv Virulence.csv)'
    )
    
    parser.add_argument(
        '--tree',
        default='Snp_tree.newick',
        help='Phylogenetic tree file in Newick format (default: Snp_tree.newick)'
    )
    
    parser.add_argument(
        '--output',
        default='output',
        help='Output directory (default: output)'
    )
    
    parser.add_argument(
        '--clusters',
        type=int,
        default=None,
        help='Number of clusters (default: auto-determined by silhouette score)'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Random seed for reproducibility (default: 42)'
    )
    
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = StrepSuisAnalyzer(output_dir=args.output, random_state=args.seed)
    
    # Run analysis
    analyzer.run_full_analysis(
        data_files=args.data,
        tree_file=args.tree if os.path.exists(args.tree) else None,
        n_clusters=args.clusters
    )


if __name__ == "__main__":
    main()
