#!/bin/bash
# Script to generate coverage reports for all StrepSuis modules
# Usage: ./generate_coverage_reports.sh

set -e

REPOS_DIR="/home/runner/work/MKrep/MKrep/separated_repos"
MODULES=("strepsuis-mdr" "strepsuis-amrvirkm" "strepsuis-genphennet" "strepsuis-phylotrait")

echo "========================================="
echo "Coverage Report Generator for StrepSuis Suite"
echo "========================================="
echo ""

for module in "${MODULES[@]}"; do
    echo "Processing: $module"
    echo "-----------------------------------------"
    
    cd "$REPOS_DIR/$module"
    
    # Install if not already installed
    if ! python -c "import ${module//-/_}" 2>/dev/null; then
        echo "Installing $module..."
        pip install -e .[dev] -q
    fi
    
    # Run tests with coverage (excluding slow tests)
    echo "Running tests..."
    pytest -m "not slow" --cov=$(echo $module | tr '-' '_') \
           --cov-report=term --cov-report=html --cov-report=xml \
           --cov-fail-under=0 -q 2>&1 | tail -20
    
    echo ""
done

echo "========================================="
echo "Coverage reports generated successfully!"
echo "========================================="
echo ""
echo "HTML reports are available in each module's htmlcov/ directory"
echo "XML reports are available as coverage.xml in each module"
