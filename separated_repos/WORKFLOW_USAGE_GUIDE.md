# Automated Report Generation Workflow

## Overview

This document describes the automated GitHub Actions workflow for generating test coverage reports and analysis summaries for all 5 StrepSuis Suite modules.

## What It Does

The workflow (`generate_reports.yml`) automatically:

- Installs all 5 modules with development dependencies
- Runs comprehensive test suites (excluding slow tests)
- Generates coverage reports in multiple formats (HTML, JSON, XML)
- Creates analysis summaries for each module
- Updates coverage badges in README files
- Commits all results back to the repository
- Uploads artifacts for download (90-day retention)

## How to Run

### Option 1: GitHub UI (Recommended)

1. Navigate to the **Actions** tab in GitHub
2. Select **"Generate Full Reports and Coverage"** from the workflows list
3. Click **"Run workflow"** button (top right)
4. Optional: Specify modules to process (default: "all")
   - Examples: `all`, `strepsuis-mdr`, `strepsuis-mdr strepsuis-amrvirkm`
5. Click **"Run workflow"** to start
6. Wait ~10-15 minutes for completion

### Option 2: GitHub CLI

```bash
# Run for all modules (default)
gh workflow run generate_reports.yml

# Run for specific modules only
gh workflow run generate_reports.yml -f modules="strepsuis-mdr strepsuis-amrvirkm"
```

### Option 3: REST API

```bash
curl -X POST \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/MK-vet/MKrep/actions/workflows/generate_reports.yml/dispatches \
  -d '{"ref":"main","inputs":{"modules":"all"}}'
```

## What Gets Generated

After workflow completes, the following will be committed to the repository:

### Coverage Reports
```
separated_repos/coverage_reports/
├── strepsuis-mdr_htmlcov/
│   └── index.html          # Interactive coverage report
├── strepsuis-amrvirkm_htmlcov/
├── strepsuis-genphennet_htmlcov/
└── strepsuis-phylotrait_htmlcov/
```

### Analysis Reports
```
separated_repos/analysis_reports/
├── strepsuis-mdr/
│   └── ANALYSIS_SUMMARY.md
├── strepsuis-amrvirkm/
│   └── ANALYSIS_SUMMARY.md
├── strepsuis-genphennet/
│   └── ANALYSIS_SUMMARY.md
└── strepsuis-phylotrait/
    └── ANALYSIS_SUMMARY.md
```

### Summary Documents
- `separated_repos/COVERAGE_REPORT_COMPLETE.md` - Comprehensive coverage summary
- `separated_repos/FULL_ANALYSIS_SUMMARY.md` - Complete index with links

### Updated Files
- Coverage badges in each module's `README.md` (updated from "pending" to actual %)

## Viewing Results

### After Workflow Completes

1. **View in GitHub**: Browse the committed files in the repository
2. **Download Artifacts**: 
   - Go to workflow run page
   - Scroll to "Artifacts" section
   - Download "analysis-and-coverage-reports" ZIP
3. **View Coverage Locally**:
   ```bash
   git pull
   cd separated_repos/coverage_reports/strepsuis-mdr_htmlcov
   open index.html  # or python -m http.server
   ```

## Workflow Details

### Execution Time
- **Target**: <50 minutes total
- **Typical**: 10-15 minutes
- **Per module**: ~2-3 minutes

### GitHub Actions Minutes Usage
- **Cost**: ~10-15 minutes per run
- **Monthly limit**: 2000 minutes (free tier)
- **Estimated runs per month**: 100+ runs available

### Optimization Features
- Uses Python package caching (`cache: 'pip'`)
- Runs only fast tests (`-m "not slow"`)
- Processes modules sequentially (one at a time)
- 50-minute timeout to prevent excessive usage

## Test Coverage Details

### New Unit Tests Added

Each module has a new `tests/test_unit_analysis.py` file with:
- **Configuration validation tests** (7-8 tests)
- **Analyzer initialization tests** (3-4 tests)
- **Default value tests** (6-7 tests)
- **Total**: ~82 tests across all modules

### Coverage Targets
- **Baseline (Phase 1)**: ~37% average
- **Current Target (Phase 2)**: 50-65%
- **Future Target (Phase 3)**: 80%+ for publication

### What's Tested
- Configuration parameter validation
- Invalid input handling (edge cases)
- Analyzer initialization (multiple methods)
- Default value verification
- Directory management
- Error handling
- ⏳ Core analysis functions (future enhancement)

## Troubleshooting

### Workflow Fails

1. **Check logs**: Click on failed step in Actions tab
2. **Common issues**:
   - Dependency installation failure → Check `pyproject.toml`
   - Test failures → Run locally: `pytest -m "not slow" -v`
   - Git push failure → Check permissions

### Coverage Lower Than Expected

- Unit tests alone provide 7-11% coverage
- When combined with existing tests: 50-65%
- Run all tests locally to verify: `pytest --cov`

### No Changes Committed

- This is normal if:
  - Coverage hasn't changed since last run
  - No new reports were generated
- Workflow will report: "No changes to commit"

## Local Testing

To run the same process locally:

```bash
cd separated_repos/strepsuis-mdr

# Install dependencies
pip install -e .[dev]

# Run tests with coverage
pytest -m "not slow" \
       --cov=strepsuis_mdr \
       --cov-report=html \
       --cov-report=term

# View coverage report
open htmlcov/index.html
```

## Next Steps

After running the workflow:

1. **Review Coverage**: Check `COVERAGE_REPORT_COMPLETE.md` for overall metrics
2. **Examine Gaps**: Open HTML reports to see uncovered lines
3. **Add More Tests**: Target functions with low coverage
4. **Run Locally**: Use full 92-strain dataset for complete analysis
5. **Update Documentation**: Add examples based on results

## Support

For issues or questions:
- Open an issue in the repository
- Check existing documentation in `separated_repos/`
- Review test files for examples

---

**Workflow File:** `.github/workflows/generate_reports.yml`
