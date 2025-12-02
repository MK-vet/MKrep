# Results Interpretation Guide for MKrep

**How to understand and interpret your analysis results**

This guide provides detailed explanations of statistical results, visualizations, and recommendations 
for each type of analysis in MKrep.

---

## Table of Contents

1. [General Statistical Concepts](#general-statistical-concepts)
2. [Cluster Analysis Interpretation](#cluster-analysis-interpretation)
3. [MDR Analysis Interpretation](#mdr-analysis-interpretation)
4. [Network Analysis Interpretation](#network-analysis-interpretation)
5. [Phylogenetic Analysis Interpretation](#phylogenetic-analysis-interpretation)
6. [StrepSuis Analysis Interpretation](#strepsuis-analysis-interpretation)
7. [Common Questions](#common-questions)

---

## General Statistical Concepts

### P-values and Statistical Significance

**What it means:**
- **P-value < 0.05:** Result is statistically significant (unlikely due to chance)
- **P-value ≥ 0.05:** Result is not statistically significant (could be due to chance)

**How to interpret:**
- Lower p-values indicate stronger evidence
- Statistical significance ≠ biological importance
- Always consider effect size along with p-value

**Example:**
```
Feature A: p-value = 0.001 (highly significant)
Feature B: p-value = 0.045 (marginally significant)
Feature C: p-value = 0.12 (not significant)
```

### FDR (False Discovery Rate) Correction

**What it means:**
- Adjusts p-values for multiple testing
- Controls expected proportion of false positives
- FDR < 0.05 means < 5% expected false discoveries

**How to interpret:**
- More stringent than individual p-values
- Reduces false positives in large datasets
- Recommended for genomic studies

### Confidence Intervals (CI)

**What it means:**
- Range of plausible values for a parameter
- 95% CI: 95% confident true value is within range
- Narrower CI = more precise estimate

**How to interpret:**
```
Prevalence: 35% (95% CI: 28%-42%)
→ True prevalence likely between 28% and 42%
→ Point estimate is 35%
```

### Effect Sizes

**What it means:**
- Magnitude of difference or association
- Independent of sample size
- More informative than p-values alone

**Common measures:**
- **Cohen's d:** Standardized mean difference
- **Odds Ratio (OR):** Relative odds of outcome
- **Cramér's V:** Strength of categorical association

---

## Cluster Analysis Interpretation

### Silhouette Score

**Range:** -1 to +1

**Interpretation:**
- **0.71-1.00:** Strong, well-separated clusters
- **0.51-0.70:** Reasonable cluster structure
- **0.26-0.50:** Weak, overlapping clusters
- **< 0.25:** No substantial cluster structure

**Example:**
```
Average Silhouette Score: 0.62

INTERPRETATION:
✓ Reasonable cluster quality
✓ Clusters are fairly well-separated
✓ Some overlap between clusters expected
→ Results are meaningful but not perfect separation
```

### Number of Clusters

**How it's determined:**
1. Test range of cluster numbers (e.g., 2-8)
2. Calculate silhouette score for each
3. Select number with highest score

**Interpretation:**
```
Optimal clusters: 4
Silhouette: 0.65

INTERPRETATION:
✓ Data naturally groups into 4 categories
✓ More clusters would reduce quality
✓ Fewer clusters would miss distinctions
→ Focus on characterizing these 4 groups
```

### Cluster Characterization

**Chi-square Test Results:**

**Interpretation:**
- **High chi-square (χ²):** Strong association with clusters
- **Low p-value:** Statistically significant
- **Post-FDR significant:** Robust finding

**Example:**
```
Feature: Beta-lactam Resistance
χ² = 45.6, p < 0.001, FDR < 0.001
Cluster 1: 90% present
Cluster 2: 20% present

INTERPRETATION:
✓ Strong cluster-specific feature
✓ Highly significant association
✓ Cluster 1 characterized by β-lactam resistance
→ This is a key distinguishing feature
```

### MCA (Multiple Correspondence Analysis)

**What it shows:**
- Dimensional reduction of binary data
- Similar strains plotted close together
- Feature associations visible

**Interpretation:**
```
MCA explains 45% variance in 2 dimensions

INTERPRETATION:
✓ Good dimensional reduction
✓ 2D plot captures nearly half the variation
✓ Remaining variation in additional dimensions
→ 2D visualization is informative but simplified
```

### Bootstrap Confidence

**What it means:**
- Stability of cluster assignments
- Tested by resampling data

**Interpretation:**
```
Bootstrap agreement: 87%

INTERPRETATION:
✓ Clusters are stable
✓ 87% of assignments confirmed
✓ Some uncertainty in borderline strains
→ Results are reliable
```

### Recommendations

1. **Focus on significant features**
   - FDR < 0.05 and high χ²
   - These define cluster differences

2. **Consider cluster size**
   - Very small clusters may be outliers
   - Balance statistical and biological meaning

3. **Validate findings**
   - Check against known biology
   - Test with independent data

---

## MDR Analysis Interpretation

### MDR Prevalence

**Definition:** Percentage of strains resistant to ≥ threshold antibiotic classes

**Interpretation:**
```
MDR Prevalence: 45% (95% CI: 38%-52%)
Threshold: 3 classes

INTERPRETATION:
✓ Nearly half of strains are MDR
✓ True prevalence likely 38-52%
✓ High MDR burden in this population
→ Concern for treatment options
```

**Clinical Significance:**
- **< 10%:** Low MDR prevalence
- **10-30%:** Moderate MDR prevalence
- **> 30%:** High MDR prevalence

### Resistance Patterns

**Association Rules:**

**Interpretation:**
```
Rule: {Amp} → {Tet, Erm}
Support: 35%
Confidence: 82%
Lift: 2.1

INTERPRETATION:
✓ 35% of strains have all three resistances
✓ 82% of Amp-resistant strains also resist Tet & Erm
✓ Co-occurrence 2.1× more than expected
→ Likely genetic linkage (e.g., mobile element)
```

**Metrics:**
- **Support:** How common the pattern is
- **Confidence:** How reliable the association is
- **Lift:** How much more common than random

### Network Communities

**What they represent:**
- Groups of co-occurring resistances
- Potential genetic linkages
- Treatment considerations

**Interpretation:**
```
Community 1: β-lactams + aminoglycosides
Community 2: Macrolides + tetracyclines
Community 3: Fluoroquinolones + sulfonamides

INTERPRETATION:
✓ Three distinct resistance modules
✓ Within-community resistances often co-occur
✓ Between-community resistances independent
→ Target vulnerabilities between communities
```

### Hub Genes/Phenotypes

**What they are:**
- Highly connected nodes in network
- Central to resistance patterns

**Interpretation:**
```
Hub: ermB gene
Degree centrality: 0.45
Betweenness centrality: 0.38

INTERPRETATION:
✓ ermB connects to many other resistances
✓ Central to resistance network
✓ Bridges multiple communities
→ Key target for surveillance and intervention
```

### Recommendations

1. **Empirical therapy**
   - Avoid antibiotics in same community
   - Target resistance-free communities

2. **Surveillance**
   - Monitor hub genes/phenotypes
   - Track community evolution

3. **Stewardship**
   - High MDR prevalence requires action
   - Consider antibiotic cycling

---

## Network Analysis Interpretation

### Chi-square Associations

**What they test:**
- Independence between features
- Strength of association

**Interpretation:**
```
Feature Pair: Gene A × Gene B
χ² = 78.3, p < 0.001
Cramér's V = 0.42

INTERPRETATION:
✓ Strongly associated (not independent)
✓ Medium-strong effect size (V = 0.42)
✓ Highly significant
→ Genes A & B frequently co-occur
```

**Cramér's V Scale:**
- **< 0.1:** Weak association
- **0.1-0.3:** Moderate association
- **0.3-0.5:** Strong association
- **> 0.5:** Very strong association

### Entropy Analysis

**What it measures:**
- Variability/diversity of features
- Predictability

**Interpretation:**
```
Feature A entropy: 0.95
Feature B entropy: 0.12

INTERPRETATION:
Feature A: High entropy
✓ High variability across strains
✓ Unpredictable presence/absence
→ Useful for classification

Feature B: Low entropy
✓ Present in most strains
✓ Predictable (mostly 1 or mostly 0)
→ Less informative for classification
```

### Mutual Exclusivity

**What it means:**
- Features rarely occur together
- Potential functional redundancy

**Interpretation:**
```
Gene X and Gene Y: Mutually exclusive
Co-occurrence: 2%
Expected: 35%

INTERPRETATION:
✓ Genes almost never co-occur
✓ Much less than expected by chance
✓ Possible functional redundancy
→ May serve similar roles
```

### Network Communities

**What they represent:**
- Modules of related features
- Potential functional groups

**Interpretation:**
```
Community 1: Virulence genes
Community 2: Resistance genes
Community 3: Metabolism genes

INTERPRETATION:
✓ Features cluster by function
✓ Within-community features interact
✓ Between-community features independent
→ Modular genetic architecture
```

### Recommendations

1. **Feature selection**
   - High entropy features more informative
   - Remove low-variance features

2. **Functional modules**
   - Study communities as functional units
   - Look for biological explanations

3. **Redundancy**
   - Mutually exclusive features may be redundant
   - Consider as alternatives, not independent

---

## Phylogenetic Analysis Interpretation

### Phylogenetic Diversity (PD)

**What it measures:**
- Evolutionary diversity
- Total branch length

**Interpretation:**
```
Faith's PD: 3.45
Number of strains: 50

INTERPRETATION:
✓ Moderate phylogenetic diversity
✓ Strains span 3.45 substitutions/site
✓ More diversity = more evolutionary distance
→ Consider phylogeny in trait analysis
```

### Tree-based Clustering

**Methods:**
- Considers phylogenetic relationships
- Groups nearby strains

**Interpretation:**
```
Phylogenetic clusters: 5
Average pairwise distance: 0.15

INTERPRETATION:
✓ Five phylogenetically coherent groups
✓ Within-cluster strains closely related
✓ Between-cluster strains more distant
→ Clustering reflects evolution
```

### Trait-Phylogeny Associations

**What they test:**
- Whether traits cluster on tree
- Phylogenetic signal

**Interpretation:**
```
Trait: Ampicillin resistance
Phylogenetic signal: Strong
p < 0.001

INTERPRETATION:
✓ Resistance clusters phylogenetically
✓ Related strains have similar phenotypes
✓ Vertical transmission likely
→ Trait evolved in specific lineages
```

### UMAP Visualization

**What it shows:**
- 2D representation of high-dimensional data
- Phylogenetic and trait relationships

**Interpretation:**
```
UMAP 2D projection
Variance explained: 65%

INTERPRETATION:
✓ Good dimensional reduction
✓ Similar strains plot together
✓ Clusters visible in 2D
→ Use for visual exploration
```

### Recommendations

1. **Consider phylogeny**
   - Don't treat strains as independent
   - Account for evolutionary relationships

2. **Trait evolution**
   - Strong signal suggests vertical transmission
   - Weak signal suggests horizontal transfer

3. **Lineage-specific traits**
   - Focus on clade-defining features
   - Understand evolutionary context

---

## StrepSuis Analysis Interpretation

This analysis combines phylogenetic and trait profiling specifically for *Streptococcus suis*.

### Ensemble Clustering

**What it is:**
- Combination of multiple algorithms
- More robust than single method

**Interpretation:**
```
Ensemble consensus: 85%
Number of methods: 5

INTERPRETATION:
✓ Most methods agree (85%)
✓ Robust cluster assignments
✓ Some disagreement at boundaries
→ Reliable clustering results
```

### Log-odds Ratios

**What they measure:**
- Strength of trait-cluster association
- Direction of effect

**Interpretation:**
```
Trait: Virulence gene X
Cluster 2 log-odds: 2.3
95% CI: [1.8, 2.8]

INTERPRETATION:
✓ Strongly associated with Cluster 2
✓ Positive log-odds (enriched)
✓ CI excludes zero (significant)
→ Gene X characteristic of Cluster 2
```

**Scale:**
- **< -1:** Depleted (trait absent)
- **-1 to +1:** Weak/no association
- **> +1:** Enriched (trait present)

### Random Forest Importance

**What it measures:**
- Feature importance for prediction
- Non-linear relationships

**Interpretation:**
```
Feature: Capsule type
RF importance: 0.25
Rank: 1

INTERPRETATION:
✓ Most important feature
✓ Strong predictive power
✓ Critical for classification
→ Key distinguishing characteristic
```

### Recommendations

1. **Focus on top features**
   - High RF importance
   - Significant log-odds
   - These define clusters

2. **S. suis specific**
   - Results tailored to this species
   - Consider known biology

3. **Validation**
   - Test findings with independent data
   - Compare to literature

---

## Common Questions

### Q1: What if no significant results?

**A:** This can happen when:
- Sample size is small
- Features have low variability
- True associations are weak

**What to do:**
- Increase sample size if possible
- Check data quality
- Consider relaxing FDR threshold (with caution)
- Report negative findings (also valuable!)

### Q2: How to choose parameters?

**A:** Use defaults unless:
- Domain knowledge suggests changes
- Sensitivity analysis shows better results
- Specific research questions require adjustment

### Q3: What sample size is needed?

**A:** Rule of thumb:
- **Minimum:** 20 strains
- **Recommended:** 50+ strains
- **Ideal:** 100+ strains
- More strains = more statistical power

### Q4: How to handle conflicting results?

**A:** When methods disagree:
- Trust ensemble/consensus results
- Consider biological plausibility
- Validate with independent data
- Report uncertainty honestly

### Q5: Are results clinically relevant?

**A:** Consider:
- **Statistical significance:** Is it real?
- **Effect size:** Is it large enough to matter?
- **Clinical context:** Does it affect treatment?
- **Prevalence:** How common is it?

### Q6: How to report in publications?

**A:** Include:
- All parameters used
- Random seed for reproducibility
- Software versions
- Sample sizes
- Effect sizes and CIs (not just p-values)

---

## Quick Reference Tables

### Interpretation Thresholds

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| Silhouette | > 0.7 | 0.5-0.7 | < 0.5 |
| Cramér's V | > 0.3 | 0.1-0.3 | < 0.1 |
| Bootstrap | > 85% | 70-85% | < 70% |
| MCA variance | > 50% | 30-50% | < 30% |

### Effect Size Interpretation

| Cohen's d | Interpretation |
|-----------|----------------|
| < 0.2 | Negligible |
| 0.2-0.5 | Small |
| 0.5-0.8 | Medium |
| > 0.8 | Large |

| Odds Ratio | Interpretation |
|------------|----------------|
| 0.9-1.1 | No association |
| 1.5-2.0 | Weak association |
| 2.0-4.0 | Moderate association |
| > 4.0 | Strong association |

---

**Last Updated:** 2025-01-15  
**Version:** 1.0.0  
**For More Help:** See USER_GUIDE.md or contact support
