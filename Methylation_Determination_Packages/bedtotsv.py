#remora_bedtotsv#

import pandas as pd

# .bed path for bed
bed_file = "file.bed"

# TSV path for tsv
tsv_file = "file.tsv"

# DataFrame create
data = {
    "Chr": [],
    "Pos_start": [],
    "Pos_end": [],
    "Methylation": [],
    "Strand": []
}

# .bed reading bed file and adding data to the data frame
with open(bed_file, 'r') as bed:
    for line in bed:
        # Line setup
        line_data = line.strip().split('\t')
        # Headings
        data["Chr"].append(line_data[0])
        data["Pos_start"].append(int(line_data[1]))
        data["Pos_end"].append(int(line_data[2]))
        data["Methylation"].append(line_data[10])
        data["Strand"].append(line_data[5])

# DataFrame 
df = pd.DataFrame(data)

# Typing data from data frame to tsv file
df.to_csv(tsv_file, sep="\t", index=False)
