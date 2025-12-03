"""
Report generation utilities for StrepSuisAnalyzer.

Provides functions to generate Excel and HTML reports from analysis results.
"""

from typing import Dict, List, Optional, Any
import pandas as pd
from pathlib import Path
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows


class ReportGenerator:
    """Generates reports from analysis results."""

    def __init__(self):
        """Initialize the ReportGenerator."""
        self.report_data = {}
        self.metadata = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tool": "StrepSuisAnalyzer",
            "version": "1.0.0",
        }

    def add_dataframe(self, name: str, df: pd.DataFrame, description: str = ""):
        """
        Add a DataFrame to the report.

        Args:
            name: Name for this data section
            df: DataFrame to add
            description: Optional description
        """
        self.report_data[name] = {"data": df, "description": description, "type": "dataframe"}

    def add_statistics(self, name: str, stats_dict: Dict[str, Any], description: str = ""):
        """
        Add statistics to the report.

        Args:
            name: Name for this statistics section
            stats_dict: Dictionary of statistics
            description: Optional description
        """
        self.report_data[name] = {
            "data": stats_dict,
            "description": description,
            "type": "statistics",
        }

    def add_text(self, name: str, text: str):
        """
        Add text content to the report.

        Args:
            name: Name for this text section
            text: Text content
        """
        self.report_data[name] = {"data": text, "type": "text"}

    def export_to_excel(
        self, filepath: str, include_metadata: bool = True, style_headers: bool = True
    ):
        """
        Export report to Excel file.

        Args:
            filepath: Output file path
            include_metadata: Whether to include metadata sheet
            style_headers: Whether to style header rows
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
            # Add metadata sheet
            if include_metadata:
                metadata_df = pd.DataFrame([self.metadata]).T
                metadata_df.columns = ["Value"]
                metadata_df.to_excel(writer, sheet_name="Metadata")

            # Add data sheets
            for name, content in self.report_data.items():
                sheet_name = self._sanitize_sheet_name(name)

                if content["type"] == "dataframe":
                    df = content["data"]
                    df.to_excel(writer, sheet_name=sheet_name, index=True)

                    if style_headers:
                        self._style_excel_sheet(writer.book[sheet_name])

                elif content["type"] == "statistics":
                    stats_df = pd.DataFrame([content["data"]]).T
                    stats_df.columns = ["Value"]
                    stats_df.to_excel(writer, sheet_name=sheet_name)

                    if style_headers:
                        self._style_excel_sheet(writer.book[sheet_name])

                elif content["type"] == "text":
                    text_df = pd.DataFrame({"Content": [content["data"]]})
                    text_df.to_excel(writer, sheet_name=sheet_name, index=False)

    def export_to_html(self, filepath: str, include_css: bool = True) -> str:
        """
        Export report to HTML file.

        Args:
            filepath: Output file path
            include_css: Whether to include CSS styling

        Returns:
            HTML content as string
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        html_parts = []

        # HTML header
        if include_css:
            html_parts.append(self._get_html_header())
        else:
            html_parts.append("<html><body>")

        # Title
        html_parts.append("<h1>StrepSuisAnalyzer Report</h1>")

        # Metadata
        html_parts.append("<h2>Metadata</h2>")
        html_parts.append("<table class='metadata'>")
        for key, value in self.metadata.items():
            html_parts.append(f"<tr><td><b>{key}</b></td><td>{value}</td></tr>")
        html_parts.append("</table>")

        # Data sections
        for name, content in self.report_data.items():
            html_parts.append(f"<h2>{name}</h2>")

            if content.get("description"):
                html_parts.append(f"<p class='description'>{content['description']}</p>")

            if content["type"] == "dataframe":
                df = content["data"]
                html_parts.append(df.to_html(classes="data-table", index=True))

            elif content["type"] == "statistics":
                stats_df = pd.DataFrame([content["data"]]).T
                stats_df.columns = ["Value"]
                html_parts.append(stats_df.to_html(classes="data-table"))

            elif content["type"] == "text":
                html_parts.append(f"<p class='text-content'>{content['data']}</p>")

        # HTML footer
        html_parts.append("</body></html>")

        html_content = "\n".join(html_parts)

        # Write to file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        return html_content

    def _sanitize_sheet_name(self, name: str) -> str:
        """
        Sanitize sheet name for Excel.

        Args:
            name: Original name

        Returns:
            Sanitized name
        """
        # Excel sheet names cannot exceed 31 characters and cannot contain certain characters
        invalid_chars = ['\\', '/', '*', '[', ']', ':', '?']
        sanitized = name
        for char in invalid_chars:
            sanitized = sanitized.replace(char, '_')

        return sanitized[:31]

    def _style_excel_sheet(self, worksheet):
        """
        Apply styling to Excel worksheet.

        Args:
            worksheet: openpyxl worksheet object
        """
        # Style header row
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")

        for cell in worksheet[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")

        # Adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width

    def _get_html_header(self) -> str:
        """
        Get HTML header with CSS.

        Returns:
            HTML header string
        """
        return """
        <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }
                h1 {
                    color: #366092;
                    border-bottom: 2px solid #366092;
                    padding-bottom: 10px;
                }
                h2 {
                    color: #555;
                    margin-top: 30px;
                    border-bottom: 1px solid #ccc;
                    padding-bottom: 5px;
                }
                table.metadata {
                    background-color: white;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }
                table.metadata td {
                    padding: 8px;
                    border: 1px solid #ddd;
                }
                table.data-table {
                    border-collapse: collapse;
                    background-color: white;
                    margin-bottom: 20px;
                }
                table.data-table th {
                    background-color: #366092;
                    color: white;
                    padding: 10px;
                    text-align: left;
                }
                table.data-table td {
                    padding: 8px;
                    border: 1px solid #ddd;
                }
                table.data-table tr:nth-child(even) {
                    background-color: #f9f9f9;
                }
                .description {
                    color: #666;
                    font-style: italic;
                    margin-bottom: 10px;
                }
                .text-content {
                    background-color: white;
                    padding: 15px;
                    border-left: 3px solid #366092;
                }
            </style>
        </head>
        <body>
        """

    def clear(self):
        """Clear all report data."""
        self.report_data = {}
        self.metadata["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
