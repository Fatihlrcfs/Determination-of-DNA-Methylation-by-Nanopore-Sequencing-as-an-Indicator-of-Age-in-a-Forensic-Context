#comparing generated ref agains the our sample ref #

import pandas as pd
from scipy.stats import spearmanr, ttest_ind

# Step 1: Data Loading
methylation_data_path = 'liftover_corrected_processed_methylation_values.csv'  # Update with actual file path
average_readings_path = 'average_readings_5sample_deepsignal_5cover_output.tsv'  # Update with actual file path

methylation_data = pd.read_csv(methylation_data_path, dtype={'chr': str})
average_readings = pd.read_csv(average_readings_path, sep='\\t', engine='python', dtype={'Chr': str})

print("Data loaded successfully.")

# Step 2: Data Merging
# Merging the two datasets on the basis of the coordinates (chr, start)
merged_data = pd.merge(methylation_data, average_readings, left_on=['chr', 'start'], right_on=['Chr', 'Pos_start'])

if merged_data.empty:
    print("No matching coordinates found. Check the data or merging criteria.")
else:
    print(f"Found {len(merged_data)} matching coordinates.")

    # Removing duplicate columns and renaming
    merged_data = merged_data[['chr', 'start', 'Pos_end', 'Average_Readings', 'VALUE', 'Reporter_Identifier']].rename(columns={'Pos_end': 'end', 'Average_Readings': 
'average_reading'})

    # Step 3: Statistical Analysis
    spearman_corr, spearman_p = spearmanr(merged_data['VALUE'], merged_data['average_reading'])
    t_stat, t_p = ttest_ind(merged_data['VALUE'], merged_data['average_reading'])

    print(f"Spearman Correlation: {spearman_corr}, P-value: {spearman_p}")
    print(f"T-test: T-statistic: {t_stat}, P-value: {t_p}")

    # Step 4: Saving Results
    merged_data.to_csv('merged_data_results.csv', index=False)
    with open('statistical_results.txt', 'w') as f:
        f.write(f"Spearman Correlation: {spearman_corr}, P-value: {spearman_p}\\n")
        f.write(f"T-test: T-statistic: {t_stat}, P-value: {t_p}")

    print("Results saved to 'merged_data_results.csv' and 'statistical_results.txt'.")

