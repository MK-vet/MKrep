# GitHub Actions for MKrep

This document describes the GitHub Actions workflows that enable running all MKrep tools directly from GitHub.

## Overview

MKrep includes comprehensive GitHub Actions workflows that:
- ✅ Test all deployment options (Python scripts, CLI, Voilà, Colab notebooks)
- ✅ Verify compatibility across Python 3.8-3.12 and multiple operating systems
- ✅ Provide interactive demos that can be triggered manually
- ✅ Collect and display version information for all tools

## Available Workflows

### 1. CI - All Tools (`ci.yml`)

**Trigger**: Automatic on push/pull request to main or develop branches, or manual dispatch

**Purpose**: Continuous integration testing for all tools

**Jobs**:
- **test-python-scripts**: Tests standalone Python analysis scripts
  - Verifies script syntax and imports
  - Runs validation script
  - Tests on Python 3.8, 3.9, 3.10, 3.11, 3.12

- **test-cli-package**: Tests CLI package installation
  - Installs mkrep package
  - Verifies all CLI commands (mkrep, mkrep-cluster, mkrep-mdr, etc.)
  - Tests on Python 3.8-3.12

- **test-voila-dashboard**: Tests Voilà dashboard setup
  - Installs Voilà dependencies
  - Validates notebook syntax
  - Verifies example data
  - Tests on Python 3.9-3.12

- **test-notebooks**: Tests Jupyter/Colab notebooks
  - Validates notebook structure
  - Checks syntax conversion
  - Tests on Python 3.9-3.11

- **integration-test**: Final integration verification
  - Installs all tools
  - Displays summary of available commands
  - Confirms all tools are ready

**Status Badge**:
```markdown
[![CI - All Tools](https://github.com/MK-vet/MKrep/actions/workflows/ci.yml/badge.svg)](https://github.com/MK-vet/MKrep/actions/workflows/ci.yml)
```

### 2. Deployment Tests (`deployment.yml`)

**Trigger**: Automatic on push to main branch, or manual dispatch

**Purpose**: Comprehensive deployment verification

**Jobs**:
- **test-standalone-execution**: Verifies Python scripts can be executed
- **test-cli-full**: Full CLI package installation and testing
- **test-voila-deployment**: Voilà dashboard deployment readiness
- **test-colab-notebooks**: Colab notebook validation
- **version-matrix-test**: Tests across OS/Python version combinations
  - Ubuntu, Windows, macOS
  - Python 3.8-3.12
- **deployment-summary**: Displays overall deployment status

**Status Badge**:
```markdown
[![Deployment Tests](https://github.com/MK-vet/MKrep/actions/workflows/deployment.yml/badge.svg)](https://github.com/MK-vet/MKrep/actions/workflows/deployment.yml)
```

### 3. Version Info & Documentation (`version-info.yml`)

**Trigger**: Automatic on push to main branch, or manual dispatch

**Purpose**: Collect and display version information for all tools

**Jobs**:
- **version-info**: Collects comprehensive version information
  - Python environment
  - MKrep package version
  - All dependencies
  - Voilà and Jupyter versions
  - Available scripts and commands
  - Creates VERSION_INFO.md artifact

- **check-documentation**: Verifies all documentation files
- **requirements-check**: Validates requirements files
- **comprehensive-check**: Final deployment readiness report

**Artifact**: `VERSION_INFO.md` (retained for 90 days)

**Status Badge**:
```markdown
[![Version Info](https://github.com/MK-vet/MKrep/actions/workflows/version-info.yml/badge.svg)](https://github.com/MK-vet/MKrep/actions/workflows/version-info.yml)
```

### 4. Quick Start Demo (`quickstart-demo.yml`)

**Trigger**: Manual dispatch only (workflow_dispatch)

**Purpose**: Interactive demonstration of all tools

**Input Options**:
- `all` - Demonstrate all tools (default)
- `python-scripts` - Only Python standalone scripts
- `cli-package` - Only CLI package
- `voila-dashboard` - Only Voilà dashboard
- `notebooks` - Only Jupyter/Colab notebooks

**Jobs**:
- **demo-python-scripts**: Shows available Python scripts and usage
- **demo-cli-package**: Demonstrates CLI commands
- **demo-voila-dashboard**: Shows Voilà dashboard setup
- **demo-notebooks**: Lists available notebooks with metadata
- **demo-summary**: Overall demonstration summary

**How to Use**:
1. Go to [GitHub Actions tab](https://github.com/MK-vet/MKrep/actions)
2. Select "Quick Start Demo" workflow
3. Click "Run workflow"
4. Choose which tools to demonstrate
5. View the demonstration output in the workflow run

## Viewing Workflow Results

### From GitHub Website:

1. Navigate to https://github.com/MK-vet/MKrep/actions
2. Select a workflow from the left sidebar
3. Click on a specific run to see details
4. Expand jobs to see step-by-step execution
5. Download artifacts (like VERSION_INFO.md) if available

### Status Badges on README:

The README includes status badges that show the current state of workflows:
- 🟢 Green: All tests passing
- 🔴 Red: Tests failing
- 🟡 Yellow: Tests running

## Supported Versions

### Python Versions:
- ✅ Python 3.8
- ✅ Python 3.9
- ✅ Python 3.10
- ✅ Python 3.11
- ✅ Python 3.12

### Operating Systems:
- ✅ Ubuntu (Linux)
- ✅ Windows
- ✅ macOS

### Tools Tested:
- ✅ Standalone Python scripts
- ✅ CLI package (mkrep)
- ✅ Voilà dashboard
- ✅ Jupyter/Colab notebooks

## Workflow Files Location

All workflow files are located in:
```
.github/
└── workflows/
    ├── ci.yml              # Main CI testing
    ├── deployment.yml      # Deployment verification
    ├── version-info.yml    # Version information
    └── quickstart-demo.yml # Interactive demos
```

## Manual Workflow Triggers

Some workflows can be triggered manually:

### Using GitHub Website:
1. Go to Actions tab
2. Select a workflow from the left sidebar
3. Click "Run workflow" button
4. Select branch (usually "main")
5. Fill in any required inputs
6. Click "Run workflow"

### Using GitHub CLI:
```bash
# Trigger Quick Start Demo for all tools
gh workflow run quickstart-demo.yml -f tool_choice=all

# Trigger Quick Start Demo for CLI only
gh workflow run quickstart-demo.yml -f tool_choice=cli-package

# Trigger deployment tests
gh workflow run deployment.yml

# Trigger version info collection
gh workflow run version-info.yml
```

## CI/CD Best Practices

### What Gets Tested:
- ✅ Script syntax and imports
- ✅ Package installation
- ✅ CLI command availability
- ✅ Notebook validation
- ✅ Dependency resolution
- ✅ Cross-platform compatibility
- ✅ Multiple Python versions

### What's NOT Tested (by design):
- ❌ Full analysis runs with real data (time-intensive)
- ❌ GUI interactions (Voilà dashboard UI)
- ❌ Network-dependent operations
- ❌ Large dataset processing

The workflows focus on verifying that tools can be installed and are ready to run, not on executing complete analyses.

## Troubleshooting

### If CI Fails:

1. **Check the workflow logs**:
   - Navigate to Actions tab
   - Click on failed workflow
   - Expand failed job and step
   - Read error messages

2. **Common issues**:
   - **Missing dependencies**: Check requirements.txt
   - **Python version compatibility**: Check if using supported Python version
   - **Import errors**: Verify all source files are present
   - **Syntax errors**: Run `python -m py_compile script.py` locally

3. **Local testing**:
   ```bash
   # Test Python scripts
   python validate.py
   
   # Test CLI package
   cd python_package && pip install -e . && mkrep --help
   
   # Test Voilà
   cd huggingface_demo && voila --version
   ```

## Contributing

When adding new features:
1. Ensure workflows still pass with your changes
2. Add tests for new functionality if applicable
3. Update workflow files if adding new tools or dependencies
4. Test locally before pushing

## Version Information Artifact

The `version-info.yml` workflow generates a `VERSION_INFO.md` artifact containing:
- Python version
- All package versions
- Available CLI commands
- List of analysis scripts
- Notebook inventory

To download:
1. Go to completed "Version Info" workflow run
2. Scroll to "Artifacts" section at bottom
3. Download `version-information` artifact
4. Extract and view VERSION_INFO.md

## Summary

GitHub Actions enable:
- ✅ **Automated testing** of all tools on every commit
- ✅ **Version verification** across Python 3.8-3.12
- ✅ **Cross-platform testing** on Ubuntu, Windows, macOS
- ✅ **Interactive demos** that can be triggered on demand
- ✅ **Continuous deployment readiness** verification

All tools can be verified as working from GitHub without local installation!

## Related Documentation

- [README.md](README.md) - Main project documentation
- [INSTALLATION.md](INSTALLATION.md) - Installation instructions
- [FEATURES.md](FEATURES.md) - Complete feature list
- [python_package/README.md](python_package/README.md) - CLI package documentation
- [huggingface_demo/README.md](huggingface_demo/README.md) - Voilà dashboard documentation

## Support

For issues with GitHub Actions workflows:
- Check workflow logs in Actions tab
- Open an issue: https://github.com/MK-vet/MKrep/issues
- Include workflow name and error messages
