"""
CLI wrapper for the E2E analysis runner.

This module provides a command-line interface for running comprehensive
end-to-end analyses using the strepsuis-analyzer application.
"""

import sys
from pathlib import Path


def main():
    """Entry point for strepsuis-analyzer-e2e CLI command."""
    # Import and run the E2E script
    scripts_dir = Path(__file__).parent.parent.parent / "scripts"
    sys.path.insert(0, str(scripts_dir))
    
    from e2e_run import main as e2e_main
    
    e2e_main()


if __name__ == "__main__":
    main()
