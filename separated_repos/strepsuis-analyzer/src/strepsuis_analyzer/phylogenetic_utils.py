"""
Phylogenetic analysis utilities for StrepSuisAnalyzer.

Provides tools for phylogenetic tree analysis including Robinson-Foulds distance,
tree comparison, and bipartition analysis.
"""

from typing import Dict, List, Optional, Set, Tuple
import numpy as np
from io import StringIO
import warnings

try:
    from Bio import Phylo
    BIOPYTHON_AVAILABLE = True
except ImportError:
    BIOPYTHON_AVAILABLE = False
    warnings.warn("BioPython not available, phylogenetic analysis limited")

try:
    import dendropy
    DENDROPY_AVAILABLE = True
except ImportError:
    DENDROPY_AVAILABLE = False
    warnings.warn("DendroPy not available, some phylogenetic features disabled")


class PhylogeneticAnalyzer:
    """Analyzes phylogenetic trees and computes tree-based metrics."""

    def __init__(self):
        """Initialize the PhylogeneticAnalyzer."""
        self.tree = None
        self.taxa = []

    def load_tree_from_newick(self, newick_string: str) -> bool:
        """
        Load a phylogenetic tree from Newick format.

        Args:
            newick_string: Newick format tree string

        Returns:
            True if successful, False otherwise
        """
        if not BIOPYTHON_AVAILABLE:
            warnings.warn("BioPython not available")
            return False

        try:
            tree_io = StringIO(newick_string)
            self.tree = Phylo.read(tree_io, "newick")
            self.taxa = [leaf.name for leaf in self.tree.get_terminals()]
            return True
        except Exception as e:
            warnings.warn(f"Failed to load tree: {e}")
            return False

    def get_leaf_names(self) -> List[str]:
        """
        Get names of all leaf nodes.

        Returns:
            List of leaf names
        """
        if self.tree is None:
            return []
        return self.taxa.copy()

    def get_tree_depth(self) -> float:
        """
        Get maximum root-to-tip distance.

        Returns:
            Maximum depth
        """
        if self.tree is None or not BIOPYTHON_AVAILABLE:
            return 0.0

        depths = self.tree.depths()
        if not depths:
            return 0.0

        return float(max(depths.values()))

    def compute_robinson_foulds_distance(
        self, tree1_newick: str, tree2_newick: str, normalize: bool = False
    ) -> float:
        """
        Compute Robinson-Foulds distance between two trees.

        Args:
            tree1_newick: First tree in Newick format
            tree2_newick: Second tree in Newick format
            normalize: Whether to normalize by maximum possible distance

        Returns:
            Robinson-Foulds distance
        """
        if not DENDROPY_AVAILABLE:
            warnings.warn("DendroPy required for RF distance")
            return np.nan

        try:
            tns = dendropy.TaxonNamespace()
            tree1 = dendropy.Tree.get(
                data=tree1_newick, schema="newick", taxon_namespace=tns
            )
            tree2 = dendropy.Tree.get(
                data=tree2_newick, schema="newick", taxon_namespace=tns
            )

            rf_dist = dendropy.calculate.treecompare.symmetric_difference(tree1, tree2)

            if normalize:
                # Maximum RF distance is 2(n-3) where n is number of taxa
                n_taxa = len(tns)
                max_rf = 2 * (n_taxa - 3) if n_taxa > 3 else 1
                rf_dist = rf_dist / max_rf if max_rf > 0 else 0

            return float(rf_dist)

        except Exception as e:
            warnings.warn(f"Failed to compute RF distance: {e}")
            return np.nan

    def get_bipartitions(self, newick_string: str) -> Set[frozenset]:
        """
        Get bipartitions (splits) from a tree.

        Args:
            newick_string: Tree in Newick format

        Returns:
            Set of bipartitions as frozensets of leaf names
        """
        if not DENDROPY_AVAILABLE:
            warnings.warn("DendroPy required for bipartition analysis")
            return set()

        try:
            tree = dendropy.Tree.get(data=newick_string, schema="newick")
            tree.encode_bipartitions()

            bipartitions = set()
            for edge in tree.postorder_edge_iter():
                if edge.bipartition:
                    # Get taxa on one side of the split
                    taxa_subset = frozenset(
                        [taxon.label for taxon in edge.bipartition.leafset_taxa(tree.taxon_namespace)]
                    )
                    # Only store non-trivial bipartitions
                    if len(taxa_subset) > 1 and len(taxa_subset) < len(tree.taxon_namespace):
                        bipartitions.add(taxa_subset)

            return bipartitions

        except Exception as e:
            warnings.warn(f"Failed to get bipartitions: {e}")
            return set()

    def compare_bipartitions(
        self, tree1_newick: str, tree2_newick: str
    ) -> Tuple[int, int, int]:
        """
        Compare bipartitions between two trees.

        Args:
            tree1_newick: First tree in Newick format
            tree2_newick: Second tree in Newick format

        Returns:
            Tuple of (common_bipartitions, unique_to_tree1, unique_to_tree2)
        """
        bp1 = self.get_bipartitions(tree1_newick)
        bp2 = self.get_bipartitions(tree2_newick)

        common = len(bp1.intersection(bp2))
        unique1 = len(bp1 - bp2)
        unique2 = len(bp2 - bp1)

        return common, unique1, unique2

    def compute_pairwise_distances(
        self, newick_string: Optional[str] = None
    ) -> Optional[np.ndarray]:
        """
        Compute pairwise patristic distances between all taxa.

        Args:
            newick_string: Tree in Newick format (uses loaded tree if None)

        Returns:
            Distance matrix as numpy array, or None if failed
        """
        if newick_string is not None:
            self.load_tree_from_newick(newick_string)

        if self.tree is None or not BIOPYTHON_AVAILABLE:
            return None

        try:
            terminals = self.tree.get_terminals()
            n = len(terminals)
            distances = np.zeros((n, n))

            for i, term1 in enumerate(terminals):
                for j, term2 in enumerate(terminals):
                    if i != j:
                        distances[i, j] = self.tree.distance(term1, term2)

            return distances

        except Exception as e:
            warnings.warn(f"Failed to compute distances: {e}")
            return None

    def compute_cophenetic_correlation(
        self, newick_string: str, distance_matrix: np.ndarray
    ) -> float:
        """
        Compute cophenetic correlation between tree and distance matrix.

        Args:
            newick_string: Tree in Newick format
            distance_matrix: Original distance matrix

        Returns:
            Cophenetic correlation coefficient
        """
        tree_distances = self.compute_pairwise_distances(newick_string)

        if tree_distances is None:
            return np.nan

        # Flatten upper triangles
        n = tree_distances.shape[0]
        tree_flat = tree_distances[np.triu_indices(n, k=1)]
        orig_flat = distance_matrix[np.triu_indices(n, k=1)]

        # Compute correlation
        if len(tree_flat) < 2:
            return np.nan

        correlation = np.corrcoef(tree_flat, orig_flat)[0, 1]

        return float(correlation)

    def get_monophyletic_groups(
        self, newick_string: str, group_dict: Dict[str, List[str]]
    ) -> Dict[str, bool]:
        """
        Check if specified groups are monophyletic.

        Args:
            newick_string: Tree in Newick format
            group_dict: Dictionary mapping group names to lists of taxa

        Returns:
            Dictionary mapping group names to monophyly status
        """
        if not BIOPYTHON_AVAILABLE:
            return {group: False for group in group_dict}

        self.load_tree_from_newick(newick_string)
        if self.tree is None:
            return {group: False for group in group_dict}

        results = {}
        for group_name, taxa_list in group_dict.items():
            try:
                # Get terminal nodes for this group
                terminals = [
                    term for term in self.tree.get_terminals() if term.name in taxa_list
                ]

                if len(terminals) == 0:
                    results[group_name] = False
                    continue

                # Check if monophyletic
                is_monophyletic = self.tree.is_monophyletic(terminals)
                results[group_name] = is_monophyletic

            except Exception:
                results[group_name] = False

        return results

    def compute_faith_pd(
        self, newick_string: str, taxa_subset: Optional[List[str]] = None
    ) -> float:
        """
        Compute Faith's Phylogenetic Diversity.

        Args:
            newick_string: Tree in Newick format
            taxa_subset: Subset of taxa to consider (all if None)

        Returns:
            Faith's PD value
        """
        if not BIOPYTHON_AVAILABLE:
            return np.nan

        self.load_tree_from_newick(newick_string)
        if self.tree is None:
            return np.nan

        try:
            if taxa_subset is None:
                # Use all taxa
                return float(self.tree.total_branch_length())

            # Get terminals for subset
            terminals_subset = [
                term for term in self.tree.get_terminals() if term.name in taxa_subset
            ]

            if len(terminals_subset) == 0:
                return 0.0

            # Find MRCA and sum branch lengths
            if len(terminals_subset) == 1:
                # Single taxon - sum from root to tip
                return float(self.tree.distance(self.tree.root, terminals_subset[0]))

            # Get all paths
            paths = []
            for terminal in terminals_subset:
                path = self.tree.get_path(terminal)
                paths.extend(path)

            # Unique branches
            unique_branches = set(paths)

            # Sum branch lengths
            pd = sum(
                clade.branch_length
                for clade in unique_branches
                if clade.branch_length is not None
            )

            return float(pd)

        except Exception as e:
            warnings.warn(f"Failed to compute Faith's PD: {e}")
            return np.nan

    def validate_tree_structure(self, newick_string: str) -> Tuple[bool, List[str]]:
        """
        Validate tree structure and return issues.

        Args:
            newick_string: Tree in Newick format

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        # Try to load tree
        if not self.load_tree_from_newick(newick_string):
            issues.append("Failed to parse tree")
            return False, issues

        if self.tree is None:
            issues.append("Tree is None after loading")
            return False, issues

        # Check for duplicate leaf names
        leaf_names = self.get_leaf_names()
        if len(leaf_names) != len(set(leaf_names)):
            issues.append("Tree contains duplicate leaf names")

        # Check for zero or negative branch lengths
        for clade in self.tree.find_clades():
            if clade.branch_length is not None and clade.branch_length < 0:
                issues.append("Tree contains negative branch lengths")
                break

        # Check if tree is bifurcating
        for clade in self.tree.find_clades(terminal=False):
            if len(clade.clades) > 2:
                issues.append("Tree is not strictly bifurcating")
                break

        is_valid = len(issues) == 0
        return is_valid, issues
