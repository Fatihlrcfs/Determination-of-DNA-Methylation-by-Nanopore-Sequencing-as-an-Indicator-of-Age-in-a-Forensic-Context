#output_method.txt file plot with trend generation#

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Load the data from the output.txt file
file_path = 'output_method.txt'
df = pd.read_csv(file_path, sep='\t')

# Extract ages from sample IDs for spacing on x-axis
# Extract valid sample columns (those that start with 'age' and end with the specific suffix)
sample_columns = [col for col in df.columns if col.startswith('age') and '_method_differentiate.tsv_Methylation_Average' in col]
sample_ids = [col.split('_')[0] for col in sample_columns]
def extract_age_from_sample_id(sample_id):
    """Attempt to extract age from sample ID (e.g., age21 -> 21). 
    Returns None if unsuccessful."""
    try:
        return int(sample_id[3:5])
    except ValueError:
        return None

ages = [extract_age_from_sample_id(sample_id) for sample_id in sample_ids]
# Remove None values if any
ages = [age for age in ages if age is not None]


# Calculate the spacing based on age differences
x_ticks_positions = [0]  # starting at 0
for i in range(1, len(ages)):
    age_diff = ages[i] - ages[i-1]
    x_ticks_positions.append(x_ticks_positions[-1] + age_diff)

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    chr_val = row['Chr']
    start_val = row['Start']
    end_val = row['End']

    # Extract the methylation values for the current row
    met_values = [row[f'{sample}_method_differentiate.tsv_Methylation_Average'] for sample in sample_ids]

    # Calculate the correlation and R-squared value
    slope, intercept, r_value, p_value, std_err = linregress(x_ticks_positions, met_values)
    r_squared = r_value ** 2

    # Plot the methylation values
    plt.figure(figsize=(20, 10))
    plt.plot(x_ticks_positions, met_values, marker='o', linestyle='-', color='b', label='Methylation_Average')
    # Calculate trend line values
    trend_y = [slope * x + intercept for x in x_ticks_positions]
    
    # Plot the trend line
    plt.plot(x_ticks_positions, trend_y, linestyle='--', color='r', label='Trend Line')

    plt.xlabel('Sample IDs', fontsize=15)
    plt.ylabel('Methylation Average', fontsize=15)
    plt.title(f'Chr: {chr_val}, Start: {start_val}, End: {end_val}\nR-squared: {r_squared:.2f}', fontsize=18)
    plt.legend(fontsize=12)
    
    # Set the x-axis tick labels to be sample IDs and position them based on x_ticks_positions
    plt.xticks(ticks=x_ticks_positions, labels=sample_ids, rotation=45, fontsize=12, ha='right')
    
    # Set y-axis limit to make room for count numbers
    plt.ylim(bottom=min(met_values) - 0.2)
    
    # Add faint grid lines to the plot
    plt.grid(True, linestyle='--', alpha=0.5)

    # Save the plot with a filename indicating the R-squared value
    output_filename = f'chr{chr_val}_start{start_val}_end{end_val}.png'
    if r_squared > 0.25:
        output_filename = f'chr{chr_val}_start{start_val}_end{end_val}_promising.png'
    plt.savefig(output_filename)

    # Show the plot (optional)
    plt.show()
