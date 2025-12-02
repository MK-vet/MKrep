# MKrep - Microbial Genomics Analysis Pipeline
# Docker image for running MKrep in containerized environments

FROM python:3.11-slim

LABEL maintainer="MK-vet"
LABEL description="Comprehensive bioinformatics analysis pipeline for microbial genomics"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . /app/

# Install the package in development mode
WORKDIR /app/python_package
RUN pip install -e .

# Create directories for data and output
RUN mkdir -p /app/data /app/output

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:${PYTHONPATH}
ENV MKREP_DATA_DIR=/app/data
ENV MKREP_OUTPUT_DIR=/app/output

# Go back to app directory
WORKDIR /app

# Default command shows help
CMD ["mkrep", "--help"]

# Usage examples:
# Build: docker build -t mkrep:latest .
# Run cluster analysis: docker run -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output mkrep:latest python src/cluster_mic_amr_virulence.py
# Run MDR analysis: docker run -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output mkrep:latest python src/mdr_analysis.py
# Run network analysis: docker run -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output mkrep:latest python src/network_analysis.py
# Run phylogenetic analysis: docker run -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output mkrep:latest python src/phylogenetic_clustering.py
# Interactive shell: docker run -it -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output mkrep:latest /bin/bash
