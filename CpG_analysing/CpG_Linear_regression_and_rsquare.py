# Cpg regresion and r2#

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

sample_filenames = [ 
    'age21bc15_method_cpg.tsv',
    'age24bc09_method_cpg.tsv',
    'age26bc18_method_cpg.tsv',
    'age27bc05_method_cpg.tsv',
    'age29bc07_method_cpg.tsv',
    'age29bc12_method_cpg.tsv',
    'age31bc16_method_cpg.tsv',
    'age31single_method_cpg.tsv',
    'age33bc21_method_cpg.tsv',
    'age35bc22_method_cpg.tsv',
    'age38bc13_method_cpg.tsv',
    'age39single_method_cpg.tsv',
    'age43bc10_method_cpg.tsv',
    'age43single_method_cpg.tsv',
    'age45bc14_method_cpg.tsv',
    'age48single_method_cpg.tsv',
    'age53bc19_method_cpg.tsv',
    'age54bc17_method_cpg.tsv',
    'age56bc10_method_cpg.tsv',
    'age58bc11_method_cpg.tsv',
    'age59single_method_cpg.tsv',
    'age63bc20_method_cpg.tsv',
    'age76bc08_method_cpg.tsv',
    'age77bc06_method_cpg.tsv',
]  

result = {}


for filename in sample_filenames:
    print(f"isleniyor: {filename}")
    df = pd.read_csv(filename, sep="\t")
    filtered_df = df[df['cover'] >= 3]

    for index, row in filtered_df.iterrows():
        gene = row['Gene']
        if pd.isnull(gene):
            gene = f"{row['chr']}_{row['start']}_{row['end']}"

        if gene not in result:
            result[gene] = []

        # Taking age from file name
        age_str = filename.split('age')[1]
        if 'bc' in age_str:
            age_from_filename = int(age_str.split('bc')[0])
        elif 'single' in age_str:
            age_from_filename = int(age_str.split('single')[0])
        else:
            # Eliminating Errors
            raise ValueError(f"Unexpected filename format: {filename}")

        result[gene].append((age_from_filename, row['methylation']))


for gene, values in result.items():
    if len(values) < 2:
        continue

    plt.figure(figsize=(10, 5))
    
    # ordering sample ages
    sorted_values = sorted(values, key=lambda x: x[0])
    ages = [item[0] for item in sorted_values]  # sıralı yaslar
    y = [item[1] for item in sorted_values]
    
    # Linear Regression
    model = LinearRegression()
    model.fit(np.array(ages).reshape(-1, 1), y)
    trend_y = model.predict(np.array(ages).reshape(-1, 1))

    # Calculate R^2 
    r2_score = model.score(np.array(ages).reshape(-1, 1), y)

    plt.scatter(ages, y)
    plt.plot(ages, trend_y, color='red')  # Trend cizgisini ekle
    plt.title(f"{gene} (R^2 = {r2_score:.2f})")  # Adding R2 to the table headding
    plt.xlabel('Age')
    plt.ylabel('Methylation Value')
    
    # x-ticks label sample name 
    plt.xticks(ages, [f'age{age}' for age in ages], rotation=90)
    
    plt.tight_layout()
    plt.savefig(f"{gene}_scatter_plot.png")
    plt.close()

