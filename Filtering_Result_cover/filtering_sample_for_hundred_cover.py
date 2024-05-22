# filteren position morehan cover #

import os

# Specify file names
files = [
    "filtered_age39single_method-freq-perCG-combStrand.tsv",
    "filtered_age43single_method-freq-perCG-combStrand.tsv",
    "filtered_age45bc14_method-freq-perCG-combStrand.tsv",
    "filtered_age59single_method-freq-perCG-combStrand.tsv",
    "filtered_age77bc06_method-freq-perCG-combStrand.tsv",
]

# Read files and add locations to a dictionary.
all_data = {}
headers = ['Chr', 'Pos_start', 'Pos_end']

for file in files:
    sample_name = file.split("_")[1]  # Extract the sample name from the file name.
    headers.append(sample_name)
    with open(file, 'r') as f:
        next(f)  # Skip the header row.
        for line in f:
            parts = line.strip().split("\t")
            loc = (parts[0], parts[1], parts[2])  # Lokasyon tuple (Chr, Pos_start, Pos_end)
            
             # Check the coverage value
            coverage_value = int(parts[3])
            if coverage_value < 100:
                continue  # Skip this line if the coverage value is less than 100.

            if loc not in all_data:
                all_data[loc] = {}
            all_data[loc][sample_name] = parts[4]  # Store the methylation value.

# Write common locations and methylation values to a new file.
output_file = "merged_sampleselected_hundredcover_output.tsv"
with open(output_file, 'w') as out:
    out.write("\t".join(headers) + "\n")  # Write the header row.
    for loc, samples in all_data.items():
        if len(samples) == len(files):  # Check for locations common to all samples.
            out_vals = [loc[0], loc[1], loc[2]]
            for file in files:
                sample_name = file.split("_")[1]  # Extract the appropriate index from the file name.
                out_vals.append(samples.get(sample_name, 'NA'))  # 'NA' is a placeholder for cases where methylation values are not found.
            out.write("\t".join(out_vals) + "\n")

print(f"islem tamamlandi. Ortak lokasyonlar ve metilasyon degerleri {output_file} dosyasinda bulunmaktadir.")



