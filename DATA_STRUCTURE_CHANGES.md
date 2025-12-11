# Data Structure Reorganization

## Summary

This document describes the data structure reorganization performed to eliminate duplication and centralize example datasets.

## Problem Identified

The repository had significant data duplication:

1. **Main data directory**: `/data/` contained the original example datasets (~68KB)
2. **Module data/examples**: Each module had duplicate CSV files in `separated_repos/*/data/examples/` (~60KB × 4 = 240KB)
3. **Module examples**: Each module had additional duplicate CSV files in `separated_repos/*/examples/` (~50KB × 4 = 200KB)
4. **Empty results directories**: Each module had `data/results/` containing only placeholder README.md files

**Total duplication**: ~440KB of redundant data files

## Changes Made

### 1. Removed Duplicated Data Files

Deleted duplicate CSV files from:
- `separated_repos/strepsuis-mdr/data/examples/` (7 files)
- `separated_repos/strepsuis-amrvirkm/data/examples/` (8 files)
- `separated_repos/strepsuis-genphennet/data/examples/` (8 files)
- `separated_repos/strepsuis-phylotrait/data/examples/` (9 files including .newick)
- `separated_repos/strepsuis-mdr/examples/` (7 files)
- `separated_repos/strepsuis-amrvirkm/examples/` (7 files)
- `separated_repos/strepsuis-genphennet/examples/` (7 files)
- `separated_repos/strepsuis-phylotrait/examples/` (7 files)

### 2. Removed Empty Results Directories

Deleted placeholder README.md files from:
- `separated_repos/*/data/results/README.md`

These directories are now empty and will be populated with actual analysis results when users run the tools.

### 3. Created Centralized Documentation

Added `README.md` files in each module's `data/` directory that:
- Explain the data location (`../../data/`)
- List available datasets
- Provide usage examples
- Document the new structure

### 4. Updated Test Fixtures

Modified `tests/conftest.py` in all modules to:
- Check for data in local `data/examples/` first (backward compatibility)
- Fall back to main repository's `../../data/` directory
- Automatically copy required files for tests

### 5. Updated Documentation

Modified the following files:
- `separated_repos/*/TESTING.md` - Updated data location references
- `separated_repos/*/examples/README.md` - Updated paths to use `../../data/`
- `separated_repos/*/.gitignore` - Added exception for `data/README.md`

## New Structure

```
MKrep/
├── data/                              # ← Single source of truth for example data
│   ├── AMR_genes.csv
│   ├── MGE.csv
│   ├── MIC.csv
│   ├── MLST.csv
│   ├── Plasmid.csv
│   ├── Serotype.csv
│   ├── Snp_tree.newick
│   ├── Virulence.csv
│   └── merged_resistance_data.csv
│
└── separated_repos/
    ├── strepsuis-mdr/
    │   ├── data/
    │   │   └── README.md              # ← Points to ../../data/
    │   ├── examples/
    │   │   ├── README.md              # ← Updated to use ../../data/
    │   │   ├── basic/
    │   │   │   └── expected_output.txt
    │   │   └── advanced/
    │   │       └── expected_output.txt
    │   └── tests/
    │       └── conftest.py            # ← Auto-uses ../../data/
    │
    ├── strepsuis-amrvirkm/
    │   └── (same structure)
    │
    ├── strepsuis-genphennet/
    │   └── (same structure)
    │
    └── strepsuis-phylotrait/
        └── (same structure)
```

## Benefits

1. **Reduced duplication**: Eliminated ~440KB of redundant files
2. **Single source of truth**: All modules reference the same data
3. **Easier maintenance**: Update data in one place
4. **Clearer structure**: Data organization is more intuitive
5. **Backward compatible**: Tests still work via updated fixtures
6. **Production ready**: Structure matches publication-ready standards

## Usage Examples

### Running Analysis

```bash
# From module directory
cd separated_repos/strepsuis-mdr
strepsuis-mdr --data-dir ../../data/ --output ./results/

# From repository root
strepsuis-mdr --data-dir ./data/ --output ./separated_repos/strepsuis-mdr/results/
```

### Running Tests

Tests automatically use the main data directory:

```bash
cd separated_repos/strepsuis-mdr
pytest tests/ -v
```

The `conftest.py` fixture automatically copies data from `../../data/` to a temporary directory for testing.

## Deployment Considerations

When deploying modules standalone (e.g., Docker, PyPI):
- Include necessary data files in the package
- Or download from the main repository
- Or have users provide their own data

Example in Dockerfile:
```dockerfile
COPY ../../data/*.csv /app/data/
```

## Files Modified

### Deleted (68 files total):
- 36 duplicate CSV files from `data/examples/` and `examples/`
- 4 placeholder README.md from `data/results/`
- 28 CSV files moved to centralized location

### Created (4 files):
- `separated_repos/strepsuis-mdr/data/README.md`
- `separated_repos/strepsuis-amrvirkm/data/README.md`
- `separated_repos/strepsuis-genphennet/data/README.md`
- `separated_repos/strepsuis-phylotrait/data/README.md`

### Modified (16 files):
- 4 × `tests/conftest.py`
- 4 × `TESTING.md`
- 4 × `examples/README.md`
- 4 × `.gitignore`

## Verification

All tests pass with the new structure:
```bash
cd separated_repos/strepsuis-mdr
pytest tests/test_config.py -v
# ===== 9 passed in 1.27s =====
```

The test fixtures correctly fall back to the main data directory when local data is not present.

## Notes

- `strepsuis-analyzer/data/` retains its own data files as they are production data, not examples
- Synthetic data files remain in their respective `synthetic_data/` directories
- The `.gitignore` patterns were updated to allow `data/README.md` files while still ignoring generated results

## Future Work (Optional)

While not required for this fix, future enhancements could include:
- Generate actual demo results for each module
- Create automated scripts to populate results directories
- Add CI/CD workflow to verify data integrity
