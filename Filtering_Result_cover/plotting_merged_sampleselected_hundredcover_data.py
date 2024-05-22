
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read data
df = pd.read_csv("merged_sampleselected_hundredcover_output.tsv", sep="\t")

# file name
samples = df.columns[3:].to_list()

# Extraction age info from file name
ages = [int(sample.split('age')[1][:2]) for sample in samples]

for index, row in df.iterrows():
    methylation_values = row[samples].to_list()

    # Calculating correlation and r^2 value
    correlation_matrix = np.corrcoef(ages, methylation_values)
    r2_value = correlation_matrix[0, 1] ** 2
    
    # Calculate trend line
    coeffs = np.polyfit(ages, methylation_values, 1)
    trend_line = np.poly1d(coeffs)
    trend_values = trend_line(ages)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(ages, methylation_values, '-o', label=f"R^2 = {r2_value:.2f}")
    plt.plot(ages, trend_values, '--r', label="Trend Line")
    
    age_labels = [f"age{age}" for age in ages]
    plt.xticks(ages, labels=age_labels, rotation=45)
    
    plt.xlabel("Age")
    plt.ylabel("Methylation Value")
    plt.title(f"Coordinant: {row['Chr']}:{row['Pos_start']}-{row['Pos_end']}")
    plt.legend()
    plt.tight_layout()
    
    # File named and saving
    filename = f"chr{row['Chr']}.{row['Pos_start']}_Pos_end{row['Pos_end']}_comparison.png"
    if r2_value > 0.95:
        filename = "promising_" + filename
    plt.savefig(filename)
    plt.close()

