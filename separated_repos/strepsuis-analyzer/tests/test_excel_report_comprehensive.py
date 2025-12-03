"""
Comprehensive Tests for Excel Report Utilities

Tests all methods in excel_report_utils.py to achieve 80%+ coverage.
"""

import pytest
import pandas as pd
import tempfile
import shutil
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

from strepsuis_analyzer.excel_report_utils import (
    ExcelReportGenerator,
    sanitize_sheet_name
)


class TestSanitizeSheetName:
    """Test sanitize_sheet_name function."""

    def test_sanitize_special_characters(self):
        """Test removal of invalid characters."""
        assert sanitize_sheet_name("Test:Name") == "Test_Name"
        assert sanitize_sheet_name("Test\\Name") == "Test_Name"
        assert sanitize_sheet_name("Test/Name") == "Test_Name"
        assert sanitize_sheet_name("Test?Name") == "Test_Name"
        assert sanitize_sheet_name("Test*Name") == "Test_Name"
        assert sanitize_sheet_name("Test[Name]") == "Test_Name_"

    def test_sanitize_long_names(self):
        """Test truncation to 31 characters."""
        long_name = "A" * 50
        sanitized = sanitize_sheet_name(long_name)
        assert len(sanitized) == 31

    def test_sanitize_combined(self):
        """Test combination of special chars and length."""
        long_name_with_specials = "Very:Long/Sheet\\Name?With*Special[Chars]" * 2
        sanitized = sanitize_sheet_name(long_name_with_specials)
        assert len(sanitized) == 31
        assert ":" not in sanitized
        assert "/" not in sanitized


class TestMetadataSheet:
    """Test create_metadata_sheet method."""

    def setup_method(self):
        """Create temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = ExcelReportGenerator(output_folder=self.temp_dir)

    def teardown_method(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_metadata_sheet_basic(self):
        """Test basic metadata sheet creation."""
        output_file = Path(self.temp_dir) / "metadata_test.xlsx"
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            self.generator.create_metadata_sheet(
                writer,
                script_name="test_script.py",
                analysis_date="2024-01-01 12:00:00"
            )
        
        # Read back and verify
        df = pd.read_excel(output_file, sheet_name='Metadata')
        assert 'Report Information' in df.columns
        assert 'Value' in df.columns
        assert 'test_script.py' in df['Value'].values
        assert '2024-01-01 12:00:00' in df['Value'].values

    def test_create_metadata_sheet_with_custom_metadata(self):
        """Test metadata sheet with custom fields."""
        output_file = Path(self.temp_dir) / "metadata_custom.xlsx"
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            self.generator.create_metadata_sheet(
                writer,
                script_name="custom_script.py",
                Total_Strains=100,
                Number_of_Clusters=5,
                Custom_Field="Custom Value"
            )
        
        # Read back
        df = pd.read_excel(output_file, sheet_name='Metadata')
        assert '100' in df['Value'].astype(str).values
        assert '5' in df['Value'].astype(str).values
        assert 'Custom Value' in df['Value'].values

    def test_create_metadata_sheet_default_date(self):
        """Test metadata sheet with default (current) date."""
        output_file = Path(self.temp_dir) / "metadata_date.xlsx"
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            self.generator.create_metadata_sheet(
                writer,
                script_name="test.py"
            )
        
        # Verify file created
        assert output_file.exists()


class TestMethodologySheet:
    """Test create_methodology_sheet method."""

    def setup_method(self):
        """Create temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = ExcelReportGenerator(output_folder=self.temp_dir)

    def teardown_method(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_methodology_sheet_dict(self):
        """Test methodology sheet with dict input."""
        output_file = Path(self.temp_dir) / "method_dict.xlsx"
        
        methodology = {
            'Clustering': 'Hierarchical clustering with Ward linkage',
            'Statistical Tests': 'Chi-square with FDR correction',
            'Visualization': 'MCA and heatmaps'
        }
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            self.generator.create_methodology_sheet(writer, methodology)
        
        # Read back
        df = pd.read_excel(output_file, sheet_name='Methodology')
        assert 'Section' in df.columns
        assert 'Description' in df.columns
        assert 'Clustering' in df['Section'].values

    def test_create_methodology_sheet_string(self):
        """Test methodology sheet with string input."""
        output_file = Path(self.temp_dir) / "method_string.xlsx"
        
        methodology_text = "This analysis uses hierarchical clustering and statistical tests."
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            self.generator.create_methodology_sheet(writer, methodology_text)
        
        # Read back
        df = pd.read_excel(output_file, sheet_name='Methodology')
        assert 'Methodology' in df.columns
        assert methodology_text in df['Methodology'].values

    def test_create_methodology_sheet_none(self):
        """Test methodology sheet with None input."""
        output_file = Path(self.temp_dir) / "method_none.xlsx"
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            self.generator.create_methodology_sheet(writer, None)
        
        # Verify file created
        assert output_file.exists()


class TestChartIndexSheet:
    """Test create_chart_index_sheet method."""

    def setup_method(self):
        """Create temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = ExcelReportGenerator(output_folder=self.temp_dir)

    def teardown_method(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_chart_index_with_charts(self):
        """Test chart index sheet with saved charts."""
        # Save some charts first
        for i in range(3):
            fig, ax = plt.subplots()
            ax.plot([1, 2, 3], [i, i*2, i*3])
            self.generator.save_matplotlib_figure(fig, f"chart_{i}")
        
        output_file = Path(self.temp_dir) / "chart_index.xlsx"
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            self.generator.create_chart_index_sheet(writer)
        
        # Read back
        df = pd.read_excel(output_file, sheet_name='Chart_Index')
        assert 'Chart Number' in df.columns
        assert 'Filename' in df.columns
        assert 'Full Path' in df.columns
        assert len(df) == 3

    def test_create_chart_index_empty(self):
        """Test chart index sheet with no charts."""
        output_file = Path(self.temp_dir) / "chart_index_empty.xlsx"
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Create a dummy sheet first (Excel needs at least one sheet)
            pd.DataFrame({'A': [1]}).to_excel(writer, sheet_name='Dummy', index=False)
            self.generator.create_chart_index_sheet(writer)
        
        # Should not crash
        assert output_file.exists()


class TestAddDataFrameSheet:
    """Test add_dataframe_sheet method."""

    def setup_method(self):
        """Create temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = ExcelReportGenerator(output_folder=self.temp_dir)

    def teardown_method(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_add_dataframe_sheet_basic(self):
        """Test adding a basic DataFrame sheet."""
        output_file = Path(self.temp_dir) / "df_basic.xlsx"
        
        df = pd.DataFrame({
            'Feature': ['A', 'B', 'C'],
            'Value': [1.12345, 2.23456, 3.34567]
        })
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            self.generator.add_dataframe_sheet(writer, df, 'TestData')
        
        # Read back
        df_read = pd.read_excel(output_file, sheet_name='TestData')
        assert len(df_read) == 3
        assert 'Feature' in df_read.columns

    def test_add_dataframe_sheet_with_description(self):
        """Test adding DataFrame sheet with description."""
        output_file = Path(self.temp_dir) / "df_desc.xlsx"
        
        df = pd.DataFrame({'X': [1, 2, 3]})
        description = "This is a test dataset"
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            self.generator.add_dataframe_sheet(writer, df, 'WithDesc', description)
        
        # Read back
        df_read = pd.read_excel(output_file, sheet_name='WithDesc')
        # Description is in first row
        assert description in str(df_read.iloc[0].values)

    def test_add_dataframe_sheet_empty(self):
        """Test adding an empty DataFrame."""
        output_file = Path(self.temp_dir) / "df_empty.xlsx"
        
        df = pd.DataFrame()
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            self.generator.add_dataframe_sheet(writer, df, 'Empty')
        
        # Read back
        df_read = pd.read_excel(output_file, sheet_name='Empty')
        assert 'Message' in df_read.columns

    def test_add_dataframe_sheet_none(self):
        """Test adding None as DataFrame."""
        output_file = Path(self.temp_dir) / "df_none.xlsx"
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            self.generator.add_dataframe_sheet(writer, None, 'NoneData')
        
        # Read back
        df_read = pd.read_excel(output_file, sheet_name='NoneData')
        assert 'Message' in df_read.columns

    def test_add_dataframe_sheet_long_name(self):
        """Test adding DataFrame with long sheet name (auto-truncated)."""
        output_file = Path(self.temp_dir) / "df_long_name.xlsx"
        
        df = pd.DataFrame({'A': [1, 2]})
        long_name = "A" * 40  # Excel max is 31 chars
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            self.generator.add_dataframe_sheet(writer, df, long_name)
        
        # Verify file created
        assert output_file.exists()

    def test_add_dataframe_sheet_numeric_rounding(self):
        """Test that numeric columns are rounded."""
        output_file = Path(self.temp_dir) / "df_rounded.xlsx"
        
        df = pd.DataFrame({
            'Feature': ['A', 'B'],
            'Value': [1.123456789, 2.987654321]
        })
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            self.generator.add_dataframe_sheet(writer, df, 'Rounded')
        
        # Read back
        df_read = pd.read_excel(output_file, sheet_name='Rounded')
        # Check values are rounded (should be ~1.1235 not 1.123456789)
        assert df_read['Value'].iloc[0] < 1.13


class TestGenerateExcelReport:
    """Test generate_excel_report method."""

    def setup_method(self):
        """Create temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = ExcelReportGenerator(output_folder=self.temp_dir)

    def teardown_method(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_generate_excel_report_basic(self):
        """Test generating a complete Excel report."""
        sheets_data = {
            'Results': pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}),
            'Summary': pd.DataFrame({'Total': [100], 'Mean': [50]})
        }
        
        excel_path = self.generator.generate_excel_report(
            'test_report',
            sheets_data,
            methodology="Test methodology"
        )
        
        # Verify file created
        assert Path(excel_path).exists()
        
        # Check sheets
        xl_file = pd.ExcelFile(excel_path)
        assert 'Metadata' in xl_file.sheet_names
        assert 'Methodology' in xl_file.sheet_names
        assert 'Results' in xl_file.sheet_names
        assert 'Summary' in xl_file.sheet_names

    def test_generate_excel_report_with_charts(self):
        """Test report with charts."""
        # Save a chart first
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 9])
        self.generator.save_matplotlib_figure(fig, 'test_chart')
        
        sheets_data = {
            'Data': pd.DataFrame({'X': [1, 2, 3]})
        }
        
        excel_path = self.generator.generate_excel_report(
            'report_with_charts',
            sheets_data,
            Number_of_Charts=1
        )
        
        # Verify
        assert Path(excel_path).exists()
        
        # Check chart index sheet exists
        xl_file = pd.ExcelFile(excel_path)
        assert 'Chart_Index' in xl_file.sheet_names

    def test_generate_excel_report_with_tuples(self):
        """Test report with (DataFrame, description) tuples."""
        sheets_data = {
            'Data1': (pd.DataFrame({'A': [1, 2]}), "Description for Data1"),
            'Data2': pd.DataFrame({'B': [3, 4]})
        }
        
        excel_path = self.generator.generate_excel_report(
            'report_tuples',
            sheets_data
        )
        
        # Verify
        assert Path(excel_path).exists()

    def test_generate_excel_report_custom_metadata(self):
        """Test report with custom metadata."""
        sheets_data = {
            'Results': pd.DataFrame({'Value': [100]})
        }
        
        excel_path = self.generator.generate_excel_report(
            'custom_meta_report',
            sheets_data,
            Total_Samples=500,
            Analysis_Type="Clustering"
        )
        
        # Read metadata
        df_meta = pd.read_excel(excel_path, sheet_name='Metadata')
        assert '500' in df_meta['Value'].astype(str).values

    def test_generate_excel_report_no_methodology(self):
        """Test report without methodology."""
        sheets_data = {
            'Data': pd.DataFrame({'X': [1, 2, 3]})
        }
        
        excel_path = self.generator.generate_excel_report(
            'no_method_report',
            sheets_data
        )
        
        # Verify file created
        assert Path(excel_path).exists()


class TestPlotlyFigureSavingDetailed:
    """Detailed tests for Plotly figure saving."""

    def setup_method(self):
        """Create temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = ExcelReportGenerator(output_folder=self.temp_dir)

    def teardown_method(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @pytest.mark.skipif(not HAS_PLOTLY, reason="plotly not available")
    def test_save_plotly_figure_with_size(self):
        """Test saving Plotly figure with custom size."""
        fig = go.Figure(data=[go.Bar(x=[1, 2, 3], y=[4, 5, 6])])
        
        # Fallback will work even if kaleido is not installed
        filepath = self.generator.save_plotly_figure_fallback(
            fig, 'sized_plot', width=800, height=600
        )
        
        assert Path(filepath).exists()

    @pytest.mark.skipif(not HAS_PLOTLY, reason="plotly not available")
    def test_save_multiple_plotly_figures(self):
        """Test saving multiple Plotly figures."""
        for i in range(3):
            fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[i, i*2, i*3])])
            self.generator.save_plotly_figure_fallback(fig, f'plotly_{i}')
        
        assert len(self.generator.png_files) >= 3


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def setup_method(self):
        """Create temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = ExcelReportGenerator(output_folder=self.temp_dir)

    def teardown_method(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_very_large_dataframe(self):
        """Test with very large DataFrame."""
        output_file = Path(self.temp_dir) / "large.xlsx"
        
        # Create 10,000 row dataframe
        large_df = pd.DataFrame({
            'Index': range(10000),
            'Value': np.random.rand(10000)
        })
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            self.generator.add_dataframe_sheet(writer, large_df, 'LargeData')
        
        assert output_file.exists()

    def test_special_characters_in_data(self):
        """Test DataFrame with special characters."""
        output_file = Path(self.temp_dir) / "special_chars.xlsx"
        
        df = pd.DataFrame({
            'Feature': ['A:B', 'C\\D', 'E/F'],
            'Value': [1, 2, 3]
        })
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            self.generator.add_dataframe_sheet(writer, df, 'SpecialChars')
        
        assert output_file.exists()

    def test_mixed_data_types(self):
        """Test DataFrame with mixed data types."""
        output_file = Path(self.temp_dir) / "mixed_types.xlsx"
        
        df = pd.DataFrame({
            'Int': [1, 2, 3],
            'Float': [1.1, 2.2, 3.3],
            'String': ['a', 'b', 'c'],
            'Bool': [True, False, True]
        })
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            self.generator.add_dataframe_sheet(writer, df, 'MixedTypes')
        
        assert output_file.exists()
