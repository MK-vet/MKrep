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
RUN mkdir -p /data /output

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MKREP_DATA_DIR=/data
ENV MKREP_OUTPUT_DIR=/output

# Go back to app directory
WORKDIR /app

# Default command shows help
CMD ["mkrep", "--help"]

# Usage examples:
# Build: docker build -t mkrep:latest .
# Run cluster analysis: docker run -v $(pwd)/data:/data -v $(pwd)/output:/output mkrep:latest mkrep-cluster --data-dir /data --output /output
# Run MDR analysis: docker run -v $(pwd)/data:/data -v $(pwd)/output:/output mkrep:latest mkrep-mdr --data-dir /data --output /output
# Interactive shell: docker run -it -v $(pwd)/data:/data -v $(pwd)/output:/output mkrep:latest /bin/bash
