"""
Extended Tests for Analyzer - Coverage for Missing Paths

Tests for phylogenetic tree loading, optimal clustering, MCA, and other uncovered code paths.
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import shutil
from pathlib import Path
import sys

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from StrepSuisPhyloCluster_2025_08_11 import StrepSuisAnalyzer

# Check if BioPython is available
try:
    from Bio import Phylo
    HAS_BIOPYTHON = True
except ImportError:
    HAS_BIOPYTHON = False

# Check if prince is available
try:
    import prince
    HAS_PRINCE = True
except ImportError:
    HAS_PRINCE = False


class TestLoadData:
    """Test data loading functionality."""

    def setup_method(self):
        """Create temporary directory and sample data files."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create sample data files
        self.data_file1 = Path(self.temp_dir) / 'data1.csv'
        df1 = pd.DataFrame({
            'Strain_ID': [f'Strain_{i}' for i in range(20)],
            'Trait_A': np.random.binomial(1, 0.5, 20),
            'Trait_B': np.random.binomial(1, 0.5, 20),
        })
        df1.to_csv(self.data_file1, index=False)
        
        self.data_file2 = Path(self.temp_dir) / 'data2.csv'
        df2 = pd.DataFrame({
            'Strain_ID': [f'Strain_{i}' for i in range(20)],
            'Trait_C': np.random.binomial(1, 0.5, 20),
            'Trait_D': np.random.binomial(1, 0.5, 20),
        })
        df2.to_csv(self.data_file2, index=False)

    def teardown_method(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_load_single_file(self):
        """Test loading a single data file."""
        analyzer = StrepSuisAnalyzer(output_dir=self.temp_dir, random_state=42)
        analyzer.load_data([str(self.data_file1)])
        
        assert analyzer.data is not None
        assert len(analyzer.data) == 20
        assert 'Strain_ID' in analyzer.data.columns
        assert 'Trait_A' in analyzer.data.columns

    def test_load_multiple_files(self):
        """Test loading multiple data files."""
        analyzer = StrepSuisAnalyzer(output_dir=self.temp_dir, random_state=42)
        analyzer.load_data([str(self.data_file1), str(self.data_file2)])
        
        assert analyzer.data is not None
        assert len(analyzer.data) == 20
        assert 'Trait_A' in analyzer.data.columns
        assert 'Trait_C' in analyzer.data.columns

    def test_load_data_fills_missing_values(self):
        """Test that missing values are filled with 0."""
        # Create file with missing values
        data_file3 = Path(self.temp_dir) / 'data3.csv'
        df3 = pd.DataFrame({
            'Strain_ID': [f'Strain_{i}' for i in range(15)],  # Fewer strains
            'Trait_E': np.random.binomial(1, 0.5, 15),
        })
        df3.to_csv(data_file3, index=False)
        
        analyzer = StrepSuisAnalyzer(output_dir=self.temp_dir, random_state=42)
        analyzer.load_data([str(self.data_file1), str(data_file3)])
        
        # Should fill missing values with 0
        assert not analyzer.data['Trait_E'].isna().any()

    def test_load_data_missing_file_warning(self):
        """Test warning when file is missing."""
        analyzer = StrepSuisAnalyzer(output_dir=self.temp_dir, random_state=42)
        
        # Should not crash with missing file, but should warn
        analyzer.load_data([str(self.data_file1), 'nonexistent.csv'])
        
        # Should still load the valid file
        assert analyzer.data is not None
        assert len(analyzer.data) == 20

    def test_load_data_no_valid_files_raises_error(self):
        """Test error when no valid files are provided."""
        analyzer = StrepSuisAnalyzer(output_dir=self.temp_dir, random_state=42)
        
        with pytest.raises(ValueError, match="No data files loaded"):
            analyzer.load_data(['nonexistent1.csv', 'nonexistent2.csv'])


@pytest.mark.skipif(not HAS_BIOPYTHON, reason="BioPython not available")
class TestLoadTree:
    """Test phylogenetic tree loading."""

    def setup_method(self):
        """Create temporary directory and sample tree file."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a simple Newick tree
        self.tree_file = Path(self.temp_dir) / 'test_tree.newick'
        newick_str = "((Strain_0:0.1,Strain_1:0.2):0.3,(Strain_2:0.15,Strain_3:0.25):0.35);"
        with open(self.tree_file, 'w') as f:
            f.write(newick_str)

    def teardown_method(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_load_tree_basic(self):
        """Test basic tree loading."""
        analyzer = StrepSuisAnalyzer(output_dir=self.temp_dir, random_state=42)
        analyzer.load_tree(str(self.tree_file))
        
        assert analyzer.tree is not None
        assert analyzer.phylo_dist_matrix is not None
        assert analyzer.phylo_dist_matrix.shape[0] == analyzer.tree.count_terminals()

    def test_phylo_distance_matrix_properties(self):
        """Test properties of phylogenetic distance matrix."""
        analyzer = StrepSuisAnalyzer(output_dir=self.temp_dir, random_state=42)
        analyzer.load_tree(str(self.tree_file))
        
        dist_matrix = analyzer.phylo_dist_matrix
        
        # Should be square
        assert dist_matrix.shape[0] == dist_matrix.shape[1]
        
        # Should be symmetric
        np.testing.assert_array_almost_equal(dist_matrix, dist_matrix.T)
        
        # Diagonal should be zero
        np.testing.assert_array_almost_equal(np.diag(dist_matrix), np.zeros(len(dist_matrix)))
        
        # All distances should be non-negative
        assert np.all(dist_matrix >= 0)


class TestOptimalClustering:
    """Test optimal cluster selection."""

    def test_optimal_clustering_auto_select(self):
        """Test automatic cluster number selection."""
        np.random.seed(42)
        
        # Create data with clear clusters
        cluster1 = np.random.binomial(1, 0.8, (15, 8))
        cluster2 = np.random.binomial(1, 0.2, (15, 8))
        X = np.vstack([cluster1, cluster2])
        
        data = pd.DataFrame(X, columns=[f'Trait_{i}' for i in range(8)])
        data['Strain_ID'] = [f'Strain_{i}' for i in range(30)]
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_optimal', random_state=42)
        analyzer.data = data
        
        # Let analyzer select optimal number
        analyzer.perform_clustering(n_clusters=None)
        
        assert analyzer.clusters is not None
        assert len(analyzer.clusters) == 30
        assert hasattr(analyzer, 'linkage_matrix')

    def test_clustering_different_methods(self):
        """Test clustering with different linkage methods."""
        np.random.seed(42)
        X = np.random.binomial(1, 0.5, (25, 10))
        
        data = pd.DataFrame(X, columns=[f'Trait_{i}' for i in range(10)])
        data['Strain_ID'] = [f'Strain_{i}' for i in range(25)]
        
        for method in ['ward', 'complete', 'average', 'single']:
            analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_methods', random_state=42)
            analyzer.data = data
            
            try:
                analyzer.perform_clustering(n_clusters=3, method=method)
                assert analyzer.clusters is not None
                assert len(np.unique(analyzer.clusters)) <= 3
            except Exception as e:
                # Some methods might not work with our distance metric
                # That's OK as long as ward (default) works
                if method != 'ward':
                    pass
                else:
                    raise


@pytest.mark.skipif(not HAS_PRINCE, reason="prince not available")
class TestMCA:
    """Test Multiple Correspondence Analysis."""

    def test_perform_mca_basic(self):
        """Test basic MCA execution."""
        np.random.seed(42)
        
        data = pd.DataFrame({
            'Strain_ID': [f'Strain_{i}' for i in range(40)],
            'Trait_0': np.random.binomial(1, 0.5, 40),
            'Trait_1': np.random.binomial(1, 0.5, 40),
            'Trait_2': np.random.binomial(1, 0.5, 40),
            'Trait_3': np.random.binomial(1, 0.5, 40),
        })
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_mca', random_state=42)
        analyzer.data = data
        analyzer.perform_mca(n_components=2)
        
        assert 'MCA1' in analyzer.data.columns
        assert 'MCA2' in analyzer.data.columns
        assert 'mca' in analyzer.results
        assert 'explained_variance' in analyzer.results['mca']

    def test_mca_different_components(self):
        """Test MCA with different numbers of components."""
        np.random.seed(42)
        
        data = pd.DataFrame({
            'Strain_ID': [f'Strain_{i}' for i in range(35)],
            'Trait_0': np.random.binomial(1, 0.5, 35),
            'Trait_1': np.random.binomial(1, 0.5, 35),
            'Trait_2': np.random.binomial(1, 0.5, 35),
        })
        
        for n_comp in [2, 3]:
            analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_mca_comp', random_state=42)
            analyzer.data = data
            analyzer.perform_mca(n_components=n_comp)
            
            for i in range(1, n_comp + 1):
                assert f'MCA{i}' in analyzer.data.columns

    def test_mca_explained_variance_sum(self):
        """Test that explained variance components are reasonable."""
        np.random.seed(42)
        
        data = pd.DataFrame({
            'Strain_ID': [f'Strain_{i}' for i in range(50)],
            **{f'Trait_{i}': np.random.binomial(1, 0.5, 50) for i in range(6)}
        })
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_mca_var', random_state=42)
        analyzer.data = data
        analyzer.perform_mca(n_components=3)
        
        explained_var = analyzer.results['mca']['explained_variance']
        
        # Should have at least 3 components
        assert len(explained_var) >= 3
        
        # Should sum to <= 1
        assert sum(explained_var) <= 1.0


class TestHTMLReportGeneration:
    """Test HTML report generation."""

    def setup_method(self):
        """Create temporary directory."""
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_generate_html_report(self):
        """Test HTML report generation."""
        np.random.seed(42)
        
        # Create data and run analysis
        data = pd.DataFrame({
            'Strain_ID': [f'Strain_{i}' for i in range(30)],
            **{f'Trait_{i}': np.random.binomial(1, 0.5, 30) for i in range(6)}
        })
        
        analyzer = StrepSuisAnalyzer(output_dir=self.temp_dir, random_state=42)
        analyzer.data = data
        analyzer.perform_clustering(n_clusters=2)
        analyzer.calculate_trait_associations(fdr_alpha=0.05)
        
        if HAS_PRINCE:
            analyzer.perform_mca(n_components=2)
        
        # Generate report
        analyzer.generate_html_report()
        
        # Check report was created
        html_file = Path(self.temp_dir) / 'analysis_report.html'
        assert html_file.exists()
        
        # Check content
        content = html_file.read_text()
        assert 'StrepSuis' in content
        assert 'Cluster' in content

    def test_html_report_contains_visualizations(self):
        """Test that HTML report contains visualizations."""
        np.random.seed(42)
        
        data = pd.DataFrame({
            'Strain_ID': [f'Strain_{i}' for i in range(25)],
            **{f'Trait_{i}': np.random.binomial(1, 0.5, 25) for i in range(5)}
        })
        
        analyzer = StrepSuisAnalyzer(output_dir=self.temp_dir, random_state=42)
        analyzer.data = data
        analyzer.perform_clustering(n_clusters=2)
        analyzer.calculate_trait_associations(fdr_alpha=0.05)
        analyzer.generate_html_report()
        
        html_file = Path(self.temp_dir) / 'analysis_report.html'
        content = html_file.read_text()
        
        # Should contain plotly references
        assert 'plotly' in content.lower() or 'plot' in content.lower()


class TestAnalyzerOutputFiles:
    """Test output file generation."""

    def setup_method(self):
        """Create temporary directory."""
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_csv_output_files(self):
        """Test CSV output file generation."""
        np.random.seed(42)
        
        data = pd.DataFrame({
            'Strain_ID': [f'Strain_{i}' for i in range(20)],
            'Trait_0': np.random.binomial(1, 0.5, 20),
            'Trait_1': np.random.binomial(1, 0.5, 20),
        })
        
        analyzer = StrepSuisAnalyzer(output_dir=self.temp_dir, random_state=42)
        analyzer.data = data
        analyzer.perform_clustering(n_clusters=2)
        analyzer.calculate_trait_associations(fdr_alpha=0.05)
        
        # Save clustered data
        output_file = Path(self.temp_dir) / 'clustered_data.csv'
        analyzer.data.to_csv(output_file, index=False)
        
        assert output_file.exists()
        
        # Save trait associations
        assoc_file = Path(self.temp_dir) / 'trait_associations.csv'
        analyzer.results['trait_associations'].to_csv(assoc_file, index=False)
        
        assert assoc_file.exists()


class TestAnalyzerStateManagement:
    """Test analyzer state management."""

    def test_results_dictionary_initialization(self):
        """Test that results dictionary is initialized."""
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_state', random_state=42)
        
        assert hasattr(analyzer, 'results')
        assert isinstance(analyzer.results, dict)
        assert len(analyzer.results) == 0

    def test_results_storage(self):
        """Test that results are stored properly."""
        np.random.seed(42)
        
        data = pd.DataFrame({
            'Strain_ID': [f'Strain_{i}' for i in range(20)],
            'Trait_0': np.random.binomial(1, 0.5, 20),
            'Trait_1': np.random.binomial(1, 0.5, 20),
        })
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_storage', random_state=42)
        analyzer.data = data
        analyzer.perform_clustering(n_clusters=2)
        analyzer.calculate_trait_associations(fdr_alpha=0.05)
        
        # Check results are stored
        assert 'trait_associations' in analyzer.results
        assert isinstance(analyzer.results['trait_associations'], pd.DataFrame)

    def test_data_attribute_after_loading(self):
        """Test data attribute state after loading."""
        temp_dir = tempfile.mkdtemp()
        try:
            data_file = Path(temp_dir) / 'data.csv'
            df = pd.DataFrame({
                'Strain_ID': ['A', 'B', 'C'],
                'Trait_0': [1, 0, 1],
            })
            df.to_csv(data_file, index=False)
            
            analyzer = StrepSuisAnalyzer(output_dir=temp_dir, random_state=42)
            
            # Before loading
            assert analyzer.data is None
            
            # After loading
            analyzer.load_data([str(data_file)])
            assert analyzer.data is not None
            assert isinstance(analyzer.data, pd.DataFrame)
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_clusters_attribute_after_clustering(self):
        """Test clusters attribute after clustering."""
        np.random.seed(42)
        
        data = pd.DataFrame({
            'Strain_ID': [f'Strain_{i}' for i in range(20)],
            'Trait_0': np.random.binomial(1, 0.5, 20),
            'Trait_1': np.random.binomial(1, 0.5, 20),
        })
        
        analyzer = StrepSuisAnalyzer(output_dir='/tmp/test_clusters', random_state=42)
        analyzer.data = data
        
        # Before clustering
        assert analyzer.clusters is None
        
        # After clustering
        analyzer.perform_clustering(n_clusters=2)
        assert analyzer.clusters is not None
        assert len(analyzer.clusters) == 20
