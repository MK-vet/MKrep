import pandas as pd
import numpy as np
from kmodes.kmodes import KModes
from sklearn.metrics import silhouette_score

# Load the virulence genes dataset
virulence_genes_df = pd.read_csv('Virulence.csv')

# Retain Strain_ID for reference
strain_ids = virulence_genes_df['Strain_ID']

# Drop Strain_ID from the data used for clustering
virulence_genes_df = virulence_genes_df.drop(columns=['Strain_ID'])

# Fill missing values and convert to binary
virulence_genes_df.fillna(0, inplace=True)
binary_virulence_df = virulence_genes_df.astype(int)

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

# Determine optimal number of clusters for Virulence genes
optimal_virulence_clusters = determine_optimal_clusters(binary_virulence_df)

# Perform k-modes clustering
virulence_model, virulence_clusters = perform_kmodes(binary_virulence_df, optimal_virulence_clusters)

# Extract characteristic patterns for Virulence genes
virulence_patterns = extract_characteristic_patterns(virulence_model, binary_virulence_df)

# Create results dataframe
results_df = pd.DataFrame({
    'Strain_ID': strain_ids,
    'Virulence_Cluster': virulence_clusters
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

virulence_patterns_df = patterns_to_dataframe(virulence_patterns, 'Virulence')

# Save results
results_df.to_csv("virulence_kmodes_clustering_results.csv", index=False)
virulence_patterns_df.to_csv("virulence_kmodes_characteristic_patterns.csv", index=False)

print(results_df.head())
print("\nVirulence Characteristic Patterns:")
print(virulence_patterns_df)

