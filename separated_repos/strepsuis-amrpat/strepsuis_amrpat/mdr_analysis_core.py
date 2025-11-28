#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ENHANCED MDR ANALYSIS PIPELINE (HYBRID NETWORK APPROACH)
-------------------------------------------------------
This script implements comprehensive statistical analyses for phenotypic antibiotic resistance
and antimicrobial resistance (AMR) genes in both the complete isolate collection and the
Multi-Drug Resistant (MDR) subset.

Statistical methods employed:
1. Bootstrap resampling (5000 iterations) with 95% confidence intervals for prevalence estimation
2. Chi-square test and Fisher's exact test (when expected cell counts <5) for association analysis
3. Phi coefficient for association strength measurement
4. Multiple hypothesis testing correction using Benjamini-Hochberg procedure (FDR)
5. Louvain community detection algorithm for network module identification
6. Association rule mining with support and lift metrics

Major analytical steps:
1)  Frequencies of phenotypic resistance in all isolates (bootstrap 95% CI)
2)  Frequencies of phenotypic resistance in MDR isolates (bootstrap 95% CI)
3)  Frequencies of AMR genes in all isolates (bootstrap 95% CI)
4)  Frequencies of AMR genes in MDR isolates (bootstrap 95% CI)
5)  Frequencies of phenotypic resistance patterns in MDR (bootstrap 95% CI)
6)  Frequencies of AMR gene patterns in MDR (bootstrap 95% CI)
7)  Co-occurrence among antibiotic classes in MDR (phi, p-value, significance)
8)  Co-occurrence among AMR genes in MDR (phi, p-value, significance)
9)  AMR Gene – Phenotypic Resistance Associations (phi, p-value, significance)
10) Association Rules for Phenotypic Resistances (support, confidence, lift metrics)
11) Association Rules for AMR Genes (support, confidence, lift metrics)
12) Hybrid Co-resistance Network (Phenotype–Gene + optional Pheno–Pheno & Gene–Gene edges):
    a) Interactive figure (Plotly)
    b) Significant edges table (corrected p-values)
    c) Network communities (Louvain)
"""

import logging
import os
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from itertools import combinations
from typing import Any, Dict, List, Tuple

import networkx as nx
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, fisher_exact
from statsmodels.stats.multitest import multipletests

try:
    from .excel_report_utils import ExcelReportGenerator
except ImportError:
    from strepsuis_amrpat.excel_report_utils import ExcelReportGenerator

warnings.filterwarnings("ignore")  # for cleaner console output


###############################################################################
# 0) ENVIRONMENT SETUP
###############################################################################
def setup_environment() -> str:
    """
    Detect if running on Google Colab or locally, handle user input,
    create output directories, and configure logging. Returns the CSV path.

    The function performs the following operations:
    1. Detects execution environment (Google Colab or local machine)
    2. Creates necessary output directories for results storage
    3. Configures logging to both file and console
    4. Handles file upload in Colab or path input locally

    Returns:
        str: Path to the input CSV file containing resistance data
    """
    IN_COLAB = False
    try:
        from google.colab import files

        IN_COLAB = True
        logging.info("Google Colab environment detected.")
    except ImportError:
        logging.info("Local environment detected.")

    # Create output directories
    try:
        os.makedirs("output", exist_ok=True)
        os.makedirs("output/figures", exist_ok=True)
        os.makedirs("output/data", exist_ok=True)
    except Exception as e:
        logging.error(f"Could not create output directories: {e}")
        raise

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(os.path.join("output", "analysis_log.txt")),
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Get CSV path from user
    if IN_COLAB:
        print("Please upload your CSV file containing resistance data...")
        from google.colab import files

        uploaded = files.upload()
        if not uploaded:
            raise ValueError("No file was uploaded. Please run again and upload a file.")
        csv_filename = list(uploaded.keys())[0]
        logging.info(f"Uploaded file: {csv_filename}")
        return csv_filename
    else:
        csv_path = input("Enter the path to your CSV file: ")
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"File not found: {csv_path}")
        return csv_path


###############################################################################
# 1) ANTIBIOTIC CLASSES
###############################################################################
# Predefined classification of antibiotics into functional classes
# This mapping is used for determining MDR status and analyzing class-level resistance patterns
ANTIBIOTIC_CLASSES: Dict[str, List[str]] = {
    "Tetracyclines": ["Oxytetracycline", "Doxycycline"],
    "Macrolides": ["Tulathromycin"],
    "Aminoglycosides": ["Spectinomycin", "Gentamicin"],
    "Pleuromutilins": ["Tiamulin"],
    "Sulfonamides": ["Trimethoprim_Sulphamethoxazole"],
    "Fluoroquinolones": ["Enrofloxacin"],
    "Penicillins": ["Penicillin", "Ampicillin", "Amoxicillin_Clavulanic_acid"],
    "Cephalosporins": ["Ceftiofur"],
    "Phenicols": ["Florfenicol"],
}


###############################################################################
# 2) CORE UTILITY FUNCTIONS
###############################################################################
def safe_contingency(table: pd.DataFrame) -> Tuple[float, float, float]:
    """
    Compute contingency table analysis using Chi-square or Fisher's exact test
    based on expected cell counts (Cochran's rule).

    Statistical methods:
    - Chi-square test: Used when all expected cell frequencies >= 5 and at least
      80% of cells have expected frequency >= 5
    - Fisher's exact test: Used when minimum expected frequency < 1 or <80%
      of cells have expected frequency >= 5
    - Phi coefficient: Calculated as (ad-bc)/sqrt(r₁r₂c₁c₂) for 2×2 tables

    Mathematical details:
    - Chi-square statistic: χ² = Σ[(O-E)²/E] where O=observed, E=expected
    - Expected cell counts: E_ij = (row_i total × column_j total)/grand total
    - Phi coefficient: φ = (ad-bc)/sqrt(r₁r₂c₁c₂) bounded in [-1, 1]
    - When Fisher's test is used, chi2 is derived as φ² × N for consistency

    Parameters:
        table (pd.DataFrame): 2×2 contingency table

    Returns:
        Tuple[float, float, float]: (chi2_statistic, p_value, phi_coefficient)
        - chi2_statistic: Chi-square value (always derived from phi for consistency)
        - p_value: Statistical significance
        - phi_coefficient: Effect size measure (-1 to +1)
    """
    if table.shape != (2, 2):
        return np.nan, np.nan, np.nan

    total = table.values.sum()
    if total == 0:
        return np.nan, np.nan, np.nan

    (a, b), (c, d) = table.values
    row_sums = table.sum(axis=1)
    col_sums = table.sum(axis=0)

    # Calculate phi coefficient for 2×2 table
    num = float(a * d - b * c)
    den = float(row_sums.iloc[0] * row_sums.iloc[1] * col_sums.iloc[0] * col_sums.iloc[1])
    phi_val = num / np.sqrt(den) if den > 0 else np.nan

    if np.isnan(phi_val):
        return np.nan, np.nan, np.nan

    expected = np.outer(row_sums, col_sums) / total
    min_expected = expected.min()
    pct_above_5 = (expected >= 5).sum() / expected.size

    # Cochran's rule: use Fisher's if min expected < 1 or <80% cells have expected >= 5
    if min_expected < 1 or pct_above_5 < 0.8:
        try:
            # Fisher's exact test for small expected frequencies
            _, p_val = fisher_exact(table)
            # Derive chi2 from phi² × N for consistency
            chi2 = phi_val ** 2 * total
            return (float(chi2), float(p_val), float(phi_val))
        except (ValueError, TypeError, ZeroDivisionError):
            return (np.nan, np.nan, np.nan)
    else:
        try:
            # Chi-square test for adequate expected frequencies
            chi2, p_val, _, _ = chi2_contingency(table)
            return (float(chi2), float(p_val), float(phi_val))
        except (ValueError, TypeError, ZeroDivisionError):
            return (np.nan, np.nan, np.nan)


def add_significance_stars(p_value: float) -> str:
    """
    Add standard significance level indicators to p-values.

    Statistical convention:
    - p < 0.05 (*): Statistically significant at 5% level
    - p < 0.01 (**): Statistically significant at 1% level
    - p < 0.001 (***): Statistically significant at 0.1% level

    Parameters:
        p_value (float): The p-value to evaluate

    Returns:
        str: Formatted p-value with significance stars:
             * p<0.05 (significant)
             ** p<0.01 (highly significant)
             *** p<0.001 (extremely significant)
    """
    if p_value is None or pd.isna(p_value):
        return ""
    p_str = f"{p_value:.3f}"
    if p_value < 0.001:
        p_str += " ***"
    elif p_value < 0.01:
        p_str += " **"
    elif p_value < 0.05:
        p_str += " *"
    return p_str


###############################################################################
# 3) BOOTSTRAP FREQUENCIES
###############################################################################


def _bootstrap_col(
    col_data: np.ndarray, size: int, n_iter: int, confidence: float
) -> Tuple[float, float, float]:
    """
    Perform bootstrap resampling for a single binary column to estimate
    proportion and confidence intervals.

    Statistical method:
    - Non-parametric bootstrap: Repeatedly sample with replacement to
      estimate the sampling distribution of a statistic (proportion)
    - Percentile method: CI bounds are determined by empirical quantiles
      of the bootstrap distribution

    Mathematical details:
    - For each iteration i (1 to n_iter):
      1. Draw a random sample S_i of size 'size' with replacement
      2. Compute proportion p_i = sum(S_i)/size
    - Final estimate: mean of all p_i values
    - CI bounds: percentiles of the empirical distribution of p_i values
      - Lower bound: (alpha/2) percentile
      - Upper bound: (1-alpha/2) percentile
      where alpha = 1-confidence

    Parameters:
        col_data (np.ndarray): Binary (0/1) column data
        size (int): Sample size (usually equal to original data size)
        n_iter (int): Number of bootstrap iterations
        confidence (float): Confidence level (e.g., 0.95 for 95% CI)

    Returns:
        Tuple[float,float,float]: (mean_proportion, ci_lower, ci_upper)
    """
    proportions = []
    for _ in range(n_iter):
        samp = np.random.choice(col_data, size=size, replace=True)
        proportions.append(samp.mean())
    alpha = 1.0 - confidence
    lower = np.percentile(proportions, alpha / 2 * 100)
    upper = np.percentile(proportions, (1 - alpha / 2) * 100)
    return (np.mean(proportions), lower, upper)


def compute_bootstrap_ci(
    df: pd.DataFrame, n_iter: int = 5000, confidence_level: float = 0.95
) -> pd.DataFrame:
    """
    Compute bootstrap confidence intervals for proportions in each column.

    Statistical method:
    - Parallel implementation of non-parametric bootstrap for computational efficiency
    - Fixed confidence level (default 95%) with 5000 iterations for stable estimates

    Mathematical details:
    - For each column, the _bootstrap_col function is called to:
      1. Generate n_iter bootstrap samples of the same size as original data
      2. Compute the proportion for each sample
      3. Calculate mean proportion and percentile-based CI
    - Parallelization is achieved using ProcessPoolExecutor
      for efficient multi-core utilization

    Parameters:
        df (pd.DataFrame): DataFrame with binary (0/1) columns
        n_iter (int): Number of bootstrap iterations (default: 5000)
        confidence_level (float): Confidence level for intervals (default: 0.95)

    Returns:
        pd.DataFrame: Results with columns:
            - ColumnName: Original column name
            - Mean: Proportion as percentage
            - CI_Lower: Lower bound of confidence interval
            - CI_Upper: Upper bound of confidence interval

    Note: Results are sorted by Mean in descending order.
    """
    if df.empty:
        return pd.DataFrame(columns=["ColumnName", "Mean", "CI_Lower", "CI_Upper"])

    for c in df.columns:
        df[c] = df[c].astype(int)

    results = []
    size = len(df)
    with ProcessPoolExecutor() as executor:
        futures = {}
        for col in df.columns:
            futures[col] = executor.submit(
                _bootstrap_col, df[col].values, size, n_iter, confidence_level
            )
        for col, fut in futures.items():
            try:
                mean_val, low_val, up_val = fut.result()
                results.append(
                    {
                        "ColumnName": col,
                        "Mean": round(mean_val * 100, 3),
                        "CI_Lower": round(low_val * 100, 3),
                        "CI_Upper": round(up_val * 100, 3),
                    }
                )
            except Exception as e:
                logging.error(f"Bootstrap for {col} failed: {e}")
    out = pd.DataFrame(results)
    out.sort_values("Mean", ascending=False, inplace=True)
    out.reset_index(drop=True, inplace=True)
    return out


###############################################################################
# 4) BASIC MDR ANALYSIS
###############################################################################
def build_class_resistance(data: pd.DataFrame, pheno_cols: List[str]) -> pd.DataFrame:
    """
    Construct a binary (0/1) matrix for antibiotic class resistance.

    Method:
    - For each antibiotic class, combines all individual drug resistance
      indicators using logical OR operation (max function)
    - A value of 1 indicates resistance to at least one drug in that class

    Mathematical representation:
    - Let X_i,j be the resistance status (0 or 1) of isolate i to drug j
    - Let C_k be the set of drugs belonging to class k
    - Then class resistance Y_i,k = max(X_i,j) for all j in C_k
      (equivalent to logical OR of all drug resistances in that class)

    Parameters:
        data (pd.DataFrame): Original data with phenotypic resistance columns
        pheno_cols (List[str]): List of phenotypic resistance column names

    Returns:
        pd.DataFrame: Binary matrix of antibiotic class resistance
    """
    out = pd.DataFrame(index=data.index)
    for cls_name, drugs in ANTIBIOTIC_CLASSES.items():
        valid = [d for d in drugs if d in pheno_cols]
        if valid:
            out[cls_name] = data[valid].max(axis=1)
        else:
            out[cls_name] = 0
    return out.astype(int)


def identify_mdr_isolates(class_df: pd.DataFrame, threshold: int = 3) -> pd.Series:
    """
    Identify Multi-Drug Resistant (MDR) isolates based on class resistance.

    Definition:
    - An isolate is considered MDR if it shows resistance to at least
      'threshold' different antibiotic classes (default: 3)

    Mathematical representation:
    - Let Y_i,k be the class resistance status (0 or 1) of isolate i to class k
    - Let n_i = sum(Y_i,k) for all classes k
    - Isolate i is MDR if n_i ≥ threshold

    Parameters:
        class_df (pd.DataFrame): Antibiotic class resistance matrix (0/1)
        threshold (int): Minimum number of resistance classes for MDR (default: 3)

    Returns:
        pd.Series: Boolean mask identifying MDR isolates
    """
    return class_df.sum(axis=1) >= threshold


###############################################################################
# 5) AMR GENE + PATTERNS
###############################################################################
def extract_amr_genes(data: pd.DataFrame, gene_cols: List[str]) -> pd.DataFrame:
    """
    Extract antimicrobial resistance gene data as binary presence/absence.

    Method:
    - Converts potentially mixed data types to binary (0/1) format
    - Any non-zero, non-empty value is considered present (1)

    Data conversion details:
    - Numeric columns: All non-zero values converted to 1
    - Non-numeric columns: Values converted using the following rule:
      Value is 1 if not NA, not 0, and not empty string

    Parameters:
        data (pd.DataFrame): Original data containing AMR gene information
        gene_cols (List[str]): Column names for AMR genes

    Returns:
        pd.DataFrame: Binary matrix of AMR gene presence (0/1)
    """
    amr = data[gene_cols].copy()
    for c in amr.columns:
        if not pd.api.types.is_numeric_dtype(amr[c]):
            try:
                amr[c] = amr[c].astype(int)
            except (ValueError, TypeError):
                amr[c] = (~amr[c].isna() & (amr[c] != 0) & (amr[c] != "")).astype(int)
    return amr.astype(int)


def get_mdr_patterns_pheno(mdr_class_df: pd.DataFrame) -> pd.Series:
    """
    Identify unique patterns of phenotypic resistance in MDR isolates.

    Method:
    - Creates a tuple of resistance classes for each isolate
    - Each tuple represents the specific combination of classes
      to which the isolate shows resistance

    Pattern representation:
    - Each row in the input matrix represents an isolate
    - The pattern is a tuple of column names where the value is 1
    - Patterns are sorted alphabetically for consistency
    - Empty patterns return as ("No_Resistance",) for clarity

    Parameters:
        mdr_class_df (pd.DataFrame): Binary matrix of class resistance in MDR isolates

    Returns:
        pd.Series: Series with tuples of resistance patterns for each isolate
    """

    def row_pat(row):
        items = [col for col, val in row.items() if val == 1]
        return tuple(sorted(items)) if items else ("No_Resistance",)

    return mdr_class_df.apply(row_pat, axis=1)


def get_mdr_patterns_geno(mdr_gene_df: pd.DataFrame) -> pd.Series:
    """
    Identify unique patterns of AMR gene presence in MDR isolates.

    Method:
    - Creates a tuple of AMR genes present in each isolate
    - Each tuple represents the specific combination of genes
      present in the isolate

    Pattern representation:
    - Each row in the input matrix represents an isolate
    - The pattern is a tuple of column names where the value is 1
    - Patterns are sorted alphabetically for consistency
    - Empty patterns return as ("No_Genes",) for clarity

    Parameters:
        mdr_gene_df (pd.DataFrame): Binary matrix of gene presence in MDR isolates

    Returns:
        pd.Series: Series with tuples of gene patterns for each isolate
    """

    def row_pat(row):
        items = [col for col, val in row.items() if val == 1]
        return tuple(sorted(items)) if items else ("No_Genes",)

    return mdr_gene_df.apply(row_pat, axis=1)


def bootstrap_pattern_freq(
    patterns: pd.Series, n_iter: int = 5000, conf_level: float = 0.95
) -> pd.DataFrame:
    """
    Calculate frequencies and bootstrap confidence intervals for resistance patterns.

    Statistical method:
    - Non-parametric bootstrap resampling to estimate pattern frequency distribution
    - Percentile method for confidence interval calculation

    Mathematical details:
    - Let P be the set of unique patterns
    - For each pattern p in P:
      1. Count original frequency f_p = count(p)/total
      2. For bootstrap iterations i=1 to n_iter:
         a. Draw a sample S_i of size n with replacement
         b. Compute bootstrap frequency f_p,i = count(p in S_i)/n
      3. CI bounds for pattern p:
         - Lower: (alpha/2) percentile of {f_p,1, f_p,2, ..., f_p,n_iter}
         - Upper: (1-alpha/2) percentile of {f_p,1, f_p,2, ..., f_p,n_iter}
         where alpha = 1-conf_level

    Parameters:
        patterns (pd.Series): Series of pattern tuples
        n_iter (int): Number of bootstrap iterations (default: 5000)
        conf_level (float): Confidence level (default: 0.95 for 95% CI)

    Returns:
        pd.DataFrame: Table with [Pattern, Count, Frequency(%), CI_Lower, CI_Upper]
    """
    from collections import Counter

    if patterns.empty:
        return pd.DataFrame(columns=["Pattern", "Count", "Frequency(%)", "CI_Lower", "CI_Upper"])
    counts = Counter(patterns)
    total = len(patterns)
    df = pd.DataFrame({"Pattern": list(counts.keys()), "Count": list(counts.values())})
    df["Frequency(%)"] = (df["Count"] / total) * 100

    def single_boot():
        s = patterns.sample(total, replace=True)
        return Counter(s)

    alpha = 1.0 - conf_level
    store: Dict[str, List[float]] = {p: [] for p in counts}
    for _ in range(n_iter):
        c = single_boot()
        for pat in counts:
            store[pat].append((c.get(pat, 0) / total) * 100)

    df["CI_Lower"] = 0.0
    df["CI_Upper"] = 0.0
    for i, r in df.iterrows():
        pat = r["Pattern"]
        arr = np.array(store[pat])
        df.at[i, "CI_Lower"] = round(np.percentile(arr, alpha / 2 * 100), 3)
        df.at[i, "CI_Upper"] = round(np.percentile(arr, (1 - alpha / 2) * 100), 3)

    df["Frequency(%)"] = df["Frequency(%)"].round(3)
    df.sort_values("Count", ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df["Pattern"] = df["Pattern"].apply(lambda x: ", ".join(x))
    return df


###############################################################################
# 6) CO-OCCURRENCE
###############################################################################
def pairwise_cooccurrence(
    df: pd.DataFrame, alpha: float = 0.05, method: str = "fdr_bh"
) -> pd.DataFrame:
    """
    Calculate statistically significant co-occurrences between all column pairs.

    Statistical methods:
    - Contingency table analysis for each pair of binary variables
    - Multiple testing correction to control false discovery rate

    Mathematical details:
    - For each pair of columns (A, B):
      1. Construct 2×2 contingency table
      2. Calculate test statistic and p-value using safe_contingency()
      3. Calculate phi coefficient for effect size
    - After testing all pairs:
      1. Apply multiple testing correction using specified method
      2. Retain only statistically significant pairs (corrected p < alpha)

    Multiple testing correction methods:
    - 'fdr_bh': Benjamini-Hochberg procedure (controls false discovery rate)
      Algorithm:
      1. Sort p-values in ascending order: p_1 ≤ p_2 ≤ ... ≤ p_m
      2. Find largest k such that p_k ≤ (k/m)×alpha
      3. Reject null hypotheses for all p_i where i ≤ k

    Parameters:
        df (pd.DataFrame): Binary matrix (0/1 values)
        alpha (float): Significance threshold (default: 0.05)
        method (str): Multiple testing correction method (default: 'fdr_bh')

    Returns:
        pd.DataFrame: Table with [Item1, Item2, Phi, Raw_p, Corrected_p]
    """
    if df.shape[1] < 2:
        return pd.DataFrame(columns=["Item1", "Item2", "Phi", "Corrected_p", "Raw_p"])

    cols = df.columns
    recs = []
    pvals = []
    combos = []
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            c1, c2 = cols[i], cols[j]
            tbl = pd.crosstab(df[c1], df[c2])
            _, p_val, phi_val = safe_contingency(tbl)
            if not np.isnan(p_val):
                combos.append((c1, c2, phi_val))
                pvals.append(p_val)

    if not pvals:
        return pd.DataFrame(columns=["Item1", "Item2", "Phi", "Corrected_p", "Raw_p"])

    reject, corr, _, _ = multipletests(pvals, alpha=alpha, method=method)
    for (it1, it2, phi), rp, cp, r in zip(combos, pvals, corr, reject):
        if r:
            recs.append(
                {
                    "Item1": it1,
                    "Item2": it2,
                    "Phi": round(phi, 3),
                    "Raw_p": round(rp, 3),
                    "Corrected_p": round(cp, 3),
                }
            )
    out = pd.DataFrame(recs)
    out.sort_values("Corrected_p", inplace=True)
    out.reset_index(drop=True, inplace=True)
    return out


def phenotype_gene_cooccurrence(
    phen_df: pd.DataFrame, gene_df: pd.DataFrame, alpha: float = 0.05, method: str = "fdr_bh"
) -> pd.DataFrame:
    """
    Calculate statistically significant associations between phenotypes and genes.

    Statistical methods:
    - Contingency table analysis for each phenotype-gene pair
    - Multiple testing correction to control false discovery rate

    Mathematical details:
    - For each phenotype-gene pair (P, G):
      1. Construct 2×2 contingency table
      2. Calculate test statistic and p-value using safe_contingency()
      3. Calculate phi coefficient for effect size
    - After testing all pairs:
      1. Apply multiple testing correction using specified method
      2. Retain only statistically significant pairs (corrected p < alpha)

    Multiple testing correction methods:
    - 'fdr_bh': Benjamini-Hochberg procedure (controls false discovery rate)
      Algorithm:
      1. Sort p-values in ascending order: p_1 ≤ p_2 ≤ ... ≤ p_m
      2. Find largest k such that p_k ≤ (k/m)×alpha
      3. Reject null hypotheses for all p_i where i ≤ k

    Parameters:
        phen_df (pd.DataFrame): Binary matrix for phenotypic resistance
        gene_df (pd.DataFrame): Binary matrix for AMR gene presence
        alpha (float): Significance threshold (default: 0.05)
        method (str): Multiple testing correction method (default: 'fdr_bh')

    Returns:
        pd.DataFrame: Table with [Phenotype, Gene, Phi, Raw_p, Corrected_p]
    """
    if phen_df.empty or gene_df.empty:
        return pd.DataFrame(columns=["Phenotype", "Gene", "Phi", "Corrected_p", "Raw_p"])

    ph_cols = phen_df.columns
    g_cols = gene_df.columns
    recs = []
    pvals = []
    combos = []
    for ph in ph_cols:
        for gn in g_cols:
            tbl = pd.crosstab(phen_df[ph], gene_df[gn])
            _, p_val, phi_val = safe_contingency(tbl)
            if not np.isnan(p_val):
                combos.append((ph, gn, phi_val))
                pvals.append(p_val)

    if not pvals:
        return pd.DataFrame(columns=["Phenotype", "Gene", "Phi", "Corrected_p", "Raw_p"])

    reject, corr, _, _ = multipletests(pvals, alpha=alpha, method=method)
    for (p1, g1, phi), rp, cp, r in zip(combos, pvals, corr, reject):
        if r:
            recs.append(
                {
                    "Phenotype": p1,
                    "Gene": g1,
                    "Phi": round(phi, 3),
                    "Raw_p": round(rp, 3),
                    "Corrected_p": round(cp, 3),
                }
            )
    out = pd.DataFrame(recs)
    out.sort_values("Corrected_p", inplace=True)
    out.reset_index(drop=True, inplace=True)
    return out


###############################################################################
# 7) ASSOCIATION RULES
###############################################################################
def association_rules_phenotypic(
    class_res_df: pd.DataFrame, min_support: float = 0.1, lift_thresh: float = 1.0
) -> pd.DataFrame:
    """
    Discover association rules among phenotypic resistance classes.

    Statistical methods:
    - Apriori algorithm for frequent itemset mining
    - Association rule generation with support, confidence, and lift metrics

    Mathematical details:
    - Let D be the set of transactions (isolates)
    - For an itemset X (set of resistance classes):
      * Support(X) = |{d ∈ D | X ⊆ d}| / |D|
        (proportion of isolates containing all items in X)
    - For a rule X → Y:
      * Support(X → Y) = Support(X ∪ Y)
      * Confidence(X → Y) = Support(X ∪ Y) / Support(X)
        (conditional probability of Y given X)
      * Lift(X → Y) = Support(X ∪ Y) / (Support(X) × Support(Y))
        (ratio of observed co-occurrence to expected co-occurrence under independence)
        - Lift > 1: Positive association
        - Lift = 1: Independence
        - Lift < 1: Negative association

    Parameters:
        class_res_df (pd.DataFrame): Binary matrix for antibiotic class resistance
        min_support (float): Minimum support threshold (default: 0.1 = 10% of isolates)
        lift_thresh (float): Minimum lift threshold (default: 1.0)

    Returns:
        pd.DataFrame: Association rules with metrics (support, confidence, lift)
    """
    try:
        from mlxtend.frequent_patterns import apriori, association_rules

        if class_res_df.empty:
            return pd.DataFrame()

        bool_df = class_res_df.astype(bool)
        itemsets = apriori(bool_df, min_support=min_support, use_colnames=True)
        if itemsets.empty:
            return pd.DataFrame()
        rules = association_rules(itemsets, metric="lift", min_threshold=lift_thresh)
        if rules.empty:
            return pd.DataFrame()
        rules["antecedents"] = rules["antecedents"].apply(lambda x: ", ".join(list(x)))
        rules["consequents"] = rules["consequents"].apply(lambda x: ", ".join(list(x)))
        for c in ["support", "confidence", "lift", "leverage", "conviction"]:
            if c in rules.columns:
                rules[c] = rules[c].round(3)
        return rules.sort_values("lift", ascending=False).reset_index(drop=True)
    except ImportError:
        logging.warning("mlxtend not installed => skipping phenotypic association rules.")
        return pd.DataFrame()


def association_rules_genes(
    amr_df: pd.DataFrame, min_support: float = 0.1, lift_thresh: float = 1.0
) -> pd.DataFrame:
    """
    Discover association rules among AMR genes.

    Statistical methods:
    - Apriori algorithm for frequent itemset mining
    - Association rule generation with support, confidence, and lift metrics

    Mathematical details:
    - Let D be the set of transactions (isolates)
    - For an itemset X (set of AMR genes):
      * Support(X) = |{d ∈ D | X ⊆ d}| / |D|
        (proportion of isolates containing all genes in X)
    - For a rule X → Y:
      * Support(X → Y) = Support(X ∪ Y)
      * Confidence(X → Y) = Support(X ∪ Y) / Support(X)
        (conditional probability of Y given X)
      * Lift(X → Y) = Support(X ∪ Y) / (Support(X) × Support(Y))
        (ratio of observed co-occurrence to expected co-occurrence under independence)
        - Lift > 1: Positive association
        - Lift = 1: Independence
        - Lift < 1: Negative association

    Parameters:
        amr_df (pd.DataFrame): Binary matrix for AMR gene presence
        min_support (float): Minimum support threshold (default: 0.1 = 10% of isolates)
        lift_thresh (float): Minimum lift threshold (default: 1.0)

    Returns:
        pd.DataFrame: Association rules with metrics (support, confidence, lift)
    """
    try:
        from mlxtend.frequent_patterns import apriori, association_rules

        if amr_df.empty:
            return pd.DataFrame()

        bool_df = amr_df.astype(bool)
        itemsets = apriori(bool_df, min_support=min_support, use_colnames=True)
        if itemsets.empty:
            return pd.DataFrame()
        rules = association_rules(itemsets, metric="lift", min_threshold=lift_thresh)
        if rules.empty:
            return pd.DataFrame()
        rules["antecedents"] = rules["antecedents"].apply(lambda x: ", ".join(list(x)))
        rules["consequents"] = rules["consequents"].apply(lambda x: ", ".join(list(x)))
        for c in ["support", "confidence", "lift", "leverage", "conviction"]:
            if c in rules.columns:
                rules[c] = rules[c].round(3)
        return rules.sort_values("lift", ascending=False).reset_index(drop=True)
    except ImportError:
        logging.warning("mlxtend not installed => skipping gene association rules.")
        return pd.DataFrame()


###############################################################################
# 8) HYBRID NETWORK
###############################################################################
def build_hybrid_co_resistance_network(
    data: pd.DataFrame,
    pheno_cols: List[str],
    gene_cols: List[str],
    alpha: float = 0.05,
    method: str = "fdr_bh",
) -> nx.Graph:
    """
    Build an integrated network of phenotypic resistances and AMR genes.

    Network construction method:
    - Nodes represent either antibiotic classes or AMR genes
    - Edges represent statistically significant associations
    - Three types of edges: phenotype-phenotype, gene-gene, phenotype-gene
    - Edge weights correspond to association strength (phi coefficient)
    - Only statistically significant associations (after correction) are included

    Mathematical details:
    - For all pairs of variables (phenotypes and genes):
      1. Construct 2×2 contingency table
      2. Calculate test statistic, p-value, and phi coefficient
    - Apply multiple testing correction to all p-values
    - Create edge if corrected p-value < alpha
    - Edge attributes include:
      * phi: Strength and direction of association (-1 to +1)
      * pvalue: Corrected p-value
      * edge_type: Relationship type (pheno-pheno, gene-gene, pheno-gene)

    Parameters:
        data (pd.DataFrame): Dataset with both phenotype and gene columns
        pheno_cols (List[str]): List of phenotypic resistance columns
        gene_cols (List[str]): List of AMR gene columns
        alpha (float): Significance threshold (default: 0.05)
        method (str): Multiple testing correction method (default: 'fdr_bh')

    Returns:
        nx.Graph: NetworkX graph with significant associations as edges
    """
    if not pheno_cols and not gene_cols:
        return nx.Graph()

    all_cols = pheno_cols + gene_cols
    combos = []

    # Calculate all pairwise associations
    for c1, c2 in combinations(all_cols, 2):
        tab = pd.crosstab(data[c1], data[c2])
        _, p_val, phi_val = safe_contingency(tab)
        if not np.isnan(p_val):
            combos.append((c1, c2, phi_val, p_val))

    if not combos:
        return nx.Graph()

    # Apply multiple testing correction
    raw_pvals = [c[3] for c in combos]
    reject, corrected, _, _ = multipletests(raw_pvals, alpha=alpha, method=method)

    # Initialize network
    G = nx.Graph()

    # Add nodes for all phenotypes and genes
    for p in pheno_cols:
        G.add_node(p, node_type="Phenotype")
    for g in gene_cols:
        G.add_node(g, node_type="Genotype")

    # Add significant edges (avoiding isolated nodes)
    for (c1, c2, phi, pv), c_p, is_sig in zip(combos, corrected, reject):
        if is_sig:
            # determine edge type
            if (c1 in pheno_cols) and (c2 in pheno_cols):
                e_type = "pheno-pheno"
            elif (c1 in gene_cols) and (c2 in gene_cols):
                e_type = "gene-gene"
            else:
                e_type = "pheno-gene"
            G.add_edge(c1, c2, phi=round(phi, 3), pvalue=round(c_p, 3), edge_type=e_type)

    # Remove isolated nodes
    G.remove_nodes_from(list(nx.isolates(G)))

    return G


def compute_louvain_communities(G: nx.Graph) -> pd.DataFrame:
    """
    Identify communities in the hybrid network using the Louvain algorithm.

    Statistical method:
    - Louvain algorithm for community detection in networks
    - Based on modularity optimization

    Mathematical details:
    - Modularity (Q): Measures the density of links inside communities
      compared to links between communities
    - Q = (1/2m)∑[A_ij - k_i*k_j/(2m)]δ(c_i,c_j)
      where:
      * m is the total number of edges
      * A_ij is the adjacency matrix
      * k_i, k_j are degrees of nodes i and j
      * c_i, c_j are communities of nodes i and j
      * δ is the Kronecker delta (1 if c_i=c_j, 0 otherwise)

    Louvain algorithm steps:
    1. Initialize each node as its own community
    2. Iterative process:
       a. For each node, evaluate gain in modularity by moving to neighbor communities
       b. Move node to community with highest gain (if positive)
       c. Repeat until no improvement in modularity
    3. Aggregate nodes in same community and build new network
    4. Repeat steps 2-3 until no further improvements

    Parameters:
        G (nx.Graph): NetworkX graph of the hybrid network

    Returns:
        pd.DataFrame: Table with [Node, Community] mapping
    """
    if G.number_of_nodes() == 0:
        return pd.DataFrame(columns=["Node", "Community"])

    try:
        from networkx.algorithms import community

        cset = list(community.louvain_communities(G, weight="phi"))
        recs = []
        for i, comm in enumerate(cset, 1):
            for nd in comm:
                recs.append({"Node": nd, "Community": i})
        df = pd.DataFrame(recs).sort_values(["Community", "Node"])
        df.reset_index(drop=True, inplace=True)
        return df
    except ImportError:
        logging.warning("networkx-louvain not installed => skipping communities.")
        return pd.DataFrame(columns=["Node", "Community"])
    except Exception as e:
        logging.warning(f"Louvain error: {e}")
        return pd.DataFrame(columns=["Node", "Community"])


def create_hybrid_network_figure(G: nx.Graph) -> Tuple[str, Any]:
    """
    Create an interactive visualization of the hybrid network.

    Visualization details:
    - Force-directed layout algorithm (Fruchterman-Reingold variant)
    - Node color based on type: phenotype (red), gene (blue)
    - Node size proportional to connectivity (degree)
    - Edge color based on type:
      * phenotype-phenotype: red
      * gene-gene: blue
      * phenotype-gene: purple
    - Interactive features:
      * Hover information for nodes and edges
      * Zoom and pan capabilities
      * Download options (PNG, SVG, CSV)

    Layout algorithm:
    - Modified spring layout based on node-node repulsion
      and edge-based attraction
    - Position optimization using 50 iterations
    - Fixed random seed (42) for reproducibility

    Parameters:
        G (nx.Graph): NetworkX graph of the hybrid network

    Returns:
        tuple: (HTML string for interactive Plotly figure, Figure object)
    """
    import plotly.graph_objs as go

    if G.number_of_nodes() == 0:
        return "<p>No hybrid network to display.</p>", None

    # Use a force-directed layout algorithm for better node positioning
    pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)

    # Separate edge collections by type
    edge_x_pheno_pheno, edge_y_pheno_pheno, edge_text_pheno_pheno = [], [], []
    edge_x_gene_gene, edge_y_gene_gene, edge_text_gene_gene = [], [], []
    edge_x_pheno_gene, edge_y_pheno_gene, edge_text_pheno_gene = [], [], []

    # Process edges by type
    for u, v, d in G.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_type = d.get("edge_type", "unknown")

        phi = d.get("phi", 0)
        pval = d.get("pvalue", np.nan)
        st = add_significance_stars(pval)

        # Detailed edge information
        label = f"<b>{u}–{v}</b><br>Type: {edge_type}<br>Phi: {phi:.3f}<br>p-value: {pval:.3f}{st}"

        # Add to appropriate list based on edge type
        if edge_type == "pheno-pheno":
            edge_x_pheno_pheno.extend([x0, x1, None])
            edge_y_pheno_pheno.extend([y0, y1, None])
            edge_text_pheno_pheno.extend([label, label, None])
        elif edge_type == "gene-gene":
            edge_x_gene_gene.extend([x0, x1, None])
            edge_y_gene_gene.extend([y0, y1, None])
            edge_text_gene_gene.extend([label, label, None])
        else:  # pheno-gene or unknown
            edge_x_pheno_gene.extend([x0, x1, None])
            edge_y_pheno_gene.extend([y0, y1, None])
            edge_text_pheno_gene.extend([label, label, None])

    # Create separate trace for each edge type
    traces = []

    if edge_x_pheno_pheno:
        traces.append(
            go.Scatter(
                x=edge_x_pheno_pheno,
                y=edge_y_pheno_pheno,
                mode="lines",
                line=dict(width=2, color="rgba(255,0,0,0.5)"),
                hoverinfo="text",
                text=edge_text_pheno_pheno,
                name="pheno-pheno",
            )
        )

    if edge_x_gene_gene:
        traces.append(
            go.Scatter(
                x=edge_x_gene_gene,
                y=edge_y_gene_gene,
                mode="lines",
                line=dict(width=2, color="rgba(0,0,255,0.5)"),
                hoverinfo="text",
                text=edge_text_gene_gene,
                name="gene-gene",
            )
        )

    if edge_x_pheno_gene:
        traces.append(
            go.Scatter(
                x=edge_x_pheno_gene,
                y=edge_y_pheno_gene,
                mode="lines",
                line=dict(width=2, color="rgba(128,0,128,0.5)"),
                hoverinfo="text",
                text=edge_text_pheno_gene,
                name="pheno-gene",
            )
        )

    # Node trace
    node_x, node_y = [], []
    node_text = []
    hover_text = []
    marker_color = []
    marker_size = []

    # Process all nodes
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        # Node type determines color
        ntype = G.nodes[node].get("node_type", "Unknown")
        color = "red" if ntype == "Phenotype" else "blue"
        marker_color.append(color)

        # Node size based on degree
        deg = nx.degree(G, node)
        size_val = 15 + 3 * deg
        marker_size.append(size_val)

        # Node label
        node_text.append(str(node))

        # Detailed hover information
        connections = [f"• {n}" for n in nx.neighbors(G, node)]
        connections_text = "<br>".join(connections) if connections else "None"

        hover_info = f"<b>{node}</b><br>Type: {ntype}<br>Degree: {deg}<br><b>Connections:</b><br>{connections_text}"
        hover_text.append(hover_info)

    # Add node trace
    traces.append(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=node_text,
            textposition="top center",
            hoverinfo="text",
            hovertext=hover_text,
            marker=dict(size=marker_size, color=marker_color, line=dict(width=1, color="#333")),
            name="Nodes",
        )
    )

    # Create figure with all traces
    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            title=dict(text="Hybrid Co-resistance Network", font=dict(size=18)),
            showlegend=True,
            hovermode="closest",
            width=1000,
            height=800,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(x=1, y=0.5),
            updatemenus=[
                dict(
                    type="buttons",
                    direction="left",
                    buttons=[
                        dict(
                            args=[{"width": 1000, "height": 800}], label="Reset", method="relayout"
                        ),
                        dict(
                            args=[{"width": 1500, "height": 1200}],
                            label="Enlarge",
                            method="relayout",
                        ),
                    ],
                    pad={"r": 10, "t": 10},
                    showactive=False,
                    x=0.1,
                    xanchor="left",
                    y=1.1,
                    yanchor="top",
                )
            ],
        ),
    )

    # Add download options
    config = {
        "toImageButtonOptions": {
            "format": "png",
            "filename": "hybrid_network",
            "height": 800,
            "width": 1000,
            "scale": 2,
        },
        "modeBarButtonsToAdd": ["downloadSVG", "downloadCSV"],
    }

    return fig.to_html(full_html=False, include_plotlyjs="cdn", config=config), fig


###############################################################################
# 9) REPORT + MAIN
###############################################################################
def df_to_html(df: pd.DataFrame, caption: str) -> str:
    """
    Convert DataFrame to enhanced HTML table with interactive features.

    Presentation details:
    - Integrates DataTables jQuery plugin for enhanced functionality
    - Adds interactive features: search, sort, pagination
    - Includes data export options (copy, CSV, Excel, PDF)
    - Creates unique ID for each table to allow multiple tables on page
    - Handles empty dataframes with informative message

    Parameters:
        df (pd.DataFrame): Data to be displayed in the table
        caption (str): Table title/caption

    Returns:
        str: HTML code for interactive DataTables display
    """
    if df.empty:
        return f"<h4>{caption}</h4><p>No data available.</p>"

    # Generate unique ID for this table
    import hashlib

    table_id = f"table_{hashlib.md5(caption.encode(), usedforsecurity=False).hexdigest()[:8]}"

    # Round all float columns to 3 decimal places
    for col in df.columns:
        if df[col].dtype == "float64" or df[col].dtype == "float32":
            df[col] = df[col].round(3)

    # Convert DataFrame to HTML table with unique ID
    html_table = df.to_html(index=False, table_id=table_id, classes="display nowrap compact")

    # Add DataTables initialization script
    script = f"""
    <script>
        $(document).ready(function() {{
            $('#{table_id}').DataTable({{
                pageLength: 20,
                lengthMenu: [[10, 20, 50, 100, -1], [10, 20, 50, 100, "All"]],
                dom: 'Blfrtip',
                buttons: [
                    'copy', 'csv', 'excel', 'pdf'
                ]
            }});
        }});
    </script>
    """

    return f"<h4>{caption}</h4>\n<div class='table-responsive'>{html_table}</div>\n{script}"


def generate_html_report(
    data: pd.DataFrame,
    class_res_all: pd.DataFrame,
    class_res_mdr: pd.DataFrame,
    amr_all: pd.DataFrame,
    amr_mdr: pd.DataFrame,
    freq_pheno_all: pd.DataFrame,
    freq_pheno_mdr: pd.DataFrame,
    freq_gene_all: pd.DataFrame,
    freq_gene_mdr: pd.DataFrame,
    pat_pheno_mdr: pd.DataFrame,
    pat_gene_mdr: pd.DataFrame,
    coocc_pheno_mdr: pd.DataFrame,
    coocc_gene_mdr: pd.DataFrame,
    gene_pheno_assoc: pd.DataFrame,
    assoc_rules_pheno: pd.DataFrame,
    assoc_rules_genes: pd.DataFrame,
    hybrid_net: nx.Graph,
    edges_df: pd.DataFrame,
    comm_df: pd.DataFrame,
    net_html: str,
) -> str:
    """
    Generate comprehensive HTML report with all analysis results.

    Report structure:
    - Header with timestamp and dataset overview
    - Separate sections for each analysis type
    - Interactive tables and visualizations
    - Detailed statistical methodology descriptions
    - Downloads and export functionality

    Technical details:
    - HTML5 compliant structure with responsive design
    - CSS styling for readability and visual consistency
    - jQuery and DataTables for client-side interactivity
    - Plotly for network visualization

    Parameters:
        data: Original dataset
        class_res_all: Class resistance matrix (all isolates)
        class_res_mdr: Class resistance matrix (MDR isolates only)
        amr_all: AMR gene presence matrix (all isolates)
        amr_mdr: AMR gene presence matrix (MDR isolates only)
        freq_pheno_all: Phenotypic resistance frequencies (all isolates)
        freq_pheno_mdr: Phenotypic resistance frequencies (MDR isolates)
        freq_gene_all: AMR gene frequencies (all isolates)
        freq_gene_mdr: AMR gene frequencies (MDR isolates)
        pat_pheno_mdr: Phenotypic resistance patterns (MDR isolates)
        pat_gene_mdr: AMR gene patterns (MDR isolates)
        coocc_pheno_mdr: Co-occurrence among antibiotic classes
        coocc_gene_mdr: Co-occurrence among AMR genes
        gene_pheno_assoc: Phenotype-gene associations
        assoc_rules_pheno: Association rules for phenotypes
        assoc_rules_genes: Association rules for genes
        hybrid_net: Hybrid network graph
        edges_df: Significant edges in the network
        comm_df: Communities identified in the network
        net_html: Interactive network visualization HTML

    Returns:
        str: Complete HTML report with all visualizations and tables
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>StrepSuis-AMRPat: Automated Detection of Antimicrobial Resistance Patterns in Streptococcus suis</title>
  <!-- jQuery -->
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

  <!-- DataTables CSS -->
  <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.1/css/jquery.dataTables.min.css">
  <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/buttons/2.3.2/css/buttons.dataTables.min.css">

  <!-- DataTables JS -->
  <script type="text/javascript" src="https://cdn.datatables.net/1.13.1/js/jquery.dataTables.min.js"></script>
  <script type="text/javascript" src="https://cdn.datatables.net/buttons/2.3.2/js/dataTables.buttons.min.js"></script>
  <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.1.3/jszip.min.js"></script>
  <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/pdfmake.min.js"></script>
  <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/vfs_fonts.js"></script>
  <script type="text/javascript" src="https://cdn.datatables.net/buttons/2.3.2/js/buttons.html5.min.js"></script>
  <script type="text/javascript" src="https://cdn.datatables.net/buttons/2.3.2/js/buttons.print.min.js"></script>

  <style>
    body {{
      font-family: Arial, sans-serif;
      margin:20px;
      background-color:#f9f9f9;
    }}
    .container {{
      background-color:#fff;
      padding:30px;
      border-radius:6px;
      max-width:1200px;
      margin:0 auto;
    }}
    h1,h2,h3,h4 {{
      color:#333;
    }}
    table {{
      border-collapse:collapse;
      width:100%;
      margin-bottom:20px;
    }}
    table,th,td {{
      border:1px solid #ccc;
    }}
    th,td {{
      padding:8px;
      text-align:left;
      font-size:0.9em;
    }}
    th {{
      background-color:#fafafa;
    }}
    .footer {{
      text-align:center;
      margin-top:40px;
      font-size:0.85em;
      color:#666;
      border-top:1px solid #ccc;
      padding-top:10px;
    }}
    .section {{
      margin-bottom:40px;
    }}
    .network-container {{
      border:1px solid #ccc;
      padding:10px;
      margin-bottom:20px;
      overflow-x:auto;
    }}
    .table-responsive {{
      overflow-x: auto;
      margin-bottom: 20px;
    }}
    .dataTables_wrapper {{
      padding: 10px 0;
    }}
    .dt-buttons {{
      margin-bottom: 15px;
    }}
    .methodology {{
      background-color: #f8f9fa;
      border-left: 4px solid #6c757d;
      padding: 10px 15px;
      margin-bottom: 20px;
      font-size: 0.9em;
    }}
    .methodology h4 {{
      margin-top: 0;
      color: #495057;
    }}
    .methodology ul {{
      padding-left: 20px;
    }}
  </style>
</head>
<body>
<div class="container">
<h1>StrepSuis-AMRPat: Automated Detection of Antimicrobial Resistance Patterns in Streptococcus suis</h1>
<p><strong>Timestamp:</strong> {ts}</p>
<p><strong>Total isolates:</strong> {len(data)}</p>
<hr/>

<div class="section">
  <h2>1) Phenotypic Resistance Frequencies (All Isolates)</h2>
  
  <div class="methodology">
    <h4>Statistical Methodology</h4>
    <p>These frequencies were calculated using non-parametric bootstrap resampling with the following parameters:</p>
    <ul>
      <li><strong>Bootstrap iterations:</strong> 5,000</li>
      <li><strong>Confidence level:</strong> 95%</li>
      <li><strong>Method:</strong> Percentile bootstrap CI (empirical distribution)</li>
    </ul>
    <p>The bootstrap approach makes no assumptions about the underlying distribution and is robust for prevalence estimation.
    Confidence intervals are calculated directly from the resampled distribution using quantiles corresponding to the
    (α/2) and (1-α/2) percentiles, where α = 0.05 for 95% confidence.</p>
  </div>
  
  {df_to_html(freq_pheno_all,"All isolates (bootstrap 95% CI)")}
</div>

<div class="section">
  <h2>2) Phenotypic Resistance Frequencies (MDR Subset)</h2>
  
  <div class="methodology">
    <h4>Statistical Methodology</h4>
    <p>Frequencies in the MDR subset follow the same bootstrap methodology as the full dataset, with identical parameters:</p>
    <ul>
      <li><strong>Bootstrap iterations:</strong> 5,000</li>
      <li><strong>Confidence level:</strong> 95%</li>
      <li><strong>MDR definition:</strong> Resistance to ≥3 antibiotic classes</li>
    </ul>
    <p>This analysis focuses only on isolates meeting the MDR criteria (resistance to three or more antibiotic classes),
    allowing comparison of resistance patterns between the general population and the MDR subset.</p>
  </div>
  
  {df_to_html(freq_pheno_mdr,"MDR subset (bootstrap 95% CI)")}
</div>

<div class="section">
  <h2>3) AMR Gene Frequencies (All Isolates)</h2>
  
  <div class="methodology">
    <h4>Statistical Methodology</h4>
    <p>AMR gene frequencies were calculated using the same bootstrap approach as phenotypic resistances:</p>
    <ul>
      <li><strong>Bootstrap iterations:</strong> 5,000</li>
      <li><strong>Confidence level:</strong> 95%</li>
      <li><strong>Data type:</strong> Binary gene presence (1) or absence (0)</li>
    </ul>
    <p>All gene data was standardized to binary format before analysis, with any non-zero, 
    non-empty value considered as gene presence (1) and zero or empty values as absence (0).</p>
  </div>
  
  {df_to_html(freq_gene_all,"All isolates (AMR genes)")}
</div>

<div class="section">
  <h2>4) AMR Gene Frequencies (MDR Subset)</h2>
  
  <div class="methodology">
    <h4>Statistical Methodology</h4>
    <p>Gene frequencies in the MDR subset follow the same bootstrap methodology, focusing on isolates meeting MDR criteria:</p>
    <ul>
      <li><strong>Bootstrap iterations:</strong> 5,000</li>
      <li><strong>Confidence level:</strong> 95%</li>
      <li><strong>MDR definition:</strong> Resistance to ≥3 antibiotic classes</li>
    </ul>
    <p>This analysis helps identify genes potentially associated with multidrug resistance phenotypes
    by comparing their prevalence in MDR versus non-MDR isolates.</p>
  </div>
  
  {df_to_html(freq_gene_mdr,"MDR subset (AMR genes)")}
</div>

<div class="section">
  <h2>5) Phenotypic Patterns in MDR</h2>
  
  <div class="methodology">
    <h4>Statistical Methodology</h4>
    <p>This analysis identifies and quantifies unique combinations of resistance phenotypes:</p>
    <ul>
      <li><strong>Pattern identification:</strong> Each isolate's resistance profile is converted to a sorted tuple of resistance classes</li>
      <li><strong>Bootstrap iterations:</strong> 5,000</li>
      <li><strong>Confidence level:</strong> 95%</li>
    </ul>
    <p>The bootstrapping procedure estimates the frequency distribution of each pattern in the population. Patterns are sorted by descending frequency, highlighting the most common resistance combinations.</p>
  </div>
  
  {df_to_html(pat_pheno_mdr,"Phenotypic MDR patterns (bootstrap)")}
</div>

<div class="section">
  <h2>6) AMR Gene Patterns in MDR</h2>
  
  <div class="methodology">
    <h4>Statistical Methodology</h4>
    <p>Similar to phenotypic patterns, this analysis identifies unique combinations of AMR genes:</p>
    <ul>
      <li><strong>Pattern identification:</strong> Each isolate's gene profile is converted to a sorted tuple of present genes</li>
      <li><strong>Bootstrap iterations:</strong> 5,000</li>
      <li><strong>Confidence level:</strong> 95%</li>
    </ul>
    <p>The prevalence of specific gene combinations may indicate horizontal gene transfer, mobile genetic elements,
    or co-selection mechanisms. Patterns are sorted by descending frequency.</p>
  </div>
  
  {df_to_html(pat_gene_mdr,"Gene MDR patterns (bootstrap)")}
</div>

<div class="section">
  <h2>7) Co-occurrence Among Antibiotic Classes in MDR</h2>
  
  <div class="methodology">
    <h4>Statistical Methodology</h4>
    <p>This analysis identifies statistically significant associations between pairs of resistance phenotypes:</p>
    <ul>
      <li><strong>Association measure:</strong> Phi coefficient (φ), range from -1 to +1</li>
      <li><strong>Statistical test:</strong> Chi-square or Fisher's exact test (when expected counts <5)</li>
      <li><strong>Multiple testing correction:</strong> Benjamini-Hochberg FDR procedure (α=0.05)</li>
      <li><strong>Result filtering:</strong> Only statistically significant associations after correction are shown</li>
    </ul>
    <p>The phi coefficient indicates the strength and direction of association:
       φ>0 indicates positive association (co-occurrence),
       φ<0 indicates negative association (mutual exclusivity).</p>
  </div>
  
  {df_to_html(coocc_pheno_mdr,"Significant class–class co-occurrences")}
</div>

<div class="section">
  <h2>8) Co-occurrence Among AMR Genes in MDR</h2>
  
  <div class="methodology">
    <h4>Statistical Methodology</h4>
    <p>This analysis uses the same methodology as phenotypic co-occurrence to identify gene-gene associations:</p>
    <ul>
      <li><strong>Association measure:</strong> Phi coefficient (φ), range from -1 to +1</li>
      <li><strong>Statistical test:</strong> Chi-square or Fisher's exact test (when expected counts <5)</li>
      <li><strong>Multiple testing correction:</strong> Benjamini-Hochberg FDR procedure (α=0.05)</li>
      <li><strong>Result filtering:</strong> Only statistically significant associations after correction are shown</li>
    </ul>
    <p>Strong positive associations between genes may indicate co-location on the same genetic element (e.g., plasmid, transposon)
    or co-selection under similar antibiotic pressure.</p>
  </div>
  
  {df_to_html(coocc_gene_mdr,"Significant gene–gene co-occurrences")}
</div>

<div class="section">
  <h2>9) Gene–Phenotypic Associations (Entire Dataset)</h2>
  
  <div class="methodology">
    <h4>Statistical Methodology</h4>
    <p>This cross-dataset analysis identifies associations between AMR genes and resistance phenotypes:</p>
    <ul>
      <li><strong>Association measure:</strong> Phi coefficient (φ), range from -1 to +1</li>
      <li><strong>Statistical test:</strong> Chi-square or Fisher's exact test (when expected counts <5)</li>
      <li><strong>Multiple testing correction:</strong> Benjamini-Hochberg FDR procedure (α=0.05)</li>
      <li><strong>Result filtering:</strong> Only statistically significant associations after correction are shown</li>
    </ul>
    <p>These associations suggest potential gene-phenotype relationships, which may indicate genetic determinants of 
    specific resistance phenotypes. Strong positive associations may indicate causality or co-selection.</p>
  </div>
  
  {df_to_html(gene_pheno_assoc,"Significant gene–class associations")}
</div>

<div class="section">
  <h2>10) Phenotypic Association Rules</h2>
  
  <div class="methodology">
    <h4>Statistical Methodology</h4>
    <p>Association rule mining identifies frequent if-then relationships between phenotypic resistances:</p>
    <ul>
      <li><strong>Algorithm:</strong> Apriori for frequent itemset generation</li>
      <li><strong>Minimum support:</strong> 0.1 (10% of isolates)</li>
      <li><strong>Metrics:</strong>
        <ul>
          <li>Support: Proportion of isolates exhibiting both antecedent and consequent</li>
          <li>Confidence: Conditional probability of consequent given antecedent</li>
          <li>Lift: Ratio of observed support to expected support under independence</li>
        </ul>
      </li>
      <li><strong>Filtering:</strong> Only rules with lift ≥ 1.0 are included</li>
    </ul>
    <p>Rules are sorted by lift (measure of association strength). Lift > 1 indicates positive association,
    with higher values suggesting stronger relationships beyond what would be expected by chance.</p>
  </div>
  
  {df_to_html(assoc_rules_pheno,"Association Rules (Phenotypes)")}
</div>

<div class="section">
  <h2>11) AMR Gene Association Rules</h2>
  
  <div class="methodology">
    <h4>Statistical Methodology</h4>
    <p>This analysis applies the same association rule mining approach to AMR genes:</p>
    <ul>
      <li><strong>Algorithm:</strong> Apriori for frequent itemset generation</li>
      <li><strong>Minimum support:</strong> 0.1 (10% of isolates)</li>
      <li><strong>Metrics:</strong>
        <ul>
          <li>Support: Proportion of isolates carrying both gene sets</li>
          <li>Confidence: Conditional probability of consequent genes given antecedent genes</li>
          <li>Lift: Ratio of observed support to expected support under independence</li>
        </ul>
      </li>
      <li><strong>Filtering:</strong> Only rules with lift ≥ 1.0 are included</li>
    </ul>
    <p>High-confidence, high-lift rules may suggest genetic linkage, co-selection mechanisms,
    or consistent horizontal gene transfer patterns between isolates.</p>
  </div>
  
  {df_to_html(assoc_rules_genes,"Association Rules (Genes)")}
</div>

<!-- 12) HYBRID NETWORK -->
<div class="section">
<h2>12) Hybrid Co-resistance Network (Pheno–Pheno, Gene–Gene, Pheno–Gene)</h2>

<div class="methodology">
  <h4>Statistical Methodology</h4>
  <p>The hybrid network integrates all significant associations into a comprehensive visualization:</p>
  <ul>
    <li><strong>Nodes:</strong> Represent phenotypic resistances and AMR genes</li>
    <li><strong>Edges:</strong> Represent statistically significant associations
      <ul>
        <li>pheno-pheno: Associations between resistance phenotypes</li>
        <li>gene-gene: Associations between AMR genes</li>
        <li>pheno-gene: Associations between phenotypes and genes</li>
      </ul>
    </li>
    <li><strong>Association criteria:</strong>
      <ul>
        <li>Statistical test: Chi-square or Fisher's exact test</li>
        <li>Multiple testing correction: Benjamini-Hochberg FDR</li>
        <li>Significance threshold: α=0.05 after correction</li>
      </ul>
    </li>
    <li><strong>Edge weights:</strong> Proportional to phi coefficient strength</li>
    <li><strong>Layout algorithm:</strong> Force-directed spring layout</li>
  </ul>
  <p>The network visualization offers an integrated view of resistance relationships,
  providing insights into potential resistance mechanisms and gene-phenotype connections.</p>
</div>

<h3>12a) Interactive Figure</h3>
<div class="network-container">
  {net_html}
</div>

<h3>12b) Significant Edges</h3>
<div class="methodology">
  <h4>Edge Details</h4>
  <p>This table provides detailed information about all statistically significant associations in the network:</p>
  <ul>
    <li><strong>Node1, Node2:</strong> The connected phenotypes or genes</li>
    <li><strong>Edge_Type:</strong> Type of connection (pheno-pheno, gene-gene, pheno-gene)</li>
    <li><strong>Phi:</strong> Association strength and direction (-1 to +1)</li>
    <li><strong>p-value:</strong> FDR-corrected statistical significance</li>
    <li><strong>Significance:</strong> p-value with stars indicating significance level</li>
  </ul>
  <p>All edges shown are statistically significant after multiple testing correction (FDR-adjusted p < 0.05).</p>
</div>

{df_to_html(edges_df,"Significant Edges (All Types)")}

<h3>12c) Network Communities (Louvain)</h3>
<div class="methodology">
  <h4>Community Detection Methodology</h4>
  <p>The Louvain algorithm was used to detect communities in the network:</p>
  <ul>
    <li><strong>Algorithm:</strong> Louvain community detection (modularity optimization)</li>
    <li><strong>Modularity objective:</strong> Maximize within-community connections relative to between-community connections</li>
    <li><strong>Edge weights:</strong> Phi coefficient values used as weights</li>
    <li><strong>Community numbering:</strong> Sequential (1, 2, 3, etc.)</li>
  </ul>
  <p>Communities represent groups of genes and phenotypes that are more densely connected with each other than with
  the rest of the network, potentially indicating functional modules or co-selection units.</p>
</div>

{df_to_html(comm_df,"Network Communities")}
</div>

<div class="footer">
  <p>© Hybrid MDR Pipeline with enhanced statistical analysis and visualization.</p>
</div>
</div>

</body>
</html>
"""
    return html


def generate_excel_report(
    data: pd.DataFrame,
    class_res_all: pd.DataFrame,
    class_res_mdr: pd.DataFrame,
    amr_all: pd.DataFrame,
    amr_mdr: pd.DataFrame,
    freq_pheno_all: pd.DataFrame,
    freq_pheno_mdr: pd.DataFrame,
    freq_gene_all: pd.DataFrame,
    freq_gene_mdr: pd.DataFrame,
    pat_pheno_mdr: pd.DataFrame,
    pat_gene_mdr: pd.DataFrame,
    coocc_pheno_mdr: pd.DataFrame,
    coocc_gene_mdr: pd.DataFrame,
    gene_pheno_assoc: pd.DataFrame,
    assoc_rules_pheno: pd.DataFrame,
    assoc_rules_genes: pd.DataFrame,
    hybrid_net: nx.Graph,
    edges_df: pd.DataFrame,
    comm_df: pd.DataFrame,
    fig_network=None,
) -> str:
    """
    Generate comprehensive Excel report with all analysis results and PNG charts.

    This function creates a detailed Excel workbook with multiple sheets containing:
    - Dataset overview and metadata
    - Methodology descriptions
    - Frequency analyses with bootstrap confidence intervals
    - Pattern identification results
    - Co-occurrence matrices
    - Association rules
    - Network analysis results
    - Community detection outcomes

    All network visualizations are saved as PNG files.

    Parameters:
        data: Original dataset
        class_res_all: Class resistance matrix (all isolates)
        class_res_mdr: Class resistance matrix (MDR isolates only)
        amr_all: AMR gene presence matrix (all isolates)
        amr_mdr: AMR gene presence matrix (MDR isolates only)
        freq_pheno_all: Phenotypic resistance frequencies (all isolates)
        freq_pheno_mdr: Phenotypic resistance frequencies (MDR isolates)
        freq_gene_all: AMR gene frequencies (all isolates)
        freq_gene_mdr: AMR gene frequencies (MDR isolates)
        pat_pheno_mdr: Phenotypic resistance patterns (MDR isolates)
        pat_gene_mdr: AMR gene patterns (MDR isolates)
        coocc_pheno_mdr: Co-occurrence among antibiotic classes
        coocc_gene_mdr: Co-occurrence among AMR genes
        gene_pheno_assoc: Phenotype-gene associations
        assoc_rules_pheno: Association rules for phenotypes
        assoc_rules_genes: Association rules for genes
        hybrid_net: Hybrid network graph
        edges_df: Significant edges in the network
        comm_df: Communities identified in the network
        fig_network: Plotly figure object for the network (optional)

    Returns:
        str: Path to generated Excel file
    """
    # Initialize Excel report generator
    excel_gen = ExcelReportGenerator(output_folder="output")

    # Save network visualization as PNG if available
    if fig_network is not None:
        try:
            excel_gen.save_plotly_figure_fallback(
                fig_network, "hybrid_network_visualization", width=1400, height=1000
            )
        except Exception as e:
            print(f"Could not save network visualization: {e}")

    # Prepare methodology description
    methodology = {
        "Bootstrap Resampling": (
            "5000 iterations with 95% confidence intervals for prevalence estimation. "
            "Non-parametric approach suitable for complex distributions."
        ),
        "Association Testing": (
            "Chi-square test for general associations, Fisher's exact test when expected cell counts <5. "
            "Phi coefficient measures association strength. "
            "Benjamini-Hochberg FDR correction for multiple hypothesis testing."
        ),
        "Pattern Analysis": (
            "Identification of phenotypic resistance patterns and AMR gene patterns in MDR isolates. "
            "Patterns are ranked by frequency with bootstrap confidence intervals."
        ),
        "Co-occurrence Analysis": (
            "Matrix-based analysis of feature co-occurrence using phi coefficient. "
            "Statistical significance assessed via chi-square or Fisher's exact test."
        ),
        "Association Rules": (
            "Mining of predictive rules using support and lift metrics. "
            "Identifies antecedent → consequent relationships with high confidence."
        ),
        "Hybrid Network Construction": (
            "Network combining phenotype-gene, phenotype-phenotype, and gene-gene edges. "
            "Edges represent significant associations (corrected p < 0.05). "
            "Louvain community detection identifies functional modules."
        ),
    }

    # Prepare sheets data
    sheets_data = {}

    # Dataset Overview
    overview_data = {
        "Metric": [
            "Total Isolates",
            "MDR Isolates",
            "MDR Percentage",
            "Phenotype Columns",
            "Gene Columns",
        ],
        "Value": [
            len(data),
            len(class_res_mdr) if class_res_mdr is not None else 0,
            (
                f"{(len(class_res_mdr) / len(data) * 100):.2f}%"
                if class_res_mdr is not None and len(data) > 0
                else "N/A"
            ),
            len([c for c in data.columns if "MIC_" in c or "Resistance_" in c]),
            len(
                [
                    c
                    for c in data.columns
                    if c not in ["Strain_ID"] and "MIC_" not in c and "Resistance_" not in c
                ]
            ),
        ],
    }
    sheets_data["Dataset_Overview"] = (
        pd.DataFrame(overview_data),
        "Summary statistics for the analyzed dataset",
    )

    # Frequency Analyses
    if freq_pheno_all is not None and not freq_pheno_all.empty:
        sheets_data["Freq_Pheno_All"] = (
            freq_pheno_all,
            "Phenotypic resistance frequencies in all isolates",
        )

    if freq_pheno_mdr is not None and not freq_pheno_mdr.empty:
        sheets_data["Freq_Pheno_MDR"] = (
            freq_pheno_mdr,
            "Phenotypic resistance frequencies in MDR isolates",
        )

    if freq_gene_all is not None and not freq_gene_all.empty:
        sheets_data["Freq_Gene_All"] = (freq_gene_all, "AMR gene frequencies in all isolates")

    if freq_gene_mdr is not None and not freq_gene_mdr.empty:
        sheets_data["Freq_Gene_MDR"] = (freq_gene_mdr, "AMR gene frequencies in MDR isolates")

    # Pattern Analyses
    if pat_pheno_mdr is not None and not pat_pheno_mdr.empty:
        sheets_data["Patterns_Pheno_MDR"] = (
            pat_pheno_mdr,
            "Phenotypic resistance patterns in MDR isolates",
        )

    if pat_gene_mdr is not None and not pat_gene_mdr.empty:
        sheets_data["Patterns_Gene_MDR"] = (pat_gene_mdr, "AMR gene patterns in MDR isolates")

    # Co-occurrence Analyses
    if coocc_pheno_mdr is not None and not coocc_pheno_mdr.empty:
        sheets_data["Coocc_Pheno_MDR"] = (
            coocc_pheno_mdr,
            "Co-occurrence among antibiotic classes in MDR",
        )

    if coocc_gene_mdr is not None and not coocc_gene_mdr.empty:
        sheets_data["Coocc_Gene_MDR"] = (coocc_gene_mdr, "Co-occurrence among AMR genes in MDR")

    # Association Analyses
    if gene_pheno_assoc is not None and not gene_pheno_assoc.empty:
        sheets_data["Gene_Pheno_Assoc"] = (
            gene_pheno_assoc,
            "Gene-Phenotype associations with statistical significance",
        )

    if assoc_rules_pheno is not None and not assoc_rules_pheno.empty:
        sheets_data["Assoc_Rules_Pheno"] = (
            assoc_rules_pheno,
            "Association rules for phenotypic resistances",
        )

    if assoc_rules_genes is not None and not assoc_rules_genes.empty:
        sheets_data["Assoc_Rules_Genes"] = (assoc_rules_genes, "Association rules for AMR genes")

    # Network Analyses
    if edges_df is not None and not edges_df.empty:
        sheets_data["Network_Edges"] = (
            edges_df,
            f"Significant edges in hybrid network (total: {len(edges_df)})",
        )

    if comm_df is not None and not comm_df.empty:
        sheets_data["Network_Communities"] = (
            comm_df,
            f"Louvain communities in network (total: {comm_df['Community'].nunique()} communities)",
        )

    # Network Statistics
    if hybrid_net is not None and hybrid_net.number_of_nodes() > 0:
        network_stats = {
            "Metric": [
                "Total Nodes",
                "Total Edges",
                "Phenotype Nodes",
                "Gene Nodes",
                "Average Degree",
                "Network Density",
                "Number of Communities",
            ],
            "Value": [
                hybrid_net.number_of_nodes(),
                hybrid_net.number_of_edges(),
                len(
                    [n for n, d in hybrid_net.nodes(data=True) if d.get("node_type") == "Phenotype"]
                ),
                len([n for n, d in hybrid_net.nodes(data=True) if d.get("node_type") == "Gene"]),
                (
                    f"{sum(dict(hybrid_net.degree()).values()) / hybrid_net.number_of_nodes():.2f}"
                    if hybrid_net.number_of_nodes() > 0
                    else 0
                ),
                f"{nx.density(hybrid_net):.4f}",
                comm_df["Community"].nunique() if comm_df is not None and not comm_df.empty else 0,
            ],
        }
        sheets_data["Network_Stats"] = (
            pd.DataFrame(network_stats),
            "Overall network statistics and topology metrics",
        )

    # Prepare metadata
    metadata = {
        "Total_Isolates": len(data),
        "MDR_Isolates": len(class_res_mdr) if class_res_mdr is not None else 0,
        "Network_Nodes": hybrid_net.number_of_nodes() if hybrid_net is not None else 0,
        "Network_Edges": hybrid_net.number_of_edges() if hybrid_net is not None else 0,
        "Bootstrap_Iterations": 5000,
        "FDR_Threshold": 0.05,
    }

    # Generate Excel report
    excel_path = excel_gen.generate_excel_report(
        report_name="MDR_Analysis_Hybrid_Report",
        sheets_data=sheets_data,
        methodology=methodology,
        **metadata,
    )

    return excel_path


def save_report(html_code: str, out_dir: str = "output") -> str:
    """
    Save the HTML report to a file with timestamp.

    File handling details:
    - Creates output directory if it doesn't exist
    - Uses Unix timestamp for unique filename
    - UTF-8 encoding for proper character handling
    - Logs the file path for reference

    Parameters:
        html_code (str): Complete HTML report content
        out_dir (str): Output directory path (default: "output")

    Returns:
        str: Path to the saved HTML file
    """
    os.makedirs(out_dir, exist_ok=True)
    ts = int(time.time())
    fname = f"mdr_analysis_hybrid_{ts}.html"
    path = os.path.join(out_dir, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_code)
    logging.info(f"Report saved => {path}")
    return path


###############################################################################
# MAIN
###############################################################################
def main():
    """
    Main function that orchestrates the entire analysis pipeline.

    Execution flow:
    1. Environment initialization and data loading
    2. Preprocessing and identification of phenotype/genotype columns
    3. MDR classification based on class resistance
    4. Frequency analysis with bootstrap confidence intervals
    5. Pattern identification and quantification
    6. Co-occurrence analysis for phenotypes and genes
    7. Association rule mining for predictive patterns
    8. Hybrid network construction and community detection
    9. Interactive visualization generation
    10. Comprehensive HTML report creation

    Statistical considerations:
    - Correction for multiple testing using Benjamini-Hochberg FDR
    - Bootstrap resampling for non-parametric confidence intervals
    - Appropriate statistical tests based on data characteristics
    - Modular analysis pipeline with clear parameter specifications
    """
    start_time = time.time()
    logging.info("Starting Hybrid MDR pipeline with enhanced statistical documentation...")

    csv_path = setup_environment()
    try:
        data = pd.read_csv(csv_path, sep=None, engine="python")
    except Exception as e:
        logging.error(f"Error reading CSV: {e}")
        return

    logging.info(f"Data loaded => shape={data.shape}")

    # Identify phenotype vs. genotype columns
    antibiotic_list = [d for arr in ANTIBIOTIC_CLASSES.values() for d in arr]
    phenotype_cols = [c for c in data.columns if c in antibiotic_list]
    skip_cols = {"id", "strain", "sample", "isolate", "date", "strain_id"}
    genotype_cols = [
        c for c in data.columns if c not in phenotype_cols and c.lower() not in skip_cols
    ]

    # 1) Build class-based resistance matrix and identify MDR isolates
    class_res_all = build_class_resistance(data, phenotype_cols)
    mdr_mask = identify_mdr_isolates(class_res_all, threshold=3)
    class_res_mdr = class_res_all[mdr_mask]

    # 2) Extract AMR gene data
    amr_all = extract_amr_genes(data, genotype_cols)
    amr_mdr = amr_all[mdr_mask]

    # 3) Calculate frequencies with bootstrap confidence intervals
    freq_pheno_all = compute_bootstrap_ci(class_res_all, 5000, 0.95)
    freq_pheno_mdr = compute_bootstrap_ci(class_res_mdr, 5000, 0.95)
    freq_gene_all = compute_bootstrap_ci(amr_all, 5000, 0.95)
    freq_gene_mdr = compute_bootstrap_ci(amr_mdr, 5000, 0.95)

    # 4) Analyze resistance patterns
    pheno_mdr_ser = get_mdr_patterns_pheno(class_res_mdr)
    pat_pheno_mdr = bootstrap_pattern_freq(pheno_mdr_ser, 5000, 0.95)

    gene_mdr_ser = get_mdr_patterns_geno(amr_mdr)
    pat_gene_mdr = bootstrap_pattern_freq(gene_mdr_ser, 5000, 0.95)

    # 5) Analyze co-occurrence among antibiotic classes in MDR isolates
    if class_res_mdr.shape[1] > 1:
        coocc_pheno_mdr = pairwise_cooccurrence(class_res_mdr)
    else:
        coocc_pheno_mdr = pd.DataFrame()

    # 6) Analyze co-occurrence among AMR genes in MDR isolates
    if amr_mdr.shape[1] > 1:
        coocc_gene_mdr = pairwise_cooccurrence(amr_mdr)
    else:
        coocc_gene_mdr = pd.DataFrame()

    # 7) Analyze phenotype-gene associations in the entire dataset
    gene_pheno_assoc = phenotype_gene_cooccurrence(class_res_all, amr_all)

    # 8) Apply association rule mining
    assoc_pheno = association_rules_phenotypic(class_res_all)
    assoc_genes = association_rules_genes(amr_all)

    # 9) Prepare data for hybrid network analysis
    df_hybrid = data[phenotype_cols + genotype_cols].copy()
    for c in df_hybrid.columns:
        df_hybrid[c] = df_hybrid[c].apply(lambda x: 1 if x != 0 else 0 if pd.notna(x) else 0)

    # 10) Build enhanced hybrid network
    hybrid_net = build_hybrid_co_resistance_network(
        df_hybrid, phenotype_cols, genotype_cols, alpha=0.05, method="fdr_bh"
    )

    # 11) Extract network edges for tabular display
    edges_list = []
    for u, v, d in hybrid_net.edges(data=True):
        pval = d.get("pvalue", np.nan)
        ety = d.get("edge_type", "unknown")
        edges_list.append(
            {
                "Node1": u,
                "Node2": v,
                "Edge_Type": ety,
                "Phi": round(d.get("phi", 0), 3),
                "p-value": round(pval, 3),
                "Significance": add_significance_stars(pval),
            }
        )
    edges_df = pd.DataFrame(edges_list).sort_values("p-value") if edges_list else pd.DataFrame()

    # 12) Detect network communities
    comm_df = compute_louvain_communities(hybrid_net)

    # 13) Generate interactive network visualization
    net_html, fig_network = create_hybrid_network_figure(hybrid_net)

    # 14) Generate comprehensive HTML report
    html_report = generate_html_report(
        data=data,
        class_res_all=class_res_all,
        class_res_mdr=class_res_mdr,
        amr_all=amr_all,
        amr_mdr=amr_mdr,
        freq_pheno_all=freq_pheno_all,
        freq_pheno_mdr=freq_pheno_mdr,
        freq_gene_all=freq_gene_all,
        freq_gene_mdr=freq_gene_mdr,
        pat_pheno_mdr=pat_pheno_mdr,
        pat_gene_mdr=pat_gene_mdr,
        coocc_pheno_mdr=coocc_pheno_mdr,
        coocc_gene_mdr=coocc_gene_mdr,
        gene_pheno_assoc=gene_pheno_assoc,
        assoc_rules_pheno=assoc_pheno,
        assoc_rules_genes=assoc_genes,
        hybrid_net=hybrid_net,
        edges_df=edges_df,
        comm_df=comm_df,
        net_html=net_html,
    )

    # 15) Save HTML report
    out_html = save_report(html_report, "output")

    # 16) Generate and save Excel report with PNG charts
    excel_path = generate_excel_report(
        data=data,
        class_res_all=class_res_all,
        class_res_mdr=class_res_mdr,
        amr_all=amr_all,
        amr_mdr=amr_mdr,
        freq_pheno_all=freq_pheno_all,
        freq_pheno_mdr=freq_pheno_mdr,
        freq_gene_all=freq_gene_all,
        freq_gene_mdr=freq_gene_mdr,
        pat_pheno_mdr=pat_pheno_mdr,
        pat_gene_mdr=pat_gene_mdr,
        coocc_pheno_mdr=coocc_pheno_mdr,
        coocc_gene_mdr=coocc_gene_mdr,
        gene_pheno_assoc=gene_pheno_assoc,
        assoc_rules_pheno=assoc_pheno,
        assoc_rules_genes=assoc_genes,
        hybrid_net=hybrid_net,
        edges_df=edges_df,
        comm_df=comm_df,
        fig_network=fig_network,
    )

    end_time = time.time()
    logging.info(f"Hybrid pipeline completed in {end_time - start_time:.2f}s")
    logging.info(f"HTML report: {out_html}")
    logging.info(f"Excel report: {excel_path}")


if __name__ == "__main__":
    main()
