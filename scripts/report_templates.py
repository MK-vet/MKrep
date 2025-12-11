"""
Shared HTML Report Templates for MKrep Analysis Tools

This module provides standardized HTML templates and utilities for generating
consistent, professional reports across all MKrep analysis tools.

Features:
- Unified Bootstrap 5 styling
- Interactive DataTables with export functionality
- Responsive design
- Plotly integration for interactive charts
- Collapsible sections
- Consistent color scheme and layout
"""

def get_html_head(title="MKrep Analysis Report"):
    """
    Get standardized HTML head section with all required CSS and meta tags.
    
    Args:
        title: Page title
        
    Returns:
        str: HTML head section
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- DataTables CSS -->
    <link href="https://cdn.datatables.net/1.13.6/css/dataTables.bootstrap5.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/buttons/2.4.1/css/buttons.bootstrap5.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/searchbuilder/1.4.2/css/searchBuilder.bootstrap5.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/searchpanes/2.1.2/css/searchPanes.bootstrap5.min.css" rel="stylesheet">
    
    <!-- Plotly -->
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    
    <!-- Custom Styles -->
    <style>
        :root {{
            --primary-color: #667eea;
            --secondary-color: #764ba2;
            --success-color: #28a745;
            --info-color: #17a2b8;
            --warning-color: #ffc107;
            --danger-color: #dc3545;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
            padding: 20px;
        }}
        
        .main-container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header-section {{
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        
        .header-section h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: bold;
        }}
        
        .header-section p {{
            margin: 10px 0 0 0;
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .section-card {{
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            margin-bottom: 25px;
            overflow: hidden;
        }}
        
        .section-header {{
            background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            padding: 15px 20px;
            font-weight: bold;
            font-size: 1.3em;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .section-header:hover {{
            opacity: 0.9;
        }}
        
        .section-content {{
            padding: 20px;
        }}
        
        .interpretation-box {{
            background: #f0f7ff;
            border-left: 4px solid var(--info-color);
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}
        
        .interpretation-box h4 {{
            color: var(--info-color);
            margin-top: 0;
            font-size: 1.1em;
        }}
        
        .interpretation-box ul {{
            margin-bottom: 0;
        }}
        
        .methodology-box {{
            background: #fff3cd;
            border-left: 4px solid var(--warning-color);
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}
        
        .methodology-box h4 {{
            color: #856404;
            margin-top: 0;
            font-size: 1.1em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: var(--primary-color);
            margin: 10px 0;
        }}
        
        .stat-label {{
            font-size: 1.1em;
            color: #666;
        }}
        
        .table-container {{
            margin: 20px 0;
            overflow-x: auto;
        }}
        
        .data-table {{
            width: 100% !important;
        }}
        
        .data-table th {{
            background: var(--primary-color) !important;
            color: white !important;
        }}
        
        .plot-container {{
            margin: 20px 0;
            min-height: 400px;
        }}
        
        .alert-custom {{
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
        }}
        
        .badge-custom {{
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
        }}
        
        .footer {{
            margin-top: 40px;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 2px solid #e0e0e0;
        }}
        
        /* Print styles */
        @media print {{
            body {{
                background: white;
            }}
            .main-container {{
                box-shadow: none;
            }}
            .section-card {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
"""


def get_html_scripts():
    """
    Get standardized JavaScript section with DataTables initialization.
    
    Returns:
        str: HTML script section
    """
    return """
    <!-- jQuery (required for DataTables) -->
    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    
    <!-- Bootstrap 5 JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- DataTables JS -->
    <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.6/js/dataTables.bootstrap5.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/2.4.1/js/dataTables.buttons.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/2.4.1/js/buttons.bootstrap5.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/2.4.1/js/buttons.html5.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/2.4.1/js/buttons.print.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/pdfmake.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/vfs_fonts.js"></script>
    
    <script>
        $(document).ready(function() {
            // Initialize all DataTables
            $('.data-table').DataTable({
                dom: 'Blfrtip',
                buttons: [
                    {
                        extend: 'copy',
                        className: 'btn btn-sm btn-primary'
                    },
                    {
                        extend: 'csv',
                        className: 'btn btn-sm btn-primary'
                    },
                    {
                        extend: 'excel',
                        className: 'btn btn-sm btn-primary'
                    },
                    {
                        extend: 'pdf',
                        className: 'btn btn-sm btn-primary'
                    },
                    {
                        extend: 'print',
                        className: 'btn btn-sm btn-primary'
                    }
                ],
                lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
                pageLength: 25,
                responsive: true,
                order: [[0, 'asc']]
            });
            
            // Collapsible sections
            $('.section-header').click(function() {
                $(this).next('.section-content').slideToggle(300);
                $(this).find('.toggle-icon').toggleClass('rotated');
            });
            
            // Smooth scrolling for navigation
            $('a[href^="#"]').on('click', function(e) {
                e.preventDefault();
                var target = $(this.getAttribute('href'));
                if(target.length) {
                    $('html, body').stop().animate({
                        scrollTop: target.offset().top - 20
                    }, 500);
                }
            });
        });
    </script>
</body>
</html>
"""


def create_header(title, subtitle, analysis_date=None):
    """
    Create standardized header section.
    
    Args:
        title: Main title
        subtitle: Subtitle/description
        analysis_date: Date of analysis (optional)
        
    Returns:
        str: HTML header section
    """
    date_str = f"<p><small>Analysis Date: {analysis_date}</small></p>" if analysis_date else ""
    
    return f"""
    <div class="header-section">
        <h1>🧬 {title}</h1>
        <p>{subtitle}</p>
        {date_str}
    </div>
    """


def create_nav_menu(sections):
    """
    Create navigation menu for report sections.
    
    Args:
        sections: List of tuples (section_id, section_name)
        
    Returns:
        str: HTML navigation menu
    """
    nav_items = "\n".join([
        f'<li class="nav-item"><a class="nav-link" href="#{sid}">{sname}</a></li>'
        for sid, sname in sections
    ])
    
    return f"""
    <nav class="navbar navbar-expand-lg navbar-light bg-light mb-4" style="border-radius: 8px;">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" 
                    data-bs-target="#navbarNav" aria-controls="navbarNav" 
                    aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    {nav_items}
                </ul>
            </div>
        </div>
    </nav>
    """


def create_section(section_id, title, content, collapsible=False, open_by_default=True):
    """
    Create a standardized section card.
    
    Args:
        section_id: Unique section ID
        title: Section title
        content: HTML content
        collapsible: Whether section can be collapsed
        open_by_default: Whether section is open initially
        
    Returns:
        str: HTML section
    """
    toggle_icon = '<span class="toggle-icon">▼</span>' if collapsible else ''
    display_style = '' if open_by_default else 'style="display: none;"'
    
    return f"""
    <div id="{section_id}" class="section-card">
        <div class="section-header">
            <span>{title}</span>
            {toggle_icon}
        </div>
        <div class="section-content" {display_style}>
            {content}
        </div>
    </div>
    """


def create_interpretation_box(interpretation_text):
    """
    Create an interpretation box for results.
    
    Args:
        interpretation_text: HTML interpretation content
        
    Returns:
        str: HTML interpretation box
    """
    return f"""
    <div class="interpretation-box">
        <h4>📊 Interpretation</h4>
        {interpretation_text}
    </div>
    """


def create_methodology_box(methodology_text):
    """
    Create a methodology box.
    
    Args:
        methodology_text: HTML methodology content
        
    Returns:
        str: HTML methodology box
    """
    return f"""
    <div class="methodology-box">
        <h4>🔬 Methodology</h4>
        {methodology_text}
    </div>
    """


def create_stats_grid(stats_dict):
    """
    Create a grid of statistics cards.
    
    Args:
        stats_dict: Dictionary of {label: value}
        
    Returns:
        str: HTML stats grid
    """
    cards = "\n".join([
        f"""
        <div class="stat-card">
            <div class="stat-label">{label}</div>
            <div class="stat-value">{value}</div>
        </div>
        """
        for label, value in stats_dict.items()
    ])
    
    return f'<div class="stats-grid">{cards}</div>'


def df_to_html_table(df, table_id="datatable", show_index=False):
    """
    Convert DataFrame to HTML table with DataTables class.
    
    Args:
        df: pandas DataFrame
        table_id: Unique table ID
        show_index: Whether to show DataFrame index
        
    Returns:
        str: HTML table
    """
    return f'<div class="table-container">{df.to_html(classes="table table-striped data-table", table_id=table_id, index=show_index)}</div>'


def create_alert(message, alert_type="info"):
    """
    Create a Bootstrap alert.
    
    Args:
        message: Alert message
        alert_type: Bootstrap alert type (success, info, warning, danger)
        
    Returns:
        str: HTML alert
    """
    icons = {
        'success': '✓',
        'info': 'ℹ',
        'warning': '⚠',
        'danger': '✗'
    }
    icon = icons.get(alert_type, 'ℹ')
    
    return f"""
    <div class="alert alert-{alert_type} alert-custom" role="alert">
        <strong>{icon}</strong> {message}
    </div>
    """


def create_footer():
    """
    Create standardized footer.
    
    Returns:
        str: HTML footer
    """
    return """
    <div class="footer">
        <p><strong>MKrep</strong> - Comprehensive Bioinformatics Analysis Pipeline</p>
        <p>
            <a href="https://github.com/MK-vet/MKrep" target="_blank">GitHub Repository</a> | 
            <a href="https://github.com/MK-vet/MKrep/issues" target="_blank">Report Issues</a>
        </p>
        <p><small>Version 1.0.0 | MIT License | Generated: {}</small></p>
    </div>
    """.format(pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))


def create_full_report(title, subtitle, sections_data, analysis_date=None):
    """
    Create a complete HTML report with all sections.
    
    Args:
        title: Report title
        subtitle: Report subtitle
        sections_data: List of tuples (section_id, section_title, section_content)
        analysis_date: Date of analysis (optional)
        
    Returns:
        str: Complete HTML report
    """
    # Build navigation menu
    nav_sections = [(sid, stitle) for sid, stitle, _ in sections_data]
    nav_menu = create_nav_menu(nav_sections)
    
    # Build sections
    sections_html = "\n".join([
        create_section(sid, stitle, scontent)
        for sid, stitle, scontent in sections_data
    ])
    
    # Combine all parts
    html = get_html_head(title)
    html += '<div class="main-container">'
    html += create_header(title, subtitle, analysis_date)
    html += nav_menu
    html += sections_html
    html += create_footer()
    html += '</div>'
    html += get_html_scripts()
    
    return html


# Example usage for reproducibility documentation
REPRODUCIBILITY_SECTION = """
<div class="methodology-box">
    <h4>🔁 Reproducibility</h4>
    <p>This analysis is fully reproducible. To replicate the results:</p>
    <ol>
        <li><strong>Use the same input data:</strong> Ensure CSV files have identical content</li>
        <li><strong>Set the same random seed:</strong> Check the metadata section for the seed value</li>
        <li><strong>Use the same parameters:</strong> All parameters are documented in the metadata</li>
        <li><strong>Use the same software versions:</strong> See requirements.txt in the repository</li>
    </ol>
    <p>The analysis uses deterministic algorithms wherever possible. Random processes (e.g., bootstrap resampling) 
    are controlled by the random seed to ensure reproducibility.</p>
</div>
"""


# Example interpretation templates
CLUSTER_INTERPRETATION_TEMPLATE = """
<p><strong>Summary:</strong> The clustering analysis identified {n_clusters} distinct groups based on 
the {feature_type} profile. The average silhouette score of {silhouette:.3f} indicates 
{interpretation} cluster quality.</p>

<p><strong>Key Findings:</strong></p>
<ul>
    <li>Cluster {best_cluster} shows the highest cohesion (silhouette: {best_silhouette:.3f})</li>
    <li>{n_significant} features show statistically significant associations with clusters (FDR < 0.05)</li>
    <li>Bootstrap validation confirms {confidence}% confidence in cluster assignments</li>
</ul>

<p><strong>Recommendations:</strong></p>
<ul>
    <li>Focus on features with high chi-square values for cluster characterization</li>
    <li>Consider biological relevance when interpreting cluster differences</li>
    <li>Validate findings with independent datasets if available</li>
</ul>
"""

MDR_INTERPRETATION_TEMPLATE = """
<p><strong>Summary:</strong> Multi-drug resistance (MDR) was defined as resistance to ≥{threshold} 
antibiotic classes. Out of {n_strains} strains analyzed, {n_mdr} ({pct_mdr:.1f}%) were classified as MDR.</p>

<p><strong>Key Findings:</strong></p>
<ul>
    <li>MDR prevalence: {mdr_prevalence:.1f}% (95% CI: {ci_lower:.1f}%-{ci_upper:.1f}%)</li>
    <li>{n_patterns} distinct resistance patterns identified</li>
    <li>Most common co-resistance: {common_pattern}</li>
    <li>Network analysis revealed {n_communities} resistance communities</li>
</ul>

<p><strong>Clinical Implications:</strong></p>
<ul>
    <li>High MDR prevalence indicates need for antimicrobial stewardship</li>
    <li>Co-resistance patterns suggest common genetic linkage</li>
    <li>Consider these patterns when selecting empirical therapy</li>
</ul>
"""

# Import pandas for timestamp
import pandas as pd
