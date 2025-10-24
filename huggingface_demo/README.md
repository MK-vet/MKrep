# StrepSuis_Suite Hugging Face Demo with Voilà

**Fully functional interactive dashboard for microbial genomics analysis**

This is a production-ready Voilà dashboard that provides a user-friendly interface for analyzing 
bacterial genomic data without requiring programming knowledge.

## Quick Start

### Option 1: Use on Hugging Face Spaces

Visit the demo at: https://huggingface.co/spaces/MK-vet/mkrep-demo

### Option 2: Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Or install MKrep package
cd ..
pip install -r requirements.txt

# Navigate to demo folder
cd huggingface_demo

# Launch Voilà dashboard
voila MKrep_Dashboard.ipynb --port 8866 --enable_nbextensions=True
```

Then open your browser to: http://localhost:8866

**Note:** The dashboard is fully functional and ready for production use, not a demo or prototype.

### Option 3: Deploy to Your Own Hugging Face Space

1. Create a new Space on Hugging Face (select "Gradio" or "Streamlit")
2. Upload files from this directory
3. The Space will automatically deploy

## Features

The fully functional dashboard provides:

- **File Upload**: Drag-and-drop CSV files with automatic validation
- **Analysis Selection**: Choose from 5 analysis types with detailed descriptions
- **Parameter Configuration**: Interactive widgets for all parameters with recommended defaults
- **Real-time Progress**: Live feedback during analysis execution
- **Professional Reports**: Download HTML and Excel reports with consistent formatting
- **Data Validation**: Automatic checking of data format and binary values
- **Reproducibility**: All analyses use fixed random seeds and documented parameters
- **User-Friendly**: Designed for non-programmers with clear instructions and tooltips

## Analysis Types

1. **StrepSuis-AMRVirKM** - K-Modes clustering for antimicrobial resistance and virulence
2. **MDR Analysis** - Multi-drug resistance patterns
3. **Network Analysis** - Feature association networks
4. **Phylogenetic Clustering** - Tree-based clustering
5. **StrepSuis Analysis** - S. suis specialized analysis

## Data Format

All input CSV files must have:
- **Strain_ID** column (required)
- Binary features: 0 = absence, 1 = presence

Example:
```csv
Strain_ID,Gene1,Gene2,Antibiotic1
Strain001,1,0,1
Strain002,0,1,1
Strain003,1,1,0
```

## Files

- `MKrep_Dashboard.ipynb` - Main Voilà dashboard notebook (production-ready)
- `requirements.txt` - Python dependencies
- `README.md` - This file
- `example_data/` - Sample datasets for testing

## Production Features

This dashboard is **production-ready** and includes:

### 1. Comprehensive Data Validation
- Automatic checking for required Strain_ID column
- Binary data validation (0/1 only)
- File format verification
- Clear error messages

### 2. Professional Report Generation
- Standardized HTML reports with Bootstrap 5 styling
- Excel reports with multiple sheets and metadata
- PNG charts for publications
- Consistent appearance across all analysis types

### 3. Reproducibility Controls
- Fixed random seeds for deterministic results
- All parameters documented in reports
- Metadata tracking (date, parameters, versions)
- Complete analysis provenance

### 4. User Experience
- Clear step-by-step instructions
- Progress indicators during analysis
- Helpful tooltips and descriptions
- Download links for all outputs
- Responsive design for all devices

## Deployment to Hugging Face

### Using Voilà (Recommended)

1. Create `requirements.txt`:
```
voila
ipywidgets
jupyter
pandas
numpy
plotly
scikit-learn
scipy
statsmodels
openpyxl
```

2. Create `Dockerfile` (optional):
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["voila", "MKrep_Dashboard.ipynb", "--port=7860", "--no-browser"]
```

3. Push to Hugging Face Space

### Using Gradio (Alternative)

Use the provided `app.py` for a Gradio interface:
```python
import gradio as gr
# See app.py for full implementation
```

## Configuration

Edit the notebook to customize:
- Default parameters
- Available analysis options
- Output formats
- Visualization styles

## Support

- Issues: https://github.com/MK-vet/MKrep/issues
- Documentation: https://github.com/MK-vet/MKrep#readme

## License

MIT License - see repository root for details
