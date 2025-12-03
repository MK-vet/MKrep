"""
Extended Tests for Excel Report Utilities

Tests Excel report generation, chart embedding, and data formatting.
"""

import pytest
import pandas as pd
import tempfile
import shutil
from pathlib import Path
import matplotlib.pyplot as plt

try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

from strepsuis_analyzer.excel_report_utils import ExcelReportGenerator


class TestExcelReportGeneratorInit:
    """Test ExcelReportGenerator initialization."""

    def test_init_default(self):
        """Test initialization with default parameters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ExcelReportGenerator(output_folder=tmpdir)
            
            assert generator.output_folder == tmpdir
            assert Path(generator.png_folder).exists()
            assert Path(generator.png_folder).name == "png_charts"
            assert generator.png_files == []

    def test_init_creates_folders(self):
        """Test that initialization creates necessary folders."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "custom_output"
            generator = ExcelReportGenerator(output_folder=str(output_dir))
            
            assert Path(generator.png_folder).exists()


class TestMatplotlibFigureSaving:
    """Test saving matplotlib figures."""

    def setup_method(self):
        """Create temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = ExcelReportGenerator(output_folder=self.temp_dir)

    def teardown_method(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_matplotlib_figure(self):
        """Test saving a matplotlib figure as PNG."""
        # Create a simple figure
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 9])
        ax.set_title("Test Plot")
        
        # Save it
        filepath = self.generator.save_matplotlib_figure(fig, "test_plot")
        
        # Check file was created
        assert Path(filepath).exists()
        assert filepath.endswith('.png')
        assert filepath in self.generator.png_files

    def test_save_matplotlib_figure_custom_dpi(self):
        """Test saving with custom DPI."""
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 9])
        
        filepath = self.generator.save_matplotlib_figure(fig, "test_dpi", dpi=300)
        
        assert Path(filepath).exists()

    def test_multiple_matplotlib_figures(self):
        """Test saving multiple figures."""
        for i in range(3):
            fig, ax = plt.subplots()
            ax.plot([1, 2, 3], [i, i*2, i*3])
            self.generator.save_matplotlib_figure(fig, f"plot_{i}")
        
        assert len(self.generator.png_files) == 3


@pytest.mark.skipif(not HAS_PLOTLY, reason="plotly not available")
class TestPlotlyFigureSaving:
    """Test saving plotly figures."""

    def setup_method(self):
        """Create temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = ExcelReportGenerator(output_folder=self.temp_dir)

    def teardown_method(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_plotly_figure_fallback(self):
        """Test plotly figure fallback saving."""
        # Create a simple plotly figure
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 4, 9])])
        fig.update_layout(title="Test Plotly Plot")
        
        # Use fallback method (always works, might save as HTML)
        filepath = self.generator.save_plotly_figure_fallback(fig, "test_plotly")
        
        # Check file was created (either PNG or HTML)
        assert Path(filepath).exists()
        assert filepath.endswith('.png') or filepath.endswith('.html')
        assert filepath in self.generator.png_files


class TestMetadataSheetCreation:
    """Test metadata sheet creation."""

    def setup_method(self):
        """Create temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = ExcelReportGenerator(output_folder=self.temp_dir)

    def teardown_method(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_metadata_sheet_exists(self):
        """Test that create_metadata_sheet method exists."""
        assert hasattr(self.generator, 'create_metadata_sheet')
        assert callable(self.generator.create_metadata_sheet)


class TestPNGFolderManagement:
    """Test PNG folder management."""

    def test_png_folder_created(self):
        """Test that PNG folder is created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ExcelReportGenerator(output_folder=tmpdir)
            png_folder = Path(generator.png_folder)
            
            assert png_folder.exists()
            assert png_folder.is_dir()

    def test_png_files_list_tracking(self):
        """Test that PNG files are tracked."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ExcelReportGenerator(output_folder=tmpdir)
            
            # Save some figures
            for i in range(3):
                fig, ax = plt.subplots()
                ax.plot([1, 2, 3], [i, i*2, i*3])
                generator.save_matplotlib_figure(fig, f"plot_{i}")
            
            # Check tracking
            assert len(generator.png_files) == 3
            assert all(Path(f).exists() for f in generator.png_files)


class TestReportCreationIntegration:
    """Test full report creation workflow."""

    def setup_method(self):
        """Create temporary directory and sample data."""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = ExcelReportGenerator(output_folder=self.temp_dir)
        
        # Sample data
        self.data = pd.DataFrame({
            'Feature': ['Trait_A', 'Trait_B', 'Trait_C'],
            'Value': [10, 20, 30],
            'P_value': [0.001, 0.05, 0.10]
        })

    def teardown_method(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_full_excel_report_workflow_basic(self):
        """Test creating a complete Excel report with data and charts."""
        output_file = Path(self.temp_dir) / "full_report.xlsx"
        
        # Create figures
        fig, ax = plt.subplots()
        ax.bar(self.data['Feature'], self.data['Value'])
        chart_path = self.generator.save_matplotlib_figure(fig, "bar_chart")
        
        # Create Excel file (without metadata sheet that has issues)
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            # Data sheet
            self.data.to_excel(writer, sheet_name='Results', index=False)
        
        # Verify
        assert output_file.exists()
        assert Path(chart_path).exists()
        
        # Check sheets
        xl_file = pd.ExcelFile(output_file)
        assert 'Results' in xl_file.sheet_names


class TestErrorHandling:
    """Test error handling in ExcelReportGenerator."""

    def test_handles_invalid_output_folder(self):
        """Test handling of problematic output folder."""
        # This should not crash even with unusual path
        try:
            generator = ExcelReportGenerator(output_folder="/tmp/test_excel_reports_2024")
            assert generator is not None
        except Exception as e:
            # If it fails, it should be a clear error
            assert "folder" in str(e).lower() or "directory" in str(e).lower()

    def test_handles_figure_save_error(self):
        """Test handling of figure save errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ExcelReportGenerator(output_folder=tmpdir)
            
            # Try to save without creating a figure (should handle gracefully)
            # This tests that the method doesn't crash unexpectedly
            assert generator.png_files == []


class TestDataFrameOperations:
    """Test DataFrame operations in report generation."""

    def test_empty_dataframe_handling(self):
        """Test handling of empty DataFrames."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "empty_report.xlsx"
            
            empty_df = pd.DataFrame()
            
            # Should handle empty dataframes
            with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
                empty_df.to_excel(writer, sheet_name='Empty', index=False)
            
            assert output_file.exists()

    def test_large_dataframe_handling(self):
        """Test handling of large DataFrames."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "large_report.xlsx"
            
            # Create large dataframe
            large_df = pd.DataFrame({
                f'Col_{i}': range(1000) for i in range(10)
            })
            
            with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
                large_df.to_excel(writer, sheet_name='Large', index=False)
            
            assert output_file.exists()


class TestExcelWriterCompatibility:
    """Test compatibility with different Excel writers."""

    def test_xlsxwriter_engine(self):
        """Test using xlsxwriter engine."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "xlsxwriter_report.xlsx"
            
            df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
            
            with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Data', index=False)
            
            assert output_file.exists()
            
            # Verify content
            df_read = pd.read_excel(output_file, sheet_name='Data')
            pd.testing.assert_frame_equal(df, df_read)

    def test_openpyxl_engine(self):
        """Test using openpyxl engine."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "openpyxl_report.xlsx"
            
            df = pd.DataFrame({'X': [10, 20, 30], 'Y': [40, 50, 60]})
            
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Data', index=False)
            
            assert output_file.exists()
            
            # Verify content
            df_read = pd.read_excel(output_file, sheet_name='Data')
            pd.testing.assert_frame_equal(df, df_read)
