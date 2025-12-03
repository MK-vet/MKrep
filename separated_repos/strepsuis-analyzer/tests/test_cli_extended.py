"""
Extended Tests for CLI Module

Tests CLI argument parsing, file validation, execution paths, and error handling.
"""

import pytest
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import pandas as pd

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from strepsuis_analyzer import cli


class TestCLIArgumentParsing:
    """Test command-line argument parsing."""

    def test_parse_args_minimal(self):
        """Test parsing minimal required arguments."""
        test_args = [
            'strepsuis-analyzer',
            '--data', 'data1.csv',
            '--output', '/tmp/output'
        ]
        
        with patch.object(sys, 'argv', test_args):
            parser = cli.create_parser()
            args = parser.parse_args(test_args[1:])
            
            assert args.data == ['data1.csv']
            assert args.output == '/tmp/output'

    def test_parse_args_multiple_data_files(self):
        """Test parsing multiple data files."""
        test_args = [
            'strepsuis-analyzer',
            '--data', 'amr.csv', 'virulence.csv', 'genes.csv',
            '--output', '/tmp/output'
        ]
        
        with patch.object(sys, 'argv', test_args):
            parser = cli.create_parser()
            args = parser.parse_args(test_args[1:])
            
            assert args.data == ['amr.csv', 'virulence.csv', 'genes.csv']

    def test_parse_args_with_tree(self):
        """Test parsing with phylogenetic tree argument."""
        test_args = [
            'strepsuis-analyzer',
            '--data', 'data.csv',
            '--tree', 'tree.newick',
            '--output', '/tmp/output'
        ]
        
        parser = cli.create_parser()
        args = parser.parse_args(test_args[1:])
        
        assert args.tree == 'tree.newick'

    def test_parse_args_with_clusters(self):
        """Test parsing with custom number of clusters."""
        test_args = [
            'strepsuis-analyzer',
            '--data', 'data.csv',
            '--clusters', '5',
            '--output', '/tmp/output'
        ]
        
        parser = cli.create_parser()
        args = parser.parse_args(test_args[1:])
        
        assert args.clusters == 5

    def test_parse_args_with_random_state(self):
        """Test parsing with custom random state."""
        test_args = [
            'strepsuis-analyzer',
            '--data', 'data.csv',
            '--seed', '123',
            '--output', '/tmp/output'
        ]
        
        parser = cli.create_parser()
        args = parser.parse_args(test_args[1:])
        
        assert args.seed == 123


class TestCLIExecution:
    """Test CLI execution paths."""

    def setup_method(self):
        """Create temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create sample data file
        self.data_file = Path(self.temp_dir) / 'test_data.csv'
        data = pd.DataFrame({
            'Strain_ID': [f'Strain_{i}' for i in range(30)],
            'Trait_0': [1, 0] * 15,
            'Trait_1': [0, 1] * 15,
            'Trait_2': [1, 1, 0, 0] * 7 + [1, 0],
            'Trait_3': [0, 0, 1, 1] * 7 + [0, 1],
        })
        data.to_csv(self.data_file, index=False)

    def teardown_method(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_cli_basic_execution(self):
        """Test basic CLI execution."""
        output_dir = Path(self.temp_dir) / 'output'
        
        test_args = [
            'strepsuis-analyzer',
            '--data', str(self.data_file),
            '--output', str(output_dir),
            '--clusters', '2'
        ]
        
        with patch.object(sys, 'argv', test_args):
            # Run CLI
            try:
                cli.main()
                
                # Check outputs were created
                assert output_dir.exists(), "Output directory should be created"
                
                # Check for expected output files
                csv_files = list(output_dir.glob('*.csv'))
                assert len(csv_files) > 0, "Should create CSV output files"
                
            except SystemExit as e:
                # CLI may exit normally with code 0
                if e.code != 0:
                    raise

    def test_cli_with_invalid_data_file(self):
        """Test CLI with non-existent data file."""
        output_dir = Path(self.temp_dir) / 'output'
        
        test_args = [
            'strepsuis-analyzer',
            '--data', 'nonexistent.csv',
            '--output', str(output_dir)
        ]
        
        with patch.object(sys, 'argv', test_args):
            # Should handle missing file (may exit or return error code)
            try:
                result = cli.main()
                # If it returns, should be error code
                assert result != 0
            except (SystemExit, ValueError, FileNotFoundError):
                # These are all acceptable ways to handle missing file
                pass


class TestCLIErrorHandling:
    """Test error handling in CLI."""

    def test_missing_required_argument_data(self):
        """Test missing --data argument."""
        test_args = [
            'strepsuis-analyzer',
            '--output', '/tmp/output'
        ]
        
        parser = cli.create_parser()
        
        with pytest.raises(SystemExit):
            parser.parse_args(test_args[1:])

    def test_negative_clusters(self):
        """Test negative number of clusters."""
        test_args = [
            'strepsuis-analyzer',
            '--data', 'data.csv',
            '--output', '/tmp/output',
            '--clusters', '-1'
        ]
        
        parser = cli.create_parser()
        args = parser.parse_args(test_args[1:])
        
        # Parser accepts it, but analyzer should reject
        assert args.clusters == -1


class TestCLIHelpers:
    """Test CLI helper functions."""

    def test_create_parser(self):
        """Test parser creation."""
        parser = cli.create_parser()
        
        assert parser is not None
        assert parser.description is not None

    def test_parser_help_text(self):
        """Test that parser has help text."""
        parser = cli.create_parser()
        help_text = parser.format_help()
        
        assert '--data' in help_text
        assert '--output' in help_text
        assert '--tree' in help_text
        assert '--clusters' in help_text  # Not --n-clusters
        assert '--seed' in help_text  # Not --random-state
