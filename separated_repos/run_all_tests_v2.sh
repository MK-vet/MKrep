#!/bin/bash
# Quick test runner for all 5 modules - using pytest.ini settings

echo "=========================================="
echo "Running tests for ALL 5 modules"
echo "=========================================="

MODULES="strepsuis-amrpat strepsuis-amrvirkm strepsuis-genphen strepsuis-genphennet strepsuis-phylotrait"

for module in $MODULES; do
    echo ""
    echo "=== Testing $module ==="
    cd /home/runner/work/MKrep/MKrep/separated_repos/$module
    
    # Run all tests (pytest.ini already has coverage settings)
    pytest -q 2>&1 | tail -30
    
    # Extract and show coverage
    if [ -f coverage.json ]; then
        coverage=$(python3 -c "import json; data=json.load(open('coverage.json')); print(f\"{data['totals']['percent_covered']:.1f}%\")" 2>/dev/null || echo "N/A")
        echo "✅ Coverage for $module: $coverage"
    fi
done

echo ""
echo "=========================================="
echo "ALL MODULES TESTED"
echo "=========================================="
