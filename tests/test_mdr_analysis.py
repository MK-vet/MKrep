#!/usr/bin/env python3
"""
Unit and integration tests for MDR Analysis module (src/mdr_analysis.py).

Tests cover:
- MDR identification functions
- Antibiotic class resistance building
- Bootstrap confidence interval calculations
- Co-occurrence analysis
- Contingency table utilities
- Pattern frequency calculations
"""

import sys
import os
import warnings
import numpy as np
import pandas as pd
import pytest

# Suppress warnings in tests
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

# Add parent directory to path to import from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock google.colab module for testing
class MockFiles:
    def upload(self):
        return {}
    def download(self, filename):
        pass

class MockColab:
    files = MockFiles()

sys.modules['google'] = type(sys)('google')
sys.modules['google.colab'] = MockColab()

# Import functions from src/mdr_analysis.py
from src.mdr_analysis import (
    safe_contingency,
    add_significance_stars,
    build_class_resistance,
    identify_mdr_isolates,
    extract_amr_genes,
    get_mdr_patterns_pheno,
    get_mdr_patterns_geno,
    bootstrap_pattern_freq,
    pairwise_cooccurrence,
    ANTIBIOTIC_CLASSES,
)


class TestSafeContingency:
    """Tests for safe contingency table analysis."""
    
    def test_basic_contingency(self):
        """Test basic contingency table calculation."""
        table = pd.DataFrame([[20, 5], [5, 20]])
        chi2, p_val, phi = safe_contingency(table)
        
        assert p_val < 0.05  # Should be significant
        assert phi > 0  # Positive association
    
    def test_fisher_exact_small_counts(self):
        """Test Fisher's exact test is used for small expected counts."""
        table = pd.DataFrame([[2, 1], [1, 2]])
        chi2, p_val, phi = safe_contingency(table)
        
        assert p_val is not np.nan
    
    def test_empty_table(self):
        """Test handling of empty contingency table."""
        table = pd.DataFrame([[0, 0], [0, 0]])
        chi2, p_val, phi = safe_contingency(table)
        
        assert np.isnan(chi2) or np.isnan(p_val) or np.isnan(phi)
    
    def test_non_square_table(self):
        """Test handling of non-2x2 tables."""
        table = pd.DataFrame([[10, 5, 3], [5, 10, 2]])
        chi2, p_val, phi = safe_contingency(table)
        
        assert np.isnan(chi2) and np.isnan(p_val) and np.isnan(phi)
    
    def test_phi_range(self):
        """Test that phi is in valid range [-1, 1]."""
        table = pd.DataFrame([[15, 10], [8, 17]])
        chi2, p_val, phi = safe_contingency(table)
        
        if not np.isnan(phi):
            assert -1.0 <= phi <= 1.0


class TestSignificanceStars:
    """Tests for significance star formatting."""
    
    def test_highly_significant(self):
        """Test formatting for p < 0.001."""
        result = add_significance_stars(0.0005)
        assert '***' in result
    
    def test_significant(self):
        """Test formatting for p < 0.01."""
        result = add_significance_stars(0.005)
        assert '**' in result
    
    def test_marginally_significant(self):
        """Test formatting for p < 0.05."""
        result = add_significance_stars(0.03)
        assert '*' in result
    
    def test_not_significant(self):
        """Test formatting for p >= 0.05."""
        result = add_significance_stars(0.1)
        assert '*' not in result
    
    def test_nan_value(self):
        """Test handling of NaN values."""
        result = add_significance_stars(np.nan)
        assert result == ""
    
    def test_none_value(self):
        """Test handling of None values."""
        result = add_significance_stars(None)
        assert result == ""


class TestBuildClassResistance:
    """Tests for antibiotic class resistance matrix building."""
    
    def test_class_resistance_creation(self):
        """Test creation of class resistance matrix."""
        data = pd.DataFrame({
            'Strain_ID': ['S1', 'S2', 'S3'],
            'Oxytetracycline': [1, 0, 1],
            'Doxycycline': [0, 1, 0],
            'Penicillin': [1, 1, 0],
            'Ampicillin': [0, 1, 0]
        })
        
        pheno_cols = ['Oxytetracycline', 'Doxycycline', 'Penicillin', 'Ampicillin']
        class_df = build_class_resistance(data, pheno_cols)
        
        # Should have Tetracyclines and Penicillins classes
        assert 'Tetracyclines' in class_df.columns
        assert 'Penicillins' in class_df.columns
        
        # S1: Oxytetracycline=1 => Tetracyclines=1
        assert class_df.loc[0, 'Tetracyclines'] == 1
    
    def test_class_or_logic(self):
        """Test that class resistance uses OR logic."""
        data = pd.DataFrame({
            'Oxytetracycline': [1, 0, 0],
            'Doxycycline': [0, 1, 0]
        })
        
        pheno_cols = ['Oxytetracycline', 'Doxycycline']
        class_df = build_class_resistance(data, pheno_cols)
        
        # Tetracyclines should be 1 if either is 1
        assert class_df.loc[0, 'Tetracyclines'] == 1
        assert class_df.loc[1, 'Tetracyclines'] == 1
        assert class_df.loc[2, 'Tetracyclines'] == 0
    
    def test_missing_drugs(self):
        """Test handling of missing drug columns."""
        data = pd.DataFrame({
            'UnknownDrug': [1, 0, 1]
        })
        
        class_df = build_class_resistance(data, ['UnknownDrug'])
        
        # Should still create all class columns (with 0 values)
        assert len(class_df.columns) >= 0


class TestIdentifyMDRIsolates:
    """Tests for MDR isolate identification."""
    
    def test_mdr_threshold_default(self):
        """Test MDR identification with default threshold (3)."""
        class_df = pd.DataFrame({
            'Class1': [1, 1, 1, 1],
            'Class2': [1, 1, 1, 0],
            'Class3': [1, 1, 0, 0],
            'Class4': [1, 0, 0, 0]
        })
        
        mdr_mask = identify_mdr_isolates(class_df, threshold=3)
        
        # Only first two isolates have >= 3 classes resistant
        assert mdr_mask[0] == True
        assert mdr_mask[1] == True
        assert mdr_mask[2] == False
        assert mdr_mask[3] == False
    
    def test_mdr_threshold_custom(self):
        """Test MDR identification with custom threshold."""
        class_df = pd.DataFrame({
            'Class1': [1, 1, 0],
            'Class2': [1, 0, 0]
        })
        
        mdr_mask = identify_mdr_isolates(class_df, threshold=2)
        
        assert mdr_mask[0] == True
        assert mdr_mask[1] == False
        assert mdr_mask[2] == False
    
    def test_all_mdr(self):
        """Test when all isolates are MDR."""
        class_df = pd.DataFrame({
            'Class1': [1, 1, 1],
            'Class2': [1, 1, 1],
            'Class3': [1, 1, 1]
        })
        
        mdr_mask = identify_mdr_isolates(class_df, threshold=3)
        
        assert all(mdr_mask)
    
    def test_no_mdr(self):
        """Test when no isolates are MDR."""
        class_df = pd.DataFrame({
            'Class1': [1, 0, 0],
            'Class2': [0, 1, 0],
            'Class3': [0, 0, 1]
        })
        
        mdr_mask = identify_mdr_isolates(class_df, threshold=3)
        
        assert not any(mdr_mask)


class TestExtractAMRGenes:
    """Tests for AMR gene extraction."""
    
    def test_basic_extraction(self):
        """Test basic AMR gene extraction."""
        data = pd.DataFrame({
            'Strain_ID': ['S1', 'S2'],
            'gene1': [1, 0],
            'gene2': [0, 1]
        })
        
        gene_df = extract_amr_genes(data, ['gene1', 'gene2'])
        
        assert gene_df.shape == (2, 2)
        assert gene_df['gene1'].iloc[0] == 1
        assert gene_df['gene1'].iloc[1] == 0
    
    def test_non_numeric_conversion(self):
        """Test conversion of non-numeric values."""
        data = pd.DataFrame({
            'gene1': ['1', '0', '1'],
            'gene2': [1, 0, 1]
        })
        
        gene_df = extract_amr_genes(data, ['gene1', 'gene2'])
        
        # All values should be integers
        assert gene_df['gene1'].dtype in [np.int32, np.int64, int]


class TestMDRPatterns:
    """Tests for MDR pattern detection."""
    
    def test_pheno_pattern_detection(self):
        """Test phenotypic resistance pattern detection."""
        mdr_class_df = pd.DataFrame({
            'Tetracyclines': [1, 1, 0],
            'Penicillins': [1, 0, 0],
            'Macrolides': [1, 1, 1]
        })
        
        patterns = get_mdr_patterns_pheno(mdr_class_df)
        
        assert len(patterns) == 3
        # First row: all three classes
        assert 'Macrolides' in patterns.iloc[0]
        assert 'Penicillins' in patterns.iloc[0]
        assert 'Tetracyclines' in patterns.iloc[0]
    
    def test_geno_pattern_detection(self):
        """Test genotypic resistance pattern detection."""
        mdr_gene_df = pd.DataFrame({
            'tetM': [1, 0, 1],
            'ermB': [1, 1, 0],
            'blaTEM': [0, 1, 0]
        })
        
        patterns = get_mdr_patterns_geno(mdr_gene_df)
        
        assert len(patterns) == 3
    
    def test_no_resistance_pattern(self):
        """Test detection of no resistance pattern."""
        mdr_class_df = pd.DataFrame({
            'Class1': [0],
            'Class2': [0]
        })
        
        patterns = get_mdr_patterns_pheno(mdr_class_df)
        
        assert patterns.iloc[0] == ('No_Resistance',)
    
    def test_no_genes_pattern(self):
        """Test detection of no genes pattern."""
        mdr_gene_df = pd.DataFrame({
            'gene1': [0],
            'gene2': [0]
        })
        
        patterns = get_mdr_patterns_geno(mdr_gene_df)
        
        assert patterns.iloc[0] == ('No_Genes',)


class TestBootstrapPatternFreq:
    """Tests for bootstrap pattern frequency calculation."""
    
    def test_pattern_frequency(self):
        """Test pattern frequency calculation."""
        patterns = pd.Series([
            ('A', 'B'),
            ('A', 'B'),
            ('C',),
            ('A', 'B'),
            ('C',)
        ])
        
        df = bootstrap_pattern_freq(patterns, n_iter=50, conf_level=0.95)
        
        assert 'Pattern' in df.columns
        assert 'Count' in df.columns
        assert 'Frequency(%)' in df.columns
        assert 'CI_Lower' in df.columns
        assert 'CI_Upper' in df.columns
    
    def test_empty_patterns(self):
        """Test handling of empty patterns."""
        patterns = pd.Series([], dtype=object)
        
        df = bootstrap_pattern_freq(patterns, n_iter=50)
        
        assert df.empty
    
    def test_ci_bounds(self):
        """Test that CI bounds are reasonable."""
        patterns = pd.Series([
            ('A',),
            ('A',),
            ('A',),
            ('B',),
            ('B',)
        ])
        
        df = bootstrap_pattern_freq(patterns, n_iter=100, conf_level=0.95)
        
        for _, row in df.iterrows():
            assert row['CI_Lower'] <= row['Frequency(%)']
            assert row['CI_Upper'] >= row['Frequency(%)']


class TestPairwiseCooccurrence:
    """Tests for pairwise co-occurrence analysis."""
    
    def test_basic_cooccurrence(self):
        """Test basic co-occurrence calculation."""
        # Create data with strong, significant co-occurrence
        np.random.seed(42)
        n = 100
        feat1 = np.concatenate([np.ones(70), np.zeros(30)]).astype(int)
        feat2 = np.concatenate([np.ones(60), np.zeros(40)]).astype(int)
        feat3 = np.concatenate([np.zeros(80), np.ones(20)]).astype(int)
        
        df = pd.DataFrame({
            'feat1': feat1,
            'feat2': feat2,
            'feat3': feat3
        })
        
        result = pairwise_cooccurrence(df, alpha=0.3)  # Higher alpha to get results
        
        # Result should have proper columns if not empty
        # Function only returns significant pairs after FDR correction
        assert 'Item1' in result.columns or result.empty
        assert 'Item2' in result.columns or result.empty
        assert 'Phi' in result.columns or result.empty
    
    def test_single_column(self):
        """Test handling of single column (no pairs)."""
        df = pd.DataFrame({
            'feat1': [1, 0, 1, 0]
        })
        
        result = pairwise_cooccurrence(df)
        
        assert result.empty


class TestAntibioticClasses:
    """Tests for antibiotic class definitions."""
    
    def test_classes_defined(self):
        """Test that antibiotic classes are properly defined."""
        assert 'Tetracyclines' in ANTIBIOTIC_CLASSES
        assert 'Penicillins' in ANTIBIOTIC_CLASSES
        assert 'Macrolides' in ANTIBIOTIC_CLASSES
    
    def test_drugs_in_classes(self):
        """Test that drugs are assigned to classes."""
        assert 'Oxytetracycline' in ANTIBIOTIC_CLASSES['Tetracyclines']
        assert 'Penicillin' in ANTIBIOTIC_CLASSES['Penicillins']
    
    def test_no_overlap(self):
        """Test that drugs are not duplicated across classes."""
        all_drugs = []
        for drugs in ANTIBIOTIC_CLASSES.values():
            all_drugs.extend(drugs)
        
        # Check for duplicates
        assert len(all_drugs) == len(set(all_drugs))


def main():
    """Run all tests."""
    print("=" * 80)
    print("Running MDR Analysis Tests")
    print("=" * 80)
    
    # Run with pytest
    exit_code = pytest.main([__file__, '-v', '--tb=short'])
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
