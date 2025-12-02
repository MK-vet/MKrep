#!/usr/bin/env python3
"""
Replicate end-to-end test structure across all modules.

This script creates comprehensive end-to-end tests for each module
based on the template from strepsuis-mdr.
"""

import re
import shutil
from pathlib import Path


def get_module_info(module_path: Path) -> dict:
    """Extract module-specific information."""
    name = module_path.name
    
    # Module-specific mappings
    module_map = {
        "strepsuis-mdr": {
            "class_name": "MDRAnalyzer",
            "module_import": "strepsuis_mdr.analyzer",
            "config_import": "strepsuis_mdr.config",
            "description": "MDR pattern detection",
            "has_tree": False
        },
        "strepsuis-amrvirkm": {
            "class_name": "ClusterAnalyzer",
            "module_import": "strepsuis_amrvirkm.analyzer",
            "config_import": "strepsuis_amrvirkm.config",
            "description": "K-Modes clustering",
            "has_tree": False
        },
        "strepsuis-genphennet": {
            "class_name": "NetworkAnalyzer",
            "module_import": "strepsuis_genphennet.analyzer",
            "config_import": "strepsuis_genphennet.config",
            "description": "Network analysis",
            "has_tree": False
        },
        "strepsuis-phylotrait": {
            "class_name": "PhyloTraitAnalyzer",
            "module_import": "strepsuis_phylotrait.analyzer",
            "config_import": "strepsuis_phylotrait.config",
            "description": "Phylogenetic analysis",
            "has_tree": True
        }
    }
    
    return module_map.get(name, {
        "class_name": "Analyzer",
        "module_import": f"{name.replace('-', '_')}.analyzer",
        "config_import": f"{name.replace('-', '_')}.config",
        "description": "analysis",
        "has_tree": False
    })


def customize_test_file(template_content: str, module_info: dict) -> str:
    """Customize template test file for specific module."""
    content = template_content
    
    # Replace analyzer class name
    content = content.replace("MDRAnalyzer", module_info["class_name"])
    
    # Replace import statements
    content = re.sub(
        r'from strepsuis_mdr\.analyzer import \w+',
        f"from {module_info['module_import']} import {module_info['class_name']}",
        content
    )
    content = re.sub(
        r'from strepsuis_mdr\.config import Config',
        f"from {module_info['config_import']} import Config",
        content
    )
    
    # Update docstrings with module-specific description
    content = content.replace(
        "MDR pattern detection",
        module_info["description"]
    )
    content = content.replace(
        "multidrug resistance",
        module_info["description"]
    )
    
    # Add tree file copying if needed
    if module_info["has_tree"]:
        tree_copy = """    # Copy newick files if present
    for newick_file in example_dir.glob("*.newick"):
        shutil.copy(newick_file, data_dir)
    for nwk_file in example_dir.glob("*.nwk"):
        shutil.copy(nwk_file, data_dir)
    """
        # Insert after CSV copying
        content = content.replace(
            "df_mini.to_csv(data_dir / csv_file, index=False)",
            f"df_mini.to_csv(data_dir / csv_file, index=False)\n    \n{tree_copy}"
        )
    
    return content


def replicate_to_module(source_module: Path, target_module: Path):
    """Replicate test structure from source to target module."""
    print(f"\n{'='*60}")
    print(f"Replicating tests to {target_module.name}")
    print(f"{'='*60}")
    
    # Get module info
    module_info = get_module_info(target_module)
    
    # Read template test file
    template_file = source_module / "tests" / "test_end_to_end.py"
    if not template_file.exists():
        print(f"❌ Template file not found: {template_file}")
        return False
    
    template_content = template_file.read_text()
    
    # Customize for target module
    customized_content = customize_test_file(template_content, module_info)
    
    # Write to target
    target_test_file = target_module / "tests" / "test_end_to_end.py"
    target_test_file.write_text(customized_content)
    
    print(f"✅ Created {target_test_file}")
    
    # Update TESTING.md if it exists
    testing_md = target_module / "TESTING.md"
    if testing_md.exists():
        source_testing_md = source_module / "TESTING.md"
        if source_testing_md.exists():
            # Copy the enhanced TESTING.md
            shutil.copy(source_testing_md, testing_md)
            
            # Update module name in the file
            content = testing_md.read_text()
            content = content.replace("StrepSuis-AMRPat", target_module.name)
            content = content.replace("strepsuis-mdr", target_module.name)
            content = content.replace("strepsuis_mdr", target_module.name.replace("-", "_"))
            testing_md.write_text(content)
            
            print(f"✅ Updated {testing_md}")
    
    return True


def main():
    """Main function."""
    separated_repos_dir = Path(__file__).parent
    
    # Source module (template)
    source_module = separated_repos_dir / "strepsuis-mdr"
    
    if not source_module.exists():
        print(f"❌ Source module not found: {source_module}")
        return 1
    
    # Target modules
    target_modules = [
        d for d in separated_repos_dir.iterdir()
        if d.is_dir() 
        and d.name.startswith("strepsuis-")
        and d.name != "strepsuis-mdr"
    ]
    
    if not target_modules:
        print("⚠️  No target modules found")
        return 1
    
    print(f"Found {len(target_modules)} modules to enhance:")
    for module in target_modules:
        print(f"  - {module.name}")
    
    # Replicate to each module
    success_count = 0
    for module in sorted(target_modules):
        if replicate_to_module(source_module, module):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"Summary: Enhanced {success_count}/{len(target_modules)} modules")
    print(f"{'='*60}")
    
    if success_count == len(target_modules):
        print("✅ All modules successfully enhanced!")
        return 0
    else:
        print("⚠️  Some modules failed to enhance")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
