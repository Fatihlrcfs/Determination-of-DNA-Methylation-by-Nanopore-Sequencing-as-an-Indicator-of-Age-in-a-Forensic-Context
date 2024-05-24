# CpG extraction from sample #

#!/bin/bash

# Input files 
percg_file="sample_method-freq-perCG-combStrand.tsv"
cpg_final_file="CpG_final.txt"

# Output file
output_file="age21bc15_method_cpg.tsv"

# Create the header line
echo -e "Gene\tchr\tstart\tend\tcover\tmethylation" > $output_file

# Read each line from the CpG_final.txt file
while IFS=$'\t' read -r gene chr start end; do
    if [ -z "$gene" ]; then
        gene="None"
    fi
    
# Filter the perCG.tsv file and append to the output.tsv file  
    awk -v gene="$gene" -v chr="$chr" -v start="$start" -v end="$end" '$1 == chr && $2 >= start && $3 <= end {print gene "\t" $0}' $percg_file >> $output_file
done < $cpg_final_file

echo "islem tamamlandı. Sonuclar $output_file dosyasına kaydedildi."
