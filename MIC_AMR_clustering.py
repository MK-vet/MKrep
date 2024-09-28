import pandas as pd
import numpy as np
from kmodes.kmodes import KModes
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

# Load the datasets
mic_df = pd.read_csv('MIC.csv')
amr_genes_df = pd.read_csv('AMR_genes.csv')

# Retain Strain_ID for reference
strain_ids = mic_df['Strain_ID']

# Drop Strain_ID from the data used for clustering
mic_df = mic_df.drop(columns=['Strain_ID'])
amr_genes_df = amr_genes_df.drop(columns=['Strain_ID'])

# Fill missing values and convert to binary
mic_df.fillna(0, inplace=True)
amr_genes_df.fillna(0, inplace=True)
binary_mic_df = mic_df.astype(int)
binary_amr_df = amr_genes_df.astype(int)

def determine_optimal_clusters(data, max_clusters=10):
    silhouette_scores = []
    for k in range(2, max_clusters+1):
        km = KModes(n_clusters=k, init='Huang', n_init=5, verbose=1)
        clusters = km.fit_predict(data)
        silhouette_avg = silhouette_score(data, clusters)
        silhouette_scores.append(silhouette_avg)
        print(f"For n_clusters = {k}, the average silhouette score is : {silhouette_avg}")
    
    optimal_k = silhouette_scores.index(max(silhouette_scores)) + 2
    print(f"Optimal number of clusters: {optimal_k}")
    return optimal_k

def perform_kmodes(data, n_clusters):
    km = KModes(n_clusters=n_clusters, init='Huang', n_init=5, verbose=1)
    clusters = km.fit_predict(data)
    return km, clusters

def extract_characteristic_patterns(model, data):
    patterns = {}
    for i in range(model.n_clusters):
        cluster_data = data[model.labels_ == i]
        mode = cluster_data.mode().iloc[0]
        significant_features = mode[mode > 0.5]
        patterns[i] = significant_features
    return patterns

# Determine optimal number of clusters for MIC and AMR
optimal_mic_clusters = determine_optimal_clusters(binary_mic_df)
optimal_amr_clusters = determine_optimal_clusters(binary_amr_df)

# Perform k-modes clustering
mic_model, mic_clusters = perform_kmodes(binary_mic_df, optimal_mic_clusters)
amr_model, amr_clusters = perform_kmodes(binary_amr_df, optimal_amr_clusters)

# Extract characteristic patterns
mic_patterns = extract_characteristic_patterns(mic_model, binary_mic_df)
amr_patterns = extract_characteristic_patterns(amr_model, binary_amr_df)

# Create results dataframe
results_df = pd.DataFrame({
    'Strain_ID': strain_ids,
    'MIC_Cluster': mic_clusters,
    'AMR_Cluster': amr_clusters
})

# Convert patterns to DataFrame
def patterns_to_dataframe(patterns, pattern_type):
    pattern_list = []
    for cls, features in patterns.items():
        pattern_list.append({
            'Cluster': cls,
            'Characteristic_Pattern': ", ".join(features.index),
            'Support': ", ".join([f"{value:.2f}" for value in features.values]),
            'Type': pattern_type
        })
    return pd.DataFrame(pattern_list)

mic_patterns_df = patterns_to_dataframe(mic_patterns, 'MIC')
amr_patterns_df = patterns_to_dataframe(amr_patterns, 'AMR')

# Save results
results_df.to_csv("kmodes_clustering_results.csv", index=False)
pd.concat([mic_patterns_df, amr_patterns_df]).to_csv("kmodes_characteristic_patterns.csv", index=False)

print(results_df.head())
print("\nMIC Characteristic Patterns:")
print(mic_patterns_df)
print("\nAMR Characteristic Patterns:")
print(amr_patterns_df)

# Perform chi-square test
from scipy.stats import chi2_contingency
contingency_table = pd.crosstab(results_df['MIC_Cluster'], results_df['AMR_Cluster'])
chi2, p_value, dof, expected = chi2_contingency(contingency_table)

print(f"\nChi-square test p-value: {p_value}")
if p_value < 0.05:
    print("There is a significant association between MIC and AMR clusters.")
else:
    print("There is no significant association between MIC and AMR clusters.")
