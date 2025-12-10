# GitHub Copilot Chat - General Instructions for StrepSuis Suite

## Context
You are assisting with the StrepSuis Suite - a collection of 5 bioinformatics Python modules for antimicrobial resistance analysis in Streptococcus suis. Each module will be published independently in SoftwareX journal.

## Modules Overview
| Module | Purpose | CLI Command |
|--------|---------|-------------|
| strepsuis-mdr | AMR Pattern Detection | strepsuis-mdr |
| strepsuis-amrvirkm | K-Modes Clustering | strepsuis-amrvirkm |
| strepsuis-genphennet | Network Integration | strepsuis-genphennet |
| strepsuis-phylotrait | Phylogenetic Traits | strepsuis-phylotrait |
| strepsuis-analyzer | Interactive Analysis | streamlit run app.py |

## Key Requirements

### 1. Code Quality
- Python 3.8+ compatible, type hints required
- Formatted with black/isort/ruff
- Linted with mypy, security checked with bandit
- All functions must have docstrings with Args, Returns, Raises

### 2. Testing Standards
- pytest with coverage >70% overall, 100% for critical paths
- Unit tests: @pytest.mark.unit
- Integration tests: @pytest.mark.integration
- Slow tests: @pytest.mark.slow
- Stress tests: @pytest.mark.stress
- Performance tests: @pytest.mark.performance

### 3. Statistical Validation
- All methods validated against scipy/statsmodels gold standards
- Chi-square: validate against scipy.stats.chi2_contingency
- Fisher exact: validate against scipy.stats.fisher_exact
- FDR correction: validate against statsmodels.stats.multitest.multipletests
- Bootstrap CIs: verify coverage contains true parameter 95% of time

### 4. Documentation
- English only, publication-ready, MIT licensed
- Required per module: README.md, USER_GUIDE.md, TESTING.md, CONTRIBUTING.md, CHANGELOG.md
- Also required: CITATION.cff, SECURITY.md, ALGORITHMS.md, BENCHMARKS.md

### 5. Deployment Architecture
- CLI (primary) - Click-based with subcommands
- Docker - Install from GitHub: pip install git+https://github.com/MK-vet/REPO.git
- Google Colab - Install from GitHub with !pip install

## Module Architecture Pattern
- config.py - Configuration with dataclasses, validation
- cli.py - Click-based CLI interface
- analyzer.py - Main orchestration class
- *_core.py - Core statistical algorithms
- excel_report_utils.py - Report generation utilities

## Coverage Targets
| Component | Target |
|-----------|--------|
| config.py | 100% |
| cli.py | 85%+ |
| analyzer.py | 85%+ |
| *_core.py | 70%+ |
| Overall module | 70%+ |

## When Writing Code
1. Always include docstrings with Args, Returns, Raises
2. Always include type hints
3. Always add corresponding test cases
4. Use numpy.random.seed(42) for reproducibility
5. Validate mathematical outputs against reference implementations

## Testing Commands
- Fast tests: pytest -m "not slow" -v
- Full suite: pytest -v
- With coverage: pytest --cov --cov-report=html
- Statistical validation: pytest tests/test_statistical_validation.py -v

## Critical Files to Consult
- separated_repos/MATHEMATICAL_VALIDATION.md
- separated_repos/SYNTHETIC_DATA_VALIDATION.md
- separated_repos/COVERAGE_RESULTS.md
- separated_repos/TESTING.md
- separated_repos/COMPREHENSIVE_FIX_PROMPT.md
- separated_repos/AGENT_SERVER_CONFIG.md

## Pre-commit Hooks
Always run before committing: pre-commit run --all-files
Tools: black, isort, ruff, mypy, bandit

## Global Standards
- Consult MATHEMATICAL_VALIDATION.md before modifying numerical logic
- Do not break downstream dependencies: CLIs, Dockerfiles, Notebooks
- Consider all code in strepsuis-*/ packages as production-grade
- Focus on increasing test coverage and mathematical correctness

Version: 2.0.0 | Updated: 2025-12-10
