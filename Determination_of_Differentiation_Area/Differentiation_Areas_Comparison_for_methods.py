
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Load the data from the output files
deepsignal_df = pd.read_csv('output_deepsignal.txt', sep='\t')
megalodon_df = pd.read_csv('output_megalodon.txt', sep='\t')
nanopolish_df = pd.read_csv('output_nanopolish.txt', sep='\t')
remora_df = pd.read_csv('output_remora.txt', sep='\t')

# Drop the 'Unnamed' column if it exists
for df in [deepsignal_df, megalodon_df, nanopolish_df, remora_df]:
    df.drop(columns=[col for col in df if col.startswith('Unnamed')], inplace=True)

samples = ["21bc15", "24bc09", "26bc18", "27bc05", "31bc16", "31single", "33bc21", "35bc22", "38bc13", "39single", 
           "43bc10", "43single", "45bc14", "48single", "53bc19", "54bc17", "56bc10", "58bc11", "61single", "63bc20", 
           "76bc08", "77bc06"]

# Extract ages and sort samples by age
samples_sorted = sorted(samples, key=lambda s: int(''.join(filter(str.isdigit, s.split('bc' if 'bc' in s else 'single')[0]))))

# Compute distance based on age differences
ages = [int(''.join(filter(str.isdigit, s.split('bc' if 'bc' in s else 'single')[0]))) for s in samples_sorted]
distances = [0] + [ages[i] - ages[i - 1] if ages[i] != ages[i-1] else 0 for i in range(1, len(ages))]

cumulative_distances = np.cumsum(distances)

sample_ids = sorted(samples, key=lambda s: int(''.join(filter(str.isdigit, s.split('bc' if 'bc' in s else 'single')[0]))))
sample_indices = np.cumsum([0] + [ages[i] - ages[i - 1] if ages[i] != ages[i-1] else 0 for i in range(1, len(ages))])
# Loop through each row in one of the DataFrames (e.g., deepsignal_df)
for index, row in deepsignal_df.iterrows():
    chr_val = row['Chr']
    start_val = row['Start']
    end_val = row['End']

    # Extract the Methylation_Average values for the current row and sample IDs
    deepsignal_met = [row[f'age{sample}_deepsignal_differentiate.tsv_Methylation_Average'] for sample in sample_ids]
    megalodon_met = [megalodon_df.iloc[index][f'age{sample}_megalodon_differentiate.tsv_Methylation_Average'] for sample in sample_ids]
    nanopolish_met = [nanopolish_df.iloc[index][f'age{sample}_nanopolish_differentiate.tsv_Methylation_Average'] for sample in sample_ids]
    remora_met = [remora_df.iloc[index][f'age{sample}_remora_differentiate.tsv_Methylation_Average'] for sample in sample_ids]
    plt.figure(figsize=(12, 6))
    
    # Whether to add "promising" to filename
    is_promising = False
    
    slopes = []
    # Plot the Methylation_Average values for all methods
    for method_met, color, label in zip([deepsignal_met, megalodon_met, nanopolish_met, remora_met], ['b', 'g', 'r', 'purple'], ['DeepSignal', 'Megalodon', 'Nanopolish', 'Remora']):
        plt.plot(sample_indices, method_met, marker='o', linestyle='-', color=color, label=label)
    # Create Trend Line
        slope, intercept, _, _, _ = linregress(sample_indices, method_met)
        slopes.append(slope)  # Slope degerini listeye ekleyin
        trend_line = intercept + slope * np.array(sample_indices)
        plt.plot(sample_indices, trend_line, linestyle='--', color=color, label=f'{label} Trend')

    avg_slope = np.mean(slopes)  # Ortalama egimi hesaplayÄ±n

    if abs(avg_slope) > 0.002:  # Ortalama egimi kullanarak kontrol edin
        is_promising = True

    plt.xlabel('Sample IDs', fontsize=12)
    plt.ylabel('Methylation Average', fontsize=12)
    plt.title(f'Chr: {chr_val}, Start: {start_val}, End: {end_val}', fontsize=15)
    plt.legend(fontsize=10)
    plt.xticks(sample_indices, samples_sorted, rotation=45, fontsize=10, ha='right')
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    output_filename = f'chr{chr_val}_start{start_val}_end{end_val}_comparison.png'
    if is_promising:
        output_filename = output_filename.replace('.png', '_promising.png')
    plt.savefig(output_filename)
    
    plt.show()
