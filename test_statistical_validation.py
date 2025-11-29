#!/usr/bin/env python3
"""
Mathematical validation tests for statistical functions.

Tests verify analytical expectations, probability bounds, symmetry,
and monotonicity properties of statistical routines used across modules.
"""

import sys
import os
import numpy as np
import pandas as pd
import pytest
from scipy import stats

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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

# Import statistical functions from Network Analysis
from Network_Analysis_2025_06_26 import (
    chi2_phi,
    calculate_entropy,
    cramers_v,
    information_gain,
    normalized_mutual_info,
)


class TestEntropyProperties:
    """Mathematical validation tests for entropy calculations."""
    
    def test_entropy_bounds(self):
        """Entropy must be non-negative and bounded."""
        series = pd.Series([0, 0, 1, 1, 1, 0])
        H, Hn = calculate_entropy(series)
        
        # H >= 0 always
        assert H >= 0, "Entropy must be non-negative"
        
        # For binary with natural log: H <= ln(2) ≈ 0.693
        assert H <= np.log(2) + 1e-10, "Binary entropy bounded by ln(2)"
        
        # Normalized entropy in [0, 1]
        assert 0 <= Hn <= 1.0, "Normalized entropy must be in [0, 1]"
    
    def test_entropy_maximum_uniform(self):
        """Entropy is maximized for uniform distribution."""
        # Uniform binary distribution: p=0.5
        uniform = pd.Series([0, 1] * 50)
        H_uniform, _ = calculate_entropy(uniform)
        
        # Skewed distribution: p=0.9
        skewed = pd.Series([1] * 90 + [0] * 10)
        H_skewed, _ = calculate_entropy(skewed)
        
        # Uniform should have higher entropy
        assert H_uniform > H_skewed, "Uniform distribution maximizes entropy"
    
    def test_entropy_minimum_pure(self):
        """Entropy is zero for pure (constant) distribution."""
        pure = pd.Series([1, 1, 1, 1, 1])
        H, Hn = calculate_entropy(pure)
        
        # Pure distribution has zero entropy
        assert H < 1e-10, "Pure distribution has zero entropy"
    
    def test_entropy_analytical_value(self):
        """Test entropy against analytical calculation."""
        # p=0.5: H = -0.5*ln(0.5) - 0.5*ln(0.5) = ln(2) ≈ 0.693 (nat)
        # The implementation uses natural log (scipy_entropy default)
        balanced = pd.Series([0, 1] * 100)
        H, _ = calculate_entropy(balanced)
        
        # Should be close to ln(2) ≈ 0.693 nats
        expected = np.log(2)  # Natural log
        assert abs(H - expected) < 0.01, f"Expected ~{expected:.3f} nats, got {H}"


class TestMutualInformationProperties:
    """Mathematical validation tests for mutual information."""
    
    def test_mi_symmetry(self):
        """Mutual information is symmetric: I(X;Y) = I(Y;X)."""
        x = pd.Series(np.random.randint(0, 2, 100))
        y = pd.Series(np.random.randint(0, 2, 100))
        
        nmi_xy = normalized_mutual_info(x, y)
        nmi_yx = normalized_mutual_info(y, x)
        
        assert abs(nmi_xy - nmi_yx) < 1e-10, "NMI must be symmetric"
    
    def test_mi_bounds(self):
        """NMI is bounded in [0, 1]."""
        x = pd.Series(np.random.randint(0, 2, 100))
        y = pd.Series(np.random.randint(0, 2, 100))
        
        nmi = normalized_mutual_info(x, y)
        
        assert 0 <= nmi <= 1.0 + 1e-10, "NMI must be in [0, 1]"
    
    def test_mi_identical_variables(self):
        """NMI=1 for identical variables (perfect dependence)."""
        x = pd.Series([0, 1, 0, 1, 0, 1, 0, 1])
        
        nmi = normalized_mutual_info(x, x)
        
        # Identical variables have maximum NMI
        assert nmi > 0.99, "Identical variables should have NMI close to 1"
    
    def test_mi_independent_low(self):
        """NMI should be low for independent variables."""
        np.random.seed(42)
        # Generate independent random variables
        x = pd.Series(np.random.randint(0, 2, 1000))
        y = pd.Series(np.random.randint(0, 2, 1000))
        
        nmi = normalized_mutual_info(x, y)
        
        # Independent variables should have low NMI (< 0.1)
        assert nmi < 0.15, f"Independent variables should have low NMI, got {nmi}"


class TestInformationGainProperties:
    """Mathematical validation tests for information gain."""
    
    def test_ig_non_negative(self):
        """Information gain is non-negative."""
        x = pd.Series(np.random.randint(0, 2, 100))
        y = pd.Series(np.random.randint(0, 2, 100))
        
        ig = information_gain(x, y)
        
        assert ig >= -1e-10, "Information gain must be non-negative"
    
    def test_ig_perfect_predictor(self):
        """IG is maximized when x perfectly predicts y."""
        # Perfect prediction: y = x
        x = pd.Series([0, 0, 1, 1, 0, 1, 0, 1])
        y = x.copy()
        
        ig = information_gain(x, y)
        
        # IG should equal H(Y) for perfect predictor
        H_y, _ = calculate_entropy(y)
        assert abs(ig - H_y) < 0.01, "IG for perfect predictor equals H(Y)"
    
    def test_ig_independent_zero(self):
        """IG is zero for independent variables (asymptotically)."""
        np.random.seed(42)
        x = pd.Series(np.random.randint(0, 2, 1000))
        y = pd.Series(np.random.randint(0, 2, 1000))
        
        ig = information_gain(x, y)
        
        # Independent variables have near-zero IG
        assert ig < 0.05, f"IG for independent vars should be ~0, got {ig}"


class TestPhiCoefficientProperties:
    """Mathematical validation tests for phi coefficient."""
    
    def test_phi_bounds(self):
        """Phi coefficient is in [0, 1] for binary data."""
        x = pd.Series([0, 0, 1, 1, 0, 1, 1, 0])
        y = pd.Series([0, 1, 1, 1, 0, 1, 0, 0])
        
        p, phi, _, _, _ = chi2_phi(x, y)
        
        assert 0 <= phi <= 1, "Phi must be in [0, 1]"
    
    def test_phi_perfect_positive_correlation(self):
        """Phi = 1 for perfect positive correlation."""
        x = pd.Series([0, 0, 1, 1, 0, 0, 1, 1])
        y = pd.Series([0, 0, 1, 1, 0, 0, 1, 1])
        
        _, phi, _, _, _ = chi2_phi(x, y)
        
        assert phi > 0.99, f"Perfect correlation should give phi ~1, got {phi}"
    
    def test_phi_no_correlation(self):
        """Phi near 0 for independent variables."""
        np.random.seed(42)
        x = pd.Series(np.random.randint(0, 2, 500))
        y = pd.Series(np.random.randint(0, 2, 500))
        
        _, phi, _, _, _ = chi2_phi(x, y)
        
        # Phi should be low for independent vars
        assert phi < 0.15, f"Independent vars should have low phi, got {phi}"
    
    def test_pvalue_bounds(self):
        """P-value must be in [0, 1]."""
        x = pd.Series([0, 0, 1, 1, 0, 1, 1, 0])
        y = pd.Series([0, 1, 1, 1, 0, 1, 0, 0])
        
        p, _, _, _, _ = chi2_phi(x, y)
        
        assert 0 <= p <= 1, "P-value must be in [0, 1]"
    
    def test_significant_association_low_pvalue(self):
        """Strong association should yield low p-value."""
        # Strong association
        x = pd.Series([0, 0, 0, 0, 1, 1, 1, 1] * 10)
        y = pd.Series([0, 0, 0, 0, 1, 1, 1, 1] * 10)
        
        p, phi, _, _, _ = chi2_phi(x, y)
        
        # Perfect association should have very low p-value
        assert p < 0.001, f"Perfect association should have p < 0.001, got {p}"


class TestCramersVProperties:
    """Mathematical validation tests for Cramér's V."""
    
    def test_cramers_v_bounds(self):
        """Cramér's V is in [0, 1]."""
        contingency = pd.DataFrame([[10, 5], [3, 8]])
        v, lo, hi = cramers_v(contingency)
        
        assert 0 <= v <= 1, "Cramér's V must be in [0, 1]"
        assert lo <= v <= hi, "CI must contain point estimate"
    
    def test_cramers_v_perfect_association(self):
        """Cramér's V approaches 1 for perfect association."""
        # Perfect diagonal (no off-diagonal elements)
        contingency = pd.DataFrame([[20, 0], [0, 20]])
        v, _, _ = cramers_v(contingency)
        
        # May not be exactly 1 due to bias correction
        assert v > 0.9, f"Perfect association should give V > 0.9, got {v}"
    
    def test_cramers_v_no_association(self):
        """Cramér's V near 0 for no association."""
        # Uniform distribution (independence)
        contingency = pd.DataFrame([[10, 10], [10, 10]])
        v, _, _ = cramers_v(contingency)
        
        assert v < 0.1, f"No association should give V ~0, got {v}"


class TestStatisticalConsistency:
    """Cross-validation tests for consistency between statistical measures."""
    
    def test_phi_chi2_relationship(self):
        """Verify phi = sqrt(chi2/n) relationship."""
        x = pd.Series([0, 0, 1, 1, 0, 1, 1, 0, 0, 1])
        y = pd.Series([0, 1, 1, 1, 0, 1, 0, 0, 1, 0])
        n = len(x)
        
        p, phi, contingency, _, _ = chi2_phi(x, y)
        
        # Manual chi2 calculation
        chi2, _, _, _ = stats.chi2_contingency(contingency, correction=False)
        phi_from_chi2 = np.sqrt(chi2 / n)
        
        # Should be approximately equal
        assert abs(phi - phi_from_chi2) < 0.1, \
            f"Phi ({phi}) should equal sqrt(chi2/n) ({phi_from_chi2})"
    
    def test_mi_entropy_relationship(self):
        """Verify mutual information properties."""
        x = pd.Series([0, 0, 1, 1, 0, 1, 0, 1])
        y = pd.Series([0, 1, 1, 1, 0, 0, 1, 0])
        
        # Get mutual information (as information gain)
        ig = information_gain(x, y)
        
        # IG should be non-negative
        assert ig >= -1e-10, f"IG should be non-negative, got {ig}"
        
        # When x and y are not perfectly correlated, IG should be 
        # less than or equal to the smaller of H(X) and H(Y)
        H_x, _ = calculate_entropy(x)
        H_y, _ = calculate_entropy(y)
        
        # IG <= min(H(X), H(Y))
        assert ig <= min(H_x, H_y) + 0.1, \
            f"IG ({ig}) should be <= min(H(X), H(Y)) = {min(H_x, H_y)}"


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_entropy_single_value(self):
        """Entropy of single value series."""
        single = pd.Series([1])
        H, Hn = calculate_entropy(single)
        
        assert H == 0, "Single value has zero entropy"
    
    def test_phi_constant_column(self):
        """Phi with constant column should be handled."""
        x = pd.Series([1, 1, 1, 1, 1])
        y = pd.Series([0, 1, 0, 1, 0])
        
        # Should not raise error, phi should be 0 or NaN
        p, phi, _, _, _ = chi2_phi(x, y)
        # Result depends on implementation
        assert phi >= 0 or np.isnan(phi), "Constant column should be handled"
    
    def test_mi_constant_variable(self):
        """MI with constant variable should be zero."""
        x = pd.Series([1, 1, 1, 1, 1, 1, 1, 1])
        y = pd.Series([0, 1, 0, 1, 0, 1, 0, 1])
        
        nmi = normalized_mutual_info(x, y)
        
        # Should be 0 (or handle gracefully)
        assert nmi == 0 or np.isnan(nmi), "Constant variable has zero MI"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
