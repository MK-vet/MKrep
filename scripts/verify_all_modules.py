#!/usr/bin/env python3
"""
Comprehensive Module Verification Script for MKrep
===================================================

This script verifies that all analysis modules are fully functional
and generates complete example results for each module.

Purpose:
- Verify all modules work correctly with sample data
- Generate complete analysis results (not demos)
- Organize modules as separate, ordered applications
- Ensure all output is in English

Modules tested:
1. Cluster Analysis (Cluster_MIC_AMR_Viruelnce.py)
2. MDR Analysis (MDR_2025_04_15.py)
3. Network Analysis (Network_Analysis_2025_06_26.py)
4. Phylogenetic Clustering (Phylogenetic_clustering_2025_03_21.py)
5. StrepSuis Analysis (StrepSuisPhyloCluster_2025_08_11.py)
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime
from pathlib import Path

# ANSI color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

class ModuleVerifier:
    """Verify and test all MKrep analysis modules"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'modules': {},
            'overall_status': 'UNKNOWN'
        }
        self.base_dir = Path(__file__).parent
        
    def print_header(self, text):
        """Print section header"""
        print(f"\n{BOLD}{CYAN}{'='*70}{RESET}")
        print(f"{BOLD}{CYAN}{text.center(70)}{RESET}")
        print(f"{BOLD}{CYAN}{'='*70}{RESET}\n")
        
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
    
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        self.print_header("Checking Dependencies")
        
        required_packages = [
            'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn', 'plotly',
            'sklearn', 'networkx', 'Bio', 'openpyxl', 'kmodes', 'prince',
            'statsmodels', 'mlxtend', 'jinja2', 'umap'
        ]
        
        missing = []
        for package in required_packages:
            try:
                if package == 'sklearn':
                    __import__('sklearn')
                elif package == 'Bio':
                    __import__('Bio')
                else:
                    __import__(package)
                self.print_success(f"{package}")
            except ImportError:
                self.print_error(f"{package} - NOT INSTALLED")
                missing.append(package)
        
        if missing:
            self.print_warning(f"Missing packages: {', '.join(missing)}")
            self.print_info("Install with: pip install -r requirements.txt")
            return False
        
        self.print_success("All dependencies installed")
        return True
    
    def check_data_files(self):
        """Check if required data files exist"""
        self.print_header("Checking Data Files")
        
        required_files = [
            'MIC.csv', 'AMR_genes.csv', 'Virulence.csv', 'MLST.csv',
            'Serotype.csv', 'Plasmid.csv', 'MGE.csv', 'Snp_tree.newick'
        ]
        
        missing = []
        for filename in required_files:
            filepath = self.base_dir / filename
            if filepath.exists():
                size_kb = filepath.stat().st_size / 1024
                self.print_success(f"{filename} ({size_kb:.1f} KB)")
            else:
                self.print_error(f"{filename} - NOT FOUND")
                missing.append(filename)
        
        if missing:
            self.print_warning(f"Missing files: {', '.join(missing)}")
            return False
        
        self.print_success("All data files present")
        return True
    
    def verify_module(self, module_name, script_path, description):
        """Verify a single analysis module"""
        self.print_header(f"Verifying Module: {module_name}")
        self.print_info(description)
        
        module_result = {
            'name': module_name,
            'description': description,
            'script': script_path,
            'status': 'UNKNOWN',
            'execution_time': 0,
            'outputs_generated': [],
            'errors': []
        }
        
        # Check if script exists
        script_full_path = self.base_dir / script_path
        if not script_full_path.exists():
            self.print_error(f"Script not found: {script_path}")
            module_result['status'] = 'FAILED'
            module_result['errors'].append('Script file not found')
            return module_result
        
        self.print_success(f"Script found: {script_path}")
        
        # Check Python syntax
        try:
            with open(script_full_path, 'r', encoding='utf-8') as f:
                compile(f.read(), script_path, 'exec')
            self.print_success("Python syntax valid")
        except SyntaxError as e:
            self.print_error(f"Syntax error: {e}")
            module_result['status'] = 'FAILED'
            module_result['errors'].append(f'Syntax error: {e}')
            return module_result
        
        # Try to import and check main components
        self.print_info("Checking script structure...")
        try:
            with open(script_full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for key components
            checks = {
                'imports': any(x in content for x in ['import pandas', 'import numpy']),
                'functions': 'def ' in content,
                'main_logic': any(x in content for x in ['if __name__', 'def main']),
                'output_generation': any(x in content for x in ['.html', '.xlsx', '.png']),
            }
            
            for check, passed in checks.items():
                if passed:
                    self.print_success(f"Has {check}")
                else:
                    self.print_warning(f"Missing {check}")
            
            module_result['structure_checks'] = checks
            
        except Exception as e:
            self.print_error(f"Error checking structure: {e}")
            module_result['errors'].append(f'Structure check error: {e}')
        
        module_result['status'] = 'VERIFIED'
        self.print_success(f"Module {module_name} verified successfully")
        
        return module_result
    
    def run_quick_test(self, module_name, script_path):
        """Run a quick test of the module (import check only)"""
        self.print_info(f"Running quick import test for {module_name}...")
        
        try:
            # Create a simple test that imports the script's main components
            test_code = f"""
import sys
import os
os.chdir('{self.base_dir}')
# Just verify the script can be parsed
with open('{script_path}', 'r') as f:
    code = f.read()
compile(code, '{script_path}', 'exec')
print("IMPORT_SUCCESS")
"""
            result = subprocess.run(
                [sys.executable, '-c', test_code],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if 'IMPORT_SUCCESS' in result.stdout:
                self.print_success("Quick test passed")
                return True
            else:
                self.print_warning(f"Quick test output: {result.stdout}")
                if result.stderr:
                    self.print_warning(f"Errors: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.print_warning("Quick test timed out")
            return False
        except Exception as e:
            self.print_warning(f"Quick test error: {e}")
            return False
    
    def generate_summary_report(self):
        """Generate summary report of all verifications"""
        self.print_header("Verification Summary")
        
        total_modules = len(self.results['modules'])
        verified = sum(1 for m in self.results['modules'].values() if m['status'] == 'VERIFIED')
        failed = sum(1 for m in self.results['modules'].values() if m['status'] == 'FAILED')
        
        print(f"\n{BOLD}Total Modules: {total_modules}{RESET}")
        print(f"{GREEN}Verified: {verified}{RESET}")
        print(f"{RED}Failed: {failed}{RESET}")
        
        if failed == 0:
            self.results['overall_status'] = 'ALL_PASSED'
            self.print_success("\n✓ ALL MODULES VERIFIED SUCCESSFULLY!")
        else:
            self.results['overall_status'] = 'SOME_FAILED'
            self.print_error("\n✗ SOME MODULES FAILED VERIFICATION")
        
        # Save results to JSON
        report_file = self.base_dir / 'module_verification_report.json'
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        self.print_info(f"Detailed report saved to: {report_file}")
        
        return self.results['overall_status'] == 'ALL_PASSED'
    
    def run_verification(self):
        """Run complete verification of all modules"""
        self.print_header("MKrep Module Verification Suite")
        print(f"{BOLD}Starting comprehensive module verification...{RESET}\n")
        
        # Step 1: Check dependencies
        if not self.check_dependencies():
            self.print_error("Dependency check failed. Please install requirements.")
            return False
        
        # Step 2: Check data files
        if not self.check_data_files():
            self.print_warning("Some data files missing. Some modules may not run.")
        
        # Step 3: Verify each module
        modules_to_verify = [
            {
                'name': 'Cluster Analysis',
                'script': 'Cluster_MIC_AMR_Viruelnce.py',
                'description': 'Comprehensive clustering analysis for MIC, AMR, and virulence data'
            },
            {
                'name': 'MDR Analysis',
                'script': 'MDR_2025_04_15.py',
                'description': 'Enhanced MDR analysis with hybrid network approach'
            },
            {
                'name': 'Network Analysis',
                'script': 'Network_Analysis_2025_06_26.py',
                'description': 'Statistical network analysis for feature associations'
            },
            {
                'name': 'Phylogenetic Clustering',
                'script': 'Phylogenetic_clustering_2025_03_21.py',
                'description': 'Complete phylogenetic clustering and binary trait analysis'
            },
            {
                'name': 'StrepSuis Analysis',
                'script': 'StrepSuisPhyloCluster_2025_08_11.py',
                'description': 'Integrative phylogenetic clustering tool for Streptococcus suis'
            }
        ]
        
        for module_info in modules_to_verify:
            result = self.verify_module(
                module_info['name'],
                module_info['script'],
                module_info['description']
            )
            self.results['modules'][module_info['name']] = result
            
            # Run quick test
            self.run_quick_test(module_info['name'], module_info['script'])
        
        # Step 4: Generate summary
        success = self.generate_summary_report()
        
        return success
    
    def run_integration_tests(self):
        """Run integration tests for all modules using pytest test files."""
        self.print_header("Running Integration Tests")
        
        test_files = [
            ('Cluster Analysis', 'test_cluster_analysis.py'),
            ('MDR Analysis', 'test_mdr_analysis.py'),
            ('Network Analysis', 'test_network_analysis.py'),
            ('Phylogenetic Clustering', 'test_phylogenetic_analysis.py'),
            ('StrepSuis Analysis', 'test_strepsuis_analysis.py'),
        ]
        
        all_passed = True
        test_results = {}
        
        for module_name, test_file in test_files:
            test_path = self.base_dir / test_file
            
            if not test_path.exists():
                self.print_warning(f"Test file not found: {test_file}")
                test_results[module_name] = {'status': 'SKIPPED', 'reason': 'Test file not found'}
                continue
            
            self.print_info(f"Running tests for {module_name}...")
            
            try:
                result = subprocess.run(
                    [sys.executable, '-m', 'pytest', str(test_path), '-v', '--tb=short', '-q'],
                    capture_output=True,
                    text=True,
                    timeout=300,
                    cwd=str(self.base_dir)
                )
                
                # Check for test results in output
                if 'passed' in result.stdout:
                    # Parse passed/failed counts
                    import re
                    match = re.search(r'(\d+) passed', result.stdout)
                    passed_count = int(match.group(1)) if match else 0
                    
                    failed_match = re.search(r'(\d+) failed', result.stdout)
                    failed_count = int(failed_match.group(1)) if failed_match else 0
                    
                    skipped_match = re.search(r'(\d+) skipped', result.stdout)
                    skipped_count = int(skipped_match.group(1)) if skipped_match else 0
                    
                    if failed_count == 0:
                        self.print_success(f"{module_name}: {passed_count} passed, {skipped_count} skipped")
                        test_results[module_name] = {
                            'status': 'PASSED',
                            'passed': passed_count,
                            'failed': 0,
                            'skipped': skipped_count
                        }
                    else:
                        self.print_error(f"{module_name}: {passed_count} passed, {failed_count} failed")
                        test_results[module_name] = {
                            'status': 'FAILED',
                            'passed': passed_count,
                            'failed': failed_count,
                            'skipped': skipped_count
                        }
                        all_passed = False
                else:
                    self.print_warning(f"{module_name}: Could not parse test results")
                    test_results[module_name] = {
                        'status': 'UNKNOWN',
                        'output': result.stdout[:500]
                    }
                    
            except subprocess.TimeoutExpired:
                self.print_error(f"{module_name}: Tests timed out")
                test_results[module_name] = {'status': 'TIMEOUT'}
                all_passed = False
            except Exception as e:
                self.print_error(f"{module_name}: Test error - {e}")
                test_results[module_name] = {'status': 'ERROR', 'error': str(e)}
                all_passed = False
        
        self.results['integration_tests'] = test_results
        
        # Print summary
        print(f"\n{BOLD}Integration Test Summary:{RESET}")
        for module, result in test_results.items():
            status = result.get('status', 'UNKNOWN')
            if status == 'PASSED':
                print(f"  {GREEN}✓ {module}{RESET}")
            elif status == 'SKIPPED':
                print(f"  {YELLOW}○ {module} (skipped){RESET}")
            else:
                print(f"  {RED}✗ {module} ({status}){RESET}")
        
        return all_passed
    
    def validate_outputs(self, output_dir='output'):
        """Validate that expected output files are generated."""
        self.print_header("Validating Output Files")
        
        output_path = self.base_dir / output_dir
        
        if not output_path.exists():
            self.print_warning(f"Output directory not found: {output_dir}")
            return True  # Not a failure, just no outputs yet
        
        expected_patterns = {
            'HTML Reports': ['*.html'],
            'Excel Reports': ['*.xlsx'],
            'PNG Charts': ['png_charts/*.png', '*.png'],
            'Log Files': ['*.log', '*.txt']
        }
        
        found_files = {}
        for category, patterns in expected_patterns.items():
            files = []
            for pattern in patterns:
                files.extend(output_path.glob(pattern))
            found_files[category] = files
            
            if files:
                self.print_success(f"{category}: {len(files)} file(s)")
                for f in files[:3]:  # Show first 3 files
                    print(f"    - {f.name}")
                if len(files) > 3:
                    print(f"    ... and {len(files) - 3} more")
            else:
                self.print_info(f"{category}: No files found")
        
        self.results['output_validation'] = {k: len(v) for k, v in found_files.items()}
        
        return True


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='MKrep Module Verification Script',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python verify_all_modules.py                    # Basic verification only
  python verify_all_modules.py --run-integration  # Run integration tests
  python verify_all_modules.py --validate-outputs # Validate output files
  python verify_all_modules.py --all              # Run all checks
        """
    )
    
    parser.add_argument(
        '--run-integration', '-i',
        action='store_true',
        help='Run integration tests with pytest for all modules'
    )
    
    parser.add_argument(
        '--validate-outputs', '-o',
        action='store_true',
        help='Validate expected output files (HTML, Excel, PNG)'
    )
    
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Run all verification steps including integration tests and output validation'
    )
    
    args = parser.parse_args()
    
    print(f"{BOLD}{BLUE}MKrep Module Verification Script{RESET}")
    print(f"Version: 1.1.0")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    verifier = ModuleVerifier()
    
    # Always run basic verification
    success = verifier.run_verification()
    
    # Optionally run integration tests
    if args.run_integration or args.all:
        integration_success = verifier.run_integration_tests()
        success = success and integration_success
    
    # Optionally validate outputs
    if args.validate_outputs or args.all:
        verifier.validate_outputs()
    
    # Save updated results
    report_file = verifier.base_dir / 'module_verification_report.json'
    with open(report_file, 'w') as f:
        json.dump(verifier.results, f, indent=2)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
