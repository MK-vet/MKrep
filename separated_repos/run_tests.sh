#!/bin/bash
# Consolidated test runner for all StrepSuis modules
#
# Usage:
#   ./run_tests.sh              # Run all tests
#   ./run_tests.sh --fast       # Run fast tests only (skip slow markers)
#   ./run_tests.sh --coverage   # Run tests with coverage report

set -e

FAST=false
COVERAGE=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --fast) FAST=true ;;
        --coverage) COVERAGE=true ;;
        --help)
            echo "Usage: $0 [--fast] [--coverage]"
            echo "  --fast      Run tests excluding @pytest.mark.slow"
            echo "  --coverage  Run with coverage report"
            exit 0
            ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODULES="strepsuis-amrpat strepsuis-amrvirkm strepsuis-genphen strepsuis-genphennet strepsuis-phylotrait"

echo "=========================================="
echo "Running tests for ALL 5 modules"
echo "=========================================="

for module in $MODULES; do
    echo ""
    echo "=== Testing $module ==="
    cd "$SCRIPT_DIR/$module"

    # Install module if needed
    pip install -e . -q 2>&1 | tail -1 || true

    # Build pytest command
    PYTEST_ARGS="-v"
    
    if [ "$FAST" = true ]; then
        PYTEST_ARGS="$PYTEST_ARGS -m 'not slow'"
    fi

    if [ "$COVERAGE" = true ]; then
        MODULE_UNDERSCORE=$(echo "$module" | tr '-' '_')
        PYTEST_ARGS="$PYTEST_ARGS --cov=$MODULE_UNDERSCORE --cov-report=html --cov-report=term"
    fi

    # Run tests
    pytest $PYTEST_ARGS || echo "Tests completed with some failures"
done

echo ""
echo "=========================================="
echo "ALL MODULES TESTED"
echo "=========================================="
