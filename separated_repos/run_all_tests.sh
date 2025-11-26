#!/bin/bash
# Quick parallel test runner for all 5 modules

echo "=========================================="
echo "Running tests for ALL 5 modules"
echo "=========================================="

MODULES="strepsuis-amrpat strepsuis-amrvirkm strepsuis-genphen strepsuis-genphennet strepsuis-phylotrait"

for module in $MODULES; do
    echo ""
    echo "=== Testing $module ==="
    cd /home/runner/work/MKrep/MKrep/separated_repos/$module
    
    # Quick install if needed
    pip install -e . -q 2>&1 | tail -1
    
    # Run comprehensive tests
    pytest tests/test_comprehensive_real_data.py --cov=$(echo $module | tr '-' '_') --cov-report=json:coverage_new.json -q 2>&1 | tail -20
    
    # Extract and show coverage
    if [ -f coverage_new.json ]; then
        coverage=$(python3 -c "import json; data=json.load(open('coverage_new.json')); print(f\"{data['totals']['percent_covered']:.1f}%\")" 2>/dev/null || echo "N/A")
        echo "✅ Coverage for $module: $coverage"
        cp coverage_new.json coverage.json
    fi
done

echo ""
echo "=========================================="
echo "ALL MODULES TESTED"
echo "=========================================="
