input_file = "output_megalodon.txt"
output_file = "normalized_output_megalodon.txt"

# Dosyayı oku ve icerigi satırlara ayır
with open(input_file, "r") as f:
    lines = f.readlines()

# Baslık satırını al
header = lines[0].strip().split("\t")
new_header = header[:3]  # ilk uc sutunu koru

# Methylation_Average sutunlarını donustur ve yeni baslıkları ekle
for col in header[3:]:
    if "_Methylation_Average" in col:
        new_col = col.replace("_Methylation_Average", "")  # Sadece Methylation_Average kısmını cıkar
        new_header.extend([new_col + "_Nucleotide_Count", new_col + "_Methylation_Average"])

# Yeni baslık satırını yaz
output_lines = ["\t".join(new_header)]

# Verileri duzenle ve yeni satırlar olustur
for line in lines[1:]:
    data = line.strip().split("\t")
    new_data = data[:3]  # ilk uc sutunu koru
    for i in range(3, len(data), 2):
        nucleotide_count = data[i]
        methylation_average = float(data[i + 1])
        normalized_value = methylation_average / 100  # 0-1 arasına donustur
        new_data.extend([nucleotide_count, "{:.4f}".format(normalized_value)])
    output_lines.append("\t".join(new_data))

# Yeni verileri cıktı dosyasına yaz
with open(output_file, "w") as f:
    f.write("\n".join(output_lines))

print("Dosya duzenlendi ve normalize edildi:", output_file)
