# Multi-stage build for StrepSuis Analyzer
# Stage 1: Builder - Install dependencies and package
FROM python:3.11-slim as builder

LABEL maintainer="MK-vet <support@strepsuis-suite.org>"
LABEL description="StrepSuis Analyzer: General-Purpose Genomic Data Analysis Tool"
LABEL version="2025.8.11"

# Install system dependencies needed for building
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy package files
WORKDIR /build
COPY pyproject.toml ./
COPY requirements.txt ./
COPY strepsuis_analyzer ./strepsuis_analyzer
COPY StrepSuisPhyloCluster_2025_08_11.py ./
COPY README.md ./

# Install the package
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir .

# Stage 2: Runtime - Minimal image with only runtime dependencies
FROM python:3.11-slim

LABEL maintainer="MK-vet <support@strepsuis-suite.org>"
LABEL description="StrepSuis Analyzer: General-Purpose Genomic Data Analysis Tool"
LABEL version="2025.8.11"

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /build/StrepSuisPhyloCluster_2025_08_11.py /app/

# Set working directory
WORKDIR /app

# Create directories for data and output
RUN mkdir -p /data /output

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/data
ENV OUTPUT_DIR=/output
ENV PATH="/opt/venv/bin:$PATH"

# Add non-root user for security
RUN useradd -m -u 1000 biouser && \
    chown -R biouser:biouser /app /data /output

# Switch to non-root user
USER biouser

# Set the entrypoint to the analysis script
ENTRYPOINT ["python", "/app/StrepSuisPhyloCluster_2025_08_11.py"]

# Default command shows help
CMD ["--help"]
