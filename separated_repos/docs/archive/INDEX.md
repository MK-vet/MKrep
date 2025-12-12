# StrepSuis Suite - Documentation Index

## Quick Navigation

| Document | Purpose | Audience |
|----------|---------|----------|
| [README.md](README.md) | Suite overview and module descriptions | All users |
| [TESTING.md](TESTING.md) | Comprehensive testing guide | Developers |
| [TESTING_QUICK_START.md](TESTING_QUICK_START.md) | Quick reference for running tests | Developers |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Deployment and publishing instructions | DevOps |
| [ANALYSIS_EXAMPLES.md](ANALYSIS_EXAMPLES.md) | Example analysis results | Researchers |
| [WORKFLOW_USAGE_GUIDE.md](WORKFLOW_USAGE_GUIDE.md) | GitHub Actions workflow guide | Developers |
| [MATHEMATICAL_VALIDATION.md](MATHEMATICAL_VALIDATION.md) | Statistical validation methodology | Developers/Researchers |
| [SYNTHETIC_DATA_VALIDATION.md](SYNTHETIC_DATA_VALIDATION.md) | Synthetic data and validation | Developers/Researchers |
| [COVERAGE_RESULTS.md](COVERAGE_RESULTS.md) | Test coverage analysis | Developers |

## Modules

| Module | Coverage | Function |
|--------|----------|----------|
| [strepsuis-mdr](strepsuis-mdr/) | 62% | MDR pattern detection |
| [strepsuis-amrvirkm](strepsuis-amrvirkm/) | 50% | K-modes clustering |
| [strepsuis-genphennet](strepsuis-genphennet/) | 50% | Network-based analysis |
| [strepsuis-phylotrait](strepsuis-phylotrait/) | 50% | Phylogenetic trait analysis |
| [strepsuis-analyzer](strepsuis-analyzer/) | 85% | Interactive Streamlit analysis platform |

## Testing Summary

- 400+ tests across all modules
- 3-level testing: Unit, Integration, End-to-End
- 85-100% coverage of critical paths
- 50-62% total coverage

## Utility Scripts

| Script | Purpose |
|--------|---------|
| `generate_coverage_badge.py` | Generate coverage reports |
| `generate_coverage_reports.sh` | Run coverage for all modules |
| `run_all_tests.sh` | Execute tests for all modules |
| `replicate_tests.py` | Copy test structure to new modules |

## Quick Start

```bash
# Run tests for a module
cd strepsuis-mdr
pip install -e .[dev]
pytest -v
```

See [TESTING_QUICK_START.md](TESTING_QUICK_START.md) for more commands.

---

**Version:** 1.0.0  
**Python:** 3.8+  
**License:** MIT
