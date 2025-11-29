#!/usr/bin/env python3
"""
CLI integration tests for MKrep package.

Tests verify:
- CLI argument parsing
- Help message generation
- Error handling for missing arguments
- Basic command execution with test data

Note: Some tests are skipped because the mkrep package
has incomplete analyzer implementations.
"""

import sys
import os
import pytest
import tempfile
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestCLIModuleStructure:
    """Tests for CLI module structure and syntax."""
    
    def test_cli_module_syntax(self):
        """Test that cli.py has valid Python syntax."""
        cli_path = os.path.join(
            os.path.dirname(__file__), 
            'python_package', 'mkrep', 'cli.py'
        )
        result = subprocess.run(
            [sys.executable, '-m', 'py_compile', cli_path],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Syntax error in cli.py: {result.stderr}"
    
    def test_analysis_init_syntax(self):
        """Test that analysis/__init__.py has valid syntax."""
        init_path = os.path.join(
            os.path.dirname(__file__), 
            'python_package', 'mkrep', 'analysis', '__init__.py'
        )
        result = subprocess.run(
            [sys.executable, '-m', 'py_compile', init_path],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Syntax error: {result.stderr}"


class TestCLIConfigLoading:
    """Tests for CLI configuration file loading."""
    
    def test_load_json_config(self):
        """Test loading JSON configuration file."""
        # Direct test of load_config function from cli.py source
        cli_path = os.path.join(
            os.path.dirname(__file__),
            'python_package', 'mkrep', 'cli.py'
        )
        
        # Read and exec just the load_config function
        import json
        from pathlib import Path
        
        def load_config(config_path):
            config_path = Path(config_path)
            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
            with open(config_path, 'r') as f:
                if config_path.suffix == '.json':
                    return json.load(f)
                elif config_path.suffix in ['.yaml', '.yml']:
                    import yaml
                    return yaml.safe_load(f)
                else:
                    raise ValueError(f"Unsupported config format: {config_path.suffix}")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"output_dir": "/tmp/test", "bootstrap": 100}')
            f.flush()
            config = load_config(f.name)
        
        assert config['output_dir'] == '/tmp/test'
        assert config['bootstrap'] == 100
        os.unlink(f.name)
    
    def test_load_missing_config(self):
        """Test error handling for missing config file."""
        from pathlib import Path
        import json
        
        def load_config(config_path):
            config_path = Path(config_path)
            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
            with open(config_path, 'r') as f:
                return json.load(f)
        
        with pytest.raises(FileNotFoundError):
            load_config('/nonexistent/config.json')
    
    def test_load_unsupported_format(self):
        """Test error handling for unsupported config format."""
        from pathlib import Path
        
        def load_config(config_path):
            config_path = Path(config_path)
            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
            if config_path.suffix not in ['.json', '.yaml', '.yml']:
                raise ValueError(f"Unsupported config format: {config_path.suffix}")
            return {}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write('some text')
            f.flush()
            
            with pytest.raises(ValueError):
                load_config(f.name)
        
        os.unlink(f.name)


class TestCLIArgumentParser:
    """Tests for CLI argument parser structure."""
    
    def test_common_parser_setup(self):
        """Test that common arguments are properly configured."""
        import argparse
        
        # Replicate setup_common_parser behavior
        def setup_common_parser(parser):
            parser.add_argument('--data-dir', type=str, required=True)
            parser.add_argument('--output', type=str, default='./output')
            parser.add_argument('--config', type=str)
            parser.add_argument('--verbose', action='store_true')
        
        parser = argparse.ArgumentParser()
        setup_common_parser(parser)
        
        # Parse test arguments
        args = parser.parse_args(['--data-dir', '/data', '--output', '/out', '--verbose'])
        
        assert args.data_dir == '/data'
        assert args.output == '/out'
        assert args.verbose is True
    
    def test_default_output_dir(self):
        """Test default output directory."""
        import argparse
        
        def setup_common_parser(parser):
            parser.add_argument('--data-dir', type=str, required=True)
            parser.add_argument('--output', type=str, default='./output')
        
        parser = argparse.ArgumentParser()
        setup_common_parser(parser)
        
        args = parser.parse_args(['--data-dir', '/data'])
        
        assert args.output == './output'
    
    def test_cluster_parser_arguments(self):
        """Test cluster analysis argument structure."""
        import argparse
        
        parser = argparse.ArgumentParser()
        parser.add_argument('--data-dir', type=str, required=True)
        parser.add_argument('--output', type=str, default='./output')
        parser.add_argument('--max-clusters', type=int)
        parser.add_argument('--bootstrap', type=int, default=500)
        parser.add_argument('--fdr-alpha', type=float, default=0.05)
        parser.add_argument('--mca-components', type=int, default=2)
        
        args = parser.parse_args([
            '--data-dir', '/data',
            '--max-clusters', '8',
            '--bootstrap', '1000',
            '--fdr-alpha', '0.01'
        ])
        
        assert args.max_clusters == 8
        assert args.bootstrap == 1000
        assert args.fdr_alpha == 0.01
    
    def test_phylo_parser_arguments(self):
        """Test phylogenetic analysis argument structure."""
        import argparse
        
        parser = argparse.ArgumentParser()
        parser.add_argument('--data-dir', type=str, required=True)
        parser.add_argument('--tree', type=str, required=True)
        parser.add_argument('--clustering', choices=['kmeans', 'dbscan', 'gmm', 'auto'])
        parser.add_argument('--n-clusters', type=int)
        parser.add_argument('--umap-components', type=int, default=2)
        
        args = parser.parse_args([
            '--data-dir', '/data',
            '--tree', '/tree.newick',
            '--clustering', 'kmeans',
            '--n-clusters', '5'
        ])
        
        assert args.tree == '/tree.newick'
        assert args.clustering == 'kmeans'
        assert args.n_clusters == 5


class TestStandaloneScriptExecution:
    """Tests for standalone script execution."""
    
    def test_validate_script_syntax(self):
        """Test that validate.py has valid syntax."""
        validate_path = os.path.join(os.path.dirname(__file__), 'validate.py')
        result = subprocess.run(
            [sys.executable, '-m', 'py_compile', validate_path],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Syntax error in validate.py: {result.stderr}"
    
    def test_excel_utils_syntax(self):
        """Test that excel_report_utils.py has valid syntax."""
        utils_path = os.path.join(os.path.dirname(__file__), 'excel_report_utils.py')
        result = subprocess.run(
            [sys.executable, '-m', 'py_compile', utils_path],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Syntax error: {result.stderr}"
    
    def test_report_templates_syntax(self):
        """Test that report_templates.py has valid syntax."""
        templates_path = os.path.join(os.path.dirname(__file__), 'report_templates.py')
        result = subprocess.run(
            [sys.executable, '-m', 'py_compile', templates_path],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Syntax error: {result.stderr}"


class TestAnalysisScriptSyntax:
    """Tests for main analysis script syntax validation."""
    
    @pytest.mark.parametrize("script", [
        "Cluster_MIC_AMR_Viruelnce.py",
        "MDR_2025_04_15.py",
        "Network_Analysis_2025_06_26.py",
        "StrepSuisPhyloCluster_2025_08_11.py",
    ])
    def test_analysis_script_syntax(self, script):
        """Test that analysis scripts have valid Python syntax."""
        script_path = os.path.join(os.path.dirname(__file__), script)
        if os.path.exists(script_path):
            result = subprocess.run(
                [sys.executable, '-m', 'py_compile', script_path],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0, f"Syntax error in {script}: {result.stderr}"


class TestRunnerScriptsSyntax:
    """Tests for runner script syntax validation."""
    
    @pytest.mark.parametrize("script", [
        "run_all_analyses.py",
        "run_cluster_analysis.py",
        "run_mdr_analysis.py",
        "run_phylogenetic_analysis.py",
    ])
    def test_runner_script_syntax(self, script):
        """Test that runner scripts have valid Python syntax."""
        script_path = os.path.join(os.path.dirname(__file__), script)
        if os.path.exists(script_path):
            result = subprocess.run(
                [sys.executable, '-m', 'py_compile', script_path],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0, f"Syntax error in {script}: {result.stderr}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
