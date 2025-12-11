#!/usr/bin/env python3
"""
Generate coverage badges for all modules.

This script runs tests with coverage for each module and generates
badge data that can be used in README files.
"""

import json
import subprocess
import sys
from pathlib import Path


def run_coverage_for_module(module_path: Path) -> dict:
    """
    Run pytest with coverage for a specific module.
    
    Returns:
        dict with coverage percentage and status
    """
    print(f"\n{'='*60}")
    print(f"Running coverage for {module_path.name}")
    print(f"{'='*60}")
    
    # Run pytest with coverage
    cmd = [
        "pytest",
        "-m", "not slow",
        "--cov",
        "--cov-report=json",
        "--cov-report=term",
        "-v"
    ]
    
    try:
        result = subprocess.run(
            cmd,
            cwd=module_path,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        # Read coverage.json
        coverage_file = module_path / "coverage.json"
        if coverage_file.exists():
            with open(coverage_file) as f:
                coverage_data = json.load(f)
            
            total_coverage = coverage_data["totals"]["percent_covered"]
            
            return {
                "module": module_path.name,
                "coverage": round(total_coverage, 2),
                "status": "success" if result.returncode == 0 else "tests_failed",
                "total_statements": coverage_data["totals"]["num_statements"],
                "covered_statements": coverage_data["totals"]["covered_lines"]
            }
        else:
            return {
                "module": module_path.name,
                "coverage": 0.0,
                "status": "no_coverage_data",
                "error": "coverage.json not found"
            }
    
    except subprocess.TimeoutExpired:
        return {
            "module": module_path.name,
            "coverage": 0.0,
            "status": "timeout",
            "error": "Test execution timed out"
        }
    except Exception as e:
        return {
            "module": module_path.name,
            "coverage": 0.0,
            "status": "error",
            "error": str(e)
        }


def generate_badge_url(coverage_pct: float) -> str:
    """Generate shields.io badge URL based on coverage percentage."""
    # Color scheme
    if coverage_pct >= 80:
        color = "brightgreen"
    elif coverage_pct >= 60:
        color = "green"
    elif coverage_pct >= 40:
        color = "yellow"
    elif coverage_pct >= 20:
        color = "orange"
    else:
        color = "red"
    
    return f"https://img.shields.io/badge/coverage-{coverage_pct}%25-{color}"


def generate_badge_markdown(module_name: str, coverage_pct: float) -> str:
    """Generate markdown badge."""
    badge_url = generate_badge_url(coverage_pct)
    return f"![Coverage]({badge_url})"


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
    
    print(f"Found {len(modules)} modules to test")
    
    results = []
    
    for module_path in sorted(modules):
        # Check if tests directory exists
        if not (module_path / "tests").exists():
            print(f"⚠️  {module_path.name}: No tests directory, skipping")
            continue
        
        result = run_coverage_for_module(module_path)
        results.append(result)
    
    # Generate summary report
    print(f"\n{'='*60}")
    print("Coverage Summary")
    print(f"{'='*60}\n")
    
    summary_file = separated_repos_dir / "COVERAGE_SUMMARY.md"
    
    with open(summary_file, "w") as f:
        f.write("# Test Coverage Summary\n\n")
        f.write("Auto-generated coverage report for all modules.\n\n")
        f.write("| Module | Coverage | Status | Badge |\n")
        f.write("|--------|----------|--------|-------|\n")
        
        for result in results:
            module = result["module"]
            coverage = result["coverage"]
            status = result["status"]
            
            badge = generate_badge_markdown(module, coverage)
            
            f.write(f"| {module} | {coverage}% | {status} | {badge} |\n")
            
            print(f"{module:25} {coverage:6.2f}%  {status:15}")
        
        f.write("\n## Instructions\n\n")
        f.write("Add these badges to your module README files:\n\n")
        
        for result in results:
            module = result["module"]
            coverage = result["coverage"]
            badge_url = generate_badge_url(coverage)
            
            f.write(f"### {module}\n\n")
            f.write("```markdown\n")
            f.write(f"[![Coverage]({badge_url})]()\n")
            f.write("```\n\n")
    
    print(f"\n✅ Summary written to {summary_file}")
    
    # Write JSON report
    json_file = separated_repos_dir / "coverage_report.json"
    with open(json_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ JSON report written to {json_file}")
    
    # Calculate average coverage
    successful_results = [r for r in results if r["status"] == "success"]
    if successful_results:
        avg_coverage = sum(r["coverage"] for r in successful_results) / len(successful_results)
        print(f"\n📊 Average coverage: {avg_coverage:.2f}%")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
