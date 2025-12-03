# Notebooks Directory

This directory contains Jupyter notebooks for interactive analysis with StrepSuis Analyzer.

## Contents

- `analysis_tutorial.ipynb` - Interactive tutorial notebook
- `colab_version.ipynb` - Google Colab compatible version

## Using Locally

### Requirements

```bash
pip install jupyter notebook
pip install -r ../requirements.txt
```

### Launch Jupyter

```bash
# From this directory
jupyter notebook
```

Then open `analysis_tutorial.ipynb` in the browser.

## Using in Google Colab

1. Upload `colab_version.ipynb` to Google Colab
2. Or use the direct link: [To be added]
3. Follow the instructions in the notebook

## Notebook Features

- **Interactive Analysis**: Step-by-step analysis workflow
- **Data Upload**: Upload your own CSV files
- **Parameter Tuning**: Adjust analysis parameters interactively
- **Visualizations**: View results directly in the notebook
- **Export Results**: Download HTML and Excel reports

## Creating Your Own Notebook

You can create your own analysis notebook:

```python
# Example notebook cells
import sys
sys.path.insert(0, '../')

from StrepSuisPhyloCluster_2025_08_11 import StrepSuisAnalyzer
import pandas as pd

# Load your data
analyzer = StrepSuisAnalyzer(output_dir='my_results', random_state=42)
analyzer.load_data(['../data/Virulence.csv'])

# Run analysis
analyzer.perform_clustering(n_clusters=3)
analyzer.calculate_trait_associations()
analyzer.perform_mca()

# Generate reports
analyzer.generate_html_report()
analyzer.generate_excel_report()

print("Analysis complete! Check my_results/ directory")
```

## Tips

- Save your notebooks with meaningful names
- Document your analysis steps with markdown cells
- Export results before closing the notebook
- Use version control for custom notebooks

## Need Help?

- See USER_GUIDE.md for detailed usage instructions
- Check TESTING.md for testing examples
- Open an issue on GitHub for problems

---

**Note**: Notebook examples will be added in future releases.
