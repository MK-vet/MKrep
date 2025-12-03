# Contributing to StrepSuis Analyzer

Thank you for your interest in contributing to StrepSuis Analyzer! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)
- [Documentation](#documentation)

## Code of Conduct

This project adheres to a code of conduct that promotes a welcoming and inclusive environment. By participating, you are expected to uphold this code.

### Our Standards

- Be respectful and inclusive
- Welcome constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Set up the development environment**
4. **Create a branch** for your changes
5. **Make your changes**
6. **Test your changes**
7. **Submit a pull request**

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- pip package manager

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/MKrep.git
cd MKrep/separated_repos/strepsuis-analyzer

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e .[dev]

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-new-clustering-method`
- `fix/clustering-memory-leak`
- `docs/update-user-guide`
- `test/add-statistical-validation`

### Commit Messages

Write clear, concise commit messages:

```
Add K-modes clustering algorithm

- Implement K-modes for categorical data
- Add tests for K-modes functionality
- Update documentation with K-modes examples
```

Format:
- First line: Brief summary (50 chars or less)
- Blank line
- Detailed description (wrap at 72 chars)

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov --cov-report=html

# Run specific test file
pytest tests/test_analyzer.py -v

# Run fast tests only (skip slow tests)
pytest -m "not slow" -v
```

### Writing Tests

- Add tests for all new features
- Maintain or improve code coverage
- Use descriptive test names
- Include both success and failure cases
- Use appropriate pytest markers

Example:
```python
@pytest.mark.unit
def test_clustering_with_valid_data():
    """Test clustering with valid binary data."""
    # Arrange
    data = create_test_data()
    
    # Act
    result = perform_clustering(data, n_clusters=2)
    
    # Assert
    assert len(result) == len(data)
    assert result['Cluster'].nunique() == 2
```

## Submitting Changes

### Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Run code formatters**: `black .` and `isort .`
5. **Update CHANGELOG.md** with your changes
6. **Submit pull request** with clear description

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] All tests pass
- [ ] New tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] CHANGELOG.md updated
```

## Coding Standards

### Python Style

- Follow **PEP 8** style guide
- Use **Black** for code formatting (line length: 100)
- Use **isort** for import sorting
- Use **type hints** where possible
- Write **docstrings** for all public functions

### Code Quality Tools

```bash
# Format code
black --line-length=100 .
isort --profile=black --line-length=100 .

# Lint code
ruff check .

# Type checking
mypy --ignore-missing-imports .
```

### Docstring Format

Use Google-style docstrings:

```python
def perform_clustering(data: pd.DataFrame, n_clusters: int = 2) -> pd.Series:
    """Perform hierarchical clustering on binary data.
    
    Args:
        data: Binary trait data (strains × features)
        n_clusters: Number of clusters to create
        
    Returns:
        Series with cluster assignments for each strain
        
    Raises:
        ValueError: If data is not binary or n_clusters is invalid
        
    Example:
        >>> data = pd.DataFrame({'Gene1': [1, 0, 1], 'Gene2': [0, 1, 1]})
        >>> clusters = perform_clustering(data, n_clusters=2)
    """
    pass
```

## Documentation

### What to Document

- All public functions, classes, and modules
- Command-line interface options
- Configuration parameters
- Example usage
- Known limitations

### Documentation Files

- **README.md**: Overview and quick start
- **USER_GUIDE.md**: Detailed usage instructions
- **TESTING.md**: Testing guidelines
- **API documentation**: Inline docstrings

### Building Documentation

```bash
# Install documentation tools
pip install pdoc3

# Generate API documentation
pdoc --html --output-dir docs/api strepsuis_analyzer
```

## Review Process

Pull requests will be reviewed for:

1. **Code quality**: Follows standards, well-organized
2. **Testing**: Adequate test coverage
3. **Documentation**: Clear and complete
4. **Functionality**: Works as intended
5. **Performance**: No unnecessary performance degradation

## Questions?

- Open an **issue** for bug reports or feature requests
- Start a **discussion** for questions or ideas
- Contact maintainers for sensitive issues

## Recognition

Contributors will be recognized in:
- CHANGELOG.md for significant contributions
- Repository contributors list
- Release notes

Thank you for contributing to StrepSuis Analyzer!
