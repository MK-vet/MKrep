import pandas as pd
import numpy as np
from Bio import Phylo
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances
from scipy.cluster import hierarchy
from kneed import KneeLocator

# Load phylogenetic tree
tree = Phylo.read("tree.newick.txt", "newick")

# Load binary data
data = pd.read_csv("resistance_virulence_data.csv", index_col=0)

# Function to calculate distance between strains based on the tree
def tree_distance(tree, strain1, strain2):
    try:
        return tree.distance(str(strain1), str(strain2))
    except ValueError:
        return max(node.total_branch_length() for node in tree.get_nonterminals())

# Create distance matrix based on the tree
strains = data.index.tolist()
tree_dist_matrix = np.zeros((len(strains), len(strains)))
for i, strain1 in enumerate(strains):
    for j, strain2 in enumerate(strains):
        tree_dist_matrix[i, j] = tree_distance(tree, strain1, strain2)

# Convert binary data to numpy array
binary_data = data.values.astype(float)

# Calculate distances based on binary data
binary_dist_matrix = pairwise_distances(binary_data, metric='jaccard')

# Combine distances from tree and binary data
combined_dist_matrix = (tree_dist_matrix + binary_dist_matrix) / 2

# Hierarchical clustering analysis
linkage_matrix = linkage(combined_dist_matrix, method='ward')

# Function to determine optimal number of clusters using elbow method
def optimal_cluster_number(linkage_matrix, max_clusters=20):
    n_clusters = range(1, max_clusters + 1)
    inertias = []
    for n in n_clusters:
        clusters = hierarchy.fcluster(linkage_matrix, n, criterion='maxclust')
        inertia = sum(np.min(combined_dist_matrix[np.where(clusters == c)[0]][:, np.where(clusters == c)[0]].sum(axis=1)) for c in set(clusters))
        inertias.append(inertia)
    
    kneedle = KneeLocator(n_clusters, inertias, curve='convex', direction='decreasing')
    return kneedle.elbow

# Determine optimal number of clusters
optimal_clusters = optimal_cluster_number(linkage_matrix)
print(f"Optimal number of clusters: {optimal_clusters}")

# Identify clusters
clusters = hierarchy.fcluster(linkage_matrix, optimal_clusters, criterion='maxclust')

# Add cluster information to data
data['Cluster'] = clusters

# Display first few rows with assigned clusters
print(data[['Cluster'] + list(data.columns[:10])].head())

# Cluster analysis
cluster_summary = data.groupby('Cluster').mean()
print("\nMean feature values in clusters:")
print(cluster_summary)

# Save results to CSV file
data.to_csv("clusters_results.csv")
cluster_summary.to_csv("cluster_summary.csv")

# Function to identify characteristic features for each cluster
def identify_characteristic_features(data, clusters, threshold=0.5):
    cluster_features = {}
    for cluster in np.unique(clusters):
        cluster_data = data[clusters == cluster]
        cluster_mean = cluster_data.mean()
        characteristic_features = cluster_mean[cluster_mean > threshold].index.tolist()
        cluster_features[cluster] = characteristic_features
    return cluster_features

# Identify characteristic features
characteristic_features = identify_characteristic_features(data, clusters)

# Convert characteristic features to DataFrame and save to CSV
characteristic_features_df = pd.DataFrame([(cluster, ', '.join(features)) for cluster, features in characteristic_features.items()], 
                                          columns=['Cluster', 'Characteristic Features'])
characteristic_features_df.to_csv("characteristic_features.csv", index=False)

# Display characteristic features for each cluster
for cluster, features in characteristic_features.items():
    print(f"\nCluster {cluster} - Characteristic features:")
    print(", ".join(features))

# Visualize dendrogram
plt.figure(figsize=(20, 10))
dendrogram(linkage_matrix, labels=strains, leaf_rotation=90, leaf_font_size=6, color_threshold=linkage_matrix[-optimal_clusters+1, 2])
plt.title('Dendrogram of Phylogenetic Cluster Analysis')
plt.xlabel('Strains')
plt.ylabel('Distance')
plt.tight_layout()
plt.show()

