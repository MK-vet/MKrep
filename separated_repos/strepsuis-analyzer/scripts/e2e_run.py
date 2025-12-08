"""
Comprehensive End-to-End Analysis Runner for strepsuis-analyzer.

This script demonstrates the full capabilities of the strepsuis-analyzer
application by performing a complete analysis workflow on both example
and synthetic datasets using the public API.
"""

import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import warnings

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from strepsuis_analyzer import (
    DataValidator,
    StatisticalAnalyzer,
    PhylogeneticAnalyzer,
    Visualizer,
    ReportGenerator,
)
from strepsuis_analyzer.etl_operations import ETLOperations


class E2EAnalysisRunner:
    """End-to-end analysis runner for comprehensive testing."""
    
    def __init__(
        self,
        dataset_type: str = "both",
        results_dir: Path = None,
        fail_on_missing: bool = True,
        random_state: int = 42,
    ):
        """
        Initialize the E2E runner.
        
        Args:
            dataset_type: Which datasets to analyze ('example', 'synthetic', 'both')
            results_dir: Base directory for results
            fail_on_missing: Whether to fail if example data is missing
            random_state: Random seed for reproducibility
        """
        self.dataset_type = dataset_type
        self.fail_on_missing = fail_on_missing
        self.random_state = random_state
        
        # Setup paths
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / "data"
        
        # Create timestamped results directory
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        if results_dir is None:
            self.results_dir = self.base_dir / "results" / f"strepsuis-analyzer-{timestamp}"
        else:
            self.results_dir = Path(results_dir) / f"strepsuis-analyzer-{timestamp}"
        
        # Initialize components
        self.validator = DataValidator()
        self.stats_analyzer = StatisticalAnalyzer(random_state=random_state)
        self.phylo_analyzer = PhylogeneticAnalyzer()
        self.visualizer = Visualizer()
        self.etl_ops = ETLOperations()
        
        # Tracking
        self.datasets_analyzed = []
        self.outputs_generated = []
        self.errors = []
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup comprehensive logging."""
        log_dir = self.results_dir / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / "run.log"
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("="*80)
        self.logger.info("Starting E2E Analysis Run")
        self.logger.info(f"Results directory: {self.results_dir}")
        self.logger.info(f"Dataset type: {self.dataset_type}")
        self.logger.info(f"Random state: {self.random_state}")
        self.logger.info("="*80)
    
    def load_dataset(self, dataset_name: str) -> Dict[str, pd.DataFrame]:
        """Load a complete dataset (example or synthetic)."""
        self.logger.info(f"Loading {dataset_name} dataset...")
        
        if dataset_name == "example":
            data_path = self.data_dir
        else:
            data_path = self.data_dir / "synthetic"
        
        data = {}
        
        # Load CSV files
        csv_files = {
            "amr_genes": "AMR_genes.csv",
            "mic": "MIC.csv",
            "virulence": "Virulence.csv",
            "mlst": "MLST.csv",
            "serotype": "Serotype.csv",
        }
        
        for key, filename in csv_files.items():
            filepath = data_path / filename
            if not filepath.exists():
                msg = f"Missing file: {filepath}"
                if self.fail_on_missing and dataset_name == "example":
                    self.logger.error(msg)
                    raise FileNotFoundError(msg)
                else:
                    self.logger.warning(msg)
                    continue
            
            df = pd.read_csv(filepath)
            data[key] = df
            self.logger.info(f"  Loaded {filename}: {df.shape}")
        
        # Load tree file
        tree_file = data_path / "Snp_tree.newick"
        if tree_file.exists():
            with open(tree_file, 'r') as f:
                data["tree_newick"] = f.read().strip()
            self.logger.info(f"  Loaded Snp_tree.newick")
        elif self.fail_on_missing and dataset_name == "example":
            raise FileNotFoundError(f"Missing file: {tree_file}")
        
        self.datasets_analyzed.append(dataset_name)
        return data
    
    def run_validation(self, data: Dict, output_dir: Path):
        """Run comprehensive validation on datasets."""
        self.logger.info("Running data validation...")
        
        val_dir = output_dir / "validation"
        val_dir.mkdir(parents=True, exist_ok=True)
        
        results = []
        
        # Validate each dataset
        for key, df in data.items():
            if key == "tree_newick":
                continue
            
            is_valid, errors, warnings = self.validator.validate_dataframe(
                df, name=key, min_rows=1
            )
            
            results.append({
                "dataset": key,
                "shape": f"{df.shape[0]}x{df.shape[1]}",
                "valid": is_valid,
                "errors": "; ".join(errors) if errors else "None",
                "warnings": "; ".join(warnings) if warnings else "None",
            })
        
        # Validate binary matrices
        for key in ["amr_genes", "virulence"]:
            if key in data:
                df_binary = data[key].iloc[:, 1:]  # Skip Strain column
                is_binary, errors, warnings = self.validator.validate_binary_matrix(
                    df_binary, name=key
                )
                if not is_binary:
                    results.append({
                        "dataset": f"{key}_binary_check",
                        "shape": "",
                        "valid": is_binary,
                        "errors": "; ".join(errors),
                        "warnings": "; ".join(warnings) if warnings else "None",
                    })
        
        # Validate tree
        if "tree_newick" in data:
            tree_loaded = self.phylo_analyzer.load_tree_from_newick(data["tree_newick"])
            results.append({
                "dataset": "phylogenetic_tree",
                "shape": f"{len(self.phylo_analyzer.get_leaf_names())} taxa",
                "valid": tree_loaded,
                "errors": "Failed to parse" if not tree_loaded else "None",
                "warnings": "None",
            })
        
        # Save validation report
        val_df = pd.DataFrame(results)
        val_file = val_dir / "validation_report.csv"
        val_df.to_csv(val_file, index=False)
        self.outputs_generated.append(str(val_file))
        self.logger.info(f"  Saved validation report: {val_file}")
        
        # Summary log
        summary_file = val_dir / "summary.log"
        with open(summary_file, 'w') as f:
            f.write("Validation Summary\n")
            f.write("="*50 + "\n")
            for r in results:
                f.write(f"\n{r['dataset']}: {'VALID' if r['valid'] else 'INVALID'}\n")
                if r['errors'] != "None":
                    f.write(f"  Errors: {r['errors']}\n")
        self.outputs_generated.append(str(summary_file))
    
    def run_statistical_analysis(self, data: Dict, output_dir: Path):
        """Run comprehensive statistical analyses."""
        self.logger.info("Running statistical analysis...")
        
        stats_dir = output_dir / "stats"
        stats_dir.mkdir(parents=True, exist_ok=True)
        
        # Use MIC data for numerical analysis
        if "mic" not in data:
            self.logger.warning("MIC data not available, skipping statistical tests")
            return
        
        mic_df = data["mic"].set_index("Strain")
        
        # 1. Correlation analysis
        self.logger.info("  Computing correlations...")
        corr_results = []
        
        # Pearson correlation matrix
        corr_matrix = mic_df.corr(method='pearson')
        corr_file = stats_dir / "correlation_matrix.csv"
        corr_matrix.to_csv(corr_file)
        self.outputs_generated.append(str(corr_file))
        
        # Correlation heatmap
        fig, ax = plt.subplots(figsize=(12, 10))
        import seaborn as sns
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, ax=ax, square=True)
        ax.set_title('Pearson Correlation Matrix - MIC Data', fontsize=14, fontweight='bold')
        plt.tight_layout()
        heatmap_file = stats_dir / "correlation_heatmap.png"
        fig.savefig(heatmap_file, dpi=150)
        plt.close(fig)
        self.outputs_generated.append(str(heatmap_file))
        
        # Pairwise correlations with p-values
        cols = mic_df.columns.tolist()
        for i in range(len(cols)):
            for j in range(i+1, len(cols)):
                for method in ['pearson', 'spearman', 'kendall']:
                    corr, pval = self.stats_analyzer.compute_correlation(
                        mic_df[cols[i]], mic_df[cols[j]], method=method
                    )
                    corr_results.append({
                        'var1': cols[i],
                        'var2': cols[j],
                        'method': method,
                        'correlation': corr,
                        'p_value': pval
                    })
        
        corr_df = pd.DataFrame(corr_results)
        corr_pval_file = stats_dir / "correlations_with_pvalues.csv"
        corr_df.to_csv(corr_pval_file, index=False)
        self.outputs_generated.append(str(corr_pval_file))
        
        # 2. Normality tests
        self.logger.info("  Running normality tests...")
        normality_results = []
        
        for col in mic_df.columns:
            data_clean = mic_df[col].dropna()
            if len(data_clean) >= 3:
                stat, pval, is_normal = self.stats_analyzer.test_normality(data_clean)
                normality_results.append({
                    'variable': col,
                    'test': 'Shapiro-Wilk',
                    'statistic': stat,
                    'p_value': pval,
                    'normal': is_normal
                })
        
        norm_df = pd.DataFrame(normality_results)
        norm_file = stats_dir / "normality_results.csv"
        norm_df.to_csv(norm_file, index=False)
        self.outputs_generated.append(str(norm_file))
        
        # Q-Q plots for first few variables
        n_plots = min(4, len(mic_df.columns))
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()
        
        for idx, col in enumerate(mic_df.columns[:n_plots]):
            data_clean = mic_df[col].dropna()
            from scipy import stats as sp_stats
            sp_stats.probplot(data_clean, dist="norm", plot=axes[idx])
            axes[idx].set_title(f'Q-Q Plot: {col}')
        
        plt.tight_layout()
        qq_file = stats_dir / "qq_plots.png"
        fig.savefig(qq_file, dpi=150)
        plt.close(fig)
        self.outputs_generated.append(str(qq_file))
        
        # 3. Hypothesis tests (if we have grouping variable)
        if "mlst" in data:
            self.logger.info("  Running hypothesis tests...")
            hyp_results = []
            
            # Merge MIC with MLST
            mlst_df = data["mlst"]
            merged = mic_df.reset_index().merge(mlst_df, on='Strain')
            
            # Get top 2 STs for comparison
            top_sts = merged['ST'].value_counts().head(2).index.tolist()
            
            if len(top_sts) >= 2:
                group1 = merged[merged['ST'] == top_sts[0]]
                group2 = merged[merged['ST'] == top_sts[1]]
                
                for col in mic_df.columns:
                    g1_data = group1[col].dropna()
                    g2_data = group2[col].dropna()
                    
                    if len(g1_data) >= 3 and len(g2_data) >= 3:
                        # T-test
                        t_stat, t_pval = self.stats_analyzer.perform_ttest(g1_data, g2_data)
                        hyp_results.append({
                            'variable': col,
                            'group1': top_sts[0],
                            'group2': top_sts[1],
                            'test': 't-test',
                            'statistic': t_stat,
                            'p_value': t_pval
                        })
                        
                        # Mann-Whitney U
                        u_stat, u_pval = self.stats_analyzer.perform_mann_whitney(g1_data, g2_data)
                        hyp_results.append({
                            'variable': col,
                            'group1': top_sts[0],
                            'group2': top_sts[1],
                            'test': 'Mann-Whitney U',
                            'statistic': u_stat,
                            'p_value': u_pval
                        })
                
                hyp_df = pd.DataFrame(hyp_results)
                hyp_file = stats_dir / "hypothesis_tests.csv"
                hyp_df.to_csv(hyp_file, index=False)
                self.outputs_generated.append(str(hyp_file))
        
        # 4. Multiple testing correction
        if len(corr_df) > 0:
            self.logger.info("  Applying multiple testing corrections...")
            pvals = corr_df[corr_df['method'] == 'pearson']['p_value'].values
            
            # Apply multiple testing corrections
            _, bonf_corrected = self.stats_analyzer.apply_multiple_testing_correction(
                pvals, method='bonferroni'
            )
            _, fdr_corrected = self.stats_analyzer.apply_multiple_testing_correction(
                pvals, method='fdr_bh'
            )
            
            corr_subset = corr_df[corr_df['method'] == 'pearson'].copy()
            corr_subset['p_bonferroni'] = bonf_corrected
            corr_subset['p_fdr'] = fdr_corrected
            
            corrected_file = stats_dir / "corrected_pvalues.csv"
            corr_subset.to_csv(corrected_file, index=False)
            self.outputs_generated.append(str(corrected_file))
        
        # 5. Simple meta-analysis simulation
        self.logger.info("  Running meta-analysis example...")
        # Create synthetic effect sizes for demonstration
        effect_sizes = np.random.normal(0.5, 0.2, 5)
        variances = np.random.uniform(0.01, 0.1, 5)
        
        try:
            fixed_effect, fixed_var, fixed_se = self.stats_analyzer.meta_analysis_fixed_effects(
                effect_sizes, variances
            )
            random_effect, random_var, random_se, tau2 = self.stats_analyzer.meta_analysis_random_effects(
                effect_sizes, variances
            )
            q_stat, q_pval = self.stats_analyzer.cochrans_q_test(effect_sizes, variances)
            
            # Compute confidence intervals
            z_crit = 1.96  # 95% CI
            fixed_ci = (fixed_effect - z_crit * fixed_se, fixed_effect + z_crit * fixed_se)
            random_ci = (random_effect - z_crit * random_se, random_effect + z_crit * random_se)
            
            meta_results = pd.DataFrame([{
                'model': 'Fixed Effects',
                'pooled_effect': fixed_effect,
                'ci_lower': fixed_ci[0],
                'ci_upper': fixed_ci[1],
                'cochran_q': q_stat,
                'cochran_q_pval': q_pval
            }, {
                'model': 'Random Effects',
                'pooled_effect': random_effect,
                'ci_lower': random_ci[0],
                'ci_upper': random_ci[1],
                'cochran_q': q_stat,
                'cochran_q_pval': q_pval
            }])
            
            meta_file = stats_dir / "meta_analysis_results.csv"
            meta_results.to_csv(meta_file, index=False)
            self.outputs_generated.append(str(meta_file))
        except Exception as e:
            self.logger.warning(f"  Meta-analysis failed: {e}")
    
    def run_visualizations(self, data: Dict, output_dir: Path):
        """Create comprehensive visualizations."""
        self.logger.info("Running visualizations...")
        
        viz_dir = output_dir / "visualizations"
        viz_dir.mkdir(parents=True, exist_ok=True)
        
        if "mic" in data:
            mic_df = data["mic"].set_index("Strain")
            
            # Histogram
            fig = self.visualizer.create_histogram(
                mic_df.iloc[:, 0],
                title=f"Distribution of {mic_df.columns[0]}",
                xlabel="MIC Value",
                color='steelblue'
            )
            hist_file = viz_dir / "histogram_example.png"
            fig.savefig(hist_file, dpi=150)
            plt.close(fig)
            self.outputs_generated.append(str(hist_file))
            
            # Scatter plot
            if len(mic_df.columns) >= 2:
                fig = self.visualizer.create_scatter_plot(
                    mic_df.iloc[:, 0],
                    mic_df.iloc[:, 1],
                    title=f"{mic_df.columns[0]} vs {mic_df.columns[1]}",
                    xlabel=mic_df.columns[0],
                    ylabel=mic_df.columns[1],
                    show_regression=True
                )
                scatter_file = viz_dir / "scatter_plot_example.png"
                fig.savefig(scatter_file, dpi=150)
                plt.close(fig)
                self.outputs_generated.append(str(scatter_file))
            
            # Box plot
            data_dict = {col: mic_df[col].dropna() for col in mic_df.columns[:5]}
            fig = self.visualizer.create_box_plot(
                data_dict,
                title="MIC Distribution (Top 5 Antibiotics)"
            )
            box_file = viz_dir / "boxplot_example.png"
            fig.savefig(box_file, dpi=150)
            plt.close(fig)
            self.outputs_generated.append(str(box_file))
            
            # Violin plot
            data_dict = {col: mic_df[col].dropna() for col in mic_df.columns[:5]}
            fig = self.visualizer.create_violin_plot(
                data_dict,
                title="MIC Violin Plot"
            )
            violin_file = viz_dir / "violin_plot_example.png"
            fig.savefig(violin_file, dpi=150)
            plt.close(fig)
            self.outputs_generated.append(str(violin_file))
        
        self.logger.info(f"  Generated {4} visualization plots")
    
    def run_clustering(self, data: Dict, output_dir: Path):
        """Run clustering analyses."""
        self.logger.info("Running clustering analysis...")
        
        cluster_dir = output_dir / "clustering"
        cluster_dir.mkdir(parents=True, exist_ok=True)
        
        if "mic" in data:
            mic_df = data["mic"].set_index("Strain")
            X = mic_df.values
            
            # K-Means with elbow plot
            from sklearn.cluster import KMeans
            inertias = []
            K_range = range(2, min(11, len(mic_df)))
            
            for k in K_range:
                kmeans = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
                kmeans.fit(X)
                inertias.append(kmeans.inertia_)
            
            # Elbow plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(list(K_range), inertias, 'bo-')
            ax.set_xlabel('Number of Clusters (k)', fontsize=12)
            ax.set_ylabel('Inertia', fontsize=12)
            ax.set_title('K-Means Elbow Plot', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            elbow_file = cluster_dir / "kmeans_elbow_plot.png"
            fig.savefig(elbow_file, dpi=150)
            plt.close(fig)
            self.outputs_generated.append(str(elbow_file))
            
            # Final K-Means clustering
            kmeans = KMeans(n_clusters=3, random_state=self.random_state, n_init=10)
            labels = kmeans.fit_predict(X)
            
            labels_df = pd.DataFrame({
                'Strain': mic_df.index,
                'Cluster': labels
            })
            kmeans_file = cluster_dir / "kmeans_labels.csv"
            labels_df.to_csv(kmeans_file, index=False)
            self.outputs_generated.append(str(kmeans_file))
        
        # K-Modes for binary data
        if "amr_genes" in data:
            from kmodes.kmodes import KModes
            amr_df = data["amr_genes"].set_index("Strain")
            X_binary = amr_df.values
            
            try:
                kmodes = KModes(n_clusters=3, init='Huang', random_state=self.random_state)
                labels_binary = kmodes.fit_predict(X_binary)
                
                labels_df = pd.DataFrame({
                    'Strain': amr_df.index,
                    'Cluster': labels_binary
                })
                kmodes_file = cluster_dir / "kmodes_labels.csv"
                labels_df.to_csv(kmodes_file, index=False)
                self.outputs_generated.append(str(kmodes_file))
            except Exception as e:
                self.logger.warning(f"  K-Modes clustering failed: {e}")
        
        # Hierarchical clustering
        if "mic" in data:
            from scipy.cluster.hierarchy import dendrogram, linkage
            
            linkage_matrix = linkage(X, method='ward')
            
            fig, ax = plt.subplots(figsize=(12, 8))
            # Use fewer labels for dendrogram readability
            n_labels = min(20, len(mic_df))
            if n_labels < len(mic_df):
                dendrogram(linkage_matrix, ax=ax, no_labels=True)
            else:
                dendrogram(linkage_matrix, ax=ax, labels=mic_df.index.tolist())
            ax.set_title('Hierarchical Clustering Dendrogram', fontsize=14, fontweight='bold')
            ax.set_xlabel('Sample Index', fontsize=12)
            ax.set_ylabel('Distance', fontsize=12)
            if n_labels == len(mic_df):
                plt.xticks(rotation=90)
            plt.tight_layout()
            dend_file = cluster_dir / "hierarchical_dendrogram.png"
            fig.savefig(dend_file, dpi=150)
            plt.close(fig)
            self.outputs_generated.append(str(dend_file))
            
            # Get cluster labels
            from scipy.cluster.hierarchy import fcluster
            hier_labels = fcluster(linkage_matrix, t=3, criterion='maxclust')
            
            labels_df = pd.DataFrame({
                'Strain': mic_df.index,
                'Cluster': hier_labels
            })
            hier_file = cluster_dir / "hierarchical_labels.csv"
            labels_df.to_csv(hier_file, index=False)
            self.outputs_generated.append(str(hier_file))
        
        # DBSCAN
        if "mic" in data:
            from sklearn.cluster import DBSCAN
            from sklearn.preprocessing import StandardScaler
            
            X_scaled = StandardScaler().fit_transform(X)
            dbscan = DBSCAN(eps=0.5, min_samples=3)
            dbscan_labels = dbscan.fit_predict(X_scaled)
            
            labels_df = pd.DataFrame({
                'Strain': mic_df.index,
                'Cluster': dbscan_labels
            })
            dbscan_file = cluster_dir / "dbscan_labels.csv"
            labels_df.to_csv(dbscan_file, index=False)
            self.outputs_generated.append(str(dbscan_file))
        
        self.logger.info(f"  Completed clustering analyses")
    
    def run_phylogenetic_analysis(self, data: Dict, output_dir: Path):
        """Run phylogenetic analyses."""
        self.logger.info("Running phylogenetic analysis...")
        
        phylo_dir = output_dir / "phylogenetics"
        phylo_dir.mkdir(parents=True, exist_ok=True)
        
        if "tree_newick" not in data:
            self.logger.warning("No phylogenetic tree available")
            return
        
        tree_str = data["tree_newick"]
        
        # Load tree
        tree_loaded = self.phylo_analyzer.load_tree_from_newick(tree_str)
        if not tree_loaded:
            self.logger.warning("Failed to load phylogenetic tree")
            return
        
        # Tree visualization
        try:
            from Bio import Phylo
            from io import StringIO
            
            tree_io = StringIO(tree_str)
            tree = Phylo.read(tree_io, "newick")
            
            fig, ax = plt.subplots(figsize=(14, 10))
            Phylo.draw(tree, axes=ax, do_show=False)
            ax.set_title('Phylogenetic Tree', fontsize=14, fontweight='bold')
            plt.tight_layout()
            tree_file = phylo_dir / "tree_plot.png"
            fig.savefig(tree_file, dpi=150, bbox_inches='tight')
            plt.close(fig)
            self.outputs_generated.append(str(tree_file))
        except Exception as e:
            self.logger.warning(f"Tree visualization failed: {e}")
        
        # Robinson-Foulds distance (compare tree to itself as demo)
        try:
            rf_dist = self.phylo_analyzer.compute_robinson_foulds_distance(
                tree_str, tree_str, normalize=False
            )
            
            rf_df = pd.DataFrame([{
                'tree1': 'self',
                'tree2': 'self',
                'rf_distance': rf_dist,
                'normalized': False
            }])
            rf_file = phylo_dir / "rf_distances.csv"
            rf_df.to_csv(rf_file, index=False)
            self.outputs_generated.append(str(rf_file))
        except Exception as e:
            self.logger.warning(f"Robinson-Foulds distance failed: {e}")
        
        # Faith's PD
        try:
            taxa_subset = self.phylo_analyzer.get_leaf_names()[:10]  # First 10 taxa
            pd_value = self.phylo_analyzer.compute_faith_pd(tree_str, taxa_subset)
            
            pd_df = pd.DataFrame([{
                'taxa_count': len(taxa_subset),
                'faiths_pd': pd_value
            }])
            pd_file = phylo_dir / "phylo_diversity.csv"
            pd_df.to_csv(pd_file, index=False)
            self.outputs_generated.append(str(pd_file))
        except Exception as e:
            self.logger.warning(f"Faith's PD calculation failed: {e}")
        
        # Cophenetic correlation
        try:
            # Compute pairwise distances for cophenetic correlation
            tree_distances = self.phylo_analyzer.compute_pairwise_distances(tree_str)
            if tree_distances is not None:
                # Create a simple distance matrix for comparison
                coph_corr = self.phylo_analyzer.compute_cophenetic_correlation(
                    tree_str, tree_distances
                )
                
                coph_df = pd.DataFrame([{
                    'cophenetic_correlation': coph_corr
                }])
                coph_file = phylo_dir / "cophenetic_correlation.csv"
                coph_df.to_csv(coph_file, index=False)
                self.outputs_generated.append(str(coph_file))
        except Exception as e:
            self.logger.warning(f"Cophenetic correlation failed: {e}")
        
        self.logger.info(f"  Completed phylogenetic analyses")
    
    def run_etl_operations(self, data: Dict, output_dir: Path):
        """Run ETL operations."""
        self.logger.info("Running ETL operations...")
        
        etl_dir = output_dir / "etl"
        etl_dir.mkdir(parents=True, exist_ok=True)
        
        if "mic" in data and "mlst" in data:
            # Merge datasets
            mic_df = data["mic"]
            mlst_df = data["mlst"]
            
            merged = mic_df.merge(mlst_df, on='Strain')
            
            # Pivot table
            pivot = self.etl_ops.pivot_table(
                merged,
                index='ST',
                columns=None,
                values=mic_df.columns[1],
                aggfunc='mean'
            )
            
            # Aggregation
            agg_dict = {mic_df.columns[1]: ['mean', 'std', 'min', 'max']}
            if len(mic_df.columns) > 2:
                agg_dict[mic_df.columns[2]] = ['mean', 'std']
            
            aggregated = self.etl_ops.aggregate_data(
                merged,
                group_by='ST',
                agg_dict=agg_dict
            )
            agg_file = etl_dir / "aggregated_by_st.csv"
            aggregated.to_csv(agg_file, index=False)
            self.outputs_generated.append(str(agg_file))
            
            # Normalization
            all_cols = mic_df.set_index('Strain').columns.tolist()
            normalized = self.etl_ops.normalize_columns(
                mic_df.set_index('Strain'),
                columns=all_cols,
                method='zscore'
            )
            norm_file = etl_dir / "normalized_zscore.csv"
            normalized.to_csv(norm_file)
            self.outputs_generated.append(str(norm_file))
            
            # Min-Max normalization
            minmax = self.etl_ops.normalize_columns(
                mic_df.set_index('Strain'),
                columns=all_cols,
                method='minmax'
            )
            minmax_file = etl_dir / "normalized_minmax.csv"
            minmax.to_csv(minmax_file)
            self.outputs_generated.append(str(minmax_file))
            
            # Save transformed data
            transform_file = etl_dir / "transformed_data.csv"
            merged.to_csv(transform_file, index=False)
            self.outputs_generated.append(str(transform_file))
        
        self.logger.info(f"  Completed ETL operations")
    
    def generate_reports(self, data: Dict, output_dir: Path, dataset_name: str):
        """Generate comprehensive reports."""
        self.logger.info("Generating reports...")
        
        report_dir = output_dir / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        # Create report
        report = ReportGenerator()
        report.metadata["dataset"] = dataset_name
        report.metadata["analysis_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add dataset summaries
        for key, df in data.items():
            if key == "tree_newick":
                continue
            report.add_dataframe(
                f"{key}_summary",
                df.describe() if df.select_dtypes(include=[np.number]).shape[1] > 0 else df.head(),
                f"Summary of {key} dataset"
            )
        
        # Add statistics
        if "mic" in data:
            mic_df = data["mic"].set_index("Strain")
            stats_dict = {
                'n_strains': len(mic_df),
                'n_antibiotics': len(mic_df.columns),
                'mean_mic': float(mic_df.mean().mean()),
                'std_mic': float(mic_df.std().mean()),
            }
            report.add_statistics("overall_stats", stats_dict, "Overall dataset statistics")
        
        # Export Excel
        excel_file = report_dir / "final_report.xlsx"
        report.export_to_excel(str(excel_file))
        self.outputs_generated.append(str(excel_file))
        
        # Export HTML
        html_file = report_dir / "final_report.html"
        report.export_to_html(str(html_file))
        self.outputs_generated.append(str(html_file))
        
        self.logger.info(f"  Generated Excel and HTML reports")
    
    def run_analysis_for_dataset(self, dataset_name: str):
        """Run complete analysis for a single dataset."""
        self.logger.info(f"\n{'='*80}")
        self.logger.info(f"Analyzing {dataset_name.upper()} dataset")
        self.logger.info(f"{'='*80}\n")
        
        # Load data
        try:
            data = self.load_dataset(dataset_name)
        except FileNotFoundError as e:
            self.logger.error(f"Failed to load dataset: {e}")
            self.errors.append(str(e))
            return
        
        # Create output directory
        output_dir = self.results_dir / dataset_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Run all analyses
        try:
            self.run_validation(data, output_dir)
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            self.errors.append(f"Validation: {e}")
        
        try:
            self.run_statistical_analysis(data, output_dir)
        except Exception as e:
            self.logger.error(f"Statistical analysis failed: {e}")
            self.errors.append(f"Statistics: {e}")
        
        try:
            self.run_visualizations(data, output_dir)
        except Exception as e:
            self.logger.error(f"Visualizations failed: {e}")
            self.errors.append(f"Visualizations: {e}")
        
        try:
            self.run_clustering(data, output_dir)
        except Exception as e:
            self.logger.error(f"Clustering failed: {e}")
            self.errors.append(f"Clustering: {e}")
        
        try:
            self.run_phylogenetic_analysis(data, output_dir)
        except Exception as e:
            self.logger.error(f"Phylogenetic analysis failed: {e}")
            self.errors.append(f"Phylogenetics: {e}")
        
        try:
            self.run_etl_operations(data, output_dir)
        except Exception as e:
            self.logger.error(f"ETL operations failed: {e}")
            self.errors.append(f"ETL: {e}")
        
        try:
            self.generate_reports(data, output_dir, dataset_name)
        except Exception as e:
            self.logger.error(f"Report generation failed: {e}")
            self.errors.append(f"Reports: {e}")
    
    def run(self) -> int:
        """Execute the complete E2E analysis."""
        start_time = datetime.now()
        
        # Determine which datasets to analyze
        datasets_to_run = []
        if self.dataset_type in ["example", "both"]:
            datasets_to_run.append("example")
        if self.dataset_type in ["synthetic", "both"]:
            datasets_to_run.append("synthetic")
        
        # Run analyses
        for dataset_name in datasets_to_run:
            self.run_analysis_for_dataset(dataset_name)
        
        # Final summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        self.logger.info(f"\n{'='*80}")
        self.logger.info("ANALYSIS COMPLETE")
        self.logger.info(f"{'='*80}")
        self.logger.info(f"Duration: {duration:.2f} seconds")
        self.logger.info(f"Datasets analyzed: {', '.join(self.datasets_analyzed)}")
        self.logger.info(f"Total outputs generated: {len(self.outputs_generated)}")
        self.logger.info(f"Results directory: {self.results_dir}")
        
        if self.errors:
            self.logger.warning(f"\nErrors encountered: {len(self.errors)}")
            for err in self.errors:
                self.logger.warning(f"  - {err}")
        
        # Perform self-checks
        return self.perform_self_checks()
    
    def perform_self_checks(self) -> int:
        """
        Perform self-checks to ensure minimum outputs were generated.
        
        Returns:
            0 if all checks pass, 1 otherwise
        """
        self.logger.info(f"\n{'='*80}")
        self.logger.info("PERFORMING SELF-CHECKS")
        self.logger.info(f"{'='*80}")
        
        checks_passed = True
        
        # Check minimum outputs per category
        required_outputs = {
            'validation': 1,  # At least 1 validation report
            'stats': 2,  # At least 1 table + 1 figure
            'visualizations': 2,  # At least 2 visualizations
            'clustering': 1,  # At least 1 clustering output
            'phylogenetics': 1,  # At least 1 phylo metric
            'etl': 1,  # At least 1 ETL output
            'reports': 2,  # Excel + HTML
        }
        
        for dataset in self.datasets_analyzed:
            self.logger.info(f"\nChecking {dataset} dataset outputs...")
            
            for category, min_count in required_outputs.items():
                category_dir = self.results_dir / dataset / category
                
                if not category_dir.exists():
                    self.logger.error(f"  ✗ Missing directory: {category}")
                    checks_passed = False
                    continue
                
                output_files = list(category_dir.glob("*"))
                output_files = [f for f in output_files if f.is_file()]
                
                if len(output_files) < min_count:
                    self.logger.error(
                        f"  ✗ {category}: Expected >={min_count} outputs, found {len(output_files)}"
                    )
                    checks_passed = False
                else:
                    self.logger.info(
                        f"  ✓ {category}: {len(output_files)} outputs (>={min_count} required)"
                    )
        
        # Check that required subdirectories are not empty
        for dataset in self.datasets_analyzed:
            for category in required_outputs.keys():
                category_dir = self.results_dir / dataset / category
                if category_dir.exists():
                    if not list(category_dir.glob("*")):
                        self.logger.error(f"  ✗ Empty directory: {category_dir}")
                        checks_passed = False
        
        # Final verdict
        self.logger.info(f"\n{'='*80}")
        if checks_passed:
            self.logger.info("✓ ALL SELF-CHECKS PASSED")
            self.logger.info(f"{'='*80}\n")
            return 0
        else:
            self.logger.error("✗ SOME SELF-CHECKS FAILED")
            self.logger.error(f"{'='*80}\n")
            return 1


def main():
    """Main entry point for E2E runner."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Comprehensive E2E analysis runner for strepsuis-analyzer"
    )
    parser.add_argument(
        "--dataset",
        choices=["example", "synthetic", "both"],
        default="both",
        help="Which dataset(s) to analyze"
    )
    parser.add_argument(
        "--results-dir",
        type=str,
        default=None,
        help="Base directory for results (default: ./results/)"
    )
    parser.add_argument(
        "--fail-on-missing",
        action="store_true",
        default=True,
        help="Fail if example data is missing"
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random seed for reproducibility"
    )
    
    args = parser.parse_args()
    
    # Create and run analyzer
    runner = E2EAnalysisRunner(
        dataset_type=args.dataset,
        results_dir=Path(args.results_dir) if args.results_dir else None,
        fail_on_missing=args.fail_on_missing,
        random_state=args.random_state,
    )
    
    exit_code = runner.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
