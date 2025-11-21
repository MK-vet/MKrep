
## Testing Infrastructure

All repositories now include **comprehensive test coverage** designed for both scientific validity and minimal CI consumption.

### Test Coverage Summary

| Module | Tests | Coverage | Fast Tests | Full Suite |
|--------|-------|----------|------------|------------|
| strepsuis-amrpat | 82 | 57-80% | ~4s | ~10-30s |
| strepsuis-amrvirkm | 82 | 57-80% | ~4s | ~10-30s |
| strepsuis-genphen | 82 | 57-80% | ~4s | ~10-30s |
| strepsuis-genphennet | 82 | 57-80% | ~4s | ~10-30s |
| strepsuis-phylotrait | 82 | 57-80% | ~4s | ~10-30s |

### Test Categories

Each repository includes:
- **Unit Tests**: Fast tests of individual components
- **Integration Tests**: Tests using real example data
- **Workflow Tests**: End-to-end pipeline validation
- **CLI Tests**: Command-line interface validation
- **Data Validation Tests**: Input data format checking

### Quick Testing Commands

```bash
# Fast tests (for development)
pytest -m "not slow" -v

# Full test suite
pytest -v

# With coverage report
pytest --cov --cov-report=html
open htmlcov/index.html
```

### CI/CD Optimization

- Tests run on: Pull requests, manual triggers, releases only
- Fast tests only in CI (slow tests run locally)
- Estimated CI time: 4-6 minutes per module
- Well within GitHub's free tier

### Documentation

- [📊 Test Coverage Summary](TEST_COVERAGE_SUMMARY.md) - Comprehensive testing overview
- [⚡ Local Testing Guide](LOCAL_TESTING_GUIDE.md) - Quick reference
- [📝 Testing README](README_TESTING.md) - Complete testing documentation
- Module-specific: Each repository has a `TESTING.md` file

### Generate All Coverage Reports

```bash
cd separated_repos
./generate_coverage_reports.sh
```

