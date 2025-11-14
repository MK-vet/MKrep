# StrepSuis-PhyloTrait: Integrated Phylogenetic and Binary Trait Analysis
# Dynamic installation from GitHub - no code duplication

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install package from GitHub (dynamic installation)
ARG GITHUB_REPO=https://github.com/MK-vet/strepsuis-phylotrait.git
ARG BRANCH=main

RUN pip install --no-cache-dir "git+${GITHUB_REPO}@${BRANCH}"

# Create data and output directories
RUN mkdir -p /data /output

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/data
ENV OUTPUT_DIR=/output

# Default command
CMD ["strepsuis-phylotrait", "--help"]

# Usage:
# docker build -t strepsuis-phylotrait:latest .
# docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
#     strepsuis-phylotrait:latest --data-dir /data --output /output
