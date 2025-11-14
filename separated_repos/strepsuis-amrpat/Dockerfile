FROM python:3.11-slim

LABEL maintainer="MK-vet <support@strepsuis-suite.org>"
LABEL description="StrepSuis-AMRPat: Automated Detection of Antimicrobial Resistance Patterns"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install the package directly from GitHub
# This ensures no code duplication - the package is installed dynamically
RUN pip install --no-cache-dir git+https://github.com/MK-vet/strepsuis-amrpat.git

# Create directories for data and output
RUN mkdir -p /data /output

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/data
ENV OUTPUT_DIR=/output

# Set the entrypoint to the CLI command
ENTRYPOINT ["strepsuis-amrpat"]

# Default command shows help
CMD ["--help"]
