import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from sklearn.metrics import mutual_info_score
from collections import Counter
from scipy.stats import entropy

# Load the data (update file path as necessary)
file_path = '/content/clusters.csv'
data = pd.read_csv(file_path)

# Drop rows with NaN values from the relevant columns
data = data.dropna(subset=['mlst', 'phenotype', 'genes', 'virulence', 'serotype'])

# Define function for Cramér's V
def cramers_v(contingency_table):
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    n = contingency_table.sum().sum()
    min_dim = min(contingency_table.shape) - 1
    cramers_v_value = np.sqrt(chi2 / (n * min_dim))
    return chi2, p, cramers_v_value

# Mutual Information calculation
def calculate_mutual_information(var1, var2):
    return mutual_info_score(var1, var2)

# Entropy and Conditional Entropy Calculation
def calculate_conditional_entropy(var1, var2):
    y_counter = Counter(var2)
    xy_counter = Counter(list(zip(var1, var2)))
    total_occurrences = sum(y_counter.values())
    
    # Conditional Entropy H(var1 | var2)
    entropy_x_given_y = 0
    for y_val, y_count in y_counter.items():
        p_y = y_count / total_occurrences
        prob_x_given_y = [xy_counter[(x_val, y_val)] / y_count for x_val in set(var1) if (x_val, y_val) in xy_counter]
        entropy_x_given_y += p_y * entropy(prob_x_given_y)
    
    return entropy_x_given_y

# Define a function that calculates all metrics for any pair of variables
def calculate_association_metrics(data, var1, var2):
    # Create a contingency table (cross-tabulation)
    contingency_table = pd.crosstab(data[var1], data[var2])
    
    # 1. Chi-squared test and Cramér's V calculation
    chi2_stat, p_value, cramers_v_value = cramers_v(contingency_table)
    print(f"Metrics for {var1} vs {var2}:")
    print(f"Chi2 Statistic: {chi2_stat:.2f}, p-value: {p_value:.4f}, Cramér's V: {cramers_v_value:.4f}")
    
    # 2. Mutual Information calculation
    mutual_info = calculate_mutual_information(data[var1], data[var2])
    print(f"Mutual Information between {var1} and {var2}: {mutual_info:.4f}")
    
    # 3. Entropy and Conditional Entropy Calculation in both directions
    entropy_var1_given_var2 = calculate_conditional_entropy(data[var1], data[var2])
    entropy_var2_given_var1 = calculate_conditional_entropy(data[var2], data[var1])
    print(f"Conditional Entropy H({var1} | {var2}): {entropy_var1_given_var2:.4f}")
    print(f"Conditional Entropy H({var2} | {var1}): {entropy_var2_given_var1:.4f}\n")

# List of variables to compare
variables = ['mlst', 'phenotype', 'genes', 'virulence', 'serotype']

# Perform pairwise calculations for all combinations of variables
for i in range(len(variables)):
    for j in range(i + 1, len(variables)):
        calculate_association_metrics(data, variables[i], variables[j])
