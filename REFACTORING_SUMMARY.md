# Repository Refactoring Summary

## Overview
This document summarizes the major restructuring performed on the MKrep repository to improve organization, maintainability, and adherence to Python project conventions.

## Changes Made

### 1. Directory Structure
Created a clean, standard Python project structure:

```
MKrep/
├── data/              # All data files (CSV, newick)
├── src/               # Main analysis scripts
├── tests/             # All test files
├── docs/              # Documentation (except README.md)
├── output/            # Analysis output (gitignored)
└── README.md          # Main documentation
```

### 2. Data Files (`data/`)
Moved all data files to a dedicated directory:
- `*.csv` files (MIC, AMR_genes, Virulence, MLST, Serotype, Plasmid, MGE, merged_resistance_data)
- `*.newick` tree files (Snp_tree.newick)

**Impact:** Scripts now reference `data/` for input files

### 3. Source Code (`src/`)
Renamed and moved analysis scripts with standardized naming:

| Old Name | New Name |
|----------|----------|
| `MDR_2025_04_15.py` | `src/mdr_analysis.py` |
| `Network_Analysis_2025_06_26.py` | `src/network_analysis.py` |
| `Phylogenetic_clustering_2025_03_21.py` | `src/phylogenetic_clustering.py` |
| `StrepSuisPhyloCluster_2025_08_11.py` | `src/strep_suis_phylo_cluster.py` |
| `Cluster_MIC_AMR_Viruelnce.py` | `src/cluster_mic_amr_virulence.py` |

**Benefits:**
- Removed hardcoded dates from filenames
- Fixed typo: "Viruelnce" → "virulence"
- Consistent snake_case naming
- Clear separation of source code

### 4. Tests (`tests/`)
Moved all test files to a dedicated directory:
- All `test_*.py` files
- Created `tests/__init__.py`
- Updated import statements to use `from src.module_name import ...`

**Impact:** Tests now properly import from the `src/` package

### 5. Documentation (`docs/`)
Moved all documentation to a central location:
- `BINARY_DATA_GUIDE.md`
- `DOCKER_DEPLOYMENT.md`
- `EXAMPLE_RESULTS.md`
- `FEATURES.md`
- `GITHUB_ACTIONS.md`
- `INSTALLATION.md`
- `INTERPRETATION_GUIDE.md`
- `QUICK_START.md`
- `USER_GUIDE.md`

**Note:** `README.md` remains in the root directory as the main entry point

### 6. Configuration Updates

#### `.gitignore`
Added exclusions for generated files:
- `ANALYSIS_RESULTS.txt`
- `IMPLEMENTATION_VERIFICATION.txt`
- `TASK_COMPLETION_SUMMARY.txt`
- `module_verification_report.json`

#### `Dockerfile`
- Updated to reflect new directory structure
- Data mounted at `/app/data`
- Output at `/app/output`
- Added `PYTHONPATH=/app` to environment

#### `docker-compose.yml`
- Updated volume mounts: `./data:/app/data`
- Updated commands to use `python src/script_name.py`
- Environment variables adjusted for new paths

### 7. Script Updates

All scripts updated to reference new paths:

#### Data File References
- Changed from `MIC.csv` to `data/MIC.csv`
- Changed from `Snp_tree.newick` to `data/Snp_tree.newick`
- Fixed `Virulence3.csv` → `Virulence.csv` (standardized filename)

#### Wrapper Scripts
- `run_mdr_analysis.py` - Updated imports and paths
- `run_cluster_analysis.py` - Updated file checks and imports
- `run_phylogenetic_analysis.py` - Updated script path
- `run_all_analyses.py` - Updated all module configurations
- `validate.py` - Updated script paths

#### Main Documentation
- `README.md` - Updated all command examples and script references

## Migration Guide

### For Users

**Running Scripts:**
```bash
# Old way
python MDR_2025_04_15.py

# New way
python src/mdr_analysis.py
```

**Using Docker:**
```bash
# Old way
docker run -v $(pwd)/data:/data mkrep:latest mkrep-mdr

# New way
docker run -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output mkrep:latest python src/mdr_analysis.py
```

**Data Files:**
Ensure all data files are in the `data/` directory before running analyses.

### For Developers

**Importing Modules:**
```python
# Old way (from root)
from MDR_2025_04_15 import function_name

# New way (from src package)
from src.mdr_analysis import function_name
```

**Running Tests:**
```bash
# Tests are now in tests/ directory
cd /path/to/MKrep
python -m pytest tests/

# Or run specific test
python -m pytest tests/test_mdr_analysis.py
```

**Adding New Scripts:**
- Place new analysis scripts in `src/`
- Use snake_case naming
- Reference data files as `data/filename.csv`
- Add corresponding tests in `tests/`

## Backward Compatibility

⚠️ **Breaking Changes:**
- Old script names no longer exist in root directory
- Direct imports of old module names will fail
- Data files must be in `data/` directory

## Benefits

1. **Organization:** Clear separation of code, data, tests, and documentation
2. **Maintainability:** Standardized naming makes code easier to find and maintain
3. **Professionalism:** Follows Python project best practices
4. **Scalability:** Easier to add new modules and tests
5. **Docker-Ready:** Clean separation supports containerization
6. **Version Control:** Cleaner git history without dated filenames

## Testing

Verified functionality:
- ✅ Scripts can be imported from `src/` package
- ✅ Data files accessible from `data/` directory
- ✅ Test files can import from `src/` modules
- ✅ Docker configuration updated correctly
- ✅ Documentation references updated

## Next Steps

1. Run full test suite to verify all functionality
2. Update CI/CD pipelines if applicable
3. Rebuild Docker images with new structure
4. Update any external documentation or tutorials

## Questions or Issues?

If you encounter any issues with the new structure:
1. Check that data files are in `data/` directory
2. Verify you're using the new script paths (`src/`)
3. Ensure imports use `from src.module import ...`
4. Refer to this guide or the updated README.md

---
**Refactoring Date:** December 2, 2025
**Status:** Complete ✅
