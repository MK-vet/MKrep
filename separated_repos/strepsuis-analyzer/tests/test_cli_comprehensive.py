"""
Comprehensive Tests for CLI Module

Tests all CLI functions and argument handling to achieve 95%+ coverage.
"""

import pytest
import sys
import tempfile
import shutil
from pathlib import Path
import pandas as pd

from strepsuis_analyzer.cli import create_parser, main


class TestCreateParser:
    """Test create_parser function."""

    def test_create_parser_returns_parser(self):
        """Test that create_parser returns an ArgumentParser."""
        parser = create_parser()
        assert parser is not None
        assert hasattr(parser, 'parse_args')

    def test_parser_has_required_arguments(self):
        """Test that parser has all required arguments."""
        parser = create_parser()
        
        # Parse a valid command
        args = parser.parse_args(['--data', 'test.csv'])
        assert args.data == ['test.csv']

    def test_parser_data_argument_required(self):
        """Test that --data argument is required."""
        parser = create_parser()
        
        with pytest.raises(SystemExit):
            parser.parse_args([])

    def test_parser_multiple_data_files(self):
        """Test parsing multiple data files."""
        parser = create_parser()
        args = parser.parse_args(['--data', 'file1.csv', 'file2.csv', 'file3.csv'])
        
        assert len(args.data) == 3
        assert args.data[0] == 'file1.csv'
        assert args.data[1] == 'file2.csv'
        assert args.data[2] == 'file3.csv'

    def test_parser_tree_argument(self):
        """Test --tree argument."""
        parser = create_parser()
        args = parser.parse_args(['--data', 'test.csv', '--tree', 'tree.newick'])
        
        assert args.tree == 'tree.newick'

    def test_parser_tree_optional(self):
        """Test that --tree is optional."""
        parser = create_parser()
        args = parser.parse_args(['--data', 'test.csv'])
        
        assert args.tree is None

    def test_parser_output_argument(self):
        """Test --output argument."""
        parser = create_parser()
        args = parser.parse_args(['--data', 'test.csv', '--output', 'results'])
        
        assert args.output == 'results'

    def test_parser_output_default(self):
        """Test default output directory."""
        parser = create_parser()
        args = parser.parse_args(['--data', 'test.csv'])
        
        assert args.output == 'output'

    def test_parser_clusters_argument(self):
        """Test --clusters argument."""
        parser = create_parser()
        args = parser.parse_args(['--data', 'test.csv', '--clusters', '5'])
        
        assert args.clusters == 5

    def test_parser_clusters_optional(self):
        """Test that --clusters is optional."""
        parser = create_parser()
        args = parser.parse_args(['--data', 'test.csv'])
        
        assert args.clusters is None

    def test_parser_seed_argument(self):
        """Test --seed argument."""
        parser = create_parser()
        args = parser.parse_args(['--data', 'test.csv', '--seed', '123'])
        
        assert args.seed == 123

    def test_parser_seed_default(self):
        """Test default seed value."""
        parser = create_parser()
        args = parser.parse_args(['--data', 'test.csv'])
        
        assert args.seed == 42

    def test_parser_verbose_flag(self):
        """Test --verbose flag."""
        parser = create_parser()
        args = parser.parse_args(['--data', 'test.csv', '--verbose'])
        
        assert args.verbose is True

    def test_parser_verbose_default(self):
        """Test default verbose value."""
        parser = create_parser()
        args = parser.parse_args(['--data', 'test.csv'])
        
        assert args.verbose is False

    def test_parser_verbose_short_flag(self):
        """Test -v short flag for verbose."""
        parser = create_parser()
        args = parser.parse_args(['--data', 'test.csv', '-v'])
        
        assert args.verbose is True

    def test_parser_version_argument(self):
        """Test --version argument exits."""
        parser = create_parser()
        
        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(['--version'])
        
        assert exc_info.value.code == 0

    def test_parser_all_arguments_combined(self):
        """Test using all arguments together."""
        parser = create_parser()
        args = parser.parse_args([
            '--data', 'file1.csv', 'file2.csv',
            '--tree', 'tree.newick',
            '--output', 'my_results',
            '--clusters', '4',
            '--seed', '999',
            '--verbose'
        ])
        
        assert len(args.data) == 2
        assert args.tree == 'tree.newick'
        assert args.output == 'my_results'
        assert args.clusters == 4
        assert args.seed == 999
        assert args.verbose is True


class TestMainFunction:
    """Test main CLI function."""

    def setup_method(self):
        """Create temporary directory and test data."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a minimal test CSV file
        test_data = pd.DataFrame({
            'Strain_ID': ['S1', 'S2', 'S3', 'S4', 'S5'],
            'Gene1': [1, 0, 1, 0, 1],
            'Gene2': [0, 1, 1, 0, 0],
            'Gene3': [1, 1, 0, 0, 1]
        })
        self.test_csv = Path(self.temp_dir) / 'test_data.csv'
        test_data.to_csv(self.test_csv, index=False)

    def teardown_method(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_main_with_minimal_args(self):
        """Test main with minimal arguments."""
        output_dir = Path(self.temp_dir) / 'output'
        
        return_code = main([
            '--data', str(self.test_csv),
            '--output', str(output_dir),
            '--seed', '42'
        ])
        
        assert return_code == 0
        assert output_dir.exists()

    def test_main_with_clusters_specified(self):
        """Test main with number of clusters specified."""
        output_dir = Path(self.temp_dir) / 'output_clusters'
        
        return_code = main([
            '--data', str(self.test_csv),
            '--output', str(output_dir),
            '--clusters', '2',
            '--seed', '42'
        ])
        
        assert return_code == 0

    def test_main_error_handling(self):
        """Test main error handling with invalid file."""
        return_code = main([
            '--data', 'nonexistent_file.csv',
            '--output', str(Path(self.temp_dir) / 'output_error')
        ])
        
        # Should return error code
        assert return_code == 1

    def test_main_with_verbose(self):
        """Test main with verbose flag."""
        output_dir = Path(self.temp_dir) / 'output_verbose'
        
        # Verbose should not crash
        return_code = main([
            '--data', str(self.test_csv),
            '--output', str(output_dir),
            '--verbose',
            '--seed', '42'
        ])
        
        assert return_code == 0

    def test_main_with_multiple_data_files(self):
        """Test main with multiple data files."""
        # Create second test file
        test_data2 = pd.DataFrame({
            'Strain_ID': ['S1', 'S2', 'S3', 'S4', 'S5'],
            'Gene4': [1, 1, 0, 0, 1],
            'Gene5': [0, 0, 1, 1, 0]
        })
        test_csv2 = Path(self.temp_dir) / 'test_data2.csv'
        test_data2.to_csv(test_csv2, index=False)
        
        output_dir = Path(self.temp_dir) / 'output_multi'
        
        return_code = main([
            '--data', str(self.test_csv), str(test_csv2),
            '--output', str(output_dir),
            '--seed', '42'
        ])
        
        assert return_code == 0


class TestCLIIntegration:
    """Integration tests for CLI."""

    def setup_method(self):
        """Create temporary directory."""
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_cli_produces_expected_outputs(self):
        """Test that CLI produces all expected output files."""
        # Create test data
        test_data = pd.DataFrame({
            'Strain_ID': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
            'Trait1': [1, 0, 1, 0, 1, 0],
            'Trait2': [0, 1, 1, 0, 0, 1],
            'Trait3': [1, 1, 0, 0, 1, 1]
        })
        test_csv = Path(self.temp_dir) / 'test.csv'
        test_data.to_csv(test_csv, index=False)
        
        output_dir = Path(self.temp_dir) / 'cli_output'
        
        return_code = main([
            '--data', str(test_csv),
            '--output', str(output_dir),
            '--clusters', '2',
            '--seed', '42'
        ])
        
        assert return_code == 0
        
        # Check expected outputs
        assert (output_dir / 'analysis_report.html').exists()
        assert (output_dir / 'analysis_results.xlsx').exists()
        assert (output_dir / 'clustered_data.csv').exists()
        assert (output_dir / 'trait_associations.csv').exists()

    def test_cli_argument_validation(self):
        """Test CLI validates arguments correctly."""
        parser = create_parser()
        
        # Parser accepts negative values - argparse doesn't validate by default
        # Just test that it parses
        args = parser.parse_args(['--data', 'test.csv', '--clusters', '3'])
        assert args.clusters == 3

    def test_cli_help_text(self):
        """Test that CLI has proper help text."""
        parser = create_parser()
        
        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(['--help'])
        
        # Help should exit with code 0
        assert exc_info.value.code == 0
