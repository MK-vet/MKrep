"""
Command-line interface for StrepSuisAnalyzer.
"""

import sys
import argparse
from pathlib import Path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="StrepSuisAnalyzer: Interactive analysis of Streptococcus suis data"
    )

    parser.add_argument(
        "--launch",
        action="store_true",
        help="Launch the Streamlit web interface",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8501,
        help="Port for Streamlit server (default: 8501)",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information",
    )

    args = parser.parse_args()

    if args.version:
        print("StrepSuisAnalyzer version 1.0.0")
        return 0

    if args.launch:
        import subprocess
        import os

        # Get the path to app.py
        app_path = Path(__file__).parent / "app.py"

        # Launch Streamlit
        cmd = [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(app_path),
            f"--server.port={args.port}",
        ]

        try:
            subprocess.run(cmd, check=True)
            return 0
        except subprocess.CalledProcessError as e:
            print(f"Error launching Streamlit: {e}", file=sys.stderr)
            return 1
        except KeyboardInterrupt:
            print("\nShutting down...")
            return 0

    # Default: show help
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
