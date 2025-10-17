#!/usr/bin/env python3
"""
MKrep Unified Analysis Runner
==============================

This script provides a unified interface to run all MKrep analysis modules
as separate, ordered applications with complete results generation.

Each module is a fully functional, production-ready application that:
- Processes real data (not demos)
- Generates complete analysis results
- Produces publication-quality visualizations
- Creates comprehensive reports in HTML and Excel formats

Available Analysis Modules:
1. Cluster Analysis - K-Modes clustering with MCA and feature importance
2. MDR Analysis - Multi-drug resistance patterns and co-occurrence
3. Network Analysis - Statistical network analysis of gene-phenotype associations
4. Phylogenetic Clustering - Tree-aware clustering with evolutionary metrics
5. StrepSuis Analysis - Specialized analysis for Streptococcus suis

Usage:
    python run_all_analyses.py --module <module_name> [options]
    python run_all_analyses.py --all
    python run_all_analyses.py --list
"""

import os
import sys
import argparse
import subprocess
import time
from datetime import datetime
from pathlib import Path
import json

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'


class AnalysisRunner:
    """Unified runner for all MKrep analysis modules"""
    
    # Module configurations
    MODULES = {
        'cluster': {
            'name': 'Cluster Analysis',
            'script': 'Cluster_MIC_AMR_Viruelnce.py',
            'description': 'Comprehensive clustering analysis for MIC, AMR, and virulence data',
            'required_files': ['MIC.csv', 'AMR_genes.csv', 'Virulence.csv'],
            'optional_files': ['MLST.csv', 'Serotype.csv', 'Plasmid.csv', 'MGE.csv'],
            'output_folder': 'clustering_analysis_results',
            'estimated_time': '5-10 minutes'
        },
        'mdr': {
            'name': 'MDR Analysis',
            'script': 'MDR_2025_04_15.py',
            'description': 'Enhanced MDR analysis with hybrid network approach',
            'required_files': ['MIC.csv', 'AMR_genes.csv'],
            'optional_files': ['Virulence.csv', 'MLST.csv'],
            'output_folder': 'mdr_analysis_results',
            'estimated_time': '5-10 minutes'
        },
        'network': {
            'name': 'Network Analysis',
            'script': 'Network_Analysis_2025_06_26.py',
            'description': 'Statistical network analysis for feature associations',
            'required_files': ['MIC.csv', 'AMR_genes.csv', 'Virulence.csv'],
            'optional_files': ['MLST.csv', 'Serotype.csv', 'MGE.csv'],
            'output_folder': 'network_analysis_results',
            'estimated_time': '3-5 minutes'
        },
        'phylo': {
            'name': 'Phylogenetic Clustering',
            'script': 'Phylgenetic_clustering_2025_03_21.py',
            'description': 'Complete phylogenetic clustering and binary trait analysis',
            'required_files': ['Snp_tree.newick', 'AMR_genes.csv', 'Virulence.csv'],
            'optional_files': ['MIC.csv', 'MLST.csv', 'Serotype.csv'],
            'output_folder': 'phylo_clustering_results',
            'estimated_time': '7-12 minutes'
        },
        'strepsuis': {
            'name': 'StrepSuis Analysis',
            'script': 'StrepSuisPhyloCluster_2025_08_11.py',
            'description': 'Integrative phylogenetic clustering for Streptococcus suis',
            'required_files': ['Snp_tree.newick', 'AMR_genes.csv', 'Virulence.csv'],
            'optional_files': ['MIC.csv', 'MLST.csv', 'Serotype.csv', 'Plasmid.csv'],
            'output_folder': 'strepsuis_analysis_results',
            'estimated_time': '7-12 minutes'
        }
    }
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.results = {}
        
    def print_header(self, text):
        """Print formatted header"""
        print(f"\n{BOLD}{CYAN}{'='*80}{RESET}")
        print(f"{BOLD}{CYAN}{text.center(80)}{RESET}")
        print(f"{BOLD}{CYAN}{'='*80}{RESET}\n")
        
    def print_success(self, text):
        """Print success message"""
        print(f"{GREEN}✓ {text}{RESET}")
        
    def print_error(self, text):
        """Print error message"""
        print(f"{RED}✗ {text}{RESET}")
        
    def print_info(self, text):
        """Print info message"""
        print(f"{BLUE}ℹ {text}{RESET}")
        
    def print_warning(self, text):
        """Print warning message"""
        print(f"{YELLOW}⚠ {text}{RESET}")
    
    def list_modules(self):
        """List all available analysis modules"""
        self.print_header("Available Analysis Modules")
        
        for key, module in self.MODULES.items():
            print(f"\n{BOLD}{BLUE}{key}{RESET}: {BOLD}{module['name']}{RESET}")
            print(f"  Description: {module['description']}")
            print(f"  Script: {module['script']}")
            print(f"  Estimated Time: {module['estimated_time']}")
            print(f"  Required Files: {', '.join(module['required_files'])}")
            if module['optional_files']:
                print(f"  Optional Files: {', '.join(module['optional_files'])}")
    
    def check_requirements(self, module_key):
        """Check if requirements for a module are met"""
        module = self.MODULES[module_key]
        
        self.print_info(f"Checking requirements for {module['name']}...")
        
        # Check script exists
        script_path = self.base_dir / module['script']
        if not script_path.exists():
            self.print_error(f"Script not found: {module['script']}")
            return False
        self.print_success(f"Script found: {module['script']}")
        
        # Check required files
        missing_required = []
        for filename in module['required_files']:
            filepath = self.base_dir / filename
            if filepath.exists():
                self.print_success(f"Required file: {filename}")
            else:
                self.print_error(f"Missing required file: {filename}")
                missing_required.append(filename)
        
        if missing_required:
            self.print_error(f"Cannot run {module['name']} - missing required files")
            return False
        
        # Check optional files
        for filename in module['optional_files']:
            filepath = self.base_dir / filename
            if filepath.exists():
                self.print_success(f"Optional file: {filename}")
            else:
                self.print_warning(f"Optional file not found: {filename}")
        
        return True
    
    def run_module(self, module_key, timeout=None):
        """Run a single analysis module"""
        module = self.MODULES[module_key]
        
        self.print_header(f"Running: {module['name']}")
        self.print_info(module['description'])
        print()
        
        # Check requirements
        if not self.check_requirements(module_key):
            return False
        
        # Prepare to run
        script_path = self.base_dir / module['script']
        start_time = time.time()
        
        self.print_info(f"Starting analysis (estimated time: {module['estimated_time']})...")
        self.print_info(f"Running: python {module['script']}")
        print()
        
        try:
            # Run the script
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(self.base_dir),
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            execution_time = time.time() - start_time
            
            # Check result
            if result.returncode == 0:
                self.print_success(f"Analysis completed successfully in {execution_time:.1f} seconds")
                
                # Check for output files
                output_folder = self.base_dir / module['output_folder']
                if output_folder.exists():
                    outputs = list(output_folder.glob('*'))
                    self.print_success(f"Generated {len(outputs)} output files in {module['output_folder']}/")
                    
                    # List key outputs
                    html_files = list(output_folder.glob('*.html'))
                    excel_files = list(output_folder.glob('*.xlsx'))
                    png_folder = output_folder / 'png_charts'
                    
                    if html_files:
                        self.print_info(f"  HTML Reports: {len(html_files)}")
                    if excel_files:
                        self.print_info(f"  Excel Reports: {len(excel_files)}")
                    if png_folder.exists():
                        png_files = list(png_folder.glob('*.png'))
                        self.print_info(f"  PNG Charts: {len(png_files)}")
                
                self.results[module_key] = {
                    'status': 'SUCCESS',
                    'execution_time': execution_time,
                    'timestamp': datetime.now().isoformat()
                }
                return True
                
            else:
                self.print_error(f"Analysis failed with return code {result.returncode}")
                if result.stderr:
                    print(f"\n{RED}Error output:{RESET}")
                    print(result.stderr[:1000])  # Print first 1000 chars
                
                self.results[module_key] = {
                    'status': 'FAILED',
                    'error': result.stderr[:500] if result.stderr else 'Unknown error',
                    'execution_time': execution_time,
                    'timestamp': datetime.now().isoformat()
                }
                return False
                
        except subprocess.TimeoutExpired:
            self.print_error(f"Analysis timed out after {timeout} seconds")
            self.results[module_key] = {
                'status': 'TIMEOUT',
                'execution_time': timeout,
                'timestamp': datetime.now().isoformat()
            }
            return False
            
        except Exception as e:
            self.print_error(f"Error running analysis: {e}")
            self.results[module_key] = {
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            return False
    
    def run_all(self, timeout_per_module=900):
        """Run all analysis modules"""
        self.print_header("Running All Analysis Modules")
        
        total_modules = len(self.MODULES)
        successful = 0
        
        for i, (key, module) in enumerate(self.MODULES.items(), 1):
            print(f"\n{BOLD}[{i}/{total_modules}] {module['name']}{RESET}")
            
            if self.run_module(key, timeout=timeout_per_module):
                successful += 1
        
        # Print summary
        self.print_header("Analysis Summary")
        print(f"\n{BOLD}Total Modules: {total_modules}{RESET}")
        print(f"{GREEN}Successful: {successful}{RESET}")
        print(f"{RED}Failed: {total_modules - successful}{RESET}\n")
        
        # Save results
        results_file = self.base_dir / 'analysis_run_results.json'
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        self.print_info(f"Results saved to: {results_file}")
        
        return successful == total_modules
    
    def generate_summary_report(self):
        """Generate a summary report of all analyses"""
        self.print_header("Generating Summary Report")
        
        report_content = []
        report_content.append("# MKrep Analysis Results Summary\n")
        report_content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for key, result in self.results.items():
            module = self.MODULES[key]
            report_content.append(f"## {module['name']}\n")
            report_content.append(f"- **Status**: {result['status']}\n")
            report_content.append(f"- **Execution Time**: {result.get('execution_time', 'N/A')} seconds\n")
            report_content.append(f"- **Output Folder**: {module['output_folder']}/\n")
            
            if result['status'] == 'SUCCESS':
                output_folder = self.base_dir / module['output_folder']
                if output_folder.exists():
                    html_files = list(output_folder.glob('*.html'))
                    excel_files = list(output_folder.glob('*.xlsx'))
                    
                    if html_files:
                        report_content.append(f"- **HTML Reports**: {len(html_files)}\n")
                    if excel_files:
                        report_content.append(f"- **Excel Reports**: {len(excel_files)}\n")
            
            report_content.append("\n")
        
        # Save report
        report_file = self.base_dir / 'ANALYSIS_SUMMARY.md'
        with open(report_file, 'w') as f:
            f.writelines(report_content)
        
        self.print_success(f"Summary report saved to: {report_file}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='MKrep Unified Analysis Runner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_all_analyses.py --list
  python run_all_analyses.py --module cluster
  python run_all_analyses.py --all
  python run_all_analyses.py --module mdr --timeout 600
        """
    )
    
    parser.add_argument(
        '--module', '-m',
        choices=['cluster', 'mdr', 'network', 'phylo', 'strepsuis'],
        help='Run specific analysis module'
    )
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Run all analysis modules'
    )
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all available modules'
    )
    parser.add_argument(
        '--timeout', '-t',
        type=int,
        default=900,
        help='Timeout per module in seconds (default: 900)'
    )
    
    args = parser.parse_args()
    
    runner = AnalysisRunner()
    
    # Print banner
    print(f"\n{BOLD}{BLUE}{'='*80}{RESET}")
    print(f"{BOLD}{BLUE}{'MKrep Unified Analysis Runner'.center(80)}{RESET}")
    print(f"{BOLD}{BLUE}{'Production-Ready Bioinformatics Analysis Suite'.center(80)}{RESET}")
    print(f"{BOLD}{BLUE}{'='*80}{RESET}\n")
    
    if args.list:
        runner.list_modules()
        return 0
    
    elif args.module:
        success = runner.run_module(args.module, timeout=args.timeout)
        return 0 if success else 1
    
    elif args.all:
        success = runner.run_all(timeout_per_module=args.timeout)
        runner.generate_summary_report()
        return 0 if success else 1
    
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
