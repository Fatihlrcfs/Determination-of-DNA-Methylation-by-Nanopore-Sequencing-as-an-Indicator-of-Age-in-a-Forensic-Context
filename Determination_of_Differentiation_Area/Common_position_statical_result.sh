# Common area selection for methods #

methods = ["deepsignal", "nanopolish", "megalodon", "remora"]
data = {}

for method in methods:
    file_name = f"sample_{method}.tsv"
    with open(file_name, "r") as infile:
        if method != "remora":  # Remora dosyasında baslık satırı yok, bu yuzden yalnızca diger dosyalar icin atlayın
            infile.readline()
        for line in infile:
            parts = line.strip().split("\t")
            chr, pos_start, pos_end, coverage = parts[0:4]
            methylation_str = parts[4] if method not in ["remora"] else parts[4]  # Remora icin dogru sutunu sec
            methylation = float(methylation_str)
            if method in ["megalodon", "remora"]:
                methylation /= 100
            key = (chr, pos_start, pos_end)
            if key not in data:
                data[key] = {}
            data[key][method] = methylation

# Ã‡ıktı dosyasını yazdırma kodu aynı kalabilir
output_file = "combined_common_results.tsv"

with open(output_file, "w") as outfile:
    # Baslık satırını yaz
    outfile.write("Chr\tPos_start\tPos_end\t" + "\t".join(methods) + "\n")

    # Her pozisyon icin bir satır yaz
    for key, values in data.items():
        if all(method in values for method in methods):  # Tum yontemler icin bu pozisyonda bir deger olup olmadıgını kontrol et
            chr, pos_start, pos_end = key
            methylation_values = [str(values.get(method, "NA")) for method in methods]
            outfile.write(f"{chr}\t{pos_start}\t{pos_end}\t" + "\t".join(methylation_values) + "\n")
