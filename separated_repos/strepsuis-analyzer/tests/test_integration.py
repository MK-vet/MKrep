"""Integration tests for StrepSuisAnalyzer."""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from strepsuis_analyzer.data_validator import DataValidator
from strepsuis_analyzer.statistical_analysis import StatisticalAnalyzer
from strepsuis_analyzer.report_generator import ReportGenerator
from strepsuis_analyzer.etl_operations import ETLOperations


@pytest.mark.integration
class TestIntegration:
    """Integration tests for complete workflows."""

    def test_data_validation_and_analysis_workflow(self, sample_numeric_data):
        """Test complete workflow from validation to analysis."""
        # Validate data
        validator = DataValidator()
        is_valid, errors, warnings = validator.validate_dataframe(sample_numeric_data)
        assert is_valid

        # Perform analysis
        analyzer = StatisticalAnalyzer(random_state=42)
        corr, pval = analyzer.compute_correlation(
            sample_numeric_data["var_0"],
            sample_numeric_data["var_1"],
            method="pearson"
        )

        assert not np.isnan(corr)
        assert not np.isnan(pval)

    def test_etl_and_analysis_workflow(self, sample_numeric_data):
        """Test ETL operations followed by analysis."""
        # ETL operations
        etl = ETLOperations()
        normalized_data = etl.normalize_columns(
            sample_numeric_data,
            ["var_0", "var_1"],
            method="zscore"
        )

        # Validate normalized data
        validator = DataValidator()
        is_valid, errors, warnings = validator.validate_dataframe(normalized_data)
        assert is_valid

        # Analysis on normalized data
        analyzer = StatisticalAnalyzer(random_state=42)
        stat, pval, is_normal = analyzer.test_normality(normalized_data["var_0"])

        assert not np.isnan(stat)

    def test_analysis_and_reporting_workflow(self, sample_numeric_data):
        """Test analysis followed by report generation."""
        # Perform analysis
        analyzer = StatisticalAnalyzer(random_state=42)
        
        stats = {
            "mean_var0": sample_numeric_data["var_0"].mean(),
            "std_var0": sample_numeric_data["var_0"].std(),
            "count": len(sample_numeric_data),
        }

        # Generate report
        report = ReportGenerator()
        report.add_dataframe("Data", sample_numeric_data)
        report.add_statistics("Statistics", stats)

        # Export to temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
            report.export_to_excel(tmp.name)
            assert Path(tmp.name).exists()
            Path(tmp.name).unlink()

    def test_complete_pipeline(self, sample_binary_data, sample_numeric_data):
        """Test complete analysis pipeline."""
        # 1. Validate data
        validator = DataValidator()
        is_valid_binary, _, _ = validator.validate_binary_matrix(sample_binary_data)
        is_valid_numeric, _, _ = validator.validate_numeric_matrix(sample_numeric_data)

        assert is_valid_binary
        assert is_valid_numeric

        # 2. ETL operations
        etl = ETLOperations()
        
        # Reset indices to make them align
        binary_df = sample_binary_data.reset_index()
        numeric_df = sample_numeric_data.reset_index()
        
        # Create a common merge key
        binary_df['merge_key'] = range(len(binary_df))
        numeric_df['merge_key'] = range(len(numeric_df))
        
        merged_data = etl.merge_dataframes(
            binary_df,
            numeric_df,
            on="merge_key",
            how="inner"
        )

        assert len(merged_data) > 0

        # 3. Statistical analysis
        analyzer = StatisticalAnalyzer(random_state=42)
        
        # Correlation between binary and numeric
        corr, pval = analyzer.compute_correlation(
            merged_data["gene_0"],
            merged_data["var_0"],
            method="spearman"
        )

        # 4. Generate report
        report = ReportGenerator()
        report.add_dataframe("Merged Data", merged_data)
        report.add_statistics("Correlation", {
            "correlation": corr,
            "p_value": pval
        })

        assert len(report.report_data) == 2
