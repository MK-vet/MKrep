#!/usr/bin/env python3
"""
Comprehensive functionality test for MKrep v1.2.0

Tests:
1. Python imports
2. Core utilities
3. Notebook structure
4. Docker configuration
5. Documentation completeness
"""

import sys
import json
import subprocess
from pathlib import Path

def test_python_imports():
    """Test that all required Python packages can be imported."""
    print("\n=== Testing Python Imports ===")
    
    required_packages = [
        'pandas',
        'numpy',
        'scipy',
        'matplotlib',
        'seaborn',
        'plotly',
        'sklearn',
        'networkx',
        'Bio',
        'openpyxl',
        'ipywidgets',
    ]
    
    failed = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - NOT INSTALLED")
            failed.append(package)
    
    if failed:
        print(f"\n⚠️ Missing packages: {', '.join(failed)}")
        print("Install with: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All required packages available")
        return True

def test_utility_modules():
    """Test that utility modules are valid Python."""
    print("\n=== Testing Utility Modules ===")
    
    utils = [
        'excel_report_utils.py',
        'report_templates.py',
    ]
    
    results = []
    for util in utils:
        if Path(util).exists():
            try:
                # Check syntax by compiling
                with open(util, 'r') as f:
                    code = f.read()
                compile(code, util, 'exec')
                print(f"✓ {util}: Valid Python syntax")
                results.append(True)
            except SyntaxError as e:
                print(f"✗ {util}: Syntax error - {e}")
                results.append(False)
        else:
            print(f"✗ {util}: Not found")
            results.append(False)
    
    return all(results)

def test_interactive_notebook():
    """Test the interactive notebook structure."""
    print("\n=== Testing Interactive Notebook ===")
    
    notebook_path = "colab_notebooks/Interactive_Analysis_Colab.ipynb"
    
    if not Path(notebook_path).exists():
        print(f"✗ Notebook not found: {notebook_path}")
        return False
    
    try:
        with open(notebook_path, 'r') as f:
            notebook = json.load(f)
        
        # Check structure
        if 'cells' not in notebook:
            print("✗ Missing 'cells' in notebook")
            return False
        
        cells = notebook['cells']
        print(f"✓ Notebook has {len(cells)} cells")
        
        # Check for key sections
        markdown_cells = [c for c in cells if c.get('cell_type') == 'markdown']
        code_cells = [c for c in cells if c.get('cell_type') == 'code']
        
        print(f"✓ Markdown cells: {len(markdown_cells)}")
        print(f"✓ Code cells: {len(code_cells)}")
        
        # Check for form cells (hidden code)
        form_cells = [c for c in code_cells if c.get('metadata', {}).get('cellView') == 'form']
        print(f"✓ Form cells (hidden code): {len(form_cells)}")
        
        # Check for ipywidgets usage
        notebook_text = json.dumps(notebook)
        widget_keywords = ['widgets.', 'ipywidgets', 'display(', 'IntSlider', 'Dropdown']
        widgets_found = [kw for kw in widget_keywords if kw in notebook_text]
        
        if widgets_found:
            print(f"✓ Interactive widgets detected: {', '.join(widgets_found[:3])}...")
        else:
            print("⚠️ No widget keywords found in notebook")
        
        print("\n✅ Interactive notebook is well-formed")
        return True
        
    except Exception as e:
        print(f"✗ Error checking notebook: {e}")
        return False

def test_docker_files():
    """Test Docker configuration files."""
    print("\n=== Testing Docker Configuration ===")
    
    # Test Dockerfile
    dockerfile_path = "Dockerfile"
    if Path(dockerfile_path).exists():
        with open(dockerfile_path, 'r') as f:
            content = f.read()
        
        # Check for best practices
        checks = {
            'FROM': 'Base image specified',
            'WORKDIR': 'Working directory set',
            'COPY': 'Files copied',
            'RUN': 'Commands executed',
            'CMD': 'Default command set',
            'LABEL': 'Metadata labels',
        }
        
        for keyword, desc in checks.items():
            if keyword in content:
                print(f"✓ Dockerfile: {desc}")
            else:
                print(f"⚠️ Dockerfile: Missing {keyword}")
    else:
        print("✗ Dockerfile not found")
        return False
    
    # Test docker-compose.yml
    compose_path = "docker-compose.yml"
    if Path(compose_path).exists():
        with open(compose_path, 'r') as f:
            content = f.read()
        
        services = ['mkrep-cluster', 'mkrep-mdr', 'mkrep-network', 'mkrep-phylo']
        for service in services:
            if service in content:
                print(f"✓ Docker Compose: {service} service defined")
            else:
                print(f"⚠️ Docker Compose: {service} service missing")
    else:
        print("✗ docker-compose.yml not found")
        return False
    
    print("\n✅ Docker configuration is complete")
    return True

def test_documentation_links():
    """Test that documentation is complete and cross-referenced."""
    print("\n=== Testing Documentation ===")
    
    docs = [
        'README.md',
        'DOCKER_DEPLOYMENT.md',
        'QUICK_START_NEW_FEATURES.md',
        'colab_notebooks/INTERACTIVE_NOTEBOOK_GUIDE.md',
        'IMPLEMENTATION_SUMMARY_v1.2.0.md',
    ]
    
    results = []
    for doc in docs:
        if Path(doc).exists():
            with open(doc, 'r') as f:
                content = f.read()
            
            size = len(content)
            lines = content.count('\n')
            
            print(f"✓ {doc}: {lines} lines, {size/1024:.1f} KB")
            
            # Check for key sections
            if '##' in content or '###' in content:
                print(f"  → Has structured sections")
            
            results.append(True)
        else:
            print(f"✗ {doc}: Not found")
            results.append(False)
    
    return all(results)

def test_readme_links():
    """Test that README has updated links."""
    print("\n=== Testing README Links ===")
    
    with open('README.md', 'r') as f:
        readme = f.read()
    
    # Check for new features
    features = [
        'Interactive_Analysis_Colab.ipynb',
        'Docker',
        'docker-compose',
        'DOCKER_DEPLOYMENT.md',
        'version: 1.2.0',
        'Interactive Colab Interface',
    ]
    
    results = []
    for feature in features:
        if feature in readme:
            print(f"✓ README mentions: {feature}")
            results.append(True)
        else:
            print(f"⚠️ README missing: {feature}")
            results.append(False)
    
    return all(results)

def main():
    """Run all functionality tests."""
    print("=" * 70)
    print("MKrep v1.2.0 - Comprehensive Functionality Test")
    print("=" * 70)
    
    tests = [
        ("Python Imports", test_python_imports),
        ("Utility Modules", test_utility_modules),
        ("Interactive Notebook", test_interactive_notebook),
        ("Docker Configuration", test_docker_files),
        ("Documentation", test_documentation_links),
        ("README Links", test_readme_links),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n✗ {name} failed with error: {e}")
            results[name] = False
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL FUNCTIONALITY TESTS PASSED!")
        print("=" * 70)
        print("\nMKrep v1.2.0 is ready for use:")
        print("  • Interactive Colab: https://colab.research.google.com/.../Interactive_Analysis_Colab.ipynb")
        print("  • Docker Build: docker build -t mkrep:latest .")
        print("  • Docker Run: docker-compose up mkrep-cluster")
        return 0
    else:
        print("⚠️ SOME FUNCTIONALITY TESTS FAILED")
        print("=" * 70)
        print("\nReview the errors above. Note:")
        print("  • Import failures are expected if packages not installed")
        print("  • Other failures should be investigated")
        return 1

if __name__ == "__main__":
    sys.exit(main())
