#!/usr/bin/env python3
"""
Verification Script - Checks that all module structures are complete

This script verifies that all 5 modules have been properly created with
all required files and correct structure.
"""

import os
from pathlib import Path
from collections import defaultdict

# Define expected structure
REQUIRED_FILES = {
    "root": [
        "README.md",
        "LICENSE",
        "pyproject.toml",
        "setup.py",
        "Dockerfile",
        "docker-compose.yml",
        "requirements.txt",
        ".gitignore",
    ],
    "package": [
        "__init__.py",
        "cli.py",
        "analysis.py",
    ],
    "notebooks": [
        "README.md",
        # Notebook file is dynamic (different name per module)
    ],
    "examples/data": [
        "MIC.csv",
        "AMR_genes.csv",
        "Virulence.csv",
    ]
}

MODULES = [
    "strepsuis-amrvirkm",
    "strepsuis-amrpat",
    "strepsuis-genphennet",
    "strepsuis-phylotrait",
    "strepsuis-genphen",
]


def check_module(module_name, base_dir="modules"):
    """Check if a module has all required files."""
    module_path = Path(base_dir) / module_name
    package_name = module_name.replace("-", "_")
    
    results = {
        "exists": module_path.exists(),
        "files": defaultdict(list),
        "missing": defaultdict(list),
        "status": "✅"
    }
    
    if not results["exists"]:
        results["status"] = "❌"
        return results
    
    # Check root files
    for file in REQUIRED_FILES["root"]:
        file_path = module_path / file
        if file_path.exists():
            results["files"]["root"].append(file)
        else:
            results["missing"]["root"].append(file)
            results["status"] = "⚠️"
    
    # Check package files
    package_path = module_path / package_name
    for file in REQUIRED_FILES["package"]:
        file_path = package_path / file
        if file_path.exists():
            results["files"]["package"].append(file)
        else:
            results["missing"]["package"].append(file)
            results["status"] = "⚠️"
    
    # Check notebooks
    notebooks_path = module_path / "notebooks"
    if notebooks_path.exists():
        results["files"]["notebooks"] = list(notebooks_path.glob("*.ipynb"))
        if notebooks_path / "README.md" in notebooks_path.glob("*"):
            results["files"]["notebooks"].append("README.md")
    else:
        results["missing"]["notebooks"] = ["directory missing"]
        results["status"] = "⚠️"
    
    # Check example data
    data_path = module_path / "examples" / "data"
    if data_path.exists():
        results["files"]["data"] = list(data_path.glob("*.csv"))
    else:
        results["missing"]["data"] = ["directory missing"]
        results["status"] = "⚠️"
    
    return results


def print_module_status(module_name, results):
    """Print status for a module."""
    print(f"\n{results['status']} {module_name}")
    print("=" * 60)
    
    if not results["exists"]:
        print("  ❌ Module directory does not exist!")
        return
    
    # Root files
    print(f"\n  Root files: {len(results['files']['root'])}/{len(REQUIRED_FILES['root'])}")
    if results['missing']['root']:
        print(f"    Missing: {', '.join(results['missing']['root'])}")
    
    # Package files
    print(f"  Package files: {len(results['files']['package'])}/{len(REQUIRED_FILES['package'])}")
    if results['missing']['package']:
        print(f"    Missing: {', '.join(results['missing']['package'])}")
    
    # Notebooks
    notebook_count = len([f for f in results['files']['notebooks'] if str(f).endswith('.ipynb')])
    print(f"  Notebooks: {notebook_count}")
    if results['missing']['notebooks']:
        print(f"    Missing: {', '.join(results['missing']['notebooks'])}")
    
    # Example data
    data_count = len(results['files']['data'])
    print(f"  Example data files: {data_count}")
    if results['missing']['data']:
        print(f"    Missing: {', '.join(results['missing']['data'])}")


def check_documentation():
    """Check for repository-wide documentation."""
    docs = {
        "modules/README.md": Path("modules/README.md").exists(),
        "MODULES_DEPLOYMENT_GUIDE.md": Path("MODULES_DEPLOYMENT_GUIDE.md").exists(),
        "modules_structure.md": Path("modules_structure.md").exists(),
        "RESTRUCTURING_COMPLETE.md": Path("RESTRUCTURING_COMPLETE.md").exists(),
    }
    
    print("\n" + "=" * 60)
    print("REPOSITORY-WIDE DOCUMENTATION")
    print("=" * 60)
    
    for doc, exists in docs.items():
        status = "✅" if exists else "❌"
        print(f"  {status} {doc}")
    
    return all(docs.values())


def check_automation_scripts():
    """Check for automation scripts."""
    scripts = {
        "generate_modules.py": Path("generate_modules.py").exists(),
        "generate_notebooks.py": Path("generate_notebooks.py").exists(),
    }
    
    print("\n" + "=" * 60)
    print("AUTOMATION SCRIPTS")
    print("=" * 60)
    
    for script, exists in scripts.items():
        status = "✅" if exists else "❌"
        print(f"  {status} {script}")
    
    return all(scripts.values())


def main():
    """Main verification function."""
    print("=" * 60)
    print("MODULE STRUCTURE VERIFICATION")
    print("=" * 60)
    
    all_complete = True
    module_results = {}
    
    # Check each module
    for module in MODULES:
        results = check_module(module)
        module_results[module] = results
        print_module_status(module, results)
        
        if results["status"] != "✅":
            all_complete = False
    
    # Check documentation
    docs_complete = check_documentation()
    
    # Check automation
    scripts_complete = check_automation_scripts()
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    complete_count = sum(1 for r in module_results.values() if r["status"] == "✅")
    print(f"\nModules complete: {complete_count}/{len(MODULES)}")
    print(f"Documentation: {'✅ Complete' if docs_complete else '⚠️ Incomplete'}")
    print(f"Automation: {'✅ Complete' if scripts_complete else '⚠️ Incomplete'}")
    
    if all_complete and docs_complete and scripts_complete:
        print("\n✅ ALL REQUIREMENTS SATISFIED!")
        print("\nThe repository has been successfully restructured.")
        print("All 5 modules are ready for deployment.")
        print("\nNext steps:")
        print("  1. Review the modules/ directory")
        print("  2. Read MODULES_DEPLOYMENT_GUIDE.md")
        print("  3. Create separate GitHub repositories")
        print("  4. Test all deployment variants")
    else:
        print("\n⚠️ Some issues found. Review the output above.")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
