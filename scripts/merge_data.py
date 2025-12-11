#!/usr/bin/env python3
"""
Merge MIC.csv and AMR_genes.csv into a single dataset for MDR analysis.
"""

import pandas as pd

# Read both files
mic_df = pd.read_csv('MIC.csv')
amr_df = pd.read_csv('AMR_genes.csv')

# Merge on Strain_ID
merged_df = pd.merge(mic_df, amr_df, on='Strain_ID', how='inner')

# Save the merged data
merged_df.to_csv('merged_resistance_data.csv', index=False)

print(f"Merged data shape: {merged_df.shape}")
print(f"Columns: {merged_df.columns.tolist()}")
print(f"Output saved to: merged_resistance_data.csv")
