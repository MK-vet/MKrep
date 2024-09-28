import pandas as pd
from google.colab import files
from scipy.stats import chi2_contingency
import statsmodels.stats.multitest as smm
import numpy as np

# Upload files from the computer
uploaded = files.upload()

# Load CSV files into DataFrames
mge_df = pd.read_csv('MGE.csv')
mic_df = pd.read_csv('MIC.csv')
mlst_df = pd.read_csv('MLST.csv')
plasmid_df = pd.read_csv('Plasmid.csv')
serotype_df = pd.read_csv('Serotype.csv')
virulence_df = pd.read_csv('Virulence.csv')
amr_genes_df = pd.read_csv('AMR_genes.csv')

# Convert categorical columns into multiple binary columns
def expand_categories(df, column_name):
    return pd.get_dummies(df.set_index('Strain_ID')[column_name]).reset_index()

# Expanding categories in the respective files
mge_df_expanded = expand_categories(mge_df, 'MGE')
mlst_df_expanded = expand_categories(mlst_df, 'MLST')
plasmid_df_expanded = expand_categories(plasmid_df, 'Plasmid')
serotype_df_expanded = expand_categories(serotype_df, 'Serotype')

# Merging expanded data with other files
dfs = [
    (mge_df_expanded, 'MGE.csv'),
    (mic_df, 'MIC.csv'),
    (mlst_df_expanded, 'MLST.csv'),
    (plasmid_df_expanded, 'Plasmid.csv'),
    (serotype_df_expanded, 'Serotype.csv'),
    (virulence_df, 'Virulence.csv'),
    (amr_genes_df, 'AMR_genes.csv')
]

merged_df = dfs[0][0]
for df, _ in dfs[1:]:
    merged_df = merged_df.merge(df, on='Strain_ID', how='outer')

# Fill missing values (e.g., when no data is detected in a strain)
merged_df.fillna(0, inplace=True)

# Set Strain_ID as the index
merged_df.set_index('Strain_ID', inplace=True)

# Function to calculate Chi2 test and Phi coefficient for two columns
def chi2_and_phi(col1, col2):
    contingency_table = pd.crosstab(col1, col2)
    try:
        chi2, chi2_p, _, _ = chi2_contingency(contingency_table)
        n = np.sum(contingency_table.values)
        phi = np.sqrt(chi2 / n)
    except ValueError:
        chi2_p = 1.0  # p-value = 1.0 if the test cannot be performed
        phi = 0
    return chi2_p, phi

# List to store test results
chi2_results = []

# Perform tests between all files
for df1, file1 in dfs:
    for col1 in df1.columns[1:]:  # Skipping the Strain_ID column
        for df2, file2 in dfs:
            for col2 in df2.columns[1:]:  # Skipping the Strain_ID column
                if col1 != col2:  # Skipping comparisons of the same columns
                    chi2_p, phi = chi2_and_phi(merged_df[col1], merged_df[col2])
                    chi2_results.append((col1, file1, col2, file2, chi2_p, phi))

# Convert results to a DataFrame
chi2_results_df = pd.DataFrame(chi2_results, columns=['Feature 1', 'File 1', 'Feature 2', 'File 2', 'Chi2 P-value', 'Phi Coefficient'])

# Benjamini-Hochberg correction for multiple tests
rejected, chi2_pvals_corrected, _, _ = smm.multipletests(chi2_results_df['Chi2 P-value'], method='fdr_bh')
chi2_results_df['Chi2 P-value Corrected'] = chi2_pvals_corrected

# Display the results
print(chi2_results_df)

# Save results to a CSV file
chi2_results_df.to_csv('chi2_results_corrected.csv', index=False)
files.download('chi2_results_corrected.csv')

# Network analysis code remains unchanged, but now it uses Chi2 test results
import pandas as pd
import networkx as nx
from google.colab import files
import community.community_louvain as community_louvain
import plotly.graph_objects as go

# Upload the file from your computer
uploaded = files.upload()

# Assuming the file name is 'extended_results.csv'
file_path = list(uploaded.keys())[0]

# Read data from the CSV file
data = pd.read_csv(file_path)

# Display the first few rows to check the column names
print(data.head())
print(data.columns)

# Filter pairs of features with significant correlations based on 'Chi2 P-value Corrected' and 'Phi Coefficient'
significant_links = data[
    (data['Chi2 P-value Corrected'] < 0.05) &
    (data['Phi Coefficient'] > 0.5)
]

# Check if there are any significant results
print(f"Number of significant results: {len(significant_links)}")

# Debug: display the first few significant connections
print(significant_links.head())

# Create a graph from significant connections
G = nx.Graph()
for _, row in significant_links.iterrows():
    G.add_edge(row['Feature 1'], row['Feature 2'], weight=row['Phi Coefficient'], p_value=row['Chi2 P-value Corrected'])

# Debug: number of nodes and edges
print(f"Number of nodes: {len(G.nodes())}")
print(f"Number of edges: {len(G.edges())}")

# Perform Louvain clustering only if we have significant results
if len(G.edges) > 0:
    # Perform Louvain clustering
    partition = community_louvain.best_partition(G, weight='weight')

    # Ensure clusters are numbered starting from 1
    partition = {node: cluster + 1 for node, cluster in partition.items()}

    # Calculate centrality measures
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    eigenvector_centrality = nx.eigenvector_centrality(G)

    # Node positions for 3D layout
    pos = nx.spring_layout(G, dim=3, seed=42, k=0.4)

    # Create edges
    edge_x = []
    edge_y = []
    edge_z = []
    for edge in G.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
        edge_z.append(z0)
        edge_z.append(z1)
        edge_z.append(None)

    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Create nodes
    node_x = []
    node_y = []
    node_z = []
    node_text = []
    node_color = []
    node_hovertext = []
    node_file_category = {}
    category_colors = {
        'MIC.csv': 'blue',
        'AMR_genes.csv': 'green',
        'MLST.csv': 'orange',
        'Serotype.csv': 'purple',
        'Plasmid.csv': 'cyan',
        'MGE.csv': 'magenta',
        'Virulence.csv': 'red'
    }

    category_labels = {
        'MIC.csv': 'Phenotypic resistance',
        'AMR_genes.csv': 'AMR gene',
        'MLST.csv': 'MLST',
        'Serotype.csv': 'Serotype',
        'Plasmid.csv': 'Plasmid',
        'MGE.csv': 'MGE',
        'Virulence.csv': 'Virulence gene'
    }

    for node in G.nodes():
        x, y, z = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)
        node_text.append(node)

        # Assign colors to nodes based on category
        node_file = ''
        for category, color in category_colors.items():
            if category in significant_links.loc[significant_links['Feature 1'] == node, 'File 1'].values or category in significant_links.loc[significant_links['Feature 2'] == node, 'File 2'].values:
                node_color.append(color)
                node_file = category
                node_file_category[node] = category_labels[category]
                break
        else:
            node_color.append('gray')  # Default color if category does not match
            node_file_category[node] = 'Unknown'

        # Add hover text
        node_hovertext.append(f"{node}<br>{node_file_category[node]}<br>Cluster: {partition[node]}")

    # Debug: number of nodes with colors
    print(f"Number of nodes with colors: {len(node_color)}")

    # All nodes with annotations, semi-transparent
    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            color=node_color,
            size=10,
            opacity=0.8,
            line=dict(width=2)
        ),
        text=node_text,
        textposition='top center',
        hovertext=node_hovertext,
        textfont=dict(size=14)
    )

    # Create cluster annotations
    cluster_annotations = []
    for cluster in set(partition.values()):
        nodes_in_cluster = [node for node, cluster_label in partition.items() if cluster_label == cluster]
        if nodes_in_cluster:
            cluster_nodes = "<br>".join([f"{node}: {node_file_category[node]}" for node in nodes_in_cluster])
            hovertext = f"Cluster {cluster}<br>{cluster_nodes}"

            x_coords = [pos[node][0] for node in nodes_in_cluster]
            y_coords = [pos[node][1] for node in nodes_in_cluster]
            z_coords = [pos[node][2] for node in nodes_in_cluster]
            x_center = sum(x_coords) / len(nodes_in_cluster)
            y_center = sum(y_coords) / len(nodes_in_cluster)
            z_center = sum(z_coords) / len(nodes_in_cluster)

            cluster_annotations.append(
                go.Scatter3d(
                    x=[x_center],
                    y=[y_center + 0.2],
                    z=[z_center],
                    text=[f'Cluster {cluster}'],
                    mode='text',
                    showlegend=False,
                    hoverinfo='text',
                    hovertext=[hovertext],
                    textposition='middle center',
                    textfont=dict(size=24, color='purple'),
                    marker=dict(
                        color='purple',
                        size=12,
                        opacity=1.0,
                        line=dict(width=2)
                    )
                )
            )

    # Create plot
    fig = go.Figure(data=[edge_trace, node_trace] + cluster_annotations,
                    layout=go.Layout(
                        showlegend=True,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        scene=dict(
                            xaxis=dict(showbackground=False, showline=True, linewidth=2, linecolor='black', mirror=True),
                            yaxis=dict(showbackground=False, showline=True, linewidth=2, linecolor='black', mirror=True),
                            zaxis=dict(showbackground=False, showline=True, linewidth=2, linecolor='black', mirror=True),
                            aspectmode='data',
                            camera=dict(
                                eye=dict(x=20.0, y=20.0, z=20.0)
                            )
                        )
                    ))

    # Save plot to file
    fig.write_html("network_plot.html")
    fig.show()

    # Add clustering and centrality information to the original data
    node_data = {
        'Node': list(G.nodes()),
        'Cluster': [partition[node] for node in G.nodes()],
        'Degree Centrality': [degree_centrality[node] for node in G.nodes()],
        'Betweenness Centrality': [betweenness_centrality[node] for node in G.nodes()],
        'Closeness Centrality': [closeness_centrality[node] for node in G.nodes()],
        'Eigenvector Centrality': [eigenvector_centrality[node] for node in G.nodes()]
    }

    node_df = pd.DataFrame(node_data)

    # Merge with significant_links data
    significant_links = significant_links.merge(node_df, left_on='Feature 1', right_on='Node', how='left')
    significant_links = significant_links.merge(node_df, left_on='Feature 2', right_on='Node', suffixes=('_Feature 1', '_Feature 2'), how='left')

    # Save the extended data to a new CSV file
    significant_links.to_csv('extended_results.csv', index=False)

else:
    print("No significant edges to display.")
