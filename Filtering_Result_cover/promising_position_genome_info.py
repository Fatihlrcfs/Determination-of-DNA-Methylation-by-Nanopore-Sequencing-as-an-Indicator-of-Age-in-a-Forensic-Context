#promising position genome hit #

import requests
import pandas as pd

# Koordinatların okunacagı dosya
coordinates_file = 'coordinates.txt'

# Sonucların yazılacagı dosya (TSV formatında)
output_file = 'detailed_genomic_features.tsv'

server = "https://rest.ensembl.org"

def fetch_genomic_features(coord):
    ext = f"/overlap/region/human/{coord}?content-type=application/json;feature=regulatory;feature=gene"
    response = requests.get(f"{server}{ext}")
    return response.json() if response.ok else []

def fetch_sequence(coord):
    ext_seq = f"/sequence/region/human/{coord}?content-type=text/plain"
    response_seq = requests.get(server+ext_seq)
    return response_seq.text if response_seq.ok else "N/A"

# Koordinatları oku
with open(coordinates_file, 'r') as file:
    coordinates = [line.strip() for line in file.readlines()]

results_data = []

for coord in coordinates:
    features = fetch_genomic_features(coord)
    sequence = fetch_sequence(coord)
    if features:
        for feature in features:
            feature_type = feature.get('feature_type', 'N/A')
            feature_id = feature.get('id', 'N/A')
            biotype = feature.get('biotype', 'N/A')
            start = feature.get('start', 'N/A')
            end = feature.get('end', 'N/A')
            results_data.append({
                'Region': coord,
                'Feature Type': feature_type,
                'Feature ID': feature_id,
                'Biotype': biotype,
                'Start': start,
                'End': end,
                'Sequence': sequence[:15]  # ilk 15 baz
            })
    else:
        # Gene denk gelmeyen bolgeler icin
        results_data.append({
            'Region': coord,
            'Feature Type': 'N/A',
            'Feature ID': 'N/A',
            'Biotype': 'N/A',
            'Start': 'N/A',
            'End': 'N/A',
            'Sequence': sequence[:15]  # ilk 15 baz
        })

# Sonucları DataFrame'e donustur ve TSV dosyasına kaydet
df = pd.DataFrame(results_data)
df.to_csv(output_file, sep='\t', index=False)

print(f"Results have been saved to {output_file}")

