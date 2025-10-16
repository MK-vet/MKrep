# Docker Deployment Guide for MKrep

This guide explains how to use MKrep in Docker containers for maximum portability and consistency across different environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Building the Docker Image](#building-the-docker-image)
4. [Running Analyses](#running-analyses)
5. [Docker Compose](#docker-compose)
6. [Using Docker in Google Colab](#using-docker-in-google-colab)
7. [Advanced Usage](#advanced-usage)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### Local Installation
- Docker Engine 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose 1.29+ (usually included with Docker Desktop)
- At least 4GB of free disk space
- 2GB+ RAM available for containers

### Google Colab
- Google account (for Google Colab)
- No local installation required!

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/MK-vet/MKrep.git
cd MKrep
```

### 2. Prepare Your Data

Create a `data` directory and add your CSV files:

```bash
mkdir -p data output
cp your_data/*.csv data/
```

### 3. Build and Run

```bash
# Build the Docker image
docker build -t mkrep:latest .

# Run cluster analysis
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
    mkrep:latest mkrep-cluster --data-dir /data --output /output
```

That's it! Your results will be in the `output` directory.

## Building the Docker Image

### Standard Build

```bash
docker build -t mkrep:latest .
```

### Build with Specific Tag

```bash
docker build -t mkrep:1.0.0 .
```

### Build with Docker Compose

```bash
docker-compose build
```

### Verify the Build

```bash
# Check the image exists
docker images | grep mkrep

# Test the image
docker run mkrep:latest mkrep --version
```

## Running Analyses

### General Syntax

```bash
docker run \
    -v $(pwd)/data:/data \
    -v $(pwd)/output:/output \
    mkrep:latest [command] [options]
```

### Cluster Analysis

```bash
docker run \
    -v $(pwd)/data:/data \
    -v $(pwd)/output:/output \
    mkrep:latest mkrep-cluster \
    --data-dir /data \
    --output /output \
    --bootstrap 500 \
    --max-clusters 8
```

**Required files in `data/`:**
- `MIC.csv`
- `AMR_genes.csv`
- `Virulence.csv`

### MDR Analysis

```bash
docker run \
    -v $(pwd)/data:/data \
    -v $(pwd)/output:/output \
    mkrep:latest mkrep-mdr \
    --data-dir /data \
    --output /output \
    --mdr-threshold 3
```

**Required files in `data/`:**
- `MIC.csv`
- `AMR_genes.csv`

### Network Analysis

```bash
docker run \
    -v $(pwd)/data:/data \
    -v $(pwd)/output:/output \
    mkrep:latest mkrep-network \
    --data-dir /data \
    --output /output
```

**Required files in `data/`:**
- `MGE.csv`
- `MIC.csv`
- `MLST.csv`
- `Plasmid.csv`
- `Serotype.csv`
- `Virulence.csv`
- `AMR_genes.csv`

### Phylogenetic Analysis

```bash
docker run \
    -v $(pwd)/data:/data \
    -v $(pwd)/output:/output \
    mkrep:latest mkrep-phylo \
    --tree /data/tree.newick \
    --data-dir /data \
    --output /output
```

**Required files in `data/`:**
- `tree.newick` (phylogenetic tree)
- `MIC.csv`
- `AMR_genes.csv`
- `Virulence.csv`

### Streptococcus suis Analysis

```bash
docker run \
    -v $(pwd)/data:/data \
    -v $(pwd)/output:/output \
    mkrep:latest mkrep-strepsuis \
    --tree /data/tree.newick \
    --data-dir /data \
    --output /output
```

**Required files in `data/`:**
- `tree.newick` (phylogenetic tree)
- `MIC.csv`
- `AMR_genes.csv`
- `Virulence.csv`

## Docker Compose

Docker Compose provides a simpler way to run analyses with predefined configurations.

### List Available Services

```bash
docker-compose config --services
```

### Run Specific Analysis

```bash
# Cluster analysis
docker-compose up mkrep-cluster

# MDR analysis
docker-compose up mkrep-mdr

# Network analysis
docker-compose up mkrep-network

# Phylogenetic analysis
docker-compose up mkrep-phylo

# Streptococcus suis analysis
docker-compose up mkrep-strepsuis
```

### Run in Detached Mode

```bash
docker-compose up -d mkrep-cluster
```

### View Logs

```bash
# Follow logs in real-time
docker-compose logs -f mkrep-cluster

# View last 100 lines
docker-compose logs --tail=100 mkrep-cluster
```

### Stop Services

```bash
docker-compose down
```

### Clean Up

```bash
# Remove containers and networks
docker-compose down

# Remove containers, networks, and volumes
docker-compose down -v

# Remove everything including images
docker-compose down --rmi all -v
```

## Using Docker in Google Colab

Yes, you can run Docker containers in Google Colab! Here's how:

### 1. Install Docker in Colab

```python
# Run this in a Colab cell
!apt-get update
!apt-get install -y docker.io
!systemctl start docker
```

### 2. Clone Repository and Build

```python
# Clone the repository
!git clone https://github.com/MK-vet/MKrep.git
%cd MKrep

# Build Docker image
!docker build -t mkrep:latest .
```

### 3. Prepare Data

```python
# Upload files from local computer
from google.colab import files
import os

# Create data directory
!mkdir -p data output

# Upload CSV files
uploaded = files.upload()
for filename in uploaded.keys():
    !mv {filename} data/
```

### 4. Run Analysis

```python
# Run cluster analysis
!docker run \
    -v $(pwd)/data:/data \
    -v $(pwd)/output:/output \
    mkrep:latest mkrep-cluster \
    --data-dir /data \
    --output /output

# List output files
!ls -lh output/
```

### 5. Download Results

```python
# Download results
from google.colab import files

# Download HTML report
html_files = !ls output/*.html
for f in html_files:
    files.download(f)

# Download Excel report
xlsx_files = !ls output/*.xlsx
for f in xlsx_files:
    files.download(f)

# Create ZIP of all results
!cd output && zip -r ../results.zip . && cd ..
files.download('results.zip')
```

### Complete Colab Example

Here's a complete notebook cell sequence:

```python
# Cell 1: Setup
!apt-get update && apt-get install -y docker.io
!systemctl start docker
!git clone https://github.com/MK-vet/MKrep.git
%cd MKrep
!docker build -t mkrep:latest .

# Cell 2: Upload data
from google.colab import files
!mkdir -p data output
uploaded = files.upload()
for filename in uploaded.keys():
    !mv {filename} data/

# Cell 3: Run analysis
!docker run \
    -v $(pwd)/data:/data \
    -v $(pwd)/output:/output \
    mkrep:latest mkrep-cluster \
    --data-dir /data \
    --output /output \
    --bootstrap 500 \
    --max-clusters 8

# Cell 4: Download results
!cd output && zip -r ../results.zip . && cd ..
files.download('results.zip')
```

## Advanced Usage

### Interactive Shell

Access the container shell for debugging or manual operations:

```bash
docker run -it \
    -v $(pwd)/data:/data \
    -v $(pwd)/output:/output \
    mkrep:latest /bin/bash
```

### Custom Python Scripts

Run custom Python scripts inside the container:

```bash
# Create a custom script
cat > custom_analysis.py << 'EOF'
import pandas as pd
print("Running custom analysis...")
# Your analysis code here
EOF

# Run it in the container
docker run \
    -v $(pwd):/workspace \
    -w /workspace \
    mkrep:latest python custom_analysis.py
```

### Environment Variables

Set custom environment variables:

```bash
docker run \
    -e MKREP_LOG_LEVEL=DEBUG \
    -e MKREP_RANDOM_SEED=12345 \
    -v $(pwd)/data:/data \
    -v $(pwd)/output:/output \
    mkrep:latest mkrep-cluster \
    --data-dir /data \
    --output /output
```

### Resource Limits

Limit CPU and memory usage:

```bash
docker run \
    --cpus=2 \
    --memory=4g \
    -v $(pwd)/data:/data \
    -v $(pwd)/output:/output \
    mkrep:latest mkrep-cluster \
    --data-dir /data \
    --output /output
```

### Persistent Logs

Save logs to a file:

```bash
docker run \
    -v $(pwd)/data:/data \
    -v $(pwd)/output:/output \
    -v $(pwd)/logs:/logs \
    mkrep:latest mkrep-cluster \
    --data-dir /data \
    --output /output \
    2>&1 | tee logs/analysis.log
```

## Troubleshooting

### Permission Issues

If you get permission errors accessing output files:

```bash
# Fix permissions (Linux/Mac)
sudo chown -R $USER:$USER output/

# Or run container with your user ID
docker run \
    -u $(id -u):$(id -g) \
    -v $(pwd)/data:/data \
    -v $(pwd)/output:/output \
    mkrep:latest mkrep-cluster \
    --data-dir /data \
    --output /output
```

### Out of Memory

If analysis fails due to memory:

```bash
# Increase memory limit
docker run \
    --memory=8g \
    --memory-swap=12g \
    -v $(pwd)/data:/data \
    -v $(pwd)/output:/output \
    mkrep:latest mkrep-cluster \
    --data-dir /data \
    --output /output \
    --bootstrap 100  # Reduce iterations
```

### Build Failures

If Docker build fails:

```bash
# Clean up and rebuild
docker system prune -a
docker build --no-cache -t mkrep:latest .

# Check system resources
docker system df
```

### Container Won't Start

Check container logs:

```bash
# List all containers
docker ps -a

# View logs for specific container
docker logs [container_id]

# Remove stuck containers
docker rm [container_id]
```

### Data Not Found

Verify volume mounts:

```bash
# Check mount points
docker inspect [container_id] | grep -A 10 Mounts

# Test with simple command
docker run \
    -v $(pwd)/data:/data \
    mkrep:latest ls -la /data
```

## Best Practices

### 1. Data Organization

```
MKrep/
├── data/               # Input data (mounted to /data)
│   ├── MIC.csv
│   ├── AMR_genes.csv
│   └── Virulence.csv
├── output/             # Results (mounted to /output)
├── logs/               # Analysis logs
└── docker-compose.yml
```

### 2. Version Control

Always tag your images with versions:

```bash
docker build -t mkrep:1.0.0 .
docker tag mkrep:1.0.0 mkrep:latest
```

### 3. Regular Cleanup

Clean up unused resources:

```bash
# Remove unused images
docker image prune

# Remove unused containers
docker container prune

# Remove everything unused
docker system prune -a
```

### 4. Backup Important Data

Always keep backups of:
- Input data files
- Generated reports
- Configuration files

### 5. Monitor Resource Usage

```bash
# Real-time stats
docker stats

# Container resource usage
docker stats [container_name]
```

## Support

For issues with Docker deployment:

1. Check the [troubleshooting section](#troubleshooting) above
2. Review Docker logs: `docker logs [container_name]`
3. Open an issue on [GitHub](https://github.com/MK-vet/MKrep/issues)
4. Include:
   - Docker version: `docker --version`
   - Docker Compose version: `docker-compose --version`
   - OS and version
   - Full error messages from logs

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [MKrep User Guide](USER_GUIDE.md)
- [MKrep Installation Guide](INSTALLATION.md)

---

**MKrep Docker Deployment** - Run anywhere, anytime!
