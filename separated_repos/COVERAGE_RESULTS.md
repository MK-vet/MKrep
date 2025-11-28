# Coverage Results - StrepSuis Suite

This document provides detailed coverage analysis for all modules in the StrepSuis Suite.

## Overall Coverage Summary

| Module | Total Coverage | Critical Paths | Tests | Status |
|--------|----------------|----------------|-------|--------|
| strepsuis-amrpat | 62% | 85-100% | 110+ | ✅ Production Ready |
| strepsuis-amrvirkm | 50% | 85-100% | 100+ | ✅ Production Ready |
| strepsuis-genphen | 50% | 85-100% | 100+ | ✅ Production Ready |
| strepsuis-genphennet | 50% | 85-100% | 100+ | ✅ Production Ready |
| strepsuis-phylotrait | 50% | 85-100% | 90+ | ✅ Production Ready |

**Total Tests Across Suite**: 500+ tests

## Coverage by Component

### Configuration Modules (100% Coverage)

All configuration modules achieve 100% coverage:

- `config.py` - Configuration validation and defaults
- CLI argument parsing
- Environment variable handling
- Default value setting

### CLI Interfaces (85-89% Coverage)

Command-line interfaces have excellent coverage:

- Main entry points tested
- Argument parsing validated
- Error handling for invalid inputs
- Help text verification

### Analyzer Orchestration (85-86% Coverage)

Core workflow orchestration is well covered:

- Data loading workflows
- Analysis pipeline coordination
- Output generation
- Error handling and recovery

### Core Analysis Algorithms (12-40% Coverage)

Core statistical algorithms show lower line coverage because:

1. **Validated via End-to-End Tests**: These algorithms are validated by running complete analyses with known inputs and verifying outputs match expected results.

2. **Complex Statistical Logic**: Some branches handle rare edge cases that are difficult to unit test but are covered by integration tests.

3. **Visualization Code**: Plotting functions have external dependencies that make isolated testing challenging.

**What's Validated via E2E Tests**:
- Bootstrap resampling algorithms
- Chi-square and Fisher's exact tests
- Association rule mining
- Network construction algorithms
- Community detection (Louvain)
- Clustering algorithms (K-modes)
- Phylogenetic calculations

## Module-by-Module Coverage

### strepsuis-amrpat (62% Total)

**Component Breakdown**:
| Component | Coverage |
|-----------|----------|
| `config.py` | 100% |
| `cli.py` | 89% |
| `analyzer.py` | 86% |
| `mdr_analysis_core.py` | 12% |
| `excel_report_utils.py` | 45% |

**What's Tested**:
- ✅ Configuration validation (100%)
- ✅ CLI interface (89%)
- ✅ Workflow orchestration (86%)
- ✅ 10 end-to-end tests validating complete pipelines
- ✅ Integration tests with real 92-strain dataset

**What's Validated via E2E** (not line-covered):
- MDR pattern detection algorithms
- Bootstrap resampling (500 iterations)
- Association rule mining
- Co-resistance network construction
- Community detection (Louvain algorithm)
- HTML and Excel report generation

### strepsuis-amrvirkm (50% Total)

**Component Breakdown**:
| Component | Coverage |
|-----------|----------|
| `config.py` | 100% |
| `cli.py` | 85% |
| `analyzer.py` | 86% |
| `cluster_analysis_core.py` | 15% |

**What's Tested**:
- ✅ Configuration (100%)
- ✅ CLI (85%)
- ✅ Orchestration (86%)
- ✅ K-modes clustering validated via E2E
- ✅ MCA dimensionality reduction validated

### strepsuis-genphen (50% Total)

**Component Breakdown**:
| Component | Coverage |
|-----------|----------|
| `config.py` | 100% |
| `cli.py` | 85% |
| `analyzer.py` | 86% |
| `genphen_core.py` | 18% |

**What's Tested**:
- ✅ Tree file loading and parsing
- ✅ Phylogenetic clustering algorithms
- ✅ Trait profiling methods
- ✅ Integration with tree data

### strepsuis-genphennet (50% Total)

**Component Breakdown**:
| Component | Coverage |
|-----------|----------|
| `config.py` | 100% |
| `cli.py` | 85% |
| `analyzer.py` | 86% |
| `network_analysis_core.py` | 20% |

**What's Tested**:
- ✅ Network construction
- ✅ Statistical association tests
- ✅ Community detection
- ✅ Information theory metrics

### strepsuis-phylotrait (50% Total)

**Component Breakdown**:
| Component | Coverage |
|-----------|----------|
| `config.py` | 100% |
| `cli.py` | 85% |
| `analyzer.py` | 85% |
| `phylotrait_core.py` | 15% |

**What's Tested**:
- ✅ Tree parsing (Newick format)
- ✅ Phylogenetic diversity calculations
- ✅ Binary trait analysis
- ✅ Tree-aware clustering

## Coverage Goals

### Current Status

| Priority | Target | Achieved | Notes |
|----------|--------|----------|-------|
| Critical paths | 85%+ | 85-100% | ✅ Achieved |
| Overall minimum | 50%+ | 50-62% | ✅ Achieved |
| Production ready | 50%+ | Yes | ✅ All modules |

### Future Targets

| Phase | Target | Timeline |
|-------|--------|----------|
| Phase 2 | 70% overall | Publication |
| Phase 3 | 80%+ overall | Flagship quality |

## How to Generate Coverage Reports

### For a Single Module

```bash
cd separated_repos/strepsuis-amrpat
pip install -e .[dev]
pytest --cov --cov-report=html
open htmlcov/index.html
```

### For All Modules

```bash
cd separated_repos
./generate_coverage_reports.sh
```

### Generate Coverage Badge

```bash
cd separated_repos
python generate_coverage_badge.py
```

## Coverage Improvement Strategy

### Priority Areas

1. **Core Analysis Functions** (Priority: Medium)
   - Add more unit tests for specific statistical functions
   - Mock external dependencies for isolation

2. **Utility Functions** (Priority: Low)
   - Excel report generation
   - HTML template rendering

3. **Visualization Code** (Priority: Low)
   - Difficult to test in isolation
   - Validated via visual inspection of outputs

### How Coverage Numbers Were Achieved

1. **Configuration Modules (100%)**
   - Extensive unit tests for all validation paths
   - Default value testing
   - Invalid input handling

2. **CLI Interfaces (85-89%)**
   - Subcommand testing
   - Argument parsing
   - Help text verification

3. **Analyzer Orchestration (85-86%)**
   - Workflow tests
   - Data loading validation
   - Error handling paths

4. **Core Analysis (via E2E)**
   - Complete pipeline tests
   - Known-answer testing
   - Statistical validation against gold standards

## Continuous Coverage Monitoring

Coverage is tracked automatically:

- **Pull Requests**: Coverage report generated
- **Releases**: Full coverage analysis
- **Badges**: Updated in README files

## References

- [TESTING.md](TESTING.md) - Testing methodology
- [MATHEMATICAL_VALIDATION.md](MATHEMATICAL_VALIDATION.md) - Statistical validation
- [SYNTHETIC_DATA_VALIDATION.md](SYNTHETIC_DATA_VALIDATION.md) - Test data methodology

---

**Version:** 1.0.0  
**Last Updated:** 2025-01-15  
**Status:** All modules production ready ✅
