# MKrep Script Standardization Guide

**Guidelines for maintaining consistency across all MKrep analysis tools**

## Purpose

This guide ensures that all MKrep analysis scripts:
1. Have similar structure and appearance
2. Are fully self-contained and easy to use
3. Generate consistent, professional reports
4. Include interpretation to facilitate analysis
5. Ensure reproducibility
6. Are documented in English

---

## Script Structure

All analysis scripts should follow this structure:

```
1. Header and Documentation
   - Purpose and description
   - Required/optional files
   - Output files
   - Usage instructions
   
2. Imports
   - Organized by category
   - Standard library first
   - Third-party packages
   - MKrep modules last
   
3. Configuration
   - All parameters in Config class
   - Defaults clearly stated
   - Easy to modify
   
4. Utility Functions
   - Data validation
   - File I/O
   - Helper functions
   
5. Analysis Functions
   - Main analysis logic
   - Well-documented
   - Modular design
   
6. Visualization Functions
   - Chart generation
   - PNG export
   - Consistent styling
   
7. Report Generation
   - HTML report (using shared templates)
   - Excel report (using shared utilities)
   - Interpretation included
   
8. Main Function
   - Orchestrates workflow
   - Clear progress messages
   - Error handling
   
9. Script Execution
   - if __name__ == "__main__"
```

See `analysis_script_template.py` for complete template.

---

## Standardization Checklist

### ✓ Self-Contained Operation

- [ ] Script runs independently without external dependencies beyond requirements.txt
- [ ] All file paths are configurable in Config class
- [ ] Default values work out-of-the-box with sample data
- [ ] No hardcoded absolute paths
- [ ] Clear error messages for missing files

### ✓ Appearance and Layout

- [ ] Uses shared report templates from `report_templates.py`
- [ ] Bootstrap 5 styling for HTML reports
- [ ] Consistent color scheme (primary: #667eea, secondary: #764ba2)
- [ ] Same section structure across all reports:
  - Header with title and subtitle
  - Navigation menu
  - Summary section
  - Methodology section
  - Results sections
  - Interpretation section
  - Footer with attribution

### ✓ Reproducibility

- [ ] Fixed random seed in Config (default: 42)
- [ ] All parameters documented in reports
- [ ] Timestamp in report filenames
- [ ] Metadata sheet in Excel reports
- [ ] Reproducibility instructions in methodology section

### ✓ Report Generation

- [ ] **Exactly ONE HTML report per analysis**
  - Named: `[analysis]_report.html`
  - Interactive with DataTables
  - Includes all visualizations inline
  
- [ ] **Exactly ONE Excel report per analysis**
  - Named: `[analysis]_Report_YYYYMMDD_HHMMSS.xlsx`
  - Multi-sheet with metadata
  - Methodology sheet
  - Chart index sheet
  
- [ ] **PNG charts in subdirectory**
  - Saved in `png_charts/` folder
  - High quality (150 DPI minimum)
  - Descriptive filenames

### ✓ Interpretation

- [ ] Interpretation box in HTML report
- [ ] Explains what results mean
- [ ] Key findings highlighted
- [ ] Clinical/biological relevance discussed
- [ ] Recommendations provided
- [ ] Statistical concepts explained for non-experts

### ✓ English Language

- [ ] All comments in English
- [ ] All documentation in English
- [ ] All report text in English
- [ ] All variable names in English
- [ ] All error messages in English

### ✓ Code Organization

- [ ] Functions are modular and reusable
- [ ] Docstrings for all functions
- [ ] Type hints where appropriate
- [ ] Clear variable names
- [ ] Consistent formatting (PEP 8)
- [ ] No dead code or commented-out sections

---

## Report Template Usage

### Basic HTML Report

```python
from report_templates import (
    create_full_report,
    create_section,
    create_interpretation_box,
    create_methodology_box,
    create_stats_grid,
    df_to_html_table
)

# Prepare sections
sections_data = [
    ("summary", "Summary", summary_html),
    ("methodology", "Methodology", methodology_html),
    ("results", "Results", results_html),
    ("interpretation", "Interpretation", interpretation_html)
]

# Create report
html = create_full_report(
    title="Analysis Title",
    subtitle="Brief description",
    sections_data=sections_data,
    analysis_date="2025-01-15"
)

# Save
with open("report.html", 'w', encoding='utf-8') as f:
    f.write(html)
```

### Interpretation Box

```python
interpretation_text = """
<p><strong>Summary:</strong> Brief overview of findings</p>

<p><strong>Key Findings:</strong></p>
<ul>
    <li>Finding 1 with significance</li>
    <li>Finding 2 with effect size</li>
    <li>Finding 3 with context</li>
</ul>

<p><strong>Interpretation:</strong></p>
<ul>
    <li>What finding 1 means biologically</li>
    <li>Clinical relevance of finding 2</li>
</ul>

<p><strong>Recommendations:</strong></p>
<ul>
    <li>Next steps based on results</li>
    <li>Further validation needed</li>
</ul>
"""

interpretation_box = create_interpretation_box(interpretation_text)
```

### Methodology Box

```python
methodology_text = """
<h4>Statistical Methods</h4>
<ul>
    <li><strong>Test Name:</strong> Description and assumptions</li>
    <li><strong>Correction:</strong> FDR correction with α=0.05</li>
</ul>

<h4>Parameters</h4>
<ul>
    <li><strong>Random Seed:</strong> 42</li>
    <li><strong>Bootstrap:</strong> 500 iterations</li>
</ul>

<h4>Reproducibility</h4>
<p>To reproduce these results:</p>
<ol>
    <li>Use identical input data</li>
    <li>Set random seed to 42</li>
    <li>Use parameters listed above</li>
</ol>
"""

methodology_box = create_methodology_box(methodology_text)
```

### Stats Grid

```python
stats = {
    "Total Strains": 150,
    "Total Features": 85,
    "Significant Features": 23,
    "Analysis Time": "5.2 min"
}

stats_grid = create_stats_grid(stats)
```

### Data Table

```python
# Convert DataFrame to HTML table with DataTables
table_html = df_to_html_table(
    df=results_df,
    table_id="results_table",
    show_index=False
)
```

---

## Excel Report Usage

### Basic Excel Report

```python
from excel_report_utils import ExcelReportGenerator

# Initialize
excel_gen = ExcelReportGenerator("report.xlsx")

# Add metadata
metadata = {
    "Analysis Script": "script_name.py",
    "Analysis Date": "2025-01-15",
    "Random Seed": 42,
    "Bootstrap Iterations": 500
}
excel_gen.add_metadata_sheet(metadata)

# Add methodology
methodology_text = "Detailed methodology description..."
excel_gen.add_methodology_sheet(methodology_text)

# Add data sheets
excel_gen.add_data_sheet(
    df=results_df,
    sheet_name="Results",
    description="Main analysis results"
)

# Add chart index
excel_gen.add_chart_index("png_charts/")

# Save
excel_gen.save()
```

---

## Interpretation Guidelines

### What to Include

1. **Summary**
   - One paragraph overview
   - Main findings
   - Overall conclusion

2. **Key Findings**
   - 3-5 most important results
   - Include statistical significance
   - Include effect sizes
   - Provide context

3. **Interpretation**
   - Biological meaning
   - Clinical relevance
   - Comparison to literature
   - Limitations

4. **Recommendations**
   - Next steps
   - Validation needs
   - Clinical applications
   - Further research

### Example Templates

**Cluster Analysis:**
```
Summary: Identified {n} clusters with silhouette score of {score:.2f}, 
indicating {quality} cluster quality.

Key Findings:
• {n_features} features significantly associated with clusters (FDR < 0.05)
• Cluster {i} characterized by {feature} presence
• Bootstrap validation shows {pct}% confidence

Interpretation:
• Clear groupings suggest distinct phenotypes
• Feature {X} is key discriminator
• Results consistent with known biology

Recommendations:
• Focus on top features for characterization
• Validate with independent dataset
• Consider biological context
```

**MDR Analysis:**
```
Summary: MDR prevalence is {pct}% (95% CI: {ci_low}-{ci_high}%), 
defined as resistance to ≥{threshold} classes.

Key Findings:
• {n} strains classified as MDR
• {n_patterns} resistance patterns identified
• Network reveals {n_communities} communities

Interpretation:
• High MDR prevalence indicates treatment challenge
• Co-resistance patterns suggest genetic linkage
• Community structure reveals modular resistance

Recommendations:
• Implement antimicrobial stewardship
• Avoid antibiotics in same resistance community
• Monitor hub genes for surveillance
```

---

## Testing Checklist

Before finalizing a script update:

### Functionality
- [ ] Script runs without errors on sample data
- [ ] All required files are properly validated
- [ ] Analysis completes successfully
- [ ] Reports are generated correctly

### Reproducibility
- [ ] Running twice with same seed gives identical results
- [ ] All parameters documented in reports
- [ ] Metadata includes all necessary information

### Reports
- [ ] HTML report opens in browser
- [ ] DataTables work (sort, filter, export)
- [ ] Visualizations display correctly
- [ ] Excel report opens in Excel/LibreOffice
- [ ] All sheets present and formatted
- [ ] PNG files saved and listed

### Content
- [ ] Interpretation section present and helpful
- [ ] Methodology clearly explained
- [ ] Results clearly presented
- [ ] All text in English
- [ ] No spelling errors

### Code Quality
- [ ] Follows template structure
- [ ] Well-documented
- [ ] No hardcoded paths
- [ ] Proper error handling
- [ ] Clean and readable

---

## Migration Guide

### Updating Existing Scripts

1. **Review current script**
   - Identify analysis logic
   - Note unique features
   - Check report generation

2. **Create backup**
   ```bash
   cp script.py script_backup.py
   ```

3. **Update structure**
   - Follow template structure
   - Move code to appropriate sections
   - Add Config class

4. **Update report generation**
   - Replace HTML generation with templates
   - Use shared Excel utilities
   - Add interpretation section

5. **Test thoroughly**
   - Run with sample data
   - Check all outputs
   - Verify reproducibility

6. **Document changes**
   - Update docstrings
   - Add comments where needed
   - Update README if necessary

### Example Migration

**Before:**
```python
# Old style
html = """
<html>
<head><title>Report</title></head>
<body>
<h1>Results</h1>
""" + df.to_html() + """
</body>
</html>
"""
```

**After:**
```python
# New style using templates
from report_templates import create_full_report, df_to_html_table

results_html = df_to_html_table(df, "results_table")
sections_data = [
    ("results", "Results", results_html)
]

html = create_full_report(
    title="Analysis Report",
    subtitle="Results Summary",
    sections_data=sections_data
)
```

---

## Common Patterns

### Pattern 1: Bootstrap Confidence Intervals

```python
def bootstrap_statistic(data, statistic_func, n_iterations=500):
    """Calculate bootstrap confidence intervals"""
    np.random.seed(Config.RANDOM_SEED)
    bootstrap_values = []
    
    for i in range(n_iterations):
        sample = data.sample(n=len(data), replace=True)
        value = statistic_func(sample)
        bootstrap_values.append(value)
    
    ci_lower = np.percentile(bootstrap_values, 2.5)
    ci_upper = np.percentile(bootstrap_values, 97.5)
    
    return ci_lower, ci_upper
```

### Pattern 2: FDR Correction

```python
from statsmodels.stats.multitest import multipletests

def apply_fdr_correction(p_values, alpha=0.05):
    """Apply FDR correction to p-values"""
    reject, p_adjusted, _, _ = multipletests(
        p_values,
        alpha=alpha,
        method='fdr_bh'
    )
    return p_adjusted, reject
```

### Pattern 3: Progress Logging

```python
def log_progress(step, total, message):
    """Log progress with consistent format"""
    percentage = (step / total) * 100
    logging.info(f"[{step}/{total}] ({percentage:.1f}%) {message}")
    print(f"[{step}/{total}] {message}")
```

---

## Resources

- **Template:** `analysis_script_template.py`
- **Shared Templates:** `report_templates.py`
- **Excel Utilities:** `excel_report_utils.py`
- **User Guide:** `USER_GUIDE.md`
- **Interpretation Guide:** `INTERPRETATION_GUIDE.md`

---

**Last Updated:** 2025-01-15  
**Version:** 1.0.0
