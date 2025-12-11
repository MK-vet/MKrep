"""
Sanity Check and Startup Script for StrepSuis-Analyzer

This module provides startup sanity checks for the Streamlit application,
verifying that all components are properly configured and can be imported.

Use this script to verify Docker builds and local installations.

Author: MK-vet Team
License: MIT
Version: 1.0.0
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple


def check_python_version() -> Tuple[bool, str]:
    """Check Python version compatibility."""
    major, minor = sys.version_info[:2]
    required_major, required_minor = 3, 8

    if major >= required_major and minor >= required_minor:
        return True, f"Python {major}.{minor} (>= {required_major}.{required_minor} required)"
    else:
        return False, f"Python {major}.{minor} (>= {required_major}.{required_minor} required)"


def check_import(module_name: str) -> Tuple[bool, str]:
    """Check if a module can be imported."""
    try:
        __import__(module_name)
        return True, f"{module_name}: OK"
    except ImportError as e:
        return False, f"{module_name}: FAILED - {e}"


def check_streamlit() -> Tuple[bool, str]:
    """Check Streamlit installation and version."""
    try:
        import streamlit as st
        version = st.__version__
        return True, f"Streamlit version: {version}"
    except ImportError:
        return False, "Streamlit: NOT INSTALLED"
    except Exception as e:
        return False, f"Streamlit: ERROR - {e}"


def check_app_imports() -> Tuple[bool, List[str]]:
    """Check that the Streamlit app can be imported."""
    errors = []
    success = True

    # Try to import the main app module
    try:
        # Add parent directory to path for local imports
        app_dir = Path(__file__).parent.parent
        if str(app_dir) not in sys.path:
            sys.path.insert(0, str(app_dir))

        import app
        return True, ["app.py imports successfully"]
    except ImportError as e:
        errors.append(f"app.py import failed: {e}")
        success = False
    except Exception as e:
        errors.append(f"app.py error: {e}")
        success = False

    return success, errors


def check_required_dependencies() -> Tuple[bool, Dict[str, str]]:
    """Check all required dependencies are installed."""
    required_packages = [
        "streamlit",
        "pandas",
        "numpy",
        "scipy",
        "matplotlib",
        "seaborn",
        "plotly",
        "sklearn",  # scikit-learn
    ]

    results = {}
    all_ok = True

    for package in required_packages:
        ok, msg = check_import(package)
        results[package] = "OK" if ok else "MISSING"
        if not ok:
            all_ok = False

    return all_ok, results


def check_data_files() -> Tuple[bool, List[str]]:
    """Check for sample data files (optional)."""
    data_dir = Path(__file__).parent.parent / "data"
    messages = []

    if data_dir.exists():
        csv_files = list(data_dir.glob("*.csv"))
        if csv_files:
            messages.append(f"Found {len(csv_files)} sample data files")
        else:
            messages.append("No sample data files found (this is OK)")
    else:
        messages.append("No data directory (this is OK)")

    return True, messages


def check_static_files() -> Tuple[bool, List[str]]:
    """Check for static files like images."""
    static_dir = Path(__file__).parent.parent / "static"
    messages = []

    if static_dir.exists():
        image_files = list(static_dir.glob("*.png")) + list(static_dir.glob("*.jpg"))
        if image_files:
            messages.append(f"Found {len(image_files)} static image files")
        else:
            messages.append("No static images found (this is OK)")
    else:
        messages.append("No static directory (this is OK)")

    return True, messages


def run_sanity_checks(verbose: bool = True) -> Dict[str, Any]:
    """
    Run all sanity checks and return results.

    Parameters:
        verbose: Print results to console

    Returns:
        Dictionary with check results
    """
    results = {
        "timestamp": datetime.now().isoformat(),
        "checks": [],
        "all_passed": True,
        "errors": [],
    }

    # Check Python version
    ok, msg = check_python_version()
    results["checks"].append({"name": "Python version", "passed": ok, "message": msg})
    if not ok:
        results["all_passed"] = False
        results["errors"].append(msg)
    if verbose:
        print(f"{'✓' if ok else '✗'} {msg}")

    # Check Streamlit
    ok, msg = check_streamlit()
    results["checks"].append({"name": "Streamlit", "passed": ok, "message": msg})
    if not ok:
        results["all_passed"] = False
        results["errors"].append(msg)
    if verbose:
        print(f"{'✓' if ok else '✗'} {msg}")

    # Check required dependencies
    ok, dep_results = check_required_dependencies()
    for pkg, status in dep_results.items():
        pkg_ok = status == "OK"
        results["checks"].append({
            "name": f"Package: {pkg}",
            "passed": pkg_ok,
            "message": status,
        })
        if not pkg_ok:
            results["all_passed"] = False
            results["errors"].append(f"{pkg}: {status}")
        if verbose:
            print(f"  {'✓' if pkg_ok else '✗'} {pkg}: {status}")

    # Check app imports
    ok, messages = check_app_imports()
    for msg in messages:
        results["checks"].append({
            "name": "App imports",
            "passed": ok,
            "message": msg,
        })
    if not ok:
        results["all_passed"] = False
        results["errors"].extend(messages)
    if verbose:
        for msg in messages:
            print(f"{'✓' if ok else '✗'} {msg}")

    # Check data files (optional)
    ok, messages = check_data_files()
    for msg in messages:
        results["checks"].append({
            "name": "Data files",
            "passed": ok,
            "message": msg,
        })
    if verbose:
        for msg in messages:
            print(f"ℹ {msg}")

    # Check static files (optional)
    ok, messages = check_static_files()
    for msg in messages:
        results["checks"].append({
            "name": "Static files",
            "passed": ok,
            "message": msg,
        })
    if verbose:
        for msg in messages:
            print(f"ℹ {msg}")

    return results


def save_sanity_check_report(results: Dict[str, Any], output_path: str = None) -> str:
    """Save sanity check results to a JSON file."""
    if output_path is None:
        output_path = Path(__file__).parent.parent / "logs" / "sanity_check_report.json"
    else:
        output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    return str(output_path)


def main():
    """Run sanity checks and display results."""
    print("=" * 60)
    print("StrepSuis-Analyzer Sanity Check")
    print("=" * 60)
    print()

    results = run_sanity_checks(verbose=True)

    print()
    print("=" * 60)

    if results["all_passed"]:
        print("✓ All sanity checks PASSED")
        print("The Streamlit app should start correctly.")
        print()
        print("To run the app:")
        print("  streamlit run app.py")
        exit_code = 0
    else:
        print("✗ Some sanity checks FAILED")
        print()
        print("Errors:")
        for error in results["errors"]:
            print(f"  - {error}")
        print()
        print("Please install missing dependencies and try again.")
        exit_code = 1

    # Save report
    report_path = save_sanity_check_report(results)
    print(f"\nReport saved to: {report_path}")

    print("=" * 60)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
