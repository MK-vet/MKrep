#!/usr/bin/env python
"""
Setup script for StrepSuis-AMRVirKM

This setup.py is provided for backward compatibility.
The project primarily uses pyproject.toml for configuration.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="strepsuis-phylotrait",
    version="1.0.0",
    description="Integrated Phylogenetic and Binary Trait Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MK-vet",
    author_email="contact@example.com",
    url="https://github.com/MK-vet/strepsuis-phylotrait",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "plotly>=5.0.0",
        "scikit-learn>=1.0.0",
        "kmodes>=0.12.0",
        "prince>=0.7.0",
        "mlxtend>=0.19.0",
        "jinja2>=3.0.0",
        "openpyxl>=3.0.0",
        "xlsxwriter>=3.0.0",
        "kaleido>=0.2.0",
        "pillow>=8.0.0",
        "tqdm>=4.62.0",
        "joblib>=1.1.0",
        "numba>=0.55.0",
        "psutil>=5.8.0",
        "statsmodels>=0.13.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "strepsuis-phylotrait=strepsuis_phylotrait.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires=">=3.8",
    keywords="bioinformatics microbiology genomics AMR clustering k-modes",
    project_urls={
        "Bug Reports": "https://github.com/MK-vet/strepsuis-phylotrait/issues",
        "Source": "https://github.com/MK-vet/strepsuis-phylotrait",
        "Documentation": "https://github.com/MK-vet/strepsuis-phylotrait#readme",
    },
)
