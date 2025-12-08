"""
CLI wrapper for the E2E analysis runner.

This module provides a command-line interface for running comprehensive
end-to-end analyses using the strepsuis-analyzer application.
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Entry point for strepsuis-analyzer-e2e CLI command."""
    # Run the E2E script as a subprocess to avoid sys.path manipulation
    scripts_dir = Path(__file__).parent.parent.parent / "scripts"
    e2e_script = scripts_dir / "e2e_run.py"
    
    if not e2e_script.exists():
        print(f"Error: E2E script not found at {e2e_script}", file=sys.stderr)
        sys.exit(1)
    
    # Pass through all command-line arguments
    result = subprocess.run([sys.executable, str(e2e_script)] + sys.argv[1:])
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
