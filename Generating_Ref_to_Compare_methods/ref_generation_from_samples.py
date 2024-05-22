# Referans generation from methods #

import pandas as pd
import numpy as np

# list of file
example_files = sorted([
    "filtered_age21bc15_method-freq-perCG-combStrand.tsv",
    "filtered_age24bc09_method-freq-perCG-combStrand.tsv",
    "filtered_age26bc18_method-freq-perCG-combStrand.tsv",
    "filtered_age27bc05_method-freq-perCG-combStrand.tsv",
    "filtered_age29bc07_method-freq-perCG-combStrand.tsv",
    "filtered_age31bc16_method-freq-perCG-combStrand.tsv",
    "filtered_age31single_method-freq-perCG-combStrand.tsv",
    "filtered_age33bc21_method-freq-perCG-combStrand.tsv",
    "filtered_age35bc22_method-freq-perCG-combStrand.tsv",
    "filtered_age38bc13_method-freq-perCG-combStrand.tsv",
    "filtered_age39single_method-freq-perCG-combStrand.tsv",
    "filtered_age43bc10_method-freq-perCG-combStrand.tsv",
    "filtered_age43single_method-freq-perCG-combStrand.tsv",
    "filtered_age45bc14_method-freq-perCG-combStrand.tsv",
    "filtered_age48single_method-freq-perCG-combStrand.tsv",
    "filtered_age53bc19_method-freq-perCG-combStrand.tsv",
    "filtered_age54bc17_method-freq-perCG-combStrand.tsv",
    "filtered_age56bc10_method-freq-perCG-combStrand.tsv",
    "filtered_age58bc11_method-freq-perCG-combStrand.tsv",
    "filtered_age59single_method-freq-perCG-combStrand.tsv",
    "filtered_age63bc20_method-freq-perCG-combStrand.tsv",
    "filtered_age76bc08_method-freq-perCG-combStrand.tsv",
    "filtered_age77bc06_method-freq-perCG-combStrand.tsv",
])

# Empty  DataFrame 
all_data = pd.DataFrame()

for file in example_files:
    # extract age and type
    sample_name = file.split('_')[1]
    
    # read file
    df = pd.read_csv(file, sep='\t')
    
    # Coverage 100 or above filteration
    df_filtered = df[df['Coverage'] >= 100]
    
    # combine coordinants (Chr_Pos_start_Pos_end) ve save methylation value
    df_filtered.loc[:, 'Coord'] = df_filtered['Chr'].astype(str) + '_' + df_filtered['Pos_start'].astype(str) + '_' + df_filtered['Pos_end'].astype(str)
    df_filtered = df_filtered[['Coord', 'Methylation']]
    df_filtered.columns = ['Coord', sample_name] 
    
    # combine ready data
    if all_data.empty:
        all_data = df_filtered
    else:
        all_data = pd.merge(all_data, df_filtered, on='Coord', how='outer')

# NaN enter as 0
all_data = all_data.fillna(0)

# adding coordinant in calum
coords = all_data['Coord'].str.split('_', expand=True)
coords.columns = ['Chr', 'Pos_start', 'Pos_end']
all_data = pd.concat([coords, all_data.drop('Coord', axis=1)], axis=1)

# calculate each raw for average methylation value
all_data['Non_zero_counts'] = all_data.drop(['Chr', 'Pos_start', 'Pos_end'], axis=1).astype(bool).sum(axis=1)
all_data['Average_Methylation'] = all_data.drop(['Chr', 'Pos_start', 'Pos_end', 'Non_zero_counts'], axis=1).sum(axis=1) / all_data['Non_zero_counts']

# Save result
all_data.to_csv('corrected_merged_methylation_data_cover1.tsv', sep='\t', index=False)
