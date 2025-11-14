#!/usr/bin/env python3
"""
Verification script for separated module repositories.
Checks that all required files are present and properly structured.
"""

import os
from pathlib import Path
from typing import List, Tuple

# Module configurations
MODULES = {
    "strepsuis-amrvirkm": {
        "package": "strepsuis_amrvirkm",
        "cli": "strepsuis-amrvirkm",
        "notebook": "AMRVirKM_Analysis.ipynb",
        "requires_tree": False
    },
    "strepsuis-amrpat": {
        "package": "strepsuis_amrpat",
        "cli": "strepsuis-amrpat",
        "notebook": "AMRPat_Analysis.ipynb",
        "requires_tree": False
    },
    "strepsuis-genphennet": {
        "package": "strepsuis_genphennet",
        "cli": "strepsuis-genphennet",
        "notebook": "GenPhenNet_Analysis.ipynb",
        "requires_tree": False
    },
    "strepsuis-phylotrait": {
        "package": "strepsuis_phylotrait",
        "cli": "strepsuis-phylotrait",
        "notebook": "PhyloTrait_Analysis.ipynb",
        "requires_tree": True
    },
    "strepsuis-genphen": {
        "package": "strepsuis_genphen",
        "cli": "strepsuis-genphen",
        "notebook": "GenPhen_Analysis.ipynb",
        "requires_tree": True
    }
}

# Required files for each module
REQUIRED_ROOT_FILES = [
    "README.md",
    "LICENSE",
    ".gitignore",
    "pyproject.toml",
    "requirements.txt",
    "Dockerfile",
    "docker-compose.yml"
]

REQUIRED_PACKAGE_FILES = [
    "__init__.py",
    "config.py",
    "cli.py",
    "analyzer.py"
]

REQUIRED_EXAMPLE_FILES = [
    "README.md",
    "MIC.csv",
    "AMR_genes.csv",
    "Virulence.csv"
]


def check_module(module_name: str, config: dict, base_dir: Path) -> Tuple[bool, List[str]]:
    """
    Check if a module has all required files.
    
    Returns:
        Tuple of (success: bool, errors: List[str])
    """
    errors = []
    module_dir = base_dir / module_name
    
    # Check module directory exists
    if not module_dir.exists():
        return False, [f"Module directory not found: {module_dir}"]
    
    # Check root files
    for filename in REQUIRED_ROOT_FILES:
        filepath = module_dir / filename
        if not filepath.exists():
            errors.append(f"Missing root file: {filename}")
    
    # Check package directory
    package_dir = module_dir / config["package"]
    if not package_dir.exists():
        errors.append(f"Missing package directory: {config['package']}/")
    else:
        # Check package files
        for filename in REQUIRED_PACKAGE_FILES:
            filepath = package_dir / filename
            if not filepath.exists():
                errors.append(f"Missing package file: {config['package']}/{filename}")
    
    # Check examples directory
    examples_dir = module_dir / "examples"
    if not examples_dir.exists():
        errors.append("Missing examples/ directory")
    else:
        # Check example files
        for filename in REQUIRED_EXAMPLE_FILES:
            filepath = examples_dir / filename
            if not filepath.exists():
                errors.append(f"Missing example file: examples/{filename}")
        
        # Check tree file if required
        if config["requires_tree"]:
            tree_file = examples_dir / "tree.newick"
            if not tree_file.exists():
                errors.append("Missing required file: examples/tree.newick")
    
    # Check notebooks directory
    notebooks_dir = module_dir / "notebooks"
    if not notebooks_dir.exists():
        errors.append("Missing notebooks/ directory")
    else:
        notebook_file = notebooks_dir / config["notebook"]
        if not notebook_file.exists():
            errors.append(f"Missing notebook: notebooks/{config['notebook']}")
    
    # Check subdirectories exist
    for subdir in ["tests", "docker"]:
        subdir_path = module_dir / subdir
        if not subdir_path.exists():
            errors.append(f"Missing directory: {subdir}/")
    
    return len(errors) == 0, errors


def verify_file_content(filepath: Path, expected_content: str) -> bool:
    """Check if a file contains expected content."""
    if not filepath.exists():
        return False
    
    content = filepath.read_text()
    return expected_content in content


def main():
    """Main verification function."""
    base_dir = Path("/home/runner/work/MKrep/MKrep/separated_repos")
    
    print("=" * 70)
    print("StrepSuis Suite - Module Verification")
    print("=" * 70)
    print()
    
    all_success = True
    results = {}
    
    for module_name, config in MODULES.items():
        print(f"Checking {module_name}...")
        success, errors = check_module(module_name, config, base_dir)
        results[module_name] = (success, errors)
        
        if success:
            print(f"  ✅ All files present")
        else:
            print(f"  ❌ {len(errors)} error(s) found:")
            for error in errors:
                print(f"     - {error}")
            all_success = False
        print()
    
    # Summary
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print()
    
    success_count = sum(1 for success, _ in results.values() if success)
    total_count = len(results)
    
    print(f"Modules checked: {total_count}")
    print(f"Passed: {success_count}")
    print(f"Failed: {total_count - success_count}")
    print()
    
    if all_success:
        print("🎉 All modules verified successfully!")
        print()
        print("✅ All 5 modules are complete and ready for deployment")
        print("✅ All required files are present")
        print("✅ All directory structures are correct")
        print()
        print("Next steps:")
        print("  1. See REPOSITORY_SEPARATION_GUIDE.md for deployment instructions")
        print("  2. Push each module to its own GitHub repository")
        print("  3. Test installation from GitHub")
        print("  4. Create releases for each module")
        print()
        return 0
    else:
        print("❌ Some modules have missing files")
        print("Please fix the errors listed above")
        print()
        return 1


if __name__ == "__main__":
    exit(main())
