# COMPREHENSIVE FIX PROMPT - StrepSuis Suite

## Objective
Fix all identified issues in MK-vet/MKrep/separated_repos to meet publication-ready standards for SoftwareX journal.

## Priority 1: Critical Coverage Fixes (Target: 70% overall, 100% critical)

### Task 1.1: Fix CLI Coverage (Current: 0% in all modules)
For each module create tests/test_cli.py with:
- Test --help returns exit code 0
- Test --version returns version string
- Test each subcommand with mini dataset
- Use click.testing.CliRunner
- Target: 85%+ coverage for cli.py

### Task 1.2: Increase Core Module Coverage
- strepsuis-phylotrait (current: 9%) -> Target 70%+
- strepsuis-genphennet (current: 29%) -> Target 70%+

### Task 1.3: Add Missing Statistical Validation Tests
- Chi-square validation against scipy.stats.chi2_contingency
- Fisher exact validation against scipy.stats.fisher_exact
- FDR correction validation against statsmodels
- Bootstrap CI coverage verification

## Priority 2: Create Missing Folders
- test_reports/ (HTML coverage, XML, JUnit)
- analysis_results/ (HTML, Excel, PNG)
- assets/ (logos)

## Priority 3: Fix Docker/Colab GitHub Installation
Replace local COPY with: pip install git+https://github.com/MK-vet/REPO.git

## Priority 4: Add Missing Documentation
- CITATION.cff to all modules
- SECURITY.md to all modules
- ALGORITHMS.md to all modules
- BENCHMARKS.md to all modules

## Priority 5: Add Missing Test Types
- tests/test_stress.py (large datasets, memory, concurrent)
- tests/test_performance.py (timing benchmarks)
- Numerical stability tests

## Priority 6: Consistency Fixes
- Standardize pyproject.toml structure
- Standardize pytest.ini markers
- Standardize .pre-commit-config.yaml

## Verification Checklist
- Coverage >70% overall for all modules
- Coverage 100% for config.py
- Coverage >85% for cli.py
- All folders created with contents
- Docker installs from GitHub
- All pytest markers work
- All documentation present

## Success Criteria
1. pytest --cov shows >70% for each module
2. pytest -m stress runs successfully
3. pytest -m performance runs successfully
4. docker build and run work
5. All documentation files present

Version: 1.0.0 | Created: 2025-12-10
