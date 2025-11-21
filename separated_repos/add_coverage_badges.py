#!/usr/bin/env python3
"""
Add coverage badges to module README files.

This script adds test coverage badges to the badges section of each
module's README.md file.
"""

import re
from pathlib import Path


def add_coverage_badge(readme_path: Path, module_name: str) -> bool:
    """
    Add coverage badge to README if not already present.
    
    Args:
        readme_path: Path to README.md file
        module_name: Name of the module (e.g., strepsuis-amrpat)
    
    Returns:
        True if badge was added or already exists, False otherwise
    """
    if not readme_path.exists():
        print(f"  ⚠️  README not found: {readme_path}")
        return False
    
    content = readme_path.read_text()
    
    # Check if coverage badge already exists
    if "coverage-" in content and "img.shields.io" in content:
        print(f"  ℹ️  Coverage badge already exists")
        return True
    
    # Create coverage badge (placeholder - will be updated after tests run)
    coverage_badge = "[![Coverage](https://img.shields.io/badge/coverage-pending-lightgrey)]()"
    
    # Find the badges section (after title, before first ##)
    # Look for existing badges like Python version, License, etc.
    badge_pattern = r'(^\[!\[.*?\]\(.*?\)\]\(.*?\)\s*$)'
    
    lines = content.split('\n')
    insert_position = None
    
    for i, line in enumerate(lines):
        # Find last badge line
        if line.strip().startswith('[![') and '](' in line:
            insert_position = i + 1
    
    if insert_position is None:
        # If no badges found, insert after title
        for i, line in enumerate(lines):
            if line.startswith('#') and not line.startswith('##'):
                insert_position = i + 2  # After title and blank line
                break
    
    if insert_position is not None:
        lines.insert(insert_position, coverage_badge)
        new_content = '\n'.join(lines)
        readme_path.write_text(new_content)
        print(f"  ✅ Added coverage badge at line {insert_position}")
        return True
    else:
        print(f"  ❌ Could not find appropriate position for badge")
        return False


def main():
    """Main function."""
    separated_repos_dir = Path(__file__).parent
    
    # Find all module directories
    modules = [
        d for d in separated_repos_dir.iterdir()
        if d.is_dir() and d.name.startswith("strepsuis-")
    ]
    
    if not modules:
        print("No strepsuis-* modules found!")
        return 1
    
    print(f"Found {len(modules)} modules to update")
    
    success_count = 0
    for module_path in sorted(modules):
        print(f"\n{module_path.name}:")
        readme_path = module_path / "README.md"
        
        if add_coverage_badge(readme_path, module_path.name):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"Updated {success_count}/{len(modules)} README files")
    print(f"{'='*60}")
    
    print("\nℹ️  Note: Coverage badges show 'pending' until tests are run.")
    print("   Run 'pytest --cov' in each module to update coverage.")
    
    return 0 if success_count == len(modules) else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
