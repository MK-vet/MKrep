# StrepSuis-AMRVirKM Docker Image
# This Dockerfile installs the package dynamically from the repository
# No code duplication - installs the package at build time

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install the package directly from GitHub
# This ensures no code duplication - the package is installed dynamically
ARG GITHUB_REPO=https://github.com/MK-vet/strepsuis-amrvirkm.git
ARG BRANCH=main

RUN pip install --no-cache-dir "git+${GITHUB_REPO}@${BRANCH}"

# Create directories for data and output
RUN mkdir -p /data /output

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/data
ENV OUTPUT_DIR=/output

# Default command - show help
CMD ["strepsuis-amrvirkm", "--help"]

# Usage:
# docker build -t strepsuis-amrvirkm:latest .
# docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
#     strepsuis-amrvirkm:latest \
#     --data-dir /data --output /output
