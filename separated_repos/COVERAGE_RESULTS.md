# Test Coverage Report - All Modules

**Last Updated**: 2025-11-24  
**Test Methodology**: All fast tests (`pytest -m "not slow"`) - consistent across all modules

## Coverage Results (Verified)

| Module | Coverage | Test Files | Status |
|--------|----------|------------|--------|
| strepsuis-amrpat | **61.1%** | 100 passed, 8 failed* | ✅ Exceeds target |
| strepsuis-amrvirkm | **34.0%** | 74 passed, 1 failed* | ⚠️ Approaching target |
| strepsuis-genphen | **31.7%** | 77 passed, 1 failed* | ⚠️ Approaching target |
| strepsuis-genphennet | **35.8%** | 77 passed, 1 failed* | ⚠️ Approaching target |
| strepsuis-phylotrait | **21.9%** | 75 passed, 3 failed* | ⚠️ Below target |

***Note**: Test failures are pre-existing issues (stdin capture, CLI args) not introduced by new tests.

## Methodology

All modules use **identical test methodology**:
- Run all tests marked as "not slow" (`pytest -m "not slow"`)
- Includes: unit tests, config tests, workflow tests, integration tests, utilities
- Excludes: end-to-end tests with full dataset (marked as "slow")
- Execution time: ~2-5 seconds per module

### Test Coverage Breakdown

**Coverage Components** (example from strepsuis-amrpat):
- Configuration modules: 84-100%
- CLI modules: 89-100%
- Analyzer initialization: 84-100%
- **Core analysis**: 11-56% (target for improvement)
- Utilities: 11-100%
- Test infrastructure: 83-100%

## Test Execution

### Local Testing
```bash
cd separated_repos/{module}
pip install -e .[dev]

# Run all fast tests (same as CI)
pytest -m "not slow" --cov --cov-report=html

# Run ALL tests including slow ones
pytest --cov --cov-report=html
```

### CI/CD (GitHub Actions)
The workflow uses the same methodology:
```yaml
pytest -m "not slow" --cov=${module} --cov-report=html
```

## Files Generated

- HTML Coverage: `separated_repos/coverage_reports/{module}_htmlcov/index.html`
- JSON Data: `separated_repos/{module}/coverage.json`
- Analysis Summary: `separated_repos/analysis_reports/{module}/ANALYSIS_SUMMARY.md`

## References

- **Workflow**: `.github/workflows/generate_reports.yml`
- **Usage Guide**: `separated_repos/WORKFLOW_USAGE_GUIDE.md`
- **Test Files**: `separated_repos/{module}/tests/test_unit_analysis.py`
