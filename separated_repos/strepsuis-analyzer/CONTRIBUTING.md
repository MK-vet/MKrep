# Contributing to StrepSuisAnalyzer

Thank you for your interest in contributing to StrepSuisAnalyzer! This document provides guidelines for contributing to the project.

## Code of Conduct

This project adheres to professional standards of conduct. By participating, you are expected to maintain a respectful and collaborative environment.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- Clear and descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- Screenshots if applicable
- Environment details (OS, Python version, dependency versions)
- Error messages or logs

### Suggesting Enhancements

Enhancement suggestions are welcome. Please provide:

- Clear use case description
- Expected behavior and benefits
- Examples or mockups if applicable

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow coding standards**:
   - Use black for code formatting (line length 100)
   - Use isort for import sorting (black profile)
   - Follow PEP 8 conventions
   - Add type hints to all functions
   - Write comprehensive docstrings (Google style)

3. **Write tests**:
   - Add unit tests for new functionality
   - Ensure all tests pass: `pytest -v`
   - Maintain or improve code coverage

4. **Update documentation**:
   - Update README.md if needed
   - Update relevant documentation files
   - Add docstrings to new functions

5. **Follow the commit message convention**:
   ```
   type: brief description
   
   Detailed explanation if needed
   ```
   Types: feat, fix, docs, style, refactor, test, chore

6. **Run pre-commit hooks**:
   ```bash
   pre-commit run --all-files
   ```

## Development Setup

```bash
# Clone repository
git clone https://github.com/MK-vet/MKrep.git
cd MKrep/separated_repos/strepsuis-analyzer

# Install in development mode
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install

# Run tests
pytest -v
```

## Testing Guidelines

- Write tests for all new features
- Ensure tests are deterministic (use fixed random seeds)
- Use pytest fixtures for common test data
- Test edge cases and error conditions
- Aim for >80% code coverage

## Code Review Process

All submissions require review. The review process includes:

- Code quality and style compliance
- Test coverage and quality
- Documentation completeness
- Performance considerations
- Security implications

## Questions?

Feel free to open an issue for questions about contributing.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
