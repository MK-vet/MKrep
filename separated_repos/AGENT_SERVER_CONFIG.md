# Server Configuration for GitHub Copilot Agent - StrepSuis Suite

## Environment Setup

### Required Python Version
```
python_version: ">=3.8,<3.13"
```

### System Dependencies (for Docker builds)
```yaml
apt_packages:
  - git
  - gcc
  - g++
```

### Python Dependencies (dev)
```yaml
pip_packages:
  - pytest>=7.0
  - pytest-cov>=4.0
  - pytest-xdist
  - pytest-timeout
  - black>=23.0
  - isort>=5.12
  - ruff>=0.1.0
  - mypy>=1.0
  - bandit>=1.7
  - pre-commit>=3.0
```

## Working Directory Structure
```
separated_repos/
├── strepsuis-mdr/
├── strepsuis-amrvirkm/
├── strepsuis-genphennet/
├── strepsuis-phylotrait/
├── strepsuis-analyzer/
├── synthetic_data/
├── test_reports/
├── analysis_results/
└── assets/
```

## Test Execution Commands
```bash
cd separated_repos/strepsuis-mdr
pip install -e .[dev]
pytest --cov --cov-report=html --cov-report=xml -v
```

## Validation Commands
```bash
pytest tests/test_statistical_validation.py -v
pytest -k "chi_square or fisher or bootstrap or fdr" -v
```

## Docker Build and Test
```bash
docker build -t strepsuis-mdr:test .
docker run --rm strepsuis-mdr:test --version
```

## Coverage Thresholds
- overall_minimum: 70%
- critical_paths: 100%
- fail_under: 70%
