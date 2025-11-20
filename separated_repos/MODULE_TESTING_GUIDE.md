# Module Testing Guide

This guide provides step-by-step instructions for testing each of the 5 StrepSuis Suite modules to ensure they are fully functional and ready for publication.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Git
- Docker (for Docker testing)
- Google account (for Colab testing)

## Testing Strategy

Each module should be tested in 3 ways:
1. **Python Package** - Install via pip and test CLI and API
2. **Docker Container** - Build and run in containerized environment
3. **Google Colab** - Run in cloud-based notebook environment

## Module 1: strepsuis-amrvirkm

### Python Package Testing

```bash
# 1. Create clean virtual environment
cd separated_repos/strepsuis-amrvirkm
python -m venv test-env
source test-env/bin/activate  # Windows: test-env\Scripts\activate

# 2. Install package
pip install -e .

# 3. Test CLI
strepsuis-amrvirkm --version
# Expected: strepsuis-amrvirkm 1.0.0

strepsuis-amrvirkm --help
# Expected: Usage information displayed

# 4. Test with example data
strepsuis-amrvirkm --data-dir examples/basic --output test-output

# 5. Verify results
ls test-output/
# Expected: HTML report, Excel report, CSV files, PNG charts

# 6. Test Python API
python << EOF
from strepsuis_amrvirkm import ClusterAnalyzer
analyzer = ClusterAnalyzer(data_dir="examples/basic", output_dir="api-output")
results = analyzer.run()
print(f"Status: {results['status']}")
print(f"Output directory: {results['output_dir']}")
print(f"Total files generated: {results.get('total_files', 0)}")
EOF

# 7. Cleanup
deactivate
rm -rf test-env test-output api-output
```

### Docker Testing

```bash
cd separated_repos/strepsuis-amrvirkm

# 1. Build Docker image
docker build -t strepsuis-amrvirkm:test .

# 2. Test help
docker run --rm strepsuis-amrvirkm:test --help

# 3. Test with mounted data
docker run --rm \
  -v $(pwd)/examples/basic:/data \
  -v $(pwd)/docker-output:/output \
  strepsuis-amrvirkm:test \
  --data-dir /data --output /output

# 4. Verify results
ls docker-output/

# 5. Cleanup
docker rmi strepsuis-amrvirkm:test
rm -rf docker-output
```

### Google Colab Testing

1. Open `notebooks/AMRVirKM_Analysis.ipynb` in Google Colab
2. Run "Install Package" cell - verify no errors
3. Choose "Option A: Sample Data" or upload your own
4. Run "Configure Analysis" cell
5. Run "Run Analysis" cell - verify analysis completes
6. Run "Download Results" cell - verify ZIP file downloads
7. Extract ZIP and verify HTML/Excel reports

**Expected Results:**
- Installation completes without errors
- Analysis runs successfully
- Reports generate correctly
- All files can be downloaded

## Module 2: strepsuis-amrpat

### Python Package Testing

```bash
cd separated_repos/strepsuis-amrpat
python -m venv test-env
source test-env/bin/activate

pip install -e .

strepsuis-amrpat --version
strepsuis-amrpat --help

strepsuis-amrpat --data-dir examples/basic --output test-output --mdr-threshold 3

ls test-output/
# Expected: MDR analysis HTML report, Excel report, network visualizations

python << EOF
from strepsuis_amrpat import MDRAnalyzer
analyzer = MDRAnalyzer(data_dir="examples/basic", output_dir="api-output", mdr_threshold=3)
results = analyzer.run()
print(f"Analysis status: {results['status']}")
EOF

deactivate
rm -rf test-env test-output api-output
```

### Docker Testing

```bash
cd separated_repos/strepsuis-amrpat

docker build -t strepsuis-amrpat:test .

docker run --rm strepsuis-amrpat:test --help

docker run --rm \
  -v $(pwd)/examples/basic:/data \
  -v $(pwd)/docker-output:/output \
  strepsuis-amrpat:test \
  --data-dir /data --output /output --mdr-threshold 3

ls docker-output/

docker rmi strepsuis-amrpat:test
rm -rf docker-output
```

### Google Colab Testing

1. Open `notebooks/AMRPat_Analysis.ipynb`
2. Follow same steps as Module 1
3. Verify MDR-specific outputs (network graphs, association rules)

## Module 3: strepsuis-genphennet

### Python Package Testing

```bash
cd separated_repos/strepsuis-genphennet
python -m venv test-env
source test-env/bin/activate

pip install -e .

strepsuis-genphennet --version
strepsuis-genphennet --help

strepsuis-genphennet --data-dir examples/basic --output test-output

ls test-output/
# Expected: Network HTML report, Excel report, 3D visualizations

python << EOF
from strepsuis_genphennet import NetworkAnalyzer
analyzer = NetworkAnalyzer(data_dir="examples/basic", output_dir="api-output")
results = analyzer.run()
print(f"Status: {results['status']}")
EOF

deactivate
rm -rf test-env test-output api-output
```

### Docker Testing

```bash
cd separated_repos/strepsuis-genphennet

docker build -t strepsuis-genphennet:test .
docker run --rm strepsuis-genphennet:test --help

docker run --rm \
  -v $(pwd)/examples/basic:/data \
  -v $(pwd)/docker-output:/output \
  strepsuis-genphennet:test \
  --data-dir /data --output /output

ls docker-output/

docker rmi strepsuis-genphennet:test
rm -rf docker-output
```

### Google Colab Testing

1. Open `notebooks/GenPhenNet_Analysis.ipynb`
2. Complete installation and analysis steps
3. Verify network visualizations render correctly

## Module 4: strepsuis-phylotrait

### Python Package Testing

```bash
cd separated_repos/strepsuis-phylotrait
python -m venv test-env
source test-env/bin/activate

pip install -e .

strepsuis-phylotrait --version
strepsuis-phylotrait --help

# Note: This module requires a tree file
strepsuis-phylotrait --tree examples/basic/tree.newick --data-dir examples/basic --output test-output

ls test-output/
# Expected: Phylogenetic HTML report, Excel report, tree visualizations

python << EOF
from strepsuis_phylotrait import PhyloTraitAnalyzer
analyzer = PhyloTraitAnalyzer(
    tree_file="examples/basic/tree.newick",
    data_dir="examples/basic",
    output_dir="api-output"
)
results = analyzer.run()
print(f"Status: {results['status']}")
EOF

deactivate
rm -rf test-env test-output api-output
```

### Docker Testing

```bash
cd separated_repos/strepsuis-phylotrait

docker build -t strepsuis-phylotrait:test .
docker run --rm strepsuis-phylotrait:test --help

docker run --rm \
  -v $(pwd)/examples/basic:/data \
  -v $(pwd)/docker-output:/output \
  strepsuis-phylotrait:test \
  --tree /data/tree.newick --data-dir /data --output /output

ls docker-output/

docker rmi strepsuis-phylotrait:test
rm -rf docker-output
```

### Google Colab Testing

1. Open `notebooks/PhyloTrait_Analysis.ipynb`
2. Ensure tree file is uploaded/downloaded
3. Verify phylogenetic analyses complete
4. Check tree visualizations

## Module 5: strepsuis-genphen

### Python Package Testing

```bash
cd separated_repos/strepsuis-genphen
python -m venv test-env
source test-env/bin/activate

pip install -e .

strepsuis-genphen --version
strepsuis-genphen --help

strepsuis-genphen --tree examples/basic/tree.newick --data-dir examples/basic --output test-output

ls test-output/
# Expected: GenPhen HTML report with interactive UI, Excel report

python << EOF
from strepsuis_genphen import GenPhenAnalyzer
analyzer = GenPhenAnalyzer(
    tree_file="examples/basic/tree.newick",
    data_dir="examples/basic",
    output_dir="api-output"
)
results = analyzer.run()
print(f"Status: {results['status']}")
EOF

deactivate
rm -rf test-env test-output api-output
```

### Docker Testing

```bash
cd separated_repos/strepsuis-genphen

docker build -t strepsuis-genphen:test .
docker run --rm strepsuis-genphen:test --help

docker run --rm \
  -v $(pwd)/examples/basic:/data \
  -v $(pwd)/docker-output:/output \
  strepsuis-genphen:test \
  --tree /data/tree.newick --data-dir /data --output /output

ls docker-output/

docker rmi strepsuis-genphen:test
rm -rf docker-output
```

### Google Colab Testing

1. Open `notebooks/GenPhen_Analysis.ipynb`
2. Upload/download tree and data files
3. Verify interactive Bootstrap 5 UI generates
4. Test CSV export functionality

## Common Issues and Solutions

### Issue: Module not found after installation

**Solution:**
```bash
pip install --force-reinstall -e .
```

### Issue: Missing data files

**Solution:**
Ensure `examples/basic/` directory contains:
- MIC.csv
- AMR_genes.csv
- Virulence.csv
- tree.newick (for phylogenetic modules)

### Issue: Import errors in core scripts

**Solution:**
Check that all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Docker build fails

**Solution:**
Clear Docker cache and rebuild:
```bash
docker system prune -a
docker build --no-cache -t MODULE-NAME:test .
```

### Issue: Colab notebook can't find package

**Solution:**
Ensure installation cell uses correct GitHub URL:
```python
!pip install git+https://github.com/MK-vet/MODULE-NAME.git
```

## Automated Testing Script

Save this as `test_module.sh`:

```bash
#!/bin/bash
set -e

MODULE_NAME=$1
if [ -z "$MODULE_NAME" ]; then
    echo "Usage: ./test_module.sh <module-name>"
    exit 1
fi

echo "Testing $MODULE_NAME..."

# Create virtual environment
python -m venv test-env
source test-env/bin/activate

# Install module
cd separated_repos/$MODULE_NAME
pip install -e . > /dev/null 2>&1

# Test CLI
echo "Testing CLI..."
$MODULE_NAME --version
$MODULE_NAME --help > /dev/null

# Test with example data
echo "Testing with example data..."
if [ "$MODULE_NAME" == "strepsuis-phylotrait" ] || [ "$MODULE_NAME" == "strepsuis-genphen" ]; then
    $MODULE_NAME --tree examples/basic/tree.newick --data-dir examples/basic --output test-output
else
    $MODULE_NAME --data-dir examples/basic --output test-output
fi

# Check outputs
echo "Checking outputs..."
if [ -d "test-output" ]; then
    FILE_COUNT=$(ls test-output/ | wc -l)
    echo "Generated $FILE_COUNT files"
    if [ $FILE_COUNT -gt 0 ]; then
        echo "✓ $MODULE_NAME passed all tests"
    else
        echo "✗ $MODULE_NAME failed: No output files generated"
        exit 1
    fi
else
    echo "✗ $MODULE_NAME failed: Output directory not created"
    exit 1
fi

# Cleanup
cd ../..
deactivate
rm -rf test-env separated_repos/$MODULE_NAME/test-output

echo "All tests passed for $MODULE_NAME!"
```

Usage:
```bash
chmod +x test_module.sh
./test_module.sh strepsuis-amrvirkm
./test_module.sh strepsuis-amrpat
./test_module.sh strepsuis-genphennet
./test_module.sh strepsuis-phylotrait
./test_module.sh strepsuis-genphen
```

## Success Criteria

Each module passes when:
- ✓ CLI `--version` and `--help` work
- ✓ Analysis completes without errors
- ✓ HTML report is generated
- ✓ Excel report is generated
- ✓ CSV files are created
- ✓ Docker container builds and runs
- ✓ Colab notebook executes end-to-end
- ✓ Python API returns successful results

## Reporting Issues

If a module fails testing:
1. Note which test failed
2. Capture error messages
3. Check log files in output directory
4. Verify all dependencies are installed
5. Check example data files exist and are valid
6. Report issue with full details

---

**Last Updated:** 2025-11-20  
**For:** StrepSuis Suite Publication Testing  
**Version:** 1.0.0
