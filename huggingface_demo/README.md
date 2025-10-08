# MKrep Hugging Face Demo with Voilà

Interactive dashboard for microbial genomics analysis using Voilà.

## Quick Start

### Option 1: Use on Hugging Face Spaces

Visit the demo at: https://huggingface.co/spaces/MK-vet/mkrep-demo

### Option 2: Run Locally

```bash
# Install dependencies
pip install voila ipywidgets pandas numpy plotly jupyter

# Clone repository
git clone https://github.com/MK-vet/MKrep.git
cd MKrep/huggingface_demo

# Launch Voilà dashboard
voila MKrep_Dashboard.ipynb --port 8866
```

Then open your browser to: http://localhost:8866

### Option 3: Deploy to Your Own Hugging Face Space

1. Create a new Space on Hugging Face (select "Gradio" or "Streamlit")
2. Upload files from this directory
3. The Space will automatically deploy

## Features

The interactive dashboard provides:

- **File Upload**: Drag-and-drop CSV files
- **Analysis Selection**: Choose from 5 analysis types
- **Parameter Configuration**: Interactive widgets for all parameters
- **Real-time Results**: See analysis progress and results
- **Report Download**: Get HTML and Excel reports
- **Visualizations**: Interactive charts with Plotly

## Analysis Types

1. **Cluster Analysis** - K-Modes clustering for binary traits
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

- `MKrep_Dashboard.ipynb` - Main Voilà dashboard notebook
- `requirements.txt` - Python dependencies
- `README.md` - This file
- `app.py` - Alternative Gradio interface
- `example_data/` - Sample datasets for testing

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
