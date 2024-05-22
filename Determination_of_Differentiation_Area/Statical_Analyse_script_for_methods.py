# Statical Analysis Script #
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Read Data
data = pd.read_csv('combined_common_results.tsv', sep='\t', na_values="NA")

# Selecting Data for Specified Methods Only:
selected_methods = ['deepsignal', 'nanopolish', 'megalodon', 'remora']
selected_data = data[selected_methods]

# Basic Statistics
basic_statistics = selected_data.describe()

# Correlation Analysis
correlations = selected_data.corr()

# Statistical Test
t_test_results = []
for col1 in selected_methods:
    for col2 in selected_methods:
        if col1 < col2:
            t_statistic, p_value = ttest_ind(selected_data[col1], selected_data[col2], nan_policy='omit')
            t_test_results.append({'Method 1': col1, 'Method 2': col2, 'T-Statistic': t_statistic, 'P-Value': p_value})

# Printing Outputs
print("Basic Statistics:")
print(basic_statistics)
print("\nKorelasyonlar:")
print(correlations)
print("\nIstatistiksel Test Results:")
for result in t_test_results:
    print(f"\n{result['Method 1']} ve {result['Method 2']} arasÄ±:")
    print(f"T-Ä°statistik: {result['T-Statistic']}")
    print(f"P-DeÄŸeri: {result['P-Value']}")
