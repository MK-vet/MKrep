# Local Testing Commands - Quick Reference

## Quick Test Commands

### Fast Development Iteration
Run this during active development for immediate feedback:
```bash
pytest -m "not slow" -v
```
**Time**: ~5 seconds per module

### Full Test Suite (Local Only)
Run before committing to verify all functionality:
```bash
pytest -v
```
**Time**: ~10-30 seconds per module (depending on slow tests)

### Coverage Report Generation
Generate detailed HTML coverage report:
```bash
pytest --cov --cov-report=html
open htmlcov/index.html
```

### Coverage by Category
```bash
# Infrastructure code only (config, cli, analyzer)
pytest --cov=strepsuis_amrpat --cov-report=term

# Exclude slow tests, get coverage
pytest -m "not slow" --cov --cov-report=term
```

## Test Categories

### Unit Tests
```bash
pytest -m unit -v
```

### Integration Tests
```bash
pytest -m integration -v
```

### Workflow Tests
```bash
pytest tests/test_workflow.py -v
```

### Slow Tests (Local Execution Recommended)
```bash
# Run ONLY slow tests
pytest -m slow -v

# Run ALL tests including slow ones
pytest -v
```

## Pre-Commit Validation

Before committing, run the full local validation suite:

```bash
# 1. Format and lint
pre-commit run --all-files

# 2. Run fast tests
pytest -m "not slow" -v

# 3. Optional: Run full suite locally
pytest -v
```

## Module-Specific Commands

### strepsuis-amrpat
```bash
cd separated_repos/strepsuis-amrpat
pip install -e .[dev]
pytest -m "not slow" --cov=strepsuis_amrpat --cov-report=html
```

### strepsuis-amrvirkm
```bash
cd separated_repos/strepsuis-amrvirkm
pip install -e .[dev]
pytest -m "not slow" --cov=strepsuis_amrvirkm --cov-report=html
```

### strepsuis-genphen
```bash
cd separated_repos/strepsuis-genphen
pip install -e .[dev]
pytest -m "not slow" --cov=strepsuis_genphen --cov-report=html
```

### strepsuis-genphennet
```bash
cd separated_repos/strepsuis-genphennet
pip install -e .[dev]
pytest -m "not slow" --cov=strepsuis_genphennet --cov-report=html
```

### strepsuis-phylotrait
```bash
cd separated_repos/strepsuis-phylotrait
pip install -e .[dev]
pytest -m "not slow" --cov=strepsuis_phylotrait --cov-report=html
```

## All Modules at Once

```bash
cd separated_repos
./generate_coverage_reports.sh
```

## CI/CD vs Local Testing

### CI/CD (GitHub Actions)
- Runs on: Pull requests, manual trigger, releases
- Excludes: Slow tests (optimized for speed)
- Coverage target: 60% minimum
- Estimated time: 3-5 minutes per module

### Local Testing
- Recommended: Run full suite including slow tests
- No time constraints
- Can run comprehensive workflow validation
- Coverage target: 80%+ recommended

## Debugging Failed Tests

### Verbose output with full traceback
```bash
pytest -vv --tb=long
```

### Stop at first failure
```bash
pytest -x
```

### Run specific test
```bash
pytest tests/test_workflow.py::test_data_loading_workflow -v
```

### Drop into debugger on failure
```bash
pytest --pdb
```

### Show print statements
```bash
pytest -s
```

## Performance Tips

### Parallel Execution (Requires pytest-xdist)
```bash
pip install pytest-xdist
pytest -n auto
```

### Run only failed tests from last run
```bash
pytest --lf
```

### Run failed tests first, then rest
```bash
pytest --ff
```

## Coverage Goals

| Component | Target Coverage |
|-----------|----------------|
| Config modules | 90-100% |
| CLI interfaces | 85-100% |
| Analyzers (init) | 80-100% |
| Core analysis | 60%+ |
| Utilities | 70%+ |
| Overall package | 60% min, 80%+ recommended |

## Example Workflow

```bash
# 1. Make code changes
vim strepsuis_amrpat/analyzer.py

# 2. Quick validation
pytest -m "not slow" -v

# 3. If tests pass, run with coverage
pytest -m "not slow" --cov=strepsuis_amrpat --cov-report=html

# 4. Check coverage in browser
open htmlcov/index.html

# 5. If coverage looks good, run full suite
pytest -v

# 6. Run pre-commit hooks
pre-commit run --all-files

# 7. Commit changes
git add .
git commit -m "Description of changes"
```

## Resources

- Full testing guide: See TESTING.md in each module
- Test coverage summary: See TEST_COVERAGE_SUMMARY.md
- Coverage script: ./generate_coverage_reports.sh
