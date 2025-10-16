#!/usr/bin/env python3
"""
Validation script for MKrep deployment options.

This script checks:
1. Docker files are present and valid
2. Colab notebooks are present
3. Python package structure is correct
4. Documentation is complete
"""

import os
import sys
import json
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description} missing: {filepath}")
        return False

def check_docker_files():
    """Verify Docker deployment files."""
    print("\n=== Docker Deployment Files ===")
    checks = [
        ("Dockerfile", "Docker image definition"),
        ("docker-compose.yml", "Docker Compose configuration"),
        (".dockerignore", "Docker ignore file"),
        ("DOCKER_DEPLOYMENT.md", "Docker deployment guide"),
    ]
    
    results = []
    for file, desc in checks:
        results.append(check_file_exists(file, desc))
    
    return all(results)

def check_colab_notebooks():
    """Verify Colab notebooks."""
    print("\n=== Google Colab Notebooks ===")
    notebooks = [
        "colab_notebooks/Interactive_Analysis_Colab.ipynb",
        "colab_notebooks/Cluster_Analysis_Colab.ipynb",
        "colab_notebooks/MDR_Analysis_Colab.ipynb",
        "colab_notebooks/Network_Analysis_Colab.ipynb",
        "colab_notebooks/Phylogenetic_Clustering_Colab.ipynb",
        "colab_notebooks/StrepSuis_Analysis_Colab.ipynb",
    ]
    
    results = []
    for notebook in notebooks:
        results.append(check_file_exists(notebook, "Notebook"))
    
    # Check for README
    results.append(check_file_exists("colab_notebooks/README.md", "Colab README"))
    results.append(check_file_exists("colab_notebooks/INTERACTIVE_NOTEBOOK_GUIDE.md", "Interactive Guide"))
    
    return all(results)

def check_python_scripts():
    """Verify main Python analysis scripts."""
    print("\n=== Main Analysis Scripts ===")
    scripts = [
        "Cluster_MIC_AMR_Viruelnce.py",
        "MDR_2025_04_15.py",
        "Network_Analysis_2025_06_26.py",
        "Phylgenetic_clustering_2025_03_21.py",
        "StrepSuisPhyloCluster_2025_08_11.py",
    ]
    
    results = []
    for script in scripts:
        results.append(check_file_exists(script, "Script"))
    
    return all(results)

def check_python_package():
    """Verify Python package structure."""
    print("\n=== Python Package Structure ===")
    package_files = [
        "python_package/pyproject.toml",
        "python_package/README.md",
        "python_package/mkrep/__init__.py",
        "python_package/mkrep/cli.py",
        "python_package/mkrep/analysis/__init__.py",
        "python_package/mkrep/utils/__init__.py",
    ]
    
    results = []
    for file in package_files:
        results.append(check_file_exists(file, "Package file"))
    
    return all(results)

def check_documentation():
    """Verify documentation files."""
    print("\n=== Documentation Files ===")
    docs = [
        ("README.md", "Main README"),
        ("USER_GUIDE.md", "User Guide"),
        ("INSTALLATION.md", "Installation Guide"),
        ("DOCKER_DEPLOYMENT.md", "Docker Guide"),
        ("INTERPRETATION_GUIDE.md", "Results Interpretation"),
        ("requirements.txt", "Python requirements"),
    ]
    
    results = []
    for file, desc in docs:
        results.append(check_file_exists(file, desc))
    
    return all(results)

def check_utilities():
    """Verify utility files."""
    print("\n=== Utility Files ===")
    utils = [
        "excel_report_utils.py",
        "report_templates.py",
    ]
    
    results = []
    for util in utils:
        results.append(check_file_exists(util, "Utility"))
    
    return all(results)

def validate_dockerfile_syntax():
    """Check Dockerfile for basic syntax."""
    print("\n=== Dockerfile Syntax Check ===")
    try:
        with open("Dockerfile", "r") as f:
            content = f.read()
            
        # Check for required directives
        required = ["FROM", "WORKDIR", "COPY", "RUN", "CMD"]
        missing = []
        
        for directive in required:
            if directive not in content:
                missing.append(directive)
        
        if missing:
            print(f"✗ Missing Dockerfile directives: {', '.join(missing)}")
            return False
        else:
            print("✓ Dockerfile has all required directives")
            return True
    except Exception as e:
        print(f"✗ Error checking Dockerfile: {e}")
        return False

def validate_docker_compose():
    """Check docker-compose.yml for basic syntax."""
    print("\n=== Docker Compose Syntax Check ===")
    try:
        with open("docker-compose.yml", "r") as f:
            content = f.read()
        
        # Check for required keys
        required = ["version:", "services:", "build:", "volumes:"]
        missing = []
        
        for key in required:
            if key not in content:
                missing.append(key)
        
        if missing:
            print(f"✗ Missing docker-compose.yml keys: {', '.join(missing)}")
            return False
        else:
            print("✓ docker-compose.yml has all required keys")
            return True
    except Exception as e:
        print(f"✗ Error checking docker-compose.yml: {e}")
        return False

def validate_colab_notebook(notebook_path):
    """Check if a Colab notebook is valid JSON."""
    try:
        with open(notebook_path, "r") as f:
            data = json.load(f)
        
        # Check for required notebook structure
        if "cells" not in data:
            print(f"✗ {notebook_path}: Missing 'cells' key")
            return False
        
        if "metadata" not in data:
            print(f"✗ {notebook_path}: Missing 'metadata' key")
            return False
        
        return True
    except json.JSONDecodeError as e:
        print(f"✗ {notebook_path}: Invalid JSON - {e}")
        return False
    except Exception as e:
        print(f"✗ {notebook_path}: Error - {e}")
        return False

def validate_all_notebooks():
    """Validate all Colab notebooks."""
    print("\n=== Colab Notebook Validation ===")
    notebooks = [
        "colab_notebooks/Interactive_Analysis_Colab.ipynb",
        "colab_notebooks/Cluster_Analysis_Colab.ipynb",
        "colab_notebooks/MDR_Analysis_Colab.ipynb",
        "colab_notebooks/Network_Analysis_Colab.ipynb",
        "colab_notebooks/Phylogenetic_Clustering_Colab.ipynb",
        "colab_notebooks/StrepSuis_Analysis_Colab.ipynb",
    ]
    
    results = []
    for notebook in notebooks:
        if os.path.exists(notebook):
            if validate_colab_notebook(notebook):
                print(f"✓ {notebook}: Valid")
                results.append(True)
            else:
                results.append(False)
        else:
            print(f"✗ {notebook}: Not found")
            results.append(False)
    
    return all(results)

def main():
    """Run all validation checks."""
    print("=" * 60)
    print("MKrep Deployment Validation")
    print("=" * 60)
    
    # Change to repository root
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    results = {
        "Docker Files": check_docker_files(),
        "Colab Notebooks": check_colab_notebooks(),
        "Python Scripts": check_python_scripts(),
        "Python Package": check_python_package(),
        "Documentation": check_documentation(),
        "Utilities": check_utilities(),
        "Dockerfile Syntax": validate_dockerfile_syntax(),
        "Docker Compose Syntax": validate_docker_compose(),
        "Notebook Validation": validate_all_notebooks(),
    }
    
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL CHECKS PASSED!")
        print("=" * 60)
        print("\nMKrep is ready for deployment:")
        print("  • Docker: docker build -t mkrep:latest .")
        print("  • Docker Compose: docker-compose up mkrep")
        print("  • Colab: Open Interactive_Analysis_Colab.ipynb")
        return 0
    else:
        print("⚠️ SOME CHECKS FAILED")
        print("=" * 60)
        print("\nPlease review the errors above and fix them.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
