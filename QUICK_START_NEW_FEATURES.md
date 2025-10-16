# Quick Start Guide - New Features

This guide covers the newly added deployment options for MKrep.

## 🎯 Choose Your Method

### 1. Interactive Colab (No Coding!) ⭐ **RECOMMENDED FOR BEGINNERS**

**Perfect for:** Non-programmers, quick analysis, demonstrations

**Time to start:** 3 minutes

**Steps:**
1. Click: [Interactive Analysis Colab](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Interactive_Analysis_Colab.ipynb)
2. Run the first 2 cells (installation)
3. Upload your CSV files
4. Select analysis type from dropdown
5. Adjust parameters with sliders
6. Click "Run Analysis"
7. Download results

**No programming knowledge required!**

See [Interactive Notebook Guide](colab_notebooks/INTERACTIVE_NOTEBOOK_GUIDE.md) for details.

---

### 2. Docker Container 🐳 **RECOMMENDED FOR TEAMS**

**Perfect for:** Consistent environments, team collaboration, production use

**Time to start:** 10 minutes

**Prerequisites:**
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Your data in `data/` folder

**Quick Start:**
```bash
# Clone repository
git clone https://github.com/MK-vet/MKrep.git
cd MKrep

# Prepare data
mkdir -p data output
cp your_data/*.csv data/

# Build and run
docker build -t mkrep:latest .
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
    mkrep:latest mkrep-cluster --data-dir /data --output /output
```

**OR use Docker Compose:**
```bash
# Build
docker-compose build

# Run cluster analysis
docker-compose up mkrep-cluster

# Results will be in output/ folder
```

See [Docker Deployment Guide](DOCKER_DEPLOYMENT.md) for complete documentation.

---

### 3. Docker in Google Colab 🐳☁️ **ADVANCED**

**Perfect for:** Testing Docker deployment without local installation

**Steps:**
```python
# In a Colab notebook

# Install Docker
!apt-get update
!apt-get install -y docker.io
!systemctl start docker

# Clone and build
!git clone https://github.com/MK-vet/MKrep.git
%cd MKrep
!docker build -t mkrep:latest .

# Upload data
from google.colab import files
!mkdir -p data
uploaded = files.upload()
for f in uploaded.keys():
    !mv {f} data/

# Run analysis
!docker run \
    -v $(pwd)/data:/data \
    -v $(pwd)/output:/output \
    mkrep:latest mkrep-cluster \
    --data-dir /data \
    --output /output

# Download results
!zip -r results.zip output/
files.download('results.zip')
```

---

## 📊 Comparison of New Options

| Feature | Interactive Colab | Docker Local | Docker in Colab |
|---------|------------------|--------------|-----------------|
| **Coding Required** | ❌ No | ⚠️ Minimal | ⚠️ Some |
| **Setup Time** | ⭐⭐⭐⭐⭐ 3 min | ⭐⭐⭐⭐ 10 min | ⭐⭐⭐ 15 min |
| **Reproducibility** | ⭐⭐⭐⭐ High | ⭐⭐⭐⭐⭐ Perfect | ⭐⭐⭐⭐⭐ Perfect |
| **Portability** | ⭐⭐⭐⭐⭐ Cloud | ⭐⭐⭐⭐⭐ Anywhere | ⭐⭐⭐⭐⭐ Cloud |
| **Customization** | ⭐⭐ Limited | ⭐⭐⭐⭐⭐ Full | ⭐⭐⭐⭐⭐ Full |
| **Team Use** | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Good |
| **Best For** | Beginners | Production | Testing |

---

## 🔄 Workflow Examples

### Example 1: Quick Exploration (Interactive Colab)

**Scenario:** You want to quickly explore your data without installing anything.

```
1. Open Interactive Colab notebook
2. Upload MIC.csv, AMR_genes.csv, Virulence.csv
3. Select "Cluster Analysis"
4. Keep default parameters
5. Click "Run Analysis"
6. Download and review HTML report
Total time: ~15 minutes
```

---

### Example 2: Production Analysis (Docker)

**Scenario:** You need reproducible results for publication.

```bash
# Setup (once)
git clone https://github.com/MK-vet/MKrep.git
cd MKrep
docker build -t mkrep:1.0.0 .

# For each dataset
cp dataset1/*.csv data/
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
    mkrep:1.0.0 mkrep-cluster \
    --data-dir /data \
    --output /output \
    --bootstrap 1000 \
    --random-seed 42

# Results in output/
```

**Benefits:**
- Exact same environment every time
- Version controlled (mkrep:1.0.0)
- Reproducible with fixed seed
- Can share Docker image with reviewers

---

### Example 3: Batch Processing (Docker Compose)

**Scenario:** You have multiple datasets to analyze.

```bash
# Setup once
git clone https://github.com/MK-vet/MKrep.git
cd MKrep

# Process dataset 1
cp dataset1/*.csv data/
docker-compose up mkrep-cluster
mv output/ results_dataset1/

# Process dataset 2
cp dataset2/*.csv data/
docker-compose up mkrep-mdr
mv output/ results_dataset2/

# Process dataset 3
cp dataset3/*.csv data/
docker-compose up mkrep-network
mv output/ results_dataset3/
```

---

## 🆘 Common Issues and Solutions

### Issue: "Permission denied" in Docker

**Solution:**
```bash
# Linux/Mac
sudo chown -R $USER:$USER output/

# Or run with your user ID
docker run -u $(id -u):$(id -g) \
    -v $(pwd)/data:/data -v $(pwd)/output:/output \
    mkrep:latest mkrep-cluster --data-dir /data --output /output
```

---

### Issue: Colab runs out of memory

**Solutions:**
1. Use Google Colab Pro (more RAM)
2. Reduce bootstrap iterations (e.g., 100 instead of 500)
3. Reduce number of features in your dataset
4. Use Docker locally instead

---

### Issue: Docker build fails

**Solution:**
```bash
# Clean up Docker
docker system prune -a

# Rebuild without cache
docker build --no-cache -t mkrep:latest .

# Check disk space
df -h
docker system df
```

---

### Issue: Notebook upload fails in Colab

**Solutions:**
1. Check file size (Colab has limits)
2. Ensure files are valid CSV format
3. Try uploading files one at a time
4. Check for special characters in filenames

---

## 📚 Next Steps

After running your first analysis:

1. **Review results:**
   - Open HTML report in browser
   - Check Excel workbook for detailed tables
   - View PNG charts for publication

2. **Learn more:**
   - Read [Interpretation Guide](INTERPRETATION_GUIDE.md)
   - Check [User Guide](USER_GUIDE.md) for advanced features
   - Review [Docker Guide](DOCKER_DEPLOYMENT.md) for more options

3. **Customize:**
   - Try different parameters
   - Run multiple analysis types
   - Combine results from different analyses

4. **Share:**
   - Share Docker images with colleagues
   - Share Colab notebooks with collaborators
   - Include methods in publications

---

## 💡 Pro Tips

### For Faster Analysis:
- Use Colab Pro for large datasets
- Reduce bootstrap iterations for testing
- Use Docker with adequate CPU/RAM allocation

### For Better Results:
- Use 500+ bootstrap iterations for publication
- Try multiple parameter combinations
- Include all optional data files when available
- Use consistent random seed for reproducibility

### For Team Collaboration:
- Use Docker for consistent environments
- Version your Docker images (e.g., mkrep:1.0.0)
- Document parameters used in each analysis
- Share docker-compose.yml with team

---

## 🎓 Learning Path

**Level 1 - Beginner:**
1. Use Interactive Colab notebook
2. Upload sample data
3. Run with default parameters
4. Review HTML report

**Level 2 - Intermediate:**
1. Try advanced Colab notebooks (with code)
2. Experiment with different parameters
3. Compare results from different analyses
4. Use Docker Compose for batch processing

**Level 3 - Advanced:**
1. Build custom Docker images
2. Modify analysis scripts
3. Create custom workflows
4. Deploy in cloud environments (AWS, GCP, Azure)

---

## 📞 Getting Help

**For Interactive Colab:**
- [Interactive Notebook Guide](colab_notebooks/INTERACTIVE_NOTEBOOK_GUIDE.md)
- [Colab README](colab_notebooks/README.md)

**For Docker:**
- [Docker Deployment Guide](DOCKER_DEPLOYMENT.md)
- [Docker Documentation](https://docs.docker.com/)

**For General Issues:**
- [User Guide](USER_GUIDE.md)
- [GitHub Issues](https://github.com/MK-vet/MKrep/issues)
- [Installation Guide](INSTALLATION.md)

---

**Ready to start?** Choose your method above and begin analyzing!

🎯 **Recommendation:** If you're new to bioinformatics analysis or programming, start with the [Interactive Colab notebook](https://colab.research.google.com/github/MK-vet/MKrep/blob/main/colab_notebooks/Interactive_Analysis_Colab.ipynb).
