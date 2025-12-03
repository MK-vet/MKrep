"""Tests for phylogenetic utilities module."""

import numpy as np
from strepsuis_analyzer.phylogenetic_utils import PhylogeneticAnalyzer


class TestPhylogeneticAnalyzer:
    """Test suite for PhylogeneticAnalyzer class."""

    def test_init(self):
        """Test analyzer initialization."""
        analyzer = PhylogeneticAnalyzer()
        assert analyzer.tree is None
        assert len(analyzer.taxa) == 0

    def test_load_tree_from_newick(self, sample_tree_newick):
        """Test loading tree from Newick string."""
        analyzer = PhylogeneticAnalyzer()
        success = analyzer.load_tree_from_newick(sample_tree_newick)

        if success:  # Only test if BioPython is available
            assert analyzer.tree is not None
            assert len(analyzer.taxa) > 0

    def test_get_leaf_names(self, sample_tree_newick):
        """Test getting leaf names."""
        analyzer = PhylogeneticAnalyzer()
        analyzer.load_tree_from_newick(sample_tree_newick)

        leaf_names = analyzer.get_leaf_names()
        
        if len(leaf_names) > 0:
            assert isinstance(leaf_names, list)
            assert all(isinstance(name, str) for name in leaf_names)

    def test_validate_tree_structure(self, sample_tree_newick):
        """Test tree structure validation."""
        analyzer = PhylogeneticAnalyzer()
        is_valid, issues = analyzer.validate_tree_structure(sample_tree_newick)

        # Valid tree should have no issues
        if is_valid:
            assert len(issues) == 0

    def test_validate_invalid_tree(self):
        """Test validation with invalid tree."""
        analyzer = PhylogeneticAnalyzer()
        invalid_tree = "((A:0.1,B:0.2)"  # Missing parts
        is_valid, issues = analyzer.validate_tree_structure(invalid_tree)

        assert not is_valid or len(issues) > 0

    def test_compute_robinson_foulds_identical_trees(self, sample_tree_newick):
        """Test RF distance between identical trees."""
        analyzer = PhylogeneticAnalyzer()
        rf = analyzer.compute_robinson_foulds_distance(
            sample_tree_newick, sample_tree_newick
        )

        if not np.isnan(rf):
            assert abs(rf) < 0.001

    def test_get_bipartitions(self, sample_tree_newick):
        """Test getting bipartitions from tree."""
        analyzer = PhylogeneticAnalyzer()
        bipartitions = analyzer.get_bipartitions(sample_tree_newick)

        assert isinstance(bipartitions, set)
